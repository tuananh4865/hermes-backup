Tuấn Anh prefers sending videos as Telegram attachments and wants me to download + resend them back via Telegram (not just analyze). He got frustrated when I said I couldn't "see" Telegram-attached videos. Key workflow: when he sends a TikTok/YouTube link → download with yt-dlp → send back via MEDIA:/path in send_message. This pattern works 100%.
§
Telegram attachments: Hermes gateway passes only text/links, NOT binary media. Video workflow: yt-dlp → ffprobe streams (HEVC = likely silent content) → if HEVC without audio: silent is style not error → ffmpeg 720p H.264 AAC → send MEDIA:/path. Telegram timeout >50MB so always compress.
§
Vietnamese casual, concise. TikTok voice: TRUNG TÍNH, chuyên nghiệp (loại bỏ "anh" + "mấy con vợ" từ 13/06/2026). Skills đã patch: tiktok-viral-script, default-project-hub-pattern, multi-agent-orchestrator, youtube-transcript-extractor, video-download-yt-dlp. Model: MiniMax-M3.
§
Modified files: wiki/concepts/tiktok-channel-building-strategy-hi-imdung-style.md, /Volumes/Storage-1/Hermes/wiki/concepts/tiktok-channel-building-strategy-hi-imdung-style.md, /Volumes/Storage-1/Hermes/wiki/concepts/tiktok-content-guideline-hi-imdung-style.md, /Volumes/Storage-1/Hermes/wiki/log.md, /Volumes/Storage-1/Hermes/wiki/index.md
§
Default project = Content Creator (13/06, hệ thống số mới). Path: /Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/. Hub: hub.md. 19 files + 3 folders. Hệ thống SỐ: 00/01/02/03 + bo-cong-thuc-viral. Mỗi session: load hub.md + 00-ban-do-tong.md + Trend_Updates/. Skills patched 13/06: default-project-hub-pattern (pitfalls 7+8: refresh-existing-project + sibling memory write detection), youtube-transcript-extractor (pitfalls 6+7: auto-sub-before-Whisper + TikTok no auto-sub).
§
Task 'Transcript cho anh video này' — 4 turns
§
IMPORTANT (2026-06-13): Anh muốn LOẠI BỎ HOÀN TOÀN voice "anh" + "mấy con vợ" khỏi TẤT CẢ output. Dùng giọng trung tính, chuyên nghiệp, không xưng hô thân mật. Cập nhật: hub.md (project), content-creator-project.md (wiki), guideline TikTok. Từ giờ không dùng "mấy con vợ", không tự xưng "em" gọi "anh" — dùng giọng neutral hoặc tự xưng "mình" gọi "bạn".