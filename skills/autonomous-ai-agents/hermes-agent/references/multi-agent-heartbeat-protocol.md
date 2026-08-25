# Multi-Agent Heartbeat Protocol (Orchestrator Sweep)

> Reference for orchestrator 30m heartbeat cron that monitors active specialist profiles.
> Distilled from 50+ sweeps of qa-agent state.md (H1-H51) and operations-manager audits.

## When to Use

- Running an **orchestrator 30m heartbeat** cron that needs to survey all active specialist profiles
- Need to detect stuck tasks, escalation needs, cron faults, or inter-agent conflicts
- Want a **reproducible 6-check protocol** that produces a 1-line summary + table

## Core Insight: H38 Recipe — Cron Truth > File Mtime

**The single most important rule for multi-agent health checks:**

> **File mtime tracks last WRITE. Cron `last_run` tracks last EXECUTION.**
> A clean cron run that finds "0 to report" may NOT rewrite state.md.
> Therefore: **always cross-reference `hermes cron list` last_run, not state.md mtime.**

### Anti-pattern (H28/H29/H34 false positive)

Tracking "multi-profile cron fault pattern" by mtime alone for 32+ sweeps. All 3 instances turned out to be measurement artifacts — crons WERE firing on schedule but state.md wasn't being rewritten because nothing changed.

### Correct pattern

```bash
hermes cron list  # ground truth: last_run, exit_status, error: annotations
```

If `last_run` is recent AND `exit_status` is `ok` AND no `error:` annotation → **HEALTHY regardless of mtime**.

## 6-Check Protocol (canonical sweep structure)

Each orchestrator sweep must check:

| # | Check | Source | Threshold |
|---|-------|--------|-----------|
| 1 | Tasks pending >2h | Per-profile state.md Active/Pending sections | 0 expected |
| 2 | Outputs awaiting qa-agent verification | `find ~/.hermes/profiles -type f \( -name "pending*" -o -name "handoff*" \)` | 0 expected |
| 3 | Security CRITICAL findings | security-engineer state.md Recent Audits | 0 expected; HIGH/MEDIUM may be informational |
| 4 | Agent conflicts (same file) | Cross-reference active tasks across profiles | 0 expected |
| 5 | Owner-authority auto-fix | security-engineer perm auto-fixes (644→600) | Apply if in scope |
| 6 | Escalations needed | Stuck tasks + CRITICAL findings + cron faults | 0 expected; pre-emptive nudge OK |

## Output Format (canonical)

```
1-line summary: 5 active profiles, 0 stuck, 0 conflicts, 0 escalations, 0 CRITICAL findings — system fully healthy and idle.

| Profile | Cron | Last Run (ground truth) | Status | Goal | Stuck | Pending QA | Notes |
|---|---|---|---|---|---|---|---|
| profile-name | Cron Name (schedule) | 2026-06-27 08:01:52 ✅ | HEALTHY | None | 0 | 0 | one-line context |
```

**Critical:** "Last Run" column = `hermes cron list` value, NOT file mtime.

## Reading Protocol (parallel batch)

Always read profile state.md files in **single parallel batch** (single tool message, multiple read_file calls). This is 5-10× faster than sequential reads and avoids token bloat from per-call overhead.

```python
# Pseudocode
read_file(path=qa-agent/state.md)
read_file(path=engineering-lead/state.md)
read_file(path=operations-manager/state.md)
read_file(path=code-reviewer/state.md)
read_file(path=security-engineer/state.md)
# All in same tool message
```

## Common False Positives (H5/H10/H38 triage recipes)

When scanning for `pending*`/`handoff*` files, these are KNOWN false positives:

| Match | Location | Why FP | Recipe |
|-------|----------|--------|--------|
| `wiki-independence-pending.md` | `coder/skills/hermes-github-backup/references/` | Static ref doc, mtime >30d | H5 recipe: recheck mtime + path under `references/` |
| `coder/skills/handoff/` directory | contains only `SKILL.md` | Static skill bundle, not task queue | H10 recipe: directory match with only docs = FP |
| `coder/skills/handoff/SKILL.md` | skill bundle | Same as above | H5 + H10 |

## Pre-File-Write Sibling Collision Check (H31/H40 recipe)

When writing to a state.md file that another agent might also be writing to (e.g., orchestrator 30m heartbeat + qa-agent hourly gate both writing to qa-agent/state.md), ALWAYS do a pre-append count check:

```bash
grep -cE "^\|{1,4} H[0-9]+ \|" state.md
```

If count > expected (e.g., expected 50, found 51), a sibling write happened between your dispatch and patch. Renumber your row to the next H-number and use a multi-line context anchor (last ~30 chars of prior row + literal `\n## Verdict History`) to avoid overwriting the sibling's row.

## Multi-Profile Cron Fault Pattern (H28/H29/H34 → RESCINDED)

Historical pattern: 3 "faults" tracked across 32+ sweeps based on mtime alone. **All 3 were false positives** per H38 truth-table recipe. Only do fault classification after cross-referencing `hermes cron list`.

Real fault example (research-lead, 2026-06-25 18:01:46):
```
hermes cron list → Research Lead Trend Scan → last_run 2026-06-25 18:01:46 → error: RuntimeError: Connection error + telegram delivery failed
```
This IS a real fault: 30h stale + explicit error annotation.

## Cron Grace Fast-Forward Pattern (H77/H78/H83 — ROOT CAUSE)

When `hermes cron list` shows a daily/6h cron with **stale `last_run`** (e.g., yesterday's date) but **`exit_status: ok` and no `error:` annotation**, this is **NOT a daemon fault** — it is the scheduler's documented recovery behavior.

**Smoking gun (verified 2026-06-30 21:00 sweep):**
```
~/.hermes/logs/agent.log → grep "missed its scheduled time":
2026-06-30 09:52:14,754 INFO cron.jobs: Job 'Hermes Autoresearch Nightly' missed
  its scheduled time (2026-06-30T07:00:00+07:00, grace=7200s).
  Fast-forwarding to next run: 2026-07-01T07:00:00+07:00
```

**What this means:**
- The Hermes cron scheduler has a `grace` window (default `7200s` = 2h for daily jobs; `900s` = 15min for heartbeat).
- If the gateway daemon was down/hung during a scheduled tick, the job is **skipped** when the daemon wakes up — NOT retried.
- The scheduler then **fast-forwards to the next scheduled run** (e.g., 07:00 missed → next run = 07:00 tomorrow).
- Result: cron shows `ok` + stale `last_run`. Output dir has no new file for that day. The job is NOT broken — it just skipped one cycle.

**Diagnostic recipe (3-step verification):**

```bash
# Step 1: Identify stale crons (last_run not today)
hermes cron list | grep "Last run:" | python3 -c "
import sys, datetime
today = datetime.date.today().isoformat()
for line in sys.stdin:
    if today not in line:
        print(line.strip())
"

# Step 2: Check the smoking gun in agent.log
grep -E "missed its scheduled time" ~/.hermes/logs/agent.log | tail -20

# Step 3: Verify output dir has no new file (corroborates skip, not silent failure)
for d in ~/.hermes/cron/output/*/; do
  count=$(find "$d" -name "$(date +%Y-%m-%d)_*" -type f 2>/dev/null | wc -l | tr -d ' ')
  echo "$(basename $d): $count files today"
done
```

**Classification rule for sweeps:**
| Smoking gun found? | Output dir empty today? | Daemon now alive? | Classification |
|---|---|---|---|
| Yes | Yes | Yes | **TRANSIENT daemon downtime** — no action, fast-forwarded to next tick |
| Yes | Yes | No | **ACTIVE outage** — restart gateway immediately |
| No | Yes | Yes | **Real fault** — investigate script/logic failure |
| No | No | Yes | HEALTHY |

**Daemon-downtime window detection (H83):** When 6+ jobs all share the same `missed` log entry timestamp (e.g., 02:00–07:30 window with no successful runs between), the daemon was likely down for that entire window. The first `missed its scheduled time` log entry timestamp tells you when the daemon came back up.

**Known fast-forward-prone windows (verify with daemon uptime):**
- 02:00–07:30 daily morning crons (Memory Curator, Wiki Forget, Wiki Health, Hermes Daily Backup, Hermes Autoresearch, Hermes Agent X Research)
- Any `0 */6 * * *` 6h-cadence cron (QA, Ops Manager) — these usually recover same-day via next 6h tick

**Action threshold:** If `missed its scheduled time` log shows the daemon is still down (no subsequent successful runs after wake-up), restart with: `launchctl kickstart -k gui/$(id -u)/ai.hermes.gateway` or `hermes gateway restart`.

## 18-Cron Registry Health Check (H38 full sweep)

When you want full registry health, capture all 18 active crons:

1. Hermes Daily Backup
2. Hermes Autoresearch Nightly
3. Hermes Agent X Research Daily
4. Hermes Daily Session Review
5. Wiki Health Daily
6. Wiki Memory Forget Daily
7. TikTok 5-Channel Nightly Monitor
8. Orchestrator Heartbeat
9. Orchestrator Daily Briefing
10. Orchestrator Nightly Reflection
11. Orchestrator Weekly Cleanup
12. QA Agent Quality Gate
13. Engineering Lead Code Health
14. Operations Manager Routing Audit
15. Code Reviewer PR Watcher
16. Security Engineer Vuln Scan
17. Memory Curator Nightly Consolidation
18. Research Lead Trend Scan

All should show `ok` exit_status and recent `last_run`. Any with `error:` annotation = real fault.

## H36 Clock Anomaly (cosmetic, not data corruption)

Some profiles' state.md `updated:` frontmatter field shows timestamps in the future (e.g., `2026-06-26T18:00:00` when system time is `2026-06-26 15:00`). This is **frontmatter drift, not a fault** — the actual file mtime and audit content are correct. Per H36 recipe: use file mtime + audit content timestamp, NOT frontmatter.

## Companion Skills

- `multi-agent-orchestrator` — full orchestrator role definition
- `multi-agent-heartbeat` — recurring health-pulse pattern
- `kanban-orchestrator` — decomposition + specialist routing
- `operations-manager-routing-audit` — cron that runs 6h routing audits

## Pitfalls

1. **Don't trust mtime alone** — always cross-reference `hermes cron list` (H38 lesson)
2. **Don't skip pending/handoff scan** — 0 expected, but false positives exist (H5/H10 recipes)
3. **Don't overwrite sibling writes** — pre-append count check before patch (H31/H40 recipe)
4. **Don't classify faults prematurely** — wait for `error:` annotation in `hermes cron list`
5. **Don't explain mechanism unless asked** — solution-first reporting (Solution First, Explanation Never rule)
6. **Token-economize when dormant** — for confirmed-idle systems, drop to 4 primary reads + spot-checks every 6th sweep (H22/H25 reduction recipe)
7. **Kanban DB schema — column is `assignee`, NOT `agent`** — querying `SELECT ..., agent, ... FROM tasks` fails with `no such column: agent`. Correct schema: `id, title, body, assignee, status, priority, created_by, created_at, started_at, completed_at, workspace_kind, workspace_path, branch_name, claim_lock, claim_expires, tenant, result`. Use `.schema tasks` first if uncertain.
