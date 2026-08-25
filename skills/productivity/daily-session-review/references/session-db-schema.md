---
title: Hermes Session DB Schema + Queries
date: 2026-06-21
type: reference
tags: [sqlite, session-db, schema, query]
---

# Hermes Session DB — Schema + Query Patterns

**DB path:** `~/.hermes/state.db`

## Schema

### sessions table
```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,        -- 'cron', 'telegram', etc.
    title TEXT,
    user_id TEXT,
    model TEXT,
    parent_session_id TEXT,
    started_at REAL NOT NULL,    -- Unix timestamp (REAL)
    ended_at REAL,               -- Unix timestamp (REAL)
    end_reason TEXT,
    message_count INTEGER DEFAULT 0,
    tool_call_count INTEGER DEFAULT 0,
    ...
);
-- NOTE: There is NO `last_active` column. Use `message_count` or `ended_at` instead.
```

### messages table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,     -- FK to sessions.id
    role TEXT NOT NULL,          -- 'user' | 'assistant' | 'tool'
    content TEXT,
    tool_call_id TEXT,
    tool_calls TEXT,
    tool_name TEXT,
    timestamp REAL NOT NULL,     -- Unix timestamp (REAL)
    ...
);
```

## Key Queries

### Get sessions from last 24h
```python
import datetime
now_ts = int(datetime.datetime.now().timestamp())
ago_24h = now_ts - 86400

# In bash:
sqlite3 ~/.hermes/state.db "SELECT id, source, title, started_at FROM sessions WHERE started_at >= ${ago_24h} AND started_at < ${now_ts} ORDER BY started_at DESC;"
```

### Get messages from a session
```bash
sqlite3 ~/.hermes/state.db "SELECT session_id, role, substr(content, 1, 500) FROM messages WHERE session_id = 'session_id_here' ORDER BY timestamp LIMIT 10;"
```

### Get sessions by source
```bash
sqlite3 ~/.hermes/state.db "SELECT id, title, started_at FROM sessions WHERE source = 'cron' ORDER BY started_at DESC LIMIT 10;"
```

### Get sessions with title (null-safe)
```bash
sqlite3 ~/.hermes/state.db "SELECT id, source, title, started_at FROM sessions WHERE title IS NOT NULL ORDER BY started_at DESC LIMIT 20;"
```

### Filter sessions by keyword in title
```bash
sqlite3 ~/.hermes/state.db "SELECT id, source, title, started_at FROM sessions WHERE title LIKE '%Content Creator%' ORDER BY started_at DESC LIMIT 20;"
```

### Count messages per session
```bash
sqlite3 ~/.hermes/state.db "SELECT session_id, COUNT(*) as msg_count FROM messages WHERE session_id IN (SELECT id FROM sessions WHERE started_at >= ${ago_24h}) GROUP BY session_id ORDER BY msg_count DESC;"
```

## Common Pitfalls

1. **`datetime('now', '-24 hours')` does NOT work** on Unix timestamp columns — returns empty results. Always use raw Unix timestamps.

2. **`WHERE role = 'user'`** — user messages have role='user', assistant have role='assistant'. Tool calls have role='tool'.

3. **Large content** — `substr(content, 1, N)` limits output. Full content can be 200KB+.

4. **Schema inspect:**
   ```bash
   sqlite3 ~/.hermes/state.db ".schema sessions"
   sqlite3 ~/.hermes/state.db ".schema messages"
   ```

## Related
- [[daily-session-review]]
