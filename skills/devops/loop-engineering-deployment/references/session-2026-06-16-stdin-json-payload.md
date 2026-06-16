# Session 2026-06-16 — Hermes Shell Hook Stdin JSON Discovery

## TL;DR

Hermes shell hooks pass payload as **JSON on stdin**, not as environment variables. The existing SKILL.md and `transcript-saver-v2` hook both assumed env vars (`$RESPONSE`, `$MESSAGE`, etc.) — this was wrong. The hook registered as `✓ allowed` but the Python handler exited 0 with no output and no file created.

## What went wrong

### Assumption (WRONG)

```bash
# hook_wrapper.sh
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
exec python3 "$HERMES_HOME/hooks/transcript-saver-v2/handler.py" "$@"
```

```yaml
# config.yaml
hooks:
  on_session_end:
    - command: "/Users/tuananh4865/.hermes/hooks/transcript-saver-v2/hook_wrapper.sh --event agent_end --output \"$RESPONSE\" --message \"$MESSAGE\" --session_id \"$SESSION_ID\" --platform \"$PLATFORM\" --user_id \"$USER_ID\""
      timeout: 10
```

**Assumed:** Hermes exports `$RESPONSE`, `$MESSAGE`, `$SESSION_ID`, `$PLATFORM`, `$USER_ID` as env vars when invoking the hook.

**Reality:** Those env vars are NEVER set. Hermes passes a JSON payload on stdin. The bash variables `$RESPONSE` etc. just expand to empty strings, the wrapper passes them as empty argparse args, and the Python handler sees `args.response = ""` and exits.

### The fix

#### 1. Bash wrapper — strip the env-var args

```bash
# CORRECT — no env-var substitution
exec python3 "$HERMES_HOME/hooks/transcript-saver-v2/handler.py" "$@"
```

The bash wrapper's job is just to set `HERMES_HOME` and exec Python. The `--event` arg can stay (for testing), but `--output`/`--message`/etc. are useless.

#### 2. Python handler — read stdin JSON

```python
if __name__ == "__main__":
    import sys, json
    # ... argparse setup ...
    args = parser.parse_args()

    # NEW: read Hermes JSON payload from stdin
    if not sys.stdin.isatty():
        try:
            payload = json.loads(sys.stdin.read())
            args.event = payload.get("hook_event_name", args.event)
            args.session_id = payload.get("session_id", args.session_id)
            extra = payload.get("extra", {})
            args.response = extra.get("response", args.response)
            args.message = extra.get("message", args.message)
            args.platform = extra.get("platform", args.platform)
            args.user_id = extra.get("user_id", args.user_id)
        except (json.JSONDecodeError, Exception) as e:
            print(f"[hook] stdin parse failed: {e}", flush=True)

    event = args.event.replace(":", "_") if args.event else "agent_end"
    handle(event, {...})
```

## How to find this in the future (without rediscovering)

1. `find ~/.hermes/hermes-agent -name "shell_hooks.py"` — `_spawn()` function shows `input=stdin_json`
2. `grep -A 5 "_serialize_payload" ~/.hermes/hermes-agent/agent/shell_hooks.py` — shows the JSON schema
3. Add `print(f"[hook] stdin={sys.stdin.read()[:200]!r}", flush=True)` to handler — see what Hermes actually sends

## Diagnostic sequence for any "hook fires but does nothing" symptom

```bash
# Step 1: Confirm hook is registered and allowed
hermes hooks list | grep YOUR_HOOK
# Status should be "✓ allowed"

# Step 2: Trigger hook manually with stdin JSON (the format Hermes actually uses)
echo '{"hook_event_name":"on_session_end","session_id":"test_001","extra":{"response":"test","message":"[User] test","platform":"telegram","user_id":"123"}}' \
  | python3 ~/.hermes/hooks/YOUR_HOOK/handler.py --event on_session_end

# If THIS works but the hook doesn't fire from real messages → the wrapper or config is wrong
# If THIS doesn't work → the Python handler has a bug (event filter, missing import, etc.)

# Step 3: Check if Hermes can actually invoke the wrapper
# Add debug print to the wrapper itself:
# echo "[wrapper] argv=$@" >&2
# echo "[wrapper] env=$(env | grep -E 'RESPONSE|MESSAGE' || echo NONE)" >&2
# exec python3 ...
```

## The other bug found in the same session

**Event name form mismatch.** Handler checked `if event_type != "agent:end"` (colon). The actual `hook_event_name` from Hermes is `"on_session_end"` (underscores). The colon form appears in the old Hermes plugin hook docs but is silently NEVER fired in shell-hook mode (issue NousResearch/hermes-agent#14583).

**Fix:** Accept all valid forms:
```python
END_EVENTS = (
    "agent:end", "agent_end",        # legacy Python plugin form
    "on_session_end",                 # actual Hermes shell-hook form
)
if event_type not in END_EVENTS:
    return
```

## Lessons

1. **Source of truth is `agent/shell_hooks.py`, not blog posts or older docs.** The `_spawn` function takes `stdin_json` as a parameter — that's the delivery mechanism.
2. **Test the EXACT format the real invoker uses, not a simplified CLI form.** The earlier "E2E test" used CLI args and passed. Real Hermes invocation uses stdin JSON — the handler must handle BOTH.
3. **`hermes hooks list` shows `✓ allowed` does NOT mean the hook works.** It just means the allowlist accepted the command. The Python handler can still silently fail.
4. **Always do a final E2E test by sending a real Telegram message.** Don't trust CLI tests alone.

## Files changed in this session

- `~/.hermes/hooks/transcript-saver-v2/handler.py` — added stdin JSON parser in `__main__` block; added `on_session_end` to accepted events
- `~/.hermes/hooks/transcript-saver-v2/hook_wrapper.sh` — same (no change needed, but the previous env-var args in config.yaml were a no-op)
- `~/.hermes/config.yaml` — hooks block still has the env-var args (harmless, they expand to empty), but the new stdin JSON path is what actually delivers data
- This reference doc
- Main SKILL.md — added "🚨 CRITICAL: Hermes Shell Hooks Pass JSON via STDIN" section
