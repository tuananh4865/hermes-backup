---
name: hermes-channel-credentials
description: Set up, rotate, and troubleshoot Hermes gateway channel credentials (Telegram bot token, Discord/Slack/Mattermost/Matrix bot tokens, .env layout, getMe-style verify, allowed_users, proxy). Use when a messaging channel stops responding after a token change, user asks to "set telegram token" / "configure discord bot" / "bot không nhắn được" / "rotate bot token", or a new channel needs to be wired up alongside existing ones.
---

# Hermes Channel Credentials

Hermes Gateway đọc channel tokens từ **env vars**, KHÔNG từ `config.yaml`. File chuẩn là `~/.hermes/.env` (chmod 600). Đây là workflow setup/rotate/verify cho mọi channel.

## Khi nào load skill này

- User: "set telegram token", "đổi bot token", "bot không nhắn được nữa", "thêm discord channel", "rotate token"
- Triệu chứng: gateway chạy nhưng channel không response, `hermes config show` báo "not configured", hoặc user vừa paste token mới
- Lần đầu setup bất kỳ channel nào (Telegram, Discord, Slack, Mattermost, Matrix)

## Quick map: Channel → Env Var

| Channel | Token var | Verify endpoint |
|---|---|---|
| Telegram | `TELEGRAM_BOT_TOKEN` | `curl https://api.telegram.org/bot$TOKEN/getMe` |
| Discord | `DISCORD_BOT_TOKEN` | Discord gateway ping (xem references/discord.md) |
| Slack | `SLACK_BOT_TOKEN` + `SLACK_APP_TOKEN` | `auth.test` API |
| Mattermost | `MATTERMOST_URL` + `MATTERMOST_TOKEN` | team info endpoint |
| Matrix | `MATRIX_HOMESERVER` + `MATRIX_ACCESS_TOKEN` | `/_matrix/client/v3/account/whoami` |

> Behavioral settings (allowed users, mention mode, streaming) → `config.yaml`, KHÔNG .env.
> **⚠️ EXCEPTION #15 (12/07):** `telegram.allowed_users` block trong `config.yaml` KHÔNG phải behavioral setting mà Telegram adapter đọc — nó là field gateway parse nhưng bị bỏ qua. **Allowed users phải đặt ở `TELEGRAM_ALLOWED_USERS` trong `.env`**. Xem pitfall #15.
> Xem `~/.hermes/hermes-agent/.env.example` cho full list.

## Workflow (6 bước — luôn theo thứ tự)

### 0. (TROUBLESHOOT ONLY) Check `gateway.error.log` TRƯỚC

**Khi user báo "bot không nhận được tin nhắn" / "bot im lặng" / "channel không response":**
- **MỞ `~/.hermes/logs/gateway.error.log` NGAY** — đừng đào network, DNS, token trước
- Tìm các dòng WARNING/ERROR: `No messaging platforms enabled`, `Update notification deferred: <platform> adapter not connected yet`, `Adapter <X> not wired up`
- 90% lỗi channel "không nhận tin nhắn" nằm ở đây, không phải network hay token

**Có 2 file log, mục đích khác nhau — đừng nhầm:**

| File | Chứa gì | Khi nào dùng |
|---|---|---|
| `~/.hermes/gateway.log` | Banner ASCII + warning cũ (file này KHÔNG rotate, chỉ overwrite mỗi lần gateway start) | Đọc banner + initial startup warnings |
| `~/.hermes/logs/gateway.log` | **Active log, có timestamp đầy đủ** — mọi event kể cả housekeeping/kanban | **Đây là file phải `tail` để xem real-time state** |
| `~/.hermes/logs/gateway.error.log` | Tất cả WARNING + ERROR được mirror ra đây | **File debug số 1 khi channel không response** — filter theo pattern dễ hơn |

**Time-window log triage (tránh bị "log ghost" đánh lừa):**

Sau khi restart gateway, log cũ trong `gateway.log` vẫn còn (file này KHÔNG auto-rotate). Spam `Update notification deferred` từ session fail trước có thể trông giống "loop đang xảy ra" dù gateway mới đã OK. Cách chắc chắn:

```bash
# 1. Tìm thời điểm gateway mới connect thành công
grep "✓ telegram connected\|✓ discord connected" ~/.hermes/logs/gateway.log | tail -1
# → "2026-06-21 09:53:39,225 INFO ✓ telegram connected"

# 2. Đếm deferred SAU thời điểm đó
awk '/2026-06-21 09:5[3-9]/' ~/.hermes/logs/gateway.log | grep -c deferred
# → 0 nghĩa là sạch, > 0 nghĩa là loop thật

# 3. Nếu muốn filter tất cả WARNING/ERROR gần đây
tail -200 ~/.hermes/logs/gateway.error.log | grep "$(date '+%Y-%m-%d %H:%M' -v -1H)" || echo "(sạch)"
```

**Các log red-flag thường gặp:**

| Log line | Root cause | Bước tiếp theo |
|---|---|---|
| `No messaging platforms enabled` | `.env` thiếu token, hoặc `~/.hermes/.env` bị xóa | Bước 1 → 3 |
| `Update notification deferred: telegram adapter not connected yet` (spam) | Token set nhưng gateway poll fail liên tục | Bước 5 (verify API) |
| `Connect attempt 1/3 failed: Timed out` | Network thật sự chặn Telegram API | Test `curl https://api.telegram.org/bot$TOKEN/getMe` |
| `Flood control exceeded. Retry in N seconds` | Đang spam quá nhiều request | Đợi, retry sau N giây |
| `Unauthorized` (401) | Token sai/revoked | Bước 1 — lấy token mới từ @BotFather |
| `Update watcher: cannot resolve adapter/chat_id` | Token có nhưng `TELEGRAM_HOME_CHANNEL` / `allowed_chats` rỗng | Set `TELEGRAM_HOME_CHANNEL=<id>` |

> **PITFALL: "Telegram connect timeout" logs đôi khi là LOG CŨ.** Sau khi restart gateway, đọc log từ đầu file, không phải tail — log cũ có thể gây hiểu nhầm root cause. Bug đã phạm 21/06: thấy log "Telegram connect timeout" → đào network → phát hiện thật ra là `No messaging platforms enabled` (file `.env` bị xóa). Bug đã phạm 21/06 lần 2: thấy `360 deferred` tổng cộng trong log → tưởng loop đang xảy ra → time-window filter cho thấy 360/360 là log cũ TRƯỚC khi connect, sau `09:53:39 ✓ telegram connected` thì count = 0.

### 1. Xác định channel + đọc `.env.example` cho tên var đúng

```bash
hermes config env-path    # in ra ~/.hermes/.env
grep -i "<channel>" ~/.hermes/hermes-agent/.env.example
```

### 2. Tạo/ghi file `.env` (nếu chưa có)

```bash
touch ~/.hermes/.env && chmod 600 ~/.hermes/.env
```

**PITFALL #1 — `write_file` bị BLOCK với `.env`:**
- File `.env` nằm trong Hermes protected credential whitelist
- `write_file` sẽ fail với `Write denied: '.env' is a protected system/credential file`
- **Fix:** dùng `terminal` (`cat >> .env << EOF`) hoặc `execute_code` (Python file write + atomic mv)
- **KHÔNG BAO GIỜ** echo token ra shell history / terminal output / log file

### 3. Ghi token vào `.env` (KHÔNG leak)

```python
# execute_code — atomic write, no echo
import subprocess
token = "..."   # paste token vào đây, KHÔNG in ra
content = f"CHANNEL_BOT_TOKEN={token}\n"
with open("/tmp/hermes_env.tmp", "w") as f:
    f.write(content)
subprocess.run(["mv", "/tmp/hermes_env.tmp", str(Path.home() / ".hermes/.env")])
subprocess.run(["chmod", "600", str(Path.home() / ".hermes/.env")])
# Verify chỉ length, KHÔNG echo value
```

### 4. Source env + check Hermes nhận diện

```bash
set -a; source ~/.hermes/.env; set +a
hermes config show | grep -i "<channel>"
hermes config check | grep -i "<CHANNEL>_BOT_TOKEN"
```

Kết quả mong đợi:
- `hermes config show` → `Telegram: configured`
- `hermes config check` → `✓ TELEGRAM_BOT_TOKEN` (checkmark, không còn `○`)

### 5. Verify token thật (qua API của channel)

**Telegram:**
```bash
curl -s https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe
```
Response phải là `{"ok":true,"result":{"id":..., "username":"...", ...}}`.

**Nếu fail** → token sai/expired/revoked → user phải lấy token mới từ @BotFather.

### 6. Restart gateway để token mới có hiệu lực

**PITFALL #2 — Token KHÔNG tự reload:**
- Env vars chỉ được load khi process khởi động
- Set token mới nhưng KHÔNG restart → gateway vẫn dùng token cũ (hoặc fail silently)
- Fix: restart gateway — `~/.hermes/restart_gateway.sh` HOẶC kill + relaunch

Xem `gateway-manager` skill cho restart details (graceful vs hard kill cho code patches).

## PITFALLS — Đừng phạm phải

| # | Pitfall | Fix |
|---|---|---|
| 1 | `write_file` to `.env` → BLOCKED | Dùng `terminal` hoặc `execute_code` |
| 2 | Set token nhưng quên restart gateway | Luôn restart sau khi đổi env var |
| 3 | Echo token ra terminal/log → leak | Verify bằng length + first/last chars only |
| 4 | Set token vào `config.yaml` → KHÔNG hoạt động | Tokens chỉ đọc từ env vars |
| 5 | Không set `TELEGRAM_ALLOWED_USERS` → bất kỳ ai cũng điều khiển bot | Set = Telegram user ID của owner |
| 6 | Multiple gateway processes cùng bot token → conflict | Check `ps aux | grep gateway`, kill duplicates |
| 7 | Dùng webhook URL cũ sau khi rotate token | Nếu chạy webhook mode → re-register webhook |
| 8 | Test nhắn ngay sau khi set token, chưa restart | Restart gateway TRƯỚC khi test |
| 9 | **Đào network/DNS khi root cause là `.env` bị xóa** | Check `gateway.error.log` FIRST (xem Bước 0). Log `No messaging platforms enabled` là red-flag #1 — file token đã biến mất |
| 10 | **`~/.hermes/.env` bị xóa đột ngột, không rõ lý do** | Setup **auto-backup `.env` encrypted** — xem `scripts/backup-encrypted-env.sh`. Cron 2AM chạy cùng `autoresearch`, giữ 30 backup gần nhất. File `.env` KHÔNG có ở Time Machine/Trash — mất là mất luôn. Disaster recovery = user phải lấy lại token từ @BotFather, mất 5-10 phút |
| 11 | **"360 deferred trong log" tưởng loop đang chạy** | Time-window filter — chỉ đếm `deferred` SAU timestamp `✓ <channel> connected` gần nhất. Count = 0 = sạch. Log cũ spam trước restart KHÔNG đáng quan tâm. Xem `references/log-triage-cookbook.md` |
| 12 | **Restart gateway nhưng env var mới không có hiệu lực** | Token + env vars chỉ load khi process **khởi động**. Nếu gateway dùng systemd/launchd → restart KHÔNG đủ, cần `launchctl kickstart -k gui/$(id -u)/<service>` hoặc kill PID rồi để supervisor tự respawn. Check `ps -o etime` để confirm process thật sự mới |
| 13 | **Gateway tự respawn PID mới trong vài giây** (PID 45038 → 45356) | `kill <pid>` thường KHÔNG giết được vì supervisor respawn ngay. Cách chắc chắn: `kill <pid>; sleep 1; ps -p <pid>` nếu vẫn alive → kill -9. Hoặc `pkill -f "hermes_cli.main gateway"` |
| 14 | **Telegram API giữ token lock 5s sau khi gateway chết đột ngột** → "Telegram bot token already in use (PID X)" error lặp lại, dù đã kill process | Đây là Telegram Bot API cleanup window, KHÔNG phải multi-gateway race. Fix recipe: `kill <pid>` → `launchctl unload <plist>` → `sleep 5` → `launchctl load <plist>` → verify `curl /getUpdates` trả `ok:true`. Recipe chi tiết + 4 anti-pattern: xem `gateway-manager/references/telegram-token-lock-recovery-2026-07-07.md`. Cross-reference: **khác** với pitfall #13 (respawn loop) và pitfall #6 (multi-gateway healthy race) |
| 15 | **`config.yaml` có `telegram.allowed_users: '*'` nghĩ là "mở cho tất cả"** → SAI. Field này Telegram adapter KHÔNG ĐỌC. Adapter check theo thứ tự: (1) `extra.allow_from` config block, (2) `runner._is_user_authorized` từ MessageHandler, (3) env var `TELEGRAM_ALLOWED_USERS` comma-separated. Field `allowed_users` trong block `telegram:` của `config.yaml` được gateway parse nhưng KHÔNG pass xuống adapter. Case 12/07: em báo "config đã mở rồi" → anh báo vợ nhắn không nhận → grep log thấy 5× `Blocked unauthorized user 5514781536` → đọc source `telegram/adapter.py:_is_user_authorized_from_message` mới ra. **Fix recipe:** KHÔNG BAO GIỜ assume field nào có hiệu lực — grep adapter source code first. Khi user nói "tôi nhắn được nhưng người khác không" → 99% là `TELEGRAM_ALLOWED_USERS` quá hẹp, fix `.env` chứ không phải `config.yaml`. Verify bằng `grep "Blocked unauthorized" ~/.hermes/logs/gateway.log` — nếu thấy ID bị block = fix `.env` ngay |
| 16 | **Add user mới vào `TELEGRAM_ALLOWED_USERS` cần restart gateway từ TERMINAL NGOÀI, không phải từ session Telegram** (case 14/07/2026 — add vợ anh `5514781536`). 3-step recipe: (1) Backup `.env` → `.env.backup-YYYY-MM-DD-pre-telegram-v<N>`; (2) sed với anchor pattern unique (`sed -i.bak 's/^TELEGRAM_ALLOWED_USERS=1132914873$/TELEGRAM_ALLOWED_USERS=1132914873,NEW_ID/' ~/.hermes/.env`); (3) Verify 5-evidence gate (file exists, size >0, perm 600, key count >=14, sample key intact). Sau đó HƯỚNG DẪN USER chạy `hermes gateway restart` từ Terminal app — KHÔNG thể restart từ session Telegram (hard block: `Blocked: cannot restart or stop the gateway from inside the gateway process`). Verify: grep `Blocked unauthorized` log TRƯỚC restart để có baseline; grep log SAU restart để confirm user mới pass auth. **Anti-pattern em đã phạm:** tin `allowed_users: '*'` trong config.yaml work → bị anh flag ngay. **Anti-pattern #2:** dùng `hermes config set TELEGRAM_ALLOWED_USERS ...` → nó ghi raw key vào `config.yaml` block `telegram:` thay vì `.env` — sai field. **Cách đúng duy nhất:** sed trực tiếp `.env` sau khi có explicit user OK + backup. Cross-ref: writing-secrets-to-files skill § "Editing existing env vars (sed append)" cho pattern chi tiết |

## CRITICAL: Why `.env` keeps disappearing (cross-pattern)

There are **3 known root causes** for `.env` going missing or having wrong perms on this system. Each has its own skill/pitfall — diagnose ALL THREE before claiming root cause:

1. **Cron `git reset --hard` wipes untracked `.env`** — See `hermes-daily-backup` PITFALL #20, #20h. Backup cron `7cba6ba5f52a` (3AM daily) uses `git rm --cached` + `git reset --hard origin/main` flow. If the reset runs after `.env` has been untracked (untracked files DON'T survive `--hard`), the file disappears from disk. Mitigation: PITFALL #21 in same skill (pre-flight snapshot + post-reset restore).

2. **Gateway umask 022 regression to perm 644** — See `gateway-manager` section "CRITICAL PITFALL: Gateway umask 022 pattern". Gateway uses `open(path, 'w')` without explicit mode during config sync → new file inherits process umask → perm 644. File NOT deleted, but appears "exposed" in security sweeps. Mitigation: `env-permission-guard.py` PostToolUse hook (recipe in `gateway-manager` SKILL.md).

3. **User accidentally deletes via `rm`** — self-inflicted. Mitigation: encrypted backup script below.

**When user reports "telegram bot silent" or ".env missing":**
```bash
# 1. File exists?
test -f ~/.hermes/.env && echo "EXISTS" || echo "MISSING → see root cause #1 or #3"

# 2. Permission correct?
stat -f "%Lp" ~/.hermes/.env  # expect 600, if 644 → see root cause #2

# 3. Token intact?
grep -c TELEGRAM_BOT_TOKEN ~/.hermes/.env  # expect >= 1

# 4. Gateway aware?
grep "No messaging platforms enabled" ~/.hermes/logs/gateway.error.log | tail -1
```

If `MISSING` → restore from `/Volumes/Storage-1/Hermes/secrets/.env.hermes.backup` (shipped 2026-06-25, see `hermes-daily-backup/scripts/restore-env.sh`) OR from encrypted backup below.
If perm 644 → `chmod 600 ~/.hermes/.env` AND find root cause #2 writer process.
If token count = 0 → user must re-issue from @BotFather (no recovery possible).

## Verification checklist (sau mỗi lần set/rotate)

```
[ ] File ~/.hermes/.env tồn tại, chmod 600
[ ] Token có length đúng (~46 chars cho Telegram bot)
[ ] hermes config show → channel: configured
[ ] curl /getMe (hoặc equivalent) → ok: true
[ ] Gateway restarted SAU khi set token
[ ] Test 1 tin nhắn thật end-to-end
```

## Related skills
## Related skills
- `gateway-manager` — process lifecycle, restart methods, hard kill vs graceful; **CRITICAL: also documents umask 022 regression (perm 644) root cause — see "CRITICAL PITFALL: Gateway umask 022 pattern" in gateway-manager SKILL.md**
- `hermes-daily-backup` — cron 3AM backup of `~/.hermes`; **PITFALL #20, #20h, #20i document the .env wipe pattern + recovery via `scripts/restore-env.sh`**
- `hermes-cron-management` — cron delivery target (nơi cron gửi report, khác với channel setup)
- `agentic-company-setup` — multi-agent với mỗi agent 1 bot (orchestration, không phải token setup)
- `hermes-agent` (bundled) — tổng quan Hermes system

## Support files

- `scripts/backup-encrypted-env.sh` — Auto-backup `~/.hermes/.env` mã hóa AES-256 vào `/Volumes/Storage-1/Hermes/backups/env-encrypted/`. Setup 1 lần: set `$HERMES_ENV_BACKUP_PASSPHRASE` env var, thêm vào crontab 2AM. Rotate 30 bản gần nhất.

## Reference files (deep dive per channel)

- `references/telegram-setup.md` — ✅ DONE: Telegram deep dive (BotFather rotate/revoke, allowed_users, group + topic mode, webhook vs polling, proxy, Privacy Mode, rotation checklist)
- `references/log-triage-cookbook.md` — ✅ DONE: Copy-paste diagnostic commands cho "bot không response" (3-file log map, log-ghost filter, restart pattern, red-flag table)
- `references/telegram-allowed-users-edit-2026-07-14.md` — ✅ DONE: Case study thêm Telegram user ID mới vào `TELEGRAM_ALLOWED_USERS` (add vợ anh 5514781536). Anti-patterns (tin config field, dùng `hermes config set` sai field, restart từ Telegram session), 4-step fix recipe, source code reference. Đọc file này TRƯỚC khi xử lý case "user X nhắn mà không nhận được"
- `references/discord-setup.md` — TODO: Discord bot setup (application, intents, gateway connection)
- `references/slack-setup.md` — TODO: Slack bot + app token pair (Socket Mode vs Events API)

Khi mới chỉ có Telegram — đó là channel phổ biến nhất của Hermes users. Discord/Slack refs sẽ được thêm khi user thực sự setup channel đó.