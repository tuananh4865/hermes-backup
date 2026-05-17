---
name: hermes-memory
description: ByteRover-powered agent memory — auto-capture, query, and verify knowledge across sessions. Covers brv CLI, knowledge sync script, daily cron automation, and session review workflow. Use when user asks to "remember this", "save to memory", "what do you know about X", or when session produces durable learnings.
triggers:
  - "remember this"
  - "what do you know about"
  - "save to memory"
  - "check memory"
  - "update knowledge"
  - Session end — auto-capture learnings
  - User corrects approach/workflow
---

# Hermes Memory — ByteRover-Powered Knowledge Management

## Core Concept

ByteRover is Hermes Agent's persistent knowledge tree. It survives context compression and session boundaries. The goal is a full cycle: **capture → store → query → verify**.

## Critical Workflow: Session File Deletion

**NEVER delete session files without first extracting and saving knowledge.**

```
Session file deletion workflow:
1. READ the session file (json/jsonl)
2. Extract: user facts, preferences, learnings, tasks completed, decisions, errors fixed
3. SAVE to ByteRover via brv curate
4. THEN delete the session file
```

Failure to follow this order = permanent loss of knowledge that took time to accumulate.

## ByteRover CLI

```bash
brv status                    # Show memory tree stats, version
brv curate "knowledge item"  # Add to knowledge tree (sync, can timeout)
brv curate "knowledge" --detach  # Add async (use this for scripts)
brv curate view --since 24h   # View recent curated items
brv query "topic"            # Query knowledge (TIMEOUTS in practice — use with caution)
brv query-log                 # Show query statistics
```

## Knowledge Sync Script

Location: `~/.hermes/scripts/byterover_knowledge_sync.py`

```bash
python3 ~/.hermes/scripts/byterover_knowledge_sync.py --days-ago 1
```

What it does:
1. Finds sessions from N days ago
2. Extracts: user_facts, preferences, learnings, tasks_completed, decisions
3. Curates each to ByteRover with `--detach` (async, non-blocking)
4. Reports count of items synced

## Daily Automation (Cron Jobs)

Two jobs run automatically:

| Job | Schedule | Purpose |
|-----|----------|---------|
| ByteRover Knowledge Sync Daily | `0 1 * * *` | Sync previous day's sessions → ByteRover |
| ByteRover Health Check Daily | `0 6 * * *` | Verify ByteRover status + curate history |

Both deliver results to Telegram.

## What to Curate

After each session or significant task, curate:

- **User facts**: "Anh prefers X", "User's name is Tuấn Anh"
- **Preferences**: "communication: Vietnamese casual", "response_style: concise"
- **Learnings**: "Fixed bug by doing X", "Technique Y works better than Z"
- **Tasks completed**: "Set up cron job X", "Created skill Y"
- **Decisions**: "Chose approach X because Y"
- **Errors fixed**: "Solution to error: do Y instead of Z"

Format: `"type: content"` e.g. `"fact: user prefers concise responses"`

## Query Patterns

When user asks "what do you know about X":
1. Try `brv query "X"` — may timeout, handle gracefully
2. Fall back to `session_search(query="X")` for session history
3. Combine results, present what's relevant

## Session Review at Session End

Before ending a session, always ask: "Anything from this session worth curating to ByteRover?"

Common patterns:
- User corrected your approach → save as learning
- New preference discovered → save immediately  
- Non-trivial fix discovered → save for future reference
- Project context established → save for continuity

## WikiMemoryProvider Architecture

The WikiMemoryProvider (`~/.hermes/plugins/memory/wiki/__init__.py`) is the **active write loop** that supplements ByteRover. It has these lifecycle hooks:

### Exists ✅
| Hook | When | What it does |
|------|------|-------------|
| `sync_turn()` | After every turn | Accumulates conversation + triggers rolling checkpoint every N turns |
| `_sync_fact_realtime()` | After every turn | Writes key facts to MEMORY.md in real-time (survives crash/compression) |
| `_warm_session_search()` | On initialize | Pre-loads recent sessions from SQLite FTS5 |
| `on_pre_compress()` | Before context compression | Writes `~/.hermes/checkpoints/pre_compact_<session_id>.md` |
| `on_session_end()` | On session end | Writes rolling checkpoint + appends to wiki/log.md + TASK_STATE.md |
| `prefetch()` | On every user query | Hybrid BM25+semantic retrieval, topic-parsing, injects into system prompt |

### Missing ❌ — Resolved ✅
| Hook | Needed for | Status |
|------|-----------|--------|
| `on_post_compress()` | Read the `pre_compact_*.md` checkpoint AFTER compression and inject task state into fresh context | **RESOLVED** — implemented at line 1499 in `~/.hermes/plugins/memory/wiki/__init__.py`. Checkpoint is read post-compaction via `_proactive_retrieve_from_checkpoint()` |

### Checkpoint Recovery Flow
```
on_pre_compress()  → writes pre_compact_<session>.md
[compression happens]
on_post_compress() → reads pre_compact_<session>.md → _proactive_retrieve_from_checkpoint()
                        → injects structured task state into fresh context
```

**⚠️ PITFALL**: Session state is NOT lost after compaction anymore — the recovery loop is complete.

### Checkpoint Files
```
~/.hermes/checkpoints/
├── pre_compact_<session_id>.md    # Written by on_pre_compress() — NOT read after compaction
├── session_state_<session_id>.md  # Written by on_session_end()
├── TASK_STATE.md                   # Current task progress
└── DECISION_LOG.md                 # Session decisions log
```

### Real-Time Memory Sync (Every Turn)
Every turn calls `_sync_fact_realtime()` which writes to `~/.hermes/memories/MEMORY.md` — a rolling bounded log (last 20 entries). This survives compaction and process crash.

## Related

- `hermes-agent` — for gateway and agent configuration
- `memory` tool — for in-session memory management