---
name: youtube-transcript-extractor
title: YouTube Transcript Extractor (YouTube + Shorts + TikTok)
description: Extract full transcripts from YouTube videos, YouTube Shorts, and TikTok for content creation and research. Includes Vietnamese subtitle strategy + local Whisper fallback for videos without captions, plus TikTok audio-only path when video stream is blocked.
created: 2026-05-01
updated: 2026-06-22
type: skill
tags: [youtube, content, transcript, tiktok, whisper]
confidence: high
---

# YouTube Transcript Extractor

Extract full transcripts from YouTube videos, YouTube Shorts, and TikTok for content creation/research.

## 🚨 HARD RULE: Read the FULL request before acting (learned 2026-06-22)

**Tuấn Anh's correction:** *"Phải phân tích toàn bộ yêu cầu của anh thay vì chỉ đọc lướt qua. Ngay từ đầu anh đã bảo em lấy transcript!"*

When user message contains keywords → keyword wins, even if other words seem more prominent:

| User says | PRIMARY deliverable | What to skip |
|-----------|---------------------|--------------|
| **"transcript"** / **"lời nói"** / **"voice"** / **"phụ đề"** | Extract voice audio → Whisper SRT | Visual frame analysis |
| **"phân tích video"** (no transcript word) | Mix of transcript + visual | Don't skip either |
| **"tải về"** | Download MP4 | Transcript optional |
| **"transcript + phân tích"** | Both — but transcript FIRST (it's what user spelled out) | Don't prioritize analysis over transcript |

**Don't substitute visual frame analysis when user asks for voice transcript.** If `ffprobe` shows no audio, that's a SIGNAL to try other format variants (`-f "download"` or variant `-1`), not a SIGNAL to switch to vision-only.

**Don't promise "lần sau sẽ làm tốt hơn" without saving a real lesson** — user explicitly said: *"Anh không muốn em hứa suông, anh muốn có lesson learn"*. Concrete lesson = skill patch + memory entry + reference doc with prevention checklist. Vague promises don't count.

## Quick Decision Tree (đọc đầu tiên)

```
Anh gửi YouTube/Shorts/TikTok link + muốn transcript
    │
    ├─ Cần tải video về? (anh hay nói "tải về" + "transcript" cùng lúc)
    │   YES → skill: video-download-yt-dlp (tải + verify + gửi MEDIA:)
    │         SAU ĐÓ chạy transcript workflow (skill này)
    │
    ├─ URL là TikTok (vt.tiktok.com / tiktok.com/.../video/...)?
    │   YES → check `yt-dlp -F URL` xem có video format không
    │         ├─ Full MP4 (multiple video+audio formats) → "TikTok full video path"
    │         │   download MP4 → ffmpeg WAV → mlx_whisper SRT (xem "TikTok Full Video Path" ở dưới)
    │         │   Ưu tiên khi CẦN CẢ VIDEO + TRANSCRIPT (cho competitor analysis)
    │         └─ Chỉ có "audio mp3 audio only" → xem references/tiktok-audio-only-transcript-path.md
    │              Workflow: download MP3 → feed thẳng vào Whisper (skip ffmpeg step)
    │              Trade-off: mất video file
    │
    ├─ Video tiếng Việt? (90% trường hợp của anh)
    │   YES → dùng yt-dlp --write-auto-sub --sub-lang vi-orig,vi (xem "Vietnamese Subtitle Strategy")
    │          → SRT chất lượng cao, NHANH, không cần GPU
    │
    └─ Video tiếng Anh / không có sub?
        → Local Whisper fallback (xem "Local Whisper Fallback")
        → CHỉ dùng khi không còn cách nào khác
```

## Quick script: one-shot pipeline

For the common case "TikTok/YouTube URL → transcript files in 60 seconds":

```bash
~/.hermes/skills/media/youtube-transcript-extractor/scripts/transcribe-tiktok.sh \
  "https://vt.tiktok.com/XXX/" \
  "~/wiki/raw/tiktok-analysis/"
# → transcript.txt + transcript.srt + transcript.json + transcript_segments.txt
```

Pipeline built into script: `yt-dlp -F` → `-f "download"` → `ffprobe verify audio` → `ffmpeg WAV` → `mlx_whisper --language vi`. Script bails with error if audio stream missing (does NOT fall back to visual — per HARD RULE above).

## Khi anh chỉ nói "Transcript" (không có link)

Session 2026-06-13: anh nói "Transcript" mid-conversation → hỏi lại link. ĐỪNG đoán video nào. Anh gửi link kèm theo mới chạy workflow.

## Tool: youtube-content skill

```bash
skill_view(name="youtube-content")
```

This skill handles fetching YouTube video transcripts.

## Alternative: Direct yt-dlp

```bash
# Install if needed
pip install yt-dlp

# Get transcript (English)
yt-dlp --write-auto-sub --sub-lang en --skip-download -o /tmp/video.%(ext)s https://youtu.be/VIDEO_ID

# Get transcript (Vietnamese — anh's primary use case)
yt-dlp --write-auto-sub --sub-lang vi-orig,vi --sub-format srt --skip-download \
  -o "/tmp/VIDEO_ID-sub" https://youtube.com/shorts/VIDEO_ID
# → Tạo file /tmp/VIDEO_ID-sub.vi-orig.srt (auto-generated Vietnamese)
# → Fallback chain: vi-orig (original) → vi (translated)

# Or get subtitles as transcript
yt-dlp --convert-subs srt --skip-download -o /tmp/video.%(ext)s https://youtu.be/VIDEO_ID
```

## Vietnamese Subtitle Strategy (Anh's primary use case)

Most videos anh transcribes are Vietnamese content creators. YouTube auto-generates Vietnamese subs with high quality — use this BEFORE falling back to Whisper.

**Step 1: Check if subs exist**
```bash
yt-dlp --list-subs "https://youtu.be/VIDEO_ID" 2>&1 | grep -E "vi-orig|^vi " | head -5
```

**Step 2: Pull vi-orig first (original audio language), then vi (translated)**
- `vi-orig` = original Vietnamese audio (most accurate, no translation artifacts)
- `vi` = translated from another language (use only if vi-orig missing)

**Step 3: Parse SRT → clean text**
```bash
# Strip timestamps + line numbers, keep only text
grep -v "^[0-9]*$" /tmp/VIDEO_ID-sub.vi-orig.srt | \
  grep -vE "^[0-9]{2}:[0-9]{2}" | \
  sed '/^$/d'
```

### Step 4: When no auto-subs (foreign language, no captions)
Fall back to local Whisper via `mlx_whisper` (Apple Silicon). See "Local Whisper Fallback" section below.

### Step 4b: Exa fetch fallback for Vietnamese channels WITHOUT auto-sub (NEW 2026-07-11)

**Khi `yt-dlp --list-subs` returns empty cho Vietnamese channel** (e.g. @VuiVe, nhiều kênh VN listicle tắt captions), trước khi fall back Whisper (chậm 1-3 phút), thử `mcp__exa__web_fetch_exa` với YouTube watch URL.

```python
mcp__exa__web_fetch_exa(
    urls=["https://www.youtube.com/watch?v=VIDEO_ID"],
    maxCharacters=8000
)
# → Trả về metadata + "Transcript:" section với ~3000-4000 words verbatim
#    tiếng Việt (kể cả filler words "ấ", "nhá", "ơ")
```

**Verified case 2026-07-11:** @VuiVe video "Những fact lmao nhất về con người" (yfwDXobx07U, 774K views, 14:49) → Exa trả về full transcript verbatim Vietnamese trong ~3s. Đủ tốt cho script analysis (hook decomposition, narrative pattern, retention technique).

**Caveats Exa transcript:**
- Đôi khi ASR cleanup nhỏ ("trong th" thay vì "trong thế giới")
- Không có timestamps chính xác (chỉ text liên tục)
- Không có speaker labels
- Nếu video bị owner xóa/private → fail với `CRAWL_NOT_FOUND`

**Khi nào KHÔNG dùng Exa:** Khi cần word-level timestamps cho caption editing → vẫn phải Whisper SRT. Khi cần perfect accuracy cho legal/medical content → vẫn phải Whisper.

**Updated decision tree:**

```
YouTube video for transcript
  │
  ├─ Run `yt-dlp --list-subs URL` first
  │
  ├─ Has vi-orig or vi auto-sub?
  │   YES → yt-dlp --write-auto-sub → 2-3s, no GPU ✅ FASTEST
  │
  ├─ No subs at all (channel disabled captions)?
  │   ├─ Vietnamese content + just need text (not timestamps)?
  │   │   YES → mcp__exa__web_fetch_exa → ~3s, no GPU ✅ FAST
  │   │
  │   └─ Need timestamps, high accuracy, or non-VN content?
  │       → Local Whisper SRT (slow, but only option)
  │
  └─ Exa fails / CRAWL_NOT_FOUND?
      → Local Whisper (fallback cuối cùng)
```

**Time saved 2026-07-11:** @VuiVe 14:49 video có `yt-dlp --list-subs` returns empty → Exa transcript in 3s vs Whisper 1-3 minutes. **Quyết định nhanh đúng tool.**

## Local Whisper Fallback (no auto-subs available)

Khi video KHÔNG có auto-sub (ví dụ: video ngắn 4s không có caption, video tiếng Anh không có sub, hoặc auto-sub bị tắt), dùng local Whisper:

### Step 1: Extract audio as 16kHz mono WAV
```bash
ffmpeg -y -i /path/to/video.mp4 -ar 16000 -ac 1 -c:a pcm_s16le /tmp/video.wav
```

**EXCEPTION:** Nếu file đã là MP3 (TikTok audio-only case — xem references/tiktok-audio-only-transcript-path.md), skip bước này, feed MP3 thẳng vào Whisper.

### Step 2: Pick model by what's CACHED locally
```bash
# Check cached models (CRITICAL — auth có thể fail với fresh download)
ls ~/.cache/huggingface/hub/ | grep -i whisper
```

**Cách chọn model (quan trọng):**
- **PREFER cached models first** — HF auth thường fail với fresh download (`mlx-community/whisper-small`, `whisper-base` thường 401)
- **Known working cached model:** `mlx-community/whisper-large-v3-mlx` (large-v3 MLX port, ~3GB)
- Nếu không có model nào cached, fail fast với message rõ ràng (đừng waste time retry)

### Step 3: Run mlx_whisper
```bash
cd /tmp
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --output-format txt \
  --output-name video-transcript \
  video.wav
# → Output: /tmp/video-transcript.txt
```

### Whisper Pitfalls (từ session 2026-06-13)

1. **HF auth 401 on fresh download** — `mlx-community/whisper-small` và `whisper-base` thường fail với `RepositoryNotFoundError: 401 Client Error`. LUÔN check `~/.cache/huggingface/hub/` trước.

2. **Whisper auto-detects wrong language** — `--language` flag chưa được set → nó auto-detect từ 30s đầu. Với video ngắn (< 30s) có thể detect sai. Force language: `mlx_whisper --model ... --language vi ...`

3. **Verbose output pollutes transcript** — Whisper in `[00:00.000 --> 00:02.000]` markers vào stderr. Chỉ `cat *.txt` để lấy clean text, ignore stderr.

4. **Short videos (< 5s) thường ra kết quả rỗng hoặc sai** — Whisper cần ≥ 1s audio với content rõ. Nếu video < 5s và Whisper ra 1-2 từ vô nghĩa ("Thank you."), báo cho anh biết audio quality quá thấp.

5. **OXXoI2MF-Gs false-reassurance pitfall** — File 97KB có thể là video 4.6s Shorts thật (KHÔNG PHẢI truncated). Shorts thường chỉ 1-2MB dù format 720p. Verify bằng ffprobe `duration` (không phải size) trước khi conclude "file truncated". Đừng tự kết luận sai chỉ vì file nhỏ.

6. **Always check `--list-subs` BEFORE Whisper fallback** (added 2026-06-13) — Whisper is slow (15-30s per short video, 1-3 min for 1-min Shorts). YouTube auto-subs are FAST (2-3s download) + accurate. Decision tree:

   ```
   YouTube video for transcript
     │
     ├─ Run `yt-dlp --list-subs URL` first
     │
     ├─ Has vi-orig or vi auto-sub? (90% of Vietnamese content)
     │   YES → yt-dlp --write-auto-sub --sub-lang vi-orig,vi → 2-3s, no GPU
     │
     ├─ Has en auto-sub only?
     │   → Use that, translate if needed
     │
     └─ No subs at all?
         → Local Whisper (slow, but only option)
   ```

   **Time saved in 2026-06-13 session:** `p7d0k_QDFhs` (94s YouTube Shorts with vi-orig auto-sub) → SRT in 3s vs Whisper would have been 1-2 minutes.

7. **TikTok videos NEVER have auto-sub** — `--list-subs` always returns empty for TikTok. Skip the check, go straight to audio-only MP3 download + Whisper pipeline.

## Output Format for Tuấn Anh

When Tuấn Anh asks for video transcript:
1. Extract full transcript
2. Break into timestamped sections by topic
3. Create summary table at top (timestamp | section title)
4. Highlight key quotes/insights
5. Offer alternative formats (tweet thread, blog post, chapter-by-chapter)

**Timestamped SRT output (added 2026-06-13):** When user asks "transcript kèm timestamp" or "transcript với timestamp", use:
```bash
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --output-format srt \
  --output-name tiktok-VIDEO_ID-srt \
  /path/to/audio.mp3
# → Output: /tmp/tiktok-VIDEO_ID-srt.srt (full SRT with HH:MM:SS,mmm ranges)
```

Send both the clean text AND the SRT file (via MEDIA:/path) so user can use SRT for captions/edits.

For YouTube Vietnamese auto-sub: SRT comes from yt-dlp directly:
```bash
yt-dlp --write-auto-sub --sub-lang vi-orig,vi --sub-format srt --skip-download \
  -o "VIDEO_ID-sub" "URL"
# → /tmp/VIDEO_ID-sub.vi-orig.srt ready-to-use
```

## User Preference: SPEED > DEPTH cho video transcript (learned 2026-06-18)

**Signal:** Tuấn Anh đã correct em trong session 18/06: "Tải video về được thì dùng whisper mà transcript cho nhanh chứ!" — em đang spend 5 phút check frame-by-frame thay vì 20s whisper.

**Rule:** Khi user gửi video TikTok/YouTube, **LUÔN BẮT ĐẦU BẰNG WHISPER SRT TRƯỚC** (audio path, 20-30s). Visual frame analysis chỉ là OPTIONAL add-on khi user explicitly cần hoặc khi transcript gợi ý cần xem visual (vd: text overlay quan trọng, B-roll layout).

**Default flow khi user gửi video link:**
1. Download MP4 (5s)
2. Whisper SRT (20s)  
3. Đọc transcript → identify key insights
4. **NẾU** cần visual → extract 3-4 frame quan trọng (15s)
5. Tổng hợp + gửi cho user

**KHÔNG BAO GIỜ** extract 12 frames rồi analyze từng cái trước khi có transcript. Đó là lãng phí 4× thời gian.

**Context:** Tuấn Anh's work style preference: VERIFY/QA/TEST before saying DONE, but for analysis tasks → prioritize speed-to-insight over completeness. User ghét khi em spend 5 phút xử lý 1 video khi có thể xong trong 30s với tool đúng.

## CRITICAL: Telegram Video Attachments

**PROBLEM:** When Tuấn Anh sends videos directly as Telegram file attachments, Hermes CANNOT access them. Only text/links pass through the gateway — media files are not accessible.

**WORKAROUND:** When Tuấn Anh asks to analyze a video he sent as an attachment:
1. Politely explain: "Anh ơi, em không access được video đính kèm Telegram. Anh gửi link YouTube/TikTok thay nhé!"
2. OR: Guide him to save the file to `~/Downloads/` and tell em the filename

**NEVER:** Assume the video was received. Always confirm em can access the file before promising analysis.

---

## Note for Tuấn Anh Content

Tuấn Anh is a TikTok content creator interested in AI/tech topics. He asked for Andrej Karpathy "I've Never Felt More Behind" transcript (2026-05-01). Future requests may include:
- Tech podcast transcripts (Lex Fridman, Huberman, etc.)
- AI/LLM trend videos
- Code agent/agentic engineering content

For TikTok script purposes, focus on:
- Extractable viral hooks or insights
- Controversial/predictive statements
- Actionable advice for developers/founders

## TikTok Video Handling

yt-dlp also works for TikTok videos:
```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download -o /tmp/tiktok.%(ext)s https://vt.tiktok.com/VIDEO_ID
```

Extract frames for visual analysis:
```bash
ffmpeg -i video.mp4 -vf fps=1 -frames:v 20 frame_%03d.jpg
```

### TikTok audio-only path (when video stream blocked) — VERIFIED 2026-06-13

When `yt-dlp -F URL` only shows `audio mp3 audio only` format (1 row, audio-only mp3) → TikTok blocking video download, only audio available.

**Confirmed example:** `https://vt.tiktok.com/ZSQm9pYrV/` (@tuan_anh.review video 7650439370519940370) — only audio mp3 returned, despite video playing fine on app.

**Workflow:**
1. Download MP3: `yt-dlp -f best --merge-output-format mp3 -o "tiktok-VIDEO_ID.mp3" URL`
2. Feed MP3 directly to Whisper (skip ffmpeg WAV extraction — mlx-whisper handles MP3 natively)
3. Read transcript: `cat /tmp/tiktok-VIDEO_ID-transcript.txt`

**Trade-off:** Lose video file, only audio. If user wants the video too, must use browser-harness separately.

See `references/tiktok-audio-only-transcript-path.md` for full workflow + session example.

**Lesson learned 2026-06-13:** Khi `yt-dlp -F` chỉ trả về 1 row "audio mp3 audio only" — đây KHÔNG phải error, đây là format hiện có duy nhất. KHÔNG cần retry với format khác. Move directly to MP3 + Whisper pipeline.

### TikTok full video path (when video stream available) — VERIFIED 2026-06-18, UPDATED 2026-06-22

Khi `yt-dlp -F URL` trả về MULTIPLE formats (bao gồm video mp4) → TikTok cho download full MP4. Dùng workflow này khi CẦN CẢ VIDEO + TRANSCRIPT (vd: competitor analysis cho Content Creator project, vừa xem visual vừa phân tích voiceover).

**Confirmed examples:**
- `https://vt.tiktok.com/ZSQt1SY3m/` (video "ánh sáng 0đ" 43s, MP4 5.6MB tải về thành công 18/06/2026)
- `https://vt.tiktok.com/ZSCJB91YQ/` (@caocuongvuai video 7623055460836330772, 6 phút, MP4 32.6MB có audio 22/06/2026)

**⚠️ CRITICAL FORMAT PITFALL (NEW 2026-06-22):**

`yt-dlp -F` of TikTok Liệt kê nhiều format VỚI `ACODEC aac` NHƯNG download variant `-0` (zero) cho ra file MP4 **CHỈ CÓ VIDEO STREAM, KHÔNG CÓ AUDIO**. Variant `-1` (one) hoặc format `download` (watermarked) mới có cả audio+video.

**Example (session 22/06):**
```
$ yt-dlp -F https://vt.tiktok.com/ZSCJB91YQ/
ID                                EXT RESOLUTION  ACODEC
h264_540p_845120-0                mp4 576x1024    aac    ← variant -0: NO audio when downloaded!
h264_540p_845120-1                mp4 576x1024    aac    ← variant -1: HAS audio
bytevc1_1080p_982660-0            mp4 1080x1920   aac    ← variant -0: NO audio when downloaded!
bytevc1_1080p_982660-1            mp4 1080x1920   aac    ← variant -1: HAS audio
download                          mp4 unknown     aac    ← watermarked: ALWAYS has audio+video
```

**Sai lầm của em session 22/06:** Chạy `yt-dlp -f "bestaudio[ext=m4a]/bestaudio/best"` → file MP4 chỉ có HEVC video, NO audio → em conclude SAI "video không có audio" và làm phân tích visual thay thế. Anh phải nhắc lần 2 "có voice nói đàng hoàng mà" mới phát hiện ra format `download` có audio đầy đủ.

**Rule (HARD):** Khi user yêu cầu transcript TikTok → **`-f "download"`** là format AN TOÀN NHẤT (watermarked nhưng luôn có cả audio+video bundled). KHÔNG dùng `-f "bestvideo+bestaudio"` cho TikTok — TikTok CDN trả về HEVC video stream riêng, audio stream riêng, và yt-dlp merge không reliable.

**Workflow 4 bước (FIXED):**

```bash
# Step 1: Download full MP4 with AUDIO bundled
# ✅ SAFE: -f "download" — watermarked nhưng có audio+video
# ✅ SAFE: -f "bytevc1_1080p_982660-1/h264_540p_845120-1" — variant -1 explicitly
# ❌ UNSAFE: -f "bestvideo+bestaudio" — TikTok merge fail
# ❌ UNSAFE: -f "bytevc1_1080p_982660-0" — variant -0 = NO audio in output
cd ~/Downloads
yt-dlp --no-warnings --quiet -f "download" \
  -o "tiktok-VIDEO_ID.%(ext)s" "https://vt.tiktok.com/XXX/"
# → ~/Downloads/tiktok-VIDEO_ID.mp4 (typical 30-50MB cho 6-min video)

# Step 2: VERIFY audio presence BEFORE extracting (5 second check)
ffprobe -v error -show_streams -of json FILE.mp4 | python3 -c "
import sys, json
d = json.load(sys.stdin)
streams = d.get('streams', [])
audio = [s for s in streams if s.get('codec_type') == 'audio']
video = [s for s in streams if s.get('codec_type') == 'video']
print(f'video={len(video)}, audio={len(audio)}')
print('AUDIO_OK' if audio else 'NO_AUDIO_REDOWNLOAD')
"
# → "AUDIO_OK" = continue. "NO_AUDIO_REDOWNLOAD" = try -f variant -1 hoặc "download"

# Step 3: Extract audio 16kHz mono WAV (chuẩn cho mlx_whisper)
ffmpeg -y -i ~/Downloads/tiktok-VIDEO_ID.mp4 \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 \
  /tmp/tiktok-VIDEO_ID.wav
# → /tmp/tiktok-VIDEO_ID.wav (~12MB cho 6-min video)

# Step 4: Whisper SRT transcript (force Vietnamese — auto-detect sai với video < 30s)
mlx_whisper /tmp/tiktok-VIDEO_ID.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi --task transcribe \
  --output-dir /tmp/tiktok-transcript --output-format srt
# → /tmp/tiktok-transcript/tiktok-VIDEO_ID.srt (~178 segments cho 6-min video)
# → 60 giây processing time trên M1/M2 (MLX framework) cho 6-min audio

# Step 5: (Optional) Visual frame analysis cho hook/body/CTA
mkdir -p /tmp/frames
ffmpeg -i ~/Downloads/tiktok-VIDEO_ID.mp4 -vf fps=1 /tmp/frames/frame_%02d.jpg
# Check 3-5 frames quan trọng (frame_00 hook, frame_N body, frame_last CTA)
# Dùng mcp_MiniMax_understand_image(image_source=/tmp/frames/frame_00.jpg, prompt="...")
```

**So sánh 3 path TikTok:**

| Path | Khi nào dùng | Có video? | Có audio? | Speed |
|------|--------------|-----------|-----------|-------|
| **Full video** (này) | Cần phân tích visual (hook layout, B-roll, text overlay) | ✅ | ✅ | ~30s total |
| **Audio-only** (trên) | Chỉ cần transcript text, không cần visual | ❌ | ✅ | ~25s |
| **Auto-sub** | YouTube vi-orig (KHÔNG áp dụng cho TikTok — TikTok NEVER có auto-sub, --list-subs always empty) | — | — | — |

**Lesson learned 2026-06-18:** TikTok KHÔNG có auto-sub bao giờ (`--list-subs` luôn trả empty). Nhưng 50%+ videos vẫn cho download MP4 đầy đủ. Khi cần cả visual + audio analysis (vd: content creator research, copy viral framework), LUÔN ưu tiên "full video path" thay vì audio-only. Trade-off 5-10s download time là đáng để có video để phân tích hook layout, text overlay style, framing.

**MCP vision tool quan trọng:** Sau khi có frames, dùng `mcp_MiniMax_understand_image` để phân tích text overlay tiếng Việt, layout, tone màu. KHÔNG dùng `vision_analyze` local (fail: "No models loaded") hay LM Studio (no model loaded). mcp_MiniMax_understand_image work reliable với file path local.

### Khi nào KHÔNG dùng TikTok full video path

- Chỉ cần transcript text → audio-only path nhanh hơn
- Video > 5 phút → file MP4 quá lớn (>50MB), download chậm, xem xét audio-only
- Anh không cần visual analysis (chỉ nghe voiceover)

---

## When to use analysis layer (vs. transcript only)

Two skills overlap on extraction but differ on analysis:

| Skill | Output | When to use |
|-------|--------|-------------|
| `youtube-transcript-extractor` (this) | Raw `.txt` + `.srt` + `.json` — **NO analysis** | User only wants the transcript text for their own use |
| `tiktok-transcript-pipeline` | All of above + **`SCRIPT_ANALYSIS.md`** (hook, structure, CTA, viral formula, lessons) | User asks "phân tích transcript" or "phân tích script video" — they want extraction AND analysis |

**Decision rule (added 2026-06-23 after overlap detected):**

- User says "transcript" / "lấy transcript" / "phụ đề" → this skill (extraction only)
- User says "phân tích transcript" / "phân tích script video" / "phân tích video" → `tiktok-transcript-pipeline` (extraction + SCRIPT_ANALYSIS.md)

Keyword "phân tích" in user message = MUST produce analysis file. Don't just deliver raw transcript and call it done — that's the exact failure pattern that triggered the `tiktok-transcript-pipeline` skill creation.

## Anti-Over-Engineering Note (added 2026-06-23)

This skill was patched several times across 2026-06-13 / 18 / 22 for transcript-extraction failures. When Tuấn Anh said "over engineering" about the read-full-request mandate propagation, he meant: **put the rule in this skill body (where the work happens), don't build CI gates / shared checklist files / multi-SOUL.md injectors**. The rule is already embedded here as the "HARD RULE" at the top — that's enough.

If you're tempted to add a new script `verify_youtube_transcript.sh` to enforce this skill's pipeline: **don't**. The HARD RULE list + the Decision Tree + the section above are the entire enforcement surface. Anything else is over-engineering.

## Related References

- `references/tiktok-audio-only-transcript-path.md` — TikTok video-stream blocked → audio-only download + direct Whisper (skip ffmpeg WAV extraction)
- `references/tiktok-full-video-path.md` — TikTok video stream available → full MP4 download → ffmpeg WAV → mlx_whisper SRT + optional visual frame analysis (cho competitor research, content creator analysis)
- `references/exa-fetch-fallback-no-subs.md` (NEW 2026-07-11) — khi yt-dlp --list-subs empty cho Vietnamese channels → mcp__exa__web_fetch_exa với YouTube watch URL → full transcript verbatim in ~3s, no GPU
- `tiktok-transcript-pipeline` (sibling skill) — adds the analysis layer on top of extraction. Load when user asks "phân tích" not just "transcript".

## 🧠 Pre-Installed Tools (Default Knowledge — 2026-06-26)

**These tools are PERMANENTLY INSTALLED. Em does NOT need to check before each use.**

- **mlx-whisper**: `/Users/tuananh4865/whisper-env/bin/mlx_whisper` — large-v3 model, 2.9 GB
- **yt-dlp, ffmpeg, ffprobe**: Already installed system-wide
- **Default model**: `mlx-community/whisper-large-v3-mlx` (Vietnamese optimized)
- **DO NOT** check `pip list` / `find` for models before each task — just use it
- **Only check installation IF a command actually fails with "command not found"**
