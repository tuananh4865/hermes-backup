---
name: hyperframes
title: HyperFrames Motion Graphics + TikTok Subtitle Sync
description: Motion graphics + TikTok subtitle-sync-the-voice workflow using HyperFrames (HeyGen). HTML/CSS/JS compositions rendered to MP4 via headless Chrome + ffmpeg. Includes TikTok subtitle overlay pattern (word-level Whisper → phrases JSON → sub-composition → MP4 with word highlight).
created: 2026-05-18
updated: 2026-07-16
type: skill
tags: [motion-graphics, hyperframes, video-generation, tiktok-subtitle, word-highlight]
confidence: high
relationships: [remotion, manim-video]
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

## 🎬 HyperFrames Workflows — Subtitle vs Motion Text (CRITICAL distinction 2026-07-16)

**When user says "hiệu ứng chữ theo giọng / chữ chuyển động theo lời thoại / kinetic text / type-on"**, they want **MOTION TEXT** (real animation), NOT static subtitle boxes. The two workflows serve different intents:

| Intent | Visual | Use case | Animation |
|---|---|---|---|
| **Subtitle** (text visible during speech) | Box đen + text trắng tĩnh, word highlight VÀNG | Accessibility, B-roll where focus is content not text | opacity fade in/out, color highlight only |
| **Motion Text** (text IS the effect) | Text FLY in, bounce, scale, glow | Hook reveal, "see what I'm saying" emphasis | typewriter + slide + bounce + scale + glow |

**VERIFICATION QUESTION before starting:** If user says "subtitle / phụ đề" → use Subtitle workflow. If user says "hiệu ứng chữ / motion text / kinetic / chuyển động" → use Motion Text workflow. WRONG WORKFLOW = 4+ min wasted render + redo. (Real case 2026-07-16: user asked for "hiệu ứng chữ chuyển động" but initial implementation was Subtitle-only → user correction delayed final delivery by 30 min.)

## 🎬 TikTok Subtitle Workflow (verified 2026-07-16)

**Use case:** Render a pre-edited TikTok clip with word-level subtitle overlay that syncs with the voice — like CapCut's auto-caption but with custom TikTok styling + word highlight (yellow word being spoken).

### 5-Step Pipeline

```bash
# 1. Whisper the source clip with word-level timestamps (silent + segment JSON + WTS)
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-format json --word-timestamps True \
  --condition-on-previous-text False --output-dir ./whisper_out source.mp4
```

```python
# 2. Build phrases.json from word timestamps
# Group 3-5 words per phrase (sweet spot for TikTok readability)
phrases = []
i = 0
while i < len(words):
    chunk = words[i:i+4]  # 4 words/phrase
    if not chunk: break
    phrases.append({
        "start": chunk[0]["start"],
        "end": chunk[-1]["end"],
        "text": " ".join(w["word"] for w in chunk)
    })
    i += 3  # 1-word overlap for flow

# ⚠️ CRITICAL LIMIT: Keep phrases ≤ 30 (HyperFrames DOM element crash)
# If you have 80+ phrases in source, merge first: this[:60] + merged[:30]
```

```bash
# 3. Init project + sub-composition
npx hyperframes init my-subtitle --non-interactive --example blank
```

```html
<!-- 4. index.html: host root = video, sub-composition = overlay -->
<div id="root" data-composition-id="main" data-start="0"
     data-duration="110" data-width="1080" data-height="1920">
  <video id="a-roll-video" src="assets/clip.mp4"
         data-start="0" data-duration="109.98" data-track-index="0"
         data-has-audio="true" playsinline
         style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0"></video>
  <div data-composition-id="tiktok-subtitle"
       data-composition-src="compositions/tiktok-subtitle.html"
       data-start="0" data-duration="110" data-track-index="1"
       data-width="1080" data-height="1920"
       style="position:absolute;inset:0;z-index:1;pointer-events:none"></div>
</div>
<script>
  window.__timelines = window.__timelines || {};
  window.__timelines["main"] = gsap.timeline({ paused: true });
</script>
```

```html
<!-- 5. compositions/tiktok-subtitle.html -->
<template id="tiktok-subtitle-template">
  <div data-composition-id="tiktok-subtitle"
       data-width="1080" data-height="1920" data-duration="110">
    <div id="phrases-layer"></div>
    <div id="brand-watermark">@tuancuaban</div>
    <style>
      [data-composition-id="tiktok-subtitle"] {
        background: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
        color: white; overflow: hidden;
      }
      #phrases-layer { position: absolute; inset: 0; z-index: 10; pointer-events: none; }
      .phrase {
        position: absolute; left: 50%; bottom: 280px;
        transform: translateX(-50%) translateY(20px) scale(0.95);
        max-width: 920px; text-align: center; opacity: 0; z-index: 50;
      }
      .phrase-text {
        display: inline-block; padding: 16px 32px;
        background: rgba(0, 0, 0, 0.78);
        backdrop-filter: blur(16px);
        border-radius: 20px; font-size: 48px; font-weight: 800;
        line-height: 1.4; color: #FFFFFF;
        text-shadow: 0 2px 12px rgba(0, 0, 0, 0.8);
      }
      .word { display: inline-block; color: rgba(255,255,255,0.5); margin: 0 2px; }
      .word.active { color: #FFD700 !important; transform: scale(1.15);
                     text-shadow: 0 0 24px rgba(255,215,0,0.9); }
      .word.spoken { color: rgba(255,255,255,0.95); }
      #brand-watermark {
        position: absolute; bottom: 80px; left: 50%;
        transform: translateX(-50%); font-size: 28px; font-weight: 700;
        color: rgba(255,255,255,0.9); z-index: 60; opacity: 0;
      }
    </style>
    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["tiktok-subtitle"] = tl;

      const phrasesData = [ /* injected phrases: [{start, end, text}] */ ];

      // Build phrase DOM
      const layer = document.querySelector('[data-composition-id="tiktok-subtitle"] #phrases-layer');
      let wordIndex = 0;
      phrasesData.forEach((phrase, pIdx) => {
        const phraseDiv = document.createElement('div');
        phraseDiv.className = 'phrase';
        const textDiv = document.createElement('div');
        textDiv.className = 'phrase-text';
        const textStr = (phrase && phrase.text) ? String(phrase.text) : '';
        const words = textStr.split(/\s+/).filter(w => w.length > 0);
        words.forEach((w) => {
          const wordSpan = document.createElement('span');
          wordSpan.className = 'word';
          wordSpan.textContent = w;
          textDiv.appendChild(wordSpan);
        });
        phraseDiv.appendChild(textDiv);
        layer.appendChild(phraseDiv);
      });

      // Animate: fade in/out + word-by-word highlight
      const phraseEls = layer.querySelectorAll('.phrase');
      phrasesData.forEach((phrase, pIdx) => {
        const phraseEl = phraseEls[pIdx];
        const words = phraseEl.querySelectorAll('.word');
        tl.to(phraseEl, { opacity: 1, y: 0, scale: 1, duration: 0.2, ease: "power2.out" }, phrase.start);
        tl.to(phraseEl, { opacity: 0, duration: 0.15, ease: "power2.in" }, phrase.end);
        const phraseDur = phrase.end - phrase.start;
        if (phraseDur > 0 && words.length > 0) {
          const wordDur = phraseDur / words.length;
          words.forEach((wordEl, wIdx) => {
            const wordStart = phrase.start + (wIdx * wordDur);
            tl.call(() => {
              words.forEach(w => w.classList.remove('active'));
              wordEl.classList.add('active');
              wordEl.classList.add('spoken');
            }, [], wordStart);
          });
        }
      });

      tl.fromTo('#brand-watermark', { opacity: 0 }, { opacity: 1, duration: 0.5 }, 0);
    </script>
  </div>
</template>
```

```bash
# 6. Render
npx hyperframes render --quality draft --output final_with_subs.mp4
```

### Performance Reference (verified 2026-07-16, macOS M-series)

| Input | Phrases | Render time | Output size |
|-------|---------|-------------|-------------|
| 110s clip @ 1080×1920 | 27 phrases (merged from 80) | ~3.5 min | 71 MB |
| 110s clip @ 1080×1920 | 80 phrases | **FAILS** silently | - |

**🪦 Known hard limit:** HyperFrames silently crashes (only first phrase loads) if you inject >40 phrases into the sub-composition DOM. Always merge before render.

### Why Use This Over ffmpeg drawtext?

- ❌ **ffmpeg drawtext** — hard to coordinate word-by-word highlight timing, requires manual libfreetype install (`brew install ffmpeg-full`)
- ✅ **HyperFrames** — built-in GSAP timeline control, CSS animations for free (blur, scale, color), system font fallback, browser-accurate text rendering, **way easier to iterate visually**

## 🎬 TikTok Motion Text Workflow (NEW 2026-07-16 — KEY DIFFERENTIATOR)

**Use case:** When the TEXT ITSELF is the visual effect — words pop in bouncy as they're spoken, slide up with motion, glow when active. This is what users mean when they say "hiệu ứng chữ chuyển động theo lời thoại" or "motion text sync voice".

**Differences from Subtitle workflow:**
- Each word has ANIMATION: scale 0.5 → 1.15 (bouncy back.out(2)), translateY 40px → 0 (slide up), opacity 0 → 1 (fade in)
- Active word glows in yến (FFD700) with text-shadow 24px halo + scale 1.15
- Spoken words dim to trắng 70% (not remove)
- Box container is dim backdrop, mostly see through

### 5-Step Pipeline (similar to Subtitle)

**Same Step 1-3** as Subtitle workflow (Whisper → build phrases → init project).

**MUST do merge step (verified):** 27 phrases renders all, 80 phrases only renders 1. Apply `merge_phrases()` from `scripts/extract_tiktok_phrases.py`.

### Motion Text Composition HTML

```html
<template id="tiktok-motion-text-template">
  <div data-composition-id="tiktok-motion-text"
       data-width="1080" data-height="1920" data-duration="110">
    <div id="phrases-layer"></div>
    <div id="brand-watermark">@tuancuaban</div>

    <style>
      [data-composition-id="tiktok-motion-text"] {
        background: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
        color: white; overflow: hidden;
      }
      #phrases-layer { position: absolute; inset: 0; z-index: 10; pointer-events: none; }

      .phrase {
        position: absolute; left: 50%; bottom: 380px;
        transform: translateX(-50%);
        max-width: 940px; text-align: center; z-index: 50; opacity: 0;
      }
      .phrase-text {
        display: inline-block; padding: 24px 40px;
        background: rgba(0, 0, 0, 0.82);
        backdrop-filter: blur(20px);
        border-radius: 28px;
        font-size: 56px; font-weight: 900; line-height: 1.3;
        color: #FFFFFF; letter-spacing: 0.005em;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
      }
      .word {
        display: inline-block;
        opacity: 0;
        transform: translateY(40px) scale(0.5);
        margin: 0 4px;
        color: rgba(255, 255, 255, 0.9);
      }
      /* Active word: glow + scale (BUMPY motion) */
      .word.active {
        color: #FFD700 !important;
        transform: translateY(0) scale(1.15) !important;
        text-shadow:
          0 0 24px rgba(255, 215, 0, 0.9),
          0 0 48px rgba(255, 215, 0, 0.5),
          0 4px 16px rgba(0, 0, 0, 0.9) !important;
      }
      /* Spoken word: dimmed but stays visible */
      .word.spoken {
        color: rgba(255, 255, 255, 0.7);
        transform: translateY(0) scale(1);
      }
      #brand-watermark {
        position: absolute; bottom: 100px; left: 50%;
        transform: translateX(-50%);
        font-size: 30px; font-weight: 700;
        color: rgba(255, 255, 255, 0.92); z-index: 60;
        text-shadow: 0 2px 12px rgba(0, 0, 0, 0.8);
        letter-spacing: 0.06em; opacity: 0;
      }
    </style>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["tiktok-motion-text"] = tl;

      const phrasesData = [ /* __PHRASES_DATA__ */ ];

      // Build phrase DOM (same as Subtitle)
      const layer = document.querySelector('[data-composition-id="tiktok-motion-text"] #phrases-layer');
      phrasesData.forEach((phrase, pIdx) => {
        const phraseDiv = document.createElement('div');
        phraseDiv.className = 'phrase';
        const textDiv = document.createElement('div');
        textDiv.className = 'phrase-text';
        const words = String(phrase.text).split(/\s+/).filter(w => w.length > 0);
        words.forEach((w) => {
          const wordSpan = document.createElement('span');
          wordSpan.className = 'word';
          wordSpan.textContent = w;
          textDiv.appendChild(wordSpan);
        });
        phraseDiv.appendChild(textDiv);
        layer.appendChild(phraseDiv);
      });

      // MOTION TIMELINE — the key difference from Subtitle
      const phraseEls = layer.querySelectorAll('.phrase');
      phrasesData.forEach((phrase, pIdx) => {
        const phraseEl = phraseEls[pIdx];
        const words = phraseEl.querySelectorAll('.word');
        const phraseDur = phrase.end - phrase.start;
        const numWords = words.length;
        if (numWords === 0) return;
        const wordDur = phraseDur / numWords;

        // Set initial states (so they're hidden before timeline starts)
        gsap.set(phraseEl, { opacity: 0 });
        gsap.set(words, { opacity: 0, y: 40, scale: 0.5 });

        // 1. Container fade in
        tl.to(phraseEl, { opacity: 1, duration: 0.15, ease: "power2.out" }, phrase.start);

        // 2. Word-by-word POP-IN with bouncy easing
        words.forEach((wordEl, wIdx) => {
          const wordStart = phrase.start + (wIdx * wordDur);
          tl.to(wordEl, {
            opacity: 1, y: 0, scale: 1,
            duration: 0.15,
            ease: "back.out(2)"  // ⭐ KEY: bouncy overshoot for the wiggle effect
          }, wordStart);

          // 3. Mark active + spoken for highlight effect
          tl.call(() => {
            words.forEach(w => w.classList.add('spoken'));
            wordEl.classList.add('active');
          }, [], wordStart + 0.001);
        });

        // 4. Container fade out at end
        tl.to(phraseEl, { opacity: 0, y: -20, duration: 0.2, ease: "power2.in" }, phrase.end);
      });

      // Watermark fade in
      tl.fromTo('#brand-watermark',
        { opacity: 0, scale: 0.8 },
        { opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.5)" },
        0
      );
    </script>
  </div>
</template>
```

### Render + Verify Motion Text

```bash
npx hyperframes render --quality draft --output final_motion_text.mp4
```

### Key Motion Text Animation Anatomy (the wiggle that makes it "motion" not "subtitle")

| Element | Initial state | Animation in | Active state | Spoken state |
|---|---|---|---|---|
| `.word` | opacity 0, translateY(40px), scale(0.5) | fade in 0.15s + slide up + scale to 1.0 (bouncy `back.out(2)`) | opacity 1, scale 1.15, color #FFD700, glow text-shadow | opacity 0.7, scale 1, color trắng mờ |
| `.phrase` container | opacity 0 | fade in 0.15s (power2.out) | visible | fade out 0.2s + slide up -20px (power2.in) |

**The 3 visual signals that make it "motion" (not subtitle):**
1. **Bounce ease** (`back.out(2)`) — words overshoot scale 1.0 → settle, creating a "wiggle" feel
2. **Slide up entrance** — translateY 40px → 0, words appear from below
3. **Persistent visible words** — spoken words don't disappear, just dim + scale down (subtitle disappears entirely)

### Motion Text vs Subtitle — When to Pick

| User intent | Workflow |
|---|---|
| "thêm phụ đề / subtitle Tiếng Việt để xem trên điện thoại" | **Subtitle** |
| "làm hiệu ứng chữ chuyển động / motion text cho video hoàn hảo hơn" | **Motion Text** |
| "subtitle cho accessibility" | **Subtitle** |
| "text animation để video pro hơn / text phải bay lên" | **Motion Text** |

(Hybrid: Use Motion Text for HOOK (~10s) → switch to Subtitle for body. Render 2 cuts and concat with ffmpeg.)

### Performance Reference (verified 2026-07-16, macOS M-series)

| Input | Phrases | Render time | Output size |
|-------|---------|-------------|-------------|
| 110s clip @ 1080×1920 | 27 motion text phrases | ~3.5 min | 71 MB |
| 110s clip @ 1080×1920 | 80 motion text phrases | **FAILS** silently | - |

**🪦 Known hard limit (same for both workflows):** HyperFrames silently crashes if you inject >40 phrases into the sub-composition DOM. Always merge before render.

### Motion Text Pitfalls (NEW 2026-07-16)

**MT-1: `back.out(2)` overshoot CAN exceed viewport on long words**
- `scale: 1.15` on word đang active means the word briefly renders at 1.15× its CSS size. With very long single words (>15 chars), it can overflow horizontally.
- Fix: cap `scale: 1.10` for words >12 chars. Or wrap word in `<span style="display:inline-block; max-width: 200px; word-break: break-word;">`.

**MT-2: Active word glow requires `text-shadow` not `box-shadow`**
- `box-shadow` adds glow to the word's RECTANGULAR box (background-color).
- For glow on the LETTERS themselves (TikTok-style neon), use `text-shadow: 0 0 24px rgba(255, 215, 0, 0.9), 0 0 48px rgba(255, 215, 0, 0.5)`.
- Real case 2026-07-16: `box-shadow: 0 0 30px gold` did NOT glow the letters — only added rectangle shadow behind.

**MT-3: `gsap.set(...)` initial states (NOT `tl.fromTo`)**
- If you use `tl.fromTo` for the first animation, GSAP needs to know what "from" is — but you've already set initial state via CSS. Redundant.
- Use `gsap.set` to lock initial state, then `tl.to` (not `tl.fromTo`) for the animation in.
- Real case 2026-07-16: `tl.fromTo(words, { opacity: 0 }, { opacity: 1 }, 1.5)` looked like a 0-frame jump because `fromTo` resets to "from" state at start time.

**MT-4: Phrase container fades in BEFORE its words pop in**
- Order matters: tl.to(phraseEl, opacity 1) at phrase.start → tl.to(wordEl, ...) at wordStart.
- If you swap order, words pop in BEFORE the container is visible → invisible pops (no visual feedback).
- Real case 2026-07-16: swapping the 2 `.to()` calls made the animation look like static text appearing out of nowhere.

**MT-5: Watermark has its own pop-in animation, not just opacity**
- `tl.fromTo('#brand-watermark', { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, ease: "back.out(1.5)" }, 0)`
- The `scale: 0.8 → 1` with bouncy ease makes the watermark subtly bounce in too — consistent with word pop-in feel.

**MT-6: Inline-block word + space character → CSS collapse (CRITICAL — words appear glued together)**
- **SYMPTOM:** User reports "Chữ đang bị dính liền với nhau mà không có khoảng cách giữa 2 từ kìa" → text shows as "cáicôngđoạn" instead of "cái công đoạn", `@tuancuaban` instead of `@ tuancuaban`.
- **ROOT CAUSE:** When `.word` is `display: inline-block`, browsers COLLAPSE the space character between elements (CSS whitespace processing rule). Setting `margin`, `padding`, or even `word-spacing: 12px` does NOT fix it — the space character is gone.
- **THE FIX:** Use explicit `.word-space` span with `&nbsp;&nbsp;` (non-breaking spaces) between words:
  ```html
  <span class="word">cái</span>
  <span class="word-space">&nbsp;&nbsp;</span>  <!-- MUST be a separate element -->
  <span class="word">công</span>
  ```
  ```css
  .word-space {
    display: inline-block;
    white-space: pre;
    width: 0.6em;  /* visual space width */
    opacity: 1 !important;  /* never animate this */
    transform: none !important;
    vertical-align: baseline;
  }
  ```
- **Alternative (also works):** Just use regular spaces but force `display: flex` on `.phrase-text` with `gap: 0.4em`:
  ```css
  .phrase-text { display: flex; flex-wrap: wrap; justify-content: center; gap: 0.4em 0.3em; }
  ```
- **Watermark fix:** Apply the same pattern — `<div id="brand-watermark">@ tuancuaban</div>` (with manual space) NOT `<div id="brand-watermark">@tuancuaban</div>` because the framework's font aliasing drops `n`/Vietnamese complex glyphs when they touch punctuation.
- **Verification:** Render + view any frame with text in it. If words appear glued (`cáicôngđoạn`), the fix didn't apply. Common regression: spaces in `textContent` of `<span>` are collapsed before reaching the DOM.

**MT-7: Phase container `opacity: 0` hides ALL child text in multi-phase compositions**
- **SYMPTOM:** Multi-phase composition renders HOOK phase correctly (large fullscreen dark) but every other phase (4-18s, 18-34s, etc.) shows ZERO text — only the watermark + blank video.
- **ROOT CAUSE:** Each phase has a wrapper `<div class="phase phase-{id}">` containing all its texts. If you set `gsap.set(phaseEl, { opacity: 0 })` and forget to `.to({ opacity: 1 })` at phase start, OR if you use `tl.to(phaseEl, { opacity: 0 })` as the BASE state instead of an animation target, the phase stays invisible forever and all child text inherits `opacity: 0`.
- **THE FIX (verified pattern — see DMT-1 workflow below):**
  1. Set `.phase { opacity: 1; }` in CSS (always visible, never animated)
  2. Animate TEXT elements only, not the phase container
  3. Use `gsap.set(textEl, { opacity: 0 })` on each text, then `tl.to(textEl, { opacity: 1, ... }, startTime)` to fade in
  - The "phase background fade" only applies when the phase has a non-transparent `bg` color (like `.phase-closing { background: rgba(0,0,0,0.92); }`) — in that case, fade the PHASE container, not the text.
- **Real case 2026-07-16:** 8-phase diverse motion composition rendered 1/8 phase correctly until I changed `.phase { opacity: 0 }` → `.phase { opacity: 1 }`. After fix: 8/8 phases render text correctly.

## 🎬 Diverse Motion Workflow (NEW 2026-07-16 — multi-phase, multi-style)

**Use case:** When one style (subtitle OR motion text) is too monotonous for a 110s video. Split timeline into 6-8 semantic phases (HOOK/PROBLEM/USP/SOLUTION/INTRO/HOW/CTA/CLOSING), each with distinct font, color, position, animation, and background. Keeps viewer engaged across long-form content.

**Why:** User feedback 2026-07-16 (verbatim): *"Hiện tại chỉ đang làm khá cơ bản 1 kiểu chạy chữ cho toàn bộ video mà không thay đổi đa dạng, thử làm đa dạng hơn kiểu chứ chạy đằng sau nhân vật chính, có thể có những đoạn chữ chạy full màn hình trên một background nên tối mà không cần show mặt chủ thể, chữ có thể thay đổi nhiều font khác nhau và màu sắc khác nhau, hook 3s đầu thì chữ to rõ để nhấn mạnh"*

### 5 Steps

1. **Whisper source clip** → word-level JSON (same as Subtitle/Motion Text)
2. **Segment phrases into phases** by semantic + time:
   ```python
   # 6-8 phases typical for 110s TikTok
   phases = [
       {"id": "HOOK",          "time": "0-4s",   "style": "huge_fullscreen_dark"},
       {"id": "PROBLEM",       "time": "4-18s",  "style": "overlay_around_person"},
       {"id": "USP_BULLET",    "time": "18-34s", "style": "bullet_list_left"},
       {"id": "SOLUTION",      "time": "34-54s", "style": "split_screen_intro"},
       {"id": "INTRO_PRODUCT", "time": "54-75s", "style": "overlay_bottom_caption"},
       {"id": "HOW_TO_USE",    "time": "75-85s", "style": "step_by_step_bottom"},
       {"id": "CTA",           "time": "85-95s", "style": "corner_call_to_action"},
       {"id": "CLOSING",       "time": "95-110s","style": "fullscreen_dark_final"},
   ]
   ```
3. **Map phases → diverse style attributes** (font, color, size, position, animation):
   - HOOK: Inter Black 92px, Yellow `#FFD700`, fullscreen dark bg, typewriter bounce
   - PROBLEM: Inter Bold 64px, White + red glow, no bg (overlay around person), slide-in from random edges
   - USP_BULLET: Menlo Mono 52px, Cyan `#00E5FF`, gradient bg, checklist `✓/✗` pop-in
   - SOLUTION: Inter Bold 58px, Red→Yellow swap, split-screen boxes
   - INTRO_PRODUCT: Georgia Italic, Yellow glow, overlay bottom, fade-zoom elastic
   - HOW_TO_USE: Menlo Mono 56px, Green `#00FF88` step counter, box with step number `2`
   - CTA: Inter Black 60px, Pink `#FF1493` pulsing border, corner right
   - CLOSING: Inter Black 84px, Yellow glow, fullscreen dark, zoom-in impact
4. **Use `templates/tiktok-diverse-motion.html` as base** — see below. Replace `__PHASES_DATA__` with your phase definitions array.
5. **Render** with same `npx hyperframes render` command.

### Diverse Motion Composition HTML (skeleton)

```html
<template id="tiktok-diverse-motion-template">
  <div data-composition-id="tiktok-diverse-motion"
       data-width="1080" data-height="1920" data-duration="110">
    <div id="phrases-layer"></div>
    <div id="watermark">@ tuancuaban</div>

    <style>
      [data-composition-id="tiktok-diverse-motion"] {
        background: transparent;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif;
        color: white; overflow: hidden;
      }
      #phrases-layer { position: absolute; inset: 0; z-index: 10; pointer-events: none; }

      /* CRITICAL: phase container stays visible, animate TEXT inside */
      .phase { position: absolute; inset: 0; opacity: 1; z-index: 5; pointer-events: none; }

      /* PHASE 1: HOOK — huge fullscreen dark */
      .phase-hook { background: rgba(0, 0, 0, 0.95); display: flex; align-items: center; justify-content: center; }
      .phase-hook .text {
        font-weight: 900; font-size: 92px; color: #FFD700; text-align: center;
        line-height: 1.2; text-shadow: 0 0 40px rgba(255, 215, 0, 0.7);
        max-width: 900px; padding: 0 40px;
      }

      /* PHASE 2: PROBLEM — overlay around person */
      .phase-problem .text {
        font-weight: 800; font-size: 64px; color: #FFFFFF;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.95), 0 0 30px rgba(255, 0, 0, 0.4);
        max-width: 700px; line-height: 1.15; padding: 0 20px;
      }
      .phase-problem .text.tl { position: absolute; top: 200px; left: 60px; }
      .phase-problem .text.tr { position: absolute; top: 200px; right: 60px; text-align: right; }
      .phase-problem .text.ml { position: absolute; top: 50%; left: 60px; transform: translateY(-50%); }
      .phase-problem .text.mr { position: absolute; top: 50%; right: 60px; text-align: right; transform: translateY(-50%); }

      /* PHASE 3: USP_BULLET — checklist left */
      .phase-usp_bullet { background: linear-gradient(135deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.5) 60%, transparent 100%); }
      .phase-usp_bullet .text {
        font-family: Menlo, monospace; font-weight: 800; font-size: 52px; color: #00E5FF;
        text-shadow: 0 2px 12px rgba(0, 229, 255, 0.7), 0 4px 16px rgba(0, 0, 0, 0.9);
        position: absolute; left: 80px; line-height: 1.3; max-width: 750px;
        padding: 16px 24px; background: rgba(0, 0, 0, 0.5);
        border-left: 6px solid #00E5FF; border-radius: 4px;
      }
      .phase-usp_bullet .text.t1 { top: 250px; }
      .phase-usp_bullet .text.t2 { top: 430px; }
      .phase-usp_bullet .text.t3 { top: 610px; }
      .phase-usp_bullet .text.t4 { top: 790px; }
      .phase-usp_bullet .text.warning { color: #FF4444 !important; border-left-color: #FF4444 !important; }

      /* PHASE 7: CTA — corner call to action */
      .phase-cta .text {
        font-weight: 900; color: #FF1493;
        text-shadow: 0 4px 24px rgba(255, 20, 147, 0.8), 0 0 40px rgba(255, 20, 147, 0.5);
        position: absolute; right: 60px; top: 50%; transform: translateY(-50%);
        text-align: right; padding: 24px 36px; background: rgba(0, 0, 0, 0.85);
        border: 4px solid #FF1493; border-radius: 16px; max-width: 480px;
      }
      .phase-cta .text.pulse { animation: ctaPulse 1.2s ease-in-out infinite; }
      @keyframes ctaPulse {
        0%, 100% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-50%) scale(1.08); box-shadow: 0 8px 40px rgba(255, 20, 147, 0.6); }
      }
      /* ... PHASE 4, 5, 6, 8 styles ... */
    </style>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      window.__timelines["tiktok-diverse-motion"] = tl;

      const phasesData = [/* __PHASES_DATA__ - array of phase objects with phrases array */];

      // Build phase DOMs (each phrase gets `.text` div with optional position class)
      const layer = document.querySelector('[data-composition-id="tiktok-diverse-motion"] #phrases-layer');
      phasesData.forEach((phase) => {
        const phaseDiv = document.createElement('div');
        phaseDiv.className = `phase phase-${phase.id.toLowerCase()}`;
        phaseDiv.dataset.id = phase.id;
        phase.phrases.forEach((phrase) => {
          const textDiv = document.createElement('div');
          textDiv.className = `text ${phrase.position || ''}`;
          textDiv.dataset.phaseId = phase.id;
          textDiv.dataset.start = phrase.start;
          textDiv.dataset.end = phrase.end;
          textDiv.textContent = phrase.text;
          if (phrase.size) textDiv.style.fontSize = phrase.size + 'px';
          phaseDiv.appendChild(textDiv);
        });
        layer.appendChild(phaseDiv);
      });

      // Per-phase animation dispatcher (SWITCH ON phase.id)
      phasesData.forEach((phase) => {
        const phaseEl = layer.querySelector(`[data-id="${phase.id}"]`);
        phase.phrases.forEach((phrase) => {
          const textEl = phaseEl.querySelector(`[data-start="${phrase.start}"]`);
          if (!textEl) return;
          const start = phrase.start;
          const end = phrase.end;

          switch (phase.id) {
            case 'HOOK':
              gsap.set(textEl, { opacity: 0, scale: 0.7 });
              tl.to(textEl, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2.5)" }, start);
              tl.to(textEl, { opacity: 0, duration: 0.2 }, end);
              break;
            case 'PROBLEM':
              gsap.set(textEl, { opacity: 0, x: phrase.position?.includes('right') ? 100 : -100 });
              tl.to(textEl, { opacity: 1, x: 0, duration: 0.35, ease: "power3.out" }, start);
              tl.to(textEl, { opacity: 0, x: phrase.position?.includes('right') ? 100 : -100, duration: 0.25 }, end);
              break;
            case 'USP_BULLET':
              gsap.set(textEl, { opacity: 0, x: -50, scale: 0.8 });
              tl.to(textEl, { opacity: 1, x: 0, scale: 1, duration: 0.3, ease: "back.out(1.5)" }, start);
              tl.to(textEl, { opacity: 0.4, duration: 0.2 }, end);
              break;
            // ... case SOLUTION, INTRO_PRODUCT, HOW_TO_USE, CTA, CLOSING ...
          }
        });
      });
    </script>
  </div>
</template>
```

### Phase Style Recipe Bank (verified 2026-07-16)

| Phase ID | Font | Size | Color | Position | Animation | Background |
|----------|------|------|-------|----------|-----------|------------|
| HOOK | Inter Black | 92px | `#FFD700` Yellow | center | typewriter + scale bounce `back.out(2.5)` | `rgba(0,0,0,0.95)` fullscreen |
| PROBLEM | Inter Bold | 64px | `#FFFFFF` White + red glow text-shadow | tl/tr/ml/mr (4 corners) | slide-in `power3.out` | transparent |
| USP_BULLET | Menlo Mono | 52px | `#00E5FF` Cyan | left side, border-left 6px solid color | checklist pop-in `back.out(1.5)` | gradient dark→transparent |
| SOLUTION | Inter Bold | 58px | Red `#FF4444` → Yellow `#FFD700` | left→right swap | slide from left, swap right | transparent with split boxes |
| INTRO_PRODUCT | Georgia Italic | 50-90px | `#FFD700` Yellow glow | bottom center (overlay on product) | fade-zoom elastic | transparent |
| HOW_TO_USE | Menlo Mono | 56px | `#FFFFFF` White + Green step badge | bottom center | slide-up from below | rgba(0,0,0,0.82) box + step counter |
| CTA | Inter Black | 60-70px | `#FF1493` Pink pulsing border | corner right (don't cover face) | pulse animation infinite | rgba(0,0,0,0.85) + 4px solid pink border |
| CLOSING | Inter Black | 84px | `#FFD700` Yellow with 60px glow | center | zoom in `back.out(2.5)` | `rgba(0,0,0,0.92)` fullscreen |

### Performance Reference (verified 2026-07-16)

| Input | Phases | Render time | Output size |
|-------|---------|-------------|-------------|
| 110s clip @ 1080×1920 | 8 diverse phases, 27 phrases total | ~3 min | 20-65 MB (depends on bg opacity) |
| 110s clip @ 1080×1920 | 1 phase simple text | ~3.5 min | 71 MB |

Diverse motion is FASTER than single-phase subtitle because you render less per phase (fewer text elements per phase = smaller output).

## Additional Lint Warnings (from motion-graphic-video)

These additional warnings are caught by the HyperFrames linter:
| Warning | Fix |
|---------|-----|
| `gsap_css_transform_conflict` | Use `yPercent` instead of `transform: translateY()` in GSAP tweens |
| `overlapping_gsap_tweens` | Add `overwrite:"auto"` to GSAP tween config |
| `motion_path_missing_anchor` | Ensure each animated element has a clear anchor point |

## ⚠️ CRITICAL: HyperFrames does NOT render frame-by-frame animation

**If your goal is animated text reveals, staggered transitions, or sequential
narrative — use Remotion or Manim instead.** HyperFrames captures a single
state of the composition at render time and does NOT seek the timeline
forward through each frame interval. The resulting MP4 will show the same
frame repeated for the entire duration.

Verified empirically 2026-08-25 (Dầm Mê intro session): all 240 frames of an
8s render produced identical MD5 hashes — single static state.

**HyperFrames is suitable for:**
- ✅ Static compositions (product splash, intro cards, logo reveals that look complete at time=0)
- ✅ Ambient loops (particles, gradients) where the "static frame" is visually complete
- ✅ Single-shot animations that play once and end

**Use these instead for time-based animations:**
- `remotion` skill (React-based, native frame-by-frame)
- `manim-video` skill (Python, math/programmatic)
- Playwright manual frame capture (see `references/gsap-timeline-capture-pitfalls.md`)

## See also

- `references/gsap-timeline-capture-pitfalls.md` — Detailed pitfalls:
  `repeat:-1` infinite duration, external tweens blocking browser, why
  duration() wrapping doesn't fix capture, verified diagnostic commands.

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

### HyperFrames 1. `init` requires `--example`, `--video`, or `--audio` flag (v0.7.60+)

```bash
# WRONG — fails "Non-interactive init requires --example, --video, or --audio"
hyperframes init my-project --non-interactive

# RIGHT
hyperframes init . --example blank       # empty starter
hyperframes init . --example kinetic-type # pre-built kinetic type starter
hyperframes init . --video https://...    # capture-based starter
hyperframes init . --audio track.mp3      # beat-synced starter
```

For non-interactive CI usage, always pass one of `--example`/`--video`/`--audio`. The bare `init` opens an interactive wizard.

### HyperFrames 2. `missing_timeline_registry` lint is NOT fatal but DO register anyway

The lint check flags compositions without `window.__timelines[<id>]` registration as an error. Render still succeeds without it, BUT:

- Without registration: GSAP animations don't run because the framework can't find a paused timeline to seek/forward per frame. Your elements will be in their CSS initial state for the whole video — looks like "frozen content" until you realize the timeline was never wired.

- Always register, even if you think you don't need animations:
```js
window.__timelines = window.__timelines || {};
window.__timelines["main"] = gsap.timeline({ paused: true });
```

The framework's renderer iterates `window.__timelines` to drive frame-by-frame state. No registration = no state changes between frames.

### HyperFrames 3. `font_family_without_font_face` lint can be ignored IF you accept font fallback

The lint flags font families like `'impact'`, `'times new roman'`, `'courier new'` that aren't in the auto-resolved font list. HyperFrames auto-substitutes them:

| You write | HyperFrames renders |
|---|---|
| `'courier new'` | JetBrains Mono |
| `'times new roman'` | EB Garamond |
| `'arial black'` | Montserrat |
| `'impact'` | Generic sans-serif (no good Impact fallback) |

**Acceptable for: rough previews, internal demos, fast iteration.**
**Not acceptable for: brand-final renders where Impact/Times/Garamond differences matter.**

Fix for production: add `@font-face` declarations pointing to bundled woff2 files, OR use `src: local('Exact Font Name')` to use OS-bundled fonts without download.

### HyperFrames 4. Render 1080p is FAST (~25s for 30s clip) — default quality is 1080p

Don't pre-degrade to 720p to "speed things up" — HyperFrames' default is already 1080p@24fps and renders 30s clip in ~25s on M-series Mac. Compare:
- HyperFrames 1080p30: 25s
- Remotion 1080p24: 40s
- Manim 720p30: ~10 minutes
- Manim 1080p30: ~30 minutes

HyperFrames is the fastest 1080p option of the three for short cinematic clips. Use it for the initial draft, then evaluate if Remotion's React component model is needed for scaling.

### HyperFrames 5. `@font-face` declarations must be in `<style>` BEFORE GSAP/CSS that uses them

If you add custom fonts via Google Fonts `<link>`, the font hasn't loaded by the time the headless browser captures frame 0. First 1-2 frames may show fallback fonts. Workaround:

```html
<!-- Load fonts in <head> synchronously -->
<head>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;700&display=block" rel="stylesheet">
</head>
<!-- Then GSAP / styles -->
```

Or accept the 2-frame fallback and let GSAP `fromTo` settle into final state by frame 5.

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

### HARD RULE: Every pixel must move (NEW 2026-07-17 — Trailer session)

**Anh dặn verbatim:**
> *"Nếu làm animation thì mọi hình ảnh trên screen đều phải được animation hết chứ không được có ảnh hoặc chỗ nào tĩnh hết"*

**Rule**: Khi user yêu cầu trailer/animation dạng `motion graphics` (HyperFrames, Remotion, Manim, After Effects, etc.) — KHÔNG ĐƯỢC CÓ bất kỳ ảnh/chỗ nào tĩnh trên screen. Mọi element phải có ít nhất 1 trong 7 loại animation này, mỗi frame:

| # | Animation type | Pattern |
|---|---|---|
| 1 | SVG rebuild | `chart.innerHTML = rebuildChart(frame)` mỗi frame |
| 2 | CSS transform | `element.style.transform = 'scale(${1 + Math.sin(t*0.1)*0.02})'` |
| 3 | CSS opacity | `element.style.opacity = String(0.5 + Math.sin(t)*0.3)` |
| 4 | CSS box-shadow | `element.style.boxShadow = '0 0 ${20 + Math.sin(t)*8}px color'` |
| 5 | CSS backgroundPosition | `scanline.style.backgroundPosition = '0px ${frame*0.5}px'` |
| 6 | text-shadow blur | `text.style.textShadow = '0 0 ${60 + Math.sin(t)*20}px color'` |
| 7 | textContent update | `counter.textContent = \`[FRAME ${frame}]\`` |

**Anti-pattern (FAIL)**:
- `gsap.to(element, { opacity: 1 })` 1 lần rồi để đó → element chỉ chuyển động 1 lần rồi tĩnh
- `setInterval(..., 1000)` 1 lần → 1 motion mỗi giây, 99% thời gian tĩnh
- `innerHTML = "..."` chỉ build 1 lần → SVG tĩnh vĩnh viễn
- Random mỗi 5s → user thấy ảnh đứng yên 4s
- `gsap.fromTo(element, { opacity: 0 }, { opacity: 1 })` chỉ 1 lần

**Pattern (PASS) — Universal rAF loop**:
```js
function tick(now) {
  const frame = Math.floor((now - startTime) / (1000 / fps));
  // Update EVERY element với frame-driven value
  charts.forEach(c => c.innerHTML = rebuildChart(frame));
  elements.forEach(e => e.style.transform = `scale(${1 + Math.sin(frame * 0.1) * 0.02})`);
  monitors.forEach(m => m.style.boxShadow = `0 0 ${20 + Math.sin(frame * 0.2) * 8}px ${color}`);
  particles.forEach(p => { p.style.top = `${p.initialY - frame * p.speed}px`; p.style.opacity = String(fade * 0.7); });
  requestAnimationFrame(tick);
}
```

**Quantitative verification gate**:
```bash
python3 scripts/motion_diff_check.py trailer.mp4 --t1 0.0 --t2 0.3
# Output:
#   "At 0.3s vs 0.0s: 37.9% pixels changed"
#   "At 0.6s vs 0.3s: 45.4% pixels changed"
#   "If > 10%, animation is LIVE"
# >30% = excellent motion, <5% = FAIL (frozen content)
```

**Real case 2026-07-17**: Em ship HyperFrames V3 13.2 MB. Vision AI verify 4/4 PASS. Quantitative gate 37.9% → 45.4% pixel change per 0.3s = excellent motion. 100% pixel đều di chuyển.

**Reference**: xem `references/3d-trailer-hyperframes-progression.md` section "V3 — All-pixel-must-move rule" cho full implementation details.

### Three.js integration caveats (NEW 2026-07-17)

**Pattern**: HyperFrames host root + Three.js canvas overlay riêng. Renders qua 2 rAF loops độc lập, giao tiếp qua `window.__currentFrame`.

```html
<!-- index.html -->
<div id="three-host" class="three-canvas-host"></div>
<script type="module">
  import { initThree, tickThree } from './three-scene.js';
  initThree(document.getElementById('three-host'));
  // trailer.js rAF loop writes window.__currentFrame each frame
  // separate rAF in three-scene.js reads it and calls tickThree(frame)
</script>
```

```js
// three-scene.js init
const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;

// 3-point lighting
const ambient = new THREE.AmbientLight(0x404060, 0.8);
const keyLight = new THREE.DirectionalLight(0xffffff, 1.6);
keyLight.position.set(8, 12, 16);
keyLight.castShadow = true;
const fillLight = new THREE.DirectionalLight(0x88ff88, 0.9);
const rimLight = new THREE.DirectionalLight(0x4444ff, 0.7);
```

**Top mistakes** (verified 2026-07-17 V4 → V5):
1. `ShaderMaterial` with custom GLSL → `useProgram: program not valid` warning. Fix: use `MeshStandardMaterial` (built-in PBR).
2. `MeshBasicMaterial` for everything → flat look. Fix: add 3-point lighting.
3. No `castShadow`/`receiveShadow` → bars look glued to floor. Fix: 4 places must opt in.
4. `ShaderMaterial` errors cause silent render failure but video still outputs (corrupted). Fix: check browser console for `useProgram` warnings in render log.

**Reference**: xem `references/3d-trailer-hyperframes-progression.md` section "V4/V5" cho full patterns.

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

**SYMPTOM:** `npx hyperframes render` produces 23s video instead of expected 30s.

**CAUSE:** Timeline may be cutting off early because the last animation finishes before 30s, OR the headless browser captures at wrong rate.

**THE FIX:** Check the actual duration in the render output. If it's shorter than expected, verify all phase transitions are between correct timestamps (e.g., phase 1: 0-8s fade out at 8s, phase 2 starts at 10s = 2s gap). Ensure `staticDuration` in `meta.json` matches your actual timeline length.

### HF-TikTok-Subtitle 1: DOM element count silent crash (NEW 2026-07-16)

**SYMPTOM:** Sub-composition only renders the FIRST phrase (or first ~30 DOM elements). Video plays but most content is missing — `console.log` in browser shows the full array, so the data loaded, but only one element ends up in the rendered DOM.

**ROOT CAUSE:** HyperFrames has an undocumented limit on total DOM elements rendered per composition. Past ~40-50 elements (1 wrapper div + N word spans per phrase), the framework silently drops the rest.

**WORKING RANGE (verified):**
- 3 phrases → renders all 3 ✅
- 27 phrases (merged from 80, 4-word groups with 3-word stride) → renders all 27 ✅
- 80 phrases (1-word per phrase w/ word-by-word highlight) → renders only 1 ❌

**THE FIX — Merge before render:**
```python
# Real case: 80 raw phrases from Whisper → merge every 3 phrases
def merge_phrases(raw_phrases, group_size=3, stride=3):
    merged = []
    i = 0
    while i < len(raw_phrases):
        chunk = raw_phrases[i:i+group_size]
        if not chunk: break
        merged.append({
            "start": chunk[0]["start"],
            "end": chunk[-1]["end"],
            "text": " ".join(p["text"] for p in chunk)
        })
        i += stride
    return merged

merged = merge_phrases(raw_phrases, group_size=3, stride=3)
# 80 → 27 phrases (smoother readability too)
```

**When to apply the limit:**
- If your real case has 60+ raw phrases → merge first
- If you get "Loaded, phrases: N" but render shows fewer → DOM limit hit
- Inject phrases as JS array of `{start, end, text}` objects in `compositions/<name>.html` (not as separate JSON file — see HF-TikTok-Subtitle 2)

### HF-TikTok-Subtitle 2: Google Fonts blocked by ORB (NEW 2026-07-16)

**SYMPTOM:** Sub-composition runs but `[Browser]` logs show:
```
✗ request_failed: Failed to load css2: net::ERR_BLOCKED_BY_ORB
✗ page_error: Cannot read properties of undefined (reading 'split')
```
Timeline doesn't run, console complains, video renders without your overlay.

**ROOT CAUSE:** HyperFrames' headless Chrome runs in a hardened sandbox that blocks `<link rel="stylesheet" href="https://fonts.googleapis.com/...">` requests (`ERR_BLOCKED_BY_ORB`).

**THE FIX:** Use OS system fonts via the `-apple-system` chain (HyperFrames auto-substitutes these to `Inter` for cross-platform consistency):
```css
font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display",
             "Segoe UI", Roboto, "Helvetica Neue", sans-serif;
```

**Alternative (slower):** Bypass the block by inlining woff2 as `@font-face { src: url('./fonts/inter.woff2'); }` — adds ~100 KB to project, ~30s render overhead.

**Verification:** Run `npx hyperframes check` — should show `system_font_will_alias: Font families will be substituted at render time: 'sf pro display' → Inter. The renderer maps these to bundled fonts for cross-platform consistency.` (this is informational, NOT an error).

### HF-TikTok-Subtitle 3: Sub-composition pattern is the ONLY way to inject dynamic content (NEW 2026-07-16)

**WRONG:** Trying to inject DOM elements into the root composition directly via inline script:
```html
<div id="root" data-composition-id="main">  <!-- only video elements render here -->
  <video ...></video>
  <div id="phrases-layer"></div>  <!-- never appears in output -->
  <script>
    phrasesData.forEach(phrase => {
      const div = document.createElement('div');  // ❌ never executes
      // ... never appears
    });
  </script>
</div>
```

**RIGHT:** Use a sub-composition via `data-composition-src`:
```html
<!-- index.html (host root) -->
<div id="root" data-composition-id="main" data-width="1080" data-height="1920">
  <video ...></video>  <!-- ONLY video/audio live here -->
  <div data-composition-id="tiktok-subtitle"
       data-composition-src="compositions/tiktok-subtitle.html"
       data-track-index="1" ...></div>  <!-- ✅ renders in iframe context -->
</div>
```
```html
<!-- compositions/tiktok-subtitle.html (sub-composition) -->
<template id="tiktok-subtitle-template">
  <div data-composition-id="tiktok-subtitle" data-width="1080" data-height="1920">
    <!-- ALL DOM content + scripts live here -->
 flamboyant/scripted
    <script>...build phrases DOM...</script>
  </div>
</template>
```

**Why:** HyperFrames renders the host root in ONE browser context, but sub-compositions get THEIR OWN context (iframe-equivalent) where script execution + DOM creation works. The host root only gets video element decoding.

**Symptom of the wrong pattern:** Video plays, brand watermark renders if it's in host root, but all `<div>`s you created via JS in root are gone.

### HF-TikTok-Subtitle 4: Tab-indented phrase strings break JS template literals (NEW 2026-07-16)

**SYMPTOM:** HyperFrames console logs `Loaded, phrases: 1` instead of N (when you have many phrases). Only the first phrase renders.

**ROOT CAUSE:** Using template literals (backticks) for phrases text in inline JS, but the text contains characters that the template literal parser can't handle, OR the array of object literals gets truncated by bracket counting bugs in template.

**THE FIX — Use single quotes + safe escape:**
```js
// ✅ Safe pattern (verified 80 phrases inject correctly)
const phrasesData = [
{start: 0.0, end: 1.64, text: 'làm content được một thời'},
{start: 1.64, end: 2.54, text: 'gian ngắn rồi không phải'},
// ...78 more
];

// ❌ Avoid (template literal can break):
const phrasesData = [
{start: 0.0, end: 1.64, text: `làm content được một thời`},
];
```

When generating this from Python:
```python
phases_list = []
for p in phrases:
    text_safe = p["text"].replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
    phases_list.append(f"{{start: {p['start']}, end: {p['end']}, text: '{text_safe}'}}")
phases_str = "[\n" + ",\n".join(phases_list) + "\n      ]"
```

Then `__PHRASES_DATA__` placeholder in HTML gets replaced with this string.

### HF-TikTok-Subtitle 5: Video must be in project assets/ (not file:// or remote URL) (NEW 2026-07-16)

**SYMPTOM:** Render fails with `Video "a-roll-video" captured 0 of expected 3300 frames (coverage 0.0%, threshold 95.0%). aborting render to prevent shipping a wrong MP4.`

**THE FIX:**
```bash
# 1. Copy source clip into project
cp /Volumes/Storage-1/.../final.mp4 ./my-project/assets/clip.mp4

# 2. Use relative path in HTML
<video src="assets/clip.mp4" ...>  ✅

# WRONG — does NOT work:
<video src="file:///Volumes/Storage-1/.../final.mp4">  ❌
<video src="https://...s3.../video.mp4">  ⚠️ only if HTTPS-hosted
```

HyperFrames' headless Chrome can't access `file://` URLs outside the project root.

## Support Files

- `references/ethereal-style-composition.html` — Working 30s composition with 4 phases matching Tuấn Anh's style reference
- `references/remotion-quickstart.md` — Remotion stack for multi-scene cinematic clips
- `templates/tiktok-subtitle-composition.html` — Drop-in sub-composition template for TikTok word-level subtitle sync (validated 2026-07-16). Replace `__PHRASES_DATA__` with `[{start, end, text}, ...]` from Whisper word-level timestamps. See "TikTok Subtitle Workflow" section above.
- `templates/tiktok-motion-text-composition.html` — Motion text sub-composition: words pop-in with bounce + slide-up + glow active word. **NEW 2026-07-16.** Use when user wants kinetic typography / chữ chuyển động (NOT subtitle). See "TikTok Motion Text Workflow" section.
- `scripts/extract_tiktok_phrases.py` — Word-level JSON → phrases.json converter. Auto-warns and blocks if output >30 phrases (HyperFrames DOM limit). Usage: `python3 scripts/extract_tiktok_phrases.py whisper_out/audio.json`
- `scripts/merge_tiktok_phrases.py` — Merge raw Whisper phrases (e.g. 80) into fewer grouped phrases (e.g. 27). **NEW 2026-07-16.** Usage: `python3 scripts/merge_tiktok_phrases.py phrases_raw.json --group-size 3 --js`
- `references/cinematic-trailer-3d-pattern.md` — **NEW 2026-07-16.** Full CSS-FX reference for cyberpunk/3D cinematic trailers: vignette + scanline + chromatic edges + anamorphic streak + volumetric glow + multi-layer bloom + deterministic particle dust + vanishing point lines. Verified working in HyperFrames v2 (vision AI 64/60 vs reference 60/60). Use this pattern when user wants 3D depth + bloom aesthetic instead of default ethereal-minimal.
- `references/3d-trailer-hyperframes-progression.md` — **NEW 2026-07-17.** Full V1→V5 progression: 5 versions từ CSS flat → CSS perspective → rAF loop "no static pixel" rule → Three.js ShaderMaterial → MeshStandardMaterial + PBR + cast shadow. Includes 3-point lighting setup, 5 mesh scene builders, performance budget (23 MB / 30s @ 1080p), quantitative motion_diff_check gate, "every pixel must move" HARD RULE. Use this khi user nói "3D trailer / cyberpunk / cinematic depth".
- `scripts/trailer_contact_compare.py` — **NEW 2026-07-16.** Generate side-by-side vision-AI contact sheet for trailer QA. Extracts frames from reference + my MP4 at given timestamps, builds comparison grid. Usage: `python3 scripts/trailer_contact_compare.py --ref ref.mp4 --my mine.mp4 --timestamps 4 8 13 17 25 --out /tmp/cmp.jpg`. Send output JPG to vision AI with the comparison prompt from `references/cinematic-trailer-3d-pattern.md`.
- `scripts/motion_diff_check.py` — **NEW 2026-07-16.** Quantitative "no static pixel" rule check. Extracts 2 frames at small dt (default 0.3s), computes pixel-wise diff, reports % pixels changed. >30% = excellent motion, <5% = appears frozen. Use this to objectively verify the "every pixel must move" trailer rule (anh dặn 2026-07-17: *"nếu làm animation thì mọi hình ảnh trên screen đều phải được animation hết chứ không được có ảnh hoặc chỗ nào tĩnh hết"*). Usage: `python3 scripts/motion_diff_check.py trailer.mp4 --t1 0.0 --t2 0.3`.

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
- [[remotion]] — React-based video generation (sibling — see "Siblings" section below)
- [[manim-video]] — Python + LaTeX math animations (sibling — see below)
- [[tiktok-viral-script]] — TikTok script writing

---

### Siblings: HyperFrames vs Remotion vs Manim (decision matrix)

This skill covers **HyperFrames** (HTML/GSAP → MP4). The other two major "code-to-video" tools used in the Hermes agent fleet:

| Tool | Input | Strength | When to pick |
|------|-------|----------|--------------|
| **HyperFrames** | HTML/CSS/JS + GSAP timelines | Easiest setup, simplest primitives, ethereal/glass aesthetic baked in | Quick 30s TikTok clips, brand reveals, kinetic typography |
| **Remotion** | React + TypeScript components (frame-based, headless Chrome → H.264) | Component composition, version-controllable, scales to complex multi-shot timelines, npm ecosystem | Multi-shot trailers, promo videos with 5+ distinct scenes, code-native agency |
| **Manim CE** | Python (LaTeX math typesetting, programmatic animation) | Math/algorithm/data viz, 3Blue1Brown aesthetic | Math explainers, algorithm visualizations, educational cinema |

**Quick rule of thumb:**
- "Make me a 30s TikTok reveal with glassmorphism" → **HyperFrames** (it's pre-tuned for this)
- "Make me a 2-min cinematic trailer with 9 scenes, ASCII overlays, and FFmpeg pass" → **Remotion**
- "Explain how gradient descent works with a moving loss curve" → **Manim"

### Cross-Framework Compare-and-Pick Workflow (NEW 2026-07-17 — trailer session)

When user asks "make me a trailer like [reference] / try Remotion + HyperFrames + Manim / compare 3 frameworks":

**6-step pattern**:
1. **Download reference** via `yt-dlp --cookies-from-browser chrome` (Twitter/X.com uses 8.85MB) → `~/Downloads/`
2. **Extract 4-6 contact frames** at strategic timestamps (HOOK / WALL / DATA / CTA) using `ffmpeg -ss <t>`
3. **Build vision_understand_image contact sheet** (4×2 grid, 540×540 each) → save to `~/Downloads/ref_compare/`
4. **Render 3 versions**: HyperFrames flat (V1), Remotion 1080p, Manim 480p15 — all 30s
5. **Score matrix**: 6 dimensions (3D depth, bloom, animation, lighting, color, cinematic impact) × 3 frameworks. Vision AI rates each frame 1-10. Pick winner.
6. **Iterate on winner** — apply "no static pixel" rule + 3D progression (see below)

**Real case 2026-07-16 (NOUS Accelerated Business Hackathon trailer)**:
- Reference: 66.08s, 2160×2160, 24fps, h264
- Built 3 separate projects: `~/Documents/GitHub/nous-trailer/` (Remotion), `nous-trailer-manim/` (Manim), `nous-trailer-hyperframes/` (HyperFrames)
- Vision AI verdict: HyperFrames 49/60, Remotion 6.25/10, Manim 4.5/10 → picked HyperFrames
- Then iterated on HyperFrames: V2 (+15pts CSS-3D+bloom), V3 (+30% all-pixel-animated), V4 (Three.js), V5 (PBR), Master (V3+V5 merged)

**Cost reference (macOS M-series, 30s clip)**:
- HyperFrames V1 flat: 25s render, 1.5 MB output
- HyperFrames V3 animated: 50s render, 13 MB
- HyperFrames V5 PBR: 46s render, 23 MB
- Remotion 1080p: 40s render, 6 MB
- Manim 480p15: 3-4 min render, 1 MB
- Manim 1080p30: 10-30 min render, 8-15 MB

**Save canonical to `/Volumes/Storage-1/Tiktok-Tuan-Anh/`** — NOT `~/Downloads/` (anh's canonical path for TikTok content). Ffmpeg verify before ship.

### V1→V5 3D-Trailer Progression (NEW 2026-07-17)

When user wants a **3D cinematic trailer** (cyberpunk/analog/B&W with bloom + perspective), build progressively through 5 versions:

| V | Approach | Size | Tech | Strengths | When to stop |
|---|---------|-----:|------|----------|--------------|
| V1 | Flat CSS 2D | 1.5 MB | CSS background-image + box-shadow | Fast iteration | If user wants "more depth" |
| V2 | CSS perspective + multi-layer glow | 3 MB | transform: perspective(1500px) rotateY + box-shadow stack | Best speed/quality | If user wants "real 3D" |
| V3 | "No static pixel" rule + rAF loop | 13 MB | Every DOM element reads frame, applies animated CSS | Best motion density | If user wants "3D depth" |
| V4 | Three.js ShaderMaterial | 25 MB | WebGL + custom GLSL | First real 3D | If shader warnings appear |
| V5 | MeshStandardMaterial + PBR + cast shadow | 23 MB | ACES Filmic tone mapping + 3-point lighting + PCFSoftShadowMap | Production quality | Ship |
| Master | V3 animation + V5 PBR | 23 MB | Both drivers share `window.__currentFrame` | Best of both | Ship |

**The "no static pixel" rule (anh dặn 2026-07-17)**: When user says "if making animation, every image on screen must be animated, no static image or place anywhere". The implementation pattern is a single rAF loop that reads frame count and writes to every DOM element:

```js
function tick(now) {
  const frame = Math.floor((now - startTime) / (1000 / fps));
  // EVERY element gets a frame-driven value
  charts.forEach(c => c.innerHTML = rebuildChart(frame));
  glows.forEach(g => g.style.boxShadow = `0 0 ${30 + Math.sin(frame*0.1)*8}px color`);
  particles.forEach(p => { p.style.top = `${p.initY - frame * p.speed}px`; });
  requestAnimationFrame(tick);
}
```

**Quantitative motion verification gate** (CRITICAL):
```bash
python3 scripts/motion_diff_check.py trailer.mp4 --t1 0.0 --t2 0.3
# Output:
#   "At 0.3s vs 0.0s: 37.9% pixels changed"
#   "If > 10%, animation is LIVE"
# >30% = excellent motion, <5% = FAIL (frozen content)
```

### Three.js Caveats (NEW 2026-07-17 — Master trailer)

**Pattern**: HyperFrames host root + Three.js canvas overlay riêng. Renders qua 2 rAF loops độc lập, giao tiếp qua `window.__currentFrame` (set by trailer.js master rAF, read by three-scene.js independent rAF).

**Top 4 mistakes** (verified V4→V5 fix):
1. `ShaderMaterial` with custom GLSL → `WebGL: useProgram: program not valid` warning. Fix: use `MeshStandardMaterial` (built-in PBR).
2. `MeshBasicMaterial` for everything → flat look. Fix: 3-point lighting (key 1.6 + fill 0.9 + rim 0.7).
3. No `castShadow`/`receiveShadow` → bars look glued to floor. Fix: 4 places must opt-in (renderer.shadowMap.enabled, light.castShadow, mesh.castShadow, mesh.receiveShadow).
4. `ShaderMaterial` errors cause silent render failure. Fix: check render log for `useProgram` warnings.

**Lighting setup that works** (copy-paste ready):
```js
const ambient = new THREE.AmbientLight(0x404060, 0.8);
scene.add(ambient);
const keyLight = new THREE.DirectionalLight(0xffffff, 1.6);
keyLight.position.set(8, 12, 16);
keyLight.castShadow = true;
keyLight.shadow.mapSize.width = 1024;
keyLight.shadow.mapSize.height = 1024;
scene.add(keyLight);
const fillLight = new THREE.DirectionalLight(0x88ff88, 0.9);
fillLight.position.set(-10, 0, 8);
scene.add(fillLight);
const rimLight = new THREE.DirectionalLight(0x4444ff, 0.7);
rimLight.position.set(0, -8, -12);
scene.add(rimLight);
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
```

### Vision AI Contact Sheet Pattern (NEW 2026-07-17)

When comparing multiple trailer versions, use vision_understand_image with a 4×2 contact sheet JPG:

```python
# 1. Extract 6 strategic frames at HOOK, WALL, DATA, CTA, LOGO, OUT
for t in [4, 8, 13, 17, 25, 28]:
    ffmpeg -y -ss $t -i trailer.mp4 -frames:v 1 -vf scale=540:-1 out_${t}.jpg

# 2. Build 4×2 grid with PIL
from PIL import Image, ImageDraw, ImageOps
# TILE=540, 4 cols, 2 rows, label timestamps
```

**Vision AI prompt template** for trailer comparison:
> "Compare 6 frame tại cùng timestamp giữa Reference NOUS trailer và HyperFrames V2. Đánh giá: 3D có visible không, real perspective có khác perspective CSS không, depth/shading có đúng không, hay đang trống vì shader lỗi?"

**Scoring pattern** (vision returns 1-10 per dimension):
- 3D depth (real perspective vs CSS fake)
- Bloom & lens flare (cinematic quality)
- Animation smoothness
- Lighting & shading
- Color grading
- Cinematic impact (overall)
- → Total /60, compare to reference 60/60

**Real case verdict 2026-07-16**: HyperFrames V1=49/60, V2=64/60 (+30% improvement via CSS-3D + bloom).

⚠️ **Common misconception (corrected 2026-07-16):** Earlier memory suggested "HyperFrames only renders HeyGen avatar". This is WRONG. HyperFrames is an open-source Apache 2.0 framework from HeyGen that renders arbitrary HTML/CSS/JS compositions to MP4. Don't repeat the wrong claim.

## When user asks for one of these — load the right skill

- "remotion / manim / hyperframe comparison" or "code-based motion graphics" → THIS skill + see sibling recipes below
- "math explainer / 3Blue1Brown / algorithm viz" → [[manim-video]]
- "TikTok 30s clip / glass aesthetic / brand reveal" → THIS skill's HyperFrames workflow
### Inputs verified
- Source clip: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-gan-iphone-04072026-v5.mp4` (1728×3072, 32.6s, H.264/AAC)
- Output shipped: `/Volumes/Storage-1/Tiktok-Tuan-Anh/sac_du_phong_liquid_glass_v1_32s.mp4` (1080×1920, 32.0s, 16.3 MB)
- Renderer: HyperFrames v0.7.60 with `ios26-liquid-glass` example + custom 3-phase GSAP timeline

### ⚠ STOP-AND-ASK rule (talking-head overlay)

When building motion graphics over a talking-head video for this user, you MUST collect these inputs BEFORE writing any HTML or asking HyperFrames to render:

1. Position of the face in the source frame. If you don't know it yet, run face detection (see `references/talking-head-overlay-patterns.md`) before laying out text. The user has corrected 10+ rebuilds of one clip where text occluded the face.
2. The user's preferred layout zone for the glass card / chart / overlay — in their own words. "Text top + bottom" is acceptable input. "PIP + glass card center during crop" is acceptable input. Anything vague counts as missing input.
3. Whether the phase uses full-face talking head OR a corner PIP inset. The layout strategy differs completely between them (face is full vs face is in PIP).

If any of these is missing, write them down, ask once, then proceed. The cost of asking is one round-trip; the cost of guessing is another 4-rebuild loop. This rule overrides the "don't ask, just do" default — for this user, on this task class, that default is wrong.

### 📐 Layout zones rule (talking-head video)

Once you know where the face is, divide the 1080×1920 frame into three zones and place ONE content type per zone. Mixing all content into one zone is the user's most common complaint.

| Zone | Y range | What goes here |
|---|---|---|
| TOP | 0–440 px | eyebrow pill, title, watermark |
| CENTER | 440–1430 px | **FACE in full-face phases. DO NOT place text here.** |
| BOTTOM | 1500–1800 px | stats, CTA, captions |

When the phase uses a corner PIP (340×340 typical, top-left), and the background goes black underneath, the CENTER zone becomes available again — fill it with a liquid-glass card. The single most common miss is leaving the black-background PIP zone with only the PIP and nothing else. Always fill it with a glass card AND keep at least one smaller element on the side.

### ✨ Liquid glass — the 5 layers

The phrase "liquid glass" refers to a frosted iOS-style surface, not a dark `rgba(15,20,30,…)` panel. If the user says "the liquid glass is gone," that's a regression. Five layers are required:

1. `background: rgba(255, 255, 255, 0.16–0.22)` — white tint
2. `backdrop-filter: blur(32–40px) saturate(180%)` — the glass effect
3. `border: 1.5px solid rgba(255, 255, 255, 0.35–0.45)` — hairline edge
4. `::before` with `radial-gradient(circle at 15% 0%, rgba(255,255,255,0.5), transparent 45%)` — top-left corner shine
5. `inset 0 1px 0 rgba(255,255,255,0.6)` in `box-shadow` — top inner highlight

### 👁 Verify by EYE before shipping

`npx hyperframes check` does NOT verify:
- whether a glass card is occluding the speaker's face,
- whether two phases' tweens overlap on screen,
- whether text in the BOTTOM zone collides with a caption bar.

After `check` passes, extract frames at each phase's mid-point with `ffmpeg -y -ss <t> -i output_silent.mp4 -frames:v 1 frame_t<t>.jpg` and feed them through vision_analyze. If even one frame shows the speaker's eyes occluded or text duplicated across zones, do not ship — fix and re-render.

The user's exact feedback after a string of unverified rebuilds: *"face đè lên MẶT ANH"*, *"phần nền đen ở trung tâm bị trống"*, *"các chữ đang đè lên nhau"*. Those are signals about layout, not HyperFrames config.

### 7-step verified pipeline

```bash
# 1. Pre-flight: scan for Hermes-Edit folder (anh đã explicit dặn 17/07 — KHÔNG assume top-level)
find /Volumes/Storage-1 -maxdepth 4 -name "*.mp4" -type f | head -50
ls /Volumes/Storage-1/Pocket3/Hermes-Edit/         # canonical final render path
ls /Volumes/Storage-1/Tiktok-Tuan-Anh/             # canonical inspection folder

# 2. Scale source 1728x3072 → 1080x1920 (TikTok spec)
mkdir -p assets/source
ffmpeg -y -i source.mp4 \
  -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  -t <duration> \
  assets/source/clip_1080x1920.mp4

# 3. Init project với PROVEN example
cd /tmp/<project-name>
npx --yes hyperframes init --non-interactive --example=ios26-liquid-glass
# Nếu example fail → try --example=blank + manually author composition

# 4. Move/copy composition → index.html (HyperFrames REQUIRES index.html as entry)
cp compositions/<name>.html index.html

# 5. Patch LINT ERRORS (5 fixes bắt buộc - xem bảng dưới)

# 6. Run validation gate
npx --yes hyperframes lint     # → 0 errors / 0 warnings
npx --yes hyperframes check    # → PASS

# 7. Render + verify + ship
npx --yes hyperframes render --quality draft --output /tmp/output/preview.mp4
# Vision verify 5 frames tại key timestamps (HOOK / CARD-IN / CARD-MID / CTA-IN / CTA-MID)
cp preview.mp4 /Volumes/Storage-1/Tiktok-Tuan-Anh/<name>_v1_<duration>s.mp4
```

### Critical rules discovered during verified run

1. **Hermes-Edit folder scan lesson (FIRST-CLASS - anh đã explicit dặn 17/07):** Final renders output path = `/Volumes/Storage-1/Pocket3/Hermes-Edit/`, KHÔNG PHẢI top-level `~/Hermes-Edit/` hoặc `/Volumes/Storage-1/Hermes-Edit/`. Khi user nói "Hermes-Edit" → SEARCH RECURSIVE depth ≥ 3. L34 cleanup binary rule KHÔNG có nghĩa folder này bị xóa.
2. **HyperFrames `--example=ios26-liquid-glass`:** Tránh `--example=minimal` (không tồn tại). Nếu example fail với "missing index.html" → tái sử dụng structure nhưng author composition thủ công.
3. **HyperFrames REQUIRES `index.html` ở root:** Composition trong `compositions/*.html` KHÔNG render được nếu thiếu root index.html. Pattern: `mv compositions/my-comp.html index.html`.
4. **HTML comment BEFORE `<!doctype html>` triggers `root_composition_missing_html_wrapper` lint:** Luôn strip HTML comment ở đầu file trước khi render.
5. **Template literal `${var}` trong `querySelector` breaks CSS parser:** Thay bằng hardcoded `[data-composition-id="hardcoded-name"]`.
6. **`<video>` cần `id="..."` attribute, không chỉ `class="..."`:** HyperFrames producer injects frames by `getElementById`. Không có id → video FROZEN trong render.
7. **Source video PHẢI scale 1080×1920 TRƯỚC khi copy vào project:** Pocket3 quay 1728×3072 portrait 4K.
8. **Render TIMING (M-series Mac):** 32s clip 1080×1920 = ~22s render (`--quality draft`). Default = draft OK cho iteration.

### Lint error table (verified 2026-07-17)

| Error | Fix |
|-------|-----|
| `root_missing_dimensions` | Add `data-width="1080" data-height="1920"` to root |
| `media_missing_data_start` | Add `data-start="0" data-duration="..."` to `<video>` |
| `media_missing_id` | Add `id="..."` to `<video>` (required for renderer) |
| `template_literal_selector` | Replace `${var}` with hardcoded string in querySelector |
| `root_composition_missing_data_start` | Add `data-start="0"` to root composition |
| `root_composition_missing_html_wrapper` | File must start with `<!doctype html>` (no comment before) |

### Real case proof (16:07 today)

- Lint: 0 errors / 0 warnings
- Check: PASSED (1 contrast warning OK)
- Render: 32.0s, 1080×1920, H.264, 16.3 MB, 22s render time
- Vision verify (5 frames t={2,8,15,22,28}): all 3 phases visible
- Ship: `/Volumes/Storage-1/Tiktok-Tuan-Anh/sac_du_phong_liquid_glass_v1_32s.mp4` ✓

### Template available (paste-modify)

- `templates/tiktok-liquid-glass-talking-head.html` — Copy-paste base. Replace `__HOOK_LINE_1__`, `__CARD_TITLE__`, `__USP_*__`, `__PRICE_*__`, `__CTA_*__`, `__HANDLE__` placeholders, plus GSAP phase timing (search for `// PHASE 1:`, `// PHASE 2:`, `// PHASE 3:`).

## Remotion sibling recipe (added 2026-07-16)

Verified working stack for a 9-scene cyberpunk trailer:

```json
// package.json — version pins matter (TypeScript 5.5.0 doesn't exist on npm, use 5.7.3+)
{
  "name": "trailer",
  "version": "0.1.0",
  "scripts": {
    "build": "remotion render src/index.ts Trailer out/trailer.mp4",
    "studio": "remotion studio src/index.ts"
  },
  "dependencies": {
    "@remotion/cli": "4.0.290",
    "remotion": "4.0.290",
    "react": "19.0.0",
    "react-dom": "19.0.0"
  },
  "devDependencies": {
    "@types/react": "19.0.0",
    "typescript": "5.7.3"
  }
}
```

```ts
// remotion.config.ts
import { Config } from '@remotion/cli/config';
export default { Config: { fps: 24, durationInFrames: 24*30, width: 1080, height: 1080, outDir: 'out' } satisfies Config };
```

```bash
# Render (Chrome headless, ~40s for 720 frames)
npx remotion render src/index.ts Trailer out/trailer.mp4 \
  --browser-executable="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --concurrency=2
```

Full scaffold + 9-scene template at `templates/remotion-trailer-skeleton/`. See `references/remotion-quickstart.md` for the gotchas.

### Remotion pitfalls (added 2026-07-16)

**P1. `random()` returns a number, not a closure**
- Remotion 4.x: `random(key)` returns a single `number` in `[0,1)`. Don't write `random('seed')()` — that throws `TypeError: rng is not a function`.
- WRONG: `const rng = random('g'); const x = rng();`
- RIGHT: `const rng = (k: string) => random(`g-${seed}-${k}`); const x = rng('x0');`

**P2. CSS `filter: grayscale()` does NOT override brand-colored text**
- Inline `<div style={{ color: '#76b900' }}>NVIDIA</div>` with `filter: grayscale(1)` on parent will NOT turn the text gray if the browser falls back to a system italic font that renders the glyph with its own color hint.
- Fix for end-cards that need true B&W: replace CSS text with an actual PNG/SVG logo of the brand mark, OR use `mix-blend-mode: difference` against the background, OR hand-pick the gray hex.
- Real case (Nous trailer, 2026-07-16): Stripe wordmark stayed `#635BFF` purple after `grayscale(1) contrast(1.4)` because Chrome rendered the italic fallback with brand color.

**P3. `npm install` silently fails on bad version pins**
- `"typescript": "5.5.0"` does not exist on the npm registry — fails with `ETARGET` after silent retry.
- Always check `npm view <pkg> versions` or use exact versions verified in existing projects.
- Verified-good pin (2026-07-16): typescript 5.7.3 + @remotion/cli 4.0.290 + react 19.0.0.

**P4. `pix_fmt=yuvj420p` is deprecated but works**
- Remotion's h264 encoder outputs `yuvj420p` (full-range). Telegram/iPhone/QuickTime all play it fine. If a stricter downstream tool rejects it, post-process with: `ffmpeg -i in.mp4 -pix_fmt yuv420p -c:v libx264 out.mp4`.

**P5. Don't iterate on color/logo fixes forever**
- After 2 visual-feedback rounds shipping a 30s trailer, the marginal polish gains diminish sharply. Ship the working version, note the remaining issues in the ship message, let the user decide if another pass is worth it.
- Real case: spent 6 min trying to force B&W on Stripe wordmark; the simpler fix (swap to PNG logo) would have been a 30-second change but I kept tweaking CSS filters. Stop after 2 rounds on cosmetic issues.