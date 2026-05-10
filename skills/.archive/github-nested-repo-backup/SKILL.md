---
name: github-nested-repo-backup
description: Backup large directory (like wiki) lên GitHub khi có nested .git repos và .gitignore phức tạp
category: devops
---

# GitHub Nested Repo Backup Skill

Backup 1 directory lớn (VD: wiki/ 100+ MB) lên GitHub khi directory đó có nested .git repos hoặc nằm trong .gitignore cha.

## Problem Pattern
- Directory cần backup bị ignore trong outer `.gitignore`
- Directory có nested `.git` repos (subfolders với git riêng)
- Muốn backup markdown files nhưng exclude media (.mp4, .m4a, etc.)

## Solution: 5-Step Process

### Step 1: Find and remove nested .git repos
```bash
# Tìm nested .git
find /path/to/directory -name ".git" -type d

# Xóa nested .git repos (dùng git rm --cached để không xóa files)
git rm -rf --cached /path/to/nested/.git
```

### Step 2: Update .gitignore để allow directory
```gitignore
# BAD - blanket ignore
wiki/

# GOOD - selective
# Backup wiki content directly
wiki/

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

# Large cache/index files  
wiki/scripts/.search_index.json
wiki/fine-tuned-wiki/
wiki/.processed/
```

### Step 3: Reset và force-add với `-f`
```bash
cd /path/to/outer/repo
git reset HEAD wiki/  # Unstage any previous
git add wiki/ -f      # -f = force add ignored files
```

### Step 4: Verify trước commit
```bash
# Kiểm tra size
git diff --staged --numstat | awk '{sum += $1 + $2} END {printf "%.1f MB\n", sum/1024/1024}'

# Đảm bảo không có media files
git diff --staged --name-only | grep -E "\.(mp4|m4a|mp3)$"
# Output phải trống
```

### Step 5: Commit và push
```bash
git commit -m "Backup wiki: $(find wiki -name '*.md' | wc -l) markdown files"
git push origin main
```

## Key Insight
> Khi dùng `git add <path> -f` với `-f` flag, Git sẽ force add cả những files/directories đang bị ignore bởi .gitignore. Điều này hữu ích khi bạn muốn backup chỉ 1 phần của directory (VD: .md files) nhưng không muốn xóa hết .gitignore entries.

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| "adding embedded git repository" warning | Còn nested .git | Step 1: xóa nested .git |
| "nothing to commit" dù có thay đổi | Outer .gitignore ignore cả dir | Step 2: update .gitignore |
| Chỉ 1 vài files được add | .gitignore pattern quá rộng | Kiểm tra pattern cụ thể |
