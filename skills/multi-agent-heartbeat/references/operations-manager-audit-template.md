# Operations-Manager 6h Routing Audit — Template

> Full template for the operations-manager variant of the multi-agent-heartbeat protocol.
> Source: 3 real audits on 2026-06-24 (06:00, 12:00, 18:00) by operations-manager.
> Companion to `multi-agent-heartbeat/SKILL.md` § "Operations-Manager variant".

## 1. Trigger detection (OOB prompt recognition)

The cron prompt matches one of these patterns → load the operations-manager variant:

| Pattern | Match |
|---|---|
| "Run 6h routing audit" | ✅ Direct |
| "Run Nh routing audit" | ✅ Direct (any N) |
| "Find tasks pending >Nh" | ✅ Stale metric |
| "Find tasks waiting <verifier> verification >Nh" | ✅ Stale metric |
| "Find idle agents (>Nh no activity)" | ✅ Idle metric |
| "Report: N stuck, N pending <QA>, N idle" | ✅ Exact format |
| "Update your state.md with routing log" | ✅ State persistence |

**Default false matches** (use qa-agent 30m protocol, not this variant):
- "30m heartbeat check" → qa-agent 30m
- "Read state.md of all N active profiles" → qa-agent 30m
- Generic "check the system" → qa-agent 30m

## 2. Pre-audit mtime check (one tool call, batches all profiles)

```bash
stat -f "%Sm %N" /Users/tuananh4865/.hermes/profiles/*/state.md 2>/dev/null
```

Output: 12-13 lines, one per profile, sorted by name. Cross-reference with `ls` to find any new profiles.

**Then read all state.md files in one parallel batch** (Step 1 of main skill).

## 3. Report format (REQUIRED — copy-paste template)

```markdown
## 🔍 6H ROUTING AUDIT — 2026-06-24 18:00 +07

**Scope:** 10 active profiles read (default + 9 specialist). 2 test-profile-runner (skipped, stale).

### 📊 HEADLINE NUMBERS
| Metric | Count | Status |
|--------|-------|--------|
| **Stuck tasks (>2h pending)** | **0** | ✅ Clean |
| **Pending QA verification (>1h)** | **0** | ✅ Clean |
| **Idle agents (>4h no activity)** | **8** | ⚠️ Expected (system dormant) |

### 👥 AGENT STATUS
**Active (2):**
- `default` — run #N @ HH:MM (cron session, passive bookkeeping)
- `qa-agent` — H<N> sweep @ HH:MM (N consecutive idle sweeps; 0 outputs awaiting verification)
- `operations-manager` — self, this audit (excluded from idle count per H17 convention)

**Idle 4h–24h (N):**
- `<profile>` — <HH:MM> (<N>h<MM>m ago) — <1-line reason>

**Idle >24h (N):**
- `<profile>` — <date> (<N>h+ ago) — <1-line reason>

### ✅ VERDICT
**System stable, no escalations needed.** <1-2 sentence summary citing dormant duration and 0-failure metrics>.

### ⚠️ PERSISTENT FINDINGS
1. **<qa-agent cadence>**: N consecutive idle sweeps, 0-pending pattern held N+ days. Recommend reducing qa-agent cron from hourly to 6h.
2. **<peer cron overdue>**: <profile> <cron-type> now <N>h overdue vs <schedule>. Persistent since <first-detected-sweep>. <Security/no-security> impact.

### 📝 STATE FILE
Updated `~/.hermes/profiles/operations-manager/state.md` with:
- `frontmatter`: goal + updated timestamp set to <ISO>
- New Routing Log entry for <datetime>
- New Audit Summary — <datetime> section
- Refreshed Profile Activity Matrix (N rows, <min-idle>→<max-idle> range)
```

## 4. State.md 4-patch sequence (in order)

### Patch 1 — Frontmatter

```yaml
---
profile: operations-manager
goal: 6h routing audit (cron YYYY-MM-DD HH:00)
updated: YYYY-MM-DDTHH:MM:00+07:00
loop_engineering: enabled
---
```

Anchor: the previous frontmatter block (unique by `goal:` line).

### Patch 2 — Routing Log entry (append)

Append a single new line to the `## Routing Log` section. Anchor on the previous Routing Log line.

```
- YYYY-MM-DD HH:00: 6h routing audit (cron). **N stuck, N pending QA, N idle (>4h).** Cross-validated with qa-agent H<N> (HH:MM, Ng ago — N consecutive idle sweeps, 0 outputs awaiting verification). default active (run #N, HH:MM). Previous audit was Nh ago (HH:MM) — on cadence. [Structural-truth check line] No active tasks, no handoffs, no escalations needed. [Persistent finding 1 line]. [Persistent finding 2 line].
```

**Length target:** 1-3 lines (300-600 bytes per entry). The 06:00 entry is short (300 bytes), 12:00 entry is medium (450 bytes), 18:00 entry is verbose (650 bytes) — all 3 are valid shapes.

### Patch 3 — Audit Summary section (insert after previous summary)

```
## Audit Summary — YYYY-MM-DD HH:00 (cron 6h)
**Scope:** N profiles (default + N specialist) + N test-profile-runner (skipped, stale)
**Stuck tasks (>2h pending):** N
**Pending QA verification (>1h):** N
**Idle agents (>4h no activity):** N (<profile> <Nh+>, <profile> <Nh+>, ...)
**Active agents:** N (<profile> — <signal>; <profile> — <signal>)
**Verdict:** System idle since <date> multi-agent experiment (now Nh+ dormant). [No routing failures / Routing failed for X]. [No escalations needed / Escalate to user for Y].
**Notes:** <1-3 sentences covering cadence health, persistent issues, security regression watch if any>.
```

### Patch 4 — Profile Activity Matrix (full table replace)

```
## Profile Activity Matrix
| Profile | Last Update | Idle | Notes |
|---------|-------------|------|-------|
| default | YYYY-MM-DD HH:MM | ~Xm | ACTIVE (cron session) |
| qa-agent | YYYY-MM-DD HH:MM | ~Xh | ACTIVE (H<N> sweep, N idle consecutive) |
| operations-manager | YYYY-MM-DD HH:MM | 0h | ACTIVE (self — this audit) |
| code-reviewer | YYYY-MM-DD HH:MM | ~Xh | IDLE |
| engineering-lead | YYYY-MM-DD HH:MM | ~Xh | IDLE (last maker work; <cron> daily report only) |
| content-director | YYYY-MM-DD HH:MM | ~Xh | IDLE |
| research-lead | YYYY-MM-DD HH:MM | ~Xh | IDLE |
| security-engineer | YYYY-MM-DD HH:MM | ~Xh | IDLE (<N>h overdue — cron fault) |
| coder | YYYY-MM-DD HH:MM | ~Xh | IDLE |
| memory-curator | YYYY-MM-DD HH:MM | ~Xh | IDLE |
```

**Sort order:** ACTIVE first (default → qa-agent → self), then IDLE 4h-24h, then IDLE >24h. Test profiles excluded.

## 5. Cross-validation language (exact phrasing)

When the qa-agent ran in the last 2h, use this phrasing in the Routing Log:

```
Cross-validated with qa-agent H<N> (HH:MM, Xh ago — N consecutive idle sweeps, 0 outputs awaiting verification). default active (run #N, HH:MM). Previous audit was Xh ago (HH:MM) — on cadence.
```

**If qa-agent is >2h stale, replace with:**

```
qa-agent 6h audit at YYYY-MM-DD HH:MM is Xh old (past 2h freshness window) → RE-DERIVED from primary reads: all N profiles Goal=None, handoff/active/pending/blocked tables empty.
```

## 6. Real audit shapes (canonical examples)

### 06:00 audit (1st audit after 30h gap)

```
- 2026-06-24 06:00: 6h routing audit (cron). 0 stuck, 0 pending QA, 8 idle (>4h). qa-agent last sweep H8 at 05:00 (1h ago — within threshold). default profile last active 05:01 (1h ago). Previous ops-manager audit was 30h ago — overdue, this audit closes the gap. No active tasks, no handoffs, no escalations needed.
```

### 12:00 audit (healthy cadence, cross-validation works)

```
- 2026-06-24 12:00: 6h routing audit (cron). **0 stuck, 0 pending QA, 8 idle (>4h).** Cross-validated with qa-agent H15 (11:00, 1h ago — 15 consecutive idle sweeps, 0 outputs awaiting verification). default active (run #554, 11:34). Previous audit was 6h ago (06:00) — on cadence. No active tasks, no handoffs, no escalations needed. System dormant 165h+ since 2026-06-17 multi-agent experiment. qa-agent cadence reduction (hourly→6h) recommendation now at 15 sweeps — should be actioned.
```

### 18:00 audit (2nd healthy cadence, structural-truth check included)

```
- 2026-06-24 18:00: 6h routing audit (cron). **0 stuck, 0 pending QA, 8 idle (>4h).** Cross-validated with qa-agent H22 (17:00, 1h ago — 22 consecutive idle sweeps, 0 outputs awaiting verification). default active (run #602, 17:33). Previous audit was 6h ago (12:00) — on cadence. Structural-truth check: `ls -d profiles/*/pending profiles/*/handoffs` EMPTY; only FP is `coder/skills/handoff` (skill bundle, mtime 2026-05-19). No active tasks, no handoffs, no escalations needed. System dormant 174h+ since 2026-06-17 multi-agent experiment. security-engineer mtime 2026-06-24 03:02 (14h59m ago — daily scan now ~9h overdue vs 24h schedule; persistent cron fault since H12). qa-agent cadence reduction (hourly→6h) recommendation now at 22 sweeps — URGENT.
```

## 7. Common pitfalls (observed in real audits)

### Pitfall 1 — Frontmatter goal not updated

Symptom: `goal:` field still says previous audit's datetime. Fix: Always update both `goal:` and `updated:` in Patch 1.

### Pitfall 2 — Profile Activity Matrix not refreshed

Symptom: Previous audit's mtime still in the matrix (e.g. "12:00" stays in next audit). Fix: REPLACE entire table in Patch 4, don't append rows.

### Pitfall 3 — Cross-validation language drift

Symptom: Phrasing varies wildly between audits (e.g. "qa-agent last seen" vs "qa-agent H22 ran"). Fix: Use the exact pattern in §5.

### Pitfall 4 — Self included in idle count

Symptom: Report says "9 idle" instead of "8 idle" because operations-manager's own 6h age is included. Fix: Explicitly exclude self per the template (`operations-manager — self, this audit (excluded from idle count per H17 convention)`).

### Pitfall 5 — Persistent findings repeated verbatim across audits

Symptom: "qa-agent cadence reduction URGENT" appears in 10+ consecutive Routing Log entries. Fix: Track escalation count ("now at 22 sweeps"), but don't restate the recommendation every time. Reference the structural finding once, then track count.

## 8. Verification after audit (QA gates)

After completing the 4 patches:

1. **Stat check**: `stat -f "%Sm %z bytes" ~/.hermes/profiles/operations-manager/state.md` — mtime should be within 1 minute of now, file should have grown by ~500-1500 bytes.
2. **Lint check**: `head -1` returns `---` (frontmatter starts correctly).
3. **Routing Log check**: `grep -c "^- " ~/.hermes/profiles/operations-manager/state.md` — should be N+1 where N is previous count.
4. **Matrix check**: `grep -c "^| \(default\|qa-agent\|operations-manager\|code-reviewer\|engineering-lead\|content-director\|research-lead\|security-engineer\|coder\|memory-curator\) |" ~/.hermes/profiles/operations-manager/state.md` — should equal 10 (no test profiles).
5. **Section check**: `grep -c "^## Audit Summary" ~/.hermes/profiles/operations-manager/state.md` — should be N+1 where N is previous count.

If any check fails, fix in-place before emitting the report.

## 9. When to NOT do this audit (skip conditions)

- **OOB prompt is generic and not specifically a routing audit** → use qa-agent 30m protocol
- **Single profile needs attention** → use that profile's own watcher (engineering-lead daily check, code-reviewer noon watch, etc.)
- **No active profiles to read** (e.g. only `_template` exists) → emit a 1-line "no profiles provisioned" report, skip the audit
- **Audit requested by user mid-conversation** (not cron) → still follow the protocol, but mention "ad-hoc audit (not cron)" in the report header

## 10. Self-overdue recovery (54h+ gap, the audit IS the recovery)

When the audit fires 24h+ after the previous one (e.g. 54h gap on a 6h cadence = 9 ticks missed), the audit is the **recovery action** — not a heartbeat to be skipped.

**Hard rule:** Do NOT apply H26 silent-kill mode to operations-manager's own state.md updates. The audit MUST run + 4-patch sequence MUST execute, even though the system is deeply idle.

**Self-overdue audit recipe:**

1. **Compute gap**: `gap_hours = (now - previous_audit_iso) / 3600` and `ticks_missed = ceil(gap_hours / cadence_hours)`. Report both in the Routing Log and the Audit Summary header.

2. **Patch 1 (frontmatter)**: Update `goal:` and `updated:` as normal. The `updated:` timestamp is the recovery timestamp.

3. **Patch 2 (Routing Log)**: Cite the gap explicitly. Example:
   ```
   - 2026-06-25 06:00: 6h routing audit (cron). 0 stuck, 0 pending QA, 8 idle (>4h). System remains dormant ~225h (9.4 days) since 2026-06-17 multi-agent experiment. cron gap: this audit is 54h late vs expected 6h cadence (2026-06-23 00:00 → 2026-06-25 06:00 = 9 ticks missed). Per H8 qa-agent observation: same multi-profile cron fault pattern as code-reviewer (H28) and security-engineer (H29).
   ```

4. **Patch 3 (Audit Summary)**: Include the gap in the Verdict line:
   ```
   **Verdict:** System idle since 2026-06-17 multi-agent experiment (~9.4 days). No routing failures. No escalations needed. **This audit closes a 54h ops-manager cron gap.**
   ```

5. **Patch 4 (Profile Activity Matrix)**: Add a note for the `operations-manager` row: `ACTIVE (self — this audit closes 54h cron gap)`.

6. **Add `## Pending/Handoff Scan (<date>)` section** (new — see §11). This is a structural-truth record of `pending*`/`handoff*`/`inbox`/`queue` directories and `pending*` files. Catches real work vs skill bundle false positives.

**Why this matters:** the audit is the only signal that breaks the silence. If the audit itself is skipped (H26-misapplied), the cron-fault pattern goes unrecorded and the system never gets diagnosed. The audit's value in this case is not the metrics (still 0 stuck, 0 pending, 8 idle — same as last time) but the **gap record** that proves the cron is broken.

**Real 2026-06-25 06:00 outcome:** 4 patches clean, state.md 3051 → 3711 bytes (+660 bytes for one audit card). Routing Log recorded the 9 ticks missed. Pending/Handoff Scan section added. qa-agent H8 cross-validation confirmed 0 outputs awaiting verification.

### 10a. Drift-Recover-Drift oscillation (NEW, 2026-06-26)

**Pattern observed 2026-06-25 06:00 → 2026-06-26 12:00:** ops-manager cron recovered after the 54h gap (H10 FRESH at 07:01) but then drifted again across sweeps H11 (2h) → H13 (15h) → H21 (23h) → 2026-06-26 12:00 (30h, 5 ticks missed).

**Anti-pattern:** once you've seen a profile recover, do NOT remove it from the `Multi-Profile Cron Fault Pattern (Tracking)` table inside state.md. Drift-oscillating profiles are MORE dangerous than persistently broken ones — they create false confidence ("cron was fine 6h ago, must be a one-off").

**Recommended Status taxonomy for the tracking table:**

| Status | Meaning | Example |
|---|---|---|
| `PERSISTENT` | Never recovered | code-reviewer (H28) |
| `WITHIN TOLERANCE` | Long cadence, single missed tick is normal | security-engineer (H29, daily sweep) |
| `DRIFT-OSCILLATING` | Recovered then drifted again | operations-manager (H34) |

Full detection recipe + macOS root-cause checklist in `references/multi-profile-cron-fault-pattern.md`.

## 11. Pending/Handoff Scan (new in v1.5.0, 2026-06-25)

A new subsection in the Audit Summary (or as a stand-alone section) that records the structural-truth check for `pending*` and `handoff*` artifacts. Closes the false-positive gap (e.g. `coder/skills/handoff` is a skill bundle, not a queue).

**Required commands (run during the audit):**

```bash
# 1. Find any pending* or handoff* directories
find ~/.hermes/profiles -type d \( -name "pending*" -o -name "handoff*" -o -name "inbox" -o -name "queue" \) 2>/dev/null

# 2. Find any pending* files
find ~/.hermes/profiles -type f -name "pending*" 2>/dev/null

# 3. Triage each match:
#    - Under skills/*/ or references/*/ = FALSE POSITIVE (documentation, not queue)
#    - Under profiles/<name>/ with mtime <7 days = REAL (live queue item)
#    - Under profiles/<name>/ with mtime >7 days = STALE (consider archiving)
```

**Section template (add to state.md after Audit Summary):**

```markdown
## Pending/Handoff Scan (YYYY-MM-DD HH:MM)
- `find profiles -type d -name "pending*" -o -name "handoff*" -o -name "inbox" -o -name "queue"`: N matches
  - `<path>` — <FP/REAL/STALE>: <1-line reason>
- `find profiles -type f -name "pending*"`: N matches
- **Conclusion:** N tasks awaiting QA verification across all N active profiles. <qa-agent H<N> cross-validation: yes/no>.
```

**Real 2026-06-25 06:00 example:**

```markdown
## Pending/Handoff Scan (2026-06-25 06:00)
- `find profiles -type d -name "pending*" -o -name "handoff*" -o -name "inbox" -o -name "queue"`: 1 match
  - `coder/skills/handoff/` — FALSE POSITIVE: contains only `SKILL.md` doc (May 19, 2026), NOT a task queue
- `find profiles -type f -name "pending*"`: 0 matches
- **Conclusion:** 0 tasks awaiting QA verification across all 10 active profiles. qa-agent H8 sweep at 2026-06-25 05:01 confirms this independently.
```

**Why a new section (not just a row in Routing Log):** Pending/handoff status is a structural property of the system, not a per-audit event. Recording it as a stand-alone section makes it queryable across audits (e.g. "show me all audits where pending count > 0").
