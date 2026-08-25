# ⚠️ PITFALL: Silent video render STATIC — Diagnostic + Fix (verified V7.2, 18/07)

**Cost when missed:** 3 rebuilds of clip_0003 (V4/V5/V6) before this was caught. User says "đơ" / "làm qua loa cho xong" = first-class failure. NEVER ship a clip until this diagnostic passes.

## Why it happens

HyperFrames CLI renders headless Chrome. **`<video>` elements are NOT played during render** — only the first frame is captured. The `.mov` silent output therefore has 1 frame of the video-bg repeated for the full duration. If you composite this with ffmpeg overlay onto the source video, the overlay paints that 1 static frame ON TOP of the source's real motion, killing the visible motion in the final file.

## Symptoms (all observed)

- Final `.mp4` has bit rate ~400 Kbps (vs ~4 Mbps for a working file) — overlay of repeated frame compresses well
- Pixel diff between any two frames in the final file: 0-150 in face/chin/hand regions (real motion source has 150-400)
- "Clip looks static when I play it" — user reports this

## Diagnostic recipe (run BEFORE shipping)

```bash
# 1. Check the silent .mov itself, NOT the composited final
# Extract 2 frames 50s apart from output_silent.mov, sample a CLEAN region
# (no glass overlay → e.g. Y=200 top-left corner)
ffmpeg -y -i output_silent.mov -ss 5 -frames:v 1 -update 1 -q:v 2 /tmp/diag_t5.png
ffmpeg -y -i output_silent.mov -ss 60 -frames:v 1 -update 1 -q:v 2 /tmp/diag_t60.png

# 2. Diff pixels at clean spot (top-left, NO overlay) — should be > 30 if video played
python3 -c "
from PIL import Image
a, b = Image.open('/tmp/diag_t5.png'), Image.open('/tmp/diag_t60.png')
d = sum(abs(p1-p2) for p1,p2 in zip(a.getpixel((200,200)), b.getpixel((200,200))))
print(f'top-left diff: {d}')  # 0 = STATIC BUG, >30 = working
"

# 3. Also verify the .mov has alpha (transparency for glass cards)
python3 -c "
from PIL import Image
img = Image.open('/tmp/diag_t5.png').convert('RGBA')
print(f'alpha at face Y=600: {img.getpixel((540,600))[3]}')  # should be <50 if no glass there
"
```

## ⚠️ Common wrong diagnostic

**Sampling only the top-left background corner** (e.g. `X=200, Y=200`) — that region has no motion in TALKING-HEAD source clips even when video works. You'll see `d=0` and report STATIC incorrectly. **Sample ≥3 regions: face (540, 900), chin (540, 1100), hand-mic (600, 1100)**. Real motion source shows diff 150-400 in those regions.

## Working fix (3 steps)

```html
<!-- STEP 1: HTML — DISABLE video bg completely -->
<style>.bg-video-wrap { display: none; }</style>
<!-- (No <video> rendering during HyperFrames headless render anyway) -->
```

```bash
# STEP 2: Render silent with alpha
npx hyperframes render --format mov --output output_silent.mov
# Must be --format mov (MP4 has no alpha channel)
```

```bash
# STEP 3: Composite — source video as base, transparent overlay on top
ffmpeg -y \
  -i source.mp4 \
  -i output_silent.mov \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg]; \
                   [1:v]scale=1080:1920,format=yuva420p[v1]; \
                   [bg][v1]overlay=0:0:eof_action=pass[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset slow -crf 18 -b:v 8M \
  -c:a aac -b:a 128k -shortest \
  final.mp4
```

Bit rate target: **6-8 Mbps** (CRF 18 + preset slow). Working file at 400 Kbps = undercompressed overlay of static frame = bug.

## Anti-pattern (don't do)

- ❌ `display: block` on `.bg-video-wrap` and assume HyperFrames will play the video
- ❌ Render silent as `.mp4` (no alpha — overlay kills source motion)
- ❌ Composite with `-c:v copy` (no re-encode of overlay means full overlay bitstream passes through)
- ❌ Verify motion by sampling only top-left background corner
- ❌ Report "xong rồi anh" without bit rate + multi-region pixel diff

## See also

- `references/v7-liquid-glass-css-standards.md` — the V7 CSS that the silent overlay renders
- `references/verify-frame-checklist.md` — broader per-frame verification routine
- `references/clip-0003-v5-final-fix-transparent-overlay-2026-07-18.md` — the case study that produced this fix
