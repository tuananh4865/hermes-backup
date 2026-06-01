---
name: wiki-maintenance
description: Wiki cleanup, rebuild, and maintenance workflows — remove stale content by age/relevance, recover accidentally deleted files, manage git history with nested repos.
---

# Wiki Maintenance

## Overview

Periodic wiki rework to keep the knowledge base lean and relevant. Remove content not touched in N days, recover from cleanup mistakes, manage git history with nested repos.

## When to Use

- User asks to "clean up wiki", "rework wiki", "remove stale content"
- Wiki has grown unwieldy (1000+ files, many irrelevant)
- After bulk operations that may have deleted active content

## Cleanup Workflow (14-day window)

### Step 1: Assess Current State
```bash
# Get file counts
ls concepts/ | wc -l
ls entities/ | wc -l
ls references/ | wc -l

# Check log for recent activity
tail -100 wiki/log.md
```

### Step 2: Identify Stale Content

Key questions:
- What raw transcripts ARE current (within window)?
- What raw transcripts are OLD (pre-window)?
- What telegram scrapes are stale timestamp sessions?
- What concept/entity docs haven't been touched in N days?
- What stale directories exist (.processed/, .pytest_cache/, config/, etc.)?

### Step 3: Plan KEEP vs DELETE

**KEEP (active relevance):**
- Raw transcripts within window (e.g., May 14-28 for 14-day window)
- Concepts/articles about topics user asked about recently
- Active research in references/
- Essential entities

**DELETE (stale):**
- Raw transcripts outside window
- Telegram scrapes from old sessions (timestamp-prefixed: 10-*, 12-*, etc.)
- Stale directories (fine-tuned-wiki, .processed, .pytest_cache, config, etc.)
- Docs on topics user hasn't asked about in window

### Step 4: Execute Cleanup
```bash
# Raw transcripts — keep only recent
rm -rf raw/transcripts/2026-04-* raw/transcripts/2026-03-* ...

# Telegram scrapes — remove old timestamps
rm -f concepts/10-*.md concepts/12-*.md concepts/13-*.md ...

# Stale directories
rm -rf fine-tuned-wiki/ .processed/ .pytest_cache/ config/ ...

# Stale concept docs
rm -f concepts/apple-*.md concepts/google-*.md concepts/lm-studio.md
```

### Step 5: Update log.md
Append cleanup entry:
```bash
echo '## [YYYY-MM-DD] wiki-rework | Wiki cleaned — ...
- Raw transcripts: kept May 14-28 only (14 days)
- ...
[commit message]' >> wiki/log.md
```

### Step 6: Commit + Push
```bash
git add -A
git commit -m "Wiki cleanup: remove stale content not touched in 14 days"
git push
```

## Wiki Forget Automation (14-Day Auto-Cleanup)

A script that auto-deletes wiki/memory not referenced → connects to session DB to track what was actually used.

### Script: `~/.hermes/scripts/wiki_forget_14days.py`

**Key Implementation Details:**
```python
SESSION_DB = Path.home() / ".hermes" / "state.db"  # DB path
cutoff_ts = int(cutoff.timestamp())  # INTEGER, not float

# Query user messages from last 14 days
cur.execute("""
    SELECT content FROM messages
    WHERE timestamp > ? AND role = 'user'
    ORDER BY timestamp DESC
""", (cutoff_ts,))
```

**Run Modes:**
- Dry-run (default): `python3 wiki_forget_14days.py`
- Actual delete: `DELETE_MODE=true python3 wiki_forget_14days.py`

**Output:** Logs to `~/.hermes/cron/output/wiki_forget_YYYY-MM-DD.md`

**Cron Setup:**
```bash
# no_agent cron job, runs daily at 3AM
# Via cronjob tool:
cronjob --create --name "Wiki Memory Forget Daily" \
  --script "wiki_forget_14days.py" \
  --schedule "0 3 * * *" \
  --deliver local
```

**Pattern:** Reads session DB → extracts referenced topics → deletes everything else.

### Session DB Schema (state.db)
| Table | Key Column | Note |
|-------|-----------|------|
| messages | `timestamp` | Unix timestamp (integer), `role='user'` for user messages |
| sessions | `id`, `platform` | Session metadata |

### Recovery After Wiki Forget
```bash
# Restore references/ from git
git checkout HEAD~1 -- references/

# Restore specific directories that failed
python3 -c "import shutil; shutil.rmtree('projects/stale-dir')"
```

## Recovering Accidentally Deleted Files

After a cleanup, active content may be accidentally removed. Recover from git history:
```bash
# Find the commit before cleanup
git log --oneline -10

# Check what was in references/ at that commit
git show <ref>:references/ | head -20

# Restore entire directory
git checkout a8d3485 -- references/

# Commit restoration
git add references/
git commit -m "Restore references — active research from 14 days"
```

**Key pattern:** `git checkout <last-good-ref> -- <path>` restores files as they existed at that commit.

## Telegram Scrape Pattern

Telegram session scrapes are named with timestamps:
- Sessions from same day cluster: `14-*-*`, `17-*-*`
- Older sessions: `10-*`, `12-*`, `13-*`, `16-*`, `18-*`

**Rule:** If a telegram scrape is from a session where user wasn't asking about the wiki topic, it's likely stale and safe to delete.

## Git Notes for Wiki

- Wiki lives at `/Volumes/Storage-1/Hermes/wiki/`
- Git remote: `my-llm-wiki` on GitHub
- Obsidian plugin syncs every minute → git auto-commits
- Backup repo: `hermes-backup` (separate from wiki)
- **Nested git repos:** `.git` subdirectory inside wiki/ — operations must run INSIDE wiki/ directory

## Verification

After cleanup:
- [ ] `git status` shows expected changes only
- [ ] Active content (TikTok, Hermes, Gen Z) still exists
- [ ] Raw transcripts window correct (May 14-28)
- [ ] `log.md` updated with cleanup entry
- [ ] Pushed to remote

## Pitfalls

1. **Accidentally deleting active refs:** Always check `references/` before commit. If cleared, restore with `git checkout <ref> -- references/`
2. **Running git from wrong directory:** Wiki has nested .git — must `cd wiki/` first
3. **Forgetting to update log.md:** Cleanup without logging is untrackable
4. **Obsidian plugin still syncing during cleanup:** May create conflicting auto-commits
5. **Wiki forget deletes directories with errors:** Use `shutil.rmtree()` via Python for directories that fail with `Operation not permitted`

## Session Recording Health Check (Add to Maintenance Workflow)

**⚠️ Pattern detected (May 28-31, 2026):** Cron jobs execute normally but session recording breaks — sessions.db becomes 0 bytes, no new session files created.

**Symptoms:**
- `~/.hermes/sessions/sessions.db` is 0 bytes or empty
- `~/.hermes/sessions/session_*.json` files stop being created after a certain date
- Cron output files still being produced (cron jobs are running)
- User sessions not tracked in wiki log

**Check command:**
```bash
# Session recording health check
ls -la ~/.hermes/sessions/sessions.db
ls -t ~/.hermes/sessions/session_*.json 2>/dev/null | head -5

# If sessions.db is 0 bytes OR no session files from last 48h → recording broken
```

**If broken, document in daily review:**
```
### ⚠️ CRITICAL: Session Recording Broken
- **Last session logged:** [date]
- **Missing:** [missing dates]
- **sessions.db:** [size]
- **Root cause:** Unknown
```

**Note:** This is a Hermes Agent internal issue, not a wiki content issue. Document in daily review for user awareness. Resolution requires investigation of Hermes session service.
