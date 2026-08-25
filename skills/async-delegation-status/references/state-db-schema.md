# `async_delegations` schema reference

**Source:** `~/.hermes/hermes-agent/tools/async_delegation.py` (v3.21.4+)
**Location:** `~/.hermes/state.db` (WAL mode, created by `_connect()` on first dispatch)

## Table DDL

```sql
CREATE TABLE IF NOT EXISTS async_delegations (
    delegation_id        TEXT PRIMARY KEY,
    origin_session       TEXT NOT NULL,           -- session_key: agent:main:telegram:group:-1004366612538:307
    origin_ui_session_id TEXT NOT NULL DEFAULT '',
    parent_session_id    TEXT,                    -- state.db session_id of the dispatcher
    state                TEXT NOT NULL,           -- running | finalizing | completed | error | interrupted | unknown
    dispatched_at        REAL NOT NULL,           -- time.time() at dispatch
    completed_at         REAL,                    -- time.time() at finalize; NULL while running
    updated_at           REAL NOT NULL,           -- bumped on every _persist_* call
    event_json           TEXT,                    -- full completion event (status, summary, error, ...)
    result_json          TEXT,                    -- result payload (per-task results for batches)
    delivery_state       TEXT NOT NULL DEFAULT 'pending',  -- pending | delivered
    delivery_attempts    INTEGER NOT NULL DEFAULT 0,
    delivered_at         REAL,
    owner_pid            INTEGER,                 -- pid of the dispatcher at dispatch time
    owner_started_at     INTEGER,                 -- gateway process start time (epoch ms)
    task_json            TEXT,                    -- {goal, goals, context, toolsets, role, model, is_batch}
    delivery_claim       TEXT,                    -- UUID for delivery race prevention
    delivery_claimed_at  REAL
);
```

## Column semantics — what to read for which question

| You want to know | Read |
|---|---|
| Is the batch still running? | `state IN ('running', 'finalizing')` |
| When did it start? | `dispatched_at` (epoch seconds, UTC) — convert with `datetime.fromtimestamp` |
| When did it finish? | `completed_at` — NULL while running |
| Who dispatched it? | `parent_session_id` — joins to `state.db.sessions.id` |
| Whose gateway boot owns it? | `owner_pid` + `owner_started_at` — `recover_abandoned_delegations()` uses these to detect orphans |
| What were the per-child goals? | `task_json.goals` (list) or `task_json.goal` (single) |
| What did each child return? | `result_json.results[].summary`, `result_json.results[].status` |
| Did the gateway/CLI drain the completion? | `delivery_state = 'delivered'` means yes; `pending` means queued but not yet drained |
| Was the dispatcher process restarted mid-flight? | row exists but `state IN ('running','finalizing')` AND `pid_exists(owner_pid)` is False → recovered to `unknown` |

## State transitions

```
                   dispatch_async_delegation_batch()
                                   │
                                   ▼
                              state=running
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
       normal     │   child raised │   /stop or     │   gateway exited
       completion │   exception    │   interrupt    │   before finalize
                  ▼                ▼                ▼
             state=completed   state=error    state=interrupted
                  │                │                │
                  └────────────────┴────────────────┘
                                   │
                  delivery_queue.put(evt) — async
                                   │
                                   ▼
                          delivery_state='pending'
                                   │
                  gateway/CLI drain picks it up
                                   ▼
                         delivery_state='delivered'


            ── on gateway restart ──────────────────

            recover_abandoned_delegations()
            marks any (running|finalizing) row
            whose owner_pid is gone → state='unknown'
```

## Useful queries

**All in-flight batches right now:**

```sql
SELECT delegation_id, parent_session_id, dispatched_at,
       json_array_length(json_extract(task_json, '$.goals')) AS n_goals
FROM async_delegations
WHERE state IN ('running', 'finalizing')
ORDER BY dispatched_at DESC;
```

**Last batch dispatched by parent session:**

```sql
SELECT delegation_id, state, dispatched_at, completed_at, delivery_state
FROM async_delegations
WHERE parent_session_id = '20260718_071838_8d4cf9aa'
ORDER BY dispatched_at DESC
LIMIT 5;
```

**Per-batch failure rate (last 24h):**

```sql
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN state = 'completed' THEN 1 ELSE 0 END) AS ok,
  SUM(CASE WHEN state = 'error'     THEN 1 ELSE 0 END) AS err,
  SUM(CASE WHEN state = 'interrupted' THEN 1 ELSE 0 END) AS int,
  SUM(CASE WHEN state = 'unknown'   THEN 1 ELSE 0 END) AS unk
FROM async_delegations
WHERE dispatched_at > strftime('%s', 'now', '-1 day');
```

**Orphans from a stale gateway boot:**

```sql
SELECT delegation_id, owner_pid, owner_started_at, dispatched_at
FROM async_delegations
WHERE state IN ('running', 'finalizing')
  AND owner_pid IS NOT NULL
ORDER BY dispatched_at DESC;
-- Then cross-check: ps -p <owner_pid> for each, plus the boot time
```

## Performance / footprint

- WAL mode means readers (you) don't block writers (the gateway).
- `_prune_durable_records()` keeps at most `_MAX_RETAINED_COMPLETED = 50` terminal rows and `_MAX_DURABLE_PENDING = 1000` undelivered terminal rows. So old batches vanish — use logs for archaeology.
- `result_json` and `event_json` can be large (50KB+ for a 5-task batch with full tool_traces); use `read_file` with offset/limit rather than `SELECT *`.

## What this schema does NOT tell you

- The actual tool calls the child made (those are in `agent.log`, not in `state.db`).
- Which session_id corresponds to which child of a batch — you have to correlate via `agent.log` between the `Dispatched` line and the next N `agent.turn_context ... platform=subagent` lines.
- Whether the child is currently mid-API-call vs between calls — only `agent.log` timestamps tell you that.
