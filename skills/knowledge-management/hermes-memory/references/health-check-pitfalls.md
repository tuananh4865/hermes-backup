# ByteRover Health Check — Runbook

## Problem
The ByteRover Health Check cron job (`ba3953434244`) uses `brv status` directly in bash, but `brv` is NOT in the system PATH when cron runs under the hermes user's environment.

## Symptoms
- `brv: command not found` in cron output
- `brv curate view --since 24h` fails silently
- Cron job status: `error`

## Root Cause
The `brv` CLI is installed as a Hermes plugin tool, not as a system-wide executable. Cron jobs run in a minimal environment without the same PATH as interactive shells.

## Workaround Options

### Option 1: Use Python directly
```bash
# Check ByteRover status via Python API instead of CLI
python3 -c "
from hermes_tools import brv_api_status  # if available
print('ByteRover status')
"
```

### Option 2: Check via file system
```bash
# ByteRover stores knowledge in:
du -sh ~/.hermes/byterover/
ls -la ~/.hermes/byterover/curations/ 2>/dev/null | head -10
```

### Option 3: Remove broken cron jobs
```bash
# If ByteRover CLI isn't available system-wide, remove the cron:
# Use cronjob action='remove' with job_id='ba3953434244'
# Or disable: cronjob action='pause' with job_id='ba3953434244'
```

## Wiki Health Check — Similar Issue

The `wiki_health.sh` script is referenced in cron job `a2786fb20bac` but isn't in PATH. Scripts stored in `~/.hermes/scripts/` need to be called with full path:

```bash
# Instead of: wiki_health.sh
# Use: /Users/tuananh4865/.hermes/scripts/wiki_health.sh
```

## For This Session
- 3 cron jobs are ERRORing due to missing commands
- Core memory system (WikiMemoryProvider) is healthy
- 3 critical crons (autoresearch, X research, backup) are healthy
- ByteRover data exists: `du -sh ~/.hermes/byterover/` = 788K

## Recommendation
Review whether `brv` CLI is meant to be a system command or only available through the agent. If system-wide, install it. If agent-only, rewrite health check cron to use file-based checks or remove the cron.