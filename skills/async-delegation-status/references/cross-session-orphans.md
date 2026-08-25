# Cross-session orphan handling

**Question:** A row has `state='unknown'` (or it's `state IN ('running','finalizing')` but the dispatcher pid is dead). How do I report / recover it?

## What "orphan" means in this codebase

`recover_abandoned_delegations()` runs at gateway startup. For every row with `state IN ('running','finalizing')`, it checks:

```python
live = _pid_exists(int(pid)) and get_process_start_time(int(pid)) == int(started)
```

If the dispatcher pid is gone (process exited) OR the dispatcher pid has been re-used by something else (different boot time), the row is flipped to `state='unknown'` with `error='Delegation owner exited before recording a terminal result; outcome unknown.'`

So an orphan is **not** the same thing as a child crash. The child thread is gone (because the gateway process hosting the executor is gone), but the child might have completed cleanly and just never written to `state.db`.

## How to identify orphans

```sql
SELECT delegation_id, parent_session_id, owner_pid, owner_started_at,
       dispatched_at, json_extract(task_json, '$.goals') AS goals
FROM async_delegations
WHERE state = 'unknown'
ORDER BY dispatched_at DESC;
```

Then for each row, read `event_json.error` — true orphans will literally say "Delegation owner exited before recording a terminal result".

## How to report orphans to the user

Don't conflate orphans with real failures. Suggested phrasing:

> "3 background subagents from yesterday's batch are marked `unknown` because the gateway restarted before they finished. We don't know if they completed or failed — the result payloads are gone."

If the user needs the work redone, re-dispatch with a fresh `delegate_task` and capture the new `delegation_id`.

## Cleanup

The async_delegation table has its own retention:

- `_DURABLE_RETENTION_SECONDS = 7 * 24 * 60 * 60` (7 days) — terminal rows older than this get pruned if delivered
- `_MAX_RETAINED_COMPLETED = 50` — global cap on terminal rows
- `_MAX_DURABLE_PENDING = 1000` — global cap on undelivered terminal rows

So orphans self-evict after a week (or sooner under load). You don't need to manually delete them.

## Orphan in a different session than the user is in

If you see an orphan row whose `parent_session_id` is from a session other than the current one:

- **If the user is asking about that batch** → report it as "your session X from yesterday lost these — outcome unknown, recommend re-dispatch".
- **If the user is asking about something else** → ignore the orphan; it's not relevant to the current question.

Don't blindly offer to re-dispatch an unrelated orphan — that's invasive.

## When `state='running'` but `owner_pid` is dead

This is the pre-orphan state. The gateway boot that should have recovered it is either:

- Still running but blocked (rare — `recover_abandoned_delegations()` runs at startup)
- Crashed mid-recovery (very rare — would need a manual `_connect()` + UPDATE)

If you encounter this, treat it as an orphan for reporting purposes. Don't try to "rescue" it — the dispatcher process is gone, there's no one to wake up.

## Pre-flight: prevent orphans in the first place

`tools/async_delegation.py` writes `event_json` and `result_json` BEFORE pushing onto the completion queue, so a crash between finalize and queue.put is bounded. But a hard gateway kill mid-dispatch leaves a `running` row with no completion event.

Two mitigations already in place:

1. `owner_pid` + `owner_started_at` in `state.db` (lets `recover_abandoned_delegations` detect orphans on next boot)
2. `_finalize()` flips `state='finalizing'` BEFORE the SQLite write, then `state=<terminal>` AFTER. The narrow `finalizing` window is the only true at-risk state — and even there, a subsequent gateway boot will mark it `unknown` rather than silently succeed.
