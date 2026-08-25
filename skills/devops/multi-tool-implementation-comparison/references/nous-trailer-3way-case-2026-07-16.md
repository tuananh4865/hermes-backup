---
title: Reference Case — Nous Trailer 3-way Compare (2026-07-16)
created: 2026-07-16
type: reference
tags: [case-study, comparison, video, remotion, manim, hyperframes]
---

# Reference Case: Nous Trailer 3-way Compare

**Date:** 2026-07-16
**Brief:** Recreate a 30s cyberpunk B&W analog trailer inspired by NOUS Accelerated Business Hackathon promo (66s, 2160×2160).
**Tools compared:** Remotion v4.0 + Manim v0.19 + HyperFrames v0.7.60

## Outcome

| Tool | Resolution | FPS | Render time | File | Verdict |
|---|---|---:|---:|---:|---|
| **HyperFrames** | 1920×1080 | 24 | 25s | 1.5 MB | 🏆 9.0/10 |
| Remotion | 1080×1080 | 24 | 40s | 6.5 MB | 6.25/10 |
| Manim | 854×480 | 15 | ~3 min | 0.85 MB | 4.5/10 |

**Winner: HyperFrames** for analog-texture aesthetic + 1080p default + fast iteration.

## What worked

### Step 1: Setup (parallel)
- Remotion: `npm install` of 4 packages (Remotion 4.0.290 + React 19 + TS 5.7.3). Hit `ETARGET` on `typescript@5.5.0` (doesn't exist) — fixed to `5.7.3`.
- Manim: pycairo + libffi + pkg-config via Homebrew + venv + `pip install manim` + `pip install importlib_metadata` (Python 3.9 needs this).
- HyperFrames: `hyperframes init . --example blank` (required flag).

### Step 2: Parallel render
- HyperFrames first → 25s → preview ready
- Remotion second → 40s → preview ready
- Manim in background → 10 min projected (`-qm`). Killed at ~3 min after 2/3 results were enough for comparison.

### Step 3: Spec verify
All 3 outputs passed:
- h264 codec ✅
- Duration within ±2s target (30s) ✅
- Aspect: 1080×1080 (R), 1920×1080 (HF), 854×480 (M - unfair comparison)

### Step 4: Contact sheet
12 frames extracted (4 timestamps × 3 tools) via ffmpeg. Assembled into 3-col × 4-row sheet using PIL letterbox-preserving aspect.

### Step 5: Vision-AI scoring
Sent contact sheet + structured scoring rubric. Vision-AI picked HyperFrames as winner with specific reasons:
- CSS filters = best grain/scanline quality
- Easing mượt nhất (fade-in + glow)
- 1080p default (Manim only 480p15 in -ql)
- Tone B&W xuyên suốt

### Step 6: Ship
- 3 MP4 saved to `/Volumes/Storage-1/Tiktok-Tuan-Anh/`
- Contact sheet at `/Volumes/Storage-1/Hermes/wiki/concepts/trailer-3way-comparison/_contact.jpg`
- Wiki concept page written with full decision matrix

## What I learned

1. **Manim resolution comparison unfair** — `-ql` default = 480p15. To get 720p30 you need `-qm` which takes ~10 min background. If I'd said "Manim at 720p30 vs HyperFrames at 1080p", verdict could flip.

2. **Vision AI scoring is highly dependent on quality normalization** — first version of comparison had Manim 480p15 visible next to HyperFrames 1080p24, vision-AI correctly noted resolution differences dominate the score. Always render at same quality OR explicitly weight resolution differences in prompt.

3. **Killing background process** — Manim `-qm` at 10 min render time was wasting session budget when 2/3 results already told the story. Killed it, used `-ql` 480p15 for comparison, flagged as caveat in wiki.

4. **HyperFrames won on 3 axes**: texture (CSS filters > React SVG > Cairo rendering), speed (25s vs 40s vs 3min), default resolution (1080p > 1080×1080 > 480p). For analog/B&W aesthetic specifically, CSS filter grain is hard to replicate in React/Manim without significant effort.

5. **Contact sheet alignment matters** — using SAME timestamps across tools (3s, 13s, 17s, 26s) at scene mid-points let vision-AI compare same narrative moments, not random frames.

## Files saved

```
/Volumes/Storage-1/Tiktok-Tuan-Anh/
├── nous_trailer_v1_30s.mp4              (Remotion)
├── nous_trailer_manim_480p15.mp4       (Manim -ql)
└── nous_trailer_hyperframes_1080p.mp4  (HyperFrames - winner)

/Volumes/Storage-1/Hermes/wiki/concepts/trailer-3way-comparison/
├── _contact.jpg                        (12-frame contact sheet)
└── trailer-3way-comparison.md          (verdict + decision matrix)

~/Documents/GitHub/
├── nous-trailer/             (Remotion source - TSX)
├── nous-trailer-manim/       (Manim source - Python)
└── nous-trailer-hyperframes/ (HyperFrames source - HTML+JS+GSAP)
```

## Reusable template

This case can be templatized for any "compare N tools" task:

```python
TOOLS = {
    'TOOL_A': {'path': '/path/to/a.mp4', 'render_cmd': '...', 'expected_time': '...'},
    'TOOL_B': {'path': '/path/to/b.mp4', 'render_cmd': '...', 'expected_time': '...'},
    # ...
}

SAMPLES = [scene_midpoints]  # aligned timestamps per scene

# 1. Parallel render (slowest in background)
for tool, cfg in TOOLS.items():
    if cfg['expected_time'] < '5min':
        run_sync(cfg['render_cmd'])
    else:
        terminal(cfg['render_cmd'], background=True, notify_on_complete=True)

# 2. Spec verify
for tool, cfg in TOOLS.items():
    assert verify_spec(cfg['path'])

# 3. Contact sheet
extract_frames(TOOLS, SAMPLES, OUTDIR)
build_contact_sheet(OUTDIR, TOOLS.keys(), SAMPLES)

# 4. Vision-AI scoring
score = vision_compare(contact_sheet, rubric=...)

# 5. Ship
save_canonical(TOOLS, '/Volumes/Storage-1/Tiktok-Tuan-Anh/')
write_wiki(score, tools=TOOLS)
```

## Pitfalls hit (captured in skill)

1. **Manim `Polyline` not defined in v0.19** — used `VMobject().set_points_as_corners()` workaround
2. **`isinstance()` doesn't accept lambda** — used `getattr(o, '_is_polyline', False)` flag pattern
3. **Manim `-qm` ~10 min render** killed at 3 min for 2/3 comparison
4. **Contact sheet cropped letterbox** mismatches if aspect ratios differ
5. **Random tool order** in vision prompt to avoid anchoring bias