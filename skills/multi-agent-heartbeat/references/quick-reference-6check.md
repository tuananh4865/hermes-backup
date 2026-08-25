---
name: quick-reference-6check
description: 1-screen cheat sheet for the 30m heartbeat cron — 6+1 mandatory checks (parallel read, H38 cron truth, stuck tasks, pending QA, security perms, agent conflicts, V23+V24 kanban DB verification). Load BEFORE any heartbeat sweep; deep-dive recipes live in the parent multi-agent-heartbeat SKILL.md.
type: reference
applies-to: [multi-agent-heartbeat, operations-manager-routing-audit]
severity: reference
---

# 6+1-Check Heartbeat Quick Reference

> **Distilled from the full `multi-agent-heartbeat` skill.** Use this as a 1-screen
> cheat sheet when running the orchestrator 30m heartbeat cron. The full SKILL.md
> has the long-form recipes, edge cases, and post-mortems; this file has the
> minimum-viable protocol that produces a correct report in <3 minutes.

## When to use this

- Cron prompt matches: "30m heartbeat", "Nh heartbeat", "read state.md of all N profiles"
- All checks below return 0 → deliver 1-line summary + table, exit
- Any check returns >0 → load the full `multi-agent-heartbeat` skill for the matching pitfall

## The 7 Checks (executed in order)

### Check 1 — Parallel batch read (mandatory first)

```bash
# Read all 5 active profile state.md files in ONE parallel batch
for p in qa-agent engineering-lead operations-manager code-reviewer security-engineer; do
    read_file("~/.hermes/profiles/$p/state.md")
done
```

**Why parallel:** 5x latency reduction. Independent reads MUST be batched.

**What to capture per profile:** `goal:`, `updated:`, Active/Pending/Blocked Tasks
tables, last Run History entry.

**Token-economy note (added Validation 4, 2026-06-27):** qa-agent state.md can
exceed 50KB after H1-H66 history. Use `read_file(path=..., limit=80, offset=1)`
to read only frontmatter + Active/Pending/Blocked tables + last verdict row.
The middle (long verdict history rows) is not needed for heartbeat decisions —
only the summary tables matter. Other 4 profile state.md files are <25KB each,
full read is fine.

### Check 2 — H38 Cron Truth Sweep (the only check that matters for fault classification)

```bash
hermes cron list 2>/dev/null | grep -B 1 -A 5 "Last run"
```

**⚠ Pagination gotcha (V13/V20):** `hermes cron list` outputs 18 crons in a
boxed layout. `head -100` cuts off at ~10 crons. Use `grep -cE "Last run:.*ok"`
for the count, then full output only if you need to investigate. The V10 JSON
recipe (`sqlite3 ~/.hermes/cron/jobs.json` after schema inspection) is the
durable fix when you need cron truth at a glance.

**Decision matrix:**

| `hermes cron list` result | State.md mtime | Verdict |
|---|---|---|
| `Last run: <recent>  ok` | stale or recent | ✅ HEALTHY |
| `Last run: <stale>  error` | any | ❌ REAL FAULT |
| `Last run: <stale>  ok` | any | ⚠️ **MISSED TICK (V26)** — scheduler gap, not job failure; age > schedule's natural interval (1h `*/30` / 7h `*/6` / 25h daily) |
| Not in registry | any | ⚠️ IDLE (no cron scheduled) |

**V26 missed-tick detection** (apply on every heartbeat — recipe in `references/v26-ok-but-stale-missed-tick.md`): `hermes cron list` records only `last_run` + `last_exit_status`, not `next_expected_run`. A daily cron with `last_run: 2026-06-29  ok` and current time `2026-06-30 17:02` is a 25h-stale missed tick — distinct from "ok" (healthy) and "error" (failed). Common cause in Tuấn Anh's setup: Mac sleep during 02:00-08:00 silently skips jobs in that range; recovery is automatic at next natural fire. Only intervene with `hermes cron run <id>` if user explicitly wants today's missed output.

**V27 pmset root-cause (apply when V26 fires with multiple contiguous missed ticks — recipe in `references/v26-ok-but-stale-missed-tick.md`):** run `pmset -g log | grep "<date> 0[window]:"` to confirm `PrevIdle` state during the missed window. Real H78 case (2026-06-30 02:00-07:30): Mac in `PrevIdle`, `Hermes Daily Backup` fired at 03:05 because backup scripts wrap `pmset noidle`; the other 5 missed crons don't have wake-from-sleep handling. Cron daemon's `grace=7200s` patience window fast-forwards missed jobs to next natural fire automatically — no manual `hermes cron run <id>` needed. If V26 + V27 both fire → root cause is Mac sleep, do NOT escalate as a Hermes fault.

**Do NOT classify as fault based on state.md mtime alone.** The H38 lesson:
"0 findings" cron runs don't always rewrite state.md, so mtime can lag cron
by hours. The 32-sweep false-positive cascade (H28/H29/H34) was caused by
exactly this — mtime-as-proxy classification reinforced across dozens of sweeps.

### Check 3 — Tasks pending >2h (stuck detection)

For each profile, look at `## Active Tasks` + `## Pending Tasks` + `## Blocked Tasks`
tables from the parallel read in Check 1. Count entries with `Started` or
`ETA` >2h ago. If all tables are empty → 0 stuck.

### Check 4 — Outputs awaiting qa-agent verification

```bash
find ~/.hermes/profiles -type f \( -name "pending*" -o -name "handoff*" \) \
    2>/dev/null | head -20
find ~/.hermes/profiles -type d \( -name "pending*" -o -name "handoff*" \
    -o -name "inbox" -o -name "queue" \) 2>/dev/null | head -20
```

**Triage:** paths under `skills/` or `references/` are documentation bundles
(FP). Paths under `profiles/<name>/` with mtime <7 days are live queues (REAL).
The `coder/skills/handoff/` directory is the most common FP — it's a static
skill bundle, not a task queue.

### Check 5 — Security CRITICAL findings (H11/H24 perm regression watch)

```bash
find ~/.hermes -maxdepth 3 \( -name "*.env" -o -name "auth.json" \
    -o -name "config.yaml" -o -name "*.db" \) -not -path "*/node_modules/*" \
    -not -path "*/.venv/*" -not -path "*/state-snapshots/*" 2>/dev/null | \
while read f; do
    mode=$(stat -f "%Lp" "$f")
    if [ "$mode" != "600" ] && [ "$mode" != "700" ]; then
        echo "REGRESSION: $mode $f"
    fi
done
```

**Auto-fix authority:** if file contains no plaintext secrets, `chmod 600`
is reversible + LOW severity → auto-fix without user approval. Pre-check
with `grep -E "api_key|secret|token|password"` for literal `sk-cp-...` or
`ghp_...` strings → STOP and escalate if found.

### Check 6 — Agent conflicts (2 agents on same file)

For each pair of profiles, check if both have non-empty Active Tasks with
overlapping file paths. In a dormant system this is 0. In a busy system,
apply the priority matrix from the full skill: severity > reversibility >
cost > deadline.

### Check 7 — Kanban DB vs log mtime (V23 + V24, MANDATORY when ops-manager flags stuck)

Ops-manager's 6h audit can report "1 STUCK task" by reading
`kanban/logs/<id>.log` mtime. The log is a session transcript — NOT task
status. A task can be `done` in DB for weeks while its log file still shows
the original "artifact lost, what do you want to do?" prompt. The DB itself
can also lie — a parent-task auto-completion can flip status to `done` even
when the recorded artifact path is empty on disk.

**When to run:** only when ops-manager's audit (Check 3) reports 1+ stuck
task, OR user explicitly asks "is everything actually done?".

**3-call V23 recipe (log → DB):**

```bash
# 1. Non-done tasks
sqlite3 ~/.hermes/kanban.db "SELECT id, status, claim_lock, claim_expires, started_at, title FROM tasks WHERE status NOT IN ('done') ORDER BY COALESCE(started_at, created_at) DESC LIMIT 20;"

# 2. Status distribution
sqlite3 ~/.hermes/kanban.db "SELECT status, COUNT(*) FROM tasks GROUP BY status;"

# 3. Recent completions (2h window)
sqlite3 ~/.hermes/kanban.db "SELECT id, status, completed_at, title FROM tasks WHERE completed_at > strftime('%s','now','-2 hour') ORDER BY completed_at DESC;"
```

If all 3 show "0 non-done" / "all done" → ops-manager's claim is a V23 false
positive → report "0 stuck (FP: log mtime stale, DB = done)" → no nudge.
Schema note: `tasks` table has NO `updated_at` column — use `started_at` /
`completed_at` (sqlite3 returns "no such column" if you query `updated_at`).

**4th check V24 (DB → disk, belt-and-suspenders):** Only run when V23
returns 0 stuck AND user wants proof, OR for the headline task:

```bash
sqlite3 ~/.hermes/kanban.db "SELECT id, completed_at FROM tasks WHERE status='done' AND completed_at > strftime('%s','now','-30 day');" \
  | while IFS='|' read -r id completed_at; do
      workspace=~/.hermes/kanban/workspaces/$id
      if [ -d "$workspace" ]; then
        count=$(find "$workspace" -type f -size +0c | wc -l)
        [ "$count" = "0" ] && echo "SILENT_RECOVERY: $id (DB=done) but workspace empty"
      else
        echo "MISSING_WORKSPACE: $id (DB=done) but dir missing"
      fi
    done
```

**3-layer verification chain:** log mtime (skip) → DB status (query) →
disk file (ground truth). V24 re-validated across 2 consecutive sweeps
(H78 + H79, 2026-06-30) — pattern is durable. Full recipe + t_3a73b0af
case study in `references/kanban-log-vs-kanban-db-false-positive.md`.

## Output format (REQUIRED)

```
**🟢 HEARTBEAT SWEEP H<N> — <ISO timestamp> — <1-line summary>**

| Profile | Goal | Last Activity | Health | Notes |
|---|---|---|---|---|
| **<name>** | None/<goal> | <ISO> | 🟢/🟡/🔴 HEALTHY/<reason> | <1-line> |

**Summary: N active, N stuck, N verified-needed, N escalated.**
```

Keep total output ≤ 30 lines. A heartbeat that produces a 200-line report
will get cut off in Telegram delivery.

## When to STOP (silent-kill rule, H26)

If ALL of the following are true, deliver the report in your response ONLY —
do NOT write a new row to qa-agent/state.md:

- 20+ consecutive idle sweeps
- 0 security CRITICAL/HIGH findings
- 0 agent conflicts
- 0 outputs awaiting verification
- No new maker activity since last sweep

**Why:** writing verbose "system still idle" rows past the H20 boundary is
file bloat + corruption risk. The H32 HARD GATE in the full skill documents
the marker-file + size-cap enforcement.

## When to LOAD the full skill

Stop using this quick-reference and load `multi-agent-heartbeat` if:

- Any check returns >0 (stuck tasks, real cron fault, perm regression, conflict)
- You're about to write a verbose row (load to check the HARD GATE rules)
- You encounter Mode 6/7/8/9 (anchor collisions, silent-kill, truncated
  anchors, inherited truncation) — the full skill has the recipes
- ops-manager audit is missing or 24h+ stale (full skill has the recovery mode)
- The H36 clock-anomaly pattern appears (frontmatter in future, mtime stale)
- Ops-manager flags a stuck task (Check 3 hits 1+) — load full skill for V23+V24

## Changelog

- **v1.1.0 (2026-06-30 14:35+, this session):** Promoted Check 7 (kanban DB
  vs log mtime) from "consider" hint to active quick-reference content.
  Triggered by V24 re-validation across H78+H79 sweeps — silent-recovery
  bug (DB=done, workspace empty) is durable. Added V13/V20 pagination
  gotcha warning under Check 2. Title renamed from "6-Check" to "6+1-Check".
- **v1.0.0 (2026-06-27):** Initial 6-check recipe.
