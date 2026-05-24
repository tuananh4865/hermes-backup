# Session File Discovery Pattern

## Problem
Cron jobs running daily session reviews need to find session files from "yesterday" but session files have inconsistent naming conventions.

## Session File Facts

| Attribute | Value |
|----------|-------|
| Location | `~/.hermes/sessions/` |
| Format | `.json` (NOT `.jsonl`) |
| Naming pattern | `session_YYYYMMDD_HHMMSS_hash.json` or `session_cron_hash_YYYYMMDD_HHMMSS.json` |
| Example | `session_20260523_214518_3e9adc5a.json`, `session_cron_5aea298eb0a8_20260523_000023.json` |

## How to Find Sessions from a Given Date

### DON'T: Use search_files with date pattern
```python
# This FAILS — pattern doesn't match properly
search_files(path="~/.hermes/sessions", pattern="20260523", target="files")
# Returns: total_count: 0
```

### DO: Use terminal ls
```bash
ls -la ~/.hermes/sessions/ | grep "20260523"
```

### DO: Use Python glob
```python
import glob
files = glob.glob(os.path.join(sessions_dir, "*20260523*.json"))
```

## Session Content Extraction

```python
import json
import os

def extract_session_conversation(fpath, max_chars=500):
    """Extract user/assistant messages from a session JSON file."""
    with open(fpath) as f:
        d = json.load(f)
    messages = d.get("messages", [])
    conv = []
    for m in messages:
        if m.get("role") in ("user", "assistant"):
            content = m.get("content", "")
            if isinstance(content, str) and len(content) > 0:
                conv.append({"role": m["role"], "content": content[:max_chars]})
    return conv
```

## Cron Delivery Note

When running as a cron job with "auto-delivery" enabled:
- **DO**: Save report to `~/.hermes/cron/output/daily_review_YYYY-MM-DD.md`
- **DON'T**: Manually curl Telegram API — system handles delivery automatically
- Manual Telegram API calls fail if token extraction is complex or bot is misconfigured
