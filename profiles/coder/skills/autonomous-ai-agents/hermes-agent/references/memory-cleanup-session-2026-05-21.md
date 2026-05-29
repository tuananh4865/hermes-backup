# Memory Cleanup Session — 2026-05-21

## What Happened

User asked "Kiểm tra sức khoẻ bộ nhớ của em xem nào" → discovered USER.md was corrupted with LLM output artifacts:

**Corruption pattern:**
```
- [model] output [HIGH]
- [model] text [HIGH]
- [model] text. [HIGH]
- [model] llama [HIGH]
- [tool] the [HIGH]
- [file] py
- [preference] cần server
- [preference] với Mem0
```

These are raw LLM scratchpad outputs that got written to USER.md instead of processed facts.

## Root Cause

Session review tasks (`Review the conversation above...`) in past cron jobs were writing their OWN output text to USER.md instead of properly parsing and extracting clean facts.

The `MemoryStore.add()` in `memory_tool.py` has a `_scan_memory_content()` validator — but some process is bypassing it and writing directly to USER.md.

**Suspected bypass path:** A session review subagent or cron task used the `memory` tool with raw LLM output as the `content` parameter, and the tool's `_reload_target()` + file write cycle didn't validate properly.

## What Was Cleaned

1. **`USER.md`** — reset from 42 corrupted lines to 562 bytes clean state
   - Backup: `USER.md.bak.20260521141944`
   - Kept only: PREFERENCES, PROJECTS, FACTS (clean versions)
   - Re-established clean structure with `§` delimiters

2. **`MEMORY.md`** — reset from 39 noisy task entries to 506 bytes
   - Kept: environment notes + decision context
   - Removed: session task narratives that had accumulated

3. **`entities/learned-about-tuananh.md`** — removed 71 lines of auto-improvement note pollution
   - Kept: actual content (preferences, Gen Z slang, operating rules)
   - Removed: `> **Auto-improvement note:**...` artifacts from bottom of file
   - Content went from 296 lines → 226 lines

## Prevention Rules

1. **Any task that calls `memory` tool must format content as structured facts, not raw LLM output**
   - Session review tasks: extract key facts → format as `- fact: description` entries → pass to memory tool
   - Never pass raw LLM reasoning output directly to `memory.add()`

2. **Monitor USER.md size** — if it grows >2KB between sessions, corruption is in progress
   - Clean threshold: ~500-800 bytes for a populated USER.md
   - Corruption signature: lines starting with `[tool]`, `[file]`, `[model]`, `[preference]` (unprocessed)

3. **Before memory cleanup:**
   ```bash
   # Check corruption
   cat ~/.hermes/memories/USER.md | grep -E "^\\[|^\\- \\[tool\\]|^\\- \\[file\\]|^\\- \\[model\\]|^\\- \\[preference\\]"
   
   # Backup first
   cp ~/.hermes/memories/USER.md ~/.hermes/memories/USER.md.bak.$(date +%Y%m%d%H%M%S)
   ```

## Wiki as Source of Truth

After cleanup, USER.md and MEMORY.md are minimal. The **wiki** is the primary memory:
- `entities/learned-about-tuananh.md` — user profile
- `log.md` — activity log  
- `checkpoints/` — session state

The builtin memory files (USER.md, MEMORY.md) are for lightweight fact injection only. Wiki carries the full knowledge base.

## Related

- `references/memory-architecture.md` — full memory stack breakdown
- `references/memory-provider-architecture-gaps.md` — 3 critical gaps in memory system