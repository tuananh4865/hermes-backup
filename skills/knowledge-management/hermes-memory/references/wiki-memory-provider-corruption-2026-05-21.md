# WikiMemoryProvider Corruption Bug (2026-05-21)

## Symptom
USER.md and MEMORY.md files got corrupted — contained 28+ lines of garbage extracted from compressed context. File contained HTML-like artifacts and garbage text.

## Root Cause
WikiMemoryProvider has a bug where rapid writes (5 writes in 8ms) cause state corruption. The `sync_turn()` and `_sync_fact_realtime()` hooks write to files on every turn, and when context compression happens, the system extracts content from compressed context that includes garbage.

## Discovery
Session `20260521_140117_8de887` investigated and identified:
- `WikiMemoryProvider.initialize()` calls `_load_wiki_context()` 
- The system loads 5 wiki files at startup (start-here.md, SCHEMA.md, index.md, log.md, learned-about-tuananh.md)
- Bug is in `_sync_fact_realtime()` rapid write behavior

## Resolution

**Decision: Keep wiki as primary memory — Mem0 NOT needed**
- Mem0 is cloud-only (requires MEM0_API_KEY)
- No Hermes integration path for Mem0 OSS
- WikiMemoryProvider bug can be worked around by cleaning corrupted files

**Action taken:**
```bash
# Clean USER.md — reset garbage
# Clean MEMORY.md — reset garbage
```

## Prevention
- Don't run WikiMemoryProvider in high-frequency turn environments
- If corruption occurs, clean the files manually:
  - `~/.hermes/memories/USER.md`
  - `~/.hermes/memories/MEMORY.md`
- Consider disabling `_sync_fact_realtime()` if it causes issues

## Related
- `references/wiki-health-cron-fix.md` — wiki health cron scripts
- `references/mem0-oss-ollama-setup.md` — Mem0 OSS local setup (not needed)