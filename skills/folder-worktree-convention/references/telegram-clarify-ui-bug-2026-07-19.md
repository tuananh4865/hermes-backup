---
title: Telegram `clarify` UI Bug + Hermes-Only Folder Mandate
created: 2026-07-19
type: reference
tags: [pitfall, telegram, clarify-tool, worktree-mandate]
confidence: high
---

# Failure Mode: `clarify` UI Không Render Trên Telegram (19/07)

## Symptom

Khi em gọi `clarify` tool với `choices` array trên channel Telegram, **anh không thấy UI multiple choice xuất hiện**. Phản hồi thực tế từ anh:

> *"3 scope em hỏi anh không thấy xuất hiện? em hỏi lại xem nào"*

## Root Cause

`clarify` tool với `choices` parameter render UI selectable rows **chỉ work trên CLI / web / mobile app có rich UI**. Telegram Bot API chỉ nhận text message thường → `choices` array bị drop silently, user chỉ thấy câu hỏi không có options.

## Verified Evidence (19/07)

- Tool call: `clarify(question="Anh muốn em xử lý 3 folder NGOÀI ...?", choices=["move_all", "symlink_only", "minimal_move", "explain_first"])`
- Response từ anh: `"3 scope em hỏi anh không thấy xuất hiện? em hỏi lại xem nào"`
- Tool return: `{"choices_offered": null, "user_response": "..."}` → xác nhận UI không render

## Fix

Khi channel = Telegram, **KHÔNG dùng `clarify` với `choices`**. Thay bằng inline numbered text list:

```markdown
**Anh muốn em xử lý X sao?**

1. Option A — mô tả ngắn
2. Option B — mô tả ngắn
3. Option C — mô tả ngắn
4. Option D — em recommend + lý do

Anh gõ A/B/C/D hoặc nói rõ ý em làm
```

Alternatives OK trên Telegram:
- **Open-ended question** (omit `choices` entirely) — user types free-text
- **Inline numbered list** trong tin nhắn thường — user reply "A" / "B" / text
- **Recommend + ship default** (theo Core Philosophy rule #1) — skip hỏi nếu default safe

## Pitfall Mapping

| Decision Guard Rule | Status | Note |
|---|---|---|
| `hermes-agent-decision-guard` (NEVER ask clarifying questions when X or Y is inferable) | ✅ Đúng tinh thần | Em đã hỏi vì 3 paths đều plausible (system config / Pocket3 worktree / scope rộng) |
| Telegram `clarify` UI | ❌ FAILED | UI không render, user phải nhắc lại = waste 1 turn + mất trust |

## Related Lesson

Kết hợp với **Hermes-Only Folder Mandate** (anh escalate 19/07 với 4 dấu `!!!!`):

> *"anh muốn em làm mọi việc trong Volumes/Storage-1/Hermes phải tạo và làm tất cả mọi thứ trong đó!!!!"*

Apply ngay:
- Mọi file MỚI → `/Volumes/Storage-1/Hermes/...`
- Ngoại lệ: `~/.hermes/config.yaml`, `~/.hermes/.env`, runtime state
- Scope mở rộng từ "outputs/" (10/07) → toàn bộ `/Volumes/Storage-1/Hermes/` (19/07)

## Recommended Tooling Fix (Future)

Nếu muốn `clarify` work trên Telegram:
1. Patch Hermes gateway → render `choices` thành inline numbered list khi platform = Telegram
2. Hoặc viết helper function `telegram_ask(question, options)` → tự format inline
3. Hoặc document rõ trong `using-agent-skills` skill: "On Telegram, prefer inline numbered list over `clarify` with choices"

## Detection Signal (cảnh báo sớm)

- User reply pattern: `"em hỏi X không thấy xuất hiện?"`, `"hỏi lại xem nào"`, `"không thấy options"`
- → Telegram UI render fail → switch to inline text ngay
- → Nếu user frustrated → apologize + reformat question ngay trong cùng turn
