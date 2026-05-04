---
title: Transcript 2026-05-04 14:23:21
created: 2026-05-04
platform: telegram
user_id: 1132914873
session_id: 20260504_102938_8605bc25
timestamp: 2026-05-04 14:23:21
type: transcript
tags: [transcript]
---

## User Message (2026-05-04 14:23:21)

[Tuấn Anh] Không ý anh nói là tạo thêm một agent độc lập ngay bên trong hermes agnet luôn và agent đó có kiến thức, role và memory riêng biệt

---

## Assistant Response

Ah anh muốn tạo **HOÀN TOÀN ĐỘC LẬP** với memory + knowledge + role riêng! Hermes gọi đó là **Profiles**.

## Cách tạo Agent Độc lập trong Hermes

### Architecture
```
Hermes (Anh đang dùng - default profile)
├── Profile: research-agent  ← Research Lead riêng
├── Profile: content-agent    ← Content Director riêng  
└── Profile: engineering-agent ← Engineering Lead riêng
```

### Mỗi profile có
- Isolated config, sessions, skills, memory
- Role definition riêng
- Knowledge riêng

Để em hỏi anh: *

---
_Saved by transcript-saver hook at 2026-05-04 14:23:21_