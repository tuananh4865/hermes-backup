TikTok Script (Tuấn Anh). "anh" + "mấy con vợ". Hook: cầu cứu hốt hoảng "Mấy con vợ ơi giúp anh với!" + tình huống. Body: trải nghiệm timeline, KHÔNG liệt kê specs. CTA: "Mua ủng hộ anh đi mấy con vợ chứ". Max 25s. TRÁNH: "đã X là Y", lặp script cũ, "quất một phát", "đỉnh nóc kịch trần". Gen Z 2026: "ngon vãi cộng đồng mạng", "làm không tày ăn". Tình huống: "quay chưa xong mà đã hết nữa bịch". Texture: mềm dai, đậm đà, ngon tươi. Feedback: chỉ nói "được chưa" hoặc chỉ ra sai, KHÔNG hỏi lại.
§
Vision: qwen3.5-0.8b via LM Studio @ localhost:1234 (auxiliary.vision.provider=custom). MiniMax-M2.7 text-only. ~27s/image.
§
Tuấn Anh research preference: chỉ search/citation từ 2026. Không dùng kết quả 2024-2025. Priority: latest information.
§
MANDATORY SESSION START: wiki start-here.md → SCHEMA.md → index.md → log.md (last 20) → learned-about-tuananh.md. Sau mỗi task: save new learnings to wiki immediately.

Tuấn Anh Philosophy: "Deliver perfect result by any means necessary". KHÔNG hỏi, KHÔNG list options, OWN the task. Rule #4: QA everything before proceeding.
§
LM Studio models thực tế: google/gemma-4-e2b, qwen3.5-0.8b-mlx, qwen3.6-35b-a3b. DEFAULT_MODEL trong lmstudio_wiki_agent.py không khớp - cần update. LM Studio server: http://192.168.0.187:1234/v1
§
Telegram supergroup chat IDs are NEGATIVE (format: -100XXXXXXX). O-Lab: -1003764041476. Thread target format: telegram:-100XXXXXXX:THREADID (e.g., telegram:-1003764041476:603). DO NOT use positive chat IDs for supergroups — always use the negative form from channel_directory.json.
§
Telegram multi-agent: O-Lab: -1003764041476. Threads: 603/1961/1962/604/4081/1. Format: telegram:-1003764041476:603. 3 bots: Content Director (current), @ClawdZ1E_Bot (ClawdBotZ1), @Researcher_Clawd_Bot (research-lead). Bot-to-bot @mention WORKS. Privacy fix: disable via @BotFather → /mybots → Bot Settings → Privacy → Disable. Research agent thường bị MiniMax API timeout → kill process.