---
title: Transcript 2026-04-27 23:01:20
created: 2026-04-27
platform: telegram
user_id: 1132914873
session_id: 20260427_215644_0f64d0
timestamp: 2026-04-27 23:01:20
type: transcript
tags: [transcript]
---

## User Message (2026-04-27 23:01:20)

[Tuấn Anh] check lại xem giờ có bao nhiêu gateway đang chạy?

---

## Assistant Response

**Kết quả:**

| PID | PPID | Process | Nguồn gốc |
|-----|------|---------|-----------|
| 89028 | 89027 | `hermes gateway run --replace` | `run_hermes_gateway.sh` |
| 89027 | 89025 | `bash ./run_hermes_gateway.sh` | `run_hermes_gateway.sh` (while true loop) |
| 89025 | 1 | `bash -c nohup ./run_hermes_gateway.sh...` | **launchd** (plist) |

**Tóm tắt:**
- **1 gateway** đang chạy (89028) — restart tự động qua `run_hermes_gateway.sh`
- Script này được **launchd** khởi động qua `ai.hermes.gateway.pl

---
_Saved by transcript-saver hook at 2026-04-27 23:01:20_