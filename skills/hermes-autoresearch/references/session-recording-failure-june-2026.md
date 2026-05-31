# Session Recording Failure — June 1, 2026

**Date:** 2026-06-01 | **Status:** ACTIVE — 4 days broken

## Symptom

Hermes Agent user sessions are NOT being logged to the sessions directory:
- `~/Library/Application Support/hermes-agent/sessions/` — no new session files since May 28
- `sessions.db` — empty/0 bytes
- Cron jobs still running (evidence: cron output directories have fresh timestamps)
- Daily review (`5aea298eb0a8`) ran successfully at 00:08 June 1 but found **0 sessions**

## Timeline

| Date | Status |
|------|--------|
| May 28 | Last session logged (`20260528_100915_c553799e.jsonl`) |
| May 29 | ⚠️ No sessions recorded |
| May 30 | ⚠️ No sessions recorded |
| May 31 | ⚠️ No sessions recorded |
| June 1 | ⚠️ No sessions recorded |

## Diagnosis Checklist

Run ALL of these to diagnose:

```bash
# 1. Check session files by date
ls -lat ~/Library/Application\ Support/hermes-agent/sessions/ | head -10

# 2. Check sessions.db
ls -la ~/Library/Application\ Support/hermes-agent/sessions/sessions.db
file ~/Library/Application\ Support/hermes-agent/sessions/sessions.db

# 3. Check cron output (confirms cron scheduler working)
ls -lt ~/.hermes/cron/output/ | head -5

# 4. Check disk space
df -h ~

# 5. Check hermes service status
ps aux | grep hermes | grep -v grep
```

## Possible Root Causes

| Cause | Evidence | Check |
|-------|---------|-------|
| Disk full | `df -h ~` shows 100% | Free space |
| Permission changed | sessions/ not writable | `touch ~/Library/Application\ Support/hermes-agent/sessions/test` |
| sessions.db corruption | 0 bytes | Check file size + `file` command |
| Hermes session service crash | Service not running | `ps aux \| grep hermes` |
| sessions/ path changed | Config mismatch | Check `config.yaml` for sessions_dir |

## Impact

- **Daily Session Review cron** cannot analyze sessions → no decision/revenue/learnings extraction
- **ByteRover memory** cannot auto-capture session learnings
- **Autoresearch** cannot extract decisions from session logs
- **Context compression** may still work but without session continuity

## Investigation Commands

```bash
# Check sessions directory
ls -la ~/Library/Application\ Support/hermes-agent/sessions/

# Check sessions.db
file ~/Library/Application\ Support/hermes-agent/sessions/sessions.db
stat ~/Library/Application\ Support/hermes-agent/sessions/sessions.db

# Check last session
ls -lat ~/Library/Application\ Support/hermes-agent/sessions/ | head -5

# Try writing to sessions dir
touch ~/Library/Application\ Support/hermes-agent/sessions/test_write
ls -la ~/Library/Application\ Support/hermes-agent/sessions/test_write

# Check hermes gateway process
ps aux | grep -i hermes | grep -v grep

# Check sessions config
grep -r "sessions" ~/.hermes/config.yaml 2>/dev/null
```

## Known Working Cron Jobs (as of June 1)

```
5aea298eb0a8  Daily Session Review    0AM     ✅ Ran (found 0 sessions)
7cba6ba5f52a  Hermes Daily Backup    3AM     ✅ Ran
a5c02f2f0d87  Hermes X Research     7AM     ✅ Ran
a303e13       vault backup           hourly  ✅ Running
```

**Conclusion:** Cron scheduler working, but session recording service broken.
