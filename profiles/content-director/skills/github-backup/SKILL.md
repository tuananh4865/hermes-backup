---
title: GitHub Backup
name: github-backup
description: Backup large directories and knowledge bases to GitHub — handles nested .git repos, gitignored paths, and media file exclusion. Use when backing up wiki, skills, memories, or any large folder to GitHub.
category: devops
tags: [github, backup, git, large-files, wiki-backup]
created: 2026-05-10
updated: 2026-05-10
---

# GitHub Backup

Backup large directories (wiki, skills, knowledge bases, datasets) to GitHub when they contain nested .git repos, are gitignored by a parent, or need selective media file exclusion.

## Core Problem Pattern

All GitHub backup scenarios share the same three challenges:
1. **Nested .git repos** — subdirectories that are themselves git repositories
2. **Parent .gitignore** — the outer repo's gitignore blocks the target directory entirely
3. **Selective exclusion** — backup .md content but exclude large media files

## The Universal 5-Step Process

### Step 1: Remove nested .git repos
```bash
find /path/to/directory -name ".git" -type d
find /path/to/directory -name ".git" -type d -exec rm -rf {} \; 2>/dev/null
```
This prevents the "adding embedded git repository" warning.

### Step 2: Update parent .gitignore
Replace blanket ignores with selective ones:
```gitignore
# BAD — blocks entire directory
wiki/

# GOOD — allows .md but excludes media
wiki/
wiki/**/*.mp4
wiki/**/*.mov
wiki/**/*.m4a
wiki/**/*.mp3
wiki/**/*.wav
wiki/**/*.aac
wiki/**/*.ogg
wiki/**/*.zip
wiki/**/*.tar.gz
wiki/**/.git/
wiki/**/node_modules/
```

### Step 3: Force-add with `-f`
```bash
cd /parent/of/directory
git reset HEAD directory/ 2>/dev/null  # Unstage if previously staged
git add directory/ -f                 # -f = force add ignored files
```

### Step 4: Verify before commit
```bash
# Check size
git diff --staged --numstat | awk '{sum += $1 + $2} END {printf "%.1f MB\n", sum/1024/1024}'

# Ensure no media files leaked through
git diff --staged --name-only | grep -E "\.(mp4|m4a|mp3|mov)$"
# Output must be empty
```

### Step 5: Commit and push
```bash
git commit -m "Backup: $(date +%Y-%m-%d)"
git push origin main
```

## Backup Scopes

### Wiki + Skills + Memories (Hermes use case)
Full backup of the Hermes knowledge base at `/Volumes/Storage-1/Hermes/`:
```bash
BASE="/Volumes/Storage-1/Hermes"
cd "$BASE"

# Skills (conditional — only if changed)
if git status --short skills/ .gitignore | grep -q .; then
  git add skills/ .gitignore
  git commit -m "Backup skills: $(date +%Y-%m-%d)"
  git push origin main
fi

# Wiki (always — transcripts accumulate daily)
find wiki -name ".git" -type d -exec rm -rf {} \; 2>/dev/null
git add wiki/ -f
git commit -m "Backup wiki: $(date +%Y-%m-%d)"
git push origin main

# Memories (conditional)
if git diff --stat .hermes/memories/ | grep -q "[0-9]"; then
  git add .hermes/memories/ -f
  git commit -m "Backup memories: $(date +%Y-%m-%d)"
  git push origin main
fi
```

### Skills only (~100KB)
```bash
git add skills/ .gitignore
git commit -m "Backup skills: $(date +%Y-%m-%d)"
git push origin main
```

## Common Problems & Solutions

### Problem: "adding embedded git repository" warning
**Cause:** Nested `.git` folders inside the target directory  
**Fix:** `find dir -name ".git" -type d -exec rm -rf {} \;`

### Problem: "nothing to commit" even though files changed
**Cause:** Parent `.gitignore` has a blanket rule like `wiki/`  
**Fix:** Replace with selective excludes (see Step 2 above)

### Problem: Wiki/repository too large (500MB+)
**Cause:** Video/audio files from transcript extraction  
**Fix:** Delete by extension AND by file type detection:
```bash
# By extension
find wiki -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.m4a" -o -name "*.mp3" \) -size +1M -delete

# By file type (catches mislabeled files)
find wiki -type f -size +1M | while read f; do
  type=$(file -b "$f")
  if echo "$type" | grep -qE "ISO Media|MPEG ADTS|ALAC|AAC"; then
    rm "$f" && echo "Deleted: $f"
  fi
done
```

## .gitignore Template for Wiki Backup

```gitignore
# Large media — EXCLUDE
*.mp4 *.mov *.m4a *.mp3 *.wav *.aac *.ogg *.zip *.tar.gz *.tgz

# Embedded repos — do NOT backup
dflash/ human-cli/ rowboat/ projects/*/

# Large cache/index — exclude
.processed/ .search_index.json fine-tuned-wiki/ *.safetensors

# Wiki-specific nested .git (should be removed, but just in case)
wiki/**/.git/
```

## File Type Decisions

| Type | Backup? | Reason |
|------|---------|--------|
| .md (markdown) | ✅ Yes | Text, compresses well |
| .json (configs) | ✅ Yes | Small text files |
| Images (.png, .jpg) | ⚠️ Careful | Can bloat repo |
| Video (.mp4, .mov) | ❌ No | Too large |
| Audio (.m4a, .mp3) | ❌ No | Too large |
| .git/ folder | ❌ No | Never backup git internals |
| node_modules/ | ❌ No | Rebuildable |

## Related Skills

- `github-wiki-backup` — Specialized for Hermes wiki + skills + memories backup
- `github-large-folder-backup` — Generic version for any large folder
- `github-nested-repo-backup` — Focuses on the nested .git problem
- `hermes-github-backup` — Initial setup and cron job configuration
