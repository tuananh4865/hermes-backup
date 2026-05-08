TikTok Script: "anh" + "mấy con vợ". Max 25s. Feedback: "được chưa" hoặc chỉ ra sai. Gen Z slang: ngon vãi, toang, đỉnh, vuýp. TRÁNH: "đã X là Y", lặp script cũ, "quất một phát".
§
Vision: gemma-4-e2b (~20s) qua LM Studio localhost:1234. MiniMax-M2.7: text-only, NO vision. Config: auxiliary.vision.provider=custom, model=google/gemma-4-e2b, base_url=http://localhost:1234/v1
§
Tuấn Anh research preference: chỉ search/citation từ 2026. Không dùng kết quả 2024-2025. Priority: latest information.
§
MANDATORY SESSION START: wiki start-here.md → SCHEMA.md → index.md → log.md (last 20) → learned-about-tuananh.md. Sau mỗi task: save new learnings to wiki immediately.

Tuấn Anh Philosophy: "Deliver perfect result by any means necessary". KHÔNG hỏi, KHÔNG list options, OWN the task. Rule #4: QA everything before proceeding.
§
LM Studio models thực tế: google/gemma-4-e2b, qwen3.5-0.8b-mlx, qwen3.6-35b-a3b. DEFAULT_MODEL trong lmstudio_wiki_agent.py không khớp - cần update. LM Studio server: http://192.168.0.187:1234/v1
§
Gateway code: ~/.hermes/hermes-agent/gateway/run.py. Hook để add wiki session start: `session:start` event tại line ~3416 (trong `_handle_message_with_agent()`), triggered khi `_is_new_session`. Cron scripts ở /Volumes/Storage-1/Hermes/wiki/.crontab.
§
Antigravity: /Applications/Antigravity.app, ~/Downloads/Antigravity.dmg (195MB, v1.23.2). macOS blocks unsigned → click "Open".
§
Hermes = Orchestrator (2026-05-05): workers content-creator + research-agent. Cron: 9AM briefing, 2h agent monitor, 9PM consolidation. Workers: 8AM/6PM briefs + reports. Felix = autonomous AI company. Workers thật sự tạo 2026-05-06: ~/hermes/workers/{content-creator,research-agent,orchestrator,memory}/ với SOUL.md + HEARTBEAT.md + outputs/. Cron duplicate 90c50d1a2d3c đã xóa - chỉ còn a4b8e528983f (2AM Autoresearch).
§
ByteRover (brv CLI): Verified 2026-05-06. NO account needed — uses LM Studio. Setup: `brv providers connect openai-compatible --base-url http://localhost:1234/v1 --model google/gemma-4-e2b --api-key "no-key"`. gemma-4-e2b ✅ ~76s curate/query. LM Studio: localhost:1234 (Mac Mini 192.168.0.187 DOWN)."
§
Task 'Anh ơi test memory hooks' — session verify_f, 1 turns