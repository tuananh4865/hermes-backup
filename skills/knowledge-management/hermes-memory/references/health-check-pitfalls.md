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
# Use cronjob action='remove' with job_id='ba3953434244'
# Or disable: cronjob action='pause' with job_id='ba3953434244'
```

## Wiki Health Check — Script Path Issue

Scripts stored in `~/.hermes/scripts/` need full path in cron:
```bash
# Wrong: wiki_health.sh
# Right: /Users/tuananh4865/.hermes/scripts/wiki_health.sh
```

## ⚠️ PITFALL: Two Health Tools, Different Counts — Always Run Both

| Tool | Broken Link Count | Regex/Logic | Use |
|------|-------------------|-------------|-----|
| `wiki_self_heal.py --fix --links` | 0 after fix | Slug-based match, lowercase | Auto-fix stubs |
| `wiki_semantic_health.py` | 743 | Filename-based, reports edge cases | Edge case audit |

**Why discrepancy:** `semantic_health` catches edge cases self_heal misses:
- Empty wikilinks: `[[...]]`
- Raw/ path links: `[[raw/transcripts/...]]` (raw/ intentionally excluded)
- Self-referential: `[[self-healing-wiki]]` in self page
- Links with spaces: `[[double brackets]]`

**Correct workflow:** Run BOTH — self_heal for fix, semantic_health for edge case audit. Never trust only one tool's count.

## ⚠️ PITFALL: Auto-Create Stubs Bloat the Wiki

`wiki_self_heal.py --fix --links` was creating 2,000+ empty stub files every run (2026-05-21). Stubs are seductive but pollute the wiki:
- Auto-created stubs have "placeholder stub" content — useless for retrieval
- Each stub creates new broken wikilinks pointing to OTHER stubs → cascading bloat
- A wiki full of stubs produces false positives in health checks

**Fix applied:** Auto-stub-creation DISABLED in `wiki_self_heal.py`. Now only reports broken links, 0 stubs created.

**Rule:** NEVER auto-create stubs. Fix broken links by creating REAL content from existing source data, or leave them reported but unfixed.

## ⚠️ PITFALL: USER.md Corruption — Duplicate Entries

**Symptom:** `~/.hermes/memories/USER.md` has 1,436 duplicate entries (sentence fragments from Telegram dumps).

**Impact:** Memory tool reads USER.md for user profile. Duplicates mean profile is unreadable.

**Action needed:** Before switching to any new memory provider, cleanup USER.md. Options:
1. Manual edit to remove duplicates
2. Let session_search rebuild from clean sessions
3. Reset USER.md to empty (last resort, loses all user profile data)

## Status This Session
- 3 cron jobs ERRORing due to missing commands
- Core memory (WikiMemoryProvider) is healthy
- 3 critical crons (autoresearch, X research, backup) are healthy
- ByteRover data exists: 788K