# WikiMemoryProvider Bug Fix — 2026-05-06

## Problem Summary

WikiMemoryProvider's `_auto_extract_to_memory()` **never worked**. Memory entries were never written to `~/.hermes/memories/MEMORY.md`, causing session data to be lost across sessions.

## Root Causes (3 bugs)

### Bug 1: Silent import failure
```python
# BROKEN — from plugin context, this import fails silently
def _auto_extract_to_memory(self, summary):
    try:
        from tools.memory_tool import MemoryStore, get_memory_dir  # ❌ FAILS
        memory_store = MemoryStore()
        ...
    except Exception as e:
        logger.debug(...)  # ❌ DEBUG = invisible
```

When called from `~/.hermes/plugins/memory/wiki/__init__.py`, the Python path doesn't include the agent's tools directory. The import raises `ModuleNotFoundError`, but `logger.debug()` swallows it.

### Bug 2: Wrong logging level
```python
except Exception as e:
    logger.debug("[wiki] Memory auto-extract skipped...")  # ❌ Invisible in logs
```

### Bug 3: on_pre_compress didn't extract to MEMORY.md
```python
def on_pre_compress(self, messages):
    # Only wrote checkpoint file — didn't call _auto_extract_to_memory()
    checkpoint_path.write_text(content)  # checkpoint file only
    return context_string  # memory NOT updated
```

The `on_pre_compress()` method wrote a checkpoint file but never extracted key facts to `MEMORY.md`. Only `on_session_end()` called `_auto_extract_to_memory()`, but that only fires on `/new` or `/reset`.

## The Fix

### 1. Direct file I/O — no imports
```python
MEMORY_FILE = Path.home() / ".hermes" / "memories" / "MEMORY.md"
USER_FILE = Path.home() / ".hermes" / "memories" / "USER.md"
ENTRY_DELIMITER = "\n§\n"

def _auto_extract_to_memory(self, summary):
    memory_file = self.MEMORY_FILE
    mem_dir = memory_file.parent
    mem_dir.mkdir(parents=True, exist_ok=True)
    
    # Read existing
    existing = self._read_memory_entries(memory_file)
    
    # Build new entries
    new_entries = []
    if summary.get("current_task"):
        new_entries.append(f"Task '{task_preview}' — session {sid[:8]}, {turns} turns")
    if summary.get("files_modified"):
        new_entries.append(f"Modified files: {', '.join(unique_files[-5:])}")
    if summary.get("decisions"):
        new_entries.append(f"Decisions: {'; '.join(decisions[-3:])}")
    
    # Write — keep last 20 entries
    all_entries = existing + new_entries
    trimmed = all_entries[-20:]
    memory_file.write_text(ENTRY_DELIMITER.join(trimmed), encoding="utf-8")
```

### 2. Call from on_pre_compress
```python
def on_pre_compress(self, messages):
    # ... existing checkpoint writing ...
    
    # CRITICAL: Extract to memory BEFORE compression destroys context
    try:
        self._auto_extract_to_memory({
            "session_id": self._session_id,
            "turn_count": self._turn_count,
            "tool_call_count": self._tool_call_count,
            "current_task": self._current_task,
            "files_modified": self._files_modified,
            "decisions": self._decisions,
            "blocked": self._blocked,
            "next_steps": self._next_steps,
        })
    except Exception as e:
        logger.warning("[wiki] on_pre_compress memory extract failed: %s", e)
```

### 3. Non-silent logging
```python
except Exception as e:
    logger.warning("[wiki] Memory auto-extract failed (NON-SILENT): %s", e)
    import traceback
    logger.warning("[wiki] Traceback: %s", traceback.format_exc())
```

## What Gets Extracted

| Entry Type | Example |
|-----------|---------|
| Task | `Task 'Fix memory system' — session abc123, 12 turns` |
| Files | `Modified files: wiki/__init__.py, config.yaml` |
| Decisions | `Decisions: chose direct file I/O; kept simple` |
| Blockers resolved | `Resolved blockers: import failure, logging level` |
| Tool count | `Session abc123: 12 turns, 34 tool calls` |

## Verification

```bash
# Test the fix
python3 -c "
import sys; sys.path.insert(0, '/Users/tuananh4865/.hermes/plugins/memory/wiki')
from wiki import WikiMemoryProvider
wp = WikiMemoryProvider()
wp._auto_extract_to_memory({'session_id': 'test', 'turn_count': 1, 'tool_call_count': 0, 'current_task': 'test', 'files_modified': ['test.py'], 'decisions': ['test'], 'blocked': [], 'next_steps': []})
print(open('/Users/tuananh4865/.hermes/memories/MEMORY.md').read()[-500:])
"

# Check actual content
cat ~/.hermes/memories/MEMORY.md
```

## Memory Extraction Triggers

### Real-Time (2026-05-06 Upgrade)
```python
def sync_turn(self, user_content, assistant_content, session_id):
    self._turn_count += 1
    # ... existing tracking ...
    self._trigger_rolling_checkpoint()
    # REAL-TIME: Write quick fact to MEMORY.md every turn
    self._sync_fact_realtime()
```

`sync_turn()` fires after EVERY completed turn. `_sync_fact_realtime()` writes a single deduplicated fact to MEMORY.md — fast, no LLM, just file I/O.

### Event-Driven (original)
- `on_pre_compress()` → before context compaction (context ≥75% full) + calls `_auto_extract_to_memory()`
- `on_session_end()` → when `/new` or `/reset` + calls `_auto_extract_to_memory()`

### What Gets Extracted

| Entry Type | Trigger | Example |
|-----------|---------|---------|
| Task | Per-turn (dedup) | `Task 'Kiểm tra memory' — 2 turns` |
| Files | Per-turn tracking | `Modified files: wiki/__init__.py` |
| Decisions | Per-turn tracking | `Decision: chose direct file I/O` |
| Full summary | Compression/session-end | All of above + blockers, tool count |

### Key Insight: MLX vs GGUF for LM Studio

| Format | Use Case | LM Studio API Support |
|--------|----------|----------------------|
| **GGUF** | CPU/GPU inference, llama.cpp | ✅ Full support via `/v1/models` |
| **MLX** | Apple Silicon only (MLX library) | ❌ Not exposed via LM Studio API |

**Practical implication:** Download GGUF quantizations for local inference. MLX models (from `nightmedia/Qwen3.5-2B-mxfp4-mlx`) work only when loaded directly in LM Studio app UI, NOT via API server.

**Model experiment results (2026-05-06):**
- `Qwen3.5-2B-mxfp4` (MLX, 1.5GB) → LM Studio API server does NOT expose it
- `Qwen3.5-2B-GGUF Q4_K_M` (1.2GB) → prompt template error, unusable
- `qwen3.5-4b-awq-instruct` → ~44s curate/query ✅ FASTEST
- `gemma-4-e2b` → ~76s curate/query ✅ RECOMMENDED (stable)
- `qwen3.5-0.8b` → too small
- `qwen3.6-35b` → timeout

## Related Files

- Plugin: `~/.hermes/plugins/memory/wiki/__init__.py`
- Memory: `~/.hermes/memories/MEMORY.md`
- User profile: `~/.hermes/memories/USER.md`
- Checkpoints: `~/.hermes/checkpoints/`
- Memory architecture: `references/memory-architecture.md`
