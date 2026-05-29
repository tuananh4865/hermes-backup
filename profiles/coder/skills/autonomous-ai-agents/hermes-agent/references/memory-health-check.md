# Memory Health Check — Tuấn Anh's Agent Memory System

## System Overview

| Component | Location | Purpose |
|-----------|----------|---------|
| **Wiki** | `/Volumes/Storage-1/Hermes/wiki` | Primary knowledge base, 1,768 files |
| **Builtin memory** | `~/.hermes/memories/USER.md`, `MEMORY.md` | Lightweight fact injection |
| **Session DB** | `~/.hermes/state.db` | FTS5 search, 456 sessions, 20K+ messages |
| **Checkpoints** | `~/.hermes/checkpoints/` | Session state backups |
| **WikiMemoryProvider** | `~/.hermes/plugins/memory/wiki/` | Hybrid BM25+semantic retrieval |

## Memory Provider Stack

```
MemoryManager (agent/memory_manager.py)
├── Builtin MemoryStore (tools/memory_tool.py)
│   ├── MEMORY.md — agent notes
│   └── USER.md — user profile (600-900 bytes typical)
├── WikiMemoryProvider (plugins/memory/wiki/)
│   ├── Hybrid retrieval: BM25 (0.6) + semantic n-gram (0.4)
│   ├── sync_turn() — rolling checkpoint every 5 turns
│   ├── on_session_end() — summary → wiki/log.md
│   └── on_pre_compress() — structured backup
└── Session search (state.db FTS5)
```

## Quick Health Check Commands

```bash
# Wiki health
cd /Volumes/Storage-1/Hermes/wiki && python3 scripts/wiki_semantic_health.py 2>&1 | head -60

# Check builtin memory
wc -l ~/.hermes/memories/USER.md ~/.hermes/memories/MEMORY.md
cat ~/.hermes/memories/USER.md | head -10

# Check for corruption (garbage entries)
cat ~/.hermes/memories/USER.md | grep -E "^\\- \\[tool\\]|^\\- \\[file\\]|^\\- \\[model\\]|^\\- \\[preference\\]"

# Session DB stats
sqlite3 ~/.hermes/state.db "SELECT COUNT(*) as sessions FROM sessions; SELECT COUNT(*) as messages FROM messages;"

# Checkpoints
ls -la ~/.hermes/checkpoints/ | tail -10
```

## Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| **USER.md size** | 500-900 bytes | >1KB, <2KB | >2KB or garbage entries |
| **MEMORY.md size** | 300-600 bytes | >1KB | >2KB |
| **Wiki files** | 1,400-1,800 real files | >3,000 (stubs) | >5,000 |
| **Broken wikilinks** | <500 | 500-2000 | >2000 |
| **Stale pages** | 0 | 1-10 | >10 |
| **Orphan pages** | <100 | 100-300 | >300 |

## Corruption Patterns

### USER.md Corruption (Common)
**Pattern:** Lines like `[tool] the [HIGH]`, `[model] output [HIGH]`, `[file] py`
**Cause:** Session review tasks wrote raw LLM output instead of structured facts
**Fix:** Reset to clean structure + rebuild from wiki source

**Clean USER.md structure:**
```markdown
§ [PREFERENCES] — explicit preferences discovered over sessions
- communication: Vietnamese casual
- response_style: concise, no fluff
- tiktok_script_style: "anh" + "mấy con vợ"
§ [PROJECTS] — ongoing work
- tiktok-content: active
- hermes-agent: memory-optimizing
§ [FACTS] — durable facts about user, environment, tools
- communication: Vietnamese casual
- tiktok-content: active
§ [ENTITY_INDEX] — cross-session entity tracking
§ [GROWTH_LOG] — how user/agent improved
```

## Cleanup Procedure

1. **Backup first:**
   ```bash
   cp ~/.hermes/memories/USER.md ~/.hermes/memories/USER.md.bak.$(date +%Y%m%d%H%M%S)
   cp ~/.hermes/memories/MEMORY.md ~/.hermes/memories/MEMORY.md.bak.$(date +%Y%m%d%H%M%S)
   ```

2. **Check corruption extent:**
   ```bash
   cat ~/.hermes/memories/USER.md | grep -cE "^\\- \\[tool\\]|^\\- \\[file\\]|^\\- \\[model\\]|^\\- \\[preference\\]"
   ```

3. **If >10 garbage entries:** Reset to clean structure (see above)

4. **Rebuild from wiki** if needed: `entities/learned-about-tuananh.md` has user profile

## Wiki Retrieval Quality

The wiki uses hybrid BM25 + semantic retrieval. Quality depends on:
- Real content pages (not stubs <200 bytes)
- Proper frontmatter on all pages
- Cross-links between pages (min 2 wikilinks per page)
- Low orphan page count

**Verify wiki quality:**
```bash
# Count real content vs stubs
find wiki/concepts wiki/entities wiki/comparisons -name "*.md" -size +200c | wc -l
find wiki/concepts wiki/entities wiki/comparisons -name "*.md" -size -200c | wc -l

# Should be: real pages >> stubs
```

## Related

- `references/memory-cleanup-session-2026-05-21.md` — May 21 cleanup details
- `references/memory-architecture.md` — full 6-layer breakdown
- `references/memory-provider-architecture-gaps.md` — 3 critical gaps