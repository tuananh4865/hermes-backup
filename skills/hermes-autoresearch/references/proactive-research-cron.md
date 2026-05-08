# Proactive Research Cron — Overview

**Path:** `/Volumes/Storage-1/Hermes/wiki/scripts/proactive_research_cron.py`

**Schedule:** 7 AM daily (see crontab)

**Purpose:** Morning research on top interest areas before daily work begins.

## Research Topics (configurable)
The script researches 5 topics per run:
- TikTok Shop Vietnam
- Gen Z slang Vietnam 2026
- Agentic AI trends
- TikTok affiliate marketing
- wiki

## CRITICAL BUG (2026-05-06)

**Symptom:** `FileNotFoundError: [Errno 2] No such file or directory: 'python3.14'`

**Location:** Line ~95 in `proactive_research_cron.py`
```python
result = subprocess.run(
    ["python3.14", script_path],  # ← BUG: python3.14 doesn't exist
    ...
)
```

**Fix options:**

### Option 1: Fix the script (recommended)
```python
# Use sys.executable instead of hardcoded python3.14
import sys
subprocess.run([sys.executable, script_path], ...)
```

### Option 2: Fix crontab PATH
Add to crontab:
```
PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin
```

### Option 3: Change crontab to use full path
```
0 7 * * * /opt/homebrew/bin/python3 /Volumes/Storage-1/Hermes/wiki/scripts/proactive_research_cron.py >> ...
```

## Related
- `hermes-autoresearch` skill — main skill documenting this cron
- `wiki_self_heal.py` — complementary daily maintenance script
