# TikTok Monitor — 5-Channel Nightly Workflow (June 2026)

## Overview

Nightly cron job: monitor 5 TikTok channels, download newest 2 videos each, analyze frames, update lesson-learn files, send Telegram summary.

**Channels monitored:**
- @duymuoi
- @anhsacanh.vn
- @nguyenducduong9699
- @tam_thefox
- @goccontent

**Output:** `~/.hermes/cron/tiktok-monitor/[YYYY-MM-DD]/`

## Phase 1: Collect Video IDs + Download

### Step 1: Get fresh video IDs (NO download)

```bash
# Get top 10 video IDs from a channel — fast, no download
yt-dlp --flat-playlist --print "%(id)s" "https://www.tiktok.com/@CHANNEL_NAME" 2>/dev/null | head -10
```

**Why not download yet:** Full `yt-dlp` with video download triggers TikTok's JS challenge on some videos (error: "No video formats found"). Getting IDs first lets you filter against `seen-videos.json` before attempting download.

### Step 2: Deduplicate against seen-videos.json

```bash
# seen-videos.json format:
# {
#   "duymuoi": ["id1", "id2", ...],
#   "anhsacanh.vn": ["id1", "id2", ...],
#   ...
# }

# Cross-reference: new IDs = not in seen-videos for that channel
# Download only new IDs
```

### Step 3: Download new videos only

```bash
DATE_DIR=~/.hermes/cron/tiktok-monitor/$(date +%Y-%m-%d)/videos
mkdir -p "$DATE_DIR"
cd "$DATE_DIR"

yt-dlp -o "CHANNEL_N_1.mp4" "https://www.tiktok.com/@CHANNEL/video/ID"
```

### Step 4: Extract frames

```bash
mkdir -p frames
for f in *.mp4; do
    ffmpeg -y -i "$f" -vf fps=1 -frames:v 20 "frames/${f%.mp4}_%03d.jpg" 2>/dev/null
done
```

**Output:** 20 frames per video (fps=1 = 1 frame per second)

## Phase 2: Analyze + Update Lessons

### Analyze each video

For each video, call `mcp_MiniMax_understand_image` on the **first frame** with this prompt:

```
Analyze this TikTok video frame. Describe:
1) Visual content/what's shown
2) Any text/captions visible
3) Hook type (shock/question/stakes/visual/bold/proof)
4) Style/mood
5) Gen Z elements visible

Be specific about what makes this frame attention-grabbing.
```

### Update lesson files

Append to these files (append-only, never overwrite):

| File | Contents |
|------|----------|
| `~/.hermes/cron/tiktok-monitor/lessons/hooks.md` | Hook patterns |
| `~/.hermes/cron/tiktok-monitor/lessons/cta.md` | CTA patterns |
| `~/.hermes/cron/tiktok-monitor/lessons/storytelling.md` | Storytelling structures |
| `~/.hermes/cron/tiktok-monitor/lessons/tiktok-shop.md` | TikTok Shop-specific lessons |

**Update format:**
```markdown
## [YYYY-MM-DD] Updates

### New patterns found:

#### [Pattern Name]
- **Pattern:** [description]
- **Style:** [visual style notes]
- **Why viral:** [reason]
```

## Phase 3: Report + Telegram

### Create report

```bash
~/.hermes/cron/tiktok-monitor/[YYYY-MM-DD]/report.md
```

### Send Telegram summary

Format: <500 words
```
✅ **TikTok Monitor — [Ngày]**

**Videos analyzed:** X/10

**🔥 Top 3 Trends hôm nay**
1. [trend 1]
2. [trend 2]
3. [trend 3]

**💡 Top 3 Lessons**
1. [lesson 1]
2. [lesson 2]
3. [lesson 3]

**🎯 Recommendations cho TikTok Shop**
- [recommendation 1]
- [recommendation 2]
```

**Delivery:** Telegram chat_id: `1132914873`

## Known Failure Modes

### TikTok JS Challenge (June 9, 2026)
```
ERROR: [TikTok] VIDEO_ID: No video formats found!; please report this issue on https://github.com/yt-dlp/yt-dlp/issues?q=
```

**Cause:** TikTok returns JS challenge page instead of video data.
**Workaround:** This is per-video, not per-channel. Skip failed video, continue with others.
**No reliable retry** — JS challenge is deterministic per session.

### Duplicate Download Waste
**Problem:** Downloading 10+ videos per channel per night wastes bandwidth and storage.
**Solution:** Always get IDs first → cross-reference `seen-videos.json` → only download truly new videos.

### Frame Extraction Timeout
**Problem:** `ffmpeg` can hang on corrupted/incomplete video files.
**Solution:** Use `-y` (overwrite) and `2>/dev/null` to suppress errors. Check `ls frames/*.jpg | wc -l` after loop — expect 20 per video.

## June 9, 2026 — Session Results

| Metric | Value |
|--------|-------|
| Videos analyzed | 11/13 |
| Failed downloads | 1 (goccontent_4 — JS challenge) |
| New patterns found | 11 hook/CTA/storytelling patterns |
| Lesson files updated | 4 (hooks, cta, storytelling, tiktok-shop) |

**Top trends identified:**
1. Expert Authority + Social Proof (TikTok award + Shure mic in background)
2. Do/Don't Contrast Format (green/red boxes)
3. Raw POV Authenticity (no text overlay, lo-fi aesthetic)

**Key lesson:** Yellow text overlay remains the most reliable scroll-stopper across all 5 channels.

## June 10, 2026 — Session Results

| Metric | Value |
|--------|-------|
| Videos analyzed | 8/10 |
| Failed downloads | 1 (@goccontent — anti-bot block) |
| New patterns found | 15+ hook/CTA/storytelling patterns |
| Lesson files updated | 4 (hooks, cta, storytelling, tiktok-shop) |

**Top trends identified:**
1. Series + Listicles = Follow Acceleration ("3 YẾU TỐ" + "Tập 1/2/3")
2. Beginner-Filter Targeting ("CHO NGƯỜI MỚI XÂY KÊNH")
3. Multi-Layer Text Hierarchy (4 text layers simultaneously)

**⚠️ NEW FAILURE MODE: TikTok Anti-Bot Blocking**
- @goccontent video `7648845591035923720` — blocked by TikTok anti-bot (403/empty file)
- Workarounds to add to workflow:
  - `--user-agent "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)..."`
  - `--cookies-from-browser chrome`
  - Retry with delay: `sleep 5 && yt-dlp ...`
- **Fallback:** Mark video as `BLOCKED` in report, skip frame extraction

**Key lesson:** Multi-layer text hierarchy (red header + white sub + yellow subtitle + episode boxes) creates maximum information density for fast-scroll stopping power.