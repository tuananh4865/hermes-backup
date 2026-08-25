---
name: v25-disk-check-omission
description: Real-world example of skipping the V24 disk check even when ops-manager escalated a stuck-task claim. Captured H78 sweep (2026-06-30 16:31 ICT) where the operator correctly ran the V23 DB check (confirmed done) but DID NOT run the V24 workspace-disk check, which would have caught the silent-recovery bug (DB=done, workspace empty). Use when the heartbeat pattern recurs — proves the skill's "optional" framing of V24 was a false economy, and the 3-layer chain must be mandatory when ops-manager escalates a stuck task.
type: pitfall
applies-to: [multi-agent-heartbeat, operations-manager-routing-audit]
severity: medium (audit-only, but the missed V24 check would have surfaced a user-visible artifact-loss issue)
---

# V25 — Disk-check omission when ops-manager escalates a stuck task

## The pattern

The V23+V24 protocol says: when ops-manager flags "1+ stuck task", the heartbeat
must run the **3-layer verification chain** (log → DB → disk) to confirm
whether the claim is a false positive or a real user-visible issue.

In practice, an operator (or subagent) running the V23 recipe and seeing
`status='done'` tends to stop and report "0 stuck (FP)". The V24 disk check
("does the artifact actually exist on disk?") is documented as
"belt-and-suspenders" → it gets skipped.

**But V24 catches a different class of bug than V23.** V23 catches
log-mtime-lies-about-status. V24 catches DB-lies-about-artifact
(parent-task auto-completion flips status to `done` even when the parent's
own final artifact was never written). Skipping V24 means a silent
"task done but deliverable missing" issue goes unreported.

## Concrete instance — H78 sweep (2026-06-30 16:31 ICT)

**Setup:**
- Ops-manager 6h audit (12:00) reported: "1 STUCK task t_3a73b0af
  (YouTube niche research), blocked 31.6 days, artifact
  youtube-channel-research-final.md was lost"
- 4h31m later, the 30m orchestrator heartbeat fired (H78)

**What the operator did (correct):**
- Ran V23 recipe — sqlite query: `t_3a73b0af | status=done | completed_at=2026-06-30 12:34:36`
- Correctly identified this as a V23 false positive (log mtime stale, DB = done)
- Reported: "0 stuck (FP: ops-manager's claim, kanban DB = done at 12:34 today)"

**What the operator should have done (skipped):**
- V24 disk check: `ls -la ~/.hermes/kanban/workspaces/t_3a73b0af/`
- Expected outcome: workspace is empty (0 files), DB says done, but
  no artifact at `youtube-channel-research-final.md` → V24 SILENT_RECOVERY
- Should have reported: "🚨 Silent-recovery: t_3a73b0af DB=done but
  workspace empty. Root cause: parent-task auto-completion flipped
  status without verifying artifact on disk."

## Why V24 was skipped

Three reasons the "belt-and-suspenders" framing invited the omission:

1. **Skill says "optional"** — quick-reference phrases it as
   "V24 (DB → disk, belt-and-suspenders)" and the 4th-check recipe
   says "Only run when V23 returns 0 stuck AND user wants proof".
   The operator interpreted "user wants proof" as "user explicitly
   asked", not "ops-manager escalated a stuck task as the headline finding".

2. **V23 success feels conclusive** — `status='done'` is a satisfying
   terminal state. The temptation is to stop there. The disk check
   feels redundant because the DB already says done.

3. **Cost framing** — V24 adds 1-2 tool calls (sqlite + find). The skill
   notes this as a reason to skip. But 1-2 tool calls is cheap; an
   undetected silent-recovery is expensive (user discovers missing
   deliverable days later, mid-conversation).

## Lesson — V25 rule

**When ops-manager's audit (Check 3) reports 1+ stuck task — the heartbeat
MUST run all 3 layers of the verification chain, in order, and report
findings at each layer. The chain is not optional; it is the protocol.**

If V23 says "0 stuck, DB=done" but the task is the headline finding
of ops-manager's audit, V24 must still run. The fact that ops-manager
escalated the task is itself a signal that the deliverable may not
match the DB claim — and only the disk check can confirm that.

## Updated V25 recipe (mandatory when Check 3 fires)

```bash
# Layer 1: log mtime — never trust, but capture for the report
ls -la ~/.hermes/kanban/logs/<task_id>.log

# Layer 2: DB status — V23 recipe
sqlite3 ~/.hermes/kanban.db \
  "SELECT id, status, claim_lock, claim_expires, started_at, completed_at, title \
   FROM tasks WHERE id='<task_id>';"

# Layer 3: disk file — V24 (MANDATORY when ops-manager escalated)
workspace=~/.hermes/kanban/workspaces/<task_id>
if [ -d "$workspace" ]; then
    find "$workspace" -type f -size +0c | wc -l | xargs -I {} echo "files_in_workspace: {}"
    # claim paths from task_runs.metadata.artifacts (JSON parse)
    # verify each path: os.path.exists + size>0
else
    echo "MISSING_WORKSPACE: $workspace does not exist"
fi
```

## Report format

When all 3 layers pass:
> 0 stuck. V23+V25 cleared: t_3a73b0af DB=done 12:34 today, workspace
> has 1 artifact (final report at /path/...), no silent-recovery.

When V25 fires (DB=done but workspace empty):
> 🚨 Silent-recovery: t_3a73b0af DB=done (2026-06-30 12:34) but
> workspace /Users/.../workspaces/t_3a73b0af/ is empty (0 files).
> Same root cause as 2026-05-29 22:23 block. Recommend re-claim
> + actually write artifact, OR close-as-resolved with note.

## Skill-versioning note

- v1.24.0 of `multi-agent-heartbeat` SKILL.md documents V23+V24 as
  "Check 7" but frames V24 as "belt-and-suspenders"
- v1.1.0 of `quick-reference-6check.md` echoes the same "optional" framing
- **V25 (this file) recommends the next patch promote V24 to "mandatory
  when Check 3 fires"** — the cost of running the 4th check is always
  less than the cost of missing a silent-recovery

## Related

- `kanban-log-vs-kanban-db-false-positive.md` — V23+V24 origin + recipes
- `quick-reference-6check.md` — should be patched to mark V24 mandatory
  when Check 3 hits 1+
- `h38-mtime-vs-cron-truth-pattern.md` — the cron-state analog
  (mtime-lies-about-cron-truth); V23+V24+V25 is the task-state analog
  (log/DB/disk cascade)

## Provenance

- H78 sweep (2026-06-30 16:31 ICT) — operator ran V23, did not run V24
- Self-identified gap: the same root cause (kanban dispatcher auto-completion
  without artifact verification) is documented in the kanban-log-vs-kanban-db
  reference as recurring across 2 consecutive sweeps
- The fix is operator discipline, not a code change: the recipe is in
  the skill, the operator must follow it end-to-end
