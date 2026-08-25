# Kanban Stuck Task Triage

**Class:** Routing Audit (operations-manager)
**Codified:** 2026-06-30 (12:00 audit, t_3a73b0af discovered; 18:00 audit self-corrected via H82)
**Status:** ACTIVE — operations-manager is the only sweep that catches stuck kanban tasks (qa-agent's 6-check protocol excludes kanban per H28 scope discipline)

## Why this exists

`hermes kanban list` + `hermes kanban stats` will surface tasks in `blocked` status that have been silently waiting for weeks. The qa-agent hourly gate explicitly does NOT check kanban — it verifies file-system outputs (pending* / handoff* files), not the kanban task queue. This means any task that:
- Completed a run but lost its artifact, OR
- Blocked mid-investigation and was never retried

...will sit in the kanban indefinitely, invisible to qa-agent. Operations-manager's 7-check protocol (added 2026-06-30) is the only place this gets caught.

## 🚨 PITFALL (H82, codified 2026-06-30 18:00): DB is ground truth, NOT log file mtime

The 12:00 audit reported `t_3a73b0af` as stuck for 31.6 days because it read `~/.hermes/kanban/logs/t_3a73b0af.log` mtime (last touched 2026-05-29 22:23 when the artifact-lost question was opened to user). But the 18:00 audit queried `kanban.db` directly and found:
- `t_3a73b0af` status=`done`, completed_at=`2026-06-30T12:34:36+07:00` (32min after the 12:00 audit was written)
- All 9 tasks in kanban DB = `done`, 0 in any other state

**The log file is a session transcript (the "what do you want to do?" prompt), not a task status record.** A task can be `done` in DB for weeks while its log file still shows an unanswered prompt.

**Always verify against `kanban.db` before escalating "1+ stuck task" claims.** This is the task-state analog of H38 (cron-truth) — both say: trust the structured store, not the artifact file mtime. See `../multi-agent-heartbeat/references/kanban-log-vs-kanban-db-false-positive.md` for the full V23 recipe and the 3rd verification layer (V24 disk file presence — silent-recovery bug).

## Triage procedure

### Step 1: Detect stuck tasks (DB is ground truth)

```bash
# PRIMARY: query kanban DB directly (NEVER trust log file mtime)
sqlite3 ~/.hermes/kanban.db \
  "SELECT id, status, created_at, started_at, completed_at, claim_lock, claim_expires, title \
   FROM tasks WHERE status NOT IN ('done') AND (claim_lock IS NOT NULL OR started_at IS NOT NULL) \
   ORDER BY COALESCE(started_at, created_at) DESC LIMIT 20;"

# Status distribution (sanity check)
sqlite3 ~/.hermes/kanban.db "SELECT COUNT(*) AS total, status FROM tasks GROUP BY status;"

# Recent completions (helpful for cross-validation)
sqlite3 ~/.hermes/kanban.db "SELECT id, status, completed_at, title FROM tasks WHERE completed_at > strftime('%s','now','-2 hour') ORDER BY completed_at DESC;"

# CLI (secondary, for human-readable summary)
hermes kanban list 2>&1 | grep -E "blocked|running" | head -20
hermes kanban stats 2>&1
```

**If Step 1's SQL returns 0 non-done rows** → there are NO stuck tasks, regardless of what any log file mtime says. Stop here.

### Step 2: Age the task

```bash
hermes kanban show <task_id> 2>&1 | head -80
```

Look at:
- `created:` — original creation time
- Last `event` line with `[run N] blocked` — when it actually blocked
- Run history (`Runs (N):`) — see if any run completed successfully before the block

If the gap between `created` and now is >2h, the task is "stuck" by the routing-audit definition. Document in the audit report.

### Step 3: Classify recoverability

Not all stuck tasks are equal. Three patterns:

| Pattern | Description | Recommendation |
|---|---|---|
| **A. Run completed, artifact lost** | Run N completed with a result, but the workspace artifact file is missing. Run N+1 blocked trying to re-derive. | **Recoverable from run log** — re-claim + save the run summary as the artifact. OR close-as-resolved if the summary is sufficient. |
| **B. Genuine block, no run completion** | Run N blocked on a real failure (auth error, missing data, etc.). No run ever completed. | **Investigate root cause** — fix the underlying blocker, then re-claim. May be unrecoverable if the failure mode is permanent. |
| **C. Forgotten / orphaned** | Task was created, briefly worked, then abandoned. No recent activity. | **Close-as-stale** — if >30 days old with no work since, the data is probably no longer relevant. Add comment + archive. |

### Step 4: Document in audit

For each stuck task found, the audit report should include:
- Task ID + brief title
- Assignee profile
- Blocked-since timestamp + age in hours/days
- Pattern classification (A/B/C from above)
- Recommendation to Orchestrator

### Step 5: Surface in the audit verdict

A stuck task does NOT block the audit (the system can be "healthy" overall while a single task is stuck). It IS a real Orchestrator-attention item. The audit verdict should distinguish:
- "System healthy, 1 stuck task requires attention" (most common)
- "System degraded, multiple stuck tasks" (escalation)
- "System CRITICAL, kanban blocked >24h for active profile" (immediate escalation)

## Real example: t_3a73b0af (codified 2026-06-30, CORRECTED 18:00)

- **Task:** "Research and recommend the highest-success-rate YouTube niche from four options"
- **Assignee:** default
- **Created:** 2026-05-29 21:09
- **Log file last mtime:** 2026-05-29 22:23 (artifact-lost prompt was opened to user)
- **DB truth (verified 2026-06-30 18:00):** `status=done`, `completed_at=2026-06-30 12:34:36` (run 34, 32min after the 12:00 audit was written)
- **Pattern:** A — Run 24 completed 2026-05-29 21:19 with full result ("Niche Science/Mystery/Vũ Trụ Storytelling wins 8.05/10 — zero equipment cost, low competition, high CPM $6-18"). Artifact file `youtube-channel-research-final.md` was lost from the workspace. Run 33 (22:23) blocked trying to re-investigate. The run 34 (12:34 today) eventually wrote the artifact.
- **12:00 audit (FALSE POSITIVE):** Reported stuck 31.6 days based on log file mtime. **WRONG.**
- **18:00 audit (CORRECT):** Queried `kanban.db` directly, found `status=done`, corrected the report in `~/.hermes/profiles/operations-manager/state.md`.
- **Lesson (H82):** Always query the kanban DB for task status. The log file is a session transcript, not a status record.

This case is now cited in:
- `multi-agent-heartbeat` V23 (kanban-log-vs-kanban-db false positive)
- `multi-agent-heartbeat` V24 (silent-recovery bug — DB `done` but disk file missing for run 34's claimed artifact path)
- This file's Step 1 recipe above

## Kanban CLI quick reference

```bash
# List all tasks (status, assignee, title)
hermes kanban list

# Per-status / per-assignee counts
hermes kanban stats

# Full task details (events, runs, comments, artifacts)
hermes kanban show <task_id>

# Comment on a task (e.g., "research complete, see run 24 summary")
hermes kanban comment <task_id> "..."

# Re-claim a blocked task (assign back to a worker)
hermes kanban reclaim <task_id> --assignee <profile>

# Archive a stale task
hermes kanban archive <task_id>
```

## Cost vs benefit

- **Cost:** 2-3 tool calls per audit (`kanban list` + `kanban stats` + targeted `kanban show` if anything looks stuck). ~500-1000 tokens per sweep.
- **Benefit:** Catches zombie tasks that sit silently for weeks/months. qa-agent will never find these. The t_3a73b0af case shows 31.6 days of invisible stuck work — that's significant.

**Worth it.** Make the kanban check a permanent part of every routing audit.

## Related

- `../SKILL.md` — main routing-audit skill, 7-Check protocol section
- `references/30min-heartbeat-pattern.md` — note: 30m heartbeat is LITE variant, kanban check is FULL audit only
- `~/.hermes/profiles/operations-manager/state.md` — Audit history (H1-H76+)
