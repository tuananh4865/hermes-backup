---
title: Transcript 2026-05-04 10:26:52
created: 2026-05-04
platform: telegram
user_id: 1132914873
session_id: 20260504_070229_2ee7594c
timestamp: 2026-05-04 10:26:52
type: transcript
tags: [transcript]
---

## User Message (2026-05-04 10:26:52)

[Tuấn Anh] Setup thông qua tele được ko hay phải dùng terminal?

---

## Assistant Response

Setup Kanban **phải qua terminal/cli** — Telegram chỉ nhận notification thôi.

Cụ thể:

| Thứ | Telegram | Terminal |
|-----|----------|----------|
| Tạo task | ❌ | ✅ `hermes kanban create` |
| Xem board | ❌ | ✅ `hermes dashboard` (web) |
| Nhận thông báo | ✅ | — |
| Claim/complete/block | ❌ | ✅ |
| Xem task details | ❌ | ✅ `hermes kanban show <id>` |

**Để bắt đầu**, anh cần chạy trên terminal:

```bash
hermes kanban init
hermes dashboard   # cái này mở trình duyệt web, không phải Telegram
herm

---
_Saved by transcript-saver hook at 2026-05-04 10:26:52_