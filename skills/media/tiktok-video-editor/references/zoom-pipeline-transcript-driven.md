# Signal-Based Zoom Effect Pipeline (Transcript-Driven, No Vision)

> Added v0.06 (26/07/2026) - per Tuấn Anh feedback "em không thể liên tục dùng vision để hiểu video nên phải chuyển sang phân tích transcript"

## Nguyên lý

Khi edit clip TikTok, zoom in vào gương mặt/sản phẩm là kỹ thuật quan trọng để:
- Tăng độ tập trung viewer vào chi tiết (sợi carbon fiber, ron cao su, logo nhỏ)
- Show biểu cảm mặt khi reaction quan trọng ("trầm trồ", "thích ghê")
- Nhấn moment USP/benefit (nhanh sạch hơn, bảo vệ tốt hơn)

**Constraint:** Vision API (vision_analyze) expensive + chậm + không scale. Phải dùng TRANSCRIPT text + keep_plan structure để detect zoom moments.

## 3 Signal Layers (auto-detect, không cần vision)

### Layer 1: Range name signal (keep_plan structure)

Nếu `keep.name` thuộc nhóm show-detail → AUTO slow zoom 1.0→1.25x:
- `USP`, `DETAIL`, `SHOW`, `DESC` → slow zoom toàn range
- `HOOK`, `CTA` → giữ wide (context/closing)
- `PAIN`, `GUIDE`, `COMPATIBILITY`, `PORTABILITY` → tùy content

### Layer 2: Verbal cue (transcript text scan)

Detect trigram "deictic + show verb" trong 5-word window:
- Deictic: `đây`, `nè`, `đó`
- Show verb: `thấy`, `nhìn`, `show`
- Example: "đây nè... thấy không" / "đó là... nhìn nè" → punch zoom tại điểm deictic

### Layer 3: Product detail mention (lexical match)

Detect product-nouns trong range text → zoom để show chi tiết:
- Lenspen: "đầu chổi", "carbon fiber", "sợi carbon", "chổi lông"
- Ốp Pocket 3: "ốp", "ron", "body", "ngăn", "lỗ"
- Body mist: "chai", "vòi xịt", "nắp"

## 3 Loại zoom (technical implementation)

### Slow zoom (USP/DETAIL ranges)
- Type: linear interpolation toàn range
- Scale: 1.0 → 1.25x (25% zoom in)
- FFmpeg: `zoompan=z='1.0+0.25*on/(d-1)':d=N:s=1080x1920:fps=30`
- Phù hợp: range dài > 3s, show technical detail

### Punch zoom (verbal cue + product detail)
- Type: 1.0 → peak → hold → 1.0
- Scale: peak 1.4x (~40% zoom)
- Phases: 30% zoom in + 40% hold + 30% zoom out
- FFmpeg: expression với `if(lt(on,N), expr1, if(lt(on,M), peak, ...))`
- Phù hợp: USP reveal, comparison result, emotion peak

### Static zoom (lock 1 moment)
- Type: scale locked ở 1.3x, không animation
- Dùng khi: hold 1 image 1-2s (product close-up)
- FFmpeg: `scale=1.3x, crop`

## Architecture Pipeline (FIXED anti-pattern)

### Anti-pattern: filter_complex toàn keep ranges

Lần đầu em code zoom trong filter_complex 1 lệnh duy nhất → TIMEOUT 300s vì:
- 5 segments × zoompan filter phức tạp
- zoompan xử lý N frames × scale operation = O(N²)
- Concat demuxer fail do moov atom không tìm thấy

### Pattern ĐÚNG: render per-segment, concat demuxer -c copy

```
1. Loop qua keep_plan.keeps
   ├── Nếu có zoom_plan match → render segment với zoompan filter
   └── Nếu không → render HARD CUT (scale+crop+setpts)
2. Concat demuxer (-c copy) → không re-encode, nhanh, không bug
3. Apply speed 1.3x lên concat output
4. Verify: TikTok spec + transcript clean
```

**Lý do concat demuxer OK ở đây:** Tất cả segments đã được re-encode với cùng codec/resolution/fps ở step 1 → -c copy stream copy an toàn. Nếu segments khác resolution/fps thì PHẢI dùng filter_complex.

## Test recipe đã verified (clip_0095)

```bash
# 1. Detect zoom plan
python3 scripts/detect_zoom_moments.py clip_0095
# Output: tmp/clip_0095/zoom_plan.json
# Ví dụ: USP → slow zoom, VS_KHAN → punch zoom

# 2. Render segments riêng (zoom hoặc hard cut)
# Code ở test_zoom_clip_0095.py đã verified end-to-end

# 3. Concat demuxer
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy pre_speed.mp4

# 4. Speed 1.3x
ffmpeg -y -i pre_speed.mp4 -filter_complex "[0:v]setpts=PTS/1.3[v];[0:a]atempo=1.3[a]" \
    -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 -pix_fmt yuv420p -r 30 \
    -c:a aac -b:a 192k -ar 44100 final.mp4

# 5. Verify
ffprobe -show_entries format=duration,stream=width,height,codec_name sample.mp4
ffmpeg -i final.mp4 → extract audio → Whisper recheck → scan lặp/false_start
```

## Pitfalls đã catch (zoom pipeline)

### PITFALL: zoompan timeout (26/07 clip_0095)
- Single filter_complex với zoompan cho mỗi segment × concat demuxer fail
- Fix: render per-segment riêng → concat -c copy
- Reference: test_zoom_clip_0095.py

### PITFALL: concat demuxer "moov atom not found"
- Stream copy KHÔNG tạo moov atom nếu input đã đúng codec
- Workaround: re-encode step trước concat (đã làm ở pipeline trên)

### PITFALL: zoom scale quá lớn (1.5x+)
- 1.5x zoom sẽ crop nhiều, có thể cắt mặt/SP khỏi frame
- Recommended max: 1.4x cho punch zoom, 1.25x cho slow zoom
- Verify visually bằng extract frame tại frame 30/60/90

## Workflow preference từ anh (FIRST-CLASS)

> Anh Tuấn Anh verbatim 26/07: "Test trước đi, nếu được thì mới patch vào skill"

Workflow BẮT BUỘC khi add feature mới vào skill:
1. **Test trên 1 clip thực tế** (tạo tmp test script, render → verify visual + transcript)
2. **Báo cáo kết quả** cho anh (file size, duration, visual frames, transcript clean)
3. **Anh duyệt** (A) hay không (B) mới patch skill
4. **Patch skill** nếu OK (vĩnh viễn)
5. **Không patch** nếu fail (không spam half-broken features vào skill)

KHÔNG BAO GIỜ patch skill trước khi test. KARMA: "Hurry → ship broken skill → mọi clip sau bị ảnh hưởng".

## Cross-references

- Main skill: `tiktok-video-editor` v0.06
- Script: `scripts/detect_zoom_moments.py`
- Test artifact: `/tmp/test_zoom_clip_0095.py`
- Verification protocol: PITFALL #57 (transcript-first), PITFALL #75 (`set -e` exit code), PITFALL #76 (inline Python heredoc)

## Kết quả clip_0095 verification (26/07)

| Metric | V2 ship | With zoom | Pass? |
|---|---|---|---|
| Duration | 81.2s | 81.2s | ✅ |
| TikTok spec | 1080×1920 30fps | 1080×1920 30fps | ✅ |
| File size | 47.0MB | 36.5MB (-22%) | ✅ |
| False start | 0 | 0 | ✅ |
| Lặp liền kề | 0 | 0 | ✅ |
| Zoom visual | N/A | Frame 1→4 gradual scale + punch visible | ✅ |
