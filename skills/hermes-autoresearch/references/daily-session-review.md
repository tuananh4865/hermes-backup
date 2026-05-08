# Daily Session Review — Methodology

## Purpose
Every night at 0AM, read all session logs from the day, extract structured knowledge, update wiki + knowledge graph, index for retrieval, report to Anh.

## Session Log Locations
```
~/.hermes/hermes-agent/sessions/
~/Library/Application Support/hermes-agent/sessions/
~/.hermes/hermes-agent/gateway/sessions/
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
