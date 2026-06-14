---
name: hermes-daily-backup
description: Daily cron-driven backup of an EXISTING git repo to its OWN remote (e.g. `~/.hermes` → tuananh4865/hermes-backup). Use when a cron job says "backup full <folder> lên GitHub mỗi ngày" where the folder is already a working git repo with its own remote — NOT for first-time setup (use hermes-github-backup) and NOT for backup of a foreign folder INTO another repo (use github-large-folder-backup). Produces a structured report — file count, insertions, deletions, push SHA, errors.
category: devops
---

# Hermes Daily Backup (Same-Repo Push)

## Problem
Cron job chạy hằng ngày cần:
1. Stage toàn bộ thay đổi trong một git repo đã có sẵn (e.g. `~/.hermes`)
2. Commit + push lên chính remote `origin` của repo đó
3. Báo cáo: số file changed, insertions, deletions, push SHA, lỗi (nếu có)

Khác với:
- **`hermes-github-backup`** — one-time setup, clone/fork lần đầu
- **`github-large-folder-backup`** — backup folder NGOÀI vào repo khác (xử lý nested .git, force add, media exclusion)

## Step-by-Step Process

### Step 1: Pre-flight (verify repo + remote)
```bash
cd ~/.hermes                                # hoặc target repo
pwd
git rev-parse --abbrev-ref HEAD            # confirm branch
git remote -v | head -5                     # confirm origin
git config user.name && git config user.email   # confirm identity
```

Nếu `origin` không trỏ đúng target → DỪNG, không push. Cron job phải fail-fast chứ không push nhầm chỗ.

### Step 2: Stage + double-check trước commit
```bash
git add .
# Lưu ý: `git add .` KHÔNG stage file mới sinh ra SAU lệnh add
# (race với cron job khác đang ghi file). Luôn re-check:
git status --short
```

Các mục thường gặp cần XỬ LÝ RIÊNG (không nằm trong scope full backup):
- **Submodules** (e.g. `skills/agent-reach`): thay đổi trong submodule là của repo con. Cảnh báo user, không commit submodule pointer trừ khi user yêu cầu.
- **Nested .git directories**: nếu `git add .` báo "adding embedded git repository" → KHÔNG xóa `.git` của submodule (sẽ break install). Dùng `git rm --cached -r <path>` để untrack.

### Step 3: Commit
```bash
git commit -m "Backup hermes full: $(date +%Y-%m-%d)"
```

### Step 4: Push + verify push landed
```bash
git push origin main 2>&1
# Verify: local HEAD SHA phải match remote SHA
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git ls-remote origin main | cut -f1)
[ "$LOCAL_SHA" = "$REMOTE_SHA" ] && echo "PUSH OK" || echo "PUSH MISMATCH"
```

Một số git versions trả exit-0 dù push fail (auth-fail, non-fast-forward). Bước verify bắt buộc — exit-0 KHÔNG đủ bằng chứng.

### Step 5: Thu thập report data
```bash
# File count + insertions/deletions
git diff --shortstat HEAD~1 HEAD
# Output format: "233 files changed, 5024 insertions(+), 185 deletions(-)"
```

## Report Template (gửi Telegram/stdout)

```
✅ Hermes Daily Backup — YYYY-MM-DD
Trạng thái: Thành công
Commit: <full SHA>
Push: <old_sha>..<new_sha> main -> main (github.com/<user>/<repo>)
Thống kê: N files changed, I insertions(+), D deletions(-)
Nội dung nổi bật: [bullet list of changed top-level paths]
Lỗi: Không có. (Submodule X có thay đổi ngoài scope — quản lý riêng.)
```

## Cron Job Template
```bash
#!/bin/bash
set -e
cd ~/.hermes
git add .
# Re-stage anything that appeared mid-flight
git status --short | grep '^??' | awk '{print $2}' | xargs -r git add
git commit -m "Backup hermes full: $(date +%Y-%m-%d)" || true
git push origin main
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git ls-remote origin main | cut -f1)
[ "$LOCAL_SHA" = "$REMOTE_SHA" ]
```

Note: `|| true` trên commit để cron job không fail nếu không có gì thay đổi (empty commit không push được).

## Pitfalls
1. **`git add .` race với file mới sinh ra** — cron job khác (TikTok monitor, daily review) có thể ghi file giữa lúc `git add .` chạy và `git commit` chạy. Luôn re-check `git status --short` trước commit, hoặc dùng pattern stage-twice trong cron template.
2. **Empty commit = push fail** — Nếu không có gì thay đổi, `git commit` sẽ tạo empty commit (nếu không có `--allow-empty`) hoặc fail (nếu có). Cron cần `|| true` để idempotent.
3. **`git push` exit-0 ≠ push thành công** — Một số git versions swallow auth-fail hoặc non-fast-forward. Luôn verify `git ls-remote origin main` match local HEAD.
4. **Submodule warning spam** — Nếu `skills/agent-reach` (hoặc submodule khác) đã được track, mỗi lần backup sẽ warning "added or modified checked-out submodule". Có thể silence scoped: `git config set advice.addEmbeddedRepo false` (chỉ trong repo, không global).
5. **Commit message có `$(date +%Y-%m-%d)`** — Backup identity là NGÀY, không phải SHA. Nếu cron chạy 2 lần cùng ngày, commit message giống nhau — OK, không phải lỗi. SHA vẫn khác.
6. **Không verify branch** — Nếu cron job chạy lúc đang ở branch khác (e.g. `feature/xyz`), sẽ push nhầm branch. Luôn `git rev-parse --abbrev-ref HEAD` trước.
7. **Credentials trong cron** — HTTPS remote cần token trong credential helper. Nếu push fail với 403, kiểm tra `git config credential.helper` (macOS: `osxkeychain`).

## Verification
```bash
# 1. Local state sạch
git status --short   # chỉ nên còn submodule warning, không có M/A/D trong main repo

# 2. Remote match
git ls-remote origin main   # SHA phải == local HEAD

# 3. Report numbers
git diff --shortstat HEAD~1 HEAD   # "N files changed, I insertions(+), D deletions(-)"
```

## Related Skills
- `hermes-github-backup` — One-time setup of backup repo + remote + first push
- `github-large-folder-backup` — Backup of foreign folder INTO another repo (nested .git, force add, media exclusion)
- `git-workflow-and-versioning` — General commit/push/branch discipline

## Support Files
- `references/report-example.md` — Real output from a successful daily backup run (file counts, push SHA format, common error messages and how they were handled).
