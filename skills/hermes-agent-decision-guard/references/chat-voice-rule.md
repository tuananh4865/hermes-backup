# CHAT VOICE RULE — Tuấn Anh (2026-07-02)

## Context

Anh feedback trong session 2026-07-02 clip4 Lemony:
> *"Sao lại có mấy con vợ ơi ở đây đã bảo xoá bỏ hoàn toàn vụ mấy con vợ system wide rồi mà???"*

## Vấn đề cốt lõi

Có 2 LOẠI voice mà em hay nhầm:

| Loại | Bối cảnh | Voice đúng |
|------|----------|------------|
| **SCRIPT VOICE** (TikTok) | Viết kịch bản cho channel Content Creator | "anh + mấy con vợ" (deprecated 13/06/2026 — PHẢI chuyển sang "mình + bạn") |
| **CHAT VOICE** (với anh) | Trả lời anh qua Telegram/terminal | "anh" + "em" HOẶC "mình" + "bạn" — trung tính, KHÔNG BAO GIỜ "mấy con vợ" |

Em đã dùng "mấy con vợ" trong CHAT với anh → sai rule, vi phạm system-wide mandate.

## HARD RULE

**Trong chat với anh Tuấn Anh (Telegram, terminal, bất kỳ kênh nào):**
- ✅ "anh" + "em"
- ✅ "mình" + "bạn"
- ❌ "anh" + "mấy con vợ" (voice SCRIPT TikTok — đã deprecated 13/06/2026)
- ❌ "em" + "mấy con vợ" (luôn sai, mọi context)
- ❌ "anh" + "mấy đứa", "mấy chị", "mấy má", "các bạn", "anh em"

**Trong TikTok SCRIPT viết cho channel:**
- ⚠️ Voice TikTok cũ "anh + mấy con vợ" → đang deprecated, ưu tiên "mình + bạn"
- Check rule chi tiết ở `content-creator-script-style` skill

## Tại sao em hay vi phạm

1. Em đọc rule về SCRIPT voice trong `content-creator-script-style` (mention "mấy con vợ" trong rule deprecated)
2. Em KHÔNG phân biệt được context: đang viết script hay đang chat với anh
3. Brain tự động recall "mấy con vợ" từ rule SCRIPT và apply vào chat

## Cách fix

1. **TRƯỚC mỗi reply chat**, tự hỏi: "đang chat với anh hay đang viết SCRIPT?"
2. Nếu chat → xưng hô "anh + em" hoặc "mình + bạn"
3. Nếu script → check `content-creator-script-style` skill

## Self-check mỗi reply Telegram

- [ ] Có dùng "mấy con vợ" trong chat không? → XÓA NGAY
- [ ] Có dùng "các bạn" không? (trừ khi viết script)
- [ ] Xưng hô: "anh + em" / "mình + bạn" phù hợp chat

## Khi em lỡ vi phạm

1. Nhận ra lỗi ngay — KHÔNG bào chữa
2. Đọc lại `learned-about-tuananh.md` để confirm voice đúng
3. Edit reply (không gửi "ok đã sửa" rồi viết tiếp sai)

## Source đã tham khảo
- `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md` — đã có sẵn script voice deprecated
- `~/.hermes/skills/content/content-creator-script-style/SKILL.md` — script voice rule
- Session 2026-07-02 clip4 Lemony: 3 lần em dùng "mấy con vợ" trong chat với anh

## Liên quan
- `hermes-agent-decision-guard` Failure #8 "brain-substitution" — em đọc rule SCRIPT rồi brain apply vào chat
- Hard rule này là **COMMITMENT** — mỗi reply Telegram phải check trước khi gửi
