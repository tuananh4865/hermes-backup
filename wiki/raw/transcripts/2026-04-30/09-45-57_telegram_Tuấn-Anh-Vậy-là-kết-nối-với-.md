---
title: Transcript 2026-04-30 09:45:57
created: 2026-04-30
platform: telegram
user_id: 1132914873
session_id: 20260430_091300_b5cc3d88
timestamp: 2026-04-30 09:45:57
type: transcript
tags: [transcript]
---

## User Message (2026-04-30 09:45:57)

[Tuấn Anh] Vậy là kết nối với gemini cli được luôn phải không?

---

## Assistant Response

**Đúng rồi.** Từ search trước, Warp hỗ trợ 8 CLI agents:

- Claude Code ✓
- OpenAI Codex ✓
- OpenCode ✓
- Gemini CLI ✓
- Amp, Augmie, Droid, Pi ✓

Và tương tự Claude Code, Gemini CLI cũng có thể config dùng MiniMax API. MiniMax docs có hướng dẫn setup Gemini CLI với MiniMax endpoint.

**Vậy anh có thể setup:**
```
Warp + Gemini CLI (MiniMax API) + notifications
```

**Lưu ý:** Gemini CLI khi dùng MiniMax sẽ mất web search (vì MiniMax API không expose Anthropic websearch). Muốn search phải thêm M

---
_Saved by transcript-saver hook at 2026-04-30 09:45:57_