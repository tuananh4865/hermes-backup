# Telegram Target Discovery — Cách tìm đúng `telegram:<chat>:<thread>`

> Pattern từ Content Creator cron setup (2026-05-02).
> Use khi cần update cron delivery target mà không chắc chat_id/thread_id.

---

## Source of Truth: HERMES_SESSION_KEY

Khi đang trong session, biến môi trường `HERMES_SESSION_KEY` cho biết chính xác thread hiện tại.

```bash
echo "$HERMES_SESSION_KEY"
# Output: agent:main:telegram:group:-1003764041476:604
#                          ^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^
#                          |       chat_id:thread_id
```

**Parse:**
- Format: `agent:main:telegram:group:<chat_id>:<thread_id>`
- `chat_id` thường bắt đầu bằng `-100` (supergroup)
- `thread_id` là số topic (VD: 604)

→ Target string: `telegram:-1003764041476:604`

---

## Fallback: `send_message action='list'`

Khi KHÔNG có session key (chạy script, background task), dùng:

```
send_message action='list'
```

Output format:
```
Telegram:
  telegram:Tuấn Anh (dm)
  telegram:O-Lab (group)
  telegram:O-Lab / topic 603 (group)
  telegram:O-Lab / topic 604 (group)        ← cái này
  ...
```

Copy **CHÍNH XÁC** string trong ngoặc tròn (không bao gồm `telegram:` prefix nếu tool tự thêm).

---

## Format Reference

| Format | Ý nghĩa |
|--------|---------|
| `telegram:<chat_id>:<thread_id>` | Explicit group/topic |
| `telegram:<chat_id>` | Main group chat, không có topic |
| `telegram:<user_id>` | DM với user |
| `origin` | Topic nơi user đang active khi job fires (sticky!) |
| `local` | Save only, không gửi (cho no_agent scripts) |
| `all` | Fan out tất cả channels |

---

## Pitfalls

### 1. Old messages ≠ current thread
Nếu user nói "gửi về topic 604" mà session history có thread 118389 — KHÔNG dùng 118389. Parse từ session key hiện tại.

### 2. `origin` is sticky
Nếu job tạo khi user ở topic A, sau đó user chuyển sang topic B, `origin` vẫn gửi về A. → Dùng explicit `telegram:<chat>:<thread>` thay vì `origin` cho fleet jobs.

### 3. Topic có thể bị xóa
Nếu user xóa topic → cron delivery fail silently. Verify topic còn tồn tại trước khi set làm target dài hạn.

### 4. Personal chat vs group
Personal chat KHÔNG có thread_id. Format đúng là `telegram:<user_id>` (không có `:thread`).

### 5. Format chính xác
- ✅ `telegram:-1003764041476:604`
- ❌ `telegram: -1003764041476 : 604` (có space)
- ❌ `telegram:-1003764041476/604` (dấu /)
- ❌ `telegram://-1003764041476:604` (có //)

---

## Quick Script — Auto-detect từ session

Nếu cần script tự detect:

```bash
SESSION="$HERMES_SESSION_KEY"
# Parse: agent:main:telegram:group:<chat_id>:<thread_id>
TARGET=$(echo "$SESSION" | sed -E 's/^agent:[^:]+:telegram:(group|channel):(-[0-9]+):([0-9]+)$/telegram:\2:\3/')
echo "Detected: $TARGET"
```

Test:
- `agent:main:telegram:group:-1003764041476:604` → `telegram:-1003764041476:604` ✅
- `agent:main:telegram:user:1132914873` → `telegram:1132914873` (DM, no thread)
