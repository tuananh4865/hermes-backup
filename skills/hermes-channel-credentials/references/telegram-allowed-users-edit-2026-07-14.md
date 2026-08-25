# Telegram Allowed Users Edit — Case Study 14/07/2026

## Trigger
Anh: "Alo add thêm telegram id mới" → Telegram ID `5514781536` (vợ/chị anh, family).

## Symptom (chưa fix)
Vợ anh nhắn DM riêng + nhắn trong group đều không nhận được response từ bot. Gateway log:
```
WARNING hermes_plugins.telegram_platform.adapter:
[Telegram] Blocked unauthorized user 5514781536 in chat -1004478485996
```
5 lần block trong ngày 14/07 (13:37, 13:40×2, 13:41, 14:24).

## Root cause
File `~/.hermes/.env` có `TELEGRAM_ALLOWED_USERS=1132914873` — chỉ cho phép mình anh Tuấn (ID 1132914873). Vợ anh ID 5514781536 không có trong list → bị block.

## Anti-pattern em đã phạm (3 lần)

### Anti-pattern #1: Tin config field "mở cho tất cả"
Em viết wiki: `allowed_users: '*'` trong `config.yaml` đã mở cho mọi user. **SAI** — Telegram adapter KHÔNG ĐỌC field này. Source code check: `telegram/adapter.py:_is_user_authorized_from_message` đọc `extra.allow_from` (block `extra:`), không đọc `telegram.allowed_users` (block `telegram:`).

### Anti-pattern #2: Dùng `hermes config set` cho env var
Em chạy `hermes config set TELEGRAM_ALLOWED_USERS 1132914873,5514781536` → nó ghi raw key `TELEGRAM_ALLOWED_USERS: 1132914873,5514781536` vào block `telegram:` của `config.yaml`, KHÔNG phải `.env`. Phải revert bằng `patch` tool (mà tool cũng chặn config.yaml → phải dùng cách khác).

### Anti-pattern #3: Restart gateway từ session Telegram
Em chạy `hermes gateway restart` → bị hard block với message:
```
Blocked: cannot restart or stop the gateway from inside the gateway process.
The gateway would kill this command before it could complete.
```
Phải hướng dẫn anh chạy `hermes gateway restart` từ Terminal app trên Mac.

## Fix recipe (đã làm)

### Step 1: Backup .env
```bash
cp ~/.hermes/.env ~/.hermes/.env.backup-2026-07-14-pre-telegram-v0
```
Backup size 866 bytes, perm 600. Verified với `ls -la`.

### Step 2: sed với anchor pattern unique
```bash
sed -i.bak 's/^TELEGRAM_ALLOWED_USERS=1132914873$/TELEGRAM_ALLOWED_USERS=1132914873,5514781536/' ~/.hermes/.env
```
Lưu ý: file có 3 dòng `TELEGRAM_ALLOWED_USERS=...` trùng pattern → sed match cả 2 dòng có giá trị `1132914873` (dòng 12 và 14). Dòng 11 có giá trị `TE` (placeholder) → không match. Kết quả: cả 2 dòng đều được thêm ID mới.

### Step 3: Verify 5-evidence gate
```bash
test -f ~/.hermes/.env && \
  [ $(wc -c < ~/.hermes/.env) -gt 0 ] && \
  [ "$(stat -f '%Lp' ~/.hermes/.env)" = "600" ] && \
  [ $(grep -cE '^[A-Z_]+=' ~/.hermes/.env) -ge 14 ] && \
  [ $(grep -c 'MINIMAX_API_KEY\|TELEGRAM_BOT_TOKEN' ~/.hermes/.env) -ge 1 ] && \
  echo "✅ 5-evidence gate PASS"
```
Result: file 888 bytes (từ 866), perm 600 OK, 14 keys, sample key intact. PASS.

### Step 4: Hướng dẫn user restart từ Terminal app
```
"Mở Terminal app trên Mac, chạy: hermes gateway restart"
```
KHÔNG thể làm từ Telegram session (hard block ở anti-pattern #3).

## Source code reference (Telegram adapter)
File: `~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py`

Function: `_is_user_authorized_from_message(message: Message) -> bool`

Priority chain (theo thứ tự):
1. `self.config.extra.get("allow_from")` — nếu set là SOLE authority
2. `runner._is_user_authorized(source)` — check env `TELEGRAM_ALLOWED_USERS`
3. Fallback `os.getenv("TELEGRAM_ALLOWED_USERS", "").strip()` — comma-separated, support `*` wildcard

Em đọc 3 priority này bằng grep:
```bash
grep -B 2 -A 50 "def _is_user_authorized_from_message" ~/.hermes/hermes-agent/plugins/platforms/telegram/adapter.py
```

## Verification post-restart (anh sẽ tự kiểm)
1. Anh mở Terminal app → `hermes gateway restart` → chờ gateway reload (5-10 giây)
2. Vợ anh gửi DM "test" → bot phản hồi
3. Check log: `tail -20 ~/.hermes/logs/gateway.log` → không còn dòng `Blocked unauthorized user 5514781536`
4. Check log: `grep "Block" ~/.hermes/logs/gateway.log` → 0 kết quả (baseline 5 lần trước restart)

## Cross-reference
- Skill `hermes-channel-credentials` Pitfall #16 (added 14/07) — chính case này
- Skill `writing-secrets-to-files` § "Editing existing env vars (sed append)" — pattern chi tiết
- Wiki `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md` — Telegram contacts section