---
name: tiktok-competitor-deep-analysis
title: TikTok Competitor DEEP Analysis (50-clip stratified)
description: Deep competitor analysis on TikTok using stratified sampling of 50+ clips (not just 4 viral). Includes yt-dlp format selector pitfalls, Whisper cached model workaround, TikTok audio-only detection, and VLM error handling. Use when user says "truy cập kênh X, xem TẤT CẢ video, rút bài học, tái cấu trúc" with sample size > 20.
created: 2026-06-16
updated: 2026-06-16
type: skill
tags: [tiktok, research, competitor-analysis, deep-research, viral-content, workflow]
confidence: high
relationships: [tiktok-viral-script, default-project-hub-pattern, video-download-yt-dlp, youtube-transcript-extractor]
---

# TikTok Competitor DEEP Analysis (50-clip stratified sampling)

Class-level skill for deep competitor analysis on TikTok. Use when user says "truy cập kênh X, xem TẤT CẢ video, rút bài học, tái cấu trúc" — the "DEEP" version requires stratified sampling (50+ clips) instead of "4 viral clips only".

## When to use

Trigger when user says any of:
- "review ít nhất 50 clip" / "phân tích sâu"
- "xem tất cả video" / "phân tích toàn bộ kênh"
- "tái cấu trúc project dựa trên kênh X"
- "rút bài học từ kênh X"
- Specifically mentions a sample size > 20

Do NOT use for:
- "phân tích video này" (single video) → use `tiktok-viral-script` workflow
- 4 viral clip only → use the simpler `competitor-u40hoc-xaykenh-analysis.md` reference

## ⚠️ HARD RULE (2026-06-16): Sample size minimum

**4 clip viral KHÔNG đủ để rút pattern.** User đã sửa em khi phân tích 4 clip viral:
> "review ít nhất 50 clip cho anh! 4 clip viral nhất chưa phản ánh hết được phong cách nội dung của kênh này"

**Quy tắc:**
- Mặc định: **stratified sampling 50 clip** (10 viral + 10 trung bình + 10 reply + 10 mới nhất + 10 random)
- Lý do: 4 viral chỉ thấy 1 phần pattern → sai lầm (VD: em nói "CTA provoke" là pattern #5, nhưng 50 clip cho thấy CTA phổ biến nhất là "specific action" 42%, provoke chỉ 4%)
- Nếu user yêu cầu sample lớn hơn (100+ hoặc tất cả 158): chạy batch parallel, chấp nhận ~1-2 tiếng

## Workflow: 50-clip DEEP analysis

### Step 1: Metadata (ALL videos)
```bash
yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(duration_string)s|%(view_count)s|%(timestamp)s" \
  "https://www.tiktok.com/@USERNAME" > /tmp/username-all-metadata.txt
```
- View count + duration + timestamp cho mọi video
- Sort by view_count → biết top viral + median + distribution
- View distribution: ≥1M, ≥100K, ≥50K, ≥10K, ≥1K, ≥0

### Step 2: Stratified sampling (Python script)
```python
import random
random.seed(42)

# Sort by views
videos.sort(key=lambda x: x['views'], reverse=True)

# 1. Top 10 viral
top10 = [v['id'] for v in videos[:10]]

# 2. 10 trung bình (10K-50K, exclude reply)
mid_pool = [v for v in videos if 10000 <= v['views'] < 50000 and not v['is_reply']]
random.shuffle(mid_pool)
mid10 = [v['id'] for v in mid_pool[:10]]

# 3. 10 reply (most viewed)
replies = [v for v in videos if v['is_reply']]
replies.sort(key=lambda x: x['views'], reverse=True)
reply10 = [v['id'] for v in replies[:10]]

# 4. 10 mới nhất
videos_by_date = sorted([v for v in videos if v['timestamp'] > 0],
                       key=lambda x: x['timestamp'], reverse=True)
newest10 = [v['id'] for v in videos_by_date[:10]]

# 5. 10 random (exclude already chosen)
chosen = set(top10 + mid10 + reply10 + newest10)
remaining = [v for v in videos if v['id'] not in chosen]
random.shuffle(remaining)
random10 = [v['id'] for v in remaining[:10]]

# Total: 50
```

### Step 3: Download 50 videos (BATCH + format selector)
```bash
# Format selector that works for both video+audio AND audio-only TikTok files:
yt-dlp -S "res:540,ext:mp4:m4a" -o "u50-${vid}.mp4" \
  "https://www.tiktok.com/@user/video/${vid}"
```

**⚠️ Format selector pitfall:**
- ❌ `-f h264_540p_805128-0` — hardcoded ID fails for videos with different format IDs
- ❌ `-f audio` — TikTok doesn't have standalone audio stream
- ✅ `-S "res:540,ext:mp4:m4a"` — soft selection, works for all TikTok files

**⚠️ TikTok audio-only pitfall (2026-06-16):**
Some TikTok files (17/50 in our test) are "audio-only" — the video stream contains just a static image + voice track. yt-dlp downloads them as MP4 with audio track only (no video stream). When you try to extract frames with ffmpeg → "Output file does not contain any stream".

**Detection:**
```bash
ffprobe -v error -select_streams v -show_entries stream=codec_type -of csv=p=0 video.mp4
# Returns "video" or nothing (audio-only)
```

**Workaround:** These are intentional TikTok slideshows (text overlay + voice). Skip frame extraction for them. Use transcript text only.

### Step 4: Extract audio + Transcribe (PARALLEL)
```bash
# Extract audio from all 50
for f in u50-*.mp4; do
  vid=$(basename "$f" .mp4)
  ffmpeg -y -i "$f" -ar 16000 -ac 1 -c:a pcm_s16le "/tmp/${vid}.wav" 2>/dev/null
done

# Transcribe with mlx_whisper (cached local)
# Run 3 in parallel to balance speed vs OOM
for f in u50-*.wav; do
  vid=$(basename "$f" .wav)
  if [ ! -f "/tmp/${vid}-transcript.txt" ]; then
    mlx_whisper --model mlx-community/whisper-large-v3-mlx \
      --output-format txt --output-name "/tmp/${vid}-transcript" "$f" > /dev/null 2>&1 &
    while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 0.5; done
  fi
done
wait
```

**⚠️ Whisper model selection (2026-06-16):**
- ❌ `mlx-community/whisper-small` — Repository Not Found (401)
- ❌ `mlx-community/whisper-base` — same error
- ✅ `mlx-community/whisper-large-v3-mlx` — cached local in `~/.cache/huggingface/hub/`, works 100%

### Step 5: Visual analysis (SKIP if audio-only)
```bash
# Extract 1 frame at second 1 (when first has talking content)
for f in u50-*.mp4; do
  vid=$(basename "$f" .mp4)
  if ! ffmpeg -y -i "$f" -vf "select=eq(n\,15),scale=320:-1" -vframes 1 "/tmp/${vid}-frame-1.jpg" 2>/dev/null; then
    # Try at second 1 instead
    ffmpeg -y -i "$f" -ss 1 -frames:v 1 "/tmp/${vid}-frame-1.jpg" 2>/dev/null
  fi
done
```

**⚠️ VLM API pitfall (2026-06-16):**
- ❌ `vision_analyze` — "No models loaded" error (LMS not configured)
- ✅ `mcp_MiniMax_understand_image` — works
- ⚠️ VLM có thể trả về "1033 system error" intermittently — retry 1 lần hoặc skip frame đó

### Step 6: Analysis pipeline (text-based, since most analysis is from transcripts)
```python
# Hook pattern analysis (Python regex on first 1000 chars)
hook_patterns = {
    'cau_hoi': r'(Sao|Tại sao|Vì sao|Thế nào|Thế.*\?|Bạn.*\?|Có.*\?)',
    'phu_dinh': r'(Đừng|Đừng bao giờ|Đừng có|Sai lầm|Không nên|Tránh)',
    'top_X': r'(Top \d+|\d+ cách|\d+ lỗi|\d+ mẹo|\d+ thứ|\d+ bí kíp|\d+ bước)',
    'tinh_nang_an': r'(Tính năng ẩn|Bí mật|Mẹo ẩn|Hidden)',
    'reply_user': r'(Replying|@)',
    'analogy': r'(cũng giống|cũng như|như là|cũng giống như|ví dụ như)',
    'cta_specific': r'(Hãy|Nhớ|Thử|Dùng|Làm theo)',
    'cta_provoke': r'(Còn bạn|Thế nên mọi người|Bạn vẫn đang)',
}

# Count + cross-tabulate by stratum (viral vs medium vs reply vs new vs random)
# Also analyze: duration vs views, word count vs views, content categories, CTA patterns
```

**Key finding patterns:**
- Hook frequency: which pattern appears most in viral vs other strata?
- Sweet spots: word count, duration — bucketed and avg view
- CTA: specific action vs provoke vs social proof
- Reply template: lặp lại format cố định?

### Step 7: Honest reporting (HARD RULE)
- ✅ Báo cáo thẳng thắn: bao nhiêu file audio-only, bao nhiêu frame VLM lỗi
- ✅ Sửa sai lầm cũ: nếu phát hiện pattern #5 đã viết sai, ghi rõ "Sửa lại từ file 04"
- ✅ Giới hạn confidence: "Sample 50/158 = 32% — chưa đủ đại diện hoàn toàn"
- ✅ Chỉ ra data hạn chế: transcript sai ~5-10%, VLM lỗi, etc.

## Time budget (50 clips)
- Download: 5-10 phút (50 video × ~5s = ~4 phút parallel)
- Audio extract: 1-2 phút
- Whisper transcribe: 20-30 phút (50 × ~30s parallel, 3 at a time)
- Frame extract: 1-2 phút
- VLM analysis: 10-15 phút (50 calls × ~15s)
- Text analysis: 5-10 phút
- **Total: 45-70 phút**

## Deliverable structure

### File naming
- `04-phan-tich-N-clip-V2-DEEP.md` (in project root)
- Cite: Sample size, confidence, source, hạn chế

### Sections
1. **Thiết kế nghiên cứu** — sampling strategy + data thu thập
2. **Thống kê mẫu** — view distribution, format, duration, word count
3. **Hook pattern analysis** — by stratum
4. **Content categories** — pillar distribution
5. **Duration vs Views** — sweet spot
6. **Word count vs Views** — sweet spot
7. **CTA pattern** — specific action vs provoke vs social proof
8. **So sánh 50 clips vs 4 clips viral** — sửa sai lầm cũ
9. **Visual setup** — limited data caveat
10. **Bài học lõi (CẬP NHẬT)** — sửa nếu sai
11. **Reply video pattern** — lặp lại format cố định?
12. **Đề xuất cập nhật project** — thay thế bài học sai
13. **Hạn chế nghiên cứu (TRANSPARENCY)** — báo cáo thẳng thắn
14. **Kịch bản "Ngày 1" sẵn sàng** — gợi ý outline (KHÔNG viết chi tiết nếu user chọn đợi review)

## Pitfalls (NEW 2026-06-16)

### ⚠️ 1. Sample size < 20 = sai pattern
- 4 video viral chỉ cho thấy 25% pattern → sai lầm trong bài học #5
- 50 video = đủ cho stratified 5×10
- 158 video = toàn bộ, ~2 tiếng

### ⚠️ 2. Format selector hardcoded
- `-f h264_540p_805128-0` — fails for videos with different format IDs
- Dùng `-S "res:540,ext:mp4:m4a"` cho tất cả TikTok

### ⚠️ 3. Audio-only TikTok files
- 17/50 video chỉ có audio (slideshow)
- `ffmpeg -vf "select=eq(n)"` fails với "Output file does not contain any stream"
- Detection: `ffprobe -select_streams v -show_entries stream=codec_type`
- Workaround: skip frame extraction, dùng transcript only

### ⚠️ 4. Whisper model not cached
- `mlx-community/whisper-small` returns 401
- Dùng `mlx-community/whisper-large-v3-mlx` (cached in `~/.cache/huggingface/hub/`)

### ⚠️ 5. VLM API lỗi intermittent
- `mcp_MiniMax_understand_image` có thể trả 1033 system error
- Retry 1 lần, nếu vẫn lỗi → skip frame đó
- Ghi rõ "X frame lỗi API" trong report

### ⚠️ 6. Sửa sai lầm cũ PHẢI ghi rõ
- Nếu file 04 cũ nói pattern X, file V2 nói pattern Y (đúng)
- Phải ghi: "Sửa lại: Bài học #5 (CTA provoke) — em đã SAI, đúng là 'specific action'"
- Không xóa — sửa + cite evidence

### ⚠️ 7. Kịch bản "Ngày 1" — HỎI trước khi viết
- Sau khi phân tích xong, gợi ý outline
- **KHÔNG viết chi tiết nếu user chọn option "B: đợi review"**
- Chờ user confirm

## Example: 50-clip @u40hoc.xay.kenh (2026-06-16)

**Data collected:**
- 50/50 video downloaded
- 48/50 transcripts (1 silent, 1 missing)
- 31/50 frames (17 audio-only)
- ~50 phút tổng thời gian

**5 phát hiện MỚI quan trọng:**
1. Hook CÂU HỎI phổ biến nhất 52% (không phải Tính năng ẩn)
2. Sweet spot 150-179 từ + 60-69s = view 2.37M avg
3. Reply template lặp lại: "Thử bán X bằng video ngắn, mọi người xem có muốn mua không"
4. CTA "specific action" 42% (KHÔNG phải provoke) — SỬA sai lầm cũ
5. TikTok slideshow (audio-only) = format phổ biến thứ 2

**Bài học rút ra (cập nhật):**
- Từ 4 video viral: "CTA provoke" (SAI)
- Từ 50 video: "CTA specific action" (ĐÚNG)

## Related

- `tiktok-viral-script` — Parent skill. This skill is the DEEP version of competitor analysis.
- `default-project-hub-pattern` — Quality bar 13/06 + voice rules
- `video-download-yt-dlp` — yt-dlp format selector pitfalls
- `youtube-transcript-extractor` — Whisper fallback pattern
- `references/competitor-u40hoc-xaykenh-analysis.md` — Simpler 4-clip version (legacy, still useful for quick checks)
