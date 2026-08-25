# Daily Session Review — Methodology

## Purpose
Every night at 0AM, read all session logs from the day, extract structured knowledge, update wiki + knowledge graph, index for retrieval, report to Anh.

## Session Log Locations
```
~/.hermes/hermes-agent/sessions/        # sessions.json = POINTER/index (NOT content)
~/.hermes/hermes-agent/gateway/sessions/ # session_YYYYMMDD_HHMMSS_*.json = actual content
~/Library/Application Support/hermes-agent/sessions/
~/.hermes/state.db                      # SQLite — actual message content (primary source)
```

**⚠️ sessions.json is a POINTER, not content:**
- `sessions.json` maps channel keys → session IDs (e.g., `agent:main:telegram:dm:1132914873: 20260605_204615_66faf874`)
- Actual messages are in `state.db` with schema: `messages(timestamp, session_id, role, content)`
- Timestamp is Unix epoch float (e.g., `1780668655.9761` = `2026-06-05 21:10:55`)
- Cron output files at `~/.hermes/cron/output/{job_id}/` are RELIABLE indicators of what ran

**Query pattern for session content:**
```sql
-- Find sessions from a date range (June 5 = 1780592400 to 1780678800)
SELECT session_id, COUNT(*) as msg_count
FROM messages
WHERE timestamp >= 1780592400 AND timestamp < 1780678800
GROUP BY session_id
ORDER BY msg_count DESC;

-- Get messages from a specific session
SELECT substr(timestamp,1,19) as ts, role, substr(content,1,200)
FROM messages
WHERE session_id = '20260605_204615_66faf874'
ORDER BY timestamp;
```

## Extraction Framework

### 4 Categories Per Session

| Category | What to Extract |
|----------|----------------|
| **Decisions** | Technical choices, approach changes, what was picked over alternatives |
| **Revenue** | TikTok Shop insights, fees, commissions, product discoveries, pricing strategies |
| **Learnings** | New patterns, Gen Z slang, content strategies, tool discoveries |
| **Blockers** | Errors, failed approaches, what didn't work |

### Decision Heuristics
- "Chose X over Y because Z failed" → log the decision + reason
- "Discovered new tool/technique" → save to skills or wiki
- "User corrected X" → update relevant skill immediately
- "New Gen Z slang" → update `learned-about-tuananh.md`

## Wiki Update Targets

| File | When to Update |
|------|---------------|
| `wiki/log.md` | Always — append daily summary |
| `wiki/entities/learned-about-tuananh.md` | New preferences, slang, corrections |
| `wiki/queries/` | Research findings worth keeping |
| `wiki/index.md` | New pages created |

## Session ID Pattern (for cron jobs)
```
cron_{job_id}_{YYYYMMDD}_{HHMMSS}
```
Example: `cron_5aea298eb0a8_20260508_000045`

## Report Format
```markdown
## 🌙 Daily Review — YYYY-MM-DD

### ✅ Hoàn thành
- [Action] — [outcome]

### 🧠 Learnings
- [Key decision/insight]

### ⚠️ Cần xử lý
- [Blocker or pending]

### 📋 Action Items
- [ ] Item requiring human input
```

## Quality Gates
1. Extract minimum 1 decision, 1 learning, 1 blocker per session
2. Gen Z slang → always update `learned-about-tuananh.md`
3. Skill corrections → patch the relevant skill within 24h
4. Wiki health check after updates: `wiki_lint.py --fast`
