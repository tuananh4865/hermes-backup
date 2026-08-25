---
name: telegram-video-analysis
title: Analyze Video User Sent via Telegram (single + batch)
description: When Tuấn Anh sends a video file (screen recording, downloaded clip, etc.) via Telegram attachment, find the binary in Downloads, convert HEVC→H.264, extract frames + audio, run vision model + Whisper analysis, package summary video, and resend with structured insights. Use when user asks "phân tích từng frame", "analyze this video", shares a video file expecting visual + audio breakdown, or sends N>1 videos at once with "transcript toàn bộ" — see scripts/batch-transcribe.py for batch mode.
created: 2026-06-16
updated: 2026-07-16
type: skill
tags: [video, analysis, telegram, vision, whisper, ffmpeg, frame-extraction, transcription, contact-sheet, style-deconstruction, recipe]
confidence: high
version: 1.2.0
changelog: 'v1.2.0 (16/07/2026): NEW Step 10 — Style Deconstruction + Reproducible Recipe. Trigger: anh hỏi "làm sao em làm được video dạng này" / "phân tích công thức" — pedagogical workflow KHÁC Step 8/9 (replicate pose). 3-stage sampling (1/6fps overview → 2s/frame labeled detail → 2fps dense optional). Contact-sheet workflow: build PIL grid montage → 2 vision calls only (instead of 33+). 6-section output format: look + timeline + AI parts + composite parts + sound + recipe. Real case: NousResearch hackathon promo 66s 2160×2160. v1.1.0 (25/06): batch-transcribe script + 16+ video batch mode.'
related_skills:
  - video-download-yt-dlp
  - youtube-transcript-extractor
  - tiktok-competitor-deep-analysis
---

# Telegram Video Analysis Workflow

When Tuấn Anh sends a video file (screen recording, downloaded clip, etc.) via Telegram attachment, he expects the agent to "see" the video and give a detailed breakdown. This skill covers the end-to-end pipeline: **detect binary → convert codec → extract frames + audio → analyze → package → resend**.

## Why this workflow matters

**Critical constraint:** The Hermes Telegram gateway only passes text and links to the agent — **it does NOT pass binary attachments.** When the user sends a video file, the agent must:

1. **Find** the binary file in `~/.hermes/cache/videos/` (gateway auto-cache for Telegram uploads — **Priority #1, check FIRST**), or fall back to `~/Downloads/Telegram Desktop/` or `~/Downloads/`
2. **Convert** the codec (iPhone screen recordings default to HEVC, which vision models can't always read)
3. **Analyze** both visual frames and audio track
4. **Resend** the file via `MEDIA:/path` in `send_message` — the user expects to receive the video back in chat, not just a description

This is the **opposite workflow** of `video-download-yt-dlp` (link → download → resend). This one is **binary in `~/.hermes/cache/videos/` → analyze → resend**.

**TRIGGER PHRASES that MUST load this skill FIRST (before asking the user for a link):**
- "Tải video này về"
- "Transcript video này"
- "Phân tích video"
- "Analyze this video"
- "Video em gửi"
- "Video anh gửi"
- Any request that references a video without providing a URL

When ANY of these fire, scan `~/.hermes/cache/videos/` BEFORE asking for a link. The binary is almost certainly already on disk.

## Standard Pipeline (7 Steps)

### Step 1: Find the Video Binary

**3 chỗ video có thể nằm** (priority order):

```bash
# Priority 1: Hermes gateway auto-cache (khi user gửi attachment qua Telegram chat)
ls -lat /Users/tuananh4865/.hermes/cache/videos/*.mp4 2>/dev/null | head -5

# Priority 2: Telegram Desktop folder (user đã click "Save" trong Telegram)
ls -lat "/Users/tuananh4865/Downloads/Telegram Desktop/" | head -10

# Priority 3: Generic Downloads (user manually save từ browser/email/etc)
ls -lat ~/Downloads/*.mp4 ~/Downloads/*.MP4 ~/Downloads/*.mov 2>/dev/null | head -10

# Most recent video (filter to .mp4/.mov, sort by mtime)
stat -f "%Sm %N" -t "%Y-%m-%d %H:%M:%S" \
  /Users/tuananh4865/.hermes/cache/videos/*.mp4 \
  /Users/tuananh4865/Downloads/Telegram\ Desktop/*.mp4 \
  /Users/tuananh4865/Downloads/*.mp4 \
  /Users/tuananh4865/Downloads/*.mov 2>/dev/null | sort -r | head -5
```

**Heuristic to pick the right file:**
- Screen recording → filename pattern `ScreenRecording_*.MP4` (uppercase ext)
- Downloaded video → `VIDEO_ID.mp4` or platform-specific naming
- If user just said "video này" without context → pick the most recent file < 100MB

**🔍 Advanced fallback: macOS Apple Menu → Recent Items (khi không tìm thấy file mới)**

Khi `ls ~/Downloads` không có file mới (ví dụ: Telegram chưa auto-download xong, hoặc user vừa mở file nhưng chưa save vào Downloads), em có thể query macOS Apple Menu → Recent Items để tìm file đã mở gần đây:

```python
computer_use(action="capture", app="Telegram", mode="som")
# → AXMenuBar / AXMenuItem entries liệt kê file names user đã open gần đây
# → Ví dụ: "Close-up_mirror_selfie_video_202606172230.mp4", "Mirror_selfie_upper_torso_202606172319.mp4"
```

Sau đó search path:
```bash
find /Users/tuananh4865/Documents /Users/tuananh4865/Desktop \
     /Users/tuananh4865/Downloads -type f -iname "Close-up*" 2>/dev/null
find ~ -type f -name "*mirror_selfie*" 2>/dev/null
```

**Use case:** Khi user gửi video Telegram nhưng em quét Downloads không thấy → trước khi kết luận "không có file", thử capture Apple Menu Recent Items qua computer_use.

**⚠️ CONFIRMATION GATE (Pitfall #19 — 2026-06-18, FIX):**

Khi user nói "video này", "transcript video", "phân tích video" — **KHÔNG tự pick file rồi chạy**. Em phải:

1. **List candidates** với metadata đầy đủ (mtime, size, codec, duration):
   ```bash
   for f in $(ls -t ~/Downloads/*.mp4 ~/Downloads/*.MP4 ~/Downloads/*.mov 2>/dev/null | head -3); do
     echo "=== $f ==="
     stat -f "mtime: %Sm | size: %z bytes" "$f"
     ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$f" 2>/dev/null
   done
   ```
2. **Hỏi user confirm** trước khi chạy whisper/ffmpeg:
   > "Em thấy 2-3 file video gần đây: [list với metadata]. Anh muốn em xử lý file nào?"
3. **CHỈ chạy pipeline sau khi anh pick**.

**EXCEPTION (2026-06-18):** Khi `~/.hermes/cache/videos/` có duy nhất 1 file với mtime trong session hiện tại (gateway vừa auto-cache user upload qua Telegram) → đó là file user vừa gửi, KHÔNG cần hỏi confirm. Cache path + mtime = unambiguous evidence. Pipeline chạy thẳng.

**Sai lầm cụ thể (18/06):** Anh nói "Transcript video này và phân tích". Em thấy `p7d0k_QDFhs.mp4` (4.4MB, 13/06) — tên trùng với URL YouTube anh share 17/06. Em assume đó là file mới → transcript → phân tích dài 27 cues về ReAct loop → anh nói "Em phân tích nhầm video rồi". Em quét lại mới phát hiện file `p7d0k_QDFhs.mp4` thực ra tải về từ 5 ngày trước, không có file video mới nào trong `~/Downloads` lẫn Telegram Desktop cache.

**Rule:** Filename trùng ≠ file mới. **mtime là source of truth**. Sort by `-lat` không phải by name.

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

## ⚠️ CRITICAL: Verify Before Recall (Pitfall #16 — 2026-06-18)

Khi user gửi link mà em đã có memory về session cũ (session_search hoặc memory note), **KHÔNG ĐƯỢC assume** link đó là video đã xử lý trước đó. Em phải verify metadata TRƯỚC KHI recall.

**Ví dụ sai (2026-06-18):** User gửi lại `https://youtu.be/p7d0k_QDFhs`. Em có memory từ 12/06 về batch 3 video (`OXXoI2MF-Gs` + `p7d0k_QDFhs` + TikTok Pocket tripod) trong project Content Creator. Em assumed luôn là video trong batch đó → trả lời sai. User phải nhắc "Không phải rồi, check lại đi".

**Fix:**
```bash
# ALWAYS run yt-dlp metadata check FIRST before recalling from memory
yt-dlp --skip-download --print "%(title)s | %(channel)s | %(duration_string)s | %(view_count)s views | %(upload_date)s" "URL"
```

**Rule:** Title + channel + duration phải match với memory TRƯỚC khi claim "em nhớ". Nếu KHÔNG match → nói "Em có memory về session cũ nhưng để em verify metadata trước" rồi mới recall.

## Common Pitfalls

### 0. mlx_whisper arg ordering
`mlx_whisper` yêu cầu FILE PATH là positional đầu tiên, flags sau. Sai thứ tự (`mlx_whisper --fp16 video.mp4`) sẽ parse filename vào --fp16 → error `invalid str2bool value: 'filename.mp4'`. Đúng: `mlx_whisper video.wav --model mlx-community/whisper-large-v3-turbo --language vi --output-dir DIR --output-format srt`.

### 0a. mlx_whisper PATH bug — 2 paths available, default broken (Pitfall #38 — 2026-06-18, FIX)

**Triệu chứng:** Chạy `mlx_whisper audio.wav --model ...` → bash error `/Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper: /Applications/Xcode.app/Contents/Developer/usr/bin/python3: bad interpreter: No such file or directory`.

**Nguyên nhân:** Có 2 mlx_whisper binary trên máy:
- `/Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper` — PATH đầu tiên, nhưng shebang broken point to Xcode python3 (đã uninstall Xcode CLT)
- `/Users/tuananh4865/whisper-env/bin/mlx_whisper` — PATH riêng có Python 3.11 đúng, **DÙNG CÁI NÀY**

**Fix chuẩn — luôn dùng full path:**

```bash
# ❌ FAIL (default PATH pick broken shebang)
/Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper audio.wav --model ...

# ✅ WORK (full path whisper-env)
/Users/tuananh4865/whisper-env/bin/mlx_whisper audio.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi \
  --task transcribe \
  --output-dir /tmp/transcript-XXX \
  --output-format srt
```

**Hoặc dùng python trực tiếp:**

```bash
/Users/tuananh4865/whisper-env/bin/python3 -m mlx_whisper audio.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi
```

**Performance:** 104s video transcribe trong ~30s với whisper-large-v3-mlx trên Apple Silicon (M1/M2).

**Diagnostic reflex khi gặp "bad interpreter":**

```bash
# Check shebang của binary đang gọi
head -1 $(which mlx_whisper)
# Nếu point đến Xcode CLT python3 đã uninstall → đổi sang whisper-env path
```

### 0b. Whisper idempotency + file selection
- LUÔN check `~/whisper-output/` trước khi chạy whisper — tránh re-transcribe video đã có SRT.
- `~/Downloads/*.mp4` có thể chứa file cũ nhiều tháng — sort theộng theo `-lat` để lấy file MỚI NHẤT đúng file anh vừa gửi.
- Whisper large-v3-turbo trên Apple Silicon: ~30-60s cho video 90s, timeout 180-240s đủ.
- Khi save transcript → SCHEMA: `raw/transcripts/YYYY-MM-DD/<video-id>-<channel>-<topic>.srt` (KHÔNG dùng raw/articles/).

### 0c. ⚠️ CRITICAL — Whisper hallucinate LOOP trên audio dài tiếng Việt (>5 phút) — dùng `--condition-on-previous-text False` + verify bằng short-segment re-transcribe (Pitfall #NEW 2026-06-26, FIX; v2 2026-06-30 dùng large-v3)

**Triệu chứng:** Whisper medium/mlx-community/whisper-medium-mlx transcribe audio 7 phút tiếng Việt → output JSON có 70+ segments lặp lại cùng 1 câu (e.g. "Các bạn có thể dùng cái góc này" × 72 lần từ 264s → 408s) — nhưng khi transcribe đoạn 30s riêng lẻ ở cùng range đó, output hoàn toàn khác (nội dung wrap-up + CTA thật).

**Root cause:** Whisper mặc định dùng `condition_on_previous_text=True` — khi transcribe audio dài, model sử dụng output của segment trước làm context cho segment sau. Nếu segment trước có chuỗi ngắn dễ lặp (như "Hãy đăng ký kênh" intro ở đầu), model sẽ **continue lặp pattern đó** thay vì transcribe nội dung thật → hallucinate toàn bộ phần giữa/cuối video.

**Fix BẮT BUỘC cho audio > 3 phút tiếng Việt:**
```bash
/Users/tuananh4865/whisper-env/bin/mlx_whisper audio.wav \
  --model mlx-community/whisper-medium-mlx \
  --language vi \
  --output-format json \
  --output-name transcript-clean \
  --condition-on-previous-text False   # ← QUAN TRỌNG
```

**Sai lầm cụ thể (2026-06-26, Ulanzi ChaiBot review clip):** Em transcribe 7 phút audio bằng default settings → thấy "Các bạn có thể dùng cái góc này" × 72 lần từ 264s → 408s. Em CUT phần đó dựa trên transcript. MAY MÀ verify bằng cách transcribe đoạn ngắn 264-408s riêng lẻ → nhận ra đó là wrap-up + CTA thật ("từ lúc mình mua nó về tới giờ mình không có tháo ra khỏi chiếc pocket 3... các bạn có thể bấm vào phía dưới để mua hàng"). Nếu KHÔNG verify → cắt nhầm phần quan trọng nhất của video.

**Workflow bắt buộc (5 bước):**
1. **Transcribe audio dài với `--condition-on-previous-text False`** để tránh hallucinate loop
2. **Sau khi có transcript, scan cho repeated segments** (`x > 5` ở cùng range) — đây là red flag hallucination
3. **Verify BẮT BUỘC bằng cách transcribe đoạn ngắn 30-60s** ở range bị suspect:
   ```bash
   ffmpeg -i audio.wav -ss <start> -to <end> -vn -ar 16000 -ac 1 -c:a pcm_s16le check.wav
   mlx_whisper check.wav --model ... --condition-on-previous-text False
   ```
4. **Nếu transcript đoạn ngắn KHÁC transcript đoạn dài** → transcript dài bị hallucinate, dùng transcript đoạn ngắn

**Trigger khi nghi ngờ hallucinate:**
- Output có 50+ segments liên tiếp với text giống hệt nhau
- Cùng 1 câu lặp lại > 10 lần
- Range bị lặp nằm ở GIỮA video (không phải intro/outro)
- Text lặp có cấu trúc đơn giản (5-10 từ) — easy to continue

**Quy tắc:** Audio > 3 phút tiếng Việt + Whisper medium → LUÔN dùng `--condition-on-previous-text False`. Verify suspect ranges bằng short-segment re-transcribe.

**NÂNG CẤP 2026-06-30: Dùng Whisper LARGE-V3 thay vì medium cho transcribe chính.** Khi xử lý video > 3 phút, chạy large-v3 ngay từ đầu thay vì medium + verify. Lý do:
- Medium vẫn hallucinate dù đã có `--condition-on-previous-text False` trong một số edge case (vd transcribe 0-61s thấy "Hãy đăng ký kênh" lặp ở 0s, 30s, 60s — hallucinate vì context bias)
- Large-v3 segment count 148 vs medium 94 (nhiều timing chi tiết hơn) → re-start detection chính xác hơn
- Performance: large-v3 cache warm = 75s cho 7 phút audio (acceptable)
- Model path: `/Users/tuananh4865/whisper-env/bin/mlx_whisper`

```bash
# Best practice cho video Việt > 3 phút (2026-06-30)
mlx_whisper audio.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi \
  --output-format json \
  --output-name transcript-large \
  --condition-on-previous-text False \
  --compression-ratio-threshold 2.0 \
  --no-speech-threshold 0.6 \
  --logprob-threshold -0.5
```

VẪN dùng short-segment verify nếu large-v3 cũng có range nghi ngờ (defense in depth).

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

### 16. MCP VLM rate limit + dual-API fallback (Pitfall #17 — 2026-06-18)

Khi phân tích video 90s+ (95 frames @ 1fps), MCP MiniMax VLM API dễ trả rate-limit error liên tục (Trace-Id `06827e...` pattern). Em retry 12 lần liên tiếp, chỉ 6/12 thành công.

**Fix pattern:**
1. **Sample sparse cho video >60s** — chọn 8-12 key frames (0, 5, 10, 20, 30, 45, 60, 75, 90, end) thay vì 1fps toàn bộ
2. **Delay 5-15s giữa các batch retry** — đợi rate limit reset trước khi retry frame tiếp
3. **Honest báo cáo**: "Em phân tích được N/12 frames, các frame còn lại dùng context từ transcript + frame lân cận để infer"
4. **Fallback chain**: MCP MiniMax (preferred) → `vision_analyze` (LM Studio local, cần load model trước) → describe dựa trên transcript
5. **NEVER fabricate visual details** cho frame không phân tích được — chỉ nói "chưa verify visual của frame X"

### 17. Vietnamese explainer videos (no talking head) — visual style template (Pitfall #18 — 2026-06-18)

Video AI/tech explainer kiểu Việt Nam (nhiều kênh: AI NEWS, tech insight, **La La School**, AI Vietnam, etc.) thường có pattern đặc trưng:

| Element | Typical value |
|---|---|
| Format | Motion graphic, no talking head |
| Background | Kem/be nhạt (off-white) |
| Accent color | Cam đậm (1 tông duy nhất) |
| Font | Sans-serif đậm, viết hoa cho tiêu đề |
| Icon | Vòng tròn + bánh răng (gear) = AI Agent |
| Animation | Icon chuyển động theo vòng tròn, dashed line arrow, text fade |

Khi gặp explainer video format này → categorize ngay là "AI/tech explainer", infer các frame chưa phân tích được dựa trên pattern. KHÔNG apply format talking head review cho video explainer.

**⚠️ CAVEAT (Pitfall #21 — 2026-06-18, FIX):** Pattern recognition ở trên giúp INFER visual style NHANH, nhưng KHÔNG được dùng để XÁC ĐỊNH tên kênh/brand. Nhiều kênh khác nhau dùng chung style này (AI NEWS, La La School, AI Vietnam, Dũng RV, etc.). Brand name PHẢI lấy từ **audio Whisper cue subscribe ở 3 cue cuối SRT**, không được guess từ visual.

**Rule:** "Visual familiarity ≠ brand identity". Cùng 1 style template có thể thuộc 5-10 kênh khác nhau. Whisper audio là ground truth cho brand.

### 19. Skills-First Protocol violation — picked file before loading skill (Pitfall #20 — 2026-06-18)

**Triệu chứng:** User nói "transcript video này và phân tích". Em jump thẳng vào action — `ls Downloads/`, pick file có tên quen (`p7d0k_QDFhs.mp4` trùng URL YouTube share trước đó), chạy whisper, viết 6-phần analysis dài → user phải nhắc "Em phân tích nhầm video rồi".

**Root cause:** Em skip Skills-First Protocol (Fable-5 mandate 2026-06-16):
- KHÔNG load `telegram-video-analysis` skill TRƯỚC khi xử lý
- KHÔNG verify file là mới (mtime) trước khi process
- KHÔNG confirm với user trước khi tốn tool calls + tokens

**Fix:**
1. **ALWAYS load skill trước** khi trigger phrase match ("video này", "transcript", "phân tích video", "analyze this")
2. **Run confirmation gate** (Step 1) — list candidates với metadata, hỏi user pick
3. **Verify mtime > current_session_start** — nếu file cũ hơn session hiện tại, KHÔNG tự động process
4. **Nếu user context hint có sẵn** (link, tên file chỉ định), dùng đúng file đó KHÔNG cần hỏi lại

**Rule:** 5 giây confirm với user > 5 phút xử lý sai file.

### 15. AI video prompt is too generic
**Triệu chứng:** User pastes prompt into Veo 3/Kling, gets video that doesn't match the original
**Fix:** Always include: (1) specific pose sequence with TIMESTAMPS, (2) exact camera angle + movement, (3) micro-motion intensity ("mostly 2-3 inch movements, no large gestures"), (4) lighting direction + color temp. Use the 3-template system in Step 9a.

### 33. Agent asked for URL when binary was already on disk (Pitfall #36 — 2026-06-22, FIX)

**Triệu chứng:** User nhắn "Tải video này về và transcript đi" (KHÔNG kèm link). Em jump thẳng sang hỏi "Anh gửi link cho em đi" — sai. User phản hồi "Anh gửi trực tiếp qua telegram mà" — frustrated.

**Root cause:** Em KHÔNG load skill `telegram-video-analysis` TRƯỚC khi phản hồi. Em KHÔNG nhận ra "video này" + "transcript" + KHÔNG có link = trigger phrase cho Telegram-attached video, không phải cho URL workflow.

**Sai lầm cụ thể (2026-06-22):**
- Em scan 4 paths SAI: `~/Downloads/`, `~/Downloads/Telegram Desktop/`, `~/Library/Application Support/Telegram Desktop/tdata/`, `~/.hermes/state.db` (query session DB tìm attachment)
- BỎ QUA Priority #1: `~/.hermes/cache/videos/` (gateway auto-cache)
- Em kết luận "không có file video mới" → sai
- Em default sang "Anh gửi link cho em" → khiến user phải hint 2 lần

**Fix — Workflow khi user nói "video này" mà KHÔNG kèm link:**

1. **STOP. Đừng hỏi link.**
2. **Scan `~/.hermes/cache/videos/` TRƯỚC TIÊN** (gateway auto-cache path — Pitfall #23)
3. **Mở rộng scan nếu cache trống:**
   - `~/Downloads/Telegram Desktop/` (Telegram Desktop auto-download)
   - `~/Downloads/*.mp4`, `*.MP4`, `*.mov`
   - Sort by mtime → newest first
4. **Filter candidates**: mtime > session_start_time, size > 1MB, extension .mp4/.mov
5. **List candidates với metadata đầy đủ** (mtime, size, duration via ffprobe)
6. **Hỏi user confirm** nếu có >1 candidate:
   > "Em thấy N video mới trong gateway cache / Downloads: [list với mtime + size + duration]. Anh muốn em xử lý file nào?"
7. **CHẠY pipeline** sau khi user confirm (hoặc nếu chỉ có 1 candidate duy nhất)

**Quy tắc tiên quyết:**
- "video này" mà KHÔNG có link → 95% là file binary user vừa gửi qua Telegram
- Default = scan `~/.hermes/cache/videos/` TRƯỚC, hỏi link SAU
- Nếu cache trống + Downloads trống + Telegram Desktop trống → MỚI hỏi user "anh gửi link hoặc file đính kèm giúp em"

### 34. Telegram Bot API 20MB RECEIVE limit — silent rejection (Pitfall #37 — 2026-06-24, FIX)

**Triệu chứng:** User gửi video qua Telegram. Gateway log có dòng:
```
WARNING [Telegram] Failed to cache video: File is too big
```
→ Bot API server-side từ chối ngay lập tức (silent), không gửi error về user. Agent không nhận được gì cả, không có message text, không có attachment. Nếu user không escalate, agent tưởng "user im lặng" hoặc "user gửi nhầm chat".

**Tripled-round deadlock thực tế (2026-06-24 12:58 → 13:09):**
- 12:58: User: "Cắt những khúc ựm ờ..." → agent báo "đã lưu xong" (false positive — không có file)
- 13:01: User: "Tìm cách xem và tải nội dung..." → agent lại báo "đã xử lý" (vẫn không có file)
- 13:03-13:07: User escalate: "ủa tại sao tao gửi video qua telegram mà mày không thấy?" → agent vẫn miss
- 13:09: User: "Tao chắc chắn mày chỉ đang đọc đầu vào tin nhắn của tele rồi!" → agent mới grep `gateway.log` → thấy `File is too big` → root cause

**Root cause:** Telegram Bot API có 2 hard limits cho file upload qua bot:
- **Download (getFile)**: 20 MB max
- **Upload (sendDocument/sendVideo)**: 50 MB max
File >20MB gửi qua bot → Bot API silent reject, gateway chỉ log warning, không bubble lên agent.

**Fix — Diagnostic reflex khi user nói "tôi vừa gửi video" mà agent không thấy:**

```bash
# 1. Check cache mtime (file mới hay không?)
ls -lat ~/.hermes/cache/videos/ | head -5

# 2. Grep gateway.log cho size-related errors GẦN ĐÂY (5 phút trước)
grep -E "File is too big|File is too large|Request Entity Too Large|413" \
  ~/.hermes/logs/gateway.log | tail -10

# 3. Nếu có hit → file đó bị silent reject
# → propose 2-3 fallback paths cho user:
#    a. Compress video (crf 28 → ~10x reduction) trước khi gửi
#    b. Upload lên Google Drive / Dropbox → share link
#    c. Upload YouTube unlisted → share link
#    d. Chia nhỏ video thành nhiều clip <20MB
```

**Quy tắc cứng:**
- Khi user báo "đã gửi" mà cache `~/.hermes/cache/videos/` trống + log có "File is too big" → file đó >20MB, server reject, KHÔNG phải lỗi agent
- Khi user báo "đã gửi" mà cache trống + log không có gì → có thể user gửi nhầm chat hoặc bot chưa nhận → hỏi lại
- **KHÔNG BAO GIỜ** báo "đã lưu xong" / "đã xử lý" khi không có file trên disk — đó là [[fabricated-completion-rule]] + [[telegram-video-20mb-limit]] cùng lúc

**Cross-reference:** Sibling cause với [[fabricated-completion-rule]] (tool return success ≠ ground truth) + macOS case-insensitive path trap (silent write failures). All 3 share shape: *agent claims success, ground truth disagrees, no error message*. See [[concepts/telegram-video-20mb-limit]] for full diagnostic playbook + Active-Checklist Phase 1 reflex integration.
- KHÔNG BAO GIỜ scan `~/.hermes/state.db` để tìm attachment metadata — agent message DB chỉ chứa TEXT content, không chứa binary blob reference

**Rule:** Trigger phrase + no URL = file-on-disk workflow. Mặc định scan `~/.hermes/cache/videos/` trước khi hỏi user bất cứ điều gì.

### 23. Telegram gateway auto-caches uploads to `~/.hermes/cache/videos/` (Pitfall #24 — 2026-06-18, FIX)

**Triệu chứng:** User gửi video qua Telegram, em scan `~/Downloads/` + `~/Downloads/Telegram Desktop/` không thấy file → em kết luận "không có video mới" → sai. User phải nhắc "Phải tải video từ telegram về thì mới có trong máy chứ".

**Root cause:** Khi user gửi file qua Telegram, Hermes gateway lưu binary vào `/Users/tuananh4865/.hermes/cache/videos/video_<8-char-hash>.mp4`. File này **KHÔNG xuất hiện trong `~/Downloads/`** trừ khi user tự save. Nếu user chỉ gửi attachment qua chat → chỉ có cache, không có Downloads copy.

**Fix — Scan 3 paths theo thứ tự ưu tiên:**

```bash
# Priority 1: Hermes gateway cache (NEWEST Telegram uploads)
ls -lat /Users/tuananh4865/.hermes/cache/videos/*.mp4 2>/dev/null | head -5

# Priority 2: Telegram Desktop folder (auto-download by user)
ls -lat "/Users/tuananh4865/Downloads/Telegram Desktop/" | head -10

# Priority 3: Generic Downloads (manually saved clips)
ls -lat ~/Downloads/*.mp4 ~/Downloads/*.MP4 ~/Downloads/*.mov 2>/dev/null | head -10
```

**Path pattern khi gateway lưu:**
- Format: `/Users/tuananh4865/.hermes/cache/videos/video_<8-char-hash>.mp4`
- Ví dụ: `video_68187dc488c1.mp4`
- Mtime là timestamp user vừa gửi (realtime, không phải ngày tải YouTube)

**Sai lầm cụ thể (2026-06-18):** Em scan 3 chỗ (Downloads, Telegram Desktop, iCloud) không thấy → kết luận sai. User phải hint "Phải tải video từ telegram về". Thực ra em đã có user_data gợi ý ở `~/Library/Application Support/Telegram Desktop/tdata/`, nhưng KHÔNG scan `~/.hermes/cache/videos/` (gateway auto-cache) — đây là path quan trọng nhất khi user gửi attachment trực tiếp qua chat.

**Rule:** Khi user gửi video qua Telegram attachment (không phải link YouTube/TikTok), **`~/.hermes/cache/videos/` là source of truth #1**. Nếu path này có file mới → đó là file user muốn, KHÔNG cần hỏi confirm.

### 24. "Phân tích nhầm" có 2 nghĩa — clarify intent (Pitfall #25 — 2026-06-18, FIX)

**Triệu chứng:** User nói "Em phân tích nhầm video rồi". Em assume = em pick sai FILE → đi scan lại filesystem tìm file mới. Nhưng thực ra = em pick ĐÚNG FILE nhưng phân tích SAI NỘI DUNG (hallucinate channel name "AI Daily News" thay vì "La La School" dù transcript audio nói rõ).

**Hai loại "nhầm" cần distinguish:**
1. **Nhầm FILE** — em xử lý file cũ/khá → fix: scan lại paths, tìm file mới đúng
2. **Nhầm NỘI DUNG** — em xử lý đúng file nhưng phân tích sai (hallucinate brand, misread visual, sai context) → fix: re-read transcript cue, re-analyze vision frames

**Fix — Khi user nói "phân tích nhầm":**
1. **ĐỪNG jump to conclusion** = "nhầm file"
2. **Hỏi explicit**: "Anh ơi, em hiểu 'nhầm' theo 2 cách: (a) em xử lý sai FILE, hay (b) em xử lý đúng FILE nhưng phân tích sai NỘI DUNG? Anh nói rõ giúp em để em fix đúng chỗ."
3. **Check both possibilities song song**:
   - FILE: re-scan `~/.hermes/cache/videos/` + Downloads với metadata mtime
   - CONTENT: re-read 3 cue cuối SRT cho brand name, re-check key visual frames

**Rule:** User correction càng ngắn = càng ambiguous. Khi user chỉ nói 1 câu mơ hồ, **clarify trước khi assume**. 30s hỏi > 5 phút xử lý sai hướng.

### 25. "Hút" = "Hook" — Vietnamese translation of script framework terms (Pitfall #26 — 2026-06-18, FIX)

**Triệu chứng:** Khi transcribe video kịch bản tiếng Việt, nhiều creator Việt (La La School, Hiếu Trần, etc.) **dịch các thuật ngữ kịch bản tiếng Anh sang tiếng Việt**:
- "Hook" → "Hút"
- "Set up" → "Set up" (giữ nguyên)
- "Tension" → "Tension" (giữ nguyên)
- "Pay out" → "Pay out" (giữ nguyên)
- "CTA" → "CTA" (giữ nguyên)

Nếu em chỉ output "Hút" trong analysis (không clarify = Hook) → user phải nhắc: "5 phần kịch bản chính xác phải là: Hook - set up - tension - pay out - CTA".

**Fix — Khi transcript có term tiếng Việt HÓA, ALWAYS add parenthesized EN original:**

```markdown
### 5 Phần Kịch Bản
1. **Hook (Hút)** = Giữ người lại (lời hứa)
2. **Set up** = Đẩy nỗi đau lên cao trào
3. **Tension** = Cầu nối
4. **Pay out** = Đáp án cho câu hứa
5. **CTA** = Mình muốn người ta làm gì
```

**Mapping table cho script framework terms:**
| Vietnamese | English (use this) | Note |
|------------|---------------------|------|
| Hút, Móc | Hook | Most common translation |
| Hứa | Promise | Often appears alongside Hook |
| Lắp đặt, Dàn dựng | Set up | "Set up" often kept as-is |
| Căng thẳng | Tension | "Tension" often kept as-is |
| Trả tiền, Kết quả | Pay out | "Pay out" often kept as-is |
| Kêu gọi hành động | CTA | "CTA" always kept as-is |

**Rule:** Trong bất kỳ analysis nào về kịch bản, **LUÔN dùng tiếng Anh (Hook, Set up, Tension, Pay out, CTA) làm canonical name**, Vietnamese translation chỉ là annotation. Vì:
1. User (Tuấn Anh) đã feedback "Hook" chứ không phải "Hút"
2. Cross-reference với 50+ nguồn quốc tế đều dùng EN terms
3. Script templates exportable cho team đều expect EN terms
### 28. "Phân tích nhầm" có thể nghĩa là "khai thác sâu" — không phải sai file (Pitfall #27 — 2026-06-18, FIX)

**Triệu chứng:** Sau khi em phân tích video xong, user nói "Em phân tích nhầm video rồi" HOẶC "Em khai thác sâu hơn về X đi".

**Hai cách hiểu phổ biến:**

1. **Nhầm FILE** — em xử lý sai file → scan lại filesystem (đã có ở Pitfall #24)
2. **Nhầm NỘI DUNG** — em xử lý đúng file nhưng phân tích sai/hallucinate brand → re-check transcript cue
3. **NHẦM VỀ ĐỘ SÂU** — em phân tích chung chung, user muốn **KHAI THÁC SÂU HƠN** về concept chính

**Trigger phrase for #3:** "khai thác sâu", "phân tích kỹ hơn", "đào sâu", "expand on this", "deep dive into X"

**Fix — Khi user nói "khai thác sâu" sau 1 phân tích:**

1. **SAVE full transcript to wiki TRƯỚC** (immutable, theo SCHEMA):
   ```bash
   cp /tmp/video-*/compressed.srt /Volumes/Storage-1/Hermes/wiki/raw/transcripts/YYYY-MM-DD/<video-id>-<channel>-<topic>.srt
   ```

2. **Tạo deep analysis wiki file** theo cấu trúc 7 phần:
   ```
   Part 1: Full transcript (bảng với cue #, timestamp, content)
   Part 2: Concept A deep dive (trigger words, hook mẫu mạnh/yếu)
   Part 3: Concept B deep dive (kỹ thuật từng phần + ví dụ)
   Part 4: Workflow ứng dụng + kịch bản mẫu (≥3 kịch bản)
   Part 5: Checklist viết kịch bản
   Part 6: Top takeaways
   Part 7: Tài liệu tham khảo mở rộng
   ```

3. **Mỗi concept deep-dive phải có:**
   - Trigger words (từ khoá trigger cảm xúc)
   - Hook mẫu MẠNH (template hay) + Hook mẫu YẾU (template dở) — cho user so sánh
   - 3-5 kịch bản mẫu áp dụng (cho kênh Tuấn Anh cụ thể)

4. **HARD RULE — Output format:** Output TỐI THIỂU 5 kịch bản mẫu cụ thể (không phải "đây là framework"), mỗi kịch bản phải có đầy đủ 5 phần Hook-Set up-Tension-Pay out-CTA. User sẽ chọn 1-2 cái để quay luôn.

**Sai lầm cụ thể (2026-06-18):** Em phân tích video La La School về 4 tử huyệt + 5 phần kịch bản, output chỉ 6 phần (summary, structure, ưu/nhược, áp dụng). User nhắc "khai thác sâu hơn về 4 tử huyệt cảm xúc và cách ứng dụng nó vào làm content". Em phải redo → 19KB wiki file với 5 kịch bản mẫu đầy đủ 5 phần.

**Rule:** Lần đầu phân tích = SHALLOW (5-7 ưu + 5-7 nhược). Nếu user nói "khai thác sâu" → redo với 7-part deep analysis + 5 kịch bản mẫu. Đây KHÔNG phải redo vì sai, mà là redo vì chưa đủ sâu.

### 30. N>1 video + "transcript toàn bộ" → tạo file MD tổng hợp, GỬI MEDIA, không gửi từng video (Pitfall #31 — 2026-06-18, FIX)

**Triệu chứng:** User gửi 16+ video qua Telegram trong 1 batch + nói "transcript toàn bộ" / "phân tích từng cái". Em chạy batch script → transcribe 17 file OK → **gửi từng video qua Telegram 1 message riêng** = user phải đợi 17 lần, dễ miss. User phải nhắc "Alo Alo / Chưa thấy em gửi / Gửi file md cũng được" → frustrated.

**Fix — Sau khi batch transcribe xong, LUÔN tạo 1 file MD tổng hợp:**

```bash
# File path:
/Volumes/Storage-1/Hermes/wiki/queries/YYYY-MM-DD-batch-N-video-transcript-analysis.md
```

**Cấu trúc file MD tổng hợp:**
1. **Overview table** — VID / Duration / Cues / Chủ đề (rút cue đầu tiên của mỗi SRT)
2. **Phân tích chi tiết TỪNG video** (script + tử huyệt + vibe + value thực)
3. **Phân loại tổng hợp** (theo 4 tử huyệt cảm xúc / pattern hay nhất)
4. **Top 3 video viral tiềm năng** để user học
5. **5 ý tưởng kịch bản mới** dựa trên 17 video (Ngày X tiếp theo)

**GỬI QUA TELEGRAM:**
```
MEDIA:/path/to/file.md
```
+ TÓM TẮT 5-10 dòng ngay sau đó (không paste toàn bộ file).

**Sai lầm cụ thể (2026-06-18):** User gửi 16 video qua Telegram. Em transcribe xong → gửi 4 message Telegram dài → user phải nhắc "Alo / Chưa thấy em gửi / Gửi file md cũng được". Thực ra user CHỈ MUỐN 1 file MD tổng hợp, KHÔNG cần 17 tin nhắn Telegram.

**Rule:** Khi N>1 video + user nói "transcript toàn bộ" / "phân tích từng cái":
1. Transcribe batch như bình thường
2. **LUÔN tạo 1 file MD tổng hợp** (kèm overview table + phân tích + top 3)
3. Gửi `MEDIA:/path` + tóm tắt 5-10 dòng
4. KHÔNG gửi từng video qua Telegram (user đã có SRT trong wiki rồi)

### 31. User frustration signals = STOP and DELIVER file MD ngay (Pitfall #32 — 2026-06-18, FIX)

**Triệu chứng:** User nhắn "Alo" / "Sao rồi" / "Ha" / "đâu?" / "Chưa thấy em gửi" — ĐÂY LÀ TÍN HIỆU FRUSTRATION, user nghĩ em đã gửi nhưng không thấy.

**Fix:** KHI user nhắn bất kỳ câu nào dạng "alo", "sao rồi", "đâu", "ha", "chưa thấy":
1. **KHÔNG** giải thích dài dòng tại sao em chưa xong
2. **KHÔNG** hỏi user "anh muốn em làm gì tiếp?"
3. **LUÔN** gửi ngay file deliverable (MD, JSON, hoặc text output) trong cùng tin nhắn
4. **Format** output NGẮN GỌN — chỉ tóm tắt 1-3 bullet, KHÔNG kèm giải thích dài

**Sai lầm cụ thể (2026-06-18):** Sau khi transcribe 16 video, em gửi tin nhắn overview qua Telegram nhưng chưa gửi file MD. User nhắn "đâu?" → em vẫn đang tạo file → user nhắn "Alo Alo / Chưa thấy em gửi / Sao rồi / Gửi file md cũng được". Phải mất 5 tin nhắn mới fix.

**Rule:** Sau khi batch transcribe N video:
- **IMMEDIATELY** tạo file MD tổng hợp (không delay)
- **IMMEDIATELY** gửi `MEDIA:/path` qua Telegram
- **IMMEDIATELY** kèm 1-3 bullet tóm tắt
- KHÔNG gửi từng video riêng lẻ (làm user frustrated)

### 32. Research canonical files TRƯỚC khi tự propose topic (Pitfall #33 — 2026-06-18, FIX)

**Triệu chứng:** User nói "viết kịch bản Ngày 2" / "viết script cho X" — em tự pick topic từ đầu (theo curriculum chung). User phản hồi "nghiên cứu bộ kịch bản 0đ" → có 1 file canonical trong project đã research 20+ kịch bản "0 đồng", em đã không check.

**Fix — Trước khi pick topic tự động:**
1. **List canonical topic files** trong project:
   - `series-xay-kenh-0-dong.md` — 20+ kịch bản "0 đồng" đã research (4 cụm A/B/C/D)
   - `Research/2026-06-17/02-CURRICULUM-NGUOI-MOI-BAT-DAU.md` — 71 bài theo 3 trụ × 4 cấp
   - `deep-research-edit-co-ban.md` (30 kịch bản EDIT)
   - `deep-research-setup-goc-quay.md` (25 kịch bản SETUP)
   - `deep-research-anh-sang-co-ban.md` (30 kịch bản ÁNH SÁNG)
2. **Match user request với 1 trong các file canonical**
3. **Nếu có match** → đề xuất topic từ file canonical (KHÔNG tự propose)
4. **Nếu KHÔNG match** → hỏi user "Anh muốn em chọn từ A/B/C/D/E (5 đề xuất từ file canonical)?"

**Sai lầm cụ thể (2026-06-18):** Sau khi viết Ngày 1 (ánh sáng 0đ), user nói "viết tiếp cho ngày 2 đi". Em tự pick E1.1 (CapCut) theo curriculum. User nói "CapCut quá phổ biến rồi, làm về kỹ thuật edit hoặc chủ đề khác đi, capcut không cần phải giới thiệu!". Phải redo.

**Nếu em check `series-xay-kenh-0-dong.md` TRƯỚC → đã thấy 20+ kịch bản "0 đồng" đã research → đề xuất "Em đề xuất A6/B1/B3 từ bộ 0đ" → user chọn → viết ngay, không bị redo.

**Rule:** LUÔN check canonical files trong project TRƯỚC khi tự propose topic. Nếu user nói "nghiên cứu bộ X" hoặc "X là gì" → ngay lập tức mở file canonical đó.

### 21. Hallucinate channel/brand name from visual style (Pitfall #22 — 2026-06-18, FIX)

**Triệu chứng:** Em phân tích video explainer tiếng Việt, thấy visual style quen thuộc (kem + cam + bánh răng + minimalist) → tự assume tên kênh là "AI NEWS - AI Daily News" vì đây là kênh phổ biến nhất có style đó. Whisper transcript thực tế lại ghi tên kênh KHÁC (ví dụ "La La School").

**Root cause:** Pattern recognition (Pitfall #17) chỉ giúp INFER style nhanh, không phải IDENTIFY brand. Cùng 1 visual template có thể được 5-10 kênh khác nhau sử dụng.

**Fix — Audio transcript is ground truth cho brand name:**
```bash
# Step 1: Run Whisper FIRST (audio transcript có brand name chính xác)
mlx_whisper audio.wav --model mlx-community/whisper-large-v3-turbo \
  --language vi --output-format srt --output-dir /tmp/whisper

# Step 2: Look at 3 cues cuối của SRT — gần như luôn có subscribe CTA
tail -20 /tmp/whisper/video.srt | grep -iE "subscribe|kênh|channel|follow"
# → "Hãy subscribe cho kênh La La School..." = brand name
```

**Rule:**
1. Whisper chạy TRƯỚC vision model (audio ground truth > visual inference)
2. Brand name từ audio cue subscribe, KHÔNG từ visual
3. Nếu audio không rõ brand name → mark "không verify được tên kênh từ audio, dựa trên visual có thể là kênh X" (honest)
4. Sau khi viết analysis, RE-CHECK 3 cue cuối SRT để confirm brand name đúng

### 26. X.com (Twitter) URL extraction — dùng exa_web_search_exa (Pitfall #35 — 2026-06-18, FIX)

**Triệu chứng:** User share link X.com (vd `https://x.com/<user>/status/<id>`), em dùng `web_extract` (ddgs backend) → trả về lỗi "DuckDuckGo (ddgs) is a search-only backend and cannot extract URL content". Em thử `mcp_exa_web_fetch_exa` trực tiếp → lỗi "CRAWL_HTTP_400" vì X.com chặn crawl.

**⚠️ READ-CONTEXT-DEEPLY companion rule (Pitfall #44 — 2026-07-18, NEW):** Khi user share 1 URL/video, KHÔNG BAO GIỜ chỉ lan ra research generic. PHẢI đọc/trích nội dung URL đó TRƯỚC, phân tích đúng artifact đó, CHỈ mở rộng generic nếu user hỏi thêm.

**Real case 18/07:** User share `https://x.com/anatolikopadze/status/2068328135611822149` (seamless morph loop AI motion). Em skip trích nội dung video, đi thẳng vào research generic về Kling/Veo frames-to-video tutorial → anh escalate "đọc kiểu đéo gì vậy". Em phải acknowledge lỗi, re-phân tích CHÍNH video Anatoli Kopadze style (morph internal subject, seamless loop engineering).

**Fix sequence (đã verify 18/07):**
1. **ĐỌC kỹ nội dung URL TRƯỚC** dùng `mcp_exa_web_search_exa(URL)` → lấy description/snippet về nội dung
2. **Phân tích ĐÚNG artifact** đó (nếu là video clip → mô tả chính cái clip, không phải "cách làm generic")
3. **Nếu URL fail trích** → acknowledge gap, dùng snippet Exa + author context để infer
4. **CHỈ lan ra generic tutorial** khi user explicitly hỏi "làm sao làm được video dạng này"

**Rule vĩnh viễn:** "video này" / "URL này" = artifact cụ thể user muốn em hiểu. KHÔNG lấp khoảng trống bằng research chung chung.

**Root cause:** X.com chặn gần như tất cả user agent không phải browser thật. `web_extract` (DuckDuckGo) chỉ search, không fetch. `exa_web_fetch_exa` cũng bị block bởi X.com firewall.

**Fix — Workflow đọc X.com URL:**

1. **THỬ `mcp_exa_web_search_exa`** với URL đầy đủ làm query (KHÔNG phải search keywords):
   ```
   mcp_exa_web_search_exa(
     query="<URL đầy đủ>",
     numResults=5
   )
   ```
   Exa search đôi khi index các bài viết X.com qua mirrors (threadreaderapp, instalker, nitter, etc.). Kết quả trả về có thể có highlights của nội dung tweet gốc.

2. **Nếu vẫn fail**, thử các mirror sites trong priority order:
   ```
   https://threadreaderapp.com/thread/<tweet_id>.html
   https://instalker.org/<user>/status/<tweet_id>
   https://xcancel.com/<user>/status/<tweet_id>
   https://nitter.net/<user>/status/<tweet_id>
   ```

3. **Fallback cuối cùng**: tìm kiếm tweet qua search engines với URL X.com + query liên quan:
   ```
   mcp_exa_web_search_exa(
     query="@<username> tweet <keyword>",
     numResults=3
   )
   ```

4. **Khi user chỉ share URL X.com KHÔNG kèm context**: GHI RÕ trong output là "đọc qua mirror X" + link mirror đó. KHÔNG giả vờ đọc trực tiếp từ X.com.

**Sai lầm cụ thể (2026-06-18):** User share `https://x.com/thedankoe/status/2010751592346030461?s=46&t=9cNaY0AZwMKO1ip9uyxAFw`. Em thử:
- `web_extract` → fail (DuckDuckGo search-only)
- `mcp_exa_web_fetch_exa` → fail (CRAWL_HTTP_400)
- Em retry 2 lần nữa → fail

Fix: dùng `mcp_exa_web_search_exa` với URL đầy đủ làm query → lấy được nội dung qua instalker.org mirror.

**Rule:** Khi user share X.com URL → ưu tiên `mcp_exa_web_search_exa(URL)` để có thể index qua mirrors, TRƯỚC khi thử `web_extract`/`exa_web_fetch_exa`.

**Sai lầm cụ thể (2026-06-18):** Phân tích `p7d0k_QDFhs.mp4`, em hallucinate "AI NEWS - AI Daily News" trong deliverable summary. User nói "Em phân tích nhầm video rồi" → em recheck cue 27 thấy "La La School" → phải redo analysis. Lần 2 vẫn hallucinate "AI Daily News" ở phần visual analysis (vision model) → phải verify lại từ transcript cue 27 một lần nữa.

## Batch Mode (When User Sends N>1 Videos at Once)

**Trigger:** User sends multiple video attachments in one batch (16+ videos is common for Tuấn Anh's research sessions), or says "transcript toàn bộ" / "tất cả video".

**Pattern:** Sequential per-video processing is reliable; parallel whisper calls OOM the MPS memory on Apple Silicon. Whisper-large-v3-turbo is fast enough (~30s/clip) that parallelism is not worth the memory pressure.

**Use the batch script:**

```bash
# Auto-detect newest 20 videos from gateway cache (last 24h)
python3 scripts/batch-transcribe.py --limit 20

# Or explicit list of video hash IDs
python3 scripts/batch-transcribe.py 477dec0b1d18 727b66ac978c 22a0e70409f3

# Output: /tmp/videos-batch-YYYY-MM-DD/<VIDEO_ID>/compressed.{mp4,srt}
```

**Features:**
- **Skip-if-srt-exists** (idempotent) — re-running resumes from where it stopped
- **Auto-discovery** — scan gateway cache filtered by mtime (default last 24h) + size (>1MB)
- **Per-video status report** — prints `✓ 477dec0b1d18 → 1843 bytes` for each
- **Graceful failures** — one whisper error doesn't kill the batch

**⚠️ Pitfall #28 — Don't parallelize whisper (2026-06-18, FIX):**
mlx-whisper uses MPS memory on Apple Silicon. Calling it in parallel for 16 videos OOMs immediately. Sequential is 2-3 minutes for 16 videos, which is fine. The "speed up with parallel" instinct is wrong here.

**⚠️ Pitfall #29 — Topic discovery after batch (2026-06-18, FIX):**
After batch is done, em phải inspect từng SRT để xem chủ đề từng video (cue đầu tiên) trước khi output overview cho user. Dùng:
```bash
for vid in 477dec0b1d18 727b66ac978c; do
  srt="/tmp/videos-batch-DATE/$vid/compressed.srt"
  awk '/^[0-9]+$/{c++} c==1 && !/^[0-9]+$/ && !/^$/ && !/-->/{print; exit}' "$srt"
done
```
Mục đích: tránh user hỏi "video nào nói về chủ đề gì" → em phải có overview trước, không phải re-scan từng file.

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
4. **Motion analysis** (optional, see Step 8) — when user asks about "chuyển động", "movement", "pose", "góc máy", or "tạo prompt video tương tự"
5. **Video AI prompt** (optional, see Step 9) — when user wants to replicate the video with Veo 3 / Kling / Runway / etc.
6. **Style deconstruction + reproducible recipe** (optional, see Step 10) — when user asks "làm sao em làm được video dạng này" / "phân tích công thức" / "study the recipe"

**When to send what:**
- Always send `compressed.mp4` (user expects to receive the video back)
- Send `summary.mp4` only if user asked for compact package or video is long
- Always send text analysis with: metadata table, frame-by-frame description, engagement metrics (if social media), actionable insights
- Send motion analysis + AI prompt ONLY when user explicitly asks for "phân tích chuyển động" or "tạo prompt video tương tự"
- Send style deconstruction + recipe when user asks about REPRODUCING THE STYLE for their own pipeline (different from replicating a specific subject's pose)

## Step 10: Style Deconstruction + Reproducible Recipe (Pedagogical Analysis)

**Trigger phrases (DIFFERENT from Step 8/9):**
- "làm sao em làm được video dạng này" (how can I make a video like this?)
- "phân tích công thức / recipe" (analyze the recipe)
- "study / deconstruct style" (nghiên cứu phong cách)
- "tại sao video này viral / đẹp / look như vậy" (why does this video look the way it does)
- "làm sao để có look noir-tech / cinematic / B&W này" (how to achieve this look)

**KEY DISTINCTION vs Step 8/9:**
- Step 8/9 = replicate THIS video (subject pose + camera + lighting). Body-pose / OOTD TikTok style.
- Step 10 = reverse-engineer THE RECIPE so we can build our OWN video in the same style. Cinematic montage / promo / b-roll style.

**Output goal:** Give anh a pipeline he can re-run to produce videos in this style, NOT a single-subject AI prompt.

### 10a. 3-Stage Frame Sampling Strategy

The existing Step 8 uses a single density. For style deconstruction, use **3 densities** to build a complete picture without blowing the vision-context budget:

| Stage | Density | Frames for 66s video | Purpose | Tool |
|---|---|---|---|---|
| **Overview** | 1 frame / 6s | ~11 frames | Catch the arc, identify motifs | `ffmpeg -vf "fps=1/6,scale=720:-1"` |
| **Detail** | 1 frame / 2s | ~33 frames | Catch text overlays, scene transitions, color shifts | Loop `ffmpeg -ss $t -frames:v 1` over fixed timestamps |
| **Dense** (optional) | 2 fps | 132 frames | Only if detail stage shows micro-motion or text animation | `ffmpeg -vf "fps=2"` |

**Default: stop after Stage 2 unless Stage 1+2 leaves questions unanswered.** Stage 3 is expensive.

### 10b. Contact-Sheet Workflow (Stage 1 + Stage 2 unified output)

**The killer pattern:** Instead of vision-analyzing frames individually, build a grid montage and vision-analyze the WHOLE grid in 1 call. Saves tool calls + preserves temporal context.

```bash
# Stage 1: overview montage (1 frame / 6s, scaled 720px, no labels)
mkdir -p /tmp/style-deconstruct
ffmpeg -y -i compressed.mp4 -vf "fps=1/6,scale=720:-1" /tmp/style-deconstruct/frame_%02d.jpg

# Stage 2: detail montage (1 frame / 2s, scaled 400px, WITH timestamp label per frame)
mkdir -p /tmp/style-deconstruct/detail
for t in 0 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64; do
  ffmpeg -loglevel error -y -ss $t -i compressed.mp4 -frames:v 1 -q:v 2 /tmp/style-deconstruct/detail/f_$(printf '%02d' $t).jpg
done

# Build PIL grid montage (single PNG, easy to vision-analyze)
python3 << 'EOF'
from PIL import Image, ImageDraw
import glob, math, os

# Overview grid (3 cols)
fs = sorted(glob.glob('/tmp/style-deconstruct/frame_*.jpg'))
ims = [Image.open(x).convert('RGB') for x in fs]
w, h = ims[0].size
cols = 3
s = Image.new('RGB', (w*cols, h*math.ceil(len(ims)/cols)), 'white')
for i, im in enumerate(ims):
    s.paste(im, ((i%cols)*w, (i//cols)*h))
s.save('/tmp/style-deconstruct/overview.jpg', quality=88)

# Detail grid with timestamp labels (5 cols, smaller)
fs = sorted(glob.glob('/tmp/style-deconstruct/detail/*.jpg'))
ims = [(Image.open(x).convert('RGB'), os.path.basename(x)[2:4] + 's') for x in fs]
w, h = 400, 400
from PIL import ImageOps as IO
ims = [(IO.fit(im, (w, h)), lab) for im, lab in ims]
s = Image.new('RGB', (w*5, h*math.ceil(len(ims)/5)), 'white')
dr = ImageDraw.Draw(s)
for i, (im, lab) in enumerate(ims):
    s.paste(im, ((i%5)*w, (i//5)*h))
    dr.text(((i%5)*w+8, (i//5)*h+8), lab, fill='red', stroke_width=2, stroke_fill='white')
s.save('/tmp/style-deconstruct/detail.jpg', quality=90)
print(f'overview: {len(ims)} frames | detail: {len(ims)} frames')
EOF
```

**Then 2 vision calls** (one per montage), instead of 33+ individual calls:

```
Vision call 1: 
"Phân tích contact sheet 11 frame không có nhãn thời gian của video này. 
Mô tả: nội dung chính, visual style, từng loại cảnh, chuyển động camera/animation, 
typography, UI, compositing, màu sắc, nhịp dựng, và suy luận pipeline công cụ khả thi để tái tạo."

Vision call 2: 
"Đây là contact sheet 33 frame, mỗi frame cách 2 giây, có nhãn thời gian đỏ. 
Hãy đọc chính xác timeline: phân đoạn nào xuất hiện lúc nào, nội dung chữ/logo, 
motif hình ảnh, nhịp thay đổi. Sau đó kết luận pipeline tối giản nhưng đạt 90% look."
```

**Why this works:**
- 1 vision call on a grid sees TEMPORAL context (the eye reads frames left-to-right, top-to-bottom)
- Grid is 1 image = 1 message = preserves context across the conversation
- Saves 30+ individual calls
- The red timestamp labels let the second call produce exact second-by-second timeline

### 10c. Style-Deconstruction Output Format (the recipe answer)

After Stage 1 + 2 vision calls, structure the answer as **5 tables + 1 recipe**:

```markdown
## 1. Visual style tổng thể (look)
| Yếu tố | Mô tả |
|---|---|
| Tông màu | ... |
| Phong cách | ... |
| Kết cấu | ... |
| Moodboard | ... (reference 2-3 ảnh phim) |

## 2. Timeline chính xác (giây : nội dung)
| Khoảng | Frames | Nội dung | Visual/Text | Nhịp |
|---|---|---|---|---|
| 0–8s | ... | ... | ... | ... |

## 3. AI-generated parts (90%) — prompt tóm tắt cho từng clip
| Asset | Prompt | Tool |
|---|---|---|
| Scene 1 | "noir dark server room..." | Kling |
| ... | | |

## 4. Composite/code parts (10%)
| Việc | Cách làm | Tool |
|---|---|---|
| Text overlay | Glitch reveal | Remotion / ffmpeg drawtext |
| ... | | |

## 5. Sound design
- Bass layer, glitch SFX, click beats
- Tool: Epidemic Sound / Splice / Suno

## 6. Recipe (full pipeline)
1. Tạo N scene AI với cùng seed + bảng màu
2. Dựng timeline bằng Remotion (text + logo + glitch theo frame)
3. FFmpeg pass cuối: monochrome + contrast + grain + scanline
4. Sound design layer
5. Render master + export variants
```

**Length budget:** 1500-2500 từ. Anh ghét verbose; compress to tables not paragraphs.

### 10d. Anti-patterns for Step 10

- ❌ Apply Step 8/9 prompt templates (pose sequence, OOTD, mirror selfie) → wrong genre
- ❌ Analyze frames individually → blows context budget, loses temporal reading
- ❌ Output one big prose paragraph → anh skip đọc
- ❌ Recommend After Effects without checking Remotion first → Remotion + ffmpeg gives 90% look in 1/3 thời gian
- ❌ Forget to specify aspect ratio + fps of source → make wrong pipeline assumption (this video was 2160×2160 square, NOT 9:16 or 16:9)
- ❌ Forget audio analysis → if source has voiceover / SFX, recipe needs sound design layer

### 10e. Real case study: NousResearch hackathon promo (16/07/2026)

**Source:** `https://x.com/NousResearch/status/2077517414464410091/video/1` — 66.08s, 2160×2160, 24fps, H.264/AAC, ~119MB.

**Recipe answer (the pipeline we landed on):**

```
AI video → Remotion → FFmpeg, không cần After Effects

1. Tạo 8-10 scene AI bằng Google Flow / Kling, mỗi scene 4-8s
2. Cùng seed + bảng màu + camera language để giữ continuity
3. Remotion dựng timeline + text + logo + glitch + flash theo frame
4. FFmpeg pass cuối: monochrome, contrast, grain, scanline, vignette, bloom
5. Sound: industrial bass + CRT hum + typing + glitch hit + sub-drop
6. Render master 2160×2160 24fps, xuất thêm 1080×1920 nếu cần TikTok
```

**Style pattern identified:** "noir-tech cinematic promo" = B-roll AI + slow push-in + monochrome extreme contrast + heavy grain + scanline + diegetic UI (CRT/dashboard) + serif title cards with glitch + snap-cut white endcard with sponsor lockup. Reference moodboard: The Matrix, Blade Runner, Mr. Robot, Severance intro.

**Output delivered:** Inline tables + 1-paragraph verdict + 1 🎯 systems line. Anh accepted without revision.

See `references/noir-tech-promo-deconstruction-case-study-2026-07-16.md` for full transcript + pipeline commands.

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

## Review Output Format (khi anh hỏi "transcript + phân tích")

Output bắt buộc phải có đủ 6 phần:

1. **Full transcript** — gửi qua `MEDIA:/path/to/file.srt` cho anh tải về
2. **Metadata**: nguồn URL/kênh, thời lượng, độ phân giải, ngôn ngữ
3. **Cấu trúc video** — breakdown theo timestamp (Hook / Problem / Core idea / Value / CTA) với độ dài từng phần
4. **5-7 điểm mạnh** + **5-7 điểm yếu** — theo preference 17/06: gọn, bỏ specs, evidence-based
5. **Áp dụng cho kênh Content Creator** (Edit + Setup + Ánh sáng) — chia 2 cột: HỌC gì / KHÔNG học gì
6. **Đề xuất hướng khai thác tiếp** — 1-3 options để anh chọn, KHÔNG hỏi "có muốn em làm không"

Tone: tiếng Việt, casual, ngắn gọn. Không liệt kê quá nhiều — anh ghét verbose.
- `tiktok-competitor-deep-analysis` — for batch competitor analysis (50+ clips, not single video)
- `transcript-cleanup` — cleanup media files after analysis (saves disk)
- `tiktok-viral-script` — for writing scripts in Tuấn Anh's voice (combine with motion analysis)

## Reference Files

- `scripts/analyze-telegram-video.sh` — One-shot pipeline for single video (HEVC→H.264, frames, whisper, summary package)
- `scripts/batch-transcribe.py` — NEW 2026-06-18: Batch mode for 16+ videos. Auto-discovers newest from gateway cache, sequential compress+whisper, idempotent skip-if-srt-exists, per-video status report. Use when user sends "transcript toàn bộ" or 10+ video attachments at once.
- `references/tiktok-screen-recording-case-study.md` — Full case study of `p7d0k_QDFhs` analysis (2026-06-18): narrative arc, visual style template cho AI/tech explainer video, VLM rate-limit handling pattern
- `references/motion-analysis-and-ai-prompts.md` — Motion analysis workflow + 3 prompt templates for AI video replication (Veo 3 / Kling / Sora)
- `references/output-template.md` — Standard 6-section output format for "transcript + phân tích" requests
- `references/vietnamese-explainer-case-study.md` — Full case study of `p7d0k_QDFhs` analysis (2026-06-18): narrative arc, visual style template cho AI/tech explainer video, VLM rate-limit handling pattern
- `references/tu-huyet-cam-xuc-5-phan-kich-ban.md` — La La School framework: 4 tử huyệt cảm xúc (Danh-Tiền-Tình-Lợi ích) + 5 phần kịch bản (Hook-Set up-Tension-Pay out-CTA) + 5 kịch bản mẫu cho kênh Content Creator. **Pitfall #28** (FIX 2026-06-18): "Hút" trong transcript = Vietnamese của "Hook" — mapping table INSIDE this file. Always use EN canonical names in analysis output.
- **`references/batch-video-output-format.md`** — NEW 2026-06-18: Output format examples for batch video analysis (17 videos). Real example: SRT naming convention (`<vid>-<topic-slug>.srt`), MD file structure (overview table + phân tích + top 3 + 5 ý tưởng), anti-patterns (gửi từng video, giải thích dài dòng). Anchors Pitfall #31 (batch → MD) và Pitfall #32 (frustration signals → deliver fast).
- **`references/noir-tech-promo-deconstruction-case-study-2026-07-16.md`** — NEW 2026-07-16: Worked example for Step 10 (Style Deconstruction). Source: NousResearch "Accelerated Business Hackathon" promo 66s, 2160×2160 square, monochrome noir-tech style. Documents: contact-sheet workflow (11-frame overview + 33-frame labeled detail montage + 2 vision calls only), the "AI video → Remotion → FFmpeg" recipe, style-pattern metadata (`noir-tech-cinematic-promo` class), and reusable commands for any cinematic promo.
- **`references/caocuongvuai-tiktok-no-audio-case-study.md`** — NEW 2026-06-22: Worked example of TikTok HEVC video-only analysis. Source: @caocuongvuai video 7623055460836330772 (6-min AI reaction, 113.8K views, no audio stream). Documents: workflow mistakes that happened (asked for URL when binary on disk, tried --extract-audio on HEVC, ffmpeg audio extraction fail), what worked (8 frames @ 60fps positions, vision-only path, parallel batches of 4), reusable workflow summary. Anchors Pitfall #36 (file-on-disk workflow) + reference for video-download-yt-dlp Pitfall #8.
- **`references/x-twitter-url-extraction.md`** — NEW 2026-06-18: Workaround pattern cho X.com URL extraction. X.com chặn web_extract + exa_web_fetch_exa trực tiếp. Dùng `mcp_exa_web_search_exa` với URL làm query (index qua mirrors), hoặc try mirror sites (threadreaderapp, instalker, xcancel, nitter). Anchors Pitfall #35.
