---
name: motion-graphic-video
title: Motion Graphic Video Production
description: Create motion graphic videos for TikTok/content using HyperFrames (HTML/CSS/JS → MP4). Covers style matching, rendering, and TikTok-optimized output.
trigger: user wants to create a motion graphic / animated video / TikTok content with motion graphics
created: 2026-05-18
updated: 2026-05-18
confidence: high
tags: [video, motion-graphics, tiktok, hyperframes]
relationships: [tiktok-viral-script, learned-about-tuananh]
---

# Motion Graphic Video Production

## Overview

Use HyperFrames (HeyGen's open-source framework) to produce motion graphic videos from HTML/CSS/JS compositions. The framework compiles HTML animations into MP4 via Puppeteer/Chromium.

## Quick Start

```bash
# Install (one-time)
cd ~/.hermes/hermes-agent/optional-skills/creative/hyperframes
bash scripts/setup.sh

# Create project
npx hyperframes init my-video --non-interactive --example kinetic-type
cd my-video

# Lint (check for errors/warnings)
npx hyperframes lint

# Render
npx hyperframes render --quality draft --output /tmp/output.mp4
npx hyperframes render --quality high --output /tmp/output-hd.mp4
```

## Style Profiles for TikTok Content

### Ethereal Minimal (Tuấn Anh's preferred style)
- **Mood**: calm, mysterious, "Tech-Zen"
- **Colors**: dark backgrounds with electric blue/purple gradients, coral/orange accents, lavender tones
- **Effects**: glassmorphism UI panels (blur + transparency), volumetric light rays, floating particles, bloom/glow, chromatic aberration, deep depth of field, digital grain
- **Motion**: ease-in-out easing, floating/weightless movement, slow camera drift — AVOID aggressive/bouncy motion
- **Reference**: https://youtu.be/xBZzVNi_4Xw

### Dark Tech Minimal
- **Mood**: modern, clean, high-tech
- **Colors**: near-black background (#0a0a0f), electric blue primary (#00d4ff), white text
- **Effects**: subtle glow on key elements, gradient text, clean borders
- **Motion**: moderate slide-ins, fade transitions, badge rotation

### Glassmorphism Aesthetic
- **Background**: dark with subtle gradient
- **Cards**: `backdrop-filter: blur(20px)`, semi-transparent white/gray fill, subtle white border
- **Shadows**: colored box-shadows for glow effect
- **Text**: white/light with subtle text-shadow for glow

## Common Lint Warnings (Fix These)

| Warning | Fix |
|---------|-----|
| `gsap_css_transform_conflict` | Use `yPercent` instead of `transform: translateY()` in GSAP tweens |
| `overlapping_gsap_tweens` | Add `overwrite:"auto"` to GSAP tween config |
| `motion_path_missing_anchor` | Ensure each animated element has a clear anchor point |

## Rendering Tips

- **Draft quality**: faster, good for preview/iteration
- **High quality**: final output, longer render time
- **Dimensions**: 9:16 portrait (1080×1920) for TikTok
- **Duration**: keep under 30s for TikTok retention

## Composition Structure

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

## Tuấn Anh's Preferences

- **Hands-on testing**: wants to see results first, then discuss
- **Style**: prefers ethereal/minimal over aggressive motion
- **Voice**: Vietnamese casual — "anh" + "mấy con vợ"
- **Script**: see [[tiktok-viral-script]] for TikTok script approach

## Related Skills

- [[tiktok-viral-script]] — TikTok script writing
- [[remotion]] — alternative: React-based video generation

## References

- HyperFrames CLI: see `~/.hermes/hermes-agent/optional-skills/creative/hyperframes/`
- Style analysis reference: YouTube video analyzed May 2026