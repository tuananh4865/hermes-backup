---
name: hermes-github-backup
description: Setup GitHub backup for Hermes Agent data
created: 2026-04-27
updated: 2026-04-27
type: skill
tags: [hermes, backup, github, git]
---

# Hermes GitHub Backup Setup

## Overview
Setup daily GitHub backup cho Hermes Agent data. Chạy tự động mỗi sáng.

## Key Learnings (Trial & Error)

### ✅ Works
- Skills: backup được (~100KB)
- `.gitignore` để exclude sensitive files và large folders
- GitHub CLI (`gh`) đã auth cho anh

### ❌ DON'T
- KHÔNG backup wiki/ (464MB - TOO LARGE for GitHub)
- KHÔNG backup scripts/ (thường có embedded .git repos)
- KHÔNG backup projects/ (chưa clean)
- KHÔNG commit embedded git repos ( gây lỗi `advice.addEmbeddedRepo`)

## Setup Steps

### 1. Tạo GitHub Repo
```bash
gh repo create hermes-backup --public --description "Hermes Agent backup"
```

### 2. Init git ở Storage-1/Hermes
```bash
cd /Volumes/Storage-1/Hermes
git init
git remote add origin https://github.com/tuananh4865/hermes-backup.git
```

### 3. Create .gitignore
```gitignore
# Sensitive data
*.key
*.pem
*.env
api_key
MINIMAX_API_KEY
GITHUB_PAT

# Python
__pycache__/
*.py[cod]
venv/

# macOS
.DS_Store

# Large folders - TOO BIG for GitHub
wiki/
scripts/
projects/

# Sessions & logs
sessions/
*.log
cron/output/
trajectory_samples.jsonl
```

### 4. Backup Chỉ Skills (92KB)
```bash
git add skills/ .gitignore
git commit -m "Backup $(date +%Y-%m-%d)"
git push origin main
```

### 5. Wiki Backup Options (Tích hợp sau)
Vì wiki quá lớn, có 2 options:
1. **GitHub LFS** - trả phí, lưu large files
2. **Chỉ backup metadata** - index, log, schema (vài MB)
3. **Compress** - nén thành .tar.gz nhưng restore phức tạp

## Cron Job
Tạo cron job backup hàng ngày lúc 3AM, deliver Telegram thread.

## Files
- `/Volumes/Storage-1/Hermes/` - git repo root
- `~/.hermes/config.yaml` - chứa skills external_dirs config
