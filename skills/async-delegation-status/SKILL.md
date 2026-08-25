---
name: async-delegation-status
description: 'Class-level umbrella for inspecting and reporting the live state of background subagents dispatched via `delegate_task` (async delegation batches) while they are still running. Covers reading the durable SQLite registry at `~/.hermes/state.db` `async_delegations` table, cross-referencing per-subagent session activity via `~/.hermes/logs/agent.log` [session_id] markers, identifying per-child errors, and producing a concise status report. Use when user asks "status of background subagents", "which N subagents are still running", "ping status of delegations", "show me active subagents", or any time a parent has dispatched a `delegate_task(background=true)` batch and needs a mid-flight report.'
version: 1.0.0
author: 'Tuấn Anh + Hermes Agent (v1.0.0 — 2026-07-18 initial creation from session where 5 clip-verify subagents were dispatched and the user asked for live status)'
license: MIT
platforms: [macos, linux]
metadata:
  category: devops
  class: async-delegation-ops
  triggers: status, ping, running, which subagents, background delegations, how many left, errors, async status
---

# async-delegation-status

**Class-level umbrella** for inspecting live state of background subagents dispatched via `delegate_task` (the `tools/async_delegation.py` async registry). The parent agent (or any later session) needs a recipe for "how do I see what's running right now and what errors each child has hit?" without polling message queues or interfering with the children.

## Trigger

Load this skill when:
- User asks "status of background subagents", "ping status of delegations", "which N subagents are still running", "how many left"
- A `delegate_task(background=true)` batch was dispatched in this or a recent session and you need a mid-flight report
- Before declaring an async batch "done" (so you can verify every child completed, not just trust the executor)
- After any error pattern — "any of the background subagents fail?" — to enumerate per-child failures

## When NOT to use

- For tmux-pane-style multi-agent setup (different infrastructure, see `multi-agent-orchestrator`)
- For profile-based persistent agents (different infrastructure, see `multi-agent-orchestrator`)
- For cron jobs (`hermes cron list` covers that)
- For the in-process `_background_tasks` thread map (CLI only — not relevant from gateway / cross-session)

## The 4-state model (FIRST-CLASS)

Background subagents dispatched via `delegate_task(background=true)` live in `~/.hermes/state.db`, table `async_delegations`. Each row has a `state` column. Possible values:

| state | meaning | is_done? |
|---|---|---|
| `running` | executor thread is alive, child agent is mid-flight | NO |
| `finalizing` | worker just returned; SQLite + queue write in flight (narrow window) | NO |
| `completed` | child finished cleanly, result persisted | YES |
| `error` | child raised an exception that the runner caught | YES |
| `interrupted` | `/stop` or `interrupt_for_session()` fired | YES |
| `unknown` | `recover_abandoned_delegations()` marked it — owning process exited before recording a terminal result | YES |

`delivery_state` is a separate axis: `pending` means the completion event has not been consumed by the gateway/CLI drain yet. A batch can be `state='completed'` but `delivery_state='pending'` for ~seconds until the drain loop picks it up.

## Where the data lives

| Surface | What it tells you |
|---|---|
| `~/.hermes/state.db` → `async_delegations` | Authoritative: delegation_id, state, dispatched_at, completed_at, parent_session_id, owner_pid, task_json (goal/goals/context), result_json |
| `~/.hermes/logs/agent.log` | Per-turn timeline: `tools.async_delegation: Dispatched async delegation batch ... (N task(s))` + `[session_id]` markers for each child + `Turn ended: ... api_calls=N/150` per child |
| `ps -axo pid=,ppid=,command=` (gateway tree) | Process-level view: subagents run on the daemon executor inside the gateway process; they are threads, not separate OS processes. `tools/mcp_stdio_watchdog.py` and any explicit foreground `terminal(background=true)` children ARE separate processes. |
| `~/.hermes/cache/delegation/subagent-summary-*.txt` | Cached full per-task summaries (auto-trimmed from in-conversation display). Read these for the full text the parent only sees head+tail of. |

## Recipe — live status of N background subagents

This is the canonical recipe used by every "ping status" call. It works from any session, regardless of which session dispatched the batch.

### 1. Read the batch row from `state.db`

```bash
sqlite3 -header -column ~/.hermes/state.db \
  "SELECT delegation_id, state, dispatched_at, completed_at, owner_pid,
          json_extract(task_json, '\$.goals') AS goals
   FROM async_delegations
   WHERE delegation_id='deleg_XXXXXXXX'
   ORDER BY dispatched_at DESC;"
```

For a multi-batch sweep:

```bash
sqlite3 ~/.hermes/state.db \
  "SELECT delegation_id, state, dispatched_at,
          json_array_length(json_extract(task_json, '\$.goals')) AS n_tasks,
          json_extract(task_json, '\$.goals', '\$[0]') AS first_goal
   FROM async_delegations
   WHERE state IN ('running','finalizing')
   ORDER BY dispatched_at DESC;"
```

The `parent_session_id` column links each batch back to the session that spawned it. Use it to confirm the running batch really belongs to the chat the user is in.

### 2. Enumerate child sessions (FIRST-CLASS)

When a batch is `state='running'`, each child is an independent session_id with its own `[session_id]` marker in `agent.log`. Discover them by scanning the `Dispatched` line for the batch and then the next N `agent.turn_context: ... platform=subagent` lines:

```bash
BATCH_ID='deleg_a2a0727e'
awk -v batch="$BATCH_ID" '
  /Dispatched async delegation batch '"$BATCH_ID"'/ {
    # the line above carries "(N task(s), ...)"
    n=$0; print n
  }
  /agent\.turn_context.*platform=subagent/ {
    match($0, /\[([0-9_]+)\]/, m)
    if (m[1]) print m[1], $0
  }
' ~/.hermes/logs/agent.log
```

Better: in Python you can correlate children to a batch by the parent's `session_key` and the dispatch timestamp window. Pattern: all subagent sessions for a given batch share the same `origin_session` and were dispatched within the same second.

```python
import sqlite3, datetime, json
con = sqlite3.connect('/Users/tuananh4865/.hermes/state.db')
con.row_factory = sqlite3.Row
row = con.execute(
    "SELECT * FROM async_delegations WHERE delegation_id=?",
    ('deleg_a2a0727e',)
).fetchone()
goals = json.loads(row['task_json']).get('goals') or [json.loads(row['task_json'])['goal']]
dispatched_at = row['dispatched_at']
# Each child session is logged as agent.turn_context within ~1s of dispatch
```

Then grep `agent.log` for `session_id` of each child to get live per-child activity.

### 3. Per-child activity + error count (FIRST-CLASS)

For each child session_id (e.g. `20260718_140548_cbd09e`), build a small status block:

```bash
CHILD='20260718_140548_cbd09e'
LOG=~/.hermes/logs/agent.log

events=$(grep -c "\[$CHILD\]" "$LOG")
api_calls=$(grep "\[$CHILD\].*API call #" "$LOG" | wc -l)
turns_ended=$(grep "\[$CHILD\].*Turn ended:" "$LOG" | wc -l)
errors=$(grep "\[$CHILD\].*Tool .* returned error\|ERROR" "$LOG" | wc -l)
last_line=$(grep "\[$CHILD\]" "$LOG" | tail -1)
```

Per-child classification:

| events | turns_ended | meaning |
|---:|---:|---|
| > 0 | 0 | RUNNING |
| > 0 | ≥ 1 | COMPLETED (one or more turns ended; final API call N/150 visible) |
| 0 | 0 | never started — likely dispatch failed before runner picked up the executor slot |

### 4. Build the user-facing report

Format used in real session (2026-07-18, batch `deleg_a2a0727e` — 5 clip-verify subagents):

```
Status at 14:10:52: batch deleg_a2a0727e is still running; all 5 subagents remain active.

- Clip 0004: Running. Two recoverable terminal errors: malformed mkdir command; frame-comparison script traceback.
- Clip 0005_NEW — LED RGB diffuser: Running. No logged errors.
- Clip 0005_OLD — quick-release mount: Running. One missing-file error under tiktok-video-editor/scripts/...
- Clip 0006 — 8-phase motion: Running. One shell command rejected for using `&`; continued afterward.
- Clip 0007 — KNF carbon-fiber cleaning kit: Running. Same rejected `&` backgrounding attempt; continued afterward.

Shared warning: the evidence-gate post-tool hook is not executable, so it repeatedly logs warnings across all agents.
```

Two things matter for the user:

1. **Batch-level state** (`running` vs `completed`) — single line at top.
2. **Per-child summary** — one bullet per subagent. Name the clip/topic, the latest activity timestamp, and any error.

If a child has `events > 0` but `turns_ended = 0`, name it explicitly as "stuck at API call #N since 14:09" so the user can decide whether to interrupt.

## Pitfalls

### Pitfall A — Trusting `ps` for thread-level children

Subagents dispatched via `delegate_task` run on a module-level `ThreadPoolExecutor` inside the gateway process (parent gateway pid is `owner_pid` in `state.db`). They are **threads, not processes**. `ps` will show only the parent gateway + its explicit subprocess children (`mcp_stdio_watchdog`, `ffmpeg`, `mlx_whisper`, ...). Do not conclude "no subagent = no subagent running" from `ps` alone — always cross-reference `state.db`.

### Pitfall B — Relying on `_background_tasks` (CLI-only)

`cli.py` has a `self._background_tasks: Dict[str, threading.Thread]` dict the CLI status bar reads. That is the **interactive CLI's** thread pool — different from `tools/async_delegation._executor`. The CLI dict disappears between sessions; `state.db` persists. Always use `state.db` for cross-session "is delegation X still alive?".

### Pitfall C — `delivery_state='pending'` ≠ still running

A row with `state='completed'` and `delivery_state='pending'` has finished; the gateway/CLI drain just hasn't picked up the completion event yet. Don't re-report it as "running" in the user-facing summary — the child is done.

### Pitfall D — `state='unknown'` means orphaned, not failed

`recover_abandoned_delegations()` flips rows to `state='unknown'` when the owning pid (`owner_pid`) no longer exists with the same start time (`owner_started_at`). This happens on gateway restart, not on real child failure. Distinguish from `state='error'` by reading `event_json.error` (orphan errors say "Delegation owner exited before recording a terminal result").

### Pitfall E — Per-child sessions logged with `platform=subagent`

Every child turn is logged with `agent.turn_context: ... platform=subagent ... msg='<original goal>'`. This is the easiest way to enumerate which session_ids belong to which batch — the `msg` field echoes the goal text the parent dispatched.

### Pitfall F — Shared warnings are not per-child failures

`agent.shell_hooks: shell hook failed (event=post_tool_call command=/Users/tuananh4865/.hermes/hooks/evidence-gate/handler.py): command not executable` shows up in EVERY child's log because the hook fires for every tool call. Surface it ONCE in the report ("Shared warning: …") rather than multiplying it across all children.

## Output contract

The user-facing report must answer 4 questions in order:

1. **Batch state**: is the batch still running, completed, or partially failed?
2. **Per-child summary**: one line per subagent naming the work + status + last activity timestamp.
3. **Per-child errors**: only the ones specific to that child (filter out shared hook warnings).
4. **Shared warnings** (optional): things like the `evidence-gate` hook that hit every child equally.

Cap the report at one screen. Do not paste the SQL output verbatim — interpret it.

## Reference files

- `references/state-db-schema.md` — column-by-column meaning of `async_delegations` and how the executor mutates it.
- `references/per-child-stuck-detection.md` — pattern for distinguishing a child that crashed mid-turn from one that's just slow.
- `references/cross-session-orphans.md` — how to handle `state='unknown'` rows from a previous gateway boot.

## Real case (2026-07-18)

A parent dispatched batch `deleg_a2a0727e` with 5 goals (clip 0004 / 0005_NEW / 0005_OLD / 0006 / 0007 verify). User asked "Ping — give me status of which 5 background subagents are still running, and any errors." Recipe used:

1. `sqlite3 ~/.hermes/state.db "SELECT * FROM async_delegations WHERE delegation_id='deleg_a2a0727e'"` → batch row, state='running'.
2. Grep `agent.log` for `Dispatched async delegation batch deleg_a2a0727e` → matched at 14:05:56, 5 task(s). The next 5 lines `agent.turn_context ... platform=subagent ... msg='Verify clip 0004 ...'` etc. → child session_ids:
   - 0004 → 20260718_140548_cbd09e
   - 0005_NEW → 20260718_140555_994dd6
   - 0005_OLD → 20260718_140555_18a7e9
   - 0006 → 20260718_140556_9de52c
   - 0007 → 20260718_140556_7bc768
3. For each child, grep `[session_id]` in `agent.log`, count events/api_calls/turns_ended/errors, grab last line.
4. Compose 5-bullet summary + 1 shared-warning line.

Result: report delivered in one screen, with all 5 children classified running and 4 of 5 with at least one error (mostly recoverable, plus the `evidence-gate` shared warning).

## Changelog

**v1.0.0 (2026-07-18):**
- Initial creation from real session: 5 clip-verify subagents dispatched via `delegate_task` batch and the user asked for live status.
- Captures the 4-state model (`running` / `finalizing` / terminal / `unknown`), the SQLite schema facts, the per-child grep recipe, and the user-facing report contract.
- Captures Pitfalls A–F (most importantly A: subagents are threads, not processes; F: don't multiply shared hook warnings per-child).
