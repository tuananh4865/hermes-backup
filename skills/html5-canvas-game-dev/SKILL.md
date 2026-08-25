---
name: html5-canvas-game-dev
description: Build HTML5 Canvas games as single-file deliverables (one .html with inline CSS/JS, no build step, no framework). Covers top-down RPG, GTA-lite open world, platformer, and arcade patterns. Load when user says "make a game", "1 file HTML", "single-file game", "browser game", or wants a playable prototype in <50KB.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows, browser]
metadata:
  hermes:
    tags: [game-dev, canvas, html5, single-file, javascript, prototype]
    related_skills: [frontend-ui-engineering, prototype, shipping-and-launch, github-operations]
---

# HTML5 Canvas Game Development (Single-File)

Build browser games that ship as ONE HTML file. No npm, no build, no server — open the file in any browser and it works. Perfect for portfolio pieces, prototypes, jam entries, or "I want to test this idea in 30 minutes" tasks.

## When to Use

- User asks for a "game" and "single file" / "1 HTML" / "no install" / "test từ xa"
- Top-down RPG, action, puzzle, arcade, GTA-lite, racing, roguelike — anything that fits in one screen + tilemap or vector world
- User wants to test an agent's ability to ship a polished interactive artifact
- User wants a **GTA-style / open-world / driving game** (see `references/gta-v-mechanics-implementation.md` for the 2D adaptation map)
- User wants to build an **evolving single-game project** (v1.0 → v5.0) with research-backed roadmap (the GTA V Mini / City Drift pattern)

## When NOT to Use

- 3D / WebGL / Three.js games → needs asset pipeline, not single-file
- Multiplayer with backend → use `multi-agent-orchestrator` patterns + WebRTC layer
- Mobile-first PWA with offline support → use `prototype` skill, not this
- "Real" game with > 10K LOC → split into modules, this is for prototypes

## Core Architecture (the 8 building blocks)

Every Canvas game is a loop over these:

```
1. INPUT     → keys{} / justPressed{} / pointer / gamepad
2. STATE     → player, enemies, items, particles, world[]
3. UPDATE    → move entities, run AI, check collisions, fire timers
4. RENDER    → clear → tiles → entities → player → HUD (in z-order)
5. CAMERA    → follow player, clamp to world bounds
6. HUD       → DOM overlay (cheaper than canvas text)
7. AUDIO     → Web Audio API synth (no asset files)
8. SAVE      → localStorage (auto-save HP/gold/position every N seconds)
```

A clean 50KB game implements all 8. A 100KB game has polish on every one.

## Project Structure (recommended)

```
game-project/
├── games/
│   ├── game1.html              # single-file games live here
│   ├── game2.html
│   └── index.html              # landing page with cards linking to each
├── docs/
│   ├── ROADMAP.md              # version plan (v1.0 → vN.0)
│   ├── CHANGELOG.md            # SemVer per game
│   └── CONTRIBUTING.md
├── assets/                     # shared sprites/audio (future)
├── .github/                    # NOTHING HERE if using GitHub Pages legacy
└── README.md
```

**Why this layout:** Each game = 1 file in `games/`, landing page links them. GitHub Pages serves `games/index.html` at the repo root URL. Adding a new game = drop a file + add a card to index.html + commit. No coordination needed.

## Critical Patterns

### 1. Axis-separated collision (no wall stick)

**Anti-pattern (breaks diagonal movement):**
```js
if (!isBlocked(newX, newY)) { player.x = newX; player.y = newY; }
```

**Correct:**
```js
if (!isBlocked(newX, player.y, r)) player.x = newX;
if (!isBlocked(player.x, newY, r)) player.y = newY;
```

Check X and Y independently → player slides along walls instead of sticking.

### 2. Dot-product attack cone (cleaner than atan2)

**Use when:** "is enemy in front of me, within angle θ?"

```js
const atkDir = { up:[0,-1], down:[0,1], left:[-1,0], right:[1,0] }[player.dir];
const ddx = e.x - player.x, ddy = e.y - player.y;
const dist = Math.sqrt(ddx*ddx + ddy*ddy);
const dot = (ddx*atkDir[0] + ddy*atkDir[1]) / dist;  // normalized
if (dist < range && dot > 0.5) /* hit */;  // dot > 0.5 ≈ within 60° cone
```

**Why:** atan2 + range check has edge cases (full circle vs cone, distance-weighted angle). Dot product is one line, works at any distance, easy to tune.

### 3. AI state machine via timer (not switch-every-frame)

```js
e.dirTimer -= dt;
if (e.dirTimer <= 0) {
  e.dirTimer = 1 + Math.random() * 1.5;
  if (dist(e, player) < 200) {
    // CHASE
    const ang = Math.atan2(player.y - e.y, player.x - e.x);
    e.dirX = Math.cos(ang); e.dirY = Math.sin(ang);
  } else {
    // WANDER
    e.dirX = Math.cos(Math.random() * Math.PI * 2);
    e.dirY = Math.sin(Math.random() * Math.PI * 2);
  }
}
```

**Why:** Re-pick direction every 1-2s, not every frame. Feels more natural (jittery AI = bug), costs 0 performance.

**State variants to add:** `IDLE`, `PATROL`, `ATTACK`, `FLEE`, `SCARED` (run from player with wanted level). Pick 2-3, don't build a full FSM for a prototype.

### 4. Wanted level + police AI (engagement multiplier)

```js
if (player.wanted >= 2) {
  policeSpawnTimer -= dt;
  if (policeSpawnTimer <= 0 && policeCars.length < player.wanted) {
    policeSpawnTimer = 5;
    // Spawn at random edge of screen
    const edge = Math.floor(Math.random() * 4);
    /* offset by 400px in random direction */
  }
}
// Police speed scales with wanted level
maxSpeed: 250 + player.wanted * 15  // 3 stars = 295 km/h
```

**Decay:** `wantedDecay -= dt; if (wantedDecay <= 0) { wanted--; wantedDecay = 8; }` — 8s per star gives "tension" window.

**Why this works:** Risk/reward is the core dopamine loop of GTA-style games. Even a 5-line wanted system makes a driving game 10x more engaging.

### 5. Steering scales with speed (realistic cars)

```js
if (Math.abs(v.speed) > 5) {  // only when moving
  const turnRate = (v.speed > 0 ? 1 : -1) * 2.2 * (Math.abs(v.speed) / v.maxSpeed);
  v.angle += steering * turnRate * dt;
}
```

**Key insight:** Reverse = negative turn direction. Near stop = can't turn (must keep speed to corner). High speed = more sensitive steering.

### 6. Camera follow with world clamp

```js
camera.x = player.x - W / 2;
camera.y = player.y - H / 2;
camera.x = Math.max(0, Math.min(WORLD_W * TILE - W, camera.x));
camera.y = Math.max(0, Math.min(WORLD_H * TILE - H, camera.y));
```

Always clamp to world bounds — never let camera show void beyond map.

### 7. Pixel art without sprite files

Draw with `ctx.fillRect` + `ctx.arc` directly:

```js
// Tree = trunk rect + canopy ellipse + 2 highlight circles
ctx.fillStyle = '#5a3a1a';
ctx.fillRect(px + 12, py + 20, 8, 12);
ctx.fillStyle = '#2d4a2d';
ctx.beginPath(); ctx.arc(px + 16, py + 14, 11, 0, Math.PI * 2); ctx.fill();
```

**Pros:** 0 asset cost, perfect for prototyping, can recolor on the fly.
**Cons:** Tedious for complex sprites, can't have multi-frame animation without re-drawing.

### 8. HUD as DOM overlay (not canvas text)

```html
<div id="hud" class="panel">
  <div class="row"><span>HP</span><span id="hp">100/100</span></div>
</div>
```

```css
#hud { position: absolute; top: 12px; left: 12px; ... pointer-events: none; }
```

**Why:** DOM text is sharp at any resolution. Canvas text blurs on mobile. `pointer-events: none` so HUD doesn't block clicks on game.

## Anti-Patterns to Avoid

| Anti-pattern | Why bad | Fix |
|--------------|---------|-----|
| Use `requestAnimationFrame` without `dt` cap | Tab unfocus → huge dt → teleport | `dt = Math.min(0.05, (now - last) / 1000)` |
| Use Atan2 for "in cone" check | Edge cases, verbose | Dot product (see pattern 2) |
| Inline canvas text for HUD | Blurry on mobile, slower | DOM overlay |
| 1x1px collision check | Tunnels through thin walls | Check 4 corners of bounding box |
| Save state in `localStorage` on every action | 1000s of writes/sec | Save every 5-10s, or on milestone events |
| Custom framework (mini-react) | Defeats single-file purpose | Vanilla JS + canvas |
| External CDN dependency | Breaks offline | Inline everything, or document the dependency |
| `<canvas>` resize on every frame | Layout thrashing | Set `width`/`height` attributes, not CSS |

## Audio (Web Audio API, no asset files)

```js
const ctx = new (window.AudioContext || window.webkitAudioContext)();
function playBeep(freq, duration) {
  const osc = ctx.createOscillator();
  const gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.frequency.value = freq;
  gain.gain.setValueAtTime(0.1, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + duration);
  osc.start(); osc.stop(ctx.currentTime + duration);
}
playBeep(440, 0.1);  // A4, 100ms
```

For richer sounds: layer multiple oscillators with different envelopes.

## Deployment Pipeline

1. Write `games/game.html` (single file, all inline)
2. Add card to `games/index.html` (link only, no copy of game code)
3. `git add . && git commit -m "🎮 [game-name] v1.0 init" && git push`
4. **No custom `.github/workflows/` needed** — GitHub Pages legacy auto-deploys
5. Test URL: `https://owner.github.io/repo/games/game.html`
6. Update `CHANGELOG.md` and bump version in `index.html`

**Don't push a workflow file** unless you need multi-stage builds. See [github-operations] § Pitfalls for why.

## Testing Checklist (before commit)

- [ ] Game loads with no console errors
- [ ] Controls responsive on keyboard (WASD tested)
- [ ] All 4 cardinal directions work (no input stuck)
- [ ] Player can be killed / lose state (not infinite)
- [ ] Wall collision prevents walking through (test diagonal corners)
- [ ] HUD updates in real time
- [ ] Tested in Chrome + Safari + Firefox
- [ ] Mobile viewport tested (even if desktop-only, shouldn't break)
- [ ] No external network calls (except documented CDN)

## Reference Implementations

See the support files for full game source code:

- `references/forest-wanderer-architecture.md` — top-down RPG patterns (40×30 tile world, NPC dialogue, slime AI, level-up loop). Total ~27KB.
- `references/city-drift-architecture.md` — GTA-lite open world (50×50 tile city, vehicle physics, wanted level, mission system, minimap). Total ~40KB.
- `references/gta-v-mechanics-implementation.md` — **GTA V → 2D adaptation map**. Concrete 2D code patterns for the 5 systems that carry 80% of GTA's engagement (vehicle physics, wanted escalation, NPC AI, mission design, audio synth), plus 10 visual juice patterns and the proven 7-version evolution path (40KB → 220KB over 6-9 months). Read this when building any GTA-style / open-world / driving game.
- `references/gta-v-mini-evolution-pattern.md` — **Case study**: how a 40KB prototype evolved into a research-backed 7-version roadmap. Covers the prototype-first / parallel-research / 7-version-plan pattern, the "replicate vs simplify vs skip" decision matrix, and the discipline of "polish before content" that Tuấn Anh mandated. Read this when scaling any small game prototype into a long-running project.

These are the "good" examples Tuấn Anh approved in the 2026-06-22 session — they hit "điều khiển trau chuốt + tương tác trau chuốt" the standard. Use them as templates for new games in this class.

## Related

- [github-operations] — for deployment to GitHub Pages (auto-deploy pattern, no custom workflow)
- [shipping-and-launch] — pre-launch checklist and feature flag strategy
- [frontend-ui-engineering] — DOM/CSS polish (HUD, landing pages)
- [prototype] — for design mocks (NOT game mechanics — use this skill for games)