# WikiMemoryProvider USER.md Corruption — 2026-05-21

## Corruption Pattern

USER.md bị ghi đè bởi garbage extracted từ tool call fragments:

```
- [tool] the [HIGH]
- [preference] you to operate? [HIGH]
```

## Root Cause

WikiMemoryProvider `_extract_entity_facts()` dùng regex patterns quá rộng trên conversation buffer. Khi `on_pre_compress` (context compression) trigger, buffer đã chứa:
1. Tool call metadata (`[tool] the [HIGH]`)
2. Model output labels (`lama [HIGH]`)
3. Preference queries (`[preference] you to operate?`)

Pattern match thành "facts" và được viết vào USER.md.

**Rapid writes:** 5 writes trong 8ms tại 17:49:05 — context compression loop trigger nhiều lần, mỗi lần extract thêm garbage.

## Files Involved

| File | Role |
|------|------|
| `~/.hermes/plugins/memory/wiki/__init__.py:967` | ENTITY_PATTERNS — TOO BROAD |
| `~/.hermes/plugins/memory/wiki/__init__.py:991` | `_extract_entity_facts()` — extracts garbage |
| `~/.hermes/plugins/memory/wiki/__init__.py:1047` | `_write_structured_user_profile()` — writes to USER.md |
| `~/.hermes/plugins/memory/wiki/__init__.py:538` | `on_session_end()` — trigger |
| `~/.hermes/plugins/memory/wiki/__init__.py:1476` | `on_pre_compress()` — ALSO trigger |

## ENTITY_PATTERNS (line ~967) — Problematic Patterns)

```python
ENTITY_PATTERNS = {
    "tool": [r"\[tool\]\s+(\w+)"],
    "model": [r"\[model\]\s+([^\]]+)"],
    "preference": [r"\[preference\]\s+([^\]]+)"],
    ...
}
```

These match **literal tool output fragments** in the conversation buffer, NOT actual user facts.

## Fix Required

1. **Tighten ENTITY_PATTERNS** — bỏ patterns match "[tool]", "[model]", "[preference]" literals
2. **Skip compression artifacts** — filter extracted facts chứa `[` hoặc `]`  
3. **Rate-limit writes** — debounce/throttle USER.md writes

## Related

- `references/memory-cleanup-session-2026-05-21.md` — first cleanup (May 2026)
- `references/wikimemoryprovider-bugfix-2026-05-06.md` — earlier WikiMemoryProvider bug
- `references/wikimemoryprovider-dual-location-bug-2026-05-08.md` — dual location bug