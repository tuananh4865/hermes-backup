---
title: "Manim Agentic Video — Plan v2 (Quality Upgrade)"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [auto-filled]
---

# Manim Agentic Video — Plan v2 (Quality Upgrade)

## Goals
Từ "thô sơ và nhàm chán" → "engaging, professional motion infographic"

## Key Improvements

### 1. Easing — EVERYTHING changes with this
```python
# BAD
self.play(FadeIn(obj, run_time=1))

# GOOD — smooth ease-in-out
self.play(FadeIn(obj, run_time=1, rate_func=smooth))

# Elastic for emphasis
self.play(ScaleInFrom(obj), run_time=1, rate_func=there_and_back)

# Running start for speed feel
self.play(Write(text), run_time=0.8, rate_func=running_start)
```

### 2. Camera Movement (MovingCameraScene)
```python
# Pan left
self.play(self.camera.frame.animate.shift(LEFT * 2), run_time=3)

# Zoom in
self.play(self.camera.frame.animate.scale(0.5), run_time=2)

# Dutch angle for drama
self.play(self.camera.frame.animate.rotate(0.1 * TAU), run_time=1)
```

### 3. Kinetic Typography
```python
# Each word animates separately
words = Text("Think Plan Act Reflect").split()
for word in words:
    self.play(Write(word), run_time=0.3, rate_func=running_start)
    self.wait(0.1)
```

### 4. Particle Flow Effects (background texture)
```python
# Flowing dots/lines for energy
dots = [Dot(color=PRIMARY, radius=0.03).move_to(LEFT*7) for _ in range(20)]
self.play(*[MoveAlongPath(d, Line(LEFT*7, RIGHT*7)) for d in dots])
```

### 5. Color Breathing / Gradient Animation
```python
# Pulse effect
self.play(obj.animate.set_color(ACCENT), run_time=1, rate_func=smooth)
self.play(obj.animate.set_color(PRIMARY), run_time=1, rate_func=smooth)

# Cycle colors on loop elements
```

### 6. Staggered Group Animations
```python
from manim import LaggedStart

# Staggered fly-in — much more dynamic than sequential
self.play(LaggedStart(
    *[FadeInAndShiftFromDown(obj) for obj in group],
    lag_ratio=0.15
))
```

---

## Color Palette (Refined Neon Tech)
| Role | Hex | Usage |
|------|-----|-------|
| Background | `#0A0E14` | Deep dark blue-black |
| Primary | `#00E5FF` | Cyan — brighter, more vibrant |
| Secondary | `#FF00AA` | Magenta-pink — warmer |
| Accent | `#00FF88` | Mint green — success |
| Highlight | `#FFEE00` | Warm yellow — emphasis |
| Dim | `#2A3441` | Muted blue-grey — secondary elements |

## Typography
- Title: 52px, weight BOLD
- Keywords: animate with color pulse
- Body: 28px monospace
- Labels: 22px

## Scene-by-Scene Improvements

### S1: The Problem (Hook)
**OLD**: Simple fade in/out, static
**NEW**:
- Opening: Dark screen → particles begin to flow (subtle energy)
- Single chat bubble: Scale in với elastic easing
- Chain bubbles: Staggered fly-in từ nhiều hướng
- Question mark: Dramatic scale + glow pulse
- Camera subtle drift right as tension builds
- Easing: running_start cho mọi text appearance

### S2: The Agent Brain (Core)
**OLD**: Elements appear one by one, static positions
**NEW**:
- Center circle: Spiral-in animation
- Loop elements: Rotate-spiral-in từ center
- Keywords (REASON, PLAN, etc.): Each word appears with color wave
- Arrows connecting: Draw animation thay vì instant appear
- Entire loop: Continuous slow rotation (subtle, 1 revolution per 10s)
- Camera: Slight zoom in as loop completes

### S3: Tools Grid
**OLD**: 6 rectangles fly in, pulse each, done
**NEW**:
- Title: Kinetic typewriter effect (letter by letter)
- Grid: Cards fly in từ outside edges with staggered bounce
- Each tool: Bounce-in với elastic easing
- Icon + text: Separate animation layers
- Pulse: Color cycle cyan → magenta → green
- Background: Subtle grid pattern pulse
- Connection lines: Draw from center outward

### S4: Memory
**OLD**: Simple horizontal row, fade in
**NEW**:
- Title: Glitch-reveal effect (chars scramble then resolve)
- Timeline: Draw animation left → right
- Sessions: Fly in từ below với stagger
- "Remembered" fade: Color desaturate animation
- Arrow: Animated dash pattern (marching ants)
- Labels: Typewriter effect

### S5: Full Architecture
**OLD**: Everything appears, pulse, done
**NEW**:
- Opening: Zoom out from close-up of center
- Center circle: Pulsing glow animation
- Inner loop: Each element spirals in with rotation
- Outer elements: Fly in from edges with bounce
- Connections: Animated dashes flowing along paths
- Full system: Slow continuous rotation
- Camera: Subtle dutch angle for dynamism

### S6: Closing
**OLD**: Text fades in/out
**NEW**:
- "From assistant" → "to agent": Morph/transform animation
- Color: Gradient wave across words
- "The future of AI is agentic": Scale up với elastic bounce
- Background: Particles accelerate (builds to climax)
- Final frame: All elements fade out except key phrase
- Fade to black: Slow, 2s minimum

---

## Technical Changes

### Animation Speed Refinement
| Context | run_time | rate_func |
|---------|----------|-----------|
| Title appear | 1.5s | smooth |
| Body text | 0.8s | running_start |
| Emphasis/bounce | 1.0s | there_and_back |
| Fade transitions | 0.5s | smooth |
| Key reveals | 2.0s | smooth |
| Particles | 3-5s | linear |

### Always Use
- `rate_func=smooth` for 90% of animations
- `rate_func=running_start` for text/token reveals
- `rate_func=there_and_back` for pulsing/emphasis
- `LaggedStart` with `lag_ratio=0.1-0.2` for groups

### Never Use
- Linear rate_func (robotic)
- Instant appear without transition
- `wait()` less than 0.5s between major reveals

---

## Rendering Plan
1. Render S1-S3 first as batch (check quality/timing)
2. Fix based on preview
3. Render S4-S6
4. Stitch + ffmpeg color grade
5. Add audio if time permits

## Audio Considerations (optional v2)
- Background: Ambient electronic, 80-90 BPM
- Key moments: Soft "whoosh" transitions
- Narration: ElevenLabs voiceover
