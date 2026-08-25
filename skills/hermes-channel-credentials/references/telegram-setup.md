# Telegram Channel Setup — Deep Dive

## Lấy token mới từ @BotFather

1. Mở Telegram, search `@BotFather`
2. Gửi `/mybots` → chọn bot hiện tại (hoặc `/newbot` nếu tạo mới)
3. Chọn "API Token" → @BotFather sẽ gửi token mới (format: `<bot_id>:<46-char-secret>`)
4. Nếu rotate vì token bị leak: `/revoke` → lấy token mới, **token cũ invalid ngay lập tức**

## Cấu hình bắt buộc trong `.env`

```bash
# ~/.hermes/.env (chmod 600)
TELEGRAM_BOT_TOKEN=<id>:<secret>           # từ @BotFather
TELEGRAM_ALLOWED_USERS=<your_user_id>      # OPTIONAL nhưng recommend — lấy từ @userinfobot
TELEGRAM_PROXY=                            # OPTIONAL — socks5:// nếu cần proxy
TELEGRAM_WEBHOOK_URL=                      # OPTIONAL — nếu dùng webhook thay vì long polling
TELEGRAM_HOME_CHANNEL=                     # OPTIONAL — chat ID mặc định cho cron delivery
TELEGRAM_HOME_CHANNEL_NAME=                # OPTIONAL — display name
TELEGRAM_CRON_THREAD_ID=                   # OPTIONAL — forum topic ID cho cron
```

> ⚠️ `TELEGRAM_HOME_CHANNEL`, `TELEGRAM_CRON_THREAD_ID` → xem `hermes-cron-management` để setup cron delivery target riêng.

## Lấy user ID của anh (cho ALLOWED_USERS)

1. Nhắn `@userinfobot` bất kỳ message nào
2. Bot reply với user ID dạng số (vd: `123456789`)
3. Set `TELEGRAM_ALLOWED_USERS=123456789` (hoặc comma-separated nếu nhiều user)

**Nếu để trống** (`TELEGRAM_ALLOWED_USERS=` rỗng) → bot chấp nhận tất cả users, có thể bị abuse.

## Verify token (3 lớp)

### Lớp 1: File permission + length

```bash
ls -la ~/.hermes/.env    # phải là -rw------- (chmod 600)
wc -c ~/.hermes/.env     # token ~46 chars
```

### Lớp 2: Hermes config show

```bash
hermes config show | grep -i telegram
# → "Telegram: configured"
```

### Lớp 3: API call thật

```bash
curl -s https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe
```

Response mong đợi:
```json
{
  "ok": true,
  "result": {
    "id": 1234567890,
    "is_bot": true,
    "first_name": "YourBotName",
    "username": "YourBotHandle",
    "can_join_groups": true,
    "can_read_all_group_messages": true,
    ...
  }
}
```

Nếu `ok: false` → check error code:
- `401 Unauthorized` → token sai/expired → lấy token mới từ @BotFather
- `429 Too Many Requests` → rate limit, đợi và retry

## Test end-to-end

Sau khi restart gateway, test bằng cách nhắn `/start` cho bot trong Telegram. Nếu bot reply → setup thành công.

## Group vs Private chat

- **Private chat**: bot hoạt động ngay khi user nhắn `/start`
- **Group chat**: cần add bot vào group + set `require_mention: false` trong config.yaml nếu muốn bot reply mọi message, hoặc `true` nếu chỉ reply khi @mention
- Bot cần permission `can_read_all_group_messages: true` (mặc định từ @BotFather khi tạo) để đọc @mention trong group

## Forum topic mode (nâng cao)

Nếu group dùng Topics:
- Set `TELEGRAM_HOME_CHANNEL` = group ID (vd: `-100xxxxxxxxxx`)
- Set `TELEGRAM_CRON_THREAD_ID` = topic ID cụ thể cho cron delivery
- Cần `has_topics_enabled: true` trong bot capabilities (default với supergroup)

## Webhook mode (alternative to long polling)

Mặc định Hermes dùng long polling. Nếu cần webhook:
1. Set `TELEGRAM_WEBHOOK_URL=https://your-domain.com/telegram`
2. Cần HTTPS + cert valid
3. Restart gateway — Hermes sẽ tự register webhook với Telegram

→ Long polling đơn giản hơn cho single-user bot. Webhook cần thiết nếu scale > 1 process hoặc cần response < 100ms.

## Common issues

| Issue | Nguyên nhân | Fix |
|---|---|---|
| Bot không reply khi nhắn | Gateway chưa restart sau khi set token | `~/.hermes/restart_gateway.sh` |
| Token set nhưng `config show` vẫn "not configured" | Env var không được source vào shell | Source `.env` trước: `set -a; source ~/.hermes/.env; set +a` |
| `401 Unauthorized` khi gọi API | Token sai/revoked | Lấy token mới từ @BotFather, `/revoke` token cũ |
| Bot join group nhưng không thấy message | `can_read_all_group_messages: false` | Privacy mode ON → disable trong @BotFather: `/setprivacy → Disable` |
| Tin nhắn bị drop silently | Token bị duplicate ở 2 gateway processes | Kill duplicates — xem `gateway-manager` skill |

## Rotation checklist (khi token bị leak hoặc rotate định kỳ)

```
[ ] 1. /revoke token cũ trong @BotFather (token cũ invalid NGAY)
[ ] 2. Lấy token mới
[ ] 3. Ghi vào ~/.hermes/.env (dùng execute_code, KHÔNG echo)
[ ] 4. chmod 600, verify length
[ ] 5. curl /getMe → ok: true
[ ] 6. Restart gateway (~/.hermes/restart_gateway.sh)
[ ] 7. Test /start trong Telegram
[ ] 8. Nếu webhook mode → re-register webhook (Hermes tự làm khi restart)
[ ] 9. Audit: check token cũ KHÔNG còn trong log/backup/git history
```