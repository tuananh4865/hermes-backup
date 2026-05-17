---
name: manim-video
description: "Manim CE animations: 3Blue1Brown math/algo videos."
version: 1.0.0
platforms: [linux, macos, windows]
---

# Manim Video Production Pipeline

## When to use

Use when users request: animated explanations, math animations, concept visualizations, algorithm walkthroughs, technical explainers, 3Blue1Brown style videos, or any programmatic animation with geometric/mathematical content. Creates 3Blue1Brown-style explainer videos, algorithm visualizations, equation derivations, architecture diagrams, and data stories using Manim Community Edition.

## Creative Standard

This is educational cinema. Every frame teaches. Every animation reveals structure.

**Before writing a single line of code**, articulate the narrative arc. What misconception does this correct? What is the "aha moment"? What visual story takes the viewer from confusion to understanding? The user's prompt is a starting point — interpret it with pedagogical ambition.

**Geometry before algebra.** Show the shape first, the equation second. Visual memory encodes faster than symbolic memory. When the viewer sees the geometric pattern before the formula, the equation feels earned.

**First-render excellence is non-negotiable.** The output must be visually clear and aesthetically cohesive without revision rounds. If something looks cluttered, poorly timed, or like "AI-generated slides," it is wrong.

**Opacity layering directs attention.** Never show everything at full brightness. Primary elements at 1.0, contextual elements at 0.4, structural elements (axes, grids) at 0.15. The brain processes visual salience in layers.

**Breathing room.** Every animation needs `self.wait()` after it. The viewer needs time to absorb what just appeared. Never rush from one animation to the next. A 2-second pause after a key reveal is never wasted.

**Cohesive visual language.** All scenes share a color palette, consistent typography sizing, matching animation speeds. A technically correct video where every scene uses random different colors is an aesthetic failure.

## Prerequisites

Run `scripts/setup.sh` to verify all dependencies. Requires: Python 3.10+, Manim Community Edition v0.20+ (`pip install manim`), LaTeX (`texlive-full` on Linux, `mactex` on macOS), and ffmpeg. Reference docs tested against Manim CE v0.20.1.

### Fallback: PIL + ffmpeg (macOS / no-manim)

If manim installation fails (C extension compilation errors, missing LaTeX), use the **PIL frames + ffmpeg** pipeline instead. This is reliable on macOS with system fonts:

```bash
# Generate 1920×1080 frames with PIL
python3 -c "
from PIL import Image, ImageDraw, ImageFont
FONT = '/System/Library/Fonts/Menlo.ttc'
f = ImageFont.truetype(FONT, 72)
img = Image.new('RGB', (1920, 1080), '#0d1117')
draw = ImageDraw.Draw(img)
draw.text((100, 100), 'HELLO', fill='white', font=f)
img.save('frames/frame_0001.png')
"

# Stitch to video
ffmpeg -y -framerate 30 -i frames/frame_%04d.png \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p output.mp4
```

**Key font on macOS:** `/System/Library/Fonts/Menlo.ttc` — avoid `/System/Library/Fonts/Monaco.dfont` which may fail to load on some setups.

## Modes

| Mode | Input | Output | Reference |
|------|-------|--------|-----------|
| **Concept explainer** | Topic/concept | Animated explanation with geometric intuition | `references/scene-planning.md` |
| **Equation derivation** | Math expressions | Step-by-step animated proof | `references/equations.md` |
| **Algorithm visualization** | Algorithm description | Step-by-step execution with data structures | `references/graphs-and-data.md` |
| **Data story** | Data/metrics | Animated charts, comparisons, counters | `references/graphs-and-data.md` |
| **Architecture diagram** | System description | Components building up with connections | `references/mobjects.md` |
| **Paper explainer** | Research paper | Key findings and methods animated | `references/scene-planning.md` |
| **3D visualization** | 3D concept | Rotating surfaces, parametric curves, spatial geometry | `references/camera-and-3d.md` |

## Stack

Single Python script per project. No browser, no Node.js, no GPU required.

| Layer | Tool | Purpose |
|-------|------|---------|
| Core | Manim Community Edition | Scene rendering, animation engine |
| Math | LaTeX (texlive/MiKTeX) | Equation rendering via `MathTex` |
| Video I/O | ffmpeg | Scene stitching, format conversion, audio muxing |
| TTS | ElevenLabs / Qwen3-TTS (optional) | Narration voiceover |

## Pipeline

```
PLAN --> CODE --> RENDER --> STITCH --> AUDIO (optional) --> REVIEW
```

1. **PLAN** — Write `plan.md` with narrative arc, scene list, visual elements, color palette, voiceover script
2. **CODE** — Write `script.py` with one class per scene, each independently renderable
3. **RENDER** — `manim -ql script.py Scene1 Scene2 ...` for draft, `-qh` for production
4. **STITCH** — ffmpeg concat of scene clips into `final.mp4`
5. **AUDIO** (optional) — Add voiceover and/or background music via ffmpeg. See `references/rendering.md`
6. **REVIEW** — Render preview stills, verify against plan, adjust

### Glow Star with Multi-Layer Glow

```python
def draw_star(draw, cx, cy, r, color, glow_alpha=0):
    """Draw a 5-pointed star with optional glow layers"""
    points = []
    for i in range(10):
        angle = math.pi * i / 5 - math.pi / 2
        radius = r if i % 2 == 0 else r * 0.4
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    # Glow layers (soft outer glow)
    if glow_alpha > 0:
        for layer in range(3, 0, -1):
            expand = layer * 2
            glow_points = []
            for i in range(10):
                angle = math.pi * i / 5 - math.pi / 2
                radius = r * (1 + expand * 0.3) if i % 2 == 0 else r * 0.4 * (1 + expand * 0.3)
                x = cx + radius * math.cos(angle)
                y = cy + radius * math.sin(angle)
                glow_points.append((x, y))
            alpha = int(glow_alpha * 40 / layer)
            if alpha > 0:
                draw.polygon(glow_points, fill=(255, 215, 0, alpha))
    draw.polygon(points, fill=color)
```

### Star Motion Trail (Vệt Mờ)

```python
def draw_star_trail(draw, cx, cy, r, color, vy, progress, intensity=1.0):
    """Draw star with motion trail (vệt mờ nhẹ nhàng)"""
    trail_count = 4
    for t in range(trail_count, 0, -1):
        trail_y = cy - vy * t * 3
        trail_alpha = intensity * (t / trail_count) * 0.4
        trail_r = r * (0.5 + 0.5 * t / trail_count)
        for layer in range(2, 0, -1):
            expand = layer
            glow_r = trail_r * (1 + expand * 0.5)
            glow_points = []
            for i in range(10):
                angle = math.pi * i / 5 - math.pi / 2
                radius = glow_r if i % 2 == 0 else glow_r * 0.4
                x = cx + radius * math.cos(angle)
                y = trail_y + radius * math.sin(angle)
                glow_points.append((x, y))
            alpha = int(trail_alpha * 30 / layer)
            if alpha > 0:
                draw.polygon(glow_points, fill=(255, 215, 0, alpha))
        draw_star(draw, cx, trail_y, trail_r, color, glow_alpha=trail_alpha * 0.5)
    draw_star(draw, cx, cy, r, color, glow_alpha=int(intensity * 0.8))
```

### Centered Text Helper

```python
def center_text(draw, text, font, y, color):
    """Draw text centered horizontally"""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (W - tw) // 2
    draw.text((x, y), text, fill=color, font=font)
    return x, bbox[3] - bbox[1]
```

### Layout Overlap Prevention (Dynamic Y Calculation)

```python
# Features section - calculate spacing dynamically based on item count
num_features = len(repo_data["features"])
feat_spacing = min(38, 600 // num_features)  # auto-fit based on count
feat_end_y = 360 + num_features * feat_spacing

# Secondary section (WHY IT'S TRENDING) must start AFTER features block
why_y = feat_end_y + 20  # 20px buffer
draw.text((80, why_y), "📈 WHY IT'S TRENDING", fill=GOLD, font=f_small)
for i, info in enumerate(repo_data["more_info"]):
    typing_text(f"• {info}", 100, why_y + 33 + i * 32, f_small, TEXT_COLOR, ...)
```

### Winner Prominence (Crown + Extra Glow)

```python
is_winner = repo_data.get("rank") == "#1"

if is_winner:
    # Extra glow layers
    for glow_i in range(5, 0, -1):
        draw.text((75 - glow_i, 50), repo_data["rank"], fill=c_hex + "40", font=f_rank_p)
    draw_glow(draw, 75, 50, repo_data["rank"], f_rank_p, c_hex, 4)
    draw.text((80, 55), repo_data["rank"], fill=c_hex, font=f_rank_p)

    # Crown emoji
    f_crown = load_font(50)
    draw.text((175, 55), "👑", fill=GOLD, font=f_crown)

    # Larger name font
    name_size = 52 if is_winner else 44
```

### RGBA with Alpha for Glow Effects

When using RGBA for transparency, convert to RGB for saving:

```python
img = Image.new('RGBA', (W, H), (13, 17, 23, 255))  # BG color with full alpha
# ... draw with alpha values ...
rgb_img = Image.new('RGB', (W, H), BG_HEX)
rgb_img.paste(img, mask=img.split()[3])
return rgb_img
```

### Scanline Overlay (Subtle CRT Effect)

```python
for y in range(0, H, 5):
    draw.line([(0, y), (W, y)], fill=(0, 0, 0, 15))
```

### Glow Pulse Animation

```python
def glow_star_pulse(i, progress, base_size=8):
    """Calculate star glow intensity with pulse"""
    pulse = 0.6 + 0.4 * math.sin(progress * 3 + i * 0.7)
    size = base_size + (i % 4) * 3
    return size, pulse
```

## PIL + ffmpeg Fallback (macOS / No-LaTeX)

When manim installation fails (C extension errors, missing LaTeX) or when only simple info-card slides are needed, use the **PIL frames + ffmpeg** pipeline. Reliable on macOS with system fonts, frame-accurate animation timing.

### Core Pattern

```python
from PIL import Image, ImageDraw, ImageFont
import subprocess, os, math

W, H = 1920, 1080
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"  # macOS safe default
BG_HEX = "#0d1117"

def load_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except:
        return None

def typing_text(draw, text, x, y, font, color, progress, progress_start, type_end):
    """Draw text with typing effect — progress 0..1"""
    if progress < progress_start:
        return
    t = min(1.0, (progress - progress_start) / type_end)
    chars = int(len(text) * t)
    if chars > 0:
        draw.text((x, y), text[:chars], fill=color, font=font)

def draw_star(draw, cx, cy, r, color):
    """Draw a 5-pointed star"""
    points = []
    for i in range(10):
        angle = math.pi * i / 5 - math.pi / 2
        radius = r if i % 2 == 0 else r * 0.4
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    draw.polygon(points, fill=color)

def draw_glow(draw, x, y, text, font, color, size=3):
    """Draw text with glow effect"""
    for i in range(size, 0, -1):
        for dx, dy in [(-i, 0), (i, 0), (0, -i), (0, i)]:
            draw.text((x + dx, y + dy), text, fill=color, font=font)
```

### Timing Presets for Typing Animation

| Preset | TYPE_END | PAUSE_END | Result at 6s/slide |
|--------|----------|-----------|-------------------|
| Fast typing | 0.12 | 0.73 | 0.72s type + 3.66s read + 1.62s transition |
| Medium typing | 0.18 | 0.73 | 1.08s type + 3.30s read + 1.62s transition |
| Slow typing | 0.25 | 0.70 | 1.50s type + 2.70s read + 1.80s transition |

### Layout Overlap Prevention

When revealing multi-section content (features → "WHY IT'S TRENDING" → link), calculate final Y positions BEFORE coding. Features at y=360, 6 items × 42px = ends at ~580. "WHY IT'S TRENDING" at y=580 → overlaps. Fix: place secondary section at y=635+, items at y=668 with 34px spacing.

### Scanline Overlay

```python
for y in range(0, H, 5):
    draw.line([(0, y), (W, y)], fill=(0, 0, 0, 20))
```

### When to Use PIL+ffmpeg vs Manim

| Scenario | Tool |
|----------|------|
| Math animations, geometric proofs | Manim |
| Info-card slides, repo showcases | PIL+ffmpeg |
| Text-heavy typing effects on dark BG | PIL+ffmpeg |
| 3D objects, camera moves | Manim |

**macOS font:** `/System/Library/Fonts/Menlo.ttc` — avoid `Monaco.dfont`.

## Project Structure

```
project-name/
  plan.md                # Narrative arc, scene breakdown
  script.py              # All scenes in one file
  concat.txt             # ffmpeg scene list
  final.mp4              # Stitched output
  media/                 # Auto-generated by Manim
    videos/script/480p15/
```

## Creative Direction

### Color Palettes

| Palette | Background | Primary | Secondary | Accent | Use case |
|---------|-----------|---------|-----------|--------|----------|
| **Classic 3B1B** | `#1C1C1C` | `#58C4DD` (BLUE) | `#83C167` (GREEN) | `#FFFF00` (YELLOW) | General math/CS |
| **Warm academic** | `#2D2B55` | `#FF6B6B` | `#FFD93D` | `#6BCB77` | Approachable |
| **Neon tech** | `#0A0A0A` | `#00F5FF` | `#FF00FF` | `#39FF14` | Systems, architecture |
| **Monochrome** | `#1A1A2E` | `#EAEAEA` | `#888888` | `#FFFFFF` | Minimalist |

### Animation Speed

| Context | run_time | self.wait() after |
|---------|----------|-------------------|
| Title/intro appear | 1.5s | 1.0s |
| Key equation reveal | 2.0s | 2.0s |
| Transform/morph | 1.5s | 1.5s |
| Supporting label | 0.8s | 0.5s |
| FadeOut cleanup | 0.5s | 0.3s |
| "Aha moment" reveal | 2.5s | 3.0s |

### Typography Scale

| Role | Font size | Usage |
|------|-----------|-------|
| Title | 48 | Scene titles, opening text |
| Heading | 36 | Section headers within a scene |
| Body | 30 | Explanatory text |
| Label | 24 | Annotations, axis labels |
| Caption | 20 | Subtitles, fine print |

### Fonts

**Use monospace fonts for all text.** Manim's Pango renderer produces broken kerning with proportional fonts at all sizes. See `references/visual-design.md` for full recommendations.

```python
MONO = "Menlo"  # define once at top of file

Text("Fourier Series", font_size=48, font=MONO, weight=BOLD)  # titles
Text("n=1: sin(x)", font_size=20, font=MONO)                  # labels
MathTex(r"\nabla L")                                            # math (uses LaTeX)
```

Minimum `font_size=18` for readability.

## Layout Pitfalls (Progressive Disclosure)

When building slides that reveal content in stages (e.g., features → "WHY IT'S TRENDING" → link), calculate the final Y position BEFORE writing animation code. Progressive sections that pile up can overlap if spacing is underestimated.

**Common overlap pattern:**
- Features section starts at y=320, renders 6 items × 42px spacing = ends at ~580
- "WHY IT'S TRENDING" placed at y=580 → overlaps last feature
- Fix: place secondary section at y=635+ (below the features block)

**Calculation rule:** If section A starts at Y and reveals N items at S px spacing, section B must start at Y + (N × S) + buffer. For 6 features at 42px = 252px + header buffer → section B starts ≥ 580 + buffer.

**Safe spacing values for 1080p slides:**
- Feature item: 42px line height, header at +5px above first item
- "WHY IT'S TRENDING" header: y=635, items at y=668 with 34px spacing
- GitHub link: y=H-80 (bottom safe zone)

## Timing Presets (Typing + Pause)

For text-reveal animations where the user wants fast typing followed by a long pause to read:

| Preset | TYPE_END | PAUSE_END | Use case |
|--------|----------|-----------|----------|
| Fast typing | 0.12 (12% of slide) | 0.73 (73%) | Quick clips, social media |
| Medium typing | 0.18 (18%) | 0.73 | Standard explainer |
| Slow typing | 0.25 (25%) | 0.70 | Educational, detailed |

At 6s/slide: TYPE_END=0.12 → ~0.72s typing, PAUSE_END=0.73 → ~3.66s reading time.

### Per-Scene Variation

Never use identical config for all scenes. For each scene:
- **Different dominant color** from the palette
- **Different layout** — don't always center everything
- **Different animation entry** — vary between Write, FadeIn, GrowFromCenter, Create
- **Different visual weight** — some scenes dense, others sparse

## Workflow

### Step 1: Plan (plan.md)

Before any code, write `plan.md`. See `references/scene-planning.md` for the comprehensive template.

### Step 2: Code (script.py)

One class per scene. Every scene is independently renderable.

```python
from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
MONO = "Menlo"

class Scene1_Introduction(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("Why Does This Work?", font_size=48, color=PRIMARY, weight=BOLD, font=MONO)
        self.add_subcaption("Why does this work?", duration=2)
        self.play(Write(title), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(title), run_time=0.5)
```

Key patterns:
- **Subtitles** on every animation: `self.add_subcaption("text", duration=N)` or `subcaption="text"` on `self.play()`
- **Shared color constants** at file top for cross-scene consistency
- **`self.camera.background_color`** set in every scene
- **Clean exits** — FadeOut all mobjects at scene end: `self.play(FadeOut(Group(*self.mobjects)))`

### Step 3: Render

```bash
manim -ql script.py Scene1_Introduction Scene2_CoreConcept  # draft
manim -qh script.py Scene1_Introduction Scene2_CoreConcept  # production
```

### Step 4: Stitch

```bash
cat > concat.txt << 'EOF'
file 'media/videos/script/480p15/Scene1_Introduction.mp4'
file 'media/videos/script/480p15/Scene2_CoreConcept.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4
```

### Step 5: Review

```bash
manim -ql --format=png -s script.py Scene2_CoreConcept  # preview still
```

## Fallback: Simple Slideshow Video (when Manim unavailable)

If `manim` is not installed and `pip install manimce` fails (common on macOS — pycairo build error even when cairo/pango are installed via brew), use this lightweight alternative for simple info-card style content:

```bash
# 1. Generate slides with Python + Pillow
python3 - << 'EOF'
from PIL import Image, ImageDraw, ImageFont

def make_slide(filename, rank, color, repo, tags, tagline, features, standout):
    img = Image.new('RGB', (1920, 1080), '#0d1117')
    draw = ImageDraw.Draw(img)
    font = lambda s: ImageFont.truetype('/System/Library/Fonts/Monaco.dfont', s)
    # ... layout logic ...
    img.save(filename)

slides = [('s1.png', '#1', '#83C167', 'repo/name', 'tags', 'tagline', [...], 'standout'), ...]
for s in slides: make_slide(*s)
EOF

# 2. Compile to MP4 with ffmpeg
ffmpeg -y -framerate 1/3 -i slide%d.png \
  -vf "scale=1920:1080,setsar=1,format=yuv420p" \
  -c:v libx264 -preset medium -crf 18 \
  final.mp4
```

**When to use this vs full Manim**:
- Manim: Animated explanations, math, geometry, algorithm visualization
- PIL+ffmpeg: Static info cards, repo showcases, data comparison slides, team metrics

## Critical Implementation Notes

### Raw Strings for LaTeX
```python
# WRONG: MathTex("\frac{1}{2}")
# RIGHT:
MathTex(r"\frac{1}{2}")
```

### buff >= 0.5 for Edge Text
```python
label.to_edge(DOWN, buff=0.5)  # never < 0.5
```

### FadeOut Before Replacing Text
```python
self.play(ReplacementTransform(note1, note2))  # not Write(note2) on top
```

### Never Animate Non-Added Mobjects
```python
self.play(Create(circle))  # must add first
self.play(circle.animate.set_color(RED))  # then animate
```

## Performance Targets

| Quality | Resolution | FPS | Speed |
|---------|-----------|-----|-------|
| `-ql` (draft) | 854x480 | 15 | 5-15s/scene |
| `-qm` (medium) | 1280x720 | 30 | 15-60s/scene |
| `-qh` (production) | 1920x1080 | 60 | 30-120s/scene |

Always iterate at `-ql`. Only render `-qh` for final output.

## References

| File | Contents |
|------|----------|
| `references/animations.md` | Core animations, rate functions, composition, `.animate` syntax, timing patterns |
| `references/mobjects.md` | Text, shapes, VGroup/Group, positioning, styling, custom mobjects |
| `references/visual-design.md` | 12 design principles, opacity layering, layout templates, color palettes |
| `references/equations.md` | LaTeX in Manim, TransformMatchingTex, derivation patterns |
| `references/graphs-and-data.md` | Axes, plotting, BarChart, animated data, algorithm visualization |
| `references/camera-and-3d.md` | MovingCameraScene, ThreeDScene, 3D surfaces, camera control |
| `references/scene-planning.md` | Narrative arcs, layout templates, scene transitions, planning template |
| `references/rendering.md` | CLI reference, quality presets, ffmpeg, voiceover workflow, GIF export |
| `references/troubleshooting.md` | LaTeX errors, animation errors, common mistakes, debugging |
| `references/animation-design-thinking.md` | When to animate vs show static, decomposition, pacing, narration sync |
| `references/updaters-and-trackers.md` | ValueTracker, add_updater, always_redraw, time-based updaters, patterns |
| `references/paper-explainer.md` | Turning research papers into animations — workflow, templates, domain patterns |
| `references/decorations.md` | SurroundingRectangle, Brace, arrows, DashedLine, Angle, annotation lifecycle |
| `references/production-quality.md` | Pre-code, pre-render, post-render checklists, spatial layout, color, tempo |

---

## Creative Divergence (use only when user requests experimental/creative/unique output)

If the user asks for creative, experimental, or unconventional explanatory approaches, select a strategy and reason through it BEFORE designing the animation.

- **SCAMPER** — when the user wants a fresh take on a standard explanation
- **Assumption Reversal** — when the user wants to challenge how something is typically taught

### SCAMPER Transformation
Take a standard mathematical/technical visualization and transform it:
- **Substitute**: replace the standard visual metaphor (number line → winding path, matrix → city grid)
- **Combine**: merge two explanation approaches (algebraic + geometric simultaneously)
- **Reverse**: derive backward — start from the result and deconstruct to axioms
- **Modify**: exaggerate a parameter to show why it matters (10x the learning rate, 1000x the sample size)
- **Eliminate**: remove all notation — explain purely through animation and spatial relationships

### Assumption Reversal
1. List what's "standard" about how this topic is visualized (left-to-right, 2D, discrete steps, formal notation)
2. Pick the most fundamental assumption
3. Reverse it (right-to-left derivation, 3D embedding of a 2D concept, continuous morphing instead of steps, zero notation)
4. Explore what the reversal reveals that the standard approach hides
