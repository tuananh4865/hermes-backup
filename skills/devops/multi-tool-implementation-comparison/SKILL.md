---
name: multi-tool-implementation-comparison
title: Compare N implementations of the same brief (3-way, 4-way, ...)
description: Class-level workflow for rendering the SAME brief via N different tools/frameworks and producing a side-by-side comparison so the user can pick the winner. Covers parallel render orchestration, contact sheet assembly, vision-AI comparison, scoring rubric, and final pick handoff. Use when user says "so sánh", "compare N versions", "thử render bằng tool A và tool B", "remotion vs manim", "hyperframes vs remotion", "best framework for X", or wants to evaluate multiple implementations of the same task without committing to one upfront.
created: 2026-07-16
type: skill
tags: [comparison, evaluation, framework, rendering, video, multi-tool]
confidence: high
---

# Multi-Tool Implementation Comparison

Class-level workflow for rendering **the same brief** via **N different tools** and producing a side-by-side comparison the user can use to pick the winner.

## When to use

Trigger when user says any of:
- "compare N versions / frameworks / tools"
- "thử render bằng tool A và tool B xem cái nào đẹp hơn"
- "so sánh Remotion vs Manim vs HyperFrames"
- "best framework for X use case"
- "không biết chọn tool nào, render thử cả 3 rồi so"
- "I want N implementations of this brief to compare"

Do NOT use for:
- Single-tool optimization (just use that tool's skill)
- Choosing 1 tool upfront (just use decision matrix in the tool's SKILL.md)
- A/B test of a single tool's variants (use that tool's own skill)

## Why this works

Most "tool X vs Y" debates online are opinion. Real comparison requires:
1. Same brief across all tools (eliminate variable)
2. Same duration / aspect / scene count (eliminate variable)
3. Same time budget (each tool gets equal render window)
4. Side-by-side frames at aligned timestamps (eliminate editing bias)
5. Independent vision-AI scoring (eliminate confirmation bias)

This skill formalizes that workflow.

## Workflow: 5-step N-way comparison

### Step 1: Confirm scope with user (1 question)

Before rendering, lock the scope. User's request might be vague.

```markdown
Em sẽ render [brief] qua 3 tool: [tool A], [tool B], [tool C].
- Duration: [30s/clip]
- Aspect: [9:16 / 16:9 / 1:1 / 1080×1080]
- Style: [cyberpunk B&W / clean reveal / etc.]
- Render time budget per tool: [60s - 10min depending on tool]
- Output: 3 MP4 files + 1 contact sheet comparison

Anh OK với plan này không? Hay anh muốn em chỉ render 1 tool và pick dựa trên decision matrix?
```

**Skip this step IF user already specified tools + scope** (e.g., "remotion vs manim vs hyperframes 30s cyberpunk").

### Step 2: Parallel render with same brief across all tools

**Render order priority:**
1. Fastest tool first → gives user a preview in <30s
2. Slowest tool in background (`background=true` + `notify_on_complete=true`)
3. Wait for slowest to finish before comparing

**Per-tool render commands** (video compare example):

| Tool | Command | Expected time (30s clip) |
|---|---|---|
| **HyperFrames** | `npx hyperframes render . -o renders/trailer.mp4 --fps 24` | ~25s |
| **Remotion** | `npx remotion render src/index.ts Trailer out/trailer.mp4 --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` | ~40s |
| **Manim** | `manim render -qm trailer.py Trailer media` (or `-ql` for fast draft) | ~3min (`-ql`) / ~10min (`-qm`) |
| **PIL + ffmpeg** | `python3 generate_frames.py && ffmpeg -y -framerate 24 -i frames/frame_%04d.png ...` | ~1min |

**Background process pattern** for slow renders:
```python
terminal(f"cd {proj} && manim render -qm trailer.py Trailer media", background=True, notify_on_complete=True)
# Continue with other work, system notifies when done
```

**When to kill background**: If you have 1 fast result and the slow tool is taking >2× its expected budget AND user has comparison in hand, kill the slow one and ship. Don't make user wait.

### Step 3: Spec verify each output

Every output MUST pass spec check before comparison:

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
  -show_entries stream=codec_name,codec_type,width,height,r_frame_rate,sample_rate \
  -of default=nw=1 FILE.mp4
```

**Pass criteria (for video compare):**
- Codec h264
- Duration within ±2s of target
- Width × height matches target aspect ratio
- r_frame_rate matches target (24fps for cinematic, 30fps for motion graphics)
- File size < 100MB (Telegram hard limit)

**If any tool fails spec check**: re-render with correct settings. Don't compare broken outputs.

### Step 4: Build contact sheet (N cols × M rows)

Layout: rows = aligned timestamps, cols = tools.

```python
from PIL import Image, ImageDraw, ImageOps
import subprocess, os

# Aligned timestamps = one per scene, equally spaced
SAMPLES = [3, 13, 17, 26]  # mid-points of 4 key scenes in 30s trailer
TILE = 640

for tool, path in tools.items():
    for ts in SAMPLES:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-ss', str(ts),
                        '-i', path, '-frames:v', '1', '-q:v', '2',
                        f'{OUTDIR}/{tool}_t{ts}.jpg'], check=False)

# Build sheet: rows × cols
COLS, ROWS = len(tools), len(SAMPLES)
sheet = Image.new('RGB', (COLS * TILE + gaps, ROWS * TILE + gaps), (15, 15, 15))
# Letterbox each frame to TILE preserving aspect
```

Save to canonical wiki folder: `/Volumes/Storage-1/Hermes/wiki/concepts/<topic>-comparison/_contact.jpg`

### Step 5: Vision-AI scoring rubric

Send contact sheet to vision tool with structured scoring prompt:

```markdown
Compare N versions of [brief] at N aligned timestamps.

Score each version 1-10 on:
- Visual coherence (does it match reference brief?)
- Typography quality (legibility, hierarchy, glow/effects)
- Texture/FX (grain, scanline, particles, etc.)
- Reference fidelity (how close to original brief's style?)

Give a 1-10 total per version with justification.
Pick a winner with specific reasons.
```

**Save full vision response as wiki reference doc** — don't trust yourself to summarize it. The verifier often catches things you missed.

### Step 6: Ship deliverables

**Canonical save folder** (consistent across sessions): `/Volumes/Storage-1/Tiktok-Tuan-Anh/` (or project-specific folder)

Save 3 artifacts:
1. **N video files** at canonical folder with descriptive names: `brief_<tool>_<resolution>_<fps>.mp4`
2. **1 contact sheet** at wiki folder: `wiki/concepts/<topic>-comparison/_contact.jpg`
3. **1 concept wiki page** with: verdict, decision matrix, when-to-use-each-tool, lessons

**Ship message format:**

```
[Brief] comparison done!

MEDIA: <canonical path>/<file>.mp4 (each)
MEDIA: <wiki path>/_contact.jpg

Verdict:
- <Tool A>: X/10
- <Tool B>: X/10
- <Tool C>: X/10

Winner: <Tool> — <reason>

Decision matrix saved to: <wiki path>/<topic>-comparison.md
```

## Time budget (3-tool compare, 30s clip each)

| Phase | Time |
|---|---|
| Setup (deps, init projects) | 5-10 min |
| Fastest tool render | 30s |
| Medium tool render | 1-2 min |
| Slowest tool render (background) | 5-10 min |
| Spec verify × 3 | 30s |
| Contact sheet assembly | 1 min |
| Vision-AI scoring | 30s |
| Wiki writeup | 2-3 min |
| **Total** | ~15-25 min |

## Pitfalls

### 1. Different aspect ratios across tools → unfair comparison

If one tool renders 1080×1080 and another renders 1920×1080, comparing them is meaningless. Lock the aspect BEFORE rendering:

```python
# Remotion
durationInFrames=24*30, width=1080, height=1080

# HyperFrames
data-width="1080" data-height="1080"

# Manim - tricky because default is 16:9. Use:
config.frame_size = (1080, 1080)  # requires editing manim.cfg or CLI flag
# OR: just pick aspect ratio that all 3 tools can do
```

**For 1:1 (1080×1080):** All 3 tools work natively. **For 9:16:** Manim needs `config.frame_size` override.

### 2. Background process timeout kills slow render at wrong moment

Foreground terminal timeout = 600s = 10 min. If your slowest tool needs 12 min, it gets killed exactly at the wrong moment.

**Fix:**
- Use `background=true` + `notify_on_complete=true` for slow tools
- OR: render at lower quality (Manim `-ql` instead of `-qm`) and accept the resolution hit
- OR: split into 2 segments and render separately

### 3. Vision-AI scoring bias from order

If you ask "compare A, B, C", vision models often anchor on first option. Randomize order in contact sheet:

```python
import random
random.shuffle(tools_list)  # shuffle tool names so labels don't bias scoring
```

Or explicitly in prompt: "Score WITHOUT looking at column order. Read each cell independently."

### 4. Kill slow background render when fast result is enough

If you already have 2 of 3 results and they tell a clear story, don't make user wait for the 3rd. Kill background, ship partial result with caveat:

```
Đã render 2/3: Remotion + HyperFrames. Manim 720p30 background render đang chạy 
~10 phút nữa mới xong. Anh muốn em đợi hay ship ngay 2 bản này?
```

### 5. Spec mismatch on bit_rate / codec breaks downstream

If one tool outputs `yuvj420p` (Remotion default) and another outputs `yuv420p` (HyperFrames default), Telegram/iPhone play both but downstream ffmpeg concat may fail. Normalize before any concat step:

```bash
ffmpeg -i input.mp4 -pix_fmt yuv420p -c:v libx264 -preset fast -crf 18 normalized.mp4
```

### 6. Contact sheet crop mismatch if frames have letterbox

If one tool's video has black bars (16:9 source → 9:16 letterbox), letterbox-pad the others to match for fair visual comparison:

```python
# Pad shorter aspect to match taller aspect with black bars
def letterbox(im, target_w, target_h, bg=(0,0,0)):
    iw, ih = im.size
    scale = min(target_w/iw, target_h/ih)
    nw, nh = int(iw*scale), int(ih*scale)
    resized = im.resize((nw, nh), Image.LANCZOS)
    canvas = Image.new('RGB', (target_w, target_h), bg)
    canvas.paste(resized, ((target_w-nw)//2, (target_h-nh)//2))
    return canvas
```

### 7. v2 iteration on winner — "v1 not cinematic enough" follow-up (2026-07-16, NEW)

After the initial N-way compare, user often replies "v1 not pretty enough, v2 needs 3D + bloom + lens flare like the reference". This is a **distinct second-pass pattern**, not part of Step 2 (initial render).

**Trigger phrases:** "ảnh không đẹp bằng clip gốc", "không giống reference", "thiếu 3D/bloom/flare", "làm lại đẹp hơn"

**Workflow for v2:**
1. Take the WINNER from v1 compare
2. Keep the SAME timeline + scene structure (so v1 → v2 is comparable)
3. Layer in reference-fidelity enhancements as a v2 file:
   - **3D depth:** CSS `transform: perspective()` + `transformStyle: preserve-3d` + multiple `translateZ` layers
   - **Bloom stack:** Multi `drop-shadow()` + multi `text-shadow` + CSS `filter: drop-shadow()` chained
   - **Lens flare:** Linear-gradient horizontal streak with `mix-blend-mode: screen` + blur
   - **Volumetric shapes:** CSS-only cubes (6 face divs with rotateX/Y) or parallax cube rotations
4. Render at SHORT duration first (e.g. 16s instead of 30s) to iterate fast
5. Re-run vision AI compare — v2 should score meaningfully higher than v1

**Code organization:** Keep v1 and v2 in SAME project, register both as separate `<Composition>` in Root.tsx. User can compare side-by-side without project-switching.

```tsx
// Root.tsx
<Composition id="TrailerV1" component={TrailerV1} ... />
<Composition id="TrailerV2" component={TrailerV2} durationInFrames={24*16} ... />
// Render via: npx remotion render src/index.ts TrailerV2 out/v2.mp4
```

**Filename convention:** `<brief>_v1_30s.mp4` + `<brief>_v2_3d_16s.mp4` — distinguish iteration + enhancement.

### 8. Invisible-clip-path bug — Remotion V2 renders 100% black (2026-07-16, NEW)

**Symptom:** V2 trailer renders 6/6 black contact sheet frames despite no error. Vision AI scores 2/10.

**Root cause:** I tried to hide inactive scenes with `clipPath: inset(top% 0 bottom% 0)` per scene wrapper. All scenes stack with `display: block` so the LARGEST clipPath wins → all scenes show through a fully-black mask.

**Bad pattern (DO NOT USE):**
```tsx
const Scene1Wrapper = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{
      clipPath: `inset(${Math.min(72, frame) * 14.16}% 0 ${Math.max(0, 72 - frame) * 14.16}% 0)`,
    }}>
      <Scene1 />
    </AbsoluteFill>
  );
};
```

**Good pattern — use early-return null to actually unmount inactive scenes:**
```tsx
const Scene1Wrapper = () => {
  const frame = useCurrentFrame();
  if (frame < 0 || frame >= 72) return null;
  return <Scene1 frame={frame} />;
};
```

**Detection signal:** If vision AI says all frames are "void/black/empty", check clipPath masks BEFORE re-rendering. Quick visual debug: render just frame 1 + 50 + 100 + 200, check if anything visible.

### 9. Manim v0.19 API breaking change — `Polyline` removed (2026-07-16, NEW)

**Symptom:** `NameError: name 'Polyline' is not defined` in Manim 0.19+.

**Cause:** Manim v0.19 removed the `Polyline` symbol from `from manim import *`.

**Workaround:**
```python
from manim import *

def make_polyline(*pts, **kw):
    """Polyline replacement for Manim v0.19 - uses VMobject.set_points_as_corners."""
    m = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pts]).set(**kw)
    m._is_polyline = True  # tag for type-checking
    return m

def is_polyline(o):
    return getattr(o, '_is_polyline', False)

# Usage:
pts = [[x, y, 0], [x+1, y+1, 0], ...]
line = make_polyline(*pts, color=GREEN, stroke_width=1.5)
```

**Why not VMobject directly:** `isinstance(o, Polyline)` will fail because Polyline is now a lambda, not a class. The `_is_polyline` attribute + helper function lets you tag + check without breaking type system.

### 10. Manim install on macOS — brew pkg-config + pycairo workaround (2026-07-16, NEW)

**Problem:** `pip install manim` fails with `metadata-generation-failed` for `pycairo` on macOS.

**Fix sequence:**
```bash
# 1. System Python is Python 3.9 (brew python 3.14 is incompatible with old pip resolver)
python3 -m venv /tmp/manim-venv
/tmp/manim-venv/bin/pip install --upgrade pip setuptools wheel

# 2. Install cairo deps via brew
brew install pkg-config

# 3. Set PKG_CONFIG_PATH for pycairo to find cairo headers
export PKG_CONFIG_PATH=/opt/homebrew/opt/cairo/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig:$PKG_CONFIG_PATH

# 4. Install pycairo then manim (chain order matters)
/tmp/manim-venv/bin/pip install pycairo
/tmp/manim-venv/bin/pip install manim  # 0.19.x works with python 3.9 venv

# 5. Verify
/tmp/manim-venv/bin/python -c 'import manim; print(manim.__version__)'
```

**Important:** Use Python 3.9 venv, NOT system Python 3.14. Manim 0.19 deps don't resolve cleanly under Python 3.14 pip.

**Time cost:** ~10 min total vs 1+ hour debugging pkg-config errors otherwise.

### 11. HyperFrames v0.7.60 init — `--example blank` flag required (2026-07-16, NEW)

**Symptom:** `hyperframes init .` fails with "Non-interactive init requires --example, --video, or --audio".

**Fix:**
```bash
hyperframes init . --example blank   # empty starter project
# NOT: hyperframes init . --non-interactive  (won't work without --example)
```

**Lint errors that don't block render:** "missing_timeline_registry" + "font_family_without_font_face" are warnings only. The `window.__timelines["main"] = root` registration is the load-bearing piece — without it, runtime animations silently don't fire. Fonts without @font-face fall back to system fonts but render still works.

## Reference: 2026-07-16 Nous trailer 3-way compare

**Brief:** 30s cyberpunk B&W analog trailer, 9 scenes, 1080×1080 aspect.

| Tool | Resolution | FPS | Render time | File size | Visual score |
|---|---|---:|---:|---:|---:|
| HyperFrames | 1920×1080 | 24 | 25s | 1.5 MB | 9.0/10 🏆 |
| Remotion | 1080×1080 | 24 | 40s | 6.5 MB | 6.25/10 |
| Manim | 854×480 | 15 | ~3 min (`-ql`) | 0.85 MB | 4.5/10 |

**Winner: HyperFrames** — best FX (CSS grain), fastest 1080p, best B&W fidelity.

**Why Manim lost:** default resolution 480p15 is unfair comparison. `-qm` would have taken ~10 min background render. If aspect matched and quality was 720p30, Manim would have scored higher.

**Lesson:** When comparing tools, normalize quality first. Otherwise the comparison conflates "tool capability" with "default config quality".

## Related

- `tiktok-competitor-deep-analysis` — sibling for comparing 1 brief across N competitor implementations (TikTok videos, not tools)
- `video-clip-qa-loop` — single-tool iterative loop (different scope: same tool, N versions until QA pass)
- `remotion`, `manim-video`, `hyperframes` — per-tool skills with their own pitfall libraries
- `adversarial-content-verifier` — useful for vision-AI scoring step