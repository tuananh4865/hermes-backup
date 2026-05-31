Task 'tìm hiểu cho anh droid cli' — session 20260529, 3 turns
§
Modified files: src/auth.py, mission.md, /.factory/config.json
§
Task 'work kanban task t_0f7cfa72' — 1 turns
§
Task 'work kanban task t_0f7cfa72' — session 20260529, 1 turns
§
## Research Accuracy Failure (2026-05-29)

**What happened:** Said MiniMax-M2.7 doesn't support Anthropic-compatible endpoint. Was 100% wrong. Correct: M2.7 fully supports `https://api.minimax.io/anthropic`.

**Rule:** For API endpoints, model compatibility matrices, base URLs — ALWAYS web-search first. Never rely on old knowledge.

**Fix:** Patched `hermes-agent` skill + created `references/minimax-droid-config.md`
§
[2026-05-29] QA failure: tự tin thái quá, nói M2.7 không support Anthropic-compatible endpoint. Sai hoàn toàn. Đã tạo qa-gate skill. Rule: ALWAYS web-search cho API specs. Confidence < 9 = research bắt buộc.
§
[2026-05-29] QA failure lesson: ALWAYS web-search API specs. Created qa-gate skill. Memory limit 2200 chars in memory_tool.py line 125 - design đúng của Hermes, không phải bug.
§
Task '[Tuấn Anh] https://youtu.be/X2huNCHDwMQ?si=PjUKh4bUvebSNurC' — 1 turns
§
Anh tự restart gateway khi được hỏi — không cần hướng dẫn thêm. Config change → thông báo "restart gateway để apply" → xong.
§
Task 'Có cách nào để anh trò chuyện bằng âm thanh với em liên tục được không nhỉ?' — session 20260529, 1 turns
§
Task '[System note: Your previous turn in this session was interrupted by a gateway restart. The conversation history below is' — 1 turns
§
Task '[System note: Your previous turn in this session was interrupted by a gateway restart. The conversation history below is intact. If it contains unfini' — session 20260529, 1 turns
§
Task 'Nghe được rồi nhưng có vẻ nó đang nói tiếng Anh' — 1 turns
§
Task '[Tuấn Anh] Tiếp theo đến phần kịch bản thu hút, làm sao để có một kịch bản thu hút?' — 1 turns
§
Task '[Tuấn Anh] https://x.com/zodchiii/status/2060728613872234644/video/1?s=46 Xem được video trong tweet này không?' — 1 turns
§
Task '[Tuấn Anh] Dùng browser_harness đi' — 1 turns
§
Task 'check mcp của exa' — 1 turns
§
Task 'test lại xem' — 1 turns
§
Task '[Replying to: "Anh ơi, em đã thử nhiều cách nhưng không xem được video vì:  Vấn đề: - Video nằm trong tweet của @zodchii' — 1 turns
