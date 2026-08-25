# Noir-Tech Cinematic Promo — Style Deconstruction Case Study (16/07/2026)

**Anh's request (verbatim):** *"Phân tích xem làm sao em có thể làm được video dạng này???"*

**Source:** `https://x.com/NousResearch/status/2077517414464410091/video/1` — promo cho **"Accelerated Business Hackathon"** (NVIDIA + Stripe + NOUS).

This is the canonical worked example for **Step 10 (Style Deconstruction + Reproducible Recipe)** of the parent `telegram-video-analysis` skill.

## Source metadata (verified via ffprobe)

| Field | Value |
|---|---|
| Container | MP4 |
| Codec | H.264 + AAC |
| Resolution | **2160×2160 (SQUARE — không phải 9:16 hay 16:9)** |
| FPS | 24 |
| Duration | 66.08s |
| Size | 119 MB |
| Audio | AAC, có nhạc nền industrial + SFX glitch |

**Critical observation:** Aspect ratio SQUARE = video này optimize cho Instagram carousel / X feed / general purpose, không phải TikTok/Reels-only. Recipe phải render master 1:1 rồi xuất variant 9:16 nếu cần.

## Download + extract workflow (commands actually run)

```bash
# 1. Download via yt-dlp with Chrome cookies (X.com requires auth)
yt-dlp --cookies-from-browser chrome \
  -f 'bv*+ba/b' --merge-output-format mp4 \
  -o ~/Downloads/nous_2077517414464410091.mp4 \
  'https://x.com/NousResearch/status/2077517414464410091/video/1?s=46'

# 2. ffprobe verify (must do FIRST before any analysis)
ffprobe -v error \
  -show_entries format=duration,size \
  -show_entries stream=codec_name,width,height,r_frame_rate \
  -of default=nw=1 \
  ~/Downloads/nous_2077517414464410091.mp4
# → h264 / 2160×2160 / 24fps / 66.08s / 119MB

# 3. Stage 1: overview montage (1 frame / 6s → 11 frames)
mkdir -p /tmp/nous-overview
ffmpeg -y -i ~/Downloads/nous_2077517414464410091.mp4 \
  -vf "fps=1/6,scale=720:-1" \
  /tmp/nous-overview/frame_%02d.jpg

# Build 3-col grid via PIL
python3 -c "
from PIL import Image
import glob, math
fs = glob.glob('/tmp/nous-overview/*.jpg')
ims = [Image.open(x).convert('RGB') for x in fs]
w, h = ims[0].size
s = Image.new('RGB', (w*3, h*math.ceil(len(ims)/3)), 'white')
for i, im in enumerate(ims):
    s.paste(im, ((i%3)*w, (i//3)*h))
s.save('/tmp/nous-overview/contact.jpg', quality=88)
"

# 4. Stage 2: detail montage (1 frame / 2s → 33 frames WITH timestamp labels)
mkdir -p /tmp/nous-detail
for t in 0 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32 34 36 38 40 42 44 46 48 50 52 54 56 58 60 62 64; do
  ffmpeg -loglevel error -y -ss $t -i ~/Downloads/nous_2077517414464410091.mp4 \
    -frames:v 1 -q:v 2 /tmp/nous-detail/f_$(printf '%02d' $t).jpg
done

python3 -c "
from PIL import Image, ImageDraw, ImageOps as IO
import glob, math, os
fs = sorted(glob.glob('/tmp/nous-detail/*.jpg'))
w, h = 400, 400
ims = [(IO.fit(Image.open(x).convert('RGB'), (w, h)),
        os.path.basename(x)[2:4] + 's') for x in fs]
s = Image.new('RGB', (w*5, h*math.ceil(len(ims)/5)), 'white')
dr = ImageDraw.Draw(s)
for i, (im, lab) in enumerate(ims):
    s.paste(im, ((i%5)*w, (i//5)*h))
    dr.text(((i%5)*w+8, (i//5)*h+8), lab, fill='red', stroke_width=2, stroke_fill='white')
s.save('/tmp/nous-detail/contact.jpg', quality=90)
"
```

**Two vision calls only** (1 per montage), NOT 33 individual frame calls:

```
Vision 1: "Phân tích contact sheet 11 frame không nhãn thời gian. 
Mô tả: nội dung, visual style, cảnh, camera, animation, typography, 
UI, compositing, màu sắc, nhịp dựng, suy luận pipeline công cụ."

Vision 2: "Contact sheet 33 frame cách 2 giây, nhãn đỏ. Đọc timeline 
chính xác: phân đoạn nào lúc nào, chữ/logo, motif, nhịp. 
Kết luận pipeline tối giản đạt 90% look."
```

## What vision returned (key signals)

**Vision 1 (overview) identified:**
- B&W high-contrast monochrome (no midtones — pushed to extreme)
- Heavy film grain + scanline + vignette + CRT bloom
- Diegetic UI (trading dashboards, CRT terminals) — visual storytelling qua "nhìn vào data"
- 3 motifs: dark server room + dark warehouse + wall-of-monitors (looping)
- Endcard trắng với logo (NOUS, NVIDIA, Stripe) = classic "echo branding"

**Vision 2 (detail) identified timeline:**
| Range | Content | Beat |
|---|---|---|
| 0-8s | Server room ambient, CRT glow | slow setup |
| 10-16s | Wall-of-monitors + "HERMES AGENT" reveal | crescendo |
| 18-24s | Warehouse + "ACCELERATED BUSINESS HACKATHON" title | kinetic |
| 26-36s | Conveyor + dashboard close-ups | data rhythm |
| 38-48s | Return to control room | motif loop |
| 50-56s | Hackathon rows + "SUBMISSIONS DUE JUNE 30 (EOD)" | CTA push |
| 58-66s | White endcard + sponsor lockup | snap cut exit |

**Emotional arc:** `ambient → reveal → kinetic → data → loop → CTA → endcard`

## The Recipe (final answer to anh)

```
AI video → Remotion → FFmpeg, KHÔNG cần After Effects

1. Tạo 8-10 scene AI (Google Flow / Kling), mỗi scene 4-8s
2. Cùng seed + bảng màu + camera language để continuity
3. Remotion dựng timeline + text + logo + glitch + flash theo frame
4. FFmpeg pass cuối: monochrome, contrast, grain, scanline, vignette, bloom
5. Sound: industrial bass + CRT hum + typing + glitch hit + sub-drop
6. Render master 2160×2160 24fps, xuất variant 9:16 nếu cần TikTok
```

**Mức khả thi:** 85-90% chất lượng bản tham chiếu với pipeline hiện có. Điểm khó nhất = continuity giữa các scene AI + sync sound design. Cách đúng = dựng **style bible + storyboard + prompt từng scene**, không generate một video dài duy nhất.

## Split: AI-generated vs code/composite

| AI-generated (90%) | Code/composite (10%) |
|---|---|
| B-roll dark room + warehouse + CRT | Timecode corner (ffmpeg drawtext) |
| Cinematic camera push-in | Title text glitch reveal (Remotion) |
| Mood lighting + atmosphere | Sponsor lockup fade (Remotion) |
| Dashboard UI mockups | Flash frames 2-4 frame white |
| | Film grain + scanline + vignette (ffmpeg) |
| | Master timeline sequencing (Remotion) |

## Style-pattern metadata (for future detection)

**Class name:** `noir-tech-cinematic-promo`

**Defining features:**
- B&W monochrome (push extreme, no midtones)
- Diegetic UI (CRT/dashboard/trading terminal) as visual storytelling
- Heavy grain + scanline + CRT glow + vignette stack
- Slow push-in or dolly camera only
- Hard cut theo nhịp nhạc, không dissolve
- Serif title cards với glitch + scanline effect
- White snap-cut endcard với sponsor lockup
- Sound: industrial bass + glitch SFX + clock ticks

**Reference moodboard:** The Matrix, Blade Runner, Mr. Robot, Severance intro, Severance titles.

**Replicate score:** 85-90% look achievable với AI video + Remotion + FFmpeg, KHÔNG cần AE.

## Anti-patterns to avoid

- ❌ Apply Step 8/9 prompt templates (pose sequence, OOTD, mirror selfie) → wrong genre
- ❌ Analyze 33 frames individually → blows context budget, loses temporal reading
- ❌ Output prose paragraph → anh skip đọc
- ❌ Recommend After Effects without checking Remotion first → Remotion + ffmpeg gives 90% in 1/3 thời gian
- ❌ Forget to specify aspect ratio of source (2160×2160 SQUARE here) → wrong pipeline assumption
- ❌ Forget audio analysis → recipe needs sound design layer

## Files generated this session

- `~/Downloads/nous_2077517414464410091.mp4` — source (119MB, 66s, square 2160×2160)
- `~/Downloads/nous_detail_contact.jpg` — 33-frame labeled montage
- `~/Downloads/nous_2077517414464410091_contact.jpg` — 11-frame overview montage

## Cost / time saved by contact-sheet pattern

**Before (Step 8 individual frame analysis):** 33+ vision calls for 66s video, ~30 min processing, blows context.

**After (Step 10 contact sheet):** 2 vision calls (1 overview + 1 detail), ~5 min processing, preserves context.

**Quality:** Detail montage with red timestamp labels gives even BETTER timeline accuracy because vision model can read "frame at 28s shows X" in one pass.

## Reusable for similar videos

This workflow generalizes to:
- Music videos với cinematic style
- Brand launch trailers
- Hackathon/event promos
- Tech explainer intros
- Film title sequences

All share: B-roll AI + monochrome + text overlays + soundtrack + endcard.

Anchors: Step 10 in `telegram-video-analysis` SKILL.md (parent), Pitfall 11/17/18 in parent skill for vision context budget, references/motion-analysis-and-ai-prompts.md for adjacent (but different) workflow.