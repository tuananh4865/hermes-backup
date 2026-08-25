---
title: Send Script to Telegram — Workflow
description: Khi user yêu cầu "gửi script vào đây" / "gửi kịch bản qua đây" → workflow gửi Markdown script qua Telegram sau khi viết xong. Tránh để user phải tự mở file.
type: reference
related: [tiktok-viral-script, product-review-research-protocol, script-review-then-rewrite-workflow]
---

# Send Script to Telegram — Workflow

> **Created:** 2026-06-16 (sau khi user yêu cầu "Gửi kịch bản vào đây cho anh" sau khi viết review GOOJODOQ GD14)
> **Skill governing:** `tiktok-viral-script`

## Tại sao workflow này tồn tại

**Real failure pattern 16/06:** Sau khi viết script 18.2KB vào file `Operations/review-goojodoq-gd14.md`, user nói "Gửi kịch bản vào đây cho anh" — agent phải đọc lại toàn bộ file 396 dòng rồi gửi qua Telegram. Mất 1 lượt + tool call lớn không cần thiết.

**Lesson:** Sau khi viết xong kịch bản (hoặc review, hoặc tài liệu markdown quan trọng) cho Content Creator project, **MẶC ĐỊNH GỬI LUÔN qua Telegram** (hoặc kênh chat user đang dùng). User đọc trên Telegram tiện hơn mở file.

## Trigger conditions

User nói một trong các câu:
- "Gửi kịch bản vào đây"
- "Gửi script qua đây"
- "Gửi vào Telegram"
- "Anh muốn đọc trên điện thoại"
- "Send it here"
- Hoặc **MẶC ĐỊNH** sau khi viết bất kỳ script/review nào cho Content Creator project

## Workflow 3 bước

### Step 1: Đọc file (KHÔNG viết lại từ đầu)

Đừng viết lại nội dung từ memory. Đọc file đã ghi bằng `read_file`:

```python
content = read_file(path="path/to/script.md")
```

Lý do: Đảm bảo gửi ĐÚNG nội dung file, không bị lệch do nhớ sai.

### Step 2: Format lại cho Telegram

Markdown trong file có thể dài. Khi gửi qua Telegram:

**GIỮ:**
- Headers (##, ###)
- Bold/italic
- Code blocks
- Bullet lists
- Tables (Telegram sẽ tự convert sang row-group bullets)

**BỎ hoặc rút gọn:**
- Frontmatter YAML (cho đỡ noise)
- Long code blocks trừ khi cần
- Quá nhiều dòng trống

**Cấu trúc gửi:**

```
# [Tên kịch bản / review]

> [Mục đích + 1 dòng tóm tắt quan trọng nhất]

---

## [Phần 1: Tóm tắt nhanh]
- [1-3 bullets ngắn]

## [Phần 2: Script chi tiết]
[Toàn bộ script hoặc phần quan trọng nhất]

## [Phần 3: Bảng so sánh / Thông số]
[Bảng nếu có]

---

[Link file: path/to/file.md]
```

### Step 3: Gửi qua `send_message`

```python
send_message(
    action="send",
    target="telegram",  # hoặc target cụ thể user chỉ định
    message=<formatted_content>
)
```

**Lưu ý:**
- Telegram có giới hạn 4096 ký tự mỗi message. Nếu script dài → chia thành nhiều message
- Nếu file >4096 ký tự: gửi phần 1 (tóm tắt + script chính) + báo "phần còn lại xem file [path]"
- KHÔNG gửi MEDIA: cho markdown (chỉ gửi MEDIA kèm ảnh/video)

## Example: Gửi review GOOJODOQ GD14

**User:** "Gửi kịch bản vào đây cho anh"
**File:** `Operations/review-goojodoq-gd14.md` (18.2KB, 396 dòng)

**Action của agent:**
1. `read_file` → lấy 396 dòng
2. Format lại: bỏ YAML, giữ headers + tables, rút gọn checklist
3. `send_message` action="send" target="telegram" → gửi toàn bộ (~5KB text, trong giới hạn)

**Kết quả:** User nhận được script trên Telegram ngay, không cần mở file.

## Pitfalls

### ❌ Viết lại từ memory thay vì đọc file
- Mất công + sai nội dung
- Fix: LUÔN `read_file` file trước khi gửi

### ❌ Gửi cả YAML frontmatter
- Làm noise, user không cần metadata
- Fix: Strip frontmatter trước khi gửi

### ❌ Gửi file quá dài (>4096 ký tự) mà không chia
- Telegram sẽ bị lỗi hoặc cắt ngang
- Fix: Chia thành nhiều message HOẶC tóm tắt + báo "xem file đầy đủ"

### ❌ Không gửi sau khi viết xong
- User phải hỏi lại "gửi cho anh" → mất 1 lượt
- Fix: Mặc định gửi qua Telegram sau khi viết xong script/review quan trọng

### ❌ Gửi ngay cả khi user KHÔNG ở Telegram
- Nếu user ở platform khác (Discord, Slack, iMessage) → check trước
- Fix: Nếu không rõ platform → dùng `send_message(action='list')` xem available channels

## When NOT to send

- ❌ Khi user chỉ nói "viết file" mà KHÔNG nói "gửi" → chỉ lưu file, đợi user yêu cầu
- ❌ Khi user đang ở giữa flow research chưa xong → đợi có bản final
- ❌ Khi file >100KB → gửi excerpt + link file, không gửi toàn bộ

## Related

- `references/script-review-then-rewrite-workflow.md` — Workflow review + rewrite (thường đi kèm)
- `references/product-review-research-protocol.md` — Protocol viết review sản phẩm
- `references/video-to-telegram-delivery.md` — Workflow gửi VIDEO (khác workflow này)
- Memory: User thích gửi video/script qua Telegram
