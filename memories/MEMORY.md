Telegram video analysis (16/06): Anh gửi video binary qua Telegram → em detect file mới nhất trong `~/Downloads/Telegram Desktop/` + `~/Downloads/*.mp4` → convert HEVC→H.264 720p crf 28 → extract frames @ 1fps + audio → vision model parallel + mlx-whisper vi → gửi lại qua MEDIA:/path. Skill: `telegram-video-analysis`.
§
VERIFY bắt buộc (16/06 lesson): User QA theo 3 layers — (1) code tồn tại, (2) test behavior trong session thật, (3) test future-proof (cron + fresh session). "Yên tâm dùng" = reliability 100% chứ không phải "đã chạy". Report "done" phải kèm evidence (mtimes, exit codes) + honest caveats (cron untested, fresh session untested). User ưa "honest 97.5%" hơn "fake 100%". 16/06 em tự tìm 2 bugs thật (case-sensitive grep + fresh-file re-inject trong add-fable5-to-soul.sh) — đó là evidence QA tự bắt được lỗi. Hook stdin JSON (Hermes pass payload via stdin). Defensive: skip nếu message starts with "$". MCP web_search: `site:` operator → 1027-output new_sensitive → fallback keyword-based ("findniche" as text, not site:findniche.com).
§
Default project: Content Creator (3 trụ SETUP+EDIT+GEAR, lấy cảm hứng @hi.imdung). Path: /Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/. Hub: hub.md. Cấu trúc 16/06: Analysis/ + Operations/ + Raw/ + Archive/ + root 16 files. Mỗi session mới: load hub + Trend_Updates/ + Operations/ho-so-giong-van-...md.
§
.
§
[System-wide mandate pattern] — Tuấn Anh prefer 3-piece enforcement: shared reference file + refactor consumers + idempotent injector + CI gate + auto-check hook (WARN only). Token reduction ≥80%. AGENTS.md cấm touch core code. Verify concept in hermes-agent.nousresearch.com/docs trước khi scaffold (e.g. "Worker" concept KHÔNG tồn tại → dùng Profile/Sub-agent).
§
[16/06 review format] GỌN: chỉ điểm mạnh + nhược + so sánh ngoại hình, BỎ bảng specs. Workflow: 5-7 ưu (≥2 nguồn) + 5-7 nhược thật + so ngoại hình vs Apple Pencil + script 60s. Detail ≠ tốt hơn.
§
Task '[Tuấn Anh] Tựu chung là anh đã có thể yên tâm dùng vì đã đủ 4 parten rồi phải không? Ở cả system wide, hiện tại và tương' — 2 turns
§
Task '[Tuấn Anh] https://youtu.be/p7d0k_QDFhs?si=Wf-83VOUAxAPxd5T  Nhớ cái này không?' — 1 turns
§
Task '[Tuấn Anh] https://youtu.be/p7d0k_QDFhs?si=Wf-83VOUAxAPxd5T  Nhớ cái này không?' — session 20260617, 1 turns
§
Task '[Tuấn Anh] Không phải rồi, check lại đi' — 1 turns
§
Task '[Tuấn Anh] giờ check, verify và qa nghiêm ngặt lại loop engineering đi!' — 3 turns
