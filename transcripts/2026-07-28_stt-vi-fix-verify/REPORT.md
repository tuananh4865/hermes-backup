# STT Vietnamese Fix Verification Report (29/07/2026)

## Fix Applied
- `~/.hermes/config.yaml`:
  - `stt.local.model: medium` (upgraded from `base`)
  - `stt.local.language: vi` (was empty → fell back to "en" default)

## Root Cause
- `transcription_tools.py` DEFAULT_LOCAL_STT_LANGUAGE = "en"
- Config `language: ''` (falsy) → fall back to "en" → whisper CLI gọi `--language en`
- Audio Việt → Whisper hallucinate thành câu tiếng Anh vô nghĩa (anh quote: "I think this video is for you, Edith...")

## Verification (3 audio cached)

### Test 1 — audio_8fa584ca44e8.ogg (24s, the one anh quoted)
**Before fix:** "I think this video is for you, Edith. I haven't been able to use it for a long time. I think it's better to use it for a long time. So I can try it with a different clip."

**After fix:** "Anh nhận thấy là những cái video mà em edit / Em chưa sắp xếp được nội dung / Thành theo kiểu hay giống như anh tưởng tượng / Vậy nên là em có thể thử lại với 1 cái clip nào đó khác được không"

### Test 2 — audio_24345242fc8c.ogg
- "Đại sao? Đại sao?" (medium model nhầm "T"→"Đ", large-v3 sẽ chính xác hơn)

### Test 3 — audio_7b7431fcecca.ogg
- "Xin chào! Tôi là Tuấn Anh đây!" (đúng)

### Test 4 — audio_a153686c3bb0.ogg
- "Nguyên nhân vì sao siêu phẩm 88F Tour 2024 lại được? Tại sao các cây vật đánh đôi chuyên lên lưới lại tránh xa các cây vật dài và nặng đầu?" (đúng)

## Latency
- Whisper medium CPU: ~16-20s cho audio 24s (~0.7-0.8x real-time)
- mlx_whisper large-v3-mlx: ~3s cho audio 24s (0.13x, nhanh hơn 5-6x) — but Hermes STT wrapper không dùng MLX

## Next Steps
- Nếu anh muốn accuracy cao hơn cho mix Việt-Anh: `hermes config set stt.local.model large-v3` (chậm hơn 4-5x medium)
- Backup config ở ~/.hermes/config.yaml.bak-2026-07-28-stt-vi
