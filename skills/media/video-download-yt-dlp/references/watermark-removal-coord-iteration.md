# Watermark Removal — Coordinate Iteration Case Study

**Date:** 2026-07-10
**Source clip:** YouTube Shorts `UqdcgQ-_oN4` (27.65s, AV1, 720×1280)
**Target:** "SMASH HUB" watermark góc dưới phải, cố định suốt video

## Bối cảnh

Anh tải 3 clip YouTube Shorts trong ngày (`aq61zm10xus`, `MkAlimt7et0`, `UqdcgQ-_oN4`). Sau đó anh yêu cầu xoá chữ "SMASH HUB" trong 1 clip. Em đã iterate 5 lần để ra kết quả cuối cùng. Lần sau có thể rút xuống 2 lần.

## Timeline các iteration (đầy đủ)

### Loop 1 — `delogo` đầu tiên (FAILED)

```bash
ffmpeg -i in.mp4 -vf "delogo=x=500:y=1100:w=210:h=120:show=0" -c:a copy v1.mp4
```

- Coord từ vision estimate trên full frame 720×1280 → vision map sang pixel KHÔNG chính xác
- Verify frame → "SMASH HUB" vẫn hiện rõ ở góc dưới phải, không che được
- **Cause:** vision upscale/downscale ảnh trước khi hiển thị, pixel coordinates em đọc từ vision response không map 1:1 sang video pixels. Mất 30% công sức vì coord sai ngay từ đầu.

### Loop 2 — Boxblur overlay (FAILED, sai approach)

```bash
ffmpeg -i in.mp4 -filter_complex "[0:v]crop=320:200:430:1075,boxblur=20:1[bg];[0:v][bg]overlay=430:1075" -map "[v]" -map 0:a v2.mp4
```

- Em nghĩ boxblur rộng sẽ che triệt để
- Verify → text đã hết, mượt hơn loop 1
- **Nhưng** anh reply: *"Che đúng vùng có chữ smash hub thôi"* → vùng box 320×200 bao trùm cả phần sân cầu lông, không phù hợp
- **Lesson:** default = `delogo` rectangle vừa đủ, KHÔNG mặc định boxblur rộng

### Loop 3 — Crop+vision (FAILED, vẫn coord sai)

```bash
ffmpeg -y -i in.mp4 -ss 13 -vf "crop=400:80:300:1080" -vframes 1 /tmp/smash_hub_tight.png
# Vision ask: "Trong crop 400×80 chữ SMASH HUB chiếm x,y đến x,y nào?"
# Vision reply: x=65-330, y=15-60 trong crop
# Coord tính: x=365-630, y=1095-1140 trong video
ffmpeg -i in.mp4 -vf "delogo=x=365:y=1095:w=265:h=45:show=0" -c:a copy v3.mp4
```

- Crop CHẶT → vision coord tốt hơn nhưng vẫn không khớp video pixel
- Verify → text vẫn còn nguyên
- **Lesson:** ngay cả vision trên crop CHẶT cũng KHÔNG đảm bảo coord chính xác 100%

### Loop 4 — Wider delogo (PARTIAL success)

```bash
ffmpeg -i in.mp4 -vf "delogo=x=350:y=1000:w=240:h=120:show=0" -c:a copy v4.mp4
```

- Coord lệch → text phần lớn đã mờ, chỉ còn "HUB" mờ ở góc phải
- Verify → 60% clean, chưa ship
- **Lesson:** coord phải SHIFT sang phải + xuống dưới so với vision estimate

### Loop 5 — Final winning config (✅ SUCCESS)

```bash
ffmpeg -i in.mp4 -vf "delogo=x=380:y=1000:w=280:h=110:show=0" -c:a copy /Users/tuananh4865/Downloads/UqdcgQ-_oN4_YT_Shorts_nosmash_precise.mp4
```

- Coord shift (+30 right, +0 down) + width nhỏ lại 280 (vừa đủ)
- Verify → text sạch 100%, không động vào VICTOR / HSBC / CHANGZHOU
- Size: 4.49 MB, duration 27.65s (giữ nguyên), codec H.264 (auto re-encode từ AV1)
- Ship OK

## Final coords verified

```
WATERMARK_BBOX = {x: 380, y: 1000, w: 280, h: 110}
```

Khớp đúng vị trí text "SMASH HUB" trên frame gốc 720×1280 (verify bằng output frame 13s).

## Quy tắc rút ra cho case tiếp theo (encoded in SKILL.md W5+W8+W9)

1. **W1 (clarify):** Hỏi anh clip nào trong N clips, BLUR hay che kín
2. **W5 (loop):** Sau MỖI `delogo` → extract frame ở giây giữa → vision verify → adjust nếu còn
3. **W8 (crop trước):** Nếu coord từ full-frame vision sai, dùng `ffmpeg crop CHẶT + vision trên crop` để có coord tương đối tốt hơn. Verify với empirical loop.
4. **W9 (user preference):** Anh thường prefer **delogo rectangle vừa đủ** > boxblur rộng > drawbox solid color. Trừ khi text moving hoặc semi-transparent.

## Files đã ship

| File | Status | Vai trò |
|---|---|---|
| `UqdcgQ-_oN4_YT_Shorts.mp4` | Giữ nguyên | Gốc |
| `..._nosmash.mp4` | Loop 1: còn sọc artifact | Deprecated |
| `..._nosmash_smooth.mp4` | Loop 2: boxblur rộng | Deprecated |
| `..._nosmash_precise.mp4` | **Loop 5: ✅ FINAL** | Ship cho anh |

## Lessons cho sọt rác wiki (đã ghi vào SKILL.md)

- **W8 NEW:** Vision pixel coords KHÔNG map 1:1 sang video pixels → dùng crop CHẶT hoặc Python scan thay vì feed thẳng vào delogo
- **W9 NEW:** User preference cho "che đúng vùng có chữ" → delogo rectangle vừa đủ, KHÔNG boxblur rộng
- **W5 reinforce:** Có case cần 5 loops, không phải luôn 2 loops như expected result minh họa
