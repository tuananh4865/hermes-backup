# ByteRover Knowledge Sync — Script Reference

## Script Location
`~/.hermes/scripts/byterover_knowledge_sync.py`

## Purpose
Parse session JSONL files → extract facts/preferences/learnings/tasks → curate into ByteRover.

## Usage

```bash
# Sync yesterday's sessions
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 1

# Sync last 7 days
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 7

# Sync specific session
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --session-id <session-id>
```

## Key Design Decisions

### 1. Detached Curate
All `brv curate` calls use `--detach` flag to avoid blocking:
```python
subprocess.run(["brv", "curate", f"fact: {fact}", "--detach"], ...)
```

### 2. Prefix Taxonomy
Curated items are prefixed for query precision:
- `fact:` — durable facts (tools, paths, configs)
- `preference:` — user preferences and habits
- `learning:` — techniques, fixes, approaches
- `task_completed:` — completed work with approach notes

### 3. Skip Verify (ByteRover Timeout)
`verify_old_knowledge()` is skipped because `brv query` times out (>30s).
Fallback: use `session_search()` instead.

### 4. Session JSONL Format
Each session file is one JSONL line with fields:
- `session_id`, `timestamp`, `user_message`, `assistant_response`, `tool_calls`

## ByteRover Daemon Behavior

The ByteRover daemon (`brv-server.js`, `agent-process.js`) runs as independent node processes.
When curations are submitted with `--detach`, they queue and process asynchronously.
The daemon maintains dream-state and curation history.

**Check daemon status:**
```bash
ps aux | grep -E "brv-server|agent-process" | grep -v grep
```

**Check queue:**
```bash
brv curate view --since 10m
```

## Cron Job Integration

Two cron jobs already configured:

| Job | Schedule | Script | Job ID |
|-----|----------|--------|--------|
| Knowledge Sync Daily | `0 1 * * *` | `python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 1` | `ffda9e65a08b` |
| Health Check Daily | `0 6 * * *` | Bash script: `brv status && brv curate view --since 24h` | `ba3953434244` |

## Critical: Session Cleanup Rule

**NEVER delete session history until:**
1. ✅ Session has been read
2. ✅ Facts/preferences/learnings/tasks extracted
3. ✅ Curated into ByteRover (with `--detach`)

Failure case: 50 sessions before 2026-05-01 were deleted without curation — lost knowledge.

## Troubleshooting

### Curation stuck in "processing"
ByteRover daemon is still running if processes exist:
```bash
ps aux | grep -E "brv-server|agent-process" | grep -v grep
```

### brv query timeout
Use `session_search()` as fallback. Document in skill.

### Slow sync
Check session directory size:
```bash
du -sh ~/.hermes/sessions/
```