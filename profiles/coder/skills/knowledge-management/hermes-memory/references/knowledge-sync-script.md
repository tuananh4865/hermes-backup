# ByteRover Knowledge Sync Script

Location: `~/.hermes/scripts/byterover_knowledge_sync.py`

## What It Does

1. **Finds sessions** from specified days ago (default: 1)
2. **Extracts knowledge** using regex patterns:
   - `user_facts`: patterns like "X is Y", "X was Y"
   - `preferences`: "user prefers X"
   - `learnings`: "learned X", "fixed X"
   - `tasks_completed`: "done X", "completed X"
   - `decisions`: "chose X", "decided X"
3. **Curates to ByteRover** with `--detach` flag (async, non-blocking)
4. **Reports** items synced

## Usage

```bash
# Sync yesterday's sessions
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 1

# Sync N days ago
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 3
```

## Output Example

```
[ByteRover Knowledge Sync] Running for 1 day(s) ago...
Found 9 sessions
Extracted: 487 items
Curated 37/37 items to ByteRover
[ByteRover Knowledge Sync] Complete!
```

## Key Implementation Notes

- Uses `--detach` flag to avoid blocking on brv curate timeout
- 5-second timeout per curate call
- Deduplicates extracted items before curating
- Query verification step disabled (brv query times out in practice)

## Cron Setup

The sync runs automatically at 1AM daily via cron job `ffda9e65a08b`.

The health check runs at 6AM daily via cron job `ba3953434244`.

Both deliver to Telegram.

## Testing the Script

```bash
# Test with today's sessions
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 0
```

## Troubleshooting

**brv curate times out**: Script uses `--detach` to queue async. Check `brv curate view --since 1h` for status.

**No sessions found**: Check date prefix format in `~/.hermes/sessions/`. Expected format: `session_YYYYMMDD_*.json`

**Script errors**: Check Python version (uses Python 3.9+ features). Verify `~/.hermes/sessions/` directory exists.