---
title: TikTok Video Analysis Workflow
created: 2026-06-06
updated: 2026-06-18
type: concept
tags: [tiktok, research, video-analysis, workflow, whisper]
confidence: high
relationships: [tiktok-viral-script, tiktok-content-writing-2026, content-creator-script-style]
---

# TikTok Video Analysis Workflow (Updated June 18, 2026)

**⚠️ CRITICAL: computer_use + Chrome are BROKEN on this system.** Chrome runs but `bounds=0` — screenshot capture fails every time. browser-harness daemon may also be offline. **DO NOT try browser-based TikTok access — it WILL fail.** Use the yt-dlp pipeline below instead.

When Anh shares a TikTok URL for analysis (not for script writing), follow this pipeline.

## Trigger
- Anh shares a TikTok video URL with request like "phân tích video này", "tải và phân tích", "review video"

## Pipeline (5 steps) — TRANSCRIPT FIRST, VISION SECOND

### Step 0: Get direct video URL from web search (REQUIRED)

yt-dlp needs a direct video URL — you can't give it a channel URL or short share URL and expect it to work. **Always get the direct `/video/` URL first.**

```bash
# Search for latest video from a TikTok channel
mcp_MiniMax_web_search(query="@duymuoi TikTok latest video 2026")
```

Look for `vm.tiktok.com/` or `tiktok.com/video/` URLs in the results. Extract the full URL.

**If search doesn't return direct video URLs:** Try a more specific query:
```bash
mcp_MiniMax_web_search(query="site:tiktok.com @username video review")
```

**Extract video IDs from search results:**
- Short URLs (`vm.tiktok.com/ZSQYqMofg/`) — redirect to `tiktok.com/video/{id}`
- Full URLs already contain the video ID: `/video/7621544652222926088`

### Step 1: Download with yt-dlp

```bash
mkdir -p ~/.hermes/cron/tiktok-monitor/$(date +%Y-%m-%d)/videos/
yt-dlp -o "~/.hermes/cron/tiktok-monitor/$(date +%Y-%m-%d)/videos/[channel]_[n].mp4" \
  "https://vm.tiktok.com/..."
```

⚠️ **ALWAYS quote the URL** — parentheses in short URLs (`vt.tiktok.com/ZSQYqMofg/`) cause bash syntax error "unexpected token '('. Wrap in double quotes.

**No cookies needed** — yt-dlp downloads TikTok videos without authentication on this system (June 2026).

Output: MP4 file saved to cron monitor directory.

### Step 2 (🔥 NEW 2026-06-18): Whisper transcript FIRST, then vision frames SECOND

**🔥 NEW PREFERENCE (Tuấn Anh 2026-06-18):** *"Tải video về được thì dùng whisper mà transcript cho nhanh chứ!"* — Do NOT inspect frames one-by-one. **Transcript first, vision second.**

```bash
# 2a. Extract audio (16kHz mono WAV)
ffmpeg -y -i /path/to/video.mp4 \
  -vn -acodec pcm_s16le -ar 16000 -ac 1 \
  /tmp/video.wav

# 2b. Transcribe with mlx_whisper (~20s for 43s video, accurate Vietnamese)
mlx_whisper /tmp/video.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi --task transcribe \
  --output-format srt --output-dir /tmp/transcript
```

**Why transcript first:**
- Vietnamese speech → text → 90% of analysis done (hook, body, CTA, persuasive numbers)
- Vision frame analysis only needed for visual-only info: text overlay, B-roll, color/tone, talking head vs cinematic
- **43s video = 20s transcription** vs 30-60s of vision frame analysis (3-4× faster)

**Tool chain verified 2026-06-18:**
- ✅ `mlx-community/whisper-large-v3-mlx` — cached locally, ~20s for 43s video
- ❌ `mlx-community/whisper-small` — Repository Not Found (401)
- ❌ `lm studio` (lms) — "No models loaded" error, requires manual setup
- ❌ `vision_analyze` (Hermes native) — same "No models loaded" failure
- ✅ `mcp_MiniMax_understand_image` — fallback for visual analysis on key frames

### Step 3: Visual analysis (SELECTIVE — only key frames)

After transcript, only inspect frames for visual-only info NOT captured in transcript:
- Frame 1 (start) — text overlay (hook visual)
- Frame ~25% — visual setup (talking head? B-roll? cinematic?)
- Frame ~50% — middle visual change
- Frame ~75% — pivot/climax visual
- Frame last — CTA visual

```bash
ffmpeg -y -i /path/to/video.mp4 \
  -vf "select='eq(n\,15)+eq(n\,90)+eq(n\,180)+eq(n\,270)+eq(n\,350)',scale=640:-1" \
  -vsync vfr -q:v 2 /tmp/frame_%02d.jpg
```

Then `mcp_MiniMax_understand_image` for each frame — only what's NOT in transcript.

### Step 4: Synthesize into analysis report

Compile findings into structured report. See template below.

## Analysis Report Structure

```markdown
## Video Summary
- Kênh: @username — niche/positioning
- Video: [description], [duration]s

## Hook Analysis
| Type | Example | Effectiveness |
|------|---------|---------------|
| ... | ... | ... |

## Script Structure (5-part)
| Part | Present? | Quality |
|------|----------|---------|
| Hook (0-3s) | ✅/❌ | ... |
| Content (3-15s) | ... | ... |
| Tension (15-40s) | ... | ... |
| Pivot (40-50s) | ... | ... |
| CTA | ... | ... |

## Content Style Assessment
- Storytelling: ✅/❌
- Gen Z slang: ✅/❌
- Text overlay: ✅/❌
- Voice quality: ...

## Scoring Rubric

| Criteria | Score | Notes |
|----------|-------|-------|
| Hook | /10 | |
| Structure | /10 | |
| Storytelling | /10 | |
| Gen Z slang | /10 | |
| CTA | /10 | |
| **Total** | **/50** | |

## Content Style Classification

| Style | Characteristics | Best for |
|-------|-----------------|----------|
| **Educational/Brand Building** | Formal language, weak CTA, case study, no Gen Z slang | Course creators, personal brand |
| **TikTok Shop Direct Sales** | Casual "anh + mấy con vợ", Gen Z slang, strong CTA, urgency | Affiliate, product sales |
| **Entertainment** | Funny, no sales intent, pure engagement | Brand awareness |
| **Storytelling/POV** | Narrative arc, emotional, personal experience | Trust-building, complex products |

## Key Insights
1. ...
2. ...

## Recommendations for Anh
- What to borrow/avoid from this video
- Content style match for Anh's TikTok Shop goal
```

---

## Known Limitations

### computer_use + Chrome BROKEN on this system (June 2026)
- Chrome runs but `bounds=0` — screenshot capture fails
- browser-harness daemon may be offline
- **Do NOT try browser-based TikTok access** — it will fail
- Use yt-dlp with web-search-discovered URLs instead

### MCP vision requires ABSOLUTE paths (June 8, 2026 — discovered)
- `mcp_MiniMax_understand_image` does NOT expand `~` in file paths
- ❌ FAILS: `~/.hermes/cron/tiktok-monitor/2026-06-08/videos/frame_001.jpg`
- ✅ WORKS: `/Users/tuananh4865/.hermes/cron/tiktok-monitor/2026-06-08/videos/frame_001.jpg`
- **Always use full absolute paths** when calling image understanding tools

### Audio-only download detection (June 8, 2026 — discovered)
- yt-dlp sometimes downloads as audio only when video is deleted/privated/restricted
- If download shows `bytevc1_1080p` → video ✅
- If download shows `audio` → video was audio-only (likely deleted/restricted content)
- **Action**: If audio-only, skip that video and note it in report. Do NOT attempt frame extraction on audio files.

### MCP vision timeout
- `mcp_MiniMax_understand_image` may timeout on first attempt (120s limit)
- If timeout: try one frame at a time, or skip to next step with partial data

### video_analyze failure
- `video_analyze` requires a model loaded in LMS — often not available
- Fallback: use ffmpeg frame extraction + image understanding instead

### yt-dlp --flat-playlist timeout
- `--flat-playlist` on channel URLs times out (TikTok returns no playlist JSON)
- **Workaround:** Get individual video URLs from web search instead

### 🆕 Whisper transcript fallback (NEW 2026-06-18)
- If mlx_whisper fails (model not cached, network error), fallback to:
  1. Try smaller model `mlx-community/whisper-tiny-mlx` (less accurate but lighter)
  2. If audio has no speech (silent TikTok slideshow), skip transcript — vision only
  3. Document the gap explicitly in the report

---

## Source
- Session: 2026-06-07 — analyzed @duymuoi and @anhsacanh.vn videos
- Key finding: yt-dlp works WITHOUT cookies; web search for URL discovery is the critical first step
- Tool chain: mcp_MiniMax_web_search → yt-dlp → ffmpeg → MiniMax understand_image

- **UPDATE 2026-06-18:** Tuấn Anh's preference correction — "Tải video về được thì dùng whisper mà transcript cho nhanh chứ!" Updated Step 2 + Step 3 to use **transcript-first, vision-second** approach. New tool chain: `yt-dlp → ffmpeg WAV → mlx_whisper → mcp_MiniMax_understand_image (selective frames)`. Vietnamese accuracy with `mlx-community/whisper-large-v3-mlx` is sufficient for analyzing Vietnamese TikTok content without needing multiple vision frames. 3-4× faster end-to-end (43s video: 20s transcript + 5-6 frames vs 30-60s of 12+ frame analysis).
