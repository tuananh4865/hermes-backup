# Python 3.14 Path.write_text `mode` Parameter Removed

## Problem

In Python 3.14, `Path.write_text()` no longer accepts a `mode` parameter:

```python
# ❌ TypeError in Python 3.14
Path("log.md").write_text(entry + '\n', mode='a')

# ✅ Works in Python 3.14
Path("log.md").append_text(entry + '\n')
```

## Root Cause

Python 3.14 removed `mode` parameter from `Path.write_text()` and `Path.write_bytes()`. Use `append_text()` / `append_bytes()` for appending instead.

## Affected Scripts

- `/Volumes/Storage-1/Hermes/wiki/scripts/cron_daily_ingest.py` — line 95

## Fix Applied (2026-05-07)

```python
# Before (Python 3.14 TypeError)
LOG_FILE.write_text(entry + '\n', mode='a')

# After (correct for Python 3.14)
LOG_FILE.append_text(entry + '\n')
```

## Prevention

When writing file I/O in Python scripts for this environment:
- Use `Path.append_text()` / `Path.append_bytes()` for append mode
- Use `Path.write_text()` / `Path.write_bytes()` for write mode only
- Avoid `mode=` parameter in Path I/O calls (deprecated in 3.9+, removed in 3.14)
