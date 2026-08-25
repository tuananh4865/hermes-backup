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
- "phân tích top N video thịnh hành" (sample size 10-30 — see NEW Tier 2 below)
- Specifically mentions a sample size > 20

**NEW TIER 2 (2026-06-26) — Compact 10-30 sample for focused asks:**
When user says "top 10/20 video" or "top trending" (not "all videos" / "ít nhất 50"), use compact workflow:
1. Fetch all metadata via `yt-dlp --flat-playlist` (cheap, fast, no download yet)
2. Sort by view_count desc → take top N (where N matches user request)
3. Download top 5-8 ONLY for transcript extraction (enough to identify pattern)
4. Single-pass analysis (no need for stratified sampling if sample = top views only)
5. Deliver: top-N table + pattern analysis + universe/character reuse insights

Use this when:
- User asks for "top 20 trending" specifically (focused ask, not exhaustive)
- Channel has 50-150 videos (manageable)
- User wants to derive a TEMPLATE/UNIVERSE for own content (not just learn from one channel)

See `references/karmavid-herocat2309-case-study-2026-06-26.md` for the full KarmaVid project case where this tier was used.

Do NOT use for:
- "phân tích video này" (single video) → use `tiktok-viral-script` workflow
- 4 viral clip only → use the simpler `competitor-u40hoc-xaykenh-analysis.md` reference

## ⚠️ HARD RULE (2026-06-16): Sample size minimum

**4 clip viral KHÔNG đủ để rút pattern.** User đã sửa em khi phân tích 4 clip viral:
> "review ít nhất 50 clip cho anh! 4 clip viral nhất chưa phản ánh hết được phong cách nội dung của kênh này"

---

## 🎬 EXTENSION 2026-07-18: Motion Graphic Pattern cho TikTok Product Clip (Verified từ V22)

Khi user yêu cầu **motion cho clip TikTok product affiliate** (như clip_0003 Dodoto Lux Air V3 trong `/Volumes/Storage-1/Pocket3/Hermes-Edit/`), apply theo layout benchmark V22 đã verified PASS bằng mắt thật.

### Layout Benchmark Vertical TikTok 1080×1920 (V22 - PASS verified 17/07/2026)

**Source clip:** 1728×3072 (4K iPhone, 29.97fps, H.264 High 10, 10-bit yuv420p10le)
**Composition output:** 1080×1920 portrait, 30fps, H.264 High 8-bit, AAC 128kbps

**Vị trí glass card chuẩn (9 phase):**

| Phase | Element | Position | Size |
|---|---|---|---|
| HOOK | hook-glass | top: **1308px**, left/right: 80px | full-width × auto |
| PROBLEM | problem-glass | top: **1288px**, left/right: 80px | full-width × auto |
| CHART (crop) | pip-wrap | top: 80px, left: 80px | **420×420** |
| CHART | chart-glass | top: **720px**, left/right: 80px | full-width × auto |
| STAMP | stamp-glass | top: 50%, rotate -8deg | center |
| PRODUCT | product-glass | top: **1288px**, left/right: 80px | full-width × auto |
| PORT (crop) | pip-wrap | top: 80px, left: 80px | **420×420** |
| PORT | port-glass | top: **680px**, left/right: 80px | full-width × auto |
| USP | usp-glass | top: **1308px**, left/right: 80px | full-width × auto |
| CTA-FINAL | cta-big-glass | top: 192px, bottom: 192px | **80% khung hình** |

**Liquid glass recipe chuẩn:**
```css
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(40px) saturate(180%);
border: 1.5px solid rgba(255, 255, 255, 0.32);
border-radius: 32px;
box-shadow: 0 12px 36px rgba(0, 0, 0, 0.45);
```

### HyperFrames CLI workflow (CRITICAL)

**Theo skill `~/.hermes/skills/hyperframes-core/references/variables-and-media.md`:**

1. `<video>`/`<audio>` phải là **DIRECT CHILD** của host root - KHÔNG wrap trong div
2. KHÔNG gọi `video.play()` trong code - **HyperFrames owns playback**
3. Timeline PHẢI là **paused + tl.seek(0)**:
```js
[videoBg, pipChart, pipPort].forEach(v => v.pause());  // PAUSE pattern
const tl = gsap.timeline({ paused: true });
// ... add tweens
window.__timelines[COMPOSITION_ID] = tl;
tl.seek(0);  // seek to start
```

### Animation timing chuẩn

- Fade in: **0.6s** ease `back.out(1.5)`
- Fade out: **0.4s** linear
- Phase gap: **≥0.3s** (USP fade out + CTA fade in)
- Bar fill: **1.2s** `power1.out`

### 8 HARD RULES (verified qua 22 versions)

1. **BOTTOM glass che cằm** → Phase thường KHÔNG nên BOTTOM, chỉ TOP (Y=1288-1308)
2. **Glass trong phase crop** sai vị trí → Phase crop cần PIP + glass ngang hàng
3. **Padding 56px** (TikTok safe zone left) KHÔNG phải 80px+
4. **Caption bar đè lên chart** → bỏ caption bar
5. **Animation timing overlap** → USP fade out + CTA fade in cách ≥0.3s
6. **Liquid glass opacity = 0.15** (sweet spot, KHÔNG 0.08/0.18)
7. **Phase crop dùng infographic/text**, KHÔNG dùng glass card
8. **Watermark "@tuancuaban" + "ANH ĐANG NÓI"** label = NOISE, bỏ hết

### 3 SAI LẦM CẦN TRÁNH (lesson từ clip 0003 motion V4/V5/V6 17/07/2026)

1. **❌ Đặt glass card `bottom: 200px`** → phải dùng `top: 1308px` (Y=1308 chứ KHÔNG bottom)
2. **❌ Glass card quá nhỏ** (font 24-44px) → scale lên 48-72px để đọc rõ
3. **❌ Background video tưởng bị đơ nhưng thật ra source clip là talking head gần như STATIC** → trước khi report "video đơ", verify motion bằng pixel diff ở vùng KHÔNG có glass overlay (vì GSAP animation tạo motion giả ở vùng glass)

### Wiki Product Ground Truth Rule (NEW 2026-07-17)

Khi viết content cho sản phẩm TikTok Shop affiliate:
- Mọi claim/spec/giá phải có **citation [N]** map về nguồn verified (brand site, Shopee, Wikipedia, official)
- KHÔNG tự suy đoán specs/giá/brand
- Wiki research cache: `wiki/projects/tuan-anh-review-tiktok/products/*.md` (đã verified)
- Reference skill: `~/.hermes/skills/wiki-product-ground-truth/SKILL.md`

### Layout Benchmark file location

File đầy đủ 19.8KB lưu tại 2 vị trí:
- `/Volumes/Storage-1/Hermes/wiki/projects/content-creator/layout-benchmark-vertical-tiktok-1080x1920.md` (gốc)
- `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/layout-benchmark-vertical-tiktok-1080x1920.md` (copy)

Anh nào muốn làm motion cho clip dọc TikTok → đọc benchmark này trước, dùng layout V22 đã verified.

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

**⚠️ TikTok VIDEO-only pitfall (NEW 2026-06-22) — FIXED 2026-06-22:**

⚠️ **SỬA SAI LẦM 2026-06-22:** Pitfall này initially được viết với workflow SAI (vision-only). Thực tế kiểm tra kỹ: khi `ffprobe` thấy file TikTok MP4 chỉ có HEVC video stream (NO audio), nguyên nhân KHÔNG PHẢI là "TikTok intentionally strips audio" — mà là **yt-dlp chọn sai format variant** trong lúc download.

**Detection đúng:**
```bash
ffprobe -v error -show_streams -of json FILE.mp4 | python3 -c "
import sys, json
d = json.load(sys.stdin)
streams = d.get('streams', [])
video = [s for s in streams if s.get('codec_type') == 'video']
audio = [s for s in streams if s.get('codec_type') == 'audio']
print(f'video={len(video)}, audio={len(audio)}')
"
# Nếu video=1, audio=0 → REDOWNLOAD với format đúng, KHÔNG làm vision-only
```

**Root cause + Fix (đúng):**
- TikTok CDN trả về format `bytevc1_*_0` (variant -0) là VIDEO ONLY — chỉ HEVC stream, không có audio track bundled
- Format `bytevc1_*_1` (variant -1) hoặc `download` (watermarked) LUÔN có cả audio+video bundled
- `yt-dlp -F` liệt kê cả hai nhưng default `bestvideo+bestaudio` hoặc `--audio-multistreams` merge KHÔNG reliable với TikTok

**Workflow SỬA LẠI khi phát hiện VIDEO-only:**
```bash
# ❌ SAI: Vision-only analysis với 8 frames + caption overlay (lãng phí + thiếu transcript)
# ✅ ĐÚNG: Redownload với format có audio, sau đó Whisper transcript

# Step 1: Redownload với format có audio bundled
yt-dlp -f "download" -o "FIXED-VIDEO_ID.%(ext)s" "https://vt.tiktok.com/XXX/"
# Hoặc explicit variant -1
yt-dlp -f "bytevc1_1080p_982660-1" -o "FIXED-VIDEO_ID.%(ext)s" "URL"

# Step 2: Verify audio có
ffprobe -v error -show_streams FIXED-VIDEO_ID.mp4 | grep codec_type
# → phải thấy cả "video" và "audio"

# Step 3: Whisper transcript (force vi)
ffmpeg -i FIXED-VIDEO_ID.mp4 -ar 16000 -ac 1 /tmp/VIDEO_ID.wav
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi /tmp/VIDEO_ID.wav
```

**Khi nào vision-only VẪN đúng (case thật):**
- TikTok slideshow thật (ảnh tĩnh + voice overlay) — file vẫn có audio, em sai khi assume không có audio
- Video TikTok đã bị user manually strip audio trước khi upload — case hiếm
- Video chỉ có nhạc nền + caption overlay (KHÔNG có voice) — đây là case vision-only hợp lệ

**Detection trước khi conclude VIDEO-only:**
```bash
# Step 1: Check `yt-dlp -F URL` list có bao nhiêu format với ACODEC != "aac"
yt-dlp -F URL | grep -E "^[a-z0-9_-]+\s+mp4.*aac" | wc -l
# ≥ 4 → có nhiều variant có audio, download variant -1 hoặc "download"

# Step 2: User explicitly nói "có voice nói đàng hoàng" → KHÔNG BAO GIỜ conclude VIDEO-only
# Đây là HARD RULE — user đã sửa em 2 lần vì lỗi này
```

**LESSON LEARNED 2026-06-22 (CRITICAL — ghi nhớ kỹ):**
- ❌ KHÔNG assume "video không có audio" chỉ dựa trên 1 lần ffprobe
- ❌ KHÔNG phân tích visual frames thay thế khi user yêu cầu TRANSCRIPT voice
- ✅ LUÔN check `yt-dlp -F` TRƯỚC khi download TikTok
- ✅ LUÔN dùng `-f "download"` cho TikTok (an toàn nhất)
- ✅ Verify audio presence SAU KHI download trước khi conclude
- ✅ Nếu user nói "có voice" → tìm MỌI CÁCH lấy audio (try multiple format variants, check TikTok API, ask user for original file)

## 🚨 Meta-lesson (Tuấn Anh's correction 2026-06-22)

User feedback: *"Anh không muốn em hứa suông, anh muốn có lesson learn"*

When user corrects you with a strong signal (frustration, repeated correction, "lần này phải...", etc.):
- ❌ Don't promise "lần sau sẽ làm tốt hơn" without saving a real lesson
- ❌ Don't just say "em xin lỗi" and move on
- ✅ Save concrete artifact: patch this skill + add reference doc + memory entry with prevention checklist
- ✅ Reference doc MUST include: root cause, what user actually said (verbatim), prevention rules with checkboxes

A vague promise is a missed learning opportunity. A concrete skill patch + reference doc = the same mistake never repeats.

Xem chi tiết session 22/06 tại `references/session-2026-06-22-caocuongvuai-transcript.md` để hiểu rõ hơn về flow lỗi → sửa.

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

### ⚠️ 8. NEW 2026-06-26 — Detect channel language BEFORE Whisper

When analyzing a foreign TikTok channel, **detect language from titles/metadata FIRST**, then set `--language` flag accordingly.

**Real case (@herocat2309, 2026-06-26):**
- Channel is English-language (titles: "The strawberry girl was kicked out...")
- Initial blind `--language vi` would have produced gibberish transcripts
- Fix: read 3-5 random titles from metadata, identify dominant language, set Whisper flag

**Detection quick check (before downloading):**
```bash
# After flat-playlist metadata fetch, sample titles:
yt-dlp --flat-playlist --print "%(title)s" "URL" 2>/dev/null | head -10
# If 90%+ titles are in language X → set `--language X`
```

**Common channel language patterns:**
- Animation/food story channels (China-export style): **English** (Broccoli/Strawberry/Apple girl)
- VN TikTok Shop/affiliate: **Vietnamese**
- K-beauty/J-beauty: **Korean** or **Japanese**
- Mexican/Hispanic viral: **Spanish**
- Manga/animation reaction: **English** or **Japanese**

**⚠️ Whisper flag matters more than model choice** — `large-v3-mlx` works for all languages, but `--language vi` forces Vietnamese output regardless of input. If input is English, you get hallucinated Vietnamese garbage.

### ⚠️ 9. NEW 2026-06-26 — Voice-over emotion amplification: "X" repeated 30+ times

When analyzing transcripts, count repeated phrases. **Repetition = emotion amplification pattern**:

| Pattern | Example | Effect |
|---------|---------|--------|
| **Pain amplification** | "I'm sorry. (×30+ in last 30s)" | Trigger viewer empathy, increase watch time |
| **Stoic suffering** | "It's fine. It's fine. It's fine." | Generate "I feel you" response |
| **Countdown to climax** | "5... 4... 3... 2... 1..." | Build tension |
| **Call-and-response** | "Are you OK?" → "I'm OK." → repeat 5x | Hook viewer into rhythm |

**Discovery (2026-06-26 @herocat2309):**
- Top 1 video (120.7M views) ends with "I'm sorry" repeated 30+ times
- Pattern = "I'm sorry. I'm sorry. I'm sorry..." (one every ~1s)
- Music slows down, visual holds on crying face
- Viewers BINGE until karma happens (cliffhanger + emotion)
- Common in 60%+ of top 20 transcripts

**Apply to user's own scripts:**
- When writing climax/miserable moment, use REPETITION instead of complex sentences
- Example: "Em xin lỗi. Em xin lỗi. Em xin lỗi..." (3-5 times, slow pacing)
- Pair with: slow music + zoom on face + music drop at end
- ❌ Don't write complex dialogue in climax: "Em xin lỗi vì đã không nghe lời mẹ..."
- ✅ DO write: "Em xin lỗi. Em xin lỗi. Em xin lỗi." (let emotion + visual carry)

**When to count repetitions in analysis:**
```bash
# Count repeated phrases in transcripts
grep -oE "I'm sorry\." transcript.txt | wc -l
# If count > 5 → flag as emotion amplification pattern
```

### ⚠️ 10. NEW 2026-06-26 — Universe/Character reuse detection (multi-series channels)

When channel has 5+ videos reusing same characters (same names appear in titles), it's a **UNIVERSE channel**, not a one-off channel. Flag for special analysis.

**Detection:**
```bash
# Count character mentions in titles
yt-dlp --flat-playlist --print "%(title)s" "URL" 2>/dev/null | \
  grep -oiE "strawberry girl|apple man|onion girl|banana man" | sort | uniq -c | sort -rn
# If any character name appears 5+ times → universe channel
```

**Universe channel analysis pattern:**
1. **Identify main characters** (from title frequency)
2. **Map series** — find Part 1, Part 2, Part 3 of each character
3. **Track journey arc** — what happens to character across parts?
4. **Identify recurring villains** — who opposes the main characters?
5. **Spot common locations** — what settings appear across episodes?

**Deliverable for universe channels:**
- Character bible (visual, personality, catchphrase, journey arc)
- Series roadmap (which character has how many parts)
- Crossover potential (which characters could meet)
- Universe rules (what's the worldbuilding logic?)

**Real case (2026-06-26 @herocat2309):**
- Channel has 3 main characters: strawberry girl (most), onion girl, watermelon mother
- Plus 5+ recurring: apple man, durian man, banana, broccoli, lemon man
- Series structure: Strawberry baby (3 parts), Onion girl (8+ parts), Watermelon (2+ parts)
- Villains often = family members (stepmother, husband, sibling)
- Setting: 1 consistent world, characters visit each other

**When to use this analysis:**
- User asks "phân tích top 20 + tạo công thức kịch bản + tạo universe"
- User wants to BUILD a similar channel (not just learn from one)
- Output includes: universe bible + character designs + template

**Don't use when:**
- User only wants hook/CTA patterns (single video analysis)
- Channel is variety content (no recurring characters)

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
- `youtube-transcript-extractor` — Whisper fallback pattern + TikTok format variant pitfall
- `references/session-2026-06-22-caocuongvuai-transcript.md` — Session 22/06 case study (TikTok video 7623055460836330772): user feedback, root cause analysis, 5 prevention rules
- `references/competitor-u40hoc-xaykenh-analysis.md` — Simpler 4-clip version (legacy, still useful for quick checks)
- `references/karmavid-herocat2309-case-study-2026-06-26.md` — Tier 2 (compact 20 sample) workflow + Universe channel detection + emotion amplification pattern + KarmaVid project setup. Verified 2026-06-26.
