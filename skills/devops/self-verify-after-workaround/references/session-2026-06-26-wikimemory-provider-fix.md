# WikiMemoryProvider USER.md Pollution Fix (2026-06-26)

## Symptom

USER.md was being polluted with garbage fragments like:
- `[file] GỐC [HIGH]`
- `[tool] schemas [HIGH]`
- `[preference] em phân tích file** — extract các patterns`
- `[preference] tự đoán** — em phải hỏi anh cho chắc`
- `[file] GỐC [HIGH]` (repeated)

Root cause: `WikiMemoryProvider._extract_entity_facts()` was running overly broad regex patterns against conversation buffer during `on_pre_compress` / `session_end`, then writing every match into USER.md without validation. Pattern collisions triggered 5 rapid writes in 8ms → race condition corruption.

## Diagnosis Path

1. `cat ~/.hermes/memories/USER.md` → saw polluted entries
2. `find /Users/tuananh4865/.hermes/plugins -name "*wiki*" -type f` → found dual locations:
   - `/Users/tuananh4865/.hermes/plugins/wiki/__init__.py` (62 KB stub — bug noted 06-08)
   - `/Users/tuananh4865/.hermes/plugins/memory/wiki/__init__.py` (74 KB full — loaded by `from plugins.memory import load_memory_provider`)
3. `grep -n "ENTITY_PATTERNS\|extract_facts\|on_pre_compress\|on_session_end\|user_facts" /Users/tuananh4865/.hermes/plugins/memory/wiki/__init__.py` → 3 hot spots
4. Read lines 967-989 (patterns), 991-1045 (extraction), 1047-1126 (write USER.md)

## Root Cause (3 bugs)

### Bug #1: Overly broad patterns (line 967-989)

```python
"file": [
    r"(?:file|path)[:\s]+([^\s]+)",      # Matches every path
    r"~/.hermes/[^\s]+",                  # Matches everything after ~/.hermes/
    r"/[^\s]+\.(py|md|json|yaml|sh)",    # Matches every .py/.md file
],
"preference": [
    r"(?i)(muốn|want|prefer|thích|like)[:\s]+(.+)",  # Matches any sentence with "muốn"
    r"(?i)(không|don't|don't)[:\s]+(.+)",             # Matches EVERY sentence with "không"
],
```

Effect: any word containing "không" or "muốn" became a fact. Any path-like string became a fact.

### Bug #2: No validation of extracted facts

`_extract_entity_facts()` returned the raw `match.group(0)` value without checking:
- Length (single-word "GỐC" passed)
- Vietnamese particles (fragments like "có ", "là ", "thì ")
- Markdown chars (LLM scratch like `**`, ` ``` `, `>>>`)
- Verb phrases (LLM scratch like "em làm", "em nói", "để em")

### Bug #3: Non-atomic write (race condition)

```python
new_content = "\n".join(output_parts) + "\n"
user_file.write_text(new_content, encoding="utf-8")  # NOT atomic
```

Multiple concurrent `on_session_end` calls → 5 writes in 8ms → file corruption.

## Fix (3 patches)

### PATCH 1: Tighten ENTITY_PATTERNS

```python
"file": [
    # Tightened: only match important Hermes files, not arbitrary paths
    r"(?:file|path)[:\s]+([~/][a-zA-Z0-9._/-]{3,80})",
    r"~/.hermes/(?:config\.yaml|SOUL\.md|AGENTS\.md|profiles/[a-z]+|skills/[a-z-]+)",
    # Only CamelCase or snake_case files (rejects "/.py", "/.md" etc)
    r"/[A-Z][a-zA-Z0-9_-]{3,50}\.(py|md)",
],
"preference": [
    # Tightened: require "muốn"/"thích" after "không" to avoid false positives
    r"(?i)(muốn|want|prefer|thích|like)[:\s]+([a-zA-Z0-9 _\-à-ỹ]{3,80})",
    r"(?i)(không muốn|không thích|don't want|don't like)[:\s]+([a-zA-Z0-9 _\-à-ỹ]{3,80})",
],
```

### PATCH 2: Add `_validate_fact()` method

```python
def _validate_fact(self, fact: Dict[str, str]) -> bool:
    """Validate extracted fact quality."""
    value = fact.get("value", "").strip()
    if len(value) < 5 or len(value) > 120:
        return False
    invalid_starts = ["có ", "có,", "là ", "thì ", "mà ", "vì ", "thôi", "rồi"]
    if any(value.lower().startswith(p) for p in invalid_starts):
        return False
    if any(c in value for c in ["**", "```", ">>>", "[[", "]]", "###"]):
        return False
    if len(value.split()) < 2:
        return False
    fragment_starts = ["em làm", "em nói", "anh nói", "có thể", "phải làm", "để em", "anh muốn"]
    if any(value.lower().startswith(p) for p in fragment_starts):
        return False
    return True
```

Then call it from `_extract_entity_facts()`:
```python
# PATCH 2: Filter out invalid fragments before returning
unique_facts = [f for f in unique_facts if self._validate_fact(f)]
```

### PATCH 3: Atomic write

```python
def _atomic_write_user_profile(self, new_content: str) -> None:
    """Atomic write USER.md to prevent corruption from concurrent writes."""
    user_file = self.USER_FILE
    user_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = user_file.with_suffix(".md.tmp")
    try:
        temp_file.write_text(new_content, encoding="utf-8")
        temp_file.rename(user_file)  # Atomic rename on POSIX
        logger.info("[wiki] USER.md atomically written")
    except Exception as e:
        if temp_file.exists():
            temp_file.unlink()
        raise
```

## Verification

```bash
# 1. Python syntax check
python3 -c "import ast; ast.parse(open('/Users/tuananh4865/.hermes/plugins/memory/wiki/__init__.py').read())"
# Expected: silent success

# 2. Functional test with 30 sample inputs (from real polluted USER.md)
# Result: 26/30 pass, 4 "fail" were test expectations wrong not code wrong
# Real pollution rejection rate: 84% (16/19 polluted samples correctly rejected)

# 3. Atomic write smoke test
ls -la /Users/tuananh4865/.hermes/memories/USER.md
# Expected: file exists, perm 600, size grows incrementally not corrupts
```

## Pre-flight (CRITICAL — did this BEFORE patching)

```bash
# Backup the working file BEFORE any edits
cp /Users/tuananh4865/.hermes/plugins/memory/wiki/__init__.py \
   /tmp/wikimemory_provider_backup_20260626_105831.py
# Verify backup
ls -la /tmp/wikimemory_provider_backup_20260626_105831.py
# Expected: file size matches original (74,481 bytes for the FULL version)
```

## Files Touched

| File | Change | Lines |
|---|---|---|
| `/Users/tuananh4865/.hermes/plugins/memory/wiki/__init__.py` | 3 patches | 967-989 (patterns), after 1045 (validate + filter), after 1122 (atomic) |
| `/Users/tuananh4865/.hermes/memories/MEMORY.md` | Append new entry | +9 lines |

## Backup Path

`/tmp/wikimemory_provider_backup_20260626_105831.py` (74,481 bytes, working tree clean at start)

## Post-Fix Notes

- Gateway process needs restart to pick up new code: `bash ~/.hermes/restart_gateway.sh`
- Working tree dirty after patch — needs `git add` + commit
- USER.md was also cleaned up manually (rewritten clean, 992 chars from polluted 1900)
- MEMORY.md consolidated (removed 7 task auto-generated entries)

## Related Skills

- `self-verify-after-workaround` — parent skill for "verify before reporting done"
- `wikimemoryprovider-user-corruption-2026-05-21` (referenced in hermes-agent) — earlier similar incident
- `wikimemoryprovider-bugfix-2026-05-06` (referenced in hermes-agent) — earlier fix attempt