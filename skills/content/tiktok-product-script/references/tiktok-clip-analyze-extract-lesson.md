# TikTok Clip Analyze + Extract Lesson Workflow (v0.9.3, 21/07/2026)

> **When to use:** User gửi TikTok video URL + yêu cầu "phân tích" / "rút bài học" / "extract lessons" / "xem clip này" / "analyze video".
> **Verified case:** 21/07/2026 — clip @dungkenhnghiepdu (81s, dạy viết script bán hàng dùng Tripod Ulanzi case study) → 5 bài học → fix V2A/B/C MA66 ngay trong session.
> **Lesson file output:** `wiki/concepts/tiktok-clip-lesson-<handle>-YYYY-MM-DD.md`

## 6-STEP WORKFLOW (BẮT BUỘC)

### Step 1: Download video bằng yt-dlp

```bash
# Tạo folder theo ngày
LESSON_DIR="/Volumes/Storage-1/Hermes/scratch/tiktok-anh-tuan/lesson-$(date +%Y-%m-%d)"
mkdir -p "$LESSON_DIR"

# Download (TikTok short link resolve tự động)
yt-dlp --no-warnings -o "$LESSON_DIR/raw.%(ext)s" "<tiktok-url>"
```

**Output expected:** `raw.mp4` (1080×1920 vertical, HEVC hoặc H264).

### Step 2: Extract audio 16kHz mono

```bash
ffmpeg -y -i "$LESSON_DIR/raw.mp4" -vn -acodec pcm_s16le -ar 16000 -ac 1 "$LESSON_DIR/audio.wav"
```

**Why 16kHz mono:** Whisper medium model yêu cầu sample rate 16kHz, mono tiết kiệm 50% size.

### Step 3: Whisper transcript (KHÔNG dùng large-v3)

```bash
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir "$LESSON_DIR" "$LESSON_DIR/audio.wav"
# Output: audio.txt (transcript text thuần)
```

**CRITICAL — không dùng `large-v3-mlx`:** Large-v3 hallucinate trên tiếng Việt khi audio silent/unclear → loop lặp câu 60s+. Medium-mlx clean hơn nhiều. Codified in SOUL.md.

### Step 4: Extract 5-8 frames ở các thời điểm chiến lược

```bash
mkdir -p "$LESSON_DIR/frames"
# Pick timestamps evenly spread qua duration
TIMES=(2 8 15 25 35 50 65 78)
for i in "${!TIMES[@]}"; do
  t=${TIMES[$i]}
  ffmpeg -y -ss "$t" -i "$LESSON_DIR/raw.mp4" -vframes 1 -q:v 2 "$LESSON_DIR/frames/frame_${i}_t${t}s.jpg"
done
```

**Pick timestamps based on video duration:**
- 30-60s video: 4 frames (t=2, 15, 30, 50)
- 60-120s video: 6-8 frames (t=2, 8, 15, 25, 35, 50, 65, 78)
- 120s+ video: 8-10 frames evenly spread

### Step 5: MẮT + TAI cross-verify

```python
# Visual analysis (MẮT) — dùng vision_analyze trên 2-3 frames
from hermes_tools import vision_analyze
for frame in ["frame_00_t002s.jpg", "frame_03_t025s.jpg", "frame_07_t078s.jpg"]:
    vision_analyze(
        image_url=f"{LESSON_DIR}/frames/{frame}",
        question="Mô tả cảnh: người nói, sản phẩm, text overlay, hành động."
    )

# Audio analysis (TAI) — đọc transcript đã Whisper
with open(f"{LESSON_DIR}/audio.txt") as f:
    transcript = f.read()
```

**Cross-verify:** Nếu transcript nói "sản phẩm A" mà visual thấy "sản phẩm B" → DỪNG, không extract lesson cho đến khi resolve. Anti-pattern (case 19/07 clip_0004): Whisper báo "Doroto" nhưng visual là OTOBOP → em build sai 2 versions trước khi verify.

### Step 6: Viết bài học + apply vào scripts hiện có

**Save lesson file:** `wiki/concepts/tiktok-clip-lesson-<handle>-YYYY-MM-DD.md`

**Template structure:**
```markdown
---
title: Bài học viết script từ clip @<handle> - <topic>
created: YYYY-MM-DD
type: lesson
source: <tiktok-url>
duration: <Xs>
applies-to: tiktok-product-script v0.X+, mọi sản phẩm lifestyle
confidence: high
---

# 🎓 Bài học viết script TikTok — Từ clip @<handle>

## 📋 TÓM TẮT CLIP
- Người nói: <handle>
- Format: <type>
- Sản phẩm minh hoạ: <product>
- Hook vấn đề: <first 5s quote>

## 🎯 N BÀI HỌC CỐT LÕI
### Bài học 1: <title>
**Quote:** "<verbatim từ clip>"
**Áp dụng cho script hiện có:**
- ❌ Sai: <old pattern>
- ✅ Đúng: <new pattern>

### Bài học 2-5: ...

## 🔧 SO SÁNH SCRIPTS HIỆN CÓ vs NGUYÊN TẮC CLIP
| Bài học | Script hiện có | Verdict |
|---|---|---|

## 📝 SCRIPT CẢI TIẾN (áp dụng N bài học)
### Version A cải tiến: ...

## ✅ CHECKLIST VIẾT SCRIPT MỚI (áp dụng N bài học)
- [ ] ...

## 📂 RELATED FILES
- <link tới script đang có trong wiki>
```

**Apply vào scripts hiện có:**
1. Identify scripts trong `wiki/projects/tuan-anh-review-tiktok/scripts/` có vấn đề tương tự
2. Patch từng script (KHÔNG ghi đè V1, save V2 mới nếu cần)
3. Verify với checklist đã liệt kê trong lesson file
4. Báo cáo cho user: "đã fix X file, cụ thể Y→Z"

## ANTI-PATTERNS (FAIL cases)

| Anti-pattern | Tại sao sai | Fix |
|---|---|---|
| Chỉ "xem qua rồi tóm tắt vài dòng" trong chat | Mất 80% giá trị, không có file để apply | PHẢI save lesson file đầy đủ |
| Download nhưng không transcribe | Chỉ có visual, không có nội dung chính xác | LUÔN extract audio + Whisper |
| Apply lesson vào tất cả scripts cùng lúc | Over-applied, có thể sai context | Apply 1 script/đợt, verify, rồi mới sang cái tiếp |
| Bỏ qua step cross-verify (mắt + tai) | Transcript có thể sai (Whisper vs visual) | LUÔN cross-verify trước khi extract lesson |

## HOOK WORD-COUNT CHO CLIP SCRIPT

Nếu user yêu cầu "viết script giống clip này" hoặc "theo phong cách clip X":
- Hook ≤12 từ (tiếng Việt) hoặc ≤8 từ (tiếng Anh) — gate đã codified
- Mỗi version anchor 1 nhu cầu duy nhất (PITFALL v0.9.2)
- Văn nói đời thường, KHÔNG từ hoa mỹ (TONE rule v0.9.1)

## CROSS-REFERENCE

- PITFALL v0.9.2 trong SKILL.md (mỗi video 1 nhu cầu) — lesson này chính là nguồn gốc v0.9.2
- TONE rule v0.9.1 trong SKILL.md (văn nói đời thường) — apply khi viết script mới theo clip
- Case study v0.9.1: `references/ulanzi-ma66-problem-solution-case-study.md` (script fix sau khi apply lesson)
- Lesson file thực tế: `wiki/concepts/tiktok-script-lesson-from-ulanzi-clip-2026-07-21.md` (10.3KB)

## CHECKLIST TRƯỚC KHI SHIP

- [ ] Video đã download vào `/Volumes/Storage-1/Hermes/scratch/tiktok-anh-tuan/lesson-YYYY-MM-DD/raw.mp4`
- [ ] Audio đã extract 16kHz mono
- [ ] Whisper transcript đã save vào `audio.txt`
- [ ] 5-8 frames đã extract
- [ ] Vision analysis đã chạy trên 2-3 frames
- [ ] Transcript + visual đã cross-verify (không có conflict)
- [ ] Lesson file đã save vào `wiki/concepts/tiktok-clip-lesson-<handle>-YYYY-MM-DD.md`
- [ ] Lesson file có: N bài học + quote verbatim + so sánh scripts hiện có + script cải tiến + checklist
- [ ] Scripts hiện có đã patch theo lesson (nếu applicable)
- [ ] Báo cáo cho user: paths files + diff cụ thể

---

*Reference file created 21/07/2026 from session analyzing clip @dungkenhnghiepdu. Codify workflow để future session có thể reproduce khi user gửi TikTok URL + yêu cầu phân tích.*