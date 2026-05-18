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

### WikiMemoryProvider Architecture

The WikiMemoryProvider (`~/.hermes/plugins/memory/wiki/__init__.py`) is the **active write loop** that supplements ByteRover. It has these lifecycle hooks:

### What WikiMemoryProvider Does at Session Start ✅

`initialize()` calls `_load_wiki_context()` which loads exactly the 5 files from `start-here.md`:

```
WIKI_STARTUP_FILES = [
    ("_meta/start-here.md", False),
    ("SCHEMA.md", False),
    ("index.md", False),
    ("log.md", True),           # last 20 lines only
    ("entities/learned-about-tuananh.md", False),
]
```

This matches `start-here.md`'s "Session Startup Sequence" items 1-5 exactly. ✅

### What WikiMemoryProvider Does NOT Do (gap) ❌

| Missing | start-here.md says | Reality |
|---------|-------------------|---------|
| **Projects scan** | "6. Scan projects/ directory → Quick check for active projects" | WikiMemoryProvider only injects files into system prompt, does NOT scan `projects/` or present active projects to user |
| **User project selection** | "7. Present project summary → Let Anh choose which project to work on" | Not automated — user has to manually say "work on project X" |
| **Git push auto-sync** | None (this is our own addition) | Only writes local files, no auto-git-push after wiki writes |

### Gap Resolution — RESOLVED 2026-05-18 ✅

Both gaps have been implemented:

| Missing | Resolution | Implementation |
|---------|------------|----------------|
| **Projects scan** | ✅ Added | `_load_project_summary()` in `WikiMemoryProvider.initialize()` — scans `projects/` subdirs, reads `hub.md` for each, injects active projects list into system prompt |
| **Git push auto-sync** | ✅ Added | `_git_push_async()` (daemon thread), `_trigger_git_push()` (session-end immediate), `_maybe_git_push()` (checkpoint rate-limited 5min) |
| **User project selection** | Manual | User says what they want; system prompt includes projects list |
| **Telegram bot messages** | ✅ Fixed | Disabled privacy mode via @BotFather — Hermes now reads messages from other bots in group |

### Checkpoint Recovery Flow

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

## Wiki Self-Heal (Auto-Fix Broken Wikilinks)

### CRITICAL Bug: Case-Sensitivity (2026-05-18)

**Symptom:** `wiki_self_heal.py --fix --links` báo "Created X stubs" nhưng count = 0 dù có 5500+ broken links.

**Root cause:** Two bugs working together:
1. `_safe_slug()` trả về `"Foundation"` (case nguyên) nhưng `get_existing_pages()` lowercase hết → `"foundation"`. Kết quả: `"Foundation" not in existing_pages` = True → link bị đánh là "broken" dù page tồn tại.
2. Path-separator links (`[[projects/foo]]`) bị skip thay vì convert thành `projects-foo`.

**Fix in `wiki_self_heal.py`:**
```python
# Patched: _safe_slug() line ~265 — MUST return lowercase
def _safe_slug(title: str) -> str:
    normalized = re.sub(r'[\[\]`"\*_]', '', title.strip())
    return normalized.replace("/", "-").lower()  # ← .lower() is critical

# Patched: get_existing_pages() line ~192 — handle path-based wikilinks
pages.add(full_stem.replace("/", "-"))  # ← Convert path/ to path-
```

**Result after fix:** 0 broken links (từ 5531), stubs created = 0 (vì links đã match existing pages).

**⚠️ PITFALL: Two tools, different counts — always run both**

| Tool | Broken Link Count | Regex/Logic | Use |
|------|-------------------|-------------|-----|
| `wiki_self_heal.py --fix --links` | 0 after fix | Slug-based match, lowercase | Auto-fix stubs |
| `wiki_semantic_health.py` | 743 | Filename-based, reports edge cases | Edge case audit |

**Why discrepancy:** `semantic_health` catches edge cases self_heal misses:
- Empty wikilinks: `[[...]]`
- Raw/ path links: `[[raw/transcripts/...]]` (raw/ intentionally excluded)
- Self-referential: `[[self-healing-wiki]]` in self page
- Links with spaces: `[[double brackets]]` — link text contains space, breaks slug match

**Correct workflow:** Run BOTH — self_heal for fix, semantic_health for edge case audit.
Never trust only one tool's count.

### Two Health Tools, Different Counts

| Tool | Broken Link Count | Regex/Logic |
|------|-------------------|-------------|
| `wiki_self_heal.py` | 0 after fix | Slug-based match, lowercase |
| `wiki_semantic_health.py` | 743 | Filename-based, reports edge cases |

**Why discrepancy:** `semantic_health` catches edge cases the other misses:
- Empty wikilinks: `[[...]]`
- Raw/ path links: `[[raw/transcripts/...]]` (raw/ is intentionally excluded from wiki)
- Self-referential: `[[self-healing-wiki]]` in `concepts/self-healing-wiki.md`
- Links with spaces: `[[double brackets]]`

**Action:** Run BOTH — `self_heal.py --fix --links` for auto-fix, `semantic_health.py` for edge case audit.

### Cron Auto-Fix (4AM)

**Before (2026-05-18):** `wiki_health.sh` chỉ chạy `wiki_semantic_health.py` (detect-only, no fix).

**After (2026-05-18):** Two phases:
1. Phase 1: `wiki_semantic_health.py` → health score + JSON report
2. Phase 2: `wiki_self_heal.py --fix --links` → auto-fix broken wikilinks + log stubs count

### Related Files
- `/Volumes/Storage-1/Hermes/wiki/scripts/wiki_self_heal.py` — auto-fix broken links
- `/Volumes/Storage-1/Hermes/wiki/scripts/wiki_semantic_health.py` — health scoring + edge case audit
- `~/.hermes/scripts/wiki_health.sh` — cron script (48 lines, patched 2026-05-18)

### Path Separator Bug in `wiki_semantic_health.py` (RESOLVED 2026-05-18)

**Symptom:** `wiki_semantic_health.py` báo 743 broken wikilinks — false positives từ path-separator links như `[[skills/index]]`, `[[projects/nexus]]`.

**Root cause:** Lines 143, 167, 221 dùng regex capture group `${target}` nhưng **không normalize `/` thành `-`**. Kết quả `[[skills/index]]` → `skills/index` (slash giữ nguyên) → không khớp filename `skills-index.md` → báo broken.

**Fix (2026-05-18):** Thêm `.replace("/", "-")` vào 3 lines:
```python
# Line 143, 167, 221 — BEFORE:
target_normalized = re.sub(r'[\[\]`"*_]', '', m.group(1).strip())

# AFTER (PATCHED):
target_normalized = re.sub(r'[\[\]`"*_]', '', m.group(1).strip().replace("/", "-"))
```

**Commit:** `e82432b` — "fix: normalize / to - in wikilink path separator (lines 143,167,221)"

**Note:** Đây là bug RIÊNG BIỆT với `_safe_slug()` case-sensitivity bug trong `wiki_self_heal.py`. Cả hai đều gây false positive broken link reports nhưng có nguyên nhân khác nhau.

### Remaining Issues (743 broken per semantic_health)

Sau khi fix path separator, `wiki_semantic_health.py` vẫn báo ~743 broken links — đây là edge cases THỰC SỰ mà `wiki_self_heal.py` không xử lý:

| Type | Example | Action |
|------|---------|--------|
| Empty wikilinks | `[[...]]` in `projects/nexus/SPEC.md` | Manual review — may be draft content |
| Raw/ links | `[[raw/transcripts/...]]` | Intentional — raw/ excluded from wiki |
| Self-referential | `[[self-healing-wiki]]` in self page | Manual review — ignore in audit |
| Missing concepts | `[[assembly]]` | Create content stub with real info |
| 389 bad stubs | `projects-...`, `raw-...`, `knowledge_graph.py.md` | Need cleanup — from early path-separator bug run |

**⚠️ Action item:** 389 bad stubs cần được xóa khỏi `concepts/` — đây là artifacts từ lúc path separator bug chưa fix, tạo stubs với tên sai.

## Related

- `hermes-agent` — for gateway and agent configuration
- `memory` tool — for in-session memory management