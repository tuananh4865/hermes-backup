---
title: Transcript 2026-05-01 08:26:22
created: 2026-05-01
platform: telegram
user_id: 1132914873
session_id: 20260501_080558_8e19fc
timestamp: 2026-05-01 08:26:22
type: transcript
tags: [transcript]
---

## User Message (2026-05-01 08:26:22)

[Tuấn Anh] B em chắc là ollama có option 1536 không? hay là em đọc kĩ lại repo đi: https://github.com/garrytan/gbrain

---

## Assistant Response

Anh ơi, em đào sâu vào repo rồi. Kết quả:

**Tình hình thực tế:**

| Phiên bản | Trạng thái |
|-----------|------------|
| Local (v0.22.8) | Hardcode OpenAI, không có Ollama/LM Studio support |
| PR #257 (v0.27) | Đã có pluggable embedding — Ollama, LM Studio, Voyage, Google đều xài được |

**PR #257 là cái gì:**
- garrytan merge rất nhiều PR cộng đồng (Ollama, LM Studio, Voyage, Gemini) thành 1 hệ thống dùng Vercel AI SDK
- Environment variables mới: `EMBEDDING_PROVIDER=ollama` hoặc `openai-com

---
_Saved by transcript-saver hook at 2026-05-01 08:26:22_