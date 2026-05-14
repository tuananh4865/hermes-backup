---
title: Hermes GitHub Backup Setup
name: hermes-github-backup
created: 2026-04-28
updated: 2026-05-11
type: skill
tags: [github, backup, git, hermes-agent]
description: Setup GitHub backup cho Hermes Agent data lên GitHub repo riêng
trigger: Khi cần backup hoặc restore Hermes data
---

# Hermes GitHub Backup Setup

## Architecture (Updated 2026-05-08)

**Skills location**: `~/.hermes/skills/` (copied from `/Volumes/Storage-1/Hermes/skills/`)
- Symlink removed — skills now live natively in `~/.hermes/`
- External dirs config: `external_dirs: []` (no longer pointing to Storage-1)

**Backup scope**: Full `~/.hermes/` — skills, memories, workers, config, sessions
- **No wiki** — wiki backup SEPARATE via its own cron
- Wiki path: `/Volumes/Storage-1/Hermes/wiki/` → backup to `https://github.com/tuananh4865/my-llm-wiki`

## Wiki Backup Architecture

**Wiki repo**: `https://github.com/tuananh4865/my-llm-wiki` (NOT `hermes-backup`)
**Wiki path**: `/Volumes/Storage-1/Hermes/wiki/`
**Wiki backup**: SEPARATE from hermes backup. Wiki has its own sync mechanism.

**CRITICAL: Wiki .gitignore entries** (required to prevent tracking hermes data):
```
# Hermes data (not wiki)
../skills/
../workers/
../.hermes/
```
These must be in wiki's `.gitignore` to prevent cross-contamination.

**Fix for "wiki tracking skills/workers" issue (2026-05-08)**:
1. Wiki remote was pointing to `hermes-backup` → fixed to `my-llm-wiki`
2. Wiki was tracking `../skills/` and `../workers/` → unstaged + added to `.gitignore`
3. Local/remote diverged → force push `git push origin main --force`
4. After any force push, verify: `git status` should show clean

## Current Backup Cron (2026-05-13)

**Hermes Backup Job ID**: `7cba6ba5f52a` — Hermes Daily Backup, 3AM daily
**Wiki Backup**: SEPARATE — wiki syncs to `my-llm-wiki` via its own mechanism (manual or separate cron)

**Hermes backup command (with safety check)**:
```bash
cd ~/.hermes

# SAFETY: Abort any in-progress rebase before backing up
# (a mid-rebase state causes git add . to stage rebase files as "changes")
if git status | grep -q "rebase\|rebasing"; then
    git rebase --abort 2>/dev/null
fi

git add .
git commit -m "Backup hermes full: $(date +%Y-%m-%d)"
git push origin main
```

**Why the rebase check matters:**
- If a previous session was mid-rebase when interrupted, `git add .` stages those partial rebase files
- `git commit` then wraps rebasing state into a commit — corrupting history
- Always `git rebase --abort` first if ANY rebase state is detected

**What gets backed up**:
- `~/.hermes/skills/` — all 55 skills
- `~/.hermes/memories/` — MEMORY.md, TASK_STATE.md, DECISION_LOG.md
- `~/.hermes/workers/` — SOUL.md, HEARTBEAT.md, outputs
- `~/.hermes/autoresearch/` — research loop data
- `~/.hermes/config.yaml` — Hermes config

**NOT backed up**: Wiki (`/Volumes/Storage-1/Hermes/wiki/`) — separate repo

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
git add .
git commit -m "Initial backup"
git push origin main
```

### 6. Critical: Secret Scanning Block (auth.json)

GitHub Secret Scanning auto-blocks pushes containing `auth.json` files even on `--force` push. The remote rejects with:
```
remote: error: GH013: Repository rule violations found for refs/heads/main.
remote: Push cannot contain secrets
remote:   — GitHub Personal Access Token —
remote:   locations:
remote:     - commit: XXXXXX path: profiles/research-lead/auth.json:12
```

**Prevention — .gitignore MUST include auth files:**
```gitignore
# Auth files (contain secrets — BLOCKED by GitHub secret scanning)
auth.json
profiles/**/auth.json
state-snapshots/**/auth.json
```

**Fix if push is blocked:**
```bash
# 1. Update .gitignore to exclude auth files
echo -e "\n# Auth files (contain secrets)\nauth.json\nprofiles/**/auth.json\nstate-snapshots/**/auth.json" >> .gitignore

# 2. Remove cached auth files from git index
git rm --cached -f auth.json profiles/**/auth.json state-snapshots/**/auth.json 2>/dev/null

# 3. Amend the commit (removes auth files from history)
git commit --amend -m "Backup hermes full: $(date +%Y-%m-%d)"

# 4. Push again
git push origin main --force
```

### 7. Cron Job (auto backup 3AM daily)
```bash
cd ~/.hermes

# SAFETY: Abort any in-progress rebase before backing up
if git status | grep -q "rebase\|rebasing"; then
    git rebase --abort 2>/dev/null
fi

git add .
git commit -m "Backup hermes full: $(date +%Y-%m-%d)"
git push origin main
```

**Recovery when push is rejected (non-fast-forward):**
```bash
# Option 1: Abort any mid-rebase, then force push (preferred — preserves local state)
git rebase --abort 2>/dev/null
git push origin main --force

# Option 2: Pull with rebase, handle conflicts, continue
git pull --rebase origin main
# If conflicts → git rebase --abort (discard remote changes and force push)
# If clean → git push origin main
```

**Why force push is safe here:** This is a personal backup repo — no collaborators. Force push replaces remote with local, which is the intended behavior.

**Note**: Skills live natively at `~/.hermes/skills/` — no symlink, no external_dirs needed.

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
## Telegram Reporting

**Chat ID**: `1132914873` (Tuấn Anh DM)
**Thread ID**: `3764041476` (reply_to_message_id for threading)
**Bot**: `ClawdZ1E_Bot`

**Get token from .env** (IMPORTANT: variable name is `TELEGRAM_BOT_TOKEN`, NOT `TG_BOT_TOKEN`):
```bash
TELEGRAM_BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2)
```

**Pre-flight check** (do this before sending):
```bash
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "⚠️ TELEGRAM_BOT_TOKEN not set — skipping Telegram notification"
fi
```

**Send notification** (only if `TELEGRAM_BOT_TOKEN` is set):
```bash
TELEGRAM_BOT_TOKEN=$(grep "^TELEGRAM_BOT_TOKEN=" ~/.hermes/.env | cut -d= -f2)
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=1132914873" \
  -d "reply_to_message_id=3764041476" \
  -d "text=<message>"
```

**Failure mode**: If `TELEGRAM_BOT_TOKEN` is not set, backup still completes — just skip Telegram. Never block on missing env var.

**Common error**: `{"ok":false,"error_code":404,"description":"Not Found"}` means wrong token or wrong bot API URL. Verify token is correct in `~/.hermes/.env`.

---

## Related

- `references/secret-scanning-fix-2026-05-09.md` — Resolution for GitHub Secret Scanning block on first push

## Notes

- **Hermes backup repo**: https://github.com/tuananh4865/hermes-backup (full ~/.hermes backup)
- **Wiki repo**: https://github.com/tuananh4865/my-llm-wiki (separate wiki backup)
- **Skills location**: `~/.hermes/skills/` (55 skills, native location)
- **external_dirs config**: `external_dirs: []` (cleared 2026-05-08)
- **Cron job**: Hermes Daily Backup (job_id: `7cba6ba5f52a`) - 3AM daily, backup full `~/.hermes/`
- **Wiki backup**: Separate from hermes — wiki syncs to `my-llm-wiki`
