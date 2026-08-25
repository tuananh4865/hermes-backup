# 30-Minute Heartbeat Pattern (Orchestrator Heartbeat Cron)

Lightweight variant of the 6h routing audit, designed to fire every 30 minutes via the `Orchestrator Heartbeat` cron (`*/30 8-22 * * *` — daytime-only, 8am-10pm). Confirmed in 50+ sweeps since 2026-06-17.

## When to use this pattern

- Cron says "Orchestrator Heartbeat" / "30m heartbeat"
- Need liveness signal faster than 6h (stuck-task detection within ~2h window)
- Output must be SHORT (1-line summary + table — delivered via cron destination)
- Read-only sweep (NO writes to state.md — prevents sibling-collision with qa-agent's write-only hourly gate)

## Protocol (vs full 6h audit)

| Step | 6h audit | 30m heartbeat |
|------|----------|---------------|
| Read 5 active profile state.md files | ✅ full read | ✅ **tail read only** (last 50 lines) |
| Read qa-agent H<N> verdict | ✅ | ⚠️ optional (token economy) |
| `hermes cron list` sweep | ✅ | ✅ required |
| Handoff/pending `find` scan | ✅ | ❌ skip (qa-agent already does hourly) |
| Cross-validation with qa-agent | ✅ required | ⚠️ only if qa-agent is FRESH (<2h) |
| Write to operations-manager/state.md | ✅ full Audit Summary block | ❌ **read-only** (or light append) |
| Output format | Long-form audit + tables | **1-line summary + table** |

## Token-economy rule (CRITICAL)

**qa-agent/state.md is huge** (50KB-200KB+). On 30m cadence, full read hits the 100K char read limit and forces chunked reads — wasted context.

**Recipe:**
1. `find ~/.hermes/profiles -type f -name "state.md" -exec stat -f "%m %N" {} \;` — get mtime + path for all profiles
2. `read_file` qa-agent/state.md with `offset = total_lines - 100, limit = 100` — only the latest H rows
3. Skip reading coder/memory-curator/research-lead (no heartbeat-relevant activity)

For other profiles (operations-manager, engineering-lead, code-reviewer, security-engineer), full read is fine — they're typically <20KB each.

**⚠️ Bloat detection (added 2026-06-28):** if qa-agent/state.md >100K bytes, `read_file` will refuse the entire file. Workaround: `terminal: tail -120` to get the latest H rows. Full detection recipe + compaction trigger thresholds → `references/state-md-bloat-detection.md`. Surface a 🟡 BLOAT marker in the issues column when any file >100K.

## Output format (user-specified)

User explicitly requested: `1-line summary + table`. Example from H57 sweep:

```
**Heartbeat Summary**: 0 active · 0 stuck · 0 verified · 0 escalated · 18/18 crons healthy

| Profile | Last Update | State | Cron Health | Issues |
|---|---|---|---|---|
| qa-agent | 2026-06-27 13:00 (H57) | Healthy | ✅ Quality Gate 12:03 | None |
| engineering-lead | 2026-06-27 09:01 (daily) | Healthy | ✅ Code Health 09:01 | None — idle |
| operations-manager | 2026-06-27 12:02 (H34 sustained) | Healthy | ✅ Routing Audit 12:01 | None — H34 fully recovered |
| code-reviewer | 2026-06-27 12:01 (noon cron) | Healthy | ✅ PR Watcher 12:01 | None — no code to review |
| security-engineer | 2026-06-27 03:00 (daily) | CLEAN 8.7/10 | ✅ Vuln Scan 03:02 | 0 CRITICAL, 2 MEDIUM informational |
```

**Don't:**
- Add long bullet lists of cron statuses
- Repeat the same audit summary block operations-manager writes
- Add "## What Worked / ## What Failed" sections (those are profile state.md patterns, not heartbeat patterns)

## Read-only safety (sibling-collision prevention)

qa-agent's hourly gate **WRITES** to qa-agent/state.md via `patch()`. Heartbeat **READS** from state.md files. Different operations, no sibling-collision risk (collision only happens on concurrent writes to the SAME file).

**Safe to do in heartbeat:**
- `read_file` any profile state.md
- `find` scans
- `hermes cron list`
- `stat` mtime checks

**DO NOT do in heartbeat:**
- `patch` or `write_file` to ANY state.md (use operations-manager for state updates)
- Spawn subagents that write to state.md

## What to do when you find real issues

Heartbeat is detection-only. Actions:
- **0 stuck, 0 escalated, all crons ok** → just report the 1-line + table, done
- **1-2 stuck tasks** → mention in the issues column, NO routing decision (that's operations-manager's job)
- **Security CRITICAL** → mention in issues column, security-engineer auto-fixes per its own cron
- **Cron ERROR** → mention in issues column, ops-manager handles investigation on next 6h tick
- **2 agents touching same file** → mention in issues column, do NOT auto-resolve (operations-manager routing logic)

The heartbeat is a pulse, not a brain. Detect, surface, hand off.

### Exception: extreme-threshold nudge (added 2026-06-30, H78 heartbeat)

When a stuck task is found that exceeds the 2h threshold by **100× or more** AND a clear recovery path is documented (e.g. operations-manager's routing audit already classified it as Pattern A "run completed, artifact lost" with a "close-as-resolved" recommendation), the heartbeat MAY dispatch a `delegate_task` nudge to the owning profile rather than waiting for the next 6h audit.

**Why this exception exists:** A 31.6-day stuck task (t_3a73b0af, found 2026-06-30 12:00 by ops-manager 6h audit, re-confirmed 12:31 by H78 heartbeat) is functionally invisible to most sweeps and won't be auto-resolved by the kanban itself. Waiting 6h for the next ops-manager audit adds zero information — the situation is already known and triaged. Nudging immediately shortens recovery time from days to minutes.

**Threshold rule (codified 2026-06-30):**
- Stuck <2h → wait for 6h audit
- Stuck 2-48h → wait for 6h audit (still within tolerance for human handoff)
- Stuck >48h (100× over 2h baseline) → MAY nudge via `delegate_task` IF a concrete close-as-resolved path is documented
- Stuck >7d → SHOULD nudge (the task is almost certainly stale and the next user-facing reminder will be too late)

**Recipe:**
```python
delegate_task(
    goal="Nudge for <task_id>: <brief title> has been blocked <N.N>d. <recovery recommendation>. Take action: <specific step>.",
    context="Task ID: <id>. Kanban DB at <path>. Workspace path: <workspace>. <recovery context>. <one of two paths>. <don't re-do work, child artifacts exist>.",
    toolsets=["terminal", "file"],
)
```

**Anti-patterns:**
- DO NOT nudge when the recovery path is ambiguous (let ops-manager route)
- DO NOT nudge for <100× threshold (wait for the 6h audit, that's its job)
- DO NOT nudge for security CRITICAL — that's security-engineer's auto-fix path
- DO NOT nudge for cron ERRORs — let ops-manager investigate
- DO NOT include the original task brief in the nudge — just the recovery recommendation + child artifacts + specific action

**Real example (H78, 2026-06-30 12:31):** t_3a73b0af (YouTube niche research) blocked 31.6 days, owned by default. Ops-manager 12:00 audit already triaged as Pattern A with "close-as-resolved (research IS in run 24's summary)" recommendation. Heartbeat dispatched `delegate_task` with concrete close-as-resolved path + 3 child artifact paths. Delegation ID: `deleg_c01b2ae1`.

## CRITICAL-grep false-positive triage (H70 lesson, 2026-06-28)

When running the security CRITICAL check on heartbeat sweep, naive regex will produce false positives:

```bash
# This regex matches ALL of these, including ZERO-finding headers:
grep -lE 'CRITICAL|Severity.{0,3}9|Severity.{0,3}10' ~/.hermes/profiles/*/state.md
# Returns: operations-manager/state.md  (line 41: "### CRITICAL (0)" — header documenting ZERO CRITICAL findings)
#          qa-agent/state.md             (line 82: "0 CRITICAL findings, 0 escalations needed" — sweep verdict text)
#          security-engineer/state.md    (line 41: "### CRITICAL (0)" — section header)
```

**The false positive class:** profile state.md files use the literal string `### CRITICAL (0)` as a section header to document the COUNT of findings (which is zero). The security-engineer daily audit writes sections like `### CRITICAL (0)`, `### HIGH (0)`, `### MEDIUM (2)`, `### LOW (1)` — the grep regex `CRITICAL` matches the header even when the count is zero.

**Triage recipe (when grep returns matches):**

1. **Do NOT trust the match count as "N CRITICAL findings".** It includes zero-count headers.
2. **Run context grep** to see the actual matched lines: `grep -nE 'CRITICAL|Severity.{0,3}9|Severity.{0,3}10' <file> | tail -10`
3. **Classify each match:**
   - `### CRITICAL (0)` or `### HIGH (0)` → section header, ZERO findings, FALSE POSITIVE
   - `### CRITICAL (N)` where N>0, OR a line describing an unfixed CRITICAL → REAL FINDING
   - Inline text like "0 CRITICAL findings, 0 escalations needed" inside a verdict row → FALSE POSITIVE (it's the sweep conclusion, not a finding)
   - `Severity: 9` or `Severity: 10` annotation → REAL FINDING
4. **Cross-validate** with the security-engineer state.md `## Daily Vuln Scan` verdict line — it should explicitly state "CLEAN N.N/10" or list the actual CRITICAL/HIGH counts.

**Real test from H70 sweep (2026-06-28 ~10:00+07):** raw grep returned 3 files; after context inspection, all 3 were either `### CRITICAL (0)` headers or inline "0 CRITICAL findings" verdict text inside sweep rows. Security-engineer's daily audit at 2026-06-28 03:03:12 reported `CLEAN 8.7/10` with 0 CRITICAL / 0 HIGH / 2 MEDIUM (informational) / 1 LOW — no real findings.

**Add to your sweep:**
```bash
# After raw CRITICAL grep, always context-inspect:
grep -nE 'CRITICAL|Severity.{0,3}9|Severity.{0,3}10' ~/.hermes/profiles/*/state.md | head -20

# Then confirm with security-engineer daily verdict:
grep -E 'CLEAN|CRITICAL.*[1-9]' ~/.hermes/profiles/security-engineer/state.md | tail -3
```

This is distinct from the H10 handoff false-positive pattern (which is about file path `pending*`/`handoff*` matching static skill bundles). H70 is about CONTENT matching headers that document the ABSENCE of findings.

## Cron count ground-truth recipe (added 2026-06-29)

**Problem:** Cross-profile log drift on cron count is real and recurring. qa-agent's 12:00 H70 log wrote "**18 active crons, ALL healthy**" while operations-manager's same-day 12:00 audit (fired minutes later) wrote "**19 active crons, ALL healthy**". Both correct for their own sweep time — but the discrepancy is confusing for any reader comparing logs side-by-side.

**Why it happens:**
- qa-agent writes its H row at sweep start, with cron count snapshot from its own `hermes cron list` run a few seconds earlier
- A cron may have been added between the two sweeps (e.g. Orchestrator Weekly Cleanup was added ~2026-06-22; older H rows still cite 18)
- operations-manager's audit runs 6h later, sees the current count (19)

**The rule:** Always run `hermes cron list` fresh at sweep time. The count returned by that run IS the count to report. Never import a count from a prior sweep's log.

**Recipe:**
```bash
# Ground-truth cron count — run at sweep time
hermes cron list 2>&1 | grep -cE '^\s+[a-f0-9]{8,}\s+\[active\]'
# Whatever this returns is THE count. Report this number in the 1-line summary
# (e.g. "19/19 crons healthy") and in the per-profile cron-health table.
```

If a cross-check against qa-agent H<N> log shows a different number, the log is stale — NOT a fault. The fresh run wins.

## Cadence reality check

System has been **dormant since 2026-06-17** (~12.5+ days as of 2026-06-29). Heartbeat sweeps consistently return "0 active · 0 stuck · 0 verified · 0 escalated". This is NORMAL HEALTHY IDLE — not a fault. Per H44 cadence-decay rule, don't keep recommending "wake up the system" past 5+ sweeps.

## Pitfalls

- **DO NOT** full-read qa-agent/state.md on 30m cadence — token waste, will hit 100K char limit
- **DO NOT** write to any state.md file — sibling-collision risk with qa-agent's hourly gate
- **DO NOT** run handoff/pending find scan — qa-agent already does hourly
- **DO NOT** make routing decisions — heartbeat detects only, operations-manager routes
- **DO NOT** treat raw `CRITICAL` grep matches as findings — H70 false-positive: `### CRITICAL (0)` headers + inline "0 CRITICAL findings" verdict text both match the regex but document ZERO findings. Always context-inspect matches before declaring a CRITICAL finding.
- **DO NOT** cite a prior sweep's cron count — always run `hermes cron list` fresh. Cross-profile log drift causes count divergence (qa-agent older rows may say 18, operations-manager newer rows may say 19). The ONLY ground truth is a fresh run at sweep time.
- **DO** capture real-time cron fires (delta <60s) as supplementary evidence — strongest live-health signal
- **DO** cross-validate via qa-agent only when qa-agent is FRESH (<2h old)
- **DO** keep output to 1-line + table — user explicitly requested this format

## Related

- `../SKILL.md` — main routing-audit skill
- `references/cron-fault-taxonomy.md` — H38 ground-truth sweep
- `references/real-time-cron-fire-detection.md` — H56 technique for detecting live crons
- `~/.hermes/profiles/operations-manager/state.md` — 6h audit format (full version)
- `~/.hermes/profiles/qa-agent/state.md` — independent cross-validation source
