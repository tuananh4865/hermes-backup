---
name: mac-disk-cleanup-audit
description: Audit disk usage trên macOS để tìm phần mềm/thư mục/cache/tool rác nhằm giải phóng ổ đĩa. Classify theo 3 mức độ an toàn (rõ ràng / cần xác nhận / cần check kỹ), scan 5 layer song song (Applications + ~/Library + hidden ~/.* + /opt/homebrew + Downloads/Documents), check process đang chạy trước khi gợi ý xoá app. Use when user nói "giải phóng ổ đĩa Mac", "kiểm tra phần mềm rác", "xóa cache/tool không dùng", "ổ đĩa đầy", "disk full", "cleanup mac", hoặc reports disk usage >90%. Distinct from `recurring-junk-folder-investigation` (focus vào folder lặp lại từ cron) — đây là one-off audit.
category: devops
---

# Mac Disk Cleanup Audit

## Problem

User báo: "ổ đĩa Mac đầy", "kiểm tra phần mềm rác", "xóa cache/tool không dùng", "giải phóng dung lượng".

Goal: Tìm **TẤT CẢ** rác (apps, caches, support files, hidden dirs, dev tools, models) → classify theo mức độ an toàn → present cleanup plan có evidence (sizes, paths, ps check). **KHÔNG tự ý xoá** — user phải quyết định từng mức.

## Core Philosophy

**Audit ≠ Delete.** Em quét, classify, đề xuất — user quyết định. 3-tier safety:
- 🔴 **Mức 1 — Rác rõ ràng**: bundle cache cũ, video thô đã edit, wallpaper cache → an toàn tuyệt đối
- 🟡 **Mức 2 — App không dùng**: app có `.app` trong `/Applications` nhưng user không list → cần user xác nhận
- 🟢 **Mức 3 — Cần check kỹ**: dev tools có thể phụ thuộc lẫn nhau, local LLM models, pipx venvs → cần user biết rõ

## Step-by-Step Process

### Step 1: Establish ground truth — disk usage baseline

```bash
# 1. Overall disk state
df -h /

# 2. Top-level consumption map (parallel)
du -sh ~/Library 2>/dev/null
du -sh ~/Library/Caches 2>/dev/null
du -sh ~/Library/Application\ Support 2>/dev/null
du -sh ~/Library/Logs 2>/dev/null
du -sh ~/Library/Developer 2>/dev/null

# 3. Top apps in /Applications
du -sh /Applications/* 2>/dev/null | sort -hr | head -30

# 4. Homebrew if installed
du -sh /opt/homebrew/* 2>/dev/null | sort -hr | head -15
ls /opt/homebrew/Cellar 2>/dev/null | head -30

# 5. Hidden dirs in ~ (THE BIGGEST HUNTERS)
du -sh ~/.* 2>/dev/null | sort -hr | head -20
```

**Critical:** Run these in **parallel** (single batch), không serial. Disk audit phải nhanh — user đang chờ.

### Step 2: Deep dive — top 10 heaviest items

Với mỗi layer nặng, drill xuống 1-2 level:

```bash
# Application Support breakdown
du -sh ~/Library/Application\ Support/* 2>/dev/null | sort -hr | head -25

# Caches breakdown
du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -25

# Specific big suspects: dev tools, models, caches
du -sh /opt/homebrew/Cellar/* 2>/dev/null | sort -hr | head -30
du -sh ~/.cache/* 2>/dev/null | sort -hr | head -20
du -sh ~/.local/share/* 2>/dev/null | sort -hr | head -10
ls -la ~/Library/Application\ Support/Claude/vm_bundles/ 2>/dev/null
```

### Step 3: VERIFY EVERY "CACHE" IS ACTUALLY CACHE — CRITICAL PITFALL (see P9)

**Trước khi gợi ý xoá app bất kỳ, PHẢI check 3 thứ:**

#### 3a. Check processes — app có đang chạy không?
App có `.app` trong `/Applications` ≠ app đang dùng. App KHÔNG có `.app` nhưng vẫn có `~/Library/Application Support/<bundle>/` = orphan support (có thể xoá support khi xoá app).

```bash
# Get user's stated active apps
# (from their message: "em chỉ dùng Chrome, Obsidian, Claude Code, Hermes")

# Find processes matching candidate "unused" apps
ps aux | grep -iE "Lark|Manus|Factory|Antigravity|Comet|Steam|Vibing|Phim|GoTiengViet|TestFlight|Jump|cmux|LM Studio" | grep -v grep | awk '{print $11}' | sort -u

# If empty → app confirmed not running → can suggest uninstall
# If non-empty → app still active → DO NOT suggest removal
```

**Pattern:** App running ≠ keep forever. User có thể có app chạy nền nhưng không dùng → vẫn cần hỏi.

#### 3b. Check VM bundle structure — KHÔNG xoá nếu là live sandbox
**Đây là pitfall #9** — Claude Code / Codex / Cursor chạy trong Linux VM (gVisor), bundle KHÔNG phải cache. Apply check này cho MỌI `<App>/vm_bundles/` hoặc `*.bundle`:

```bash
# Bất kỳ bundle nào có rootfs + sessiondata + efivars = LIVE VM
ls -la ~/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle/ 2>/dev/null
# Red flags: rootfs.img ≥ 5GB, sessiondata.img ≥ 1GB, .cowork-adopted marker, gvisorMacAddress, vmIP
# → KHÔNG xoá. Xem P9 để biết chi tiết + list các app tương tự.

# Quick check: bundle có structure VM không?
ls <bundle-path>/ 2>/dev/null | grep -E "rootfs\.img|sessiondata|efivars|gvisor|vmIP"
# Nếu có → LIVE VM → giữ
```

**App có VM sandbox tương tự Claude Code** (KHÔNG xoá bundle của): Cursor, Codex CLI, Docker Desktop, OrbStack, Lima, ChatGPT Desktop, Google AI Studio Desktop.

### Step 4: Classify each candidate into 3 tiers

#### 🔴 Mức 1 — RÁC RÕ RÀNG (safe to delete, ~30GB typical)

Criteria: cache/bundle của app đang dùng, không phải user data, tự build lại được.

Common candidates:
| Path pattern | Size typical | Why safe |
|---|---|---|
| `~/Library/Application Support/<App>/vm_bundles/` | 1-20GB | VM bundles tự rebuild — **XEM P9**: Claude Code `vm_bundles` là LIVE sandbox, KHÔNG xoá |
| `~/Library/Application Support/com.apple.wallpaper` | 1-10GB | Wallpaper cache |
| `~/Library/Caches/ms-playwright/chromium-*` (old versions) | 100-600MB each | New version dùng được |
| `~/Library/Caches/Homebrew` | 100-500MB | Download cache |
| `~/Library/Caches/pip` | 50-200MB | pip rebuild on install |
| `~/Library/Application Support/<App>/Cache/` (not user data) | 100-500MB | App rebuilds on launch |
| `~/Library/Logs/` (all files) | 5-50MB | Diagnostic logs |
| `~/Downloads/*.MOV` (raw video >1GB, đã edit xong) | variable | Sau khi confirm video đã process |
| `~/Library/Caches/<App>/` for uninstalled apps | variable | App không còn → cache orphan |

**Verification before suggesting:** `ls -la <path>` để check mtime. Nếu < 30 days old + không có data user → OK.

#### 🟡 Mức 2 — APP KHÔNG DÙNG (user confirm)

Criteria: `.app` exists in `/Applications` BUT not in user's stated active list.

**Format:** List app + size + support files size + total.

Example:
```
| App | .app size | Support files | Total |
|-----|-----------|---------------|-------|
| Manus.app | 339MB | 1.6MB | ~341MB |
| Factory.app | 423MB | 0MB | 423MB |
```

**Pitfall:** Cũng check app launch at login:
```bash
osascript -e 'tell application "System Events" to get the name of every login item'
```
Nếu app trong login items → user dùng nó thường xuyên → KHÔNG list.

#### 🟢 Mức 3 — CẦN CHECK KỸ (dev tools, models, venvs)

Criteria: dev tools có thể phụ thuộc lẫn nhau, models tốn dung lượng lớn.

Common candidates:
- **Local LLM models** (`~/.lmstudio/models/`, `~/.cache/huggingface/`): 2-15GB
- **pipx venvs** (`~/.local/pipx/venvs/`): 100MB-1GB each
- **Homebrew Cellar duplicates** (e.g., `ffmpeg` + `ffmpeg-full`): MB-GB
- **Unused Cellar packages**: check `which <binary>` for each, nếu binary không trong PATH → orphan
- **Python venvs** (`~/.venvs/`): 100MB-1GB each

**Verification before suggesting:**
```bash
# Is binary actually used?
which <binary> 2>/dev/null
# If empty → orphan

# Is model loaded recently?
stat -f "%Sm" ~/.lmstudio/models/<model-dir>/ 2>/dev/null
# If > 30 days → likely unused

# Cross-reference: pipx list (which venvs are installed)
pipx list 2>/dev/null
```

### Step 5: Present plan with 3-tier table

**Output template:**

```markdown
## 🗑️ BÁO CÁO RÁC MAC

**Tổng ổ gốc: XGB | Đã dùng: YGB (Z%) | Trống: WGB**

### 🔴 MỨC 1 — Rác rõ ràng (~30GB)
| Path | Size | Lý do xoá |
|---|---|---|
| ... | ... | ... |

### 🟡 MỨC 2 — App không dùng (~5GB)
| App | Total size | Ghi chú |
|---|---|---|
| ... | ... | ... |

### 🟢 MỨC 3 — Cần check kỹ (~10-20GB nếu xoá local LLM)
| Item | Size | Cân nhắc |
|---|---|---|
| ... | ... | ... |

### ✅ Tổng giải phóng: ~XX-YY GB

## 🤔 CÂU HỎI CẦN XÁC NHẬN

1. [Specific question per Mức 2/3 item]
2. ...
```

### Step 6: CHỜ USER CONFIRM — KHÔNG TỰ XOÁ

**Critical:** Sau khi present plan, em PHẢI hỏi user confirm trước khi xoá batch. Nếu user nói "OK xoá hết Mức 1" → chỉ xoá Mức 1, KHÔNG tự ý xoá Mức 2/3.

**Backup before batch delete (nếu user explicit):**
```bash
# Backup configs quan trọng trước
mkdir -p /tmp/disk-cleanup-backup-$(date +%Y%m%d)
cp -r ~/Library/Application\ Support/Claude /tmp/disk-cleanup-backup-*/
# (only configs, không backup 16GB cache)
```

### Step 7: Verify cleanup results

```bash
# Before/after comparison
df -h /

# Per-item verify (nếu selective delete)
ls -la <deleted-path> 2>&1 | head -3
# expect "No such file or directory"
```

## Parallel Scan Recipe (5-batch, ~30s total)

```bash
# Batch 1: ground truth (3 commands parallel)
df -h /
du -sh ~/Library /Applications /opt/homebrew 2>/dev/null

# Batch 2: Library breakdown (3 commands parallel)
du -sh ~/Library/Application\ Support/* 2>/dev/null | sort -hr | head -25
du -sh ~/Library/Caches/* 2>/dev/null | sort -hr | head -25
du -sh ~/Library/Developer/* 2>/dev/null

# Batch 3: Homebrew + hidden dirs (2 commands parallel)
du -sh /opt/homebrew/Cellar/* 2>/dev/null | sort -hr | head -30
du -sh ~/.* 2>/dev/null | sort -hr | head -20

# Batch 4: dev tools + caches (3 commands parallel)
du -sh ~/.cache/* 2>/dev/null | sort -hr | head -20
du -sh ~/.local/share/* 2>/dev/null | sort -hr | head -10
ls -la ~/Library/Application\ Support/Claude/vm_bundles/ 2>/dev/null

# Batch 5: process check + downloads (2 commands parallel)
ps aux | grep -iE "<unused-app-pattern>" | grep -v grep
du -sh ~/Downloads/* 2>/dev/null | sort -hr | head -10
```

**Total time:** ~30s if parallel, ~2 min if serial. ALWAYS parallel.

## Pitfalls

### P9. Claude Code `vm_bundles/claudevm.bundle` = LIVE Linux sandbox, KHÔNG phải cache (CRITICAL — almost nuked 16GB 2026-06-30)

**Anti-pattern:** Trong lần đầu viết skill này, Mức 1 table list `vm_bundles` là "safe to delete — rebuild được". Sai. Claude Code chạy mỗi session trong một Linux VM (gVisor) với rootfs + sessiondata. Xoá bundle = Claude Code phải tải lại 10GB rootfs về (30-60 phút + bandwidth).

**Detection — structure trước khi classify:**
```bash
ls -la ~/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle/
# Nếu thấy .cowork-adopted + gvisorMacAddress + vmIP + rootfs.img (~10GB)
#   + sessiondata.img (~5GB) + efivars.fd + machineIdentifier
#   → ĐÂY LÀ LIVE VM, KHÔNG XOÁ
```

**Red flags của LIVE VM sandbox (KHÔNG phải cache):**
- File `rootfs.img` ≥ 5GB (root filesystem)
- File `sessiondata.img` ≥ 1GB (session state — Claude Code sandbox ghi vào đây)
- Hidden file `.cowork-adopted` hoặc `.rootfs.img.origin` (đánh dấu bundle đang được dùng)
- `efivars.fd`, `gvisorMacAddress`, `vmIP` → đây là VM runtime state, không phải cache

**Real-world size (Tuấn Anh, 2026-06-30):**
```
9.9G  rootfs.img            ← Linux root filesystem (Claude Code sandbox)
4.9G  sessiondata.img       ← VM session state
1.2G  rootfs.img.zst        ← compressed source để rebuild nếu rootfs.img corrupt
16G   TOTAL — KHÔNG ĐƯỢNG XOÁ nếu user dùng Claude Code
```

**Câu hỏi bắt buộc trước khi classify bất kỳ `vm_bundles` nào vào Mức 1:**
> "User có đang dùng <App> không?" — nếu user list app đó trong active stack → VM bundle PHẢI GIỮ. Chỉ classify là rác khi app ĐÃ uninstall hoàn toàn.

**Fix — verify trước khi recommend xoá:**
```bash
# 1. Check rootfs.img có đang được mmap/open không (means VM đang chạy)
lsof ~/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle/rootfs.img 2>/dev/null | head -5
# Nếu có output → VM live → KHÔNG xoá

# 2. Check mtime của rootfs.img
stat -f "%Sm" ~/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle/rootfs.img
# Nếu < 24h → Claude Code dùng trong 24h qua → giữ

# 3. Check bundle có marker files không
ls ~/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle/ | grep -E "adopted|origin|gvisor|vmIP|efivars"
# Nếu có → LIVE VM
```

**Generalization:** Bất kỳ `<App>/<sandbox>/*.bundle` nào có pattern `[rootfs|sessiondata|efivars|vmIP|gvisor]` → VM sandbox, KHÔNG xoá. Các app nguy hiểm tương tự: Cursor (Cawtine), Codex CLI (vm bundles), Docker Desktop (`~/Library/Containers/com.docker.docker/`), OrbStack, Lima.

### P1. Gợi ý xoá app mà không check `ps aux` (CRITICAL)

**Anti-pattern:** "App X không có trong list dùng → đề xuất xoá" mà KHÔNG kiểm tra app có đang chạy nền không.

**Failure mode (real):** Background app (antivirus, sync, monitoring) chiếm GB nhưng user không list nó → em tưởng là rác → gợi ý xoá → app đang sync data quan trọng.

**Fix:** LUÔN chạy `ps aux | grep -iE "<app-name>"` trước khi classify app là "không dùng". Empty result = safe. Non-empty result = STOP, hỏi user.

### P2. Bundle support không có `.app` vẫn chiếm chỗ

**Symptom:** User xoá app X, nhưng `~/Library/Application Support/X/` vẫn còn 1-2GB. macOS không auto-clean support files khi xoá `.app`.

**Detection:** Tìm `~/Library/Application Support/<bundle-id>/` mà KHÔNG có `/Applications/<App>.app/` tương ứng.

**Fix:** Khi classify app vào Mức 2, include cả `.app` + support files + cache:
```
Manus.app (339MB) + ~/Library/Application Support/Manus (1.6MB) = 341MB total
```

### P3. `du -sh /*` ở root scan quá lâu

**Anti-pattern:** `du -sh /* 2>/dev/null` scan toàn bộ root → timeout 180s.

**Fix:** Scope hẹp từ đầu:
```bash
# ✅ Scan 5 chỗ user-level, không scan system dirs
du -sh /Applications ~/Library ~/Downloads ~/Documents ~/Desktop 2>/dev/null
du -sh /opt/homebrew 2>/dev/null  # chỉ homebrew
```

System dirs (`/System`, `/usr`, `/private`) gần như không có junk user xoá được.

### P4. Cache size khác nhau wildly giữa các lần scan

**Symptom:** Scan lần 1 thấy `~/Library/Caches/Google = 763MB`. Scan lần 2 (5 phút sau) thấy `= 1.2GB`. Chrome auto-update cache liên tục.

**Fix:** Present **moment-in-time snapshot**, không promise "số này sẽ giữ nguyên". Cache rebuild nhanh.

### P5. App launch at login = "đang dùng" nhưng không có trong list

**Detection:**
```bash
osascript -e 'tell application "System Events" to get the name of every login item'
```

**Interpretation:** Nếu app X có trong login items nhưng user không list → có thể user quên, hoặc app set auto từ lúc cài. HỎI user, không tự classify.

### P6. Homebrew cask vs formula cleanup khác nhau

**Anti-pattern:** `brew cleanup` xoá cả unused Cellar packages. Nếu user có app dùng python@3.11 mà system có python@3.14 → `cleanup` có thể xoá cả 2.

**Fix:** TRƯỚC KHI chạy `brew cleanup`, check:
```bash
brew autoremove --dry-run  # show what would be removed
```

Present dry-run output cho user xem, KHÔNG chạy `autoremove` không confirm.

### P7. LM Studio models có thể rebuild từ HuggingFace cache

**Cross-reference:**
- `~/.lmstudio/models/<model>/` (theo model name) — file GGUF
- `~/.cache/huggingface/hub/<model>--<variant>/` — original HF download

**Nếu xoá LM Studio models:** Download lại từ UI (~5-30 phút/model tùy size).
**Nếu xoá HF cache:** LM Studio models KHÔNG mất (file khác path), nhưng không thể re-download offline.

**Decision rule:** Hỏi user "có dùng local LLM không?" trước khi classify. Nếu KHÔNG → cả 2 đều xoá được.

### P8. Xcode DerivedData + CoreSimulator chiếm chỗ khổng lồ nếu user từng dev iOS

**Detection:**
```bash
du -sh ~/Library/Developer/Xcode/DerivedData 2>/dev/null
du -sh ~/Library/Developer/CoreSimulator 2>/dev/null
```

Mỗi cái có thể 5-50GB. User KHÔNG dev iOS = xoá an toàn.

**Question to ask:** "Anh có dev iOS/macOS app không? Nếu không, DerivedData + Simulator xoá được ~XGB."

## Cleanup Script Template (chỉ chạy sau khi user confirm)

```bash
#!/bin/bash
# mac-disk-cleanup.sh — CHẠY SAU KHI USER CONFIRM TỪNG MỨC
set -e
LOG=/tmp/disk-cleanup-$(date +%Y%m%d-%H%M%S).log
echo "=== Disk cleanup started $(date) ===" | tee -a $LOG

# Mức 1 — safe (user confirm "OK Mức 1")
echo "[Mức 1] Removing obvious junk..." | tee -a $LOG
rm -rf ~/Library/Application\ Support/Claude/vm_bundles/claudevm.bundle
rm -rf ~/Library/Application\ Support/com.apple.wallpaper
# ... thêm paths theo plan

# Mức 2 — app uninstall (cần user confirm từng app)
# Mức 3 — dev tools (cần user confirm từng item)

echo "=== Done. Verifying... ===" | tee -a $LOG
df -h / | tee -a $LOG
echo "Log: $LOG"
```

**Best practice:** Save script to `/tmp/mac-disk-cleanup-<date>.sh`, present cho user xem trước khi chạy. User review paths → OK → run.

## Verification After Cleanup

```bash
# 1. Disk space reclaimed
df -h /
# Expected: free space tăng tương ứng với tổng Mức 1+2+3 đã xoá

# 2. Critical apps still launch (Chrome, Obsidian, etc.)
open -a "Google Chrome" && echo "✅ Chrome OK" || echo "❌ Chrome broken"
open -a "Obsidian" && echo "✅ Obsidian OK" || echo "❌ Obsidian broken"

# 3. No zombie support files
find ~/Library/Application\ Support -maxdepth 1 -type d 2>/dev/null | wc -l
# So sánh với số trước cleanup

# 4. ~/.zshrc, ~/.bash_profile, etc. intact
ls -la ~/.*rc ~/.*profile 2>/dev/null
```

## Related Skills

- `recurring-junk-folder-investigation` — SIBLING skill. Focus vào folders LẶP LẠI từ cron. Nếu sau khi cleanup mà folder X tự tạo lại → switch sang skill đó.
- `self-verify-after-workaround` — Verify cleanup actually freed space, không phải "should have freed"
- `daily-code-health-check` — Daily inspection, có thể add disk usage check
- `transcript-cleanup` — Specific cho media files (video/audio), sibling concept

## When NOT to Use This Skill

- User chỉ muốn xoá 1-2 files cụ thể (path đã biết) → dùng `terminal rm` trực tiếp
- Folder keeps reappearing after delete → `recurring-junk-folder-investigation`
- User nghi ngờ malware / system binary → `hermes-security-audit`
- User muốn backup trước khi xoá → đó là separate workflow