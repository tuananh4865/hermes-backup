# Channel "Bot not responding" — Log Triage Cookbook

**Dùng khi:** User báo "bot không reply", "channel im lặng", "Telegram nhắn không được", "Discord không phản hồi". Mục tiêu: xác định root cause trong < 2 phút, không cần restart gateway vô ích.

**Triết lý:** 90% lỗi "channel không response" nằm trong `gateway.error.log` — KHÔNG phải network, DNS, hay token. Đào log trước, đào network sau.

---

## 3 file log, mục đích khác nhau

| File | Dùng cho | Đặc điểm |
|---|---|---|
| `~/.hermes/gateway.log` | Banner + initial startup warnings | File nhỏ (~1KB), KHÔNG rotate, chỉ ghi đè mỗi restart |
| `~/.hermes/logs/gateway.log` | **Active log, có timestamp** — đây là file phải `tail` | File lớn (1-3MB), timestamp `YYYY-MM-DD HH:MM:SS,ms`, đầy đủ event |
| `~/.hermes/logs/gateway.error.log` | **WARNING + ERROR mirror** | Filter dễ hơn, đây là file debug số 1 |

> **BẪY phổ biến:** `tail -50 ~/.hermes/gateway.log` thường trả về log CŨ từ session fail trước (vì file này không rotate). Spam `Update notification deferred` trong đó có thể trông giống "loop đang chạy" dù gateway hiện tại đã OK.

---

## Triage script (copy-paste, chạy trong ~5 giây)

```bash
echo "=== 1. Gateway alive? ==="
pgrep -fl "hermes_cli.main gateway" | head -3

echo ""
echo "=== 2. Process uptime (nếu > 5 phút = stable) ==="
ps -o pid,etime,command -p $(pgrep -f "hermes_cli.main gateway" | head -1)

echo ""
echo "=== 3. Token configured? ==="
test -f ~/.hermes/.env && echo "✓ .env exists ($(stat -f%z ~/.hermes/.env) bytes)" || echo "✗ .env MISSING"
test "$(stat -f%Sa ~/.hermes/.env 2>/dev/null)" = "" || echo "  Last modified: $(stat -f%Sm ~/.hermes/.env)"

echo ""
echo "=== 4. Platform wired up? (Tìm trong error log) ==="
grep -E "No messaging platforms enabled|✓ telegram connected|✓ discord connected" \
  ~/.hermes/logs/gateway.log | tail -3

echo ""
echo "=== 5. Đếm deferred SAU connect thành công (log ghost filter) ==="
LAST_CONNECT=$(grep "✓ telegram connected\|✓ discord connected" \
  ~/.hermes/logs/gateway.log | tail -1 | awk '{print $1, $2}')
if [ -n "$LAST_CONNECT" ]; then
  # Lấy ngày + giờ từ LAST_CONNECT, filter log sau đó
  DAY=$(echo $LAST_CONNECT | cut -d' ' -f1)
  HOUR=$(echo $LAST_CONNECT | cut -d' ' -f2 | cut -d: -f1)
  COUNT=$(awk -v d="$DAY" -v h="$HOUR" \
    '$0 ~ d && $2 ~ "^" h ":" {print}' \
    ~/.hermes/logs/gateway.log | grep -c deferred)
  echo "  Last connect: $LAST_CONNECT"
  echo "  Deferred trong cùng giờ: $COUNT (0 = sạch)"
else
  echo "  ✗ Gateway CHƯA từng connect thành công → token/network issue"
fi

echo ""
echo "=== 6. Token valid? (gọi API thật) ==="
set -a; source ~/.hermes/.env; set +a
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
  RESULT=$(curl -s -m 5 "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe")
  echo "$RESULT" | python3 -c "
import json, sys
d = json.load(sys.stdin)
if d.get('ok'):
    r = d['result']
    print(f'  ✓ Token valid: @{r[\"username\"]} (ID {r[\"id\"]})')
else:
    print(f'  ✗ Token INVALID: {d.get(\"description\", d)}')
" 2>/dev/null || echo "  ✗ API call failed"
else
  echo "  ✗ TELEGRAM_BOT_TOKEN chưa set"
fi
```

**Output mẫu (sau khi fix xong):**
```
=== 1. Gateway alive? ===
45356 /Users/.../hermes_cli.main gateway run --replace
=== 2. Process uptime (nếu > 5 phút = stable) ===
  PID ELAPSED COMMAND
45356 01:11 ...
=== 3. Token configured? ===
✓ .env exists (754 bytes)
=== 4. Platform wired up? ===
... ✓ telegram connected
=== 5. Đếm deferred SAU connect thành công (log ghost filter) ===
  Last connect: 2026-06-21 09:53:39
  Deferred trong cùng giờ: 0 (0 = sạch)
=== 6. Token valid? ===
  ✓ Token valid: @ClawdZ1E_Bot (ID 8344881558)
```

---

## Red-flag patterns → Root cause → Fix

| Pattern (grep) | Root cause | Next action |
|---|---|---|
| `No messaging platforms enabled` | `~/.hermes/.env` bị xóa hoặc empty | Tạo lại `.env`, set token, restart gateway |
| `No user allowlists configured` | `TELEGRAM_ALLOWED_USERS` rỗng | Set = Telegram user ID, hoặc `*` cho open access |
| `Update notification deferred: telegram adapter not connected yet` (count > 0 SAU `✓ connected`) | Gateway thật sự đang loop | Check token + network, restart |
| `Connect attempt 1/3 failed: Timed out` | Network chặn `api.telegram.org` | Test `curl -m 5 https://api.telegram.org/bot$TOKEN/getMe` |
| `Flood control exceeded. Retry in N seconds` | Đang spam quá nhiều request | Đợi N giây, retry |
| `Unauthorized` (401) từ `getMe` | Token sai hoặc bị revoke | Lấy token mới từ @BotFather |
| `Update watcher: cannot resolve adapter/chat_id` | `TELEGRAM_HOME_CHANNEL` rỗng | Set `TELEGRAM_HOME_CHANNEL=<id>` |
| `Requested agent harness 'X' is not registered` | Model provider chưa config | Check `~/.hermes/.env` có `MINIMAX_API_KEY` / `OPENAI_API_KEY` |

---

## "Log ghost" — case thật tế ngày 21/06

**Tình huống:** Restart gateway, thấy log spam 360 lần `Update notification deferred`. Agent lần đầu nghĩ "loop đang xảy ra, phải đào tiếp".

**Root cause:** 360/360 deferred đều có timestamp TRƯỚC `09:53:39 ✓ telegram connected`. Chúng là log từ session fail trước (khi `.env` bị xóa), ghi vào `gateway.log` không tự xóa. Sau connect thành công → count = 0.

**Cách phân biệt log ghost vs log thật:**
- Log thật: timestamp SAU dòng `✓ <channel> connected` gần nhất
- Log ghost: timestamp TRƯỚC dòng đó

**Filter command:**
```bash
# Lấy timestamp của lần connect thành công gần nhất
LAST=$(grep "✓ telegram connected" ~/.hermes/logs/gateway.log | tail -1 | awk '{print $1, $2}')

# Đếm deferred SAU thời điểm đó
awk -v ts="$LAST" '$0 > ts' ~/.hermes/logs/gateway.log | grep -c deferred
# → 0 = sạch
```

---

## Khi nào cần restart vs không

| Tình huống | Restart? |
|---|---|
| Đổi token trong `.env` | **CÓ** — env var chỉ load khi process start |
| Đổi `config.yaml` (allowed_users, mention mode) | **CÓ** |
| Channel tự disconnect rồi reconnect | KHÔNG — để gateway tự retry |
| Sửa hook script | Restart hook loader thôi, không cần restart gateway |
| Update Hermes binary | **CÓ** + `hermes update` nếu có |

**Restart pattern an toàn (tránh bị respawn ngay):**
```bash
# 1. Tìm PID hiện tại
PID=$(pgrep -f "hermes_cli.main gateway" | head -1)
echo "Killing PID: $PID"

# 2. Kill
kill $PID
sleep 2

# 3. Check nếu supervisor respawn → kill -9
if ps -p $PID > /dev/null 2>&1; then
  echo "Still alive, force kill"
  kill -9 $PID
fi

# 4. Đợi supervisor tự respawn (3-10s)
sleep 8
NEW_PID=$(pgrep -f "hermes_cli.main gateway" | head -1)
echo "New PID: $NEW_PID (etime: $(ps -o etime= -p $NEW_PID))"
```

---

## Saved session transcript reference

21/06: Session `telegram-bot-khong-nhan-tin-nhan` — diagnosed `.env` bị xóa (root cause: cleanup script hoặc manual rm), restored token, gateway connected, 0 deferred. Triage script ở trên được viết ra từ session này.
