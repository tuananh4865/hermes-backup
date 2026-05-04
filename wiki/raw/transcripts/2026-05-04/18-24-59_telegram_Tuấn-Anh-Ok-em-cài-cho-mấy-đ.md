---
title: Transcript 2026-05-04 18:24:59
created: 2026-05-04
platform: telegram
user_id: 1132914873
session_id: 20260504_175426_149f1cb0
timestamp: 2026-05-04 18:24:59
type: transcript
tags: [transcript]
---

## User Message (2026-05-04 18:24:59)

[Tuấn Anh] Ok em cài cho mấy đứa kia biết trong file soul của tụi nó là luôn phải mention nếu muốn nhờ agent khác làm việc nhé

---

## Assistant Response

Anh ơi, vấn đề là logs cho thấy 2 con bot (Saturday=8594106827, ResearchClaw=8706108095) đang bị block ở **main gateway** vì không có trong `TELEGRAM_ALLOWED_USERS`. 

Có 2 cách fix:

**Cách 1 (nhanh):** Thêm bot IDs vào allowed users của main gateway:
```
TELEGRAM_ALLOWED_USERS=1132914873,8594106827,8706108095
```

**Cách 2 (đúng kiến trúc):** Cho mấy con bot chỉ respond trong DM, không dùng chung group O-Lab với main gateway.

Anh muốn fix theo cách nào?

---
_Saved by transcript-saver hook at 2026-05-04 18:24:59_