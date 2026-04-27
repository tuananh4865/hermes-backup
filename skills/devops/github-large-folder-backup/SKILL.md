---
name: github-large-folder-backup
description: Backup large folder (wiki/knowledge base) lên GitHub với nested .git repos và media file exclusion
category: devops
---

# GitHub Large Folder Backup Skill

## Problem
Cần backup folder lớn (111MB wiki) lên GitHub nhưng:
1. Folder có nested .git repos bên trong
2. Parent .gitignore có rules block cả folder đó
3. Muốn exclude media files (*.mp4, *.m4a, etc.) nhưng backup markdown content

## Step-by-Step Process

### Step 1: Remove Nested .git Repos
```bash
find /path/to/folder -name ".git" -type d
# Output: folder/subfolder/.git, folder/other/.git

# Xóa tất cả nested .git
find /path/to/folder -name ".git" -type d -exec rm -rf {} \;
```

### Step 2: Update Parent .gitignore
Cần un-ignore folder đó nhưng re-exclude media files:

```gitignore
# Thay vì: wiki/  (block cả folder)
# Dùng:
# wiki/ - backup content directly

# Wiki-specific: exclude only large media
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

### Step 3: Force Add Folder
```bash
cd /parent/of/folder
git reset HEAD folder/ 2>/dev/null  # Reset nếu đã staged trước đó
git add folder/ -f  # -f force add despite gitignore
git diff --staged --numstat | awk '{sum += $1 + $2} END {print sum/1024/1024 " MB"}'
```

### Step 4: Commit và Push
```bash
git commit -m "Backup folder: $(date +%Y-%m-%d)"
git push origin main
```

## Verification
```bash
# Kiểm tra số files đã staged
git diff --staged --name-only | wc -l

# Kiểm tra số .md files (wiki content)
git diff --staged --name-only | grep -E "\.md$" | wc -l

# Verify trên GitHub
gh repo view user/repo --json diskUsage,pushedAt
```

## Key Insights

| Vấn đề | Giải pháp |
|---------|-----------|
| Nested .git repos | `find -name ".git" -type d -exec rm -rf {} \;` |
| Parent .gitignore blocks folder | Un-comment folder, thêm specific exclude rules |
| Git add không thấy files | Dùng `-f` (force) để override gitignore |
| Media files quá lớn | .gitignore pattern: `folder/**/*.mp4` etc. |

## Cron Job Template
```bash
#!/bin/bash
# Daily backup script for large folder
cd /path/to/parent

# Step 1: Clean nested repos
find folder -name ".git" -type d -exec rm -rf {} \; 2>/dev/null

# Step 2: Stage (force add to override gitignore)
git add folder/ -f

# Step 3: Commit & Push
git commit -m "Backup folder: $(date +%Y-%m-%d)"
git push origin main
```

## Pitfalls
1. **Quên xóa nested .git** → "adding embedded git repository" warning
2. **Không dùng -f flag** → Files bị gitignore block hoàn toàn
3. **Exclude quá rộng** → KHÔNG backup được content (chỉ backup .gitignore thôi)
4. **Media files vẫn lớn** → Cần verify .gitignore patterns đúng
