---
title: Hermes GitHub Backup Setup
name: hermes-github-backup
created: 2026-04-28
updated: 2026-04-28
type: skill
tags: [github, backup, git, hermes-agent]
description: Setup GitHub backup cho Hermes Agent data lên GitHub repo riêng
trigger: Khi cần backup hoặc restore Hermes data
---

# Hermes GitHub Backup Setup

## Quick Setup

### 1. Create GitHub Repo
```bash
gh repo create hermes-backup --public --description "Hermes Agent backup"
```

### 2. Init git in storage location
```bash
cd /Volumes/Storage-1/Hermes
git init
git remote add origin https://github.com/tuananh4865/hermes-backup.git
```

### 3. Create .gitignore (IMPORTANT)
```bash
cat > .gitignore << 'EOF'
# Sensitive data
*.key
*.pem
*.env
.env
secrets/
credentials/

# API keys
api_key
MINIMAX_API_KEY
GITHUB_PAT

# Python
__pycache__/
*.py[cod]
venv/
env/
.venv/

# macOS
.DS_Store

# Logs
*.log
logs/

# Large media (VIDEO/AUDIO - common mistake!)
*.mp4
*.mov
*.avi
*.mkv
*.m4a
*.webm

# Sessions & large data
sessions/
*.session
cron/output/
trajectory_samples.jsonl

# Large folders - store separately
wiki/
scripts/
projects/
EOF
```

### 4. GitHub CLI Login
```bash
gh auth login
```

### 5. First Push
```bash
git add skills/ .gitignore
git commit -m "Initial backup"
git push origin main
```

---

## Common Issues

### "embedded git repository" warning
```
warning: adding embedded git repository: projects/orchestrator-agent-projects
```
**Cause**: Folder bên trong có `.git/` directory
**Fix**: Xóa `.git` trong folder đó hoặc remove khỏi index:
```bash
git rm -r --cached path/to/embedded/repo
```

### Wiki quá lớn (464MB+)
**Nguyên nhân**: Wiki lưu video/audio TikTok đã download để extract transcript

**Tìm files lớn:**
```bash
cd /Volumes/Storage-1/Hermes/wiki
find . -type f -size +10M 2>/dev/null
file *  # check file types
```

**File types phổ biến chiếm dung lượng:**
| Type | Size | Notes |
|------|------|-------|
| `.mp4` (TikTok videos) | 20-40MB each | Download để extract transcript, có thể xóa sau |
| `.m4a` (Audio) | 5-10MB each | Audio from videos |
| `.safetensors` | vài MB | Fine-tuning data |
| `.search_index.json` | vài MB | Search index, có thể regenerate |

**Giải pháp:**
1. Xóa video/audio sau khi extract transcript
2. Hoặc add vào .gitignore:
   ```
   wiki/**/*.mp4
   wiki/**/*.m4a
   wiki/**/*.mov
   ```

---

## Backup Scope quyết định

### Chỉ backup Skills (~100KB)
```bash
git add skills/ .gitignore
```
- Pros: Nhanh, nhẹ
- Cons: Wiki không backup

### Backup toàn bộ (nếu dùng Git LFS)
```bash
# Cài Git LFS
git lfs install

# Track large files
git lfs track "*.mp4"
git lfs track "*.m4a"

git add .gitattributes
git add wiki/ .gitignore
```
- Pros: Backup toàn bộ
- Cons: Cần Git LFS paid plan cho >1GB

### Backup Wiki metadata (thay vì source)
```bash
# Backup chỉ index, schema, log
git add wiki/index.md wiki/SCHEMA.md wiki/log.md wiki/_meta/ .gitignore
```
- Pros: Vài MB, wiki structure được backup
- Cons: Raw content không backup

---

## Cron Job cho Daily Backup

```yaml
# ~/.hermes/config.yaml
skills:
  external_dirs:
    - /Volumes/Storage-1/Hermes/skills
```

**Cron job backup command:**
```bash
cd /Volumes/Storage-1/Hermes
git add -A
git commit -m "Backup $(date +%Y-%m-%d)"
git push origin main
```

---

## Restore từ GitHub

```bash
# Clone repo
git clone https://github.com/tuananh4865/hermes-backup.git /tmp/hermes-backup

# Copy skills
cp -r /tmp/hermes-backup/skills/* /Volumes/Storage-1/Hermes/skills/

# Copy other files as needed
```

---

## Notes

- **GitHub repo**: https://github.com/tuananh4865/hermes-backup
- **LFS required**: Nếu muốn backup video/audio
- **Symlink**: `~/.hermes/skills` → `/Volumes/Storage-1/Hermes/skills`
- **external_dirs config**: Thêm `/Volumes/Storage-1/Hermes/skills` vào `~/.hermes/config.yaml`
