---
name: kanban-log-vs-kanban-db-false-positive
description: Operations-manager "1 STUCK task" claims derived from kanban/logs/<task_id>.log file mtime (last touched by the original session that flagged the artifact as lost) are FALSE POSITIVES when the kanban DB row is status='done'. Heartbeat must verify against the kanban DB before escalating. Discovered 2026-06-30 12:35 (H78 sweep).
type: pitfall
applies-to: [multi-agent-heartbeat, operations-manager-routing-audit]
severity: low (audit-only, no action needed)
---

# Kanban log-file vs kanban DB — false-positive stuck-task pitfall

## The pitfall

Operations-manager's 6h routing audit reports "1 STUCK task" by reading
`~/.hermes/kanban/logs/<task_id>.log` mtime. The log file's mtime is
**set by the original session that wrote the "artifact lost, what do you want
to do?" prompt to anh** — typically days or weeks before the task actually
completes. The DB row gets marked `done` later via a parent-task auto-completion
path (e.g. when all 3 child tasks complete, the parent flips to `done` even if
the parent's own final-artifact file is missing).

**Concrete case (H78 sweep, 2026-06-30 12:35):**

- Ops-manager audit claimed: `t_3a73b0af` stuck since 2026-05-29 22:23 (~31.6 days, 757.6h)
- Log file: `~/.hermes/kanban/logs/t_3a73b0af.log` — last mtime 2026-05-29 22:23
- Log content tail: "...❌ Root task artifact youtube-channel-research-final.md không tồn tại. Có 2 lựa chọn: 1. Tạo lại final report... 2. Verify lại..." followed by "Anh muốn em xử lý thế nào?"
- **Kanban DB ground truth (sqlite3 ~/.hermes/kanban.db):** `t_3a73b0af` status=`done`, completed_at=1782797676 (2026-06-30 04:54 ICT), 3 child tasks (`t_ae311581`, `t_58085dff`, `t_0f7cfa72`) all status=`done`
- **All 9 tasks in kanban DB = done, 0 in any other state**

The ops-manager audit itself hedged with "left for anh's review" + recommended
"re-claim + re-run OR close-as-resolved (the underlying research IS in run 24's
summary)" — i.e. it KNEW the claim was soft. But the heartbeat protocol
treats ops-manager's "1 STUCK task" output as a fact to escalate.

## Companion to H38 (mtime-vs-cron-truth)

This is the **task-state** analog of H38 (cron-truth). H38 says:
> state.md mtime ≠ cron truth. A "0 findings" audit log entry is APPENDED
> only if there's something to report — clean cron runs don't always rewrite
> state.md, so mtime can lag cron by hours or days.

The kanban-log pitfall says:
> kanban/logs/<id>.log mtime ≠ task status. The log file is the
> "session transcript" of the last time anyone OPENED a question about
> that task — not a record of when the task completed. A task can be
> done for weeks while its log file still shows an unanswered prompt
> from the last time someone touched it.

The kanban DB is the only ground truth for task status. Log files are
session artifacts, not state.

## Heartbeat verification recipe (3 calls, ~2s)

Before escalating any "1+ stuck task" claim from ops-manager:

```bash
# 1. Check kanban DB for non-done tasks
sqlite3 ~/.hermes/kanban.db "SELECT id, status, created_at, started_at, completed_at, claim_lock, claim_expires, title FROM tasks WHERE status NOT IN ('done') AND (claim_lock IS NOT NULL OR started_at IS NOT NULL) ORDER BY COALESCE(started_at, created_at) DESC LIMIT 20;"

# 2. Status distribution
sqlite3 ~/.hermes/kanban.db "SELECT COUNT(*) AS total, status FROM tasks GROUP BY status;"

# 3. Recent completions in last 2h
sqlite3 ~/.hermes/kanban.db "SELECT id, status, completed_at, title FROM tasks WHERE completed_at > strftime('%s','now','-2 hour') ORDER BY completed_at DESC;"
```

If all 3 return "0 non-done" or "all done", the ops-manager "stuck task" claim
is a **false positive from log-file mtime** → report as "0 stuck (FP: ops-manager
log file stale, kanban DB = done)" → no nudge, no escalation.

## Schema reference (kanban DB)

`tasks` table has these status-relevant columns (verified 2026-06-30):

| Column | Purpose |
|---|---|
| `status` | `todo` / `ready` / `running` / `blocked` / `done` (use this for truth) |
| `created_at` | Unix epoch seconds, task creation |
| `started_at` | Unix epoch seconds, first claim |
| `completed_at` | Unix epoch seconds, status flipped to `done` |
| `claim_lock` | Profile holding current claim (NULL = unclaimed) |
| `claim_expires` | Unix epoch seconds, claim lease expiry |

**No `updated_at` column** — the DB schema uses `started_at`/`completed_at` for
transitions, not a generic update timestamp. Do not query for `updated_at`
(common mistake — sqlite3 will return "no such column" error).

The `result` column contains the final task output if `status='done'`.

## Anti-pattern: treating log mtime as task status

```python
# ❌ WRONG — what ops-manager currently does
import os
mtime = os.path.getmtime(f'~/.hermes/kanban/logs/{task_id}.log')
hours_idle = (time.time() - mtime) / 3600
if hours_idle > 2:
    report_stuck(task_id)  # FALSE POSITIVE

# ✅ RIGHT — what heartbeat should do
import sqlite3
db = sqlite3.connect('~/.hermes/kanban.db')
row = db.execute("SELECT status FROM tasks WHERE id=?", (task_id,)).fetchone()
if row and row[0] != 'done':
    report_stuck(task_id)
```

## When this pitfall does NOT apply

- The kanban DB row genuinely is `running` or `blocked` with non-NULL `claim_lock` → real stuck task, escalate
- The kanban DB row is `done` but the artifact file is missing → user-visible issue, surface as "task done but artifact lost" (separate from "stuck") — see **Silent-recovery bug (3rd layer)** below
- The task is in `todo`/`ready` and never claimed → not stuck, just queued (don't escalate as stuck)

## Silent-recovery bug — 3rd verification layer (H78 sweep, 2026-06-30 12:45)

V23 + this file's main section handle the **log-file → DB** mismatch. But the
DB itself can lie: a task row can be flipped to `status='done'` even when the
artifact path recorded in the run's `metadata.artifacts` does not exist on disk.

**Mechanism:** The kanban dispatcher records artifact paths in
`task_runs.metadata` JSON (`artifacts: [".../youtube-channel-research-final.md"]`)
**before** verifying the file exists with `os.path.exists + size>0`. A worker
session that crashed mid-write, or a parent-task auto-completion path that
flips a task to `done` based on child-task completion alone, can mark the
parent `done` even when its own final artifact was never written.

**Concrete case (t_3a73b0af, same H78 sweep):**

- DB: `status='done'`, `completed_at=2026-06-30 12:34:36` (run 34)
- Run 34 metadata claims artifact:
  `~/.hermes/kanban/workspaces/t_3a73b0af/youtube-channel-research-final.md`
- **Disk truth:** workspace dir is empty (0 files), artifact missing
- This is the SAME root cause as the original 2026-05-29 22:23 block (run 24
  was `done` in DB but artifact never persisted to disk)

**The 3-layer verification chain (mtime → DB → disk):**

| Layer | Source | Can lie? | How to check |
|---|---|---|---|
| 1. Log mtime | `kanban/logs/<id>.log` | YES (session transcript, not status) | Don't trust |
| 2. DB `status` | `kanban.db.tasks.status` | YES (parent auto-completion, no artifact verify) | Query SQLite |
| 3. Disk file | `kanban/workspaces/<id>/*` | NO (ground truth) | `ls -la` / `find` |

**Heartbeat recipe — 4th check (after V23's 3-call recipe):**

```bash
# 4. For every task the DB says is `done`, verify artifacts on disk
sqlite3 ~/.hermes/kanban.db "SELECT id, completed_at FROM tasks WHERE status='done' AND completed_at > strftime('%s','now','-30 day');" \
  | while IFS='|' read -r id completed_at; do
      workspace=~/.hermes/kanban/workspaces/$id
      if [ -d "$workspace" ]; then
        count=$(find "$workspace" -type f -size +0c | wc -l)
        if [ "$count" = "0" ]; then
          echo "SILENT_RECOVERY: $id (DB=done, completed_at=$completed_at) but workspace is empty"
        fi
      else
        echo "MISSING_WORKSPACE: $id (DB=done, completed_at=$completed_at) but dir doesn't exist"
      fi
    done
```

**Report format when this fires:**

> 🚨 **Silent-recovery bug detected**
> Task `t_<id>` shows `done` in kanban DB (completed `<timestamp>`) but
> workspace `<path>` is empty (0 files, no artifact at claimed path).
> Root cause: kanban dispatcher records artifact paths before verifying
> `os.path.exists + size>0`. Recommend: re-claim + actually write artifact,
> OR close-as-resolved with explicit note in DB. Do NOT trust DB `done` as
> proof of work.

**When to run this check:**

- NOT every sweep — adds 1-2 tool calls (sqlite + find). Only run when:
  - Ops-manager reports "1+ stuck task" (V23 recipe returns 0, but user
    wants belt-and-suspenders), OR
  - User explicitly asks "is everything actually done?", OR
  - Daily ops-manager audit shows a task with `done` status but missing
    workspace dir (defensive check)

**Related:** This is the **task-artifact analog of H38 (mtime) + V23 (DB)**
— the third layer in the "trust nothing without verification" cascade.
A complete verification = log mtime check (skip) + DB status check + disk
file check. The disk file is the only ground truth.

## Provenance

- H78 sweep (2026-06-30 12:35 ICT) — first verified instance
- qa-agent H77 row already noted multi-cron fault (different class — cron
  ticks missed) but did not catch this kanban-log false positive because
  qa-agent doesn't read ops-manager output
- ops-manager's own audit recommended "close-as-resolved" — the audit was
  correct, but the heartbeat escalation path doesn't read the recommendation
  line, only the "1 stuck task" headline

## Related

- `h38-mtime-vs-cron-truth-pattern.md` — mtime lies about cron state
- `h37-phantom-cron-claim-pattern.md` — validate inherited claims (cites
  `hermes cron list` before escalating; this extends the pattern to
  kanban DB queries)
- `quick-reference-6check.md` — should add a 7th check: "verify stuck-task
  claims against kanban DB, not log file mtime"
