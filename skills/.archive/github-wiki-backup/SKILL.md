---
name: github-wiki-backup
description: Backup large wiki/knowledge base lên GitHub với proper .gitignore và media cleanup
category: devops
---

# GitHub Wiki Backup Skill

Backup wiki (hoặc knowledge base) lên GitHub với proper handling cho nested repos, media files, và large files.

## Backup Scope (3 Components)

The Hermes backup cron job backs up THREE separate components:

| Component | Path | When to backup |
|-----------|------|----------------|
| Skills | `/Volumes/Storage-1/Hermes/skills/` + `.gitignore` | Only if `git status --short` shows changes |
| Wiki | `/Volumes/Storage-1/Hermes/wiki/` | Always (transcripts accumulate daily) |
| Memories | `/Volumes/Storage-1/Hermes/.hermes/memories/` | Only if `git diff` shows changes |

## Complete Backup Workflow

```bash
#!/bin/bash
set -e
BASE="/Volumes/Storage-1/Hermes"
cd "$BASE"

# === 1. SKILLS (conditional) ===
if git status --short skills/ .gitignore | grep -q .; then
  echo "Backing up skills..."
  git add skills/ .gitignore
  git commit -m "Backup skills: $(date +%Y-%m-%d)"
  git push origin main
else
  echo "Skills: no changes, skipping"
fi

# === 2. WIKI (always) ===
echo "Backing up wiki..."
find wiki -name ".git" -type d -exec rm -rf {} \; 2>/dev/null
git add wiki/ -f
git commit -m "Backup wiki: $(date +%Y-%m-%d)"
git push origin main

# === 3. MEMORIES (conditional) ===
if git diff --stat .hermes/memories/ | grep -q "[0-9]"; then
  echo "Backing up memories..."
  git add .hermes/memories/ -f
  git commit -m "Backup memories: $(date +%Y-%m-%d)"
  git push origin main
else
  echo "Memories: no changes, skipping"
fi
```

## Pre-flight Checks

```bash
# Before running, verify what's changed:
git status --short skills/ .gitignore  # Skills + gitignore
git status --short wiki/               # Wiki content
git diff --stat .hermes/memories/      # Memories changes
```

## Common Problems & Solutions

### Problem 1: Wiki bị ignore hoàn toàn
```
git add wiki/ → "hint: use -f if you really want to add them"
```
**Nguyên nhân:** Outer `.gitignore` có dòng `wiki/`

**Fix:** Comment out hoặc remove `wiki/` khỏi outer .gitignore, dùng specific excludes thay thế:
```gitignore
# Thay vì:
wiki/

# Dùng:
# Wiki-specific: exclude only large media, NOT markdown content
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
wiki/scripts/.search_index.json
wiki/fine-tuned-wiki/
wiki/.processed/
```

### Problem 2: "adding embedded git repository"
```
warning: adding embedded git repository: wiki/concepts
```
**Nguyên nhân:** Wiki có nested `.git` folders từ previous git repos

**Fix:** Xóa nested .git repos trước khi add:
```bash
find wiki -name ".git" -type d -exec rm -rf {} \; 2>/dev/null
```

### Problem 3: Wiki quá lớn (500MB+)
**Nguyên nhân:** Video/audio files từ transcript extraction

**Fix:** Detect và delete media files bằng `file` command:
```bash
# Tìm và xóa video files
find /path/to/wiki -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.avi" -o -name "*.mkv" -o -name "*.webm" \) -size +1M -delete

# Tìm và xóa audio files  
find /path/to/wiki -type f \( -name "*.m4a" -o -name "*.mp3" -o -name "*.wav" -o -name "*.aac" -o -name "*.ogg" \) -size +100k -delete

# Hoặc dùng file command để detect by type (không phải by extension):
find /path/to/wiki -type f -size +1M | while read f; do
  type=$(file -b "$f")
  if echo "$type" | grep -qE "ISO Media|MPEG|ALAC|AAC"; then
    rm "$f"
    echo "Deleted $f ($type)"
  fi
done
```

## Complete Backup Workflow

```bash
#!/bin/bash
# Backup wiki to GitHub

WIKI_PATH="/Volumes/Storage-1/Hermes/wiki"
GIT_DIR="$WIKI_PATH/.git"
BACKUP_REPO="https://github.com/tuananh4865/hermes-backup.git"

cd "$WIKI_PATH" || exit 1

# 1. Remove nested .git repos
echo "Removing nested .git repos..."
find . -name ".git" -type d -exec rm -rf {} \; 2>/dev/null

# 2. Clean up large media files
echo "Cleaning up media files..."
find . -type f \( \
  -name "*.mp4" -o -name "*.mov" -o -name "*.m4a" \
  -o -name "*.mp3" -o -name "*.wav" -o -name "*.aac" \
\) -size +100k -delete 2>/dev/null

# 3. Verify .gitignore excludes media but includes .md
# (already configured in outer .gitignore)

# 4. Force add wiki content
git add . -f

# 5. Commit and push
git commit -m "Backup wiki: $(date +%Y-%m-%d)"
git push origin main
```

## .gitignore Template for Wiki Backup

```gitignore
# Large media - EXCLUDE from backup
*.mp4
*.mov
*.m4a
*.mp3
*.wav
*.aac
*.ogg
*.zip
*.tar.gz
*.tgz

# Embedded repos - do NOT backup
dflash/
human-cli/
rowboat/
projects/*/

# Large cache/index - exclude
.processed/
.search_index.json
fine-tuned-wiki/
*.safetensors

# Wiki-specific nested .git (should be removed, but just in case)
wiki/**/.git/
```

## GitHub Repo Size Management

| File Type | Action | Reason |
|-----------|--------|--------|
| .md (markdown) | ✅ Backup | Content is text, compressed well |
| .json (configs) | ✅ Backup | Small text files |
| Images (.png, .jpg) | ⚠️ Backup carefully | Can bloat repo |
| Video (.mp4, .mov) | ❌ Exclude | Too large, use external storage |
| Audio (.m4a, .mp3) | ❌ Exclude | Too large |
| .git/ folder | ❌ Exclude | Never backup git internals |
| node_modules/ | ❌ Exclude | Rebuildable |

## Related Skills
- `github-large-folder-backup` — Generic version for any large folder (wiki, datasets, etc.)
## Verification Commands

```bash
# Check what would be staged
git add wiki/ --dry-run

# Check file types in wiki
find wiki -type f | head -100 | xargs file | sort | uniq -c | sort -rn

# Check size breakdown
du -sh wiki/*/ --exclude='.git' 2>/dev/null | sort -rh | head -10

# Verify GitHub push
gh repo view tuananh4865/hermes-backup --json diskUsage,pushedAt
```

## Session Reference
- `references/2026-05-04-session.md` — 2026-05-04 backup run: signals, anti-patterns, commit conditions
