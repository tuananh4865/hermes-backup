---
name: hyperframes
title: HyperFrames Motion Graphics
description: Motion graphics creation with HyperFrames (HeyGen) — HTML/CSS/JS compositions that render to MP4. Includes ethereal/minimal style guide for Tuấn Anh's TikTok content.
created: 2026-05-18
updated: 2026-05-18
type: skill
tags: [motion-graphics, hyperframes, video-generation]
confidence: high
relationships: [remotion]
---

# HyperFrames Motion Graphics Skill

## What It Is
HyperFrames is an open-source motion graphics framework from HeyGen (Apache 2.0, v0.6.20). You write HTML/CSS/JS compositions, it renders them to MP4 video using a headless browser + ffmpeg.

**NOT** for: AI generative video (use Runway, Kling, etc. for that)
**FOR**: programmatic motion graphics — kinetic typography, product reveals, UI animations, brand animations

## Style Guide: Ethereal/Minimal (Tuấn Anh's TikTok)

Tuấn Anh prefers the style from this reference video: https://youtu.be/xBZzVNi_4Xw

### Core Aesthetic
- **Dark Tech Sphere**: Volumetric glowing orb on pure black, horizon beam, floating spheres
- **Glassmorphism UI**: Frosted glass panels with backdrop-blur, bokeh background orbs
- **Ethereal Light**: Pastel gradients (lavender/white), light bloom, anamorphic streaks, glass panes
- **Clean Reveal**: Minimal logo with spring-easing ring animations

### Color Palette
| Phase | Colors |
|-------|--------|
| Dark Sphere | `#000000` bg, `#4A90E2` orb core, `#ffffff` rim/horizon, `#1a3a6e` ambient |
| Glassmorphism | `#0a0a1a` → `#1a1a3a` bg, `rgba(255,255,255,0.06)` glass, `#FF9A62` accent circle |
| Ethereal | `#b2a7fd` lavender, `#3A62F8` blue sphere, `#C09470` warm ochre sphere |
| Clean Reveal | `#000000` bg, `#00B5AD` teal rings/core, `#ffffff` text |

### Typography
- **Font**: Inter (weight 300-700) + Space Grotesk
- **Titles**: 72-80px, weight 700, letter-spacing 0.1-0.2em, uppercase
- **Subtitles**: 24-28px, weight 300, letter-spacing 0.3-0.4em
- **Text shadows**: glow effect `0 0 60px rgba(color, 0.8)` for dark-phase text

### Animation Principles
- **Easing**: `power2.out` / `power3.out` for reveals, `back.out(1.5)` for springy UI, `sine.inOut` for pulses
- **Motion feel**: Weightless, languid, zero-gravity drift. No abrupt cuts.
- **Stagger**: 0.1-0.3s between elements, `from: "random"` for particles
- **Duration**: Transitions 1.5-2s, element reveals 2-3s, pulse cycles 2-4s

### Depth Effects (CSS)
```css
/* Glassmorphism */
.glass {
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(40px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 24px;
}

/* Volumetric orb */
#orb {
  background: radial-gradient(circle at 40% 35%,
    #ffffff 0%, #a3c9ff 15%, #4a90e2 40%, #1a5cb8 70%, #0a2a5e 100%);
  box-shadow: 0 0 100px rgba(74,144,226,0.8), 0 0 200px rgba(74,144,226,0.5);
}

/* Bokeh orb */
.bokeh {
  filter: blur(60px);
  background: radial-gradient(circle, rgba(99,102,241,0.6) 0%, transparent 70%);
}

/* Lens flare */
.anamorphic-streak {
  filter: blur(15px);
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.8) 50%, transparent 100%);
}
```

## Setup

```bash
# Install
cd ~/.hermes/hermes-agent/optional-skills/creative/hyperframes/scripts
./setup.sh

# Init project
npx hyperframes init my-project --non-interactive --example kinetic-type
cd my-project

# Dev server (long-running, run in background)
npm run dev

# Check (lint + validate + inspect)
npm run check

# Render
npx hyperframes render --quality draft --output /tmp/output.mp4
# or for high quality:
npx hyperframes render --quality high --output /tmp/output.mp4
```

## Project Structure
```
my-project/
├── index.html          # Entry point — root timeline, loads compositions
├── compositions/       # Sub-compositions (imported via data-composition-src)
│   └── main-graphics.html
├── assets/             # Media files
├── meta.json
└── AGENTS.md           # Project conventions
```

## Composition HTML Structure

```html
<!doctype html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>My Composition</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet" />
    <style>/* all styles inline */</style>
  </head>
  <body>
    <!-- ROOT element MUST have data-composition-id, data-width, data-height -->
    <div id="root" data-composition-id="main-graphics" data-width="1920" data-height="1080">
      <!-- elements -->
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["main-graphics"] = tl;

      // Your animations...
      tl.to("#my-element", { opacity: 1, duration: 2, ease: "power2.out" }, 0);
    </script>
  </body>
</html>
```

## CRITICAL Validation Rules

1. **Root element MUST have**: `data-composition-id="<name>"`, `data-width="1920"`, `data-height="1080"`
2. **Timeline ID must match**: `window.__timelines["main-graphics"]` = `data-composition-id="main-graphics"`
3. **Scope ALL GSAP selectors**: Use `#p1-bg .element` not `.element` alone, OR use `ctx = "[data-composition-id='main-graphics']"` and scope: `tl.to(ctx + " .element", ...)`
4. **Unscoped selectors fail**: Classes like `.p1-micro`, `.bokeh-orb` will target ALL compositions when bundled → data loss

## Animation Patterns

### Phase Structure (typical 30s TikTok)
```
0-10s:   Phase 1 — dramatic reveal (dark bg, main element)
10-20s:  Phase 2 — detail/showcase (glassmorphism, UI elements)
20-26s:  Phase 3 — climax (ethereal light, particles, bloom)
26-30s:  Phase 4 — clean outro (logo, CTA)
```

### Stagger Patterns
```js
// Particles — random stagger
tl.to(".particle", { opacity: 0.6, duration: 1.5, stagger: { each: 0.1, from: "random" } }, 1);

// Floating spheres — edges first
tl.to(".float-sphere", { opacity: 0.9, duration: 2, stagger: { each: 0.2, from: "random" } }, 3);

// Glass panes — clockwise
tl.to(".glass-pane", { opacity: 0.6, duration: 2, stagger: { each: 0.3, from: "edges" } }, 21);
```

### Pulse/Loop Animation
```js
// Orb pulse
tl.to("#main-orb", {
  boxShadow: "0 0 120px rgba(74,144,226,0.9),0 0 240px rgba(74,144,226,0.6)",
  duration: 2,
  ease: "sine.inOut",
  yoyo: true,
  repeat: 1
}, 5);
```

### Spring Reveal (back.out)
```js
// Logo rings expand with overshoot
tl.to(".logo-ring-outer", { scale: 1, opacity: 1, duration: 1, ease: "back.out(1.5)" }, 26.5);
tl.to(".logo-ring-mid", { scale: 1, opacity: 1, duration: 1, ease: "back.out(1.2)" }, 26.8);
tl.to(".logo-core", { scale: 1, opacity: 1, duration: 0.8, ease: "back.out(2)" }, 27.3);
```

### Phase Transitions
```js
// Crossfade between phases
tl.to("#phase1-bg", { opacity: 0, duration: 2, ease: "power2.inOut" }, 8);
tl.to("#phase2-bg", { opacity: 1, duration: 1.5, ease: "power2.out" }, 10);
```

## Rendering Tips

- **Draft quality**: Fast test render during development
- **High quality**: Final output — takes ~3x longer
- **File size**: ~4-8MB for 30s draft, ~20-50MB for high quality
- **Tool versions verified**: Node v25.9.0+, npm 11.12.1+, ffmpeg 8.1+

## Additional Lint Warnings (from motion-graphic-video)

These additional warnings are caught by the HyperFrames linter:
| Warning | Fix |
|---------|-----|
| `gsap_css_transform_conflict` | Use `yPercent` instead of `transform: translateY()` in GSAP tweens |
| `overlapping_gsap_tweens` | Add `overwrite:"auto"` to GSAP tween config |
| `motion_path_missing_anchor` | Ensure each animated element has a clear anchor point |

## Composition with Sequence Attributes (motion-graphic-video pattern)

This pattern from `motion-graphic-video` uses `data-enter`/`data-exit` attributes for timing:

```html
<div class="sequence" data-enter="500" data-exit="2500">
  <!-- Content enters at 500ms, exits at 2500ms -->
</div>
```

Use GSAP for animation within the timeline:
```javascript
gsap.from('.element', {
  opacity: 0,
  y: 50,
  duration: 0.5,
  ease: 'power2.out'
});
```

## Pitfalls

- **Missing root attributes**: Linter will catch `root_missing_composition_id` and `root_missing_dimensions`
- **Timeline ID mismatch**: `timeline_id_mismatch` when `window.__timelines["x"]` ≠ `data-composition-id="x"]`
- **Unscoped selectors**: Produces `unscoped_gsap_selector` warnings → elements in wrong composition get animated
- **npm run dev is long-running**: Must run in background, not foreground (times out)
- **Composition file too large**: Split if >200 lines — use multiple sub-compositions

### CSS Transform + GSAP Animation Conflict (CRITICAL — causes "no motion" bug)

**SYMPTOM**: User reports "no movement in the video" — all elements visible but completely static.

**ROOT CAUSE**: When an element has CSS `transform: scale(0)` AND GSAP tweens `scale`, GSAP overwrites the entire CSS transform property. The initial `scale(0)` from CSS is lost when GSAP takes over, BUT the GSAP animation may start from an unexpected value or not fire correctly because the CSS initial state was not properly set via GSAP.

**THE FIX — Two options:**

**Option A (preferred): Remove CSS transforms, use GSAP only**
```css
/* WRONG — CSS transform conflict */
#my-orb { transform: scale(0); }

/* CORRECT — GSAP handles all transform state */
#my-orb { /* no transform here */ }
```

In GSAP:
```js
// Use fromTo to set initial state explicitly
tl.fromTo("#my-orb", 
  { scale: 0, xPercent: -50, yPercent: -50 },  // initial state
  { scale: 1, duration: 2, ease: "back.out(1.2)" }  // animate to
, 0);
```

**Option B: Use inline style instead of CSS**
```html
<div id="my-orb" style="transform: scale(0);"></div>
```

**WHY Option A is preferred**: Inline styles are scoped per element and GSAP can reliably override them. CSS classes create conflicts when GSAP and CSS both try to manage the same property.

**Verification**: After fixing, render and watch — if elements still don't animate, check browser console for "GSAP target not found" warnings. Those indicate selectors aren't matching elements in the headless browser context.

### CustomEase Registration Warning

**SYMPTOM**: `GSAP target not found. https://gsap.com` warnings in browser console.

**CAUSE**: `gsap.registerPlugin(CustomEase)` fails in headless browser context because CustomEase may not load before GSAP tries to use it.

**THE FIX**: Remove `gsap.registerPlugin(CustomEase)` if you're not using custom eases, OR ensure both scripts load before any GSAP calls:
```html
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/CustomEase.min.js"></script>
<!-- THEN register -->
<script>
  gsap.registerPlugin(CustomEase);
  // then define eases and timelines
</script>
```

If you see the warning, the timeline may still work (GSAP falls back to linear), but springy effects like `back.out(1.5)` won't have the custom curve. Test with `ease: "back.out(1.5)"` — if elements still spring, it's working.

### Phase Transitions Breaking (30s video renders as 23s)

**SYMPTOM**: `npx hyperframes render` produces 23s video instead of expected 30s.

**CAUSE**: Timeline may be cutting off early because the last animation finishes before 30s, OR the headless browser captures at wrong rate.

**THE FIX**: Check the actual duration in the render output. If it's shorter than expected, verify all phase transitions are between correct timestamps (e.g., phase 1: 0-8s fade out at 8s, phase 2 starts at 10s = 2s gap). Ensure `staticDuration` in `meta.json` matches your actual timeline length.

## Support Files

- `references/ethereal-style-composition.html` — Working 30s composition with 4 phases matching Tuấn Anh's style reference

## TikTok Content Context (from motion-graphic-video)

Tuấn Anh's preferences when producing TikTok motion graphics:
- **Hands-on testing**: wants to see results first, then discuss
- **Style**: prefers ethereal/minimal over aggressive motion
- **Voice**: Vietnamese casual — "anh" + "mấy con vợ"
- **Script**: see [[tiktok-viral-script]] for TikTok script approach

### Motion Graphic Video Production Context (from motion-graphic-video)

When using HyperFrames to produce TikTok content, Tuấn Anh's preferences:
- **Hands-on testing**: wants to see results first, then discuss
- **Style**: prefers ethereal/minimal over aggressive motion
- **Voice**: Vietnamese casual — "anh" + "mấy con vợ"
- **Script**: see [[tiktok-viral-script]] for TikTok script approach

**Style profiles for TikTok:**
| Profile | Mood | Colors | Effects | Motion |
|---------|------|--------|---------|--------|
| Ethereal Minimal | calm, mysterious, Tech-Zen | dark bg, electric blue/purple gradients, coral/orange accents | glassmorphism, volumetric light, floating particles, bloom | ease-in-out, floating, weightless |
| Dark Tech Minimal | modern, clean, high-tech | near-black bg (#0a0a0f), electric blue (#00d4ff), white | subtle glow, gradient text, clean borders | moderate slide-ins, fade transitions |
| Glassmorphism Aesthetic | — | dark + subtle gradient | `backdrop-filter: blur(20px)`, semi-transparent fill, subtle border | — |

**Common lint warnings:**
| Warning | Fix |
|---------|-----|
| `gsap_css_transform_conflict` | Use `yPercent` instead of `transform: translateY()` in GSAP tweens |
| `overlapping_gsap_tweens` | Add `overwrite:"auto"` to GSAP tween config |
| `motion_path_missing_anchor` | Ensure each animated element has a clear anchor point |

**Dimensions:** 9:16 portrait (1080×1920) for TikTok. Keep under 30s.

## Related
- [[remotion]] — React-based video generation (alternative)
- [[tiktok-viral-script]] — TikTok script writing