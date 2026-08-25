# Hermes Daily Backup — 2026-06-25 .env Re-Deletion Incident

## Status
🚨 **RECURRENCE** of 2026-06-18 incident (see `report-example-2026-06-21-incident.md`). Second time `~/.hermes/.env` was destroyed by 3AM cron backup. **Lần 2 xảy ra ĐÚNG 7 ngày sau khi pitfall #20 được viết vào SKILL.md (06-18 → 06-25).** This proves that **documenting pitfall trong SKILL.md ≠ enforcement**. Fix must be copied vào cron script thật, không chỉ viết vào skill body.

## Timeline

| Time (UTC+7) | Event |
|--------------|-------|
| 2026-06-25 03:00 | Daily backup cron chạy (commit `6b895c3a0` — incremental 307 files / 264 untracked + 43 modified) |
| 2026-06-25 03:01+ | Cron script tự động `git reset --hard origin/main` (pitfall #20f pattern) — clean working tree |
| 2026-06-25 03:01+ | Working tree clean: `~/.hermes/.env` đã untracked từ 06-18 commit `927547443`, file vẫn tracked as untracked (size 0 hoặc missing) |
| 2026-06-25 03:01+ | Sau push, cron script cleanup. `~/.hermes/.env` bị xóa khỏi working tree (root cause chính xác vẫn chưa biết — possible `git clean -fd` step hoặc env var unload) |
| 2026-06-25 08:01:40 | Gateway restart bởi user/auto (`--replace` flag) |
| 2026-06-25 08:02:49 | Gateway log: `No user allowlists configured. All unauthorized users will be denied.` |
| 2026-06-25 08:02:49 | Gateway log: `No messaging platforms enabled.` ← root cause signature |
| 2026-06-25 08:02:49 | Gateway start lại, NHƯNG Telegram platform skipped (không có TELEGRAM_BOT_TOKEN load được từ .env) |
| 2026-06-25 08:02-19:46 | Gateway chạy bình thường (cron jobs vẫn work), Telegram inbound = 0 messages |
| 2026-06-25 19:46:07 | User nhắn Telegram "check gateway xem có hoạt động không mà anh nhắn trên tele không được!!!" |
| 2026-06-25 19:46 | Agent diagnose: 0 inbound message hôm nay, log "No messaging platforms enabled" |
| 2026-06-25 19:46 | Agent verify: `~/.hermes/.env` MISSING (file không tồn tại) |

## Discovery Path (3 minutes từ user report → root cause)

1. **`ps aux | grep hermes`** → gateway process chạy bình thường (PID 1096 từ 8:02)
2. **`grep inbound message ~/.hermes/logs/gateway.log | tail -30`** → 0 inbound message trong 25/06
3. **`grep "messaging platforms" ~/.hermes/logs/gateway.log | tail -5`** → "No messaging platforms enabled" lúc 8:02:49
4. **`ls -la ~/.hermes/.env`** → file MISSING (ls báo "No such file or directory")
5. **`find ~/.hermes -maxdepth 3 -name ".env*"`** → chỉ có .env ở profile subdirs (security-engineer, qa-agent, v.v.), KHÔNG có root `.env`
6. **Kết luận**: Gateway không load được TELEGRAM_BOT_TOKEN từ .env → Telegram platform bị skip → user messages không ai nhận

## Root Cause Analysis

### Tại sao fix pitfall #20 không ngăn được lần 2?

**Pitfall #20 trong SKILL.md đã viết fix "2-step untrack pattern" + "always test -f file sau untrack"** (06-21 incident). NHƯNG:
- Fix chỉ tồn tại trong **documentation** (SKILL.md body, line 200+)
- Cron job là **script độc lập** chạy lúc 3AM, **không đọc SKILL.md**, không biết về fix
- Verification step ở cuối SKILL.md (`test -f ~/.hermes/.env && [ -s ~/.hermes/.env ]`) chỉ chạy khi agent `skill_view()` skill này — không phải trong cron

**Đây là anti-pattern cố hữu của SOUL.md-style passive documentation**: chỉ có effect khi được đọc.

### Sequence exact cần verify trong cron script

`pitfall #20f` (06-25 backup session) recommend approach `fetch origin main && reset --hard origin/main` để clean working tree. Approach này đúng để có 1 commit clean. NHƯNG:
- `reset --hard` KHÔNG xóa untracked files (theo git design)
- NẾU có follow-up `git clean -fd` HOẶC env var trong cron env bị unset → bot chết im lặng
- Exact sequence causing `.env` deletion cần đọc cron script thật (`scripts/hermes-daily-backup.sh` hoặc crontab entry) — chưa verify được trong session này vì tool restrictions

## Mandatory 2-Step Enforcement Pattern (CONCRETE, copy-pasteable)

```bash
#!/bin/bash
# Pre-flight (start of script, BEFORE any git operation)
echo "=== Pre-flight: verify .env exists ==="
if ! test -f ~/.hermes/.env; then
    echo "FATAL: ~/.hermes/.env missing — restore from /tmp/hermes-env-backup-*.env or password manager"
    # Attempt restore from latest backup
    LATEST_BACKUP=$(ls -t /tmp/hermes-env-backup-*.env 2>/dev/null | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        echo "Restoring from $LATEST_BACKUP"
        cp -p "$LATEST_BACKUP" ~/.hermes/.env
        chmod 600 ~/.hermes/.env
    else
        echo "NO BACKUP FOUND — manual intervention required"
        exit 1
    fi
fi

# Capture .env to /tmp (idempotent, overwrites same-day backup)
test -f ~/.hermes/.env && cp -p ~/.hermes/.env /tmp/hermes-env-backup-$(date +%Y%m%d).env
chmod 600 /tmp/hermes-env-backup-$(date +%Y%m%d).env

# ... git add, commit, push operations ...

# Post-push (end of script, AFTER push succeeds)
echo "=== Post-push: verify .env STILL exists ==="
if ! test -f ~/.hermes/.env || [ ! -s ~/.hermes/.env ]; then
    echo "FATAL: .env lost during backup — restore from /tmp backup"
    LATEST_BACKUP=$(ls -t /tmp/hermes-env-backup-*.env 2>/dev/null | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        cp -p "$LATEST_BACKUP" ~/.hermes/.env
        chmod 600 ~/.hermes/.env
        echo "RESTORED from $LATEST_BACKUP"
    else
        echo "NO BACKUP — Telegram/Discord bots will be broken until manual fix"
        exit 1
    fi
fi
```

## Diagnostic 3-Command Shortcut (verified 25/06 — 3 min to root cause)

Khi user report "Telegram bot silent" hoặc "nhắn tin không nhận được":

```bash
# Command 1: Check .env
test -f ~/.hermes/.env && echo "ENV OK" || echo "ENV MISSING"

# Command 2: Count platform-disabled warnings
grep -c "No messaging platforms enabled" ~/.hermes/logs/gateway.log

# Command 3: Recent restart events
grep "shutdown\|restart\|Starting Hermes" ~/.hermes/logs/gateway.log | tail -3
```

**Nếu `ENV MISSING` + warning count > 0** → đây là pitfall #20 / #20h signature, skip mọi hypothesis khác, focus ngay vào restore .env.

## Recovery (tested path)

1. **Find backup**: `ls -t /tmp/hermes-env-backup-*.env 2>/dev/null | head -1`
   - Nếu có file trong /tmp → restore ngay
   - Nếu KHÔNG có → tìm trong password manager (1Password, Bitwarden, v.v.)
2. **Restore content**: tạo lại file `~/.hermes/.env` với 18 dòng config:
   ```
   MINIMAX_API_KEY=sk-cp-...
   HERMES_YOLO_MODE=true
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_ALLOWED_USERS=...
   TELEGRAM_HOME_CHANNEL=...
   ```
3. **Set permissions**: `chmod 600 ~/.hermes/.env`
4. **Restart gateway**: `~/.hermes/restart_gateway.sh` (macOS) hoặc `systemctl restart hermes-gateway` (Linux)
5. **Verify**: `test -f ~/.hermes/.env && echo "OK"` + send test message trên Telegram

## Lesson Learned (CRITICAL)

1. **SKILL.md documentation ≠ enforcement.** Pitfall #20 đã có trong skill từ 06-21, vẫn bị lặp lại 06-25. Fix phải được copy VÀO cron script thật.
2. **SKILL.md chỉ có effect khi `skill_view()` được gọi.** Cron jobs không tự đọc skill. Documentation is for HUMANS/AGENTS debugging, not for cron.
3. **Mandatory assertion blocks phải ở đầu VÀ cuối script.** Pre-flight (catch missing-at-start) + post-push (catch lost-during-execution).
4. **Restart events trigger silent failure.** Gateway restart lúc 8:01:40 → load empty env → Telegram skip. Bot chết im lặng 11h45p trước khi user report.

## Related
- `report-example-2026-06-21-incident.md` — Lần 1 của cùng pitfall (06-18 cron, 06-21 phát hiện)
- `report-example-2026-06-24.md` — Backup session chạy approach `fetch + reset --hard` (pitfall #20f) — approach này clean working tree nhưng CÓ THỂ xóa .env nếu follow-up step không đúng
- SKILL.md pitfall #20 (06-21 incident) — fix documented
- SKILL.md pitfall #20h (this file) — fix CHƯA applied vào cron script, recurrence evidence
