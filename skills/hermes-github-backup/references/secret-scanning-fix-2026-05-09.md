# GitHub Secret Scanning Fix — 2026-05-09

## Problem
Push to `hermes-backup` rejected due to GitHub Secret Scanning:
```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: Push cannot contain secrets
remote:   — GitHub Personal Access Token —
remote:     locations:
remote:       - commit: 4414d43f1243a6c290eafdbf116f32b20bf5b5af
remote:         path: profiles/research-lead/auth.json:12
remote:         path: state-snapshots/20260506-134701-pre-update/auth.json:59
```

## Root Cause
Initial setup didn't have `.gitignore` with auth.json exclusions before first push. GitHub scanned the commit and blocked it.

## Resolution Steps

1. **Created proper .gitignore** at `~/.hermes/.gitignore`:
```gitignore
# Auth files (contain secrets)
auth.json
profiles/**/auth.json
state-snapshots/**/auth.json
```

2. **Removed auth.json from git index** (didn't delete local files):
```bash
git rm --cached -f auth.json profiles/**/auth.json state-snapshots/**/auth.json
```

3. **Amended commit** to remove auth files from history:
```bash
git commit --amend -m "Backup hermes full: 2026-05-09"
```

4. **Force pushed**:
```bash
git push origin main --force
```

## Result
✅ Successfully pushed to `hermes-backup`: 8,377 files, 1,871,296 insertions

## Prevention
Always add auth exclusions to .gitignore BEFORE first push. Auth files are now excluded for all future backups.
