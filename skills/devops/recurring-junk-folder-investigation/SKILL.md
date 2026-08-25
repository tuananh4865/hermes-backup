---
name: recurring-junk-folder-investigation
description: Investigate FOLDERS THAT KEEP REAPPEARING after user deletes them — caused by cron jobs or scheduled scripts silently regenerating them. Use when user complains "anh đã phải xoá 2 lần rồi", "folder này tự tạo mỗi ngày", "có cron/script nào làm việc đó không", or reports any folder that resists deletion. Distinct from one-off disk-cleanup — the focus is FINDING THE PRODUCER (cron, launchd, hook, script) and stopping the loop at source.
category: devops
---

# Recurring Junk Folder Investigation

## Problem
User báo: "folder X tự tạo lại sau khi xoá" / "anh đã phải xoá N lần" / "có cron/script nào làm việc đó không?"

Goal: Tìm **NGUỒN tạo ra folder** (cron job, launchd plist, scheduled script, watcher, hook, agent), KHÔNG chỉ xoá một lần. Loop sẽ tiếp tục nếu không stop source.

## Step-by-Step Process

### Step 1: Confirm folder đó còn tồn tại ở đâu
```bash
# Scope hẹp — KHÔNG grep toàn disk (timeout như đã gặp 06-30)
ls -la <path-of-junk-folder>
# Check cả parent dirs nếu folder bị re-create ở nhiều nơi
find ~ -maxdepth 4 -type d -name "<junk-pattern>" 2>/dev/null | head -20
```

### Step 2: CHECK CRONS TRƯỚC (priority #1)
User đã hint "check cron" → đây là #1 attack surface. Đừng skip.
```bash
# Cron Hermes (LLM-driven jobs)
hermes cron list   # xem tất cả 18 active jobs + prompt + schedule

# Cron system (crontab user + root)
crontab -l 2>/dev/null
ls -la /etc/cron.d/ /etc/cron.daily/ /etc/cron.hourly/ 2>/dev/null

# Launchd (macOS) — built-in cron equivalent, dễ quên
ls -la ~/Library/LaunchAgents/ 2>/dev/null
launchctl list 2>/dev/null | grep -v "com.apple\|org\."
```

Match folder name/pattern với prompt của cron job. Tìm job có:
- Schedule daily/hourly (likely match daily folder naming `YYYY-MM-DD`)
- Prompt đề cập tới backup, sync, snapshot, content-creator, metadata
- Script field tham chiếo folder path

### Step 3: Match cụ thể job + prompt
Khi đã có job ID nghi vấn:
```bash
# Đọc full prompt + script của job đó (skill cron KHÔNG có 'show' subcommand)
# Workaround: read jobs.json trực tiếp
python3 -c "
import json
with open('~/.hermes/cron/jobs.json') as f:
    data = json.load(f)
# data có thể là list hoặc dict tùy version
for job in (data if isinstance(data, list) else data.get('jobs', [])):
    print(json.dumps(job, indent=2))
" | grep -B2 -A 30 "junk-folder-pattern"
```

### Step 4: Verify hypothesis — folder tạo từ job đó
```bash
# Đọc output log gần nhất của job
ls -lat ~/.hermes/cron/output/<job-id>/ | head -5
cat <latest-log> | grep -i "junk-pattern\|folder\|backup\|metadata" | head -20

# Check backup log file (nếu job có backup log riêng)
ls -lat ~/.hermes/backups/ 2>/dev/null | head -10
grep -h "junk-pattern\|not found\|fallback" ~/.hermes/backups/*.log 2>/dev/null | tail -10
```

Tìm message kiểu:
- "Repo X not found — logging locally"
- "Skipping push, fallback to local"
- "Created folder <path>" with timestamp matching folder mtime

### Step 5: PRESENT 3 OPTIONS, đợi user pick
**KHÔNG tự ý xoá cron.** User phải quyết định:
- **A. Pause cron** (`hermes cron pause <id>`) — recommended khi folder rác, không cần job nữa
- **B. Sửa job** — patch prompt để fail-fast khi thiếu dependency (GitHub repo, network, etc.)
- **C. Xoá job** (`hermes cron remove <id>`) — khi biết chắc không cần nữa

Cộng thêm option:
- **D. Fix dependency** — tạo GitHub repo còn thiếu, sau đó unpause

### Step 6: Verify fix landed
```bash
# Nếu pause:
hermes cron list | grep <job-id>
# expect "Schedule: paused" hoặc job không trigger

# Nếu sửa prompt: verify file change
hermes cron list | grep -A5 <job-id> | head -10

# Watch 1-2 ngày xem folder có re-appear không
ls <path-of-junk> 2>/dev/null && echo "STILL THERE" || echo "CLEAN"
```

## Pitfalls

### P1. Grep toàn disk = timeout (đã gặp 06-30)
**Anti-pattern:** `grep -rli "backup" ~/.hermes/` → timeout 180s vì scan 70K+ files.
**Fix:** Scope hẹp:
```bash
# ❌ Chậm
grep -rli "backup" ~/.hermes/ 2>/dev/null

# ✅ Nhanh — scope hẹp từng layer
hermes cron list                              # 5s
crontab -l                                    # 1s
ls ~/Library/LaunchAgents/                    # 1s
ls ~/.hermes/scripts/*.sh | head -20           # 1s
```

### P2. Đoán folder nặng sai (đã gặp 06-30)
Tôi từng đoán `~/hermes-agent-self-learning` (67MB) là folder rác hôm nay. Sai. Folder thật là `~/.hermes/content-creator-meta-*` chỉ ~8KB, không phải nặng.

**Fix:** ĐỪNG đoán từ size. ĐỢI user confirm cụ thể:
- Path của folder
- Tần suất xuất hiện (mỗi ngày, mỗi giờ, random?)
- Có pattern naming? (date, hash, UUID)

User hint = PRIMARY source. Của anh hôm nay: "check cron xem có cron nào làm việc đó không!" → ưu tiên cron.

### P3. Cron truth = source of truth (H38 lesson)
**Anti-pattern:** tin vào filesystem mtime → có thể stale, file đã touch mà không có new activity.
**Fix:** `hermes cron list` luôn cho ra ground truth. Cross-check với `~/.hermes/cron/output/<job-id>/` mtime (xem `multi-agent-heartbeat` H38 pitfall).

### P4. Job không có "show" subcommand — phải đọc jobs.json trực tiếp
`hermes cron show` KHÔNG tồn tại (verified 06-30). Workaround:
```bash
python3 -c "import json; print(json.dumps(json.load(open('~/.hermes/cron/jobs.json')), indent=2))" | less
```
Hoặc `cronjob` tool (skill `hermes-cron-management`) có actions đầy đủ hơn.

### P5. Folder rác có thể CHỨA data quan trọng
KHÔNG xoá blind. Folder tên "backup" / "snapshot" / "metadata" có thể có:
- Git commit history (ngày quan trọng)
- Snapshot quan trọng (recovery point)
- Last-known-good state cho recovery

**Pattern trước khi xoá:**
1. Check folder size (`du -sh`)
2. Spot-check 1-2 file nội dung
3. Nếu chỉ là metadata (~few KB) → OK xoá
4. Nếu là backup thật (>10MB) → HỎI user trước

### P6. Bug ở PROMPT, không phải ở cron engine
Khi tìm ra cron tạo folder rác, root cause thường là PROMPT của cron job chứ không phải cron engine. Ví dụ:
- Prompt không check target repo có tồn tại không
- Prompt không fail-fast khi dependency missing
- Prompt fallback graceful nhưng fallback path tạo rác

**Fix:** Sửa PROMPT (dùng `hermes cron edit <id>` hoặc `cronjob` tool), không patch cron engine.

### P7. Nhiều job có thể cùng tác nhân
Một job có thể touch nhiều folders. Khi đã tìm được 1 job nghi vấn:
```bash
# Check ALL folders job đó touch
grep -oE '/[\.~][^ ]+' ~/.hermes/cron/output/<job-id>/*.md | sort -u
```
User báo 1 folder, nhưng có thể có 3-4 folders cùng pattern → cần check hết.

## Verification
```bash
# 1. Folder không reappear (đợi 1 cron cycle)
ls <path> 2>/dev/null && echo "STILL THERE" || echo "CLEAN"

# 2. Cron không còn trigger hoặc đã sửa
hermes cron list | grep -A 5 <job-id>

# 3. Output log gần nhất không có new write
ls -lat ~/.hermes/cron/output/<job-id>/ | head -3

# 4. Nếu fixed bằng tạo repo: verify GitHub repo accessible
gh repo view <user>/<repo> 2>&1 | head -3
```

## Related Skills
- `hermes-daily-backup` — Pitfall #0 về "repo missing → silent local logging" (06-30 NEW)
- `hermes-cron-management` — Quản lý cron jobs (pause/resume/remove/edit)
- `multi-agent-heartbeat` — H38 cron-truth vs filesystem mtime
- `self-verify-after-workaround` — Verify fix actually works before reporting done

## Support Files
- (none yet — add nếu xuất hiện case phức tạp hơn)
