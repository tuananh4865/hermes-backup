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

### 3. Create .gitignore (IMPORTANT - với wiki backup)
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

# Large media - EXCLUDE from backup
*.mp4
*.mov
*.avi
*.mkv
*.m4a
*.mp3
*.wav
*.aac
*.ogg
*.zip
*.tar.gz
*.tgz

# Node
node_modules/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Sessions & large data
sessions/
*.session
cron/output/
trajectory_samples.jsonl

# Embedded repos - do NOT backup (nested git repos cause problems)
dflash/
human-cli/
rowboat/
projects/*/

# Wiki-specific: exclude only large files, backup .md content
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

# Large cache/index
.processed/
.search_index.json
fine-tuned-wiki/
*.safetensors
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

## Common Issues & Solutions

### "embedded git repository" warning
```
warning: adding embedded git repository: wiki/concepts
warning: adding embedded git repository: wiki/hermes-agent-self-evolution
```
**Cause**: Wiki có nested `.git/` directories bên trong

**Solution (đã test):**
```bash
# Xóa tất cả nested .git trong wiki
find wiki -name ".git" -type d -exec rm -rf {} \; 2>/dev/null

# Hoặc remove khỏi git index
git rm -rf --cached wiki/concepts
git rm -rf --cached wiki/hermes-agent-self-evolution
```

### Wiki bị ignore hoàn toàn
```
hint: Use -f if you really want to add them
hint: You've added another git repository inside your current repository
```
**Cause**: Outer `.gitignore` có dòng `wiki/`

**Solution:** Remove `wiki/` khỏi .gitignore, dùng specific excludes thay thế (xem section 3 ở trên)

### Wiki quá lớn (464MB+)
**Nguyên nhân**: Wiki lưu video/audio TikTok đã download để extract transcript

**Tìm files lớn:**
```bash
find /Volumes/Storage-1/Hermes/wiki -type f -size +10M 2>/dev/null | xargs -I{} ls -lh "{}"
```

**Detect file type (không phải by extension):**
```bash
find wiki -type f -size +1M | while read f; do
  type=$(file -b "$f")
  echo "$type: $f"
done | grep -E "ISO Media|MPEG|ALAC|AAC"
```

**Xóa media files (đã test thành công):**
```bash
# Xóa theo extension
find wiki -type f \( -name "*.mp4" -o -name "*.mov" -o -name "*.m4a" -o -name "*.mp3" \) -size +1M -delete

# Hoặc xóa theo file type detection
find wiki -type f -size +1M | while read f; do
  type=$(file -b "$f")
  if echo "$type" | grep -qE "ISO Media|MPEG ADTS|ALAC|AAC"; then
    rm "$f"
    echo "Deleted: $f ($type)"
  fi
done
```

**Kết quả:** Wiki giảm từ 464MB → 111MB → 74MB sau khi xóa media

---

## Backup Scope - Phương pháp ĐÃ THÀNH CÔNG

### ✅ Backup Wiki + Skills + Memories (~100MB sau khi cleanup)

**Ưu điểm:**
- Wiki (markdown content) được backup đầy đủ
- Skills được backup thường xuyên
- Memories được backup

**Workflow đã test thành công:**
```bash
cd /Volumes/Storage-1/Hermes

# 1. Xóa nested .git repos (gây "embedded git repository" warning)
find wiki -name ".git" -type d -exec rm -rf {} \; 2>/dev/null

# 2. Force add wiki (đã được .gitignore configure để exclude media)
git add wiki/ -f

# 3. Add skills và memories
git add skills/ .hermes/memories/ .gitignore

# 4. Commit và push
git commit -m "Backup $(date +%Y-%m-%d)"
git push origin main
```

**Kết quả thực tế:**
- Wiki: 3,559 files, ~100MB (sau khi xóa media)
- Skills: ~100KB
- GitHub repo: https://github.com/tuananh4865/hermes-backup

### ⚠️ Chỉ backup Skills (~100KB)
```bash
git add skills/ .gitignore
```
- Pros: Nhanh, nhẹ
- Cons: Wiki không backup

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
- **Symlink**: `~/.hermes/skills` → `/Volumes/Storage-1/Hermes/skills`
- **external_dirs config**: `/Volumes/Storage-1/Hermes/skills` in `~/.hermes/config.yaml`
- **Cron job**: Hermes Daily Backup (job_id: `7cba6ba5f52a`) - 3AM daily, backup wiki + skills + memories
- **Wiki backup size**: ~74MB (sau khi xóa media)
- **Wiki files**: 3,559 markdown files đã backup thành công
