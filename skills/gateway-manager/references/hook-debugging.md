# Hook Debugging — Gateway Manager Reference

## Hook System Architecture

Gateway hooks live in `~/.hermes/hooks/<hook-name>/`:
- `HOOK.yaml` — metadata (name, description, events list)
- `handler.py` — the `handle(event_type, context)` function

Hooks are discovered and loaded by `gateway/hooks.py` at startup. Events that fire hooks:
- `gateway:startup` — gateway process starts
- `session:start` — new session created
- `session:reset` — session reset completed
- `session:end` — session ends
- `agent:start` — agent begins processing
- `agent:step` — each turn in tool-calling loop
- `agent:end` — agent finishes processing
- `command:*` — any slash command executed

## Hook Debugging Path

### 1. Verify hook is loaded
```bash
grep "Loaded hook" ~/.hermes/logs/gateway.log | grep <hook-name>
```
If not loaded → HOOK.yaml or handler.py has a syntax error. Check the log lines immediately before.

### 2. Verify hook fires (look for print statements)
```bash
grep "hook-name" ~/.hermes/logs/gateway.log
```
Hooks print to stdout with prefix `[<hook-name>]`. If no output → hook's `handle()` is either:
- Not being called (event not firing)
- Raising exception (caught by hook runner, only "Error in handler" logged)

### 3. Force fire the event to test

The hook fires automatically on its declared events. To test manually:
```python
# From gateway run.py context, you can't manually emit
# Instead: trigger the event naturally (/new for session:start, etc.)
```

### 4. Test handler.py in isolation
```python
import sys
sys.path.insert(0, '~/.hermes/hooks/<hook-name>')
from handler import handle
handle("test-event", {"platform": "test", "user_id": "test", "session_key": "test"})
```

### 5. Common silent failure patterns

**Pattern A: Hook raises exception inside handle()**
- Gateway log shows: `[hooks] Error in handler for 'session:start': <traceback>`
- Fix: Wrap handle() body in try/except, log errors

**Pattern B: Hook path doesn't exist at import time**
- HOOK.yaml declares `events: [session:start]` but handler.py has typo in `def handle`
- Gateway log: hook loads but never fires

**Pattern C: Context dict missing expected keys**
- `handle(event_type, context)` — context keys vary by event type
- If code assumes a key that doesn't exist → KeyError → silently caught
- Check what context keys are actually available for each event type

**Context keys per event type:**
```
gateway:startup     → platform, user_id (sometimes missing)
session:start       → platform, user_id, session_id, session_key
session:reset       → platform, user_id, session_id, session_key
session:end         → platform, user_id, session_id, session_key
agent:start         → platform, user_id, session_id
agent:end           → platform, user_id, session_id, response (sometimes)
command:<name>      → platform, user_id, session_id, command
```

**Pattern D: File write fails silently**
- Hook tries to write to `~/.hermes/.recent_session_context.txt`
- Parent directory doesn't exist → FileNotFoundError → caught
- Fix: `CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)` before write

## Known Hooks on This System

| Hook | Events | Purpose | Status |
|------|--------|---------|--------|
| `transcript-saver` | agent:end | Save transcripts to wiki | ✅ Working |
| `wiki-session-start` | session:start, gateway:startup | Load wiki context at session start | ✅ Working |
| `session-resume-injector` | session:start, session:reset | Write recent session context for overflow recovery | ⚠️ Silent failure |
| `gsd-*` hooks | various | GSD workflow guards | Not loaded in this profile |

## session-resume-injector Known Issue

**Symptom:** After context overflow (session auto-reset), `~/.hermes/.recent_session_context.txt` is never created.

**Diagnosis:** The hook's `build_context_summary()` function likely raises an exception when:
- `TRANSCRIPTS_DIR` path doesn't exist (Path("/Volumes/Storage-1/Hermes/wiki") — external volume)
- `parse_transcript_for_summary()` hits encoding errors in transcript files
- `get_recent_transcript_files()` fails on permission/path issues

**Fix needed:** Add `mkdir(parents=True, exist_ok=True)` before file writes, add better exception handling around transcript parsing.

## Verifying Context File Was Written

```bash
# Check if session resume context exists
ls -la ~/.hermes/.recent_session_context.txt 2>/dev/null && echo "EXISTS" || echo "NOT CREATED"

# Check if wiki session context exists
ls -la ~/.hermes/.wiki_session_context.txt 2>/dev/null && echo "EXISTS" || echo "NOT CREATED"

# Check file content
cat ~/.hermes/.wiki_session_context.txt | head -50
```
