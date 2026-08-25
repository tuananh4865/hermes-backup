# watchdog_processor.py Bug — Path.write_text mode=

**Found**: 2026-05-08 by Orchestrator cron session
**File**: `/Volumes/Storage-1/Hermes/wiki/scripts/watchdog_processor.py`
**Line**: ~392 in `append_log()`

## Symptom

Every 15 min, watchdog batch processor crashes with:
```
TypeError: Path.write_text() got an unexpected keyword argument 'mode'
```

Stack trace:
```
File "watchdog_processor.py", line 566, in <module>
    main()
File "watchdog_processor.py", line 544, in main
    append_log("watchdog:batch", f"Batch scan: {len(results)} changes", ...)
File "watchdog_processor.py", line 392, in append_log
    LOG_FILE.write_text(entry + '\n', mode='a')
TypeError: Path.write_text() got an unexpected keyword argument 'mode'
```

## Root Cause

`Path.write_text()` does NOT accept a `mode` parameter. That API belongs to `open()`.

```python
# WRONG:
Path(LOG_FILE).write_text(entry + '\n', mode='a')

# RIGHT — use open() context manager for append:
with Path(LOG_FILE).open('a') as f:
    f.write(entry + '\n')
```

Or for write (not append):
```python
Path(LOG_FILE).write_text(entry + '\n')  # mode='w' is default
```

## Fix

Replace line ~392:
```python
# BEFORE:
LOG_FILE.write_text(entry + '\n', mode='a')

# AFTER:
with Path(LOG_FILE).open('a') as f:
    f.write(entry + '\n')
```

## Impact

- Batch watchdog processor crashes every 15 min
- No new wiki changes processed (but watchdog polling itself continues)
- Confirmed: script runs but append_log fails silently → no log entries written
