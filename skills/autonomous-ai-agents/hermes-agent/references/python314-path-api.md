# Python 3.14 Path.write_text `mode` Parameter Removed

## Problem

In Python 3.14, `Path.write_text()` no longer accepts a `mode` parameter, AND the `Path.append_text()` method does NOT exist on this Python (pathlib on Python 3.14.5 from Homebrew). The skill doc previously suggested `append_text()` as the fix, but **it is wrong** — verified 2026-06-29 by testing directly:

```python
>>> from pathlib import Path
>>> hasattr(Path, 'append_text')
False
>>> Path('/tmp/test.txt').write_text('x', mode='a')
TypeError: Path.write_text() got an unexpected keyword argument 'mode'
```

## Correct Fix (verified working 2026-06-29)

```python
# ❌ TypeError in Python 3.14
Path("log.md").write_text(entry + '\n', mode='a')

# ❌ AttributeError in Python 3.14 (skill doc was wrong)
Path("log.md").append_text(entry + '\n')

# ✅ ACTUAL fix: read-modify-write
Path("log.md").write_text(Path("log.md").read_text() + entry + '\n')
```

## Root Cause

Python 3.14.5 (Homebrew) pathlib:
- Removed `mode` parameter from `Path.write_text()` and `Path.write_bytes()` (TypeError)
- Does NOT have `Path.append_text()` or `Path.append_bytes()` (AttributeError)

The earlier skill doc claimed `append_text()` works — **it doesn't** in this environment. The "fix" was never verified by actually running it.

## Affected Scripts (FIXED 2026-06-29)

- `/Volumes/Storage-1/Hermes/wiki/scripts/cron_daily_ingest.py:95` ✅ patched
- `/Volumes/Storage-1/Hermes/wiki/scripts/watchdog_processor.py:392` ✅ patched
- `/Volumes/Storage-1/Hermes/wiki/scripts/topic_workflow.py:254` ✅ patched

All 3 now use: `LOG_FILE.write_text(LOG_FILE.read_text() + entry + '\n')`

## Prevention

When writing file I/O in Python scripts for this environment:
- ❌ Never use `mode=` in `Path.write_text()` / `write_bytes()`
- ❌ Never use `Path.append_text()` / `append_bytes()` (don't exist on this Python)
- ✅ Use read-modify-write: `Path.write_text(Path.read_text() + new_content)`
- ✅ Or use `Path.open(mode='a')` for proper append
- ✅ OR use `Path.write_bytes(content)` with full content

## Lesson

Documenting a "fix" is not the same as applying a fix. This bug was documented in skill doc on 2026-05-07 but never actually patched in 3 cron scripts. Tonight (2026-06-29) it was applied with verified working code. Future skill updates: include actual command output proving the fix works.
