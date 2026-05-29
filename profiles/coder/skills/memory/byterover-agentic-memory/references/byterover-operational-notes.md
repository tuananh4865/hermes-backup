# ByteRover Operational Notes

## Confirmed Daemon Behavior

**Process structure:**
- `brv-server.js` — main daemon process
- `agent-process.js` — curation worker process
- Both run as independent Node.js processes, managed by ByteRover CLI

**Check status:**
```bash
ps aux | grep -E "brv-server|agent-process" | grep -v grep
brv status
```

## ByteRover Command Behavior

### curate (reliable)
- `brv curate "text" --detach` — submits and returns immediately
- Processing happens async in daemon
- Queue status: `brv curate view --since 10m`
- Items show "processing" for ~30s then clear

### query (unreliable — timeout ~30s)
- `brv query "text" --timeout 10` — times out after ~30s regardless
- Fallback chain:
  1. Retry with `--timeout 5`
  2. If still fail, use `session_search()` 
  3. If session_search fails, use `memory tool`
  4. Log: "ByteRover query failed - used [fallback]"

## Session Cleanup Rule (CRITICAL)

**NEVER delete session .jsonl files until:**
1. Session read and contents understood
2. All facts/preferences/learnings extracted
3. Curated into ByteRover with `--detach`
4. Verified (query back to confirm)

**Confirmed failure case:** 50 sessions from before 2026-05-01 were deleted without curation — knowledge lost. This must never happen again.

## Cron Job Integration

| Job | Schedule | Purpose | Job ID |
|-----|----------|---------|--------|
| Knowledge Sync Daily | `0 1 * * *` | Parse sessions → curate facts | `ffda9e65a08b` |
| Health Check Daily | `0 6 * * *` | Verify ByteRover operational | `ba3953434244` |

Both use `no_agent: true` (script-only, not LLM-driven).

## Disk Usage

- Session directory: `~/.hermes/sessions/` (~282MB, 924 files as of 2026-05-16)
- Session files: `*.jsonl` (one JSON line per message pair)
- ByteRover project: `~/.hermes/byterover/` (managed by ByteRover)

**Do not delete recent sessions** (from 2026-05-01 onward) — ~270MB, 36 files.

## Judge Model

User mentioned "judge model in /goal" — location not found in current session.
If encountered, check:
- `~/.hermes/goals/` directory
- Config `model.judge` or similar in `config.yaml`
- Cron job configurations

---

**Last updated:** 2026-05-16