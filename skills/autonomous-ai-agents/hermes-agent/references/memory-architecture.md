# Hermes Agent Memory Architecture

> Discovered: 2026-05-06 | Updated: 2026-05-06

## 6-Layer Memory Stack

| Layer | Component | Location | Purpose |
|-------|-----------|----------|---------|
| **1. Builtin Memory** | `MEMORY.md` + `USER.md` | `~/.hermes/memories/` | Persistent facts via `memory` tool |
| **2. Session Context** | `.wiki_session_context.txt` | `~/.hermes/` | Wiki session start cache (auto-loaded) |
| **3. Trajectory** | `trajectory_index.db` + `trajectory_samples.jsonl` | `~/.hermes/` | Past failure patterns for PatternMatcher |
| **4. Skills Snapshot** | `.skills_prompt_snapshot.json` | `~/.hermes/` | Active skills context |
| **5. Agent Memory Manager** | `memory_manager.py` + `memory_provider.py` | `~/.hermes/hermes-agent/agent/` | Orchestrates builtin + ONE external provider |
| **6. Wiki Provider** | `plugins/memory/wiki/__init__.py` | `~/.hermes/plugins/memory/wiki/` | **ACTIVE — full write loop** |

## WikiMemoryProvider (CUSTOM PLUGIN — PHASE 1+2 COMPLETE)

**Location:** `~/.hermes/plugins/memory/wiki/__init__.py` (~940 lines)
**Status:** Active (`memory.provider: wiki` in config.yaml)

### Phase 1: Write Loop (Complete 2026-05-06)

| Method | Status | What it does |
|--------|--------|--------------|
| `initialize()` | ✅ | Resets state, creates checkpoint dir, loads wiki context, warms session_search |
| `system_prompt_block()` | ✅ | Injects 5 wiki files at session start |
| `sync_turn()` | ✅ | Accumulates conversation, regex-tracks files_modified + decisions, real-time sync to MEMORY.md every turn |
| `on_session_end()` | ✅ | Writes to wiki/log.md + TASK_STATE.md + DECISION_LOG.md + auto-extract to MEMORY.md |
| `on_pre_compress()` | ✅ | Structured checkpoint BEFORE compression, survives compaction |
| `shutdown()` | ✅ | Writes final rolling checkpoint |

**Checkpoint outputs:**
- `~/.hermes/checkpoints/session_state_<session_id>.md` — rolling checkpoint (every 5 turns)
- `~/.hermes/checkpoints/pre_compact_<session_id>.md` — pre-compact checkpoint
- `~/.hermes/checkpoints/TASK_STATE.md` — session summary
- `~/.hermes/checkpoints/DECISION_LOG.md` — decision log

### Phase 2: Hybrid Retrieval (Complete 2026-05-06)

**Verified working (2026-05-06):**
```
Query "ByteRover" → Exact setup command ✅
Query "gemma-4-e2b" → Vision config + model list ✅
Query "memory" → User frustration entry ✅
```

| Method | Status | What it does |
|--------|--------|--------------|
| `retrieve_relevant_memory(query, k=8)` | ✅ **NEW** | Main entry — hybrid BM25 + semantic → RRF fusion |
| `_bm25_search()` | ✅ **NEW** | TF-IDF cosine similarity via sklearn (ngram 1-2, max 5000 features) |
| `_semantic_search()` | ✅ **NEW** | Character n-gram fingerprinting via numpy (no external embeddings) |
| `_rrf_fusion()` | ✅ **NEW** | Reciprocal Rank Fusion (BM25 0.6 + semantic 0.4, k=60) |
| `_collect_all_memory_entries()` | ✅ **NEW** | Gathers from MEMORY.md + USER.md + EPISODES.md + recent checkpoints |
| `prefetch()` | ✅ **UPDATED** | Now calls `retrieve_relevant_memory()` for query-relevant retrieval |

**Retrieval architecture:**
```
User query
    ↓
_collect_all_memory_entries() → MEMORY.md + USER.md + EPISODES.md + checkpoints
    ↓
         ┌─────────────────┐
BM25 search ──→ scores    semantic search ──→ scores
    (TF-IDF cosine)        (n-gram fingerprint)
         └────────┬────────┘
                  ↓
           _rrf_fusion()
           (0.6 BM25 + 0.4 semantic)
                  ↓
         Top 8 results
                  ↓
    Formatted + injected into context
```

**RRF Formula:** `RRF_score = weight * (1 / (k + rank + 1))` where k=60

**EPISODES.md:** `~/.hermes/memories/EPISODES.md` — session summaries for cross-session retrieval.

### ⚠️ Daemon Thread Exit Race (Fixed 2026-05-06)

```python
# WRONG — daemon threads die on process exit:
self._checkpoint_thread = threading.Thread(target=self._write_rolling_checkpoint, daemon=True)
self._checkpoint_thread.start()
# → checkpoint never written when process exits

# CORRECT — sync write on session end, thread with join on active session:
def on_session_end(self):
    self._write_rolling_checkpoint()  # SYNC, blocking

def _trigger_rolling_checkpoint(self):
    if self._checkpoint_thread and self._checkpoint_thread.is_alive():
        self._checkpoint_thread.join(timeout=2.0)  # wait for prior write
    self._checkpoint_thread = threading.Thread(target=self._write_rolling_checkpoint, daemon=True)
    self._checkpoint_thread.start()
```

**Remaining phases:** Phase 3 (session-start retrieval), Phase 4 (consolidation/forgetting), Phase 5 (entity tracking). See `wiki:concepts/hermes-memory-master-plan.md`.

**Checkpoint outputs:**
- `~/.hermes/checkpoints/session_state_<session_id>.md` — rolling checkpoint (updated every 5 turns)
- `~/.hermes/checkpoints/pre_compact_<session_id>.md` — pre-compact checkpoint (before compression)
- `~/.hermes/checkpoints/TASK_STATE.md` — session summary (task, files, decisions, blockers, next steps)
- `~/.hermes/checkpoints/DECISION_LOG.md` — decision log (timestamped, append-only)

**Active Write Loop behavior:**
1. Each `sync_turn()` accumulates conversation buffer + tracks files/decisions via regex
2. Every 5 turns → non-blocking daemon thread writes rolling checkpoint
3. On session end → structured summary written to all checkpoint files + wiki/log.md
4. Before context compression → pre-compact checkpoint survives compaction

## MemoryManager Architecture

```python
# ~/.hermes/hermes-agent/agent/memory_manager.py
class MemoryManager:
    def build_system_prompt()  → frozen snapshot at session start
    def prefetch_all(query, session_id)  → per-turn recall

    # Only ONE external provider allowed:
    self._has_external: bool  # once set, rejected if second external attempts
```

## How Each Layer Works

### Layer 1: Builtin Memory (`~/.hermes/memories/`)
- `MEMORY.md` — agent notes (conventions, tool quirks, procedures)
- `USER.md` — user profile (preferences, style, habits)
- Updated via `memory` tool: `memory(action='add', target='memory', content='...')`
- **Also auto-updated by WikiMemoryProvider.on_session_end()** — key facts extracted automatically

### Layer 2: Session Context (`.wiki_session_context.txt`)
- 32KB cache of wiki session-start files
- Updated by `session:start` hook in `gateway/run.py:3416`
- Auto-read at session start — no skill load needed
- Hook fires when `_is_new_session` is True

### Layer 3: Trajectory Index (`trajectory_index.db`)
- Stores patterns from past failures
- PatternMatcher queries this before each task
- Warning injection: "⚠️ Similar task failed 3x with CONTEXT_OVERFLOW"

### Layer 4: Skills Snapshot (`.skills_prompt_snapshot.json`)
- Frozen snapshot of all active skills
- Loaded into system prompt at session start
- Updated when skills change

### Layer 5: Agent Memory Manager
- `memory_manager.py` — orchestrates providers
- `memory_provider.py` — base class for providers
- Builtin provider: reads `MEMORY.md` + `USER.md`
- External provider slot: ONE allowed, configured via `memory.provider`

### Layer 6: Wiki Provider (FULLY OPERATIONAL)
- WikiMemoryProvider at `~/.hermes/plugins/memory/wiki/`
- Active in config (`memory.provider: wiki`)
- Reads wiki at session start ✅
- Writes to wiki on session end ✅ (as of 2026-05-06)
- Full write loop: sync_turn + on_session_end + on_pre_compress ✅

## External Memory Providers (for future evaluation)

| Provider | Pre-Compress Hook | Auto-Extract | Local | Cost | Status |
|----------|-------------------|--------------|-------|------|--------|
| **ByteRover** | ✅ Built-in | ✅ | ✅ | Free | Pending evaluation |
| Mem0 | ❌ | ✅ | ❌ | Paid | Pending evaluation |
| Honcho | ❌ | ✅ | ✅ (self-hosted) | Free/Paid | Pending evaluation |
| Holographic | ❌ | ❌ | ✅ | Free | Not evaluated |

**ByteRover has built-in pre-compression extraction** — Tuấn Anh plans to evaluate after Tier 1-4 complete.

## Verification Commands

```bash
# Check memory layers
ls -la ~/.hermes/memories/
cat ~/.hermes/memories/MEMORY.md | head -20

# Check wiki provider line count (should be ~940 lines now)
wc -l ~/.hermes/plugins/memory/wiki/__init__.py

# Verify hybrid retrieval methods exist
grep -c "def retrieve_relevant_memory\|def _bm25_search\|def _semantic_search\|def _rrf_fusion" \
  ~/.hermes/plugins/memory/wiki/__init__.py
# Should return: 4

# Check EPISODES.md
cat ~/.hermes/memories/EPISODES.md | head -20

# Check checkpoints
ls -la ~/.hermes/checkpoints/
```

## Remaining Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 3** | Session-start retrieval (query relevant at session start, not load all) | Partial (prefetch updated) |
| **Phase 4** | Consolidation (forgetting/eviction, importance scoring) | Not started |
| **Phase 5** | Cross-session entity tracking (Mem0-style entity extraction) | Not started |

**Full roadmap:** `wiki:concepts/hermes-memory-master-plan.md`
