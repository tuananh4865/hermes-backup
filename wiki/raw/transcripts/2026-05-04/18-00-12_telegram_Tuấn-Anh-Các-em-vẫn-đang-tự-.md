---
title: Transcript 2026-05-04 18:00:12
created: 2026-05-04
platform: telegram
user_id: 1132914873
session_id: 20260504_175426_149f1cb0
timestamp: 2026-05-04 18:00:12
type: transcript
tags: [transcript]
---

## User Message (2026-05-04 18:00:12)

[Tuấn Anh] Các em vẫn đang tự trả lời mà không cần mention, tìm cách fix đi

---

## Assistant Response

Tìm ra vấn đề rồi anh! Theo wiki, đây là **Telegram Privacy Mode** - bot nhận TẤT CẢ tin nhắn thay vì chỉ @mention.

**Fix cần làm (cho mỗi bot):**

**Step 1: Enable Privacy Mode trong BotFather**
```
1. Mở @BotFather trong Telegram
2. /mybots → chọn bot (ví dụ: @SaturdayClawdBot)
3. Bot Settings → Group Privacy → Enable
```

**Step 2: Restart gateway cho từng profile**
```bash
# Research Lead
hermes gateway --profile research-lead restart

# Content Director  
hermes gateway --profile content-d

---
_Saved by transcript-saver hook at 2026-05-04 18:00:12_