---
name: telegram-video-analysis
title: Analyze Video User Sent via Telegram
description: When Tuấn Anh sends a video file (screen recording, downloaded clip, etc.) via Telegram attachment, find the binary in Downloads, convert HEVC→H.264, extract frames + audio, run vision model + Whisper analysis, package summary video, and resend with structured insights. Use when user asks "phân tích từng frame", "analyze this video", or shares a video file expecting visual + audio breakdown.
created: 2026-06-16
updated: 2026-06-16
type: skill
tags: [video, analysis, telegram, vision, whisper, ffmpeg, frame-extraction, transcription]
confidence: high
related_skills:
  - video-download-yt-dlp
  - youtube-transcript-extractor
  - tiktok-competitor-deep-analysis
---

# Telegram Video Analysis Workflow

When Tuấn Anh sends a video file (screen recording, downloaded clip, etc.) via Telegram attachment, he expects the agent to "see" the video and give a detailed breakdown. This skill covers the end-to-end pipeline: **detect binary → convert codec → extract frames + audio → analyze → package → resend**.

## Why this workflow matters

**Critical constraint:** The Hermes Telegram gateway only passes text and links to the agent — **it does NOT pass binary attachments.** When the user sends a video file, the agent must:

1. **Find** the binary file in `~/Downloads/` (Telegram Desktop auto-downloads to `~/Downloads/Telegram Desktop/`)
2. **Convert** the codec (iPhone screen recordings default to HEVC, which vision models can't always read)
3. **Analyze** both visual frames and audio track
4. **Resend** the file via `MEDIA:/path` in `send_message` — the user expects to receive the video back in chat, not just a description

This is the **opposite workflow** of `video-download-yt-dlp` (link → download → resend). This one is **binary in `~/Downloads` → analyze → resend**.

## Standard Pipeline (7 Steps)

### Step 1: Find the Video Binary

Telegram Desktop on macOS auto-downloads attachments to `~/Downloads/Telegram Desktop/`. Generic downloads go to `~/Downloads/`.

```bash
# Priority 1: Telegram Desktop folder (newest first)
ls -lat "/Users/tuananh4865/Downloads/Telegram Desktop/" | head -10

# Priority 2: Recent downloads anywhere
ls -lat ~/Downloads/ | head -15

# Most recent video (filter to .mp4/.mov, sort by mtime)
stat -f "%Sm %N" -t "%Y-%m-%d %H:%M:%S" \
  /Users/tuananh4865/Downloads/Telegram\ Desktop/*.mp4 \
  /Users/tuananh4865/Downloads/*.mp4 \
  /Users/tuananh4865/Downloads/*.mov 2>/dev/null | sort -r | head -5
```

**Heuristic to pick the right file:**
- Screen recording → filename pattern `ScreenRecording_*.MP4` (uppercase ext)
- Downloaded video → `VIDEO_ID.mp4` or platform-specific naming
- If user just said "video này" without context → pick the most recent file < 100MB

**Sanity check with ffprobe** before doing anything else:
```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_type,codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 FILE_PATH
```

**Expected outputs for common sources:**
| Source | Codec | Resolution | Audio | FPS |
|--------|-------|------------|-------|-----|
| iPhone screen recording | HEVC + AAC | 1320×2868 (portrait) | AAC | 60 |
| TikTok downloaded | H.264 + AAC | 1080×1920 | AAC | 30 |
| YouTube Shorts | H.264 + AAC | 1080×1920 | AAC | 30/60 |
| macOS screen recording | H.264 + AAC | 2560×1440 (or scaled) | AAC | 60 |

### Step 2: Convert Codec if Needed (HEVC → H.264)

Vision models (including `mcp_MiniMax_understand_image` and most VLMs) handle HEVC inconsistently. **Always convert to H.264** for reliability.

```bash
# Working dir
mkdir -p /tmp/frame-analysis
cd /tmp/frame-analysis

# Convert: scale to 720p wide, H.264, AAC audio, faststart for streaming
ffmpeg -i "INPUT.mp4" \
  -vf "scale=720:-2" \
  -c:v libx264 -preset fast -crf 28 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  compressed.mp4 -y
```

**Why these settings:**
- `scale=720:-2` — width 720, height auto (preserves aspect ratio, `-2` ensures even number for codec)
- `crf 28` — visually fine for analysis, dramatically reduces file size (~10x)
- `preset fast` — speed/quality balance
- `movflags +faststart` — moves moov atom to start, critical for Telegram delivery
- `-c:a aac` — preserves audio, format whisper can decode

**Expected compression:** iPhone 17s 32MB HEVC → ~2.9MB H.264 720p. 90%+ size reduction.

### Step 3: Extract Frames @ 1fps

```bash
ffmpeg -i compressed.mp4 -vf "fps=1" frame_%03d.jpg -y
```

**Frame count for common durations:**
- 10s video → 10 frames
- 17s video → 17 frames
- 60s video → 60 frames
- 3 min video → 180 frames (too many — bump to `fps=1/2` for half rate)

**Frame naming:** `frame_001.jpg`, `frame_002.jpg`... lexicographic sort = temporal order.

**For long videos (>2 min), sample sparsely:**
```bash
# Every 10 seconds
ffmpeg -i compressed.mp4 -vf "fps=1/10" frame_%03d.jpg -y

# Specific time points (e.g., 0, 30, 60, 90s)
ffmpeg -i compressed.mp4 -ss 0 -vframes 1 frame_001.jpg -y
ffmpeg -i compressed.mp4 -ss 30 -vframes 1 frame_030.jpg -y
```

### Step 4: Vision Model Analysis

**Parallel calls for speed.** Group frames into batches of 5.

```python
# Pseudo-code — call mcp_MiniMax_understand_image in parallel
frames_to_analyze = ["frame_001.jpg", "frame_002.jpg", "frame_003.jpg", ...]

# Use consistent prompt template
prompt = """Mô tả chi tiết frame này: Bố cục, text trên màn hình, UI elements, 
màu sắc chủ đạo, hành động đang xảy ra. 
Nếu là TikTok/Instagram/video social thì ghi rõ username, caption, số view/like.
Nếu là app thì ghi rõ app nào, màn hình gì."""
```

**Sampling strategy:**
- **First 5 frames (intro):** Catch the hook, opening text, brand reveal
- **Middle frames:** Find action changes, scene transitions
- **Last 3-5 frames (outro):** Catch CTA, end-screen, final state
- **Always analyze at least 8-10 frames** for short videos (<60s)

**Key signal: differences between frames.** If frames 1 and 17 are identical, the video is essentially a static image. Note this. If frame 8 differs significantly → that's the pivot point.

### Step 5: Audio Extraction + Whisper Transcription

```bash
# Extract audio stream as-is
ffmpeg -i compressed.mp4 -vn -acodec copy audio.aac -y

# Convert to Whisper-friendly WAV (16kHz mono)
ffmpeg -i audio.aac -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
```

**Transcribe with mlx-whisper (Apple Silicon optimized):**
```bash
mlx_whisper audio.wav \
  --model mlx-community/whisper-small-mlx \
  --language vi \
  --output-format txt \
  --output-name transcript
```

**Model selection:**
- `whisper-small-mlx` — fast, decent Vietnamese, ~460MB
- `whisper-medium-mlx` — better accuracy, ~1.5GB, slower
- `whisper-large-v3-mlx` — best accuracy, ~3GB, slowest

**Language:** Default to `--language vi` for Tuấn Anh's content. For English/other, omit `--language` for auto-detect.

**Why audio matters:** Many videos have voice-overs, music with lyrics, or sound effects that frame analysis misses. Always transcribe — it's a 30-second step that often reveals critical content.

### Step 6: Package Summary Video

For a self-contained deliverable, combine all frames + audio into a single summary video:

```bash
ffmpeg -framerate 1 -i frame_%03d.jpg -i audio.wav \
  -c:v libx264 -preset fast -crf 28 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -shortest \
  -vf "scale=540:-2" \
  -movflags +faststart \
  summary.mp4 -y
```

**Output:** ~800KB-2MB for typical analysis, fits Telegram easily.

**When NOT to package summary:**
- User only asked for analysis (text-only deliverable)
- Video > 5 minutes (summary video would be unwieldy)
- User is on data-constrained connection (file size matters)

### Step 7: Resend via Telegram

Use `send_message` with `MEDIA:/path` syntax:

```python
send_message(
  action="send",
  target="telegram",  # or specific topic
  message="""Anh ơi, em tải được video rồi! Đây là **Screen Recording TikTok** 17 giây...

**📹 Video gốc (đã convert HEVC→H.264, 2.9MB):**
MEDIA:/tmp/frame-analysis/compressed.mp4

**🎬 Summary 17 frames + audio:**
MEDIA:/tmp/frame-analysis/summary.mp4

---

## 🔍 PHÂN TÍCH CHI TIẾT

[structured analysis here]

### Engagement
| Metric | Value |
|--------|-------|
| ❤️ Like | 78 |
| 💾 Save | 44 |

### 💡 Insights
- Bullet 1
- Bullet 2
"""
)
```

**Telegram limits:**
- Max file size: 50MB (bot) / 2GB (premium) — keep under 50MB to be safe
- Format: mp4 with H.264 + AAC is the safest
- `movflags +faststart` is critical for progressive playback

## Common Pitfalls

### 1. Telegram Desktop folder has spaces in path
**Triệu chứng:** `ls` errors with "No such file or directory"
**Fix:** Always quote the path: `"/Users/tuananh4865/Downloads/Telegram Desktop/"` hoặc escape space: `/Users/tuananh4865/Downloads/Telegram\ Desktop/`

### 2. HEVC files have uppercase `.MP4` extension
**Triệu chứng:** Glob `*.mp4` doesn't match iPhone screen recordings (`ScreenRecording_*.MP4`)
**Fix:** Search for both: `*.mp4` AND `*.MP4` AND `*.mov`

### 3. Vision model hits frame count limit
**Triệu chứng:** Error or slow response when sending 50+ frames at once
**Fix:** Batch into 5-7 frames per call. For long videos, use sparse sampling (`fps=1/5` or `fps=1/10`).

### 4. Audio is silent (no voice)
**Triệu chứng:** Whisper returns empty or just punctuation
**Interpretation:** Background music only, or visual-only content. Note in analysis. Don't force voice analysis.

### 5. Whisper model not downloaded yet
**Triệu chứng:** First run downloads 460MB+ model
**Fix:** Pre-download to `~/.cache/huggingface/hub/` or accept one-time 35s download.

### 6. Wrong video picked (multiple recent files)
**Triệu chứng:** User says "video này" but Downloads has 5 recent videos
**Fix:** Look at filename patterns. If ambiguous, ask user which one. Otherwise, pick newest + largest.

### 7. Vision model hallucinates details
**Triệu chứng:** Model describes "78 likes" but the screen actually shows 0
**Fix:** Cross-check critical numbers across multiple frames. Numbers in UI elements (likes, comments) should be consistent.

### 8. Sending 50MB+ files to Telegram
**Triệu chứng:** Timeout, upload fails
**Fix:** Always compress. `crf 28` is the sweet spot — visually fine, ~10x size reduction.

### 9. Video has no audio stream
**Triệu chứng:** `ffprobe` shows only video stream
**Fix:** Skip audio extraction. Note "no audio" in analysis. Use vision-only.

### 10. ffmpeg overwrites without warning
**Triệu chứng:** Accidentally re-running commands destroys prior work
**Fix:** Always use `-y` flag explicitly. Use unique output paths per session: `/tmp/frame-analysis-$(date +%s)/`.

### 11. User asks for motion analysis but you only did frame analysis
**Triệu chứng:** User says "phân tích chuyển động" or "tạo prompt video tương tự" — these need motion timeline, pose sequence, camera analysis
**Fix:** Detect trigger phrases ("chuyển động", "movement", "pose", "góc máy", "replicate", "bắt chước", "tạo prompt video"). Extract dense frames @ 2fps, run ffmpeg scene_score, build pose sequence map. See Step 8 + Step 9.

### 12. Vision model misspeaks pose details on similar-looking frames
**Triệu chứng:** Multiple frames analyzed all return "front stance" — but the user wants to know what's different
**Fix:** Use the structured pose prompt template (Step 8c) that forces per-limb analysis with delta comparison. Cross-check with ffmpeg scene_score to identify the actual motion peaks, then focus detailed pose analysis on those specific frames.

### 13. Long video generates too many frames
**Triệu chứng:** 3-min video at 1fps = 180 frames, 2fps = 360 frames → analysis takes forever
**Fix:** Switch to sparse sampling (every 5-10s) for >2min videos. For motion analysis specifically, use `fps=1/2` or `fps=1/5` instead of 2fps.

### 14. Vision model doesn't see motion (only static frames)
**Triệu chứng:** User asks "tại sao cô ấy di chuyển tay?" but frame analysis shows hand in same place
**Fix:** Vision models analyze ONE frame at a time — they can't see motion. Always combine frame analysis with `ffmpeg scene_score` (Step 8b) for actual motion data. The frame deltas (motion bursts) tell you WHEN motion happens, not just WHERE.

### 15. AI video prompt is too generic
**Triệu chứng:** User pastes prompt into Veo 3/Kling, gets video that doesn't match the original
**Fix:** Always include: (1) specific pose sequence with TIMESTAMPS, (2) exact camera angle + movement, (3) micro-motion intensity ("mostly 2-3 inch movements, no large gestures"), (4) lighting direction + color temp. Use the 3-template system in Step 9a.

## Sample End-to-End Command (17s TikTok screen recording)

```bash
# 1. Find file
FILE="/Users/tuananh4865/Downloads/ScreenRecording_06-16-2026 12-51-06_1.MP4"
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_type,codec_name,width,height \
  -of default=noprint_wrappers=1 "$FILE"
# → codec_name=hevc, width=1320, height=2868, duration=17.04, size=32MB ✓

# 2. Convert
mkdir -p /tmp/frame-analysis && cd /tmp/frame-analysis
ffmpeg -i "$FILE" -vf "scale=720:-2" -c:v libx264 -preset fast -crf 28 \
  -c:a aac -b:a 128k -movflags +faststart compressed.mp4 -y
# → 2.9MB ✓

# 3. Extract frames
ffmpeg -i compressed.mp4 -vf "fps=1" frame_%03d.jpg -y
# → 17 frames @ ~50KB each

# 4. Extract audio
ffmpeg -i compressed.mp4 -vn -acodec copy audio.aac -y
ffmpeg -i audio.aac -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y

# 5. Transcribe (mlx-whisper downloads model on first run)
mlx_whisper audio.wav --model mlx-community/whisper-small-mlx \
  --language vi --output-format txt --output-name transcript
# → "Tạm biệt!" detected

# 6. Package summary
ffmpeg -framerate 1 -i frame_%03d.jpg -i audio.wav \
  -c:v libx264 -preset fast -crf 28 -pix_fmt yuv420p \
  -c:a aac -b:a 128k -shortest -vf "scale=540:-2" \
  -movflags +faststart summary.mp4 -y
# → 815KB ✓

# 7. Vision analysis (parallel mcp_MiniMax_understand_image calls)
# Then send via Telegram with structured insights
```

## Output Deliverables

A complete analysis produces 3-5 things:

1. **`compressed.mp4`** — the original video, codec-normalized (always resend this so user has the file)
2. **`summary.mp4`** — frames stitched with audio, compact self-contained package (resend if user wants)
3. **Text analysis** — structured breakdown in chat
4. **Motion analysis** (optional, see Step 8) — when user asks about "chuyển động", "movement", "pose", or "tạo prompt video tương tự"
5. **Video AI prompt** (optional, see Step 9) — when user wants to replicate the video with Veo 3 / Kling / Runway / etc.

**When to send what:**
- Always send `compressed.mp4` (user expects to receive the video back)
- Send `summary.mp4` only if user asked for compact package or video is long
- Always send text analysis with: metadata table, frame-by-frame description, engagement metrics (if social media), actionable insights
- Send motion analysis + AI prompt ONLY when user explicitly asks for "phân tích chuyển động" or "tạo prompt video tương tự"

## Step 8: Motion Analysis (When User Asks "Phân tích chuyển động")

**Trigger phrases:** "phân tích chuyển động", "analyze movement", "pose analysis", "góc máy", "tạo prompt video tương tự", "bắt chước hành động", "replicate this video"

### 8a. Dense Frame Extraction @ 2fps

For motion analysis, 1fps is too sparse. Extract 2fps for short videos:

```bash
cd /tmp/frame-analysis
ffmpeg -i compressed.mp4 -vf "fps=2" -q:v 2 dense_frame_%03d.jpg -y
# 17s video → ~34 dense frames
```

### 8b. ffmpeg Scene Score (Motion Detection)

Detect motion bursts between consecutive frames using `lavfi.scene_score`:

```bash
ffmpeg -i compressed.mp4 -vf "select='gte(scene\,0)',metadata=print" -an -f null - 2>&1 | grep "scene_score"
```

**Interpretation:**
- Score `0.000-0.005` = near-static (micro-motion only)
- Score `0.020-0.045` = medium motion (body sway, hand raise, pose change)
- Score `0.060-0.080` = peak motion (clear action like "tay chạm ngực", turn, step)
- Pattern: alternating static (hold pose) + burst (transition) = rhythmic posing

**What to look for:**
- Periodic peaks every 0.25s = rhythmic body sway (matching music beat)
- Single high peak = key signature pose
- Decreasing scores near end = "settle" pose with zoom in

### 8c. Pose Analysis Prompt Template

For each key frame, use this structured prompt with vision model:

```
Phân tích motion frame này trong timeline. Tôi cần biết CHÍNH XÁC:
1. Body pose (đứng thẳng, nghiêng trái/phải, xoay bao nhiêu độ, weight trên chân nào)
2. Tay trái (vị trí: eo, bụng, đùi, buông thõng; ngón tay: duỗi/co; cầm gì)
3. Tay phải (cầm điện thoại che mặt ở vị trí nào, cao/thấp, xoay bao nhiêu)
4. Đầu & mặt (nghiêng, cúi, ngẩng; điệu bộ)
5. Vai & hông (thẳng hay lệch, mở rộng hay thu)
6. Chân (dáng đứng, bước rộng/hẹp)
7. Camera angle (góc từ dưới lên/ngang/từ trên; khoảng cách; zoom/dolly)
8. Lighting (ánh sáng từ hướng nào, shadow ở đâu)
9. Frame này khác frame trước ở điểm nào? (motion delta)

Trả lời cực ngắn: POSE: ... | TAY_T: ... | TAY_P: ... | ĐẦU: ... | VAI: ... | CHÂN: ... | CAM: ... | LIGHT: ... | DELTA: ...
```

**Sample key frames for short videos:** 1, 3, 8, 12, 15, 18, 22, 28, 34 (cover intro, peak, settle)

### 8d. Build Pose Sequence Map

Group similar poses into "Pose States" (Pose A, B, C...):

```markdown
| Time | Pose | Description |
|------|------|-------------|
| 0-3s | Pose A | Front stance, hand at side |
| 3-5s | Pose B | "Tay chạm ngực" signature |
| 5-12s | Pose C | Body sway + hand at side |
| 12-15s | Pose D | S-curve, hand at waist |
| 15-17s | Pose E | Settle + slow zoom in |
```

This becomes the script for the AI video prompt.

## Step 9: Video AI Prompt Generation (For Replicate)

**Trigger:** User wants to "bắt chước", "tạo video tương tự", "replicate", or asks for a prompt to use in Veo 3 / Kling / Runway / Sora.

### 9a. Three Prompt Templates

Always generate 3 versions:

**Template 1: Full Detailed Prompt (Veo 3 / Kling 2.0+)**
```python
prompt = f"""A young Asian woman, 20-25, [SCENE DESCRIPTION] in [LOCATION].

CAMERA: [Angle, distance, movement, frame type]

POSE SEQUENCE (0-{duration}s):
- 0-Xs: [Pose A description]
- X-Ys: [Pose B description]
- ...

MOTION: [Speed, intensity, character of movement]

LIGHTING: [Direction, color temp, shadows]

STYLE: [Aesthetic, target platform, format]

FORMAT: {duration}s, {fps}fps, {aspect_ratio}, [platform] aesthetic.
"""
```

**Template 2: Compact (for tools with token limits)**
```python
prompt = f"""[Subject] [action] in [location]. [Camera]. [Pose sequence]. [Lighting]. {duration}s, {fps}fps, {aspect_ratio}."""
```

**Template 3: Image-to-Video (when user has reference image)**
```python
prompt = """SUBJECT: [Upload reference image]
MOTION: [Step-by-step pose sequence from 8d]
CAMERA: [From analysis]
STYLE: [From analysis]
MOTION_INTENSITY: [Low/Medium/High]"""
```

### 9b. Replicate Checklist Output

Always include a checklist the user can use to shoot the original:

```markdown
- [ ] Background: [Specific type — wooden wall, beige tone]
- [ ] Lighting: [Warm overhead diffuse, 2700-3000K]
- [ ] Camera: [Mirror selfie fixed, eye-level, tripod]
- [ ] Outfit: [Specific items]
- [ ] Pose sequence: [A → B → C → D → E with timings]
- [ ] Tempo: [2-3s/pose, slow graceful]
- [ ] Motion: [60% static + 40% micro-motion]
- [ ] Zoom: [Slow push-in 5-10% in final 2-3s]
- [ ] Duration: [15-20s sweet spot]
- [ ] Audio: [Music + brief voice overlay if any]
- [ ] Caption: [1-2 words, 3 hashtags]
- [ ] Shop tag: [TikTok Shop integration]
```

### 9c. Send Final Deliverables

Send a Telegram message with:
1. **Motion timeline** (table with pose states + timings)
2. **Camera analysis** (angle, distance, movement)
3. **Lighting analysis** (direction, color, shadow map)
4. **Full video prompt** (3 templates)
5. **Replicate checklist**

## Related Skills

- `video-download-yt-dlp` — for link-based video (YouTube/TikTok URLs)
- `youtube-transcript-extractor` — for transcript-only workflow (no visual analysis)
- `tiktok-competitor-deep-analysis` — for batch competitor analysis (50+ clips, not single video)
- `transcript-cleanup` — cleanup media files after analysis (saves disk)
- `tiktok-viral-script` — for writing scripts in Tuấn Anh's voice (combine with motion analysis)
