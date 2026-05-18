# HyperFrames TikTok Style Guide — Ethereal Minimal

> Reference video analyzed May 2026: https://youtu.be/xBZzVNi_4Xw

## Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Background | Near black with blue tint | `#0c0c14` |
| Electric blue | Primary accent | `#4da6ff` |
| Purple gradient | Secondary | `#9b59b6` |
| Coral/orange | Warm accent spheres | `#ff6b4a` |
| Lavender | Soft highlights | `#c8a2c8` |
| White | Text, specular | `#ffffff` |

## Typography

- **Font**: Inter (Google Fonts) — clean, modern sans-serif
- **Weights**: 300 (light) for body, 600-700 (bold) for headings
- **Sizing**: Large headlines (48-72px), moderate body (18-24px)
- **Effects**: Subtle text-shadow for glow on key text

## Layout

- **Aspect ratio**: 9:16 portrait for TikTok
- **Focal point**: Center-weighted, elements converge to center
- **Depth**: Multiple layers — background particles (slow), midground cards, foreground text
- **Spacing**: Generous whitespace, elements breathe

## Visual Effects

### Glassmorphism
```css
.glass-card {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}
```

### Glow/Bloom
```css
.glow-text {
  text-shadow: 0 0 20px rgba(77, 166, 255, 0.8),
               0 0 40px rgba(77, 166, 255, 0.4);
}
```

### Chromatic Aberration
```css
/* Use pseudo-elements offset by 1-2px in red/cyan channels */
.chromatic::before {
  content: attr(data-text);
  position: absolute;
  left: 2px;
  color: rgba(255, 0, 0, 0.5);
}
```

## Animation Principles

- **Easing**: `power2.inOut` or `power3.inOut` — smooth, never linear
- **Duration**: 0.6-1.2s for transitions, 2-4s for full reveals
- **Stagger**: 0.1-0.2s between list items
- **Motion style**: floating, weightless — elements drift not snap
- **Parallax**: Background particles move slower than foreground

## Particle Effects

```javascript
// Floating particle field
function createParticles(count) {
  for (let i = 0; i < count; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    gsap.to(particle, {
      y: `random(-100, 100)`,
      x: `random(-50, 50)`,
      opacity: `random(0.2, 0.6)`,
      duration: `random(3, 6)`,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut'
    });
  }
}
```

## DO NOT USE

- [ ] `bounce` easing — too aggressive
- [ ] `elastic` — looks cheap on TikTok
- [ ] White flash transitions (use smooth crossfades)
- [ ] Sharp snap animations
- [ ] Low contrast text on background