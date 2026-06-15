Tuấn Anh prefers sending videos as Telegram attachments and wants me to download + resend them back via Telegram (not just analyze). He got frustrated when I said I couldn't "see" Telegram-attached videos. Key workflow: when he sends a TikTok/YouTube link → download with yt-dlp → send back via MEDIA:/path in send_message. This pattern works 100%.
§
Telegram attachments: Hermes gateway passes only text/links, NOT binary media. Video workflow: yt-dlp → ffprobe streams (HEVC = likely silent content) → if HEVC without audio: silent is style not error → ffmpeg 720p H.264 AAC → send MEDIA:/path. Telegram timeout >50MB so always compress.
§
Vietnamese casual, concise. TikTok voice: TRUNG TÍNH, chuyên nghiệp (loại bỏ "anh" + "mấy con vợ" từ 13/06/2026). Skills đã patch: tiktok-viral-script, default-project-hub-pattern, multi-agent-orchestrator, youtube-transcript-extractor, video-download-yt-dlp. Model: MiniMax-M3.
§
Modified files: wiki/concepts/tiktok-channel-building-strategy-hi-imdung-style.md, /Volumes/Storage-1/Hermes/wiki/concepts/tiktok-channel-building-strategy-hi-imdung-style.md, /Volumes/Storage-1/Hermes/wiki/concepts/tiktok-content-guideline-hi-imdung-style.md, /Volumes/Storage-1/Hermes/wiki/log.md, /Volumes/Storage-1/Hermes/wiki/index.md
§
QUALITY BAR (13/06 BẮT BUỘC MỌI RESPONSE): (1) KHÔNG trả lời chung chung. (2) KHÔNG tự đoán. (3) KHÔNG bịa đặt. (4) Mọi thông tin phải có research rõ ràng: URL nguồn chính thức + ngày truy cập + đối chiếu ≥2 nguồn độc lập. (5) Không chắc → PHẢI đặt câu hỏi khai thác trước khi trả lời. Sai lầm cũ: cung cấp info thiếu sâu, chung chung, không nguồn — sửa triệt để.
§
5 CHẶNG HÀNH TRÌNH (Bản đồ tổng file 00): 0 Chuẩn bị (~90% xong, còn đăng ký Shopee Affiliate + Accesstrade + chân dung khán giả + vào 1 cộng đồng) → 1 Khởi động (30 video đầu, 4-5 tuần, mục tiêu 1.000 follower mở giỏ TikTok) → 2 Tìm Creator-Market Fit (tuần 5-8, 4-6k follower + đơn affiliate đầu tiên) → 3 Tăng tốc (tuần 9-12, 10k follower + 50tr GMV/tháng + 5k sub YT) → 4 Bền vững (tháng 4-12, đa nguồn thu + cộng đồng riêng).
§
Task 'Mục tiêu của anh là trở thành một content creator uy tín trên mạng xã hội tiktok và YouTube ở ngách công nghệ và phụ kiệ' — 2 turns
§
Task 'ngày thứ 2 đầu tuần á! đọc hết file rồi xem nên làm gì phù hơp' — 1 turns
