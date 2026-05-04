---
title: Transcript 2026-05-04 16:02:37
created: 2026-05-04
platform: telegram
user_id: 1132914873
session_id: 20260504_145734_7c559b
timestamp: 2026-05-04 16:02:37
type: transcript
tags: [transcript]
---

## User Message (2026-05-04 16:02:37)

[Tuấn Anh] Anh chỉ muốn các em trả lời khi được mention thôi thì làm sao, hiện tại các em đã trả lời bất kể là có được mention hay không

---

## Assistant Response

Ah! Vấn đề là **privacy mode bị disable** ở Telegram side. Khi disable privacy mode, bot thấy TẤT CẢ messages trong group → respond tất.

**Cách fix đúng:**

1. **Ở BotFather**: @Researcher_Clawd_Bot → Group Privacy → **ENABLE** (để bot chỉ thấy messages khi được mention)
2. **Ở config**: `require_mention: true` (đã đúng)

Sau đó restart gateway là xong. Khi đó bot CHỈ respond khi được @mention thật sự.

Anh vào @BotFather → /mybots → @Researcher_Clawd_Bot → Edit Bot → Group Privacy → **Enable**

---
_Saved by transcript-saver hook at 2026-05-04 16:02:37_