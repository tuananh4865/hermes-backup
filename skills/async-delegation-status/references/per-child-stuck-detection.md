# Per-child stuck detection

**Question:** A child has `state='running'` in `state.db`, but its `agent.log` trace looks frozen. Is it stuck, or just slow?

## Signals to combine

| Signal | Where to read | What it means |
|---|---|---|
| Time since last log line for the child session_id | `agent.log` grep `[$SESSION_ID]` | >5min with no events = probably stuck |
| `api_calls` count in last `Turn ended` vs in current conversation turn | `agent.log` `Turn ended: ... api_calls=N/150` | If `N` is at 150/150 = hard cap → stuck on max_iterations |
| Most recent tool call result vs most recent API call request | `agent.log` `tool_executor: tool X completed` vs `agent.conversation_loop: API call #N:` | Tool result AFTER last API call = idle; API call AFTER last tool result = in-flight |
| Child's `tools.async_delegation` activity in `agent.log` | `agent.log` grep `$SESSION_ID.*async_delegation` | Subagent also spawned children → its "stall" might just be waiting on its own grandchildren |
| `Whisper` / `ffmpeg` / heavy ML process in `ps -axo` with that child as ancestor | `ps -axo ppid=,...` | Child is blocked on I/O-bound subprocess, not LLM |

## Decision matrix

| Time since last event | Last event type | Likely state | Action |
|---|---|---|---|
| <2min | any | healthy | wait |
| 2-5min | tool completed | mid-thinking | wait |
| 2-5min | API call sent, no result | likely slow LLM | wait, optionally ping user |
| 5-15min | tool completed | long tool run | check `ps` for subprocess |
| 5-15min | API call sent | LLM timeout risk | ping user |
| >15min | tool completed | very stuck or looped | offer interrupt |
| >15min | API call sent | LLM hung | recommend interrupt |

## Snippet — time since last event per child

```bash
LOG=~/.hermes/logs/agent.log
NOW=$(date +%s)
for sid in 20260718_140548_cbd09e 20260718_140555_994dd6; do
    last_ts=$(grep -E "\[$sid\]" "$LOG" | tail -1 | awk '{print $1" "$2}')
    if [ -n "$last_ts" ]; then
        last_epoch=$(date -j -f '%Y-%m-%d %H:%M:%S,%3N' "$last_ts" '+%s' 2>/dev/null \
                  || date -d "$last_ts" '+%s' 2>/dev/null)
        age=$((NOW - last_epoch))
        echo "$sid: last event ${age}s ago — $last_ts"
    else
        echo "$sid: no events in log"
    fi
done
```

## Snippet — distinguish "in-flight" from "between turns"

```bash
CHILD='20260718_140548_cbd09e'
LOG=~/.hermes/logs/agent.log
last_api=$(grep "\[$CHILD\].*conversation_loop: API call #" "$LOG" | tail -1)
last_tool=$(grep "\[$CHILD\].*tool_executor:" "$LOG" | tail -1)
echo "Last API call : $last_api"
echo "Last tool call: $last_tool"
# If last_api line is newer than last_tool → child is between turns (waiting for LLM)
# If last_tool line is newer than last_api → child just finished a tool, waiting to be re-prompted
```

## When to recommend `/stop`

A child is a candidate for interrupt if **all three** hold:

1. `state='running'` AND `dispatched_at` is older than the configured `HERMES_AGENT_TIMEOUT` (default 1800s = 30min).
2. No `tool completed` or `API call` event in the last 5 minutes.
3. No `Turn ended` line for the child.

When the user accepts interrupt, run:

```bash
# From a session that has the same parent_session_id as the batch
python3 -c "
import sys; sys.path.insert(0, '~/.hermes/hermes-agent')
from tools.async_delegation import interrupt_for_session
n = interrupt_for_session(parent_session_id='20260718_071838_8d4cf9aa')
print(f'Interrupted {n} delegation(s)')
"
```

That sends the interrupt signal to every running child of the parent session. Each child will then emit a `state='interrupted'` row on its next finalize pass.

## What NOT to do

- ❌ Don't tail `agent.log` with `tail -f` from the foreground — it'll keep the parent session blocked.
- ❌ Don't conclude "stuck" from one missing log line in 30s — LLM latency spikes to 30s are normal on long prompts.
- ❌ Don't interrupt while a child is mid-`ffmpeg` or mid-`Whisper` — the subprocess won't be reaped cleanly and you'll leak a process.
