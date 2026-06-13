---
name: youtube-transcript-extractor
title: YouTube Transcript Extractor (YouTube + Shorts + TikTok)
description: Extract full transcripts from YouTube videos, YouTube Shorts, and TikTok for content creation and research. Includes Vietnamese subtitle strategy + local Whisper fallback for videos without captions, plus TikTok audio-only path when video stream is blocked.
created: 2026-05-01
updated: 2026-06-13
type: skill
tags: [youtube, content, transcript, tiktok, whisper]
confidence: high
---

# YouTube Transcript Extractor

Extract full transcripts from YouTube videos, YouTube Shorts, and TikTok for content creation/research.

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
    │         Nếu chỉ có "audio mp3 audio only" → xem references/tiktok-audio-only-transcript-path.md
    │         Workflow: download MP3 → feed thẳng vào Whisper (skip ffmpeg step)
    │
    ├─ Video tiếng Việt? (90% trường hợp của anh)
    │   YES → dùng yt-dlp --write-auto-sub --sub-lang vi-orig,vi (xem "Vietnamese Subtitle Strategy")
    │          → SRT chất lượng cao, NHANH, không cần GPU
    │
    └─ Video tiếng Anh / không có sub?
        → Local Whisper fallback (xem "Local Whisper Fallback")
        → CHỉ dùng khi không còn cách nào khác
```

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

**Step 4: When no auto-subs (foreign language, no captions)**
Fall back to local Whisper via `mlx_whisper` (Apple Silicon). See "Local Whisper Fallback" section below.

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

---

## Related References

- `references/tiktok-audio-only-transcript-path.md` — TikTok video-stream blocked → audio-only download + direct Whisper (skip ffmpeg WAV extraction)
