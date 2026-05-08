# Cron Subprocess PATH Issue (Python 3.14)

## Problem

Scripts running via **crontab** fail with `FileNotFoundError: [Errno 2] No such file or directory: 'python3.14'` even when `python3.14` works fine in interactive shell.

```python
# ❌ FAILS in crontab (PATH mismatch)
subprocess.run(["python3.14", script_path], ...)

# ✅ WORKS in crontab (absolute path)
subprocess.run(["/opt/homebrew/bin/python3.14", script_path], ...)
```

## Root Cause

Crontab runs with a **minimal PATH** that differs from your shell's PATH:

```
# Interactive shell PATH includes /opt/homebrew/bin
/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:...

# Crontab default PATH
/usr/bin:/bin
```

## Affected Scripts

All wiki cron scripts in `/Volumes/Storage-1/Hermes/wiki/scripts/*.py` that invoke `subprocess` with bare Python executables:

- `proactive_research_cron.py` — line 96: `["python3.14", ...]`
- `cron_daily_ingest.py` — uses absolute path already (`#!/opt/homebrew/bin/python3.14` shebang)
- Other scripts may also have this issue

## Fix Applied (2026-05-07)

Replaced bare `python3.14` with absolute path in `proactive_research_cron.py`:

```python
# Before
["python3.14", script_path]

# After
["/opt/homebrew/bin/python3.14", script_path]
```

## Verification

```bash
# Test the cron script manually
cd /Volumes/Storage-1/Hermes/wiki && /opt/homebrew/bin/python3.14 scripts/proactive_research_cron.py
```

## Prevention

When writing new cron scripts that use `subprocess`:
1. Always use **absolute paths** for executable invocations in subprocess
2. Or set PATH explicitly: `env={"PATH": "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"}`
3. Use shebang `#!/opt/homebrew/bin/python3.14` and call script directly (not `python3.14 script.py`)
