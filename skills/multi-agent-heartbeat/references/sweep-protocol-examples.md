# Sweep Protocol Examples

> Concrete sweep outputs across the 4 most common heartbeat scenarios. All examples are from the 2026-06-23/24 multi-agent heartbeats (H1-H15) on a 10-profile Hermes installation.

## Example 1 — Idle system, all queues empty (H15 — the canonical pattern)

**Trigger:** Orchestrator 30m cron at 11:00, all 5 active profiles read in parallel.

**Report emitted:**

```
## Orchestrator 30m Heartbeat — 2026-06-24 11:00 (UTC 04:00)

**1-line summary:** System idle & stable, 0 stuck / 0 pending / 0 conflicts / 0 escalations; 15 consecutive idle sweeps in qa-agent log, ops-manager + security-engineer cron overdue (4-8h) — recommend cron audit.

| Profile | State | Last Activity | Idle | Verdict |
|---|---|---|---|---|
| **qa-agent** | Goal=None, handoff queue empty | 11:01 (H15 self) | 0h | ✅ ACCEPT — 0 outputs awaiting verification |
| **engineering-lead** | Goal=None, daily health check done | 09:05 (09:00 cron) | 1h55m | ✅ ACCEPT — operational report, no QA work produced |
| **operations-manager** | Goal=None, all queues empty | 06:01 (06:00 audit) | 4h59m | ⚠️ **cron overdue** — next 6h tick was due 12:00, now 1h past |
| **code-reviewer** | Goal=None, no reviews since | 2026-06-17 10:36 | 171h+ | ✅ DORMANT — 0 conflicts |
| **security-engineer** | Last sweep CLEAN 8.5/10 | 2026-06-23 03:03 | 32h | ⚠️ **daily scan overdue** ~8h — cron not firing on schedule |
```

**Key signals in this example:**
- 1-line summary mentions escalation flag (cron overdue) but the verdict is still ACCEPT overall
- Table mixes ✅ and ⚠️ — ⚠️ is for cron cadence, not for actual issues
- Profile table includes 3 columns of context (State, Last Activity, Idle) so a 2nd reader can interpret without re-reading state files

## Example 2 — One specialist active, others idle (H13)

**Trigger:** Hourly sweep at 10:01, engineering-lead ran its 09:00 daily cron.

**What changed since H12:**
- engineering-lead state.md mtime: 2026-06-24 09:05:29 (was 2026-06-17 10:20)
- New section: `## Daily Code Health Check — 2026-06-24 09:00 (cron)`
- Engineering-lead's Handoff History still empty (cron output is operational, not a handoff)

**Verdict logic:**
- engineering-lead activity = **operational report** (git status, test counts, /tmp cleanup) → does NOT produce a QA-verifiable handoff
- 0 outputs awaiting qa-agent verification despite engineering-lead's first activity in 7 days
- Verdict: ACCEPT (system is functioning, cron is delivering, just nothing for QA to verify)

**Lesson:** Not all "activity" is a "handoff". Daily cron reports are operational telemetry, not work products. Distinguish in the sweep row.

## Example 3 — Security regression + auto-fix (H11)

**Trigger:** 30m heartbeat at 08:31, immediately following a default-profile config write.

**Detection:**
```bash
$ stat -f "%Sp" ~/.hermes/config.yaml
-rw-r--r--  # 644 — REGRESSION
# Expected: -rw------- (600)
# Last known good: 2026-06-24 08:00 (H10, confirmed 600)
# mtime 2026-06-24 08:18:23 (13 min before sweep)
```

**Root cause:** default-profile config write at 08:18 during the 8:01-8:30 run burst — `chmod 600` was lost when config was rewritten.

**Auto-fix per security-engineer owner authority:**
```bash
chmod 600 ~/.hermes/config.yaml
# Verify
stat -f "%Sp %N" ~/.hermes/config.yaml
# -rw-------  /Users/tuananh4865/.hermes/config.yaml ✅
```

**Report row:**
> "1 SECURITY REGRESSION DETECTED + AUTO-FIXED: `~/.hermes/config.yaml` regressed from 600→644 between H10 (08:00, confirmed 600) and H11 (08:31, mtime 13 min before sweep). Root cause: default-profile config write at 08:18. Auto-fixed per security-engineer owner authority (LOW severity, reversible perm tightening): `chmod 600` → verified `-rw-------`."

**Re-verification on H12, H13, H14, H15:** Config still at 600 — auto-fix stable, no drift.

**Lesson:** After a perm auto-fix, RE-VERIFY on subsequent sweeps. Don't claim "fixed" once and forget.

## Example 4 — Cadence trigger escalation (H9)

**Trigger:** Hourly sweep at 07:00, 9th consecutive idle.

**Cadence trigger accumulation:**
- H1-H8: 0-pending pattern held
- H9: 9 consecutive idle sweeps
- Recommendation threshold: 7+ → "recommend reducing qa-agent cron from 1h→6h"

**Co-trigger condition (H9 onwards):**
- ops-manager 6h audit cadence: 30h+ behind (last 2026-06-23 00:00, now past expected 12:00 next tick)
- This is NOT just qa-agent over-firing — it's a system-wide cron delivery issue

**Report row:**
> "CADENCE TRIGGER FIRED AGAIN: 9 consecutive idle sweeps (H1-H9) — recommendation to reduce qa-agent cron from hourly to 6h now STRONGER (9 idle sweeps, 0-pending pattern held 7+ days, ops-manager audit cadence itself overdue at 30h gap)."

**Lesson:** When cadence trigger fires AND another specialist's cron is also overdue, escalate as system-wide cron audit, not just one cron adjustment.

## Example 5 — Pre-append integrity check (H8)

**Trigger:** Hourly sweep at 05:00, after the H6 file reset incident.

**Pre-append check (manual):**
```bash
# Read last 5 rows
grep "^| H" ~/.hermes/profiles/qa-agent/state.md | tail -5
# Expected: each row matches | H<N> | <ISO> | ...
# Observed: H8 row had || H (double-pipe prefix) — corrupted by previous patch attempt
```

**Decision:** Document the corruption in the new H9 row's note, append H9 in clean format. Don't try to edit history.

**Lesson:** When the file is corrupted, append-only is still the rule. New rows must be clean even if old rows are not.

## Example 6 — Single-profile code/PR watcher (the noon PR watcher pattern)

**Trigger:** Noon cron targeted at `code-reviewer` profile with watch paths `~/.hermes/*/code/` and `/tmp/el-test/`. Other profiles NOT in scope.

**What this watcher is NOT:** Not a multi-profile sweep. Not a health check on other profiles' queues. Just: "are there new Python files dropped into the watch paths since last run?"

**Protocol:**
1. **ls/glob the watch paths** — empty result = 0 files to review, not a failure.
2. **Distinguish empty vs missing** — `ls -la` returns 2 lines (header + dir) for empty dir, error for missing. `/tmp/el-test/` missing ≠ "0 files" — it's a CONVENTION ALERT.
3. **Optional bonus scan** — `find ~ -name "*.py" -newer <last_run_marker> -not -path "*/node_modules/*" ...` to catch files dropped outside watch paths. Cheap insurance.
4. **Update state.md** — append row to the profile's `## Recent Reviews` table with verdict NO-OP if empty, file list + verdict per file otherwise.
5. **Report** — short (≤40 lines): scan paths + counts + state update confirmation. NO need to repeat full multi-profile protocol checks (1)-(6).

**Sample report (real, 2026-06-24 noon):**

```
# 🔍 Noon PR/Code Watcher — Report 2026-06-24 12:00

## Summary
- Files reviewed: 0
- Approved: 0
- Changes requested: 0

## Scan Results
| Watch path | Status |
|---|---|
| ~/.hermes/*/code/ | ❌ Missing — no code/ subdir in 14 profiles |
| /tmp/el-test/ | ❌ Missing — directory does not exist |

## State Updated ✅
File updated: ~/.hermes/profiles/code-reviewer/state.md
- updated: 2026-06-17T10:35:00 → 2026-06-24T12:00:00
- New NO-OP row in Recent Reviews
```

**Key signals in this example:**
- The watcher is INTENTIONALLY narrow — only checks 2 paths, doesn't sweep everything
- Missing paths = convention alert, but verdict is still ✅ ACCEPT (no work to do)
- Report is much shorter than a full multi-profile heartbeat (≤40 lines vs ≤80)
- Note section to user: "if convention is dead, either re-define paths or skip cron" — gives user actionable next-step

**Lesson:** Single-profile watchers are a DIFFERENT protocol from multi-profile sweeps. Don't conflate them. A 6-axis code review on 0 files is still NO-OP, not failure.

## Example 7 — Watcher path convention is dead (the convention-alert pattern)

**Trigger:** N-th consecutive run where watch paths are missing/empty.

**When this fires:**
- 1st run: log as NO-OP, note convention may be dead
- 3rd consecutive: flag in heartbeat report as "watcher convention drift"
- 7th+ consecutive: recommend deprecating the cron OR updating watch paths

**Pattern (2026-06-24):** Watch paths `~/.hermes/*/code/` and `/tmp/el-test/` set up 2026-06-17 for code-reviewer reviewer, but 7 days later = 0 files ever dropped in either path. Convention likely dead.

**Action when detected:**
- DO NOT keep emitting NO-OP reports indefinitely
- After 3+ consecutive NO-OPs on missing paths, FLAG to user with 2 options:
  1. Update watch paths to match current convention
  2. Pause/disable the cron
- Include in escalation section of the next multi-profile sweep

**Verdict:** ACCEPT (no real work to do) but with ESCALATION flag (cron may be obsolete).

**Lesson:** Distinguish "system idle because no work submitted" (genuine ACCEPT) from "watcher convention is dead" (ACCEPT + ESCALATION). The latter needs user action or it burns tokens forever.

## Format cheatsheet

| Section | Length | Purpose |
|---|---|---|
| Title (1-line) | 1 line | What time, what protocol |
| 1-line summary | 1 sentence | State of system + key flags |
| Profile table | 5-10 rows | Per-profile status at a glance |
| Checks (1)-(6) | 6 bullets | Confirm protocol was followed |
| Escalation flag | 0-3 lines | Non-blocking concerns |

**Total: ~50-80 lines.** Anything longer → chunk per loop-engineering-deployment's "Report Length Discipline".
