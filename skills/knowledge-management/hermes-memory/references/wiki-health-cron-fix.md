# Cron Script Path — Critical Fix (2026-05-18)

## Problem
Cron job `a2786fb20bac` (Wiki Health Daily) errored: "wiki_health.sh: command not found".

## Root Cause
The `script` field in cron job must be **relative to `~/.hermes/scripts/`** — just the filename, no slashes, no `~`, no absolute paths. The cron system auto-prepends `~/.hermes/scripts/`.

**Correct:**
```python
cronjob(action='update', job_id='a2786fb20bac', script='wiki_health.sh')
```

**WRONG (all rejected):**
- `/Users/tuananh4865/.hermes/scripts/wiki_health.sh` — absolute path
- `~/.hermes/scripts/wiki_health.sh` — home-relative
- `./wiki_health.sh` — relative with dot-slash

## Verified Working Scripts

| Script | Args | Works? |
|--------|------|--------|
| `wiki_health.sh` | — | ✅ |
| `byterover_knowledge_sync.py --days-ago 1` | args OK | ✅ (but needs execute permission) |

## Wiki Health Check Results (2026-05-18 baseline)
```
Wiki issues: 1049 total
  - Broken wikilinks:   742
  - Orphan pages:       218
  - Duplicate titles:   68
```
4AM cron will track trend daily.