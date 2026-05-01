---
title: Transcript 2026-05-01 09:55:19
created: 2026-05-01
platform: telegram
user_id: 1132914873
session_id: 20260501_084046_126f05
timestamp: 2026-05-01 09:55:19
type: transcript
tags: [transcript]
---

## User Message (2026-05-01 09:55:19)

[Tuấn Anh] Nhưng mà anh nghĩ gbrain này sẽ làm việc tự động chứ hoặc khi nào thì nó được trigger?

---

## Assistant Response

**gbrain có automation sẵn.** Check nhanh:

| Command | Trigger | Use case |
|---------|---------|----------|
| `gbrain sync --watch` | Real-time | Auto-sync khi file thay đổi |
| `gbrain autopilot` | Interval (default 1h) | Full maintenance cycle |
| `gbrain dream` | Cron/manual | One-shot overnight cycle |
| `gbrain sync --install-cron` | Cron | Persistent git sync daemon |

**Concretely:**
- **`autopilot`** = daemon chạy liên tục, mỗi interval tự động: lint → backlinks → sync → extract → embe

---
_Saved by transcript-saver hook at 2026-05-01 09:55:19_