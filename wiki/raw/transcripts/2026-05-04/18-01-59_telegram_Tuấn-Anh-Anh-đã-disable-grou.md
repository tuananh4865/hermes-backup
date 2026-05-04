---
title: Transcript 2026-05-04 18:01:59
created: 2026-05-04
platform: telegram
user_id: 1132914873
session_id: 20260504_175426_149f1cb0
timestamp: 2026-05-04 18:01:59
type: transcript
tags: [transcript]
---

## User Message (2026-05-04 18:01:59)

[Tuấn Anh] Anh đã disable group policy rôig

---

## Assistant Response

Gateway đã restart. Sau khi restart, các bot sẽ chỉ respond khi được @mention hoặc reply trực tiếp đến bot.

**Tóm tắt fix:**
- Config gốc: `require_mention` nằm trong `discord:` thay vì `telegram:`
- Telegram section thiếu `require_mention: true`
- Đã thêm và restart gateway

Bây giờ các agent chỉ respond khi được mention thôi anh.

---
_Saved by transcript-saver hook at 2026-05-04 18:01:59_