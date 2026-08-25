# Session Continuity Gap — ⚠️ CLAIMED FIXED BUT UNVERIFIED (2026-05-06)

> Generated: 2026-05-06 | **Status: UNVERIFIED ⚠️ — Evidence suggests fix is NOT working**

## Root Cause (Before Fix)

Hermes Agent had a **session continuity gap**: when context compresses or session ends, work-in-progress was LOST because:

1. `TASK_STATE.md` template existed but **no code ever wrote to it**
2. `BuiltinMemoryProvider` had no `on_session_end()` — MEMORY.md not auto-updated
3. Context compression was **lossy** — tool outputs → 1-line summaries, artifact trail gone
4. No pre-compact checkpoint fired **before** compression

## The Fix — ALL 4 TIER COMPLETE (2026-05-06)

**Implementation:** `~/.hermes/plugins/memory/wiki/__init__.py` — complete rewrite (22KB)

### Tier 1: WikiMemoryProvider.sync_turn() + Rolling Checkpoint ✅
- Accumulates conversation buffer + tracks files_modified + decisions via regex
- Writes rolling checkpoint every 5 turns via daemon thread (with 2s join timeout to prevent race)
- Output: `~/.hermes/checkpoints/session_state_<session_id>.md`

### Tier 2: TASK_STATE.md + DECISION_LOG.md Auto-Write ✅
- `on_session_end()` writes `~/.hermes/checkpoints/TASK_STATE.md` (session summary)
- `on_session_end()` appends to `~/.hermes/checkpoints/DECISION_LOG.md`
- Session summary auto-appended to `wiki/log.md`

### Tier 3: Auto-Extract to MEMORY.md ✅
- `on_session_end()` calls BuiltinMemoryStore to auto-extract key facts
- Files modified and decisions auto-added to MEMORY.md

### Tier 4: on_pre_compress() Pre-Compact Checkpoint ✅
- Structured 4-section checkpoint: Intent + State + Decisions + Next Steps
- Written **before** compression fires — survives compaction
- Output: `~/.hermes/checkpoints/pre_compact_<session_id>.md`
- Returns context hint string for compression LLM prompt

## Session End Lifecycle (After Fix)

```
Session end
    ↓
WikiMemoryProvider.on_session_end(messages)
    ↓
1. Rolling checkpoint (SYNC — not daemon, prevents exit-kill race)
2. wiki/log.md ← session summary appended
3. TASK_STATE.md ← full session state
4. DECISION_LOG.md ← all decisions timestamped
5. MEMORY.md ← auto-extract via BuiltinMemoryStore
    ↓
Pre-compress (if triggered)
    ↓
WikiMemoryProvider.on_pre_compress(messages)
    ↓
pre_compact_<session_id>.md ← survives compression
```

## Key Technical Detail: Daemon Thread Exit Race

**Problem:** Initial implementation used daemon threads for rolling checkpoint writes. Daemon threads are killed on Python exit — checkpoints never flushed.

**Fix:** Rolling checkpoint during `on_session_end()` writes **synchronously** (no thread). Rolling checkpoint during active session uses daemon thread with 2-second join timeout on next trigger to prevent race conditions.

## Verification Commands

```bash
# Check checkpoints exist after session
ls -la ~/.hermes/checkpoints/

# Run functional test
cd ~/.hermes && python3 -c "
from plugins.memory.wiki import WikiMemoryProvider, CHECKPOINT_DIR
p = WikiMemoryProvider()
p.initialize('verify-fix')
p.sync_turn('test user', 'test assistant')
p._decisions.append('Test decision')
p._files_modified.append('plugins/memory/wiki/__init__.py')
p.on_session_end([{'role':'user','content':'test'}])
import os
rc = CHECKPOINT_DIR / 'session_state_verify-fix.md'
ts = CHECKPOINT_DIR / 'TASK_STATE.md'
dl = CHECKPOINT_DIR / 'DECISION_LOG.md'
print(f'Rolling checkpoint: {\"✅\" if rc.exists() else \"❌\"}')
print(f'TASK_STATE.md: {\"✅\" if ts.exists() else \"❌\"}')
print(f'DECISION_LOG.md: {\"✅\" if dl.exists() else \"❌\"}')
"

# Verify wiki/log.md was updated
grep -c "session |" /Volumes/Storage-1/Hermes/wiki/log.md
```

## Impact on Agentic Capabilities

This fix directly enables:
- **Self-Correction**: Can reference past decisions when course-correcting
- **Memory Optimization**: Session state auto-extracted to long-term memory
- **Learning from Failures**: DECISION_LOG.md captures what didn't work
- **Context Management**: Pre-compact checkpoint survives compression

## Memory Provider Evaluation Findings (2026-05-06)

### ByteRover — NOT Truly Local ⚠️
**Finding:** ByteRover requires ByteRover cloud account despite marketing as "local-first".

```
$ brv curate "test"
❌ Error: No provider connected. Run "brv providers connect byterover"
$ brv providers connect byterover
❌ ByteRover Provider requires a ByteRover account.
```

**Key facts:**
- CLI is free to install: `curl -fsSL https://byterover.dev/install.sh | sh`
- Requires account + login to curate/query — no local-only mode
- Has `on_pre_compress()` hook (good)
- Plugin path: `hermes-agent/plugins/memory/byterover/`
- **Verdict: Skip unless Anh has/wants ByteRover account**

### Alternative: Holographic ✅
**Finding:** Holographic is truly local — SQLite + FTS5, zero external dependencies.

```
$ python3 -c "from plugins.memory.holographic import HolographicMemoryProvider; ..."
is_available: True  # No account, no API key, no network
```

**Key facts:**
- No external dependencies (SQLite always available)
- `fact_store` + `fact_feedback` tools
- Trust scoring + entity resolution
- **Verdict: Good second provider if multi-provider setup needed**

### Multi-Provider Discovery
MemoryManager supports **multi-provider** — WikiMemoryProvider and Holographic can run simultaneously. Both are active-write capable (wiki for checkpoints, holographic for structured facts). ByteRover cannot replace either without cloud account.

**Provider availability check (2026-05-06):**
| Provider | Available | Account Needed | Local |
|----------|-----------|---------------|-------|
| WikiMemoryProvider | ✅ Always | ❌ None | ✅ |
| Holographic | ✅ True | ❌ None | ✅ |
| ByteRover | ❌ Requires login | ✅ Yes | ⚠️ Cloud |

**Action:** Keep WikiMemoryProvider (done), consider Holographic as second provider if needed. ByteRover deferred until account created.
