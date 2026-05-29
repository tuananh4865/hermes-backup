Anh chủ động kiểm tra Kanban worker khi thấy lỗi — muốn biết root cause và fix ngay. Không thích "cứ để yên" khi có vấn đề. Khi investigation reveals 2 root causes (db corruption + missing env), fix cả 2.
§
Task '[Tuấn Anh] Anh muốn em thực hiện rework lại wiki! Xoá bỏ những gì trong 14 ngày qua anh không hỏi tới, chỉ giữ lại thông' — 1 turns
§
Task '[Tuấn Anh] Các raw transcript trong 14 ngày gần nhất thì phải giữ lại chỉ xoá những gì trong 14 ngày gần đây không quan' — 1 turns
§
Task '[Tuấn Anh] Ok' — 1 turns
§
Anh prefer PERIODIC WIKI CLEANUP based on recency — "wiki forget" pattern: only keep content discussed in last 14 days, delete everything else. Cron runs daily at 3AM auto-forget.
§
Task '[Tuấn Anh] Check memory của byterover' — 1 turns
§
Task 'cho anh biết có gì ở phiên bản mới cập nhật hôm nay của hermes?' — 1 turns
§
Task 'Update rồi mà, em check xem. Xong rồi thì check toàn bộ các tính năng nổi bật mà em vừa list ra xem có cái nào chưa hoạt' — 1 turns
§
Task 'tìm hiểu cho anh droid cli' — 1 turns
§
Task 'work kanban task t_3a73b0af' — 1 turns
§
Task 'work kanban task t_3a73b0af' — session 20260529, 1 turns
§
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