# Git Wiki Repo Management Patterns

> Session-specific patterns for managing wiki git repos and avoiding tracking leaks.
> Created: 2026-05-08 | Context: `/Volumes/Storage-1/Hermes/wiki/` and `/Volumes/Storage-1/Hermes/` repo cleanup

---

## Pattern 1: Wiki Repo Redirect (Remote → Wrong Repo)

**Symptom:** Wiki push goes to wrong repo (e.g., `hermes-backup` instead of `my-llm-wiki`).

**Check:**
```bash
cd /path/to/wiki
git remote -v
# origin → https://github.com/tuananh4865/hermes-backup.git  ❌ WRONG
# origin → https://github.com/tuananh4865/my-llm-wiki.git    ✅ CORRECT
```

**Fix:**
```bash
git remote set-url origin https://github.com/tuananh4865/my-llm-wiki.git
```

**If diverged (local vs remote have diverged):**
```bash
# Option A: Force push local (DESTRUCTIVE to remote)
git push origin main --force

# Option B: Stash, pull-rebase, then push
git stash
git pull origin main --rebase
git push origin main
git stash drop

# Option C: Abort if conflict (after Option B fails)
git rebase --abort
git stash pop
```

---

## Pattern 2: Git Tracking Files Outside Wiki Directory

**Symptom:** `git status` shows modified files like `../skills/`, `../workers/`, `../.hermes/`.

**Check:**
```bash
cd /path/to/wiki
git status --short | grep -E "\.\./" | head -20
```

**Root Cause:** Wiki git repo is inside parent directory that also has other content tracked.

**Fix — Unstage and ignore:**
```bash
cd /path/to/wiki

# Unstage all external files
git restore ../skills/ ../workers/ ../.hermes/ 2>/dev/null

# Add to .gitignore
echo -e "\n# Hermes data (not wiki)\n../skills/\n../workers/\n../.hermes/" >> .gitignore

# Commit the ignore change
git add .gitignore
git commit -m "Ignore ../skills/ and ../workers/ from wiki tracking"
```

---

## Pattern 3: Parent Repo Has Wiki-Only Tracking (Inverse Problem)

**Symptom:** `/Volumes/Storage-1/Hermes/` repo has skills/workers/scripts tracked instead of just wiki/.

**Check:**
```bash
cd /Volumes/Storage-1/Hermes
git status --short | grep -v "wiki/" | head -20
```

**Fix — Remove all except wiki/:**
```bash
cd /Volumes/Storage-1/Hermes

# Remove everything from staging (keep working dir)
git rm -r --cached .hermes/ memories/ projects/ scripts/ skills/ workers/ .gitignore 2>/dev/null

# Only stage wiki/
git add wiki/

# Verify only wiki is staged
git status --short

# Commit
git commit -m "Remove all except wiki/ - repo now wiki-only"
git push origin main
```

**Result:** 697 files deleted from git tracking, wiki/ is sole tracked content.

---

## Pattern 4: Cron Skill Attachment Causes Wrong Task Run

**Symptom:** Cron runs skill content instead of its own prompt.

**Example:** Session review cron (0AM) had `hermes-autoresearch` skill attached → ran research loop instead of session review.

**Check:**
```bash
cronjob list | grep "hermes-autoresearch"
# Any cron with this skill that shouldn't have it = BUG
```

**Fix — Update cron to remove skill:**
```bash
cronjob update --job_id {job_id} --prompt "{correct prompt}" --skills []
```

**Rule:** Session log analysis, daily review, wiki sync → CRON PROMPT, NOT skill. Skills are for research/automation patterns.

---

## Key Files Modified (2026-05-08)

| File | Action |
|------|--------|
| `/Volumes/Storage-1/Hermes/wiki/.gitignore` | Added `../skills/`, `../workers/`, `../.hermes/` |
| `/Volumes/Storage-1/Hermes/wiki/.git/config` | Changed remote from `hermes-backup` → `my-llm-wiki` |
| Cron `5aea298eb0a8` | Removed `hermes-autoresearch` skill, fixed prompt |

---

## Related

- `references/cron-management-patterns.md` — Cron creation/update/verification patterns
- `references/cron-skill-attachment-bloat.md` — Cron loading full skill instead of prompt
