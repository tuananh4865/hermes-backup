# Event-Name Filter Pitfall (2026-06-16)

## Symptom

Hermes shell hook is registered, allowlisted, and the bash wrapper is callable. Real Telegram messages arrive. The hook `on_session_end` fires (verified via gateway logs). **But the Python handler exits silently with exit 0, no stdout, no file created.**

The user then says "hello" → no V2 transcript file appears. The user then says "test test" → no V2 file appears. V1 hook keeps working fine. V2 hook appears dead.

## Root Cause

The Python handler has a filter at the top of `handle()`:

```python
if event_type != "agent:end":
    return
```

The runtime event name Hermes passes to shell hooks is **`on_session_end`** (underscore form, from `VALID_HOOKS`). The handler is checking for the **colon form** `agent:end` (from older hooks.md docs). The mismatch causes the handler to early-return without error.

```python
# What the docs say
event_type = "agent:end"  # or "session:start" etc.

# What the runtime actually passes (from _serialize_payload in shell_hooks.py)
event_type = "on_session_end"  # underscore form
```

## Debug Trail (worked 2026-06-16, took 2 minutes)

```bash
# Step 1: Check the handler's filter
python3 -c "
import sys
sys.path.insert(0, '/Users/tuananh4865/.hermes/hooks/transcript-saver-v2')
import handler
print('Accepts on_session_end?', 'on_session_end' in ('agent:end', 'agent_end'))
# → False
"

# Step 2: Inject stdin JSON, watch what happens
echo '{"hook_event_name":"on_session_end","session_id":"test","extra":{"response":"x","message":"[User] x","platform":"telegram","user_id":"123"}}' \
  | python3 /Users/tuananh4865/.hermes/hooks/transcript-saver-v2/handler.py --event agent_end
# → exit 0, no stdout, no file

# Step 3: Read the Hermes source to confirm event name
grep -A 5 "_serialize_payload" /Users/tuananh4865/.hermes/hermes-agent/agent/shell_hooks.py
# → Confirmed: payload["hook_event_name"] = event (underscore form)
```

## Fix

```python
END_EVENTS = (
    "agent:end", "agent_end",       # docs form + CLI arg form
    "on_session_end",                # ACTUAL Hermes shell hook event name
)
if event_type not in END_EVENTS:
    return
```

After fix, the same stdin JSON test produces a real V2 file with full frontmatter.

## The Two Forms Explained

| Form | Used in | Example |
|------|---------|---------|
| Colon (`agent:end`, `session:start`) | Old `hooks.md` docs, Python plugin hook events | `agent:end` |
| Underscore (`agent_end`, `on_session_end`) | `VALID_HOOKS` in `hermes_cli/plugins/__init__.py`, runtime `hook_event_name` field | `on_session_end` |

**The colon form is a documentation convention; the underscore form is what the runtime actually sends.**

## Where to Look in Hermes Source

```bash
# The runtime event name (underscore form)
grep "VALID_HOOKS\|hook_event_name" \
  /Users/tuananh4865/.hermes/hermes-agent/hermes_cli/plugins/__init__.py \
  /Users/tuananh4865/.hermes/hermes-agent/agent/shell_hooks.py

# The serialized payload (where hook_event_name is set)
sed -n '460,490p' /Users/tuananh4865/.hermes/hermes-agent/agent/shell_hooks.py
```

```python
# In _serialize_payload(event, kwargs):
payload = {
    "hook_event_name": event,  # ← this is the event name with underscores
    "tool_name": kwargs.get("tool_name"),
    "tool_input": ...,
    "session_id": ...,
    "cwd": ...,
    "extra": extras,
}
```

## Other Common Mismatches

| Docs say | Runtime sends | Filter that breaks |
|----------|---------------|-------------------|
| `agent:start` | `subagent_start` (or no event) | `if event_type == "agent:start"` |
| `session:end` | `on_session_end` | `if event_type == "session:end"` |
| `agent:step` | (no equivalent shell hook) | always false |
| `session:reset` | `on_session_reset` | `if event_type == "session:reset"` |

**Rule:** When the handler receives an event name from stdin JSON, it MUST be the **underscore form from `VALID_HOOKS`**. If your filter checks the colon form, the handler silently no-ops.

## Test That Catches This

```python
def test_accepts_all_event_forms():
    """Verify handler accepts agent:end, agent_end, AND on_session_end."""
    with tempfile.TemporaryDirectory() as tmp:
        # Setup mocked paths
        ...
        for evt in ("agent:end", "agent_end", "on_session_end"):
            ctx = {"message": "x", "response": "y", "session_id": "test"}
            # Should not raise and should attempt to save
            handler.handle(evt, ctx)
            # Verify a file was created (or at least the function ran past the filter)
```

## When This Triggered in 2026-06-16

Round 4 (transcript-saver-v2 creation): Handler was created with `if event_type != "agent:end": return`. It worked for manual E2E tests because those passed `agent_end` via argparse. But when Hermes invoked it via shell hook, the stdin JSON had `hook_event_name: "on_session_end"` → handler returned early → no file.

**The bug went undetected for ~30 minutes** because:
1. Manual E2E tests succeeded (used argparse `--event agent_end`)
2. Unit tests passed (mocked context, never went through stdin)
3. V1 hook was still saving files, masking the V2 silence

The fix (accepting `on_session_end`) made V2 start firing on real messages.

## Prevention Checklist

For ANY new Hermes shell hook, before declaring it works:

- [ ] Read `hermes_cli/plugins/__init__.py` VALID_HOOKS
- [ ] In the handler, accept BOTH colon and underscore forms of the event name
- [ ] Test 1: CLI args path (e.g. `python3 handler.py --event agent_end`) — should work
- [ ] Test 2: Stdin JSON path with real `hook_event_name` from VALID_HOOKS — should work
- [ ] Test 3: Real Hermes invocation (send a Telegram message, wait, check file)
- [ ] Test 4: Diff V2 file content against V1 file content to confirm differentiation

If test 1 passes but test 3 doesn't, the filter is the bug.
