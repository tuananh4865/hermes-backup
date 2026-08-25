# City Drift — GTA-lite Reference Architecture

> **Live:** https://tuananh4865.github.io/mini-rpg-games/games/city-drift.html
> **Source:** `~/Projects/mini-rpg-games/games/city-drift.html` (40KB, single file)
> **Status:** v1.0.0, Tuấn Anh approved 2026-06-22

The 8-pattern GTA-lite reference: 50×50 tile city, 4 drivable vehicles, 5-star wanted system, police AI, 3 mission types, top-down combat, 25 NPCs + 40 parked cars, real-time minimap.

## What this game teaches

This is the **GTA-lite template** for any top-down open world game. Once you understand how this fits together, you can extend to:
- Larger maps (80×80, 5 districts)
- Day/night cycle
- Traffic AI (NPC drivers)
- Heists / story missions
- Multiplayer (WebRTC P2P)

Roadmap for next versions: `~/Projects/mini-rpg-games/research/gta-v-mini-roadmap.md`

## Full game source (annotated)

The actual shipped code is in `~/Projects/mini-rpg-games/games/city-drift.html` (1268 lines). Below are the **extracted patterns** with line references — copy-paste ready.

### Pattern 1: City grid generation (lines 190-243)

```js
const TILE = 64;
const WORLD_W = 50, WORLD_H = 50;
const world = [];

function generateCity() {
  // Init all grass
  for (let y = 0; y < WORLD_H; y++) {
    world[y] = [];
    for (let x = 0; x < WORLD_W; x++) world[y][x] = 0;
  }

  // Roads: grid every 8 tiles (5 horizontal, 5 vertical = 9 intersections)
  for (let y = 0; y < WORLD_H; y++) {
    for (let x = 0; x < WORLD_W; x++) {
      if ([5, 12, 19, 26, 33, 40].includes(y)) world[y][x] = 1; // horizontal
      if ([8, 16, 24, 32, 40].includes(x)) world[y][x] = 1;     // vertical
    }
  }

  // Buildings fill blocks, leave sidewalk edge (1 tile) quanh road
  for (let by = 0; by < 6; by++) {
    for (let bx = 0; bx < 5; bx++) {
      const baseX = bx * 8 + 1;
      const baseY = by * 7 + 1;
      for (let dy = 0; dy < 5; dy++) {
        for (let dx = 0; dx < 7; dx++) {
          const tx = baseX + dx, ty = baseY + dy;
          if (tx >= WORLD_W || ty >= WORLD_H) continue;
          if (world[ty][tx] === 1) continue;  // skip road
          if (dy === 4 || dx === 6) { world[ty][tx] = 3; continue; }  // sidewalk
          if (Math.random() < 0.15 && (dx > 0 && dy > 0)) { world[ty][tx] = 0; continue; }  // 15% empty for variety
          world[ty][tx] = 2;  // building
        }
      }
    }
  }
}
```

**Why this works:** 8-tile road spacing leaves 7-tile building blocks = perfect for top-down scale. 15% empty = visual variety without breaking block coherence.

**To scale up:** Change `WORLD_W/H = 80` and add more blocks. For districts, group blocks by `by` index (downtown = `by < 2`, suburb = `by >= 4`).

### Pattern 2: Vehicle physics (lines 526-620)

**Steering scales with speed + reverse awareness:**
```js
if (Math.abs(v.speed) > 5) {  // only turn when moving
  const turnRate = (v.speed > 0 ? 1 : -1) * 2.2 * (Math.abs(v.speed) / v.maxSpeed);
  v.angle += steering * turnRate * dt;
}
```

**Throttle + drag:**
```js
if (throttle > 0) v.speed += v.maxSpeed * 0.3 * throttle * dt;
else if (throttle < 0) v.speed += v.maxSpeed * 0.4 * throttle * dt;
else v.speed *= 0.98;  // drag
v.speed = Math.max(-v.maxSpeed * 0.3, Math.min(v.maxSpeed * boost, v.speed));
```

**Wall collision with reflection:**
```js
const newX = v.x + Math.cos(v.angle) * v.speed * dt;
const newY = v.y + Math.sin(v.angle) * v.speed * dt;
if (isSolid(newX, v.y, 20)) { v.speed *= -0.4; hit = true; }  // 40% bounce
else v.x = newX;
if (isSolid(v.x, newY, 20)) { v.speed *= -0.4; hit = true; }
else v.y = newY;
```

**To add drift:** On Space (brake) + high speed, increase turn rate 2-3x and reduce friction. See research doc for full drift physics.

### Pattern 3: 5-star wanted system (lines 522-562)

```js
// Trigger conditions
- Đâm NPC (+2 sao, -$100)
- Đấm NPC (+1 sao)
- Bắn NPC (+1 sao per bullet)
- Đâm tường ở tốc độ cao (+1 sao)

// Decay timer
if (player.wantedDecay <= 0) {
  player.wanted--;
  player.wantedDecay = 8;  // 8s per star
}

// Police spawn at 2+ stars
if (player.wanted >= 2) {
  policeSpawnTimer -= dt;
  if (policeSpawnTimer <= 0 && policeCars.length < player.wanted) {
    policeSpawnTimer = 5;
    // Spawn at random edge of screen
    policeCars.push({ maxSpeed: 250 + player.wanted * 15, ... });
  }
}
```

**Key insight:** Police speed scales with wanted level (3 sao = 295 km/h, gần bằng Sports car). Creates escalating challenge.

### Pattern 4: Mission system (lines 410-520)

3 mission types, each with custom logic:

```js
const missions = {
  taxi: {
    title: '🚕 Tài xế Taxi',
    desc: 'Chở khách đến điểm đánh dấu',
    start: () => { player.mission = { type: 'taxi', passenger: 1 }; },
    update: (dt) => {
      // Pickup at marker[0] → drop-off at marker[0], 60s timer
    },
  },
  delivery: { /* similar structure */ },
  chase: { /* similar structure */ },
};

if (consume('m')) startMission(Math.floor(Math.random() * 3));
```

**Reward scaling:** `baseReward + (timeRemaining * timeMultiplier)` — faster = more money. Creates skill expression.

### Pattern 5: NPC + traffic reaction (lines 565-580)

```js
if (player.wanted >= 1) {
  // NPCs RUN AWAY from player
  const ang = Math.atan2(n.y - player.y, n.x - player.x);
  n.angle = ang;
  n.speed *= 2;  // panic run
}
```

**Wander timer pattern (same as Forest Wanderer):**
```js
n.wanderTimer -= dt;
if (n.wanderTimer <= 0) {
  n.wanderTimer = 2 + Math.random() * 3;
  n.angle = Math.random() * Math.PI * 2;
}
```

### Pattern 6: Minimap (lines 870-905)

```js
function drawMinimap() {
  miniCtx.fillStyle = '#000';
  miniCtx.fillRect(0, 0, 160, 160);
  const scale = 160 / (WORLD_W * TILE);
  
  // Tiles
  for (let y = 0; y < WORLD_H; y++) {
    for (let x = 0; x < WORLD_W; x++) {
      const t = world[y][x];
      const c = t === 1 ? '#555' : t === 2 ? '#7a5a3a' : t === 4 ? '#1a4a7a' : '#3d5a3d';
      miniCtx.fillStyle = c;
      miniCtx.fillRect(x * TILE * scale + ox, y * TILE * scale + oy, TILE * scale + 1, TILE * scale + 1);
    }
  }
  // Player dot (always center), vehicles, police, mission markers
}
```

**Why this is essential for open world:** Without minimap, player has no sense of direction in 50×50 tile world. The minimap is player-centered (player always at 80,80) — rotate the rendering if you want player-relative.

### Pattern 7: Vehicle entry/exit (lines 290-320)

```js
// On foot, press E
if (consume('e')) {
  let nearest = null, nearDist = 50;
  for (const v of vehicles) {
    if (v.hp <= 0) continue;
    const d = dist(player, v);
    if (d < nearDist) { nearest = v; nearDist = d; }
  }
  if (nearest) { player.inVehicle = true; player.vehicleRef = nearest; }
}

// In vehicle, press E
if (consume('e')) {
  player.inVehicle = false;
  player.vehicleRef = null;
  player.x = v.x + Math.cos(v.angle + Math.PI/2) * 35;  // exit to side
  player.y = v.y + Math.sin(v.angle + Math.PI/2) * 35;
}
```

**Pitfall:** Don't forget to sync `player.x/y = v.x/y` every frame while in vehicle. The vehicle moves; the player needs to follow.

## Lines you should refactor next (per roadmap v1.1)

These are the **highest-leverage improvements** for v1.1:

1. **Add Web Audio** — engine pitch by RPM, gun SFX, crash SFX (lines 864+ for shootBullet)
2. **Save state to localStorage** — every 5s save player + vehicle state (currently no save)
3. **Vehicle damage visual** — smoke at <50% HP, fire at <20% (currently only HP bar)
4. **Drift mechanic** — Space+Shift at high speed = handbrake drift
5. **Police roadblock** — at 3+ stars, patrol car parks perpendicular blocking road

## Common mistakes to avoid

- **Player teleports if dt > 0.05** — already capped: `const dt = Math.min(0.05, (now - last) / 1000);`
- **NPC runs INTO player wanted** — wanted reaction makes them RUN TOWARD player if `atan2(n.y, n.x)` is reversed. Triple-check direction.
- **Vehicle stuck in wall** — isSolid radius 20 for vehicles (vs 8 for pedestrian). Don't mix.
- **Police car desync** — police AI re-picks angle every frame to chase player. If player drives in circles, police can oscillate. Solution: smooth the angle delta.

## File layout reference

```
~/Projects/mini-rpg-games/
├── games/
│   ├── index.html          # Landing page (game cards)
│   └── city-drift.html     # THIS GAME (40KB)
├── research/
│   └── gta-v-mini-roadmap.md   # 5-version evolution plan
└── docs/
    └── ROADMAP.md          # Public-facing roadmap
```

## Related references

- `forest-wanderer-architecture.md` — simpler top-down RPG (good starter before City Drift)
- `../../shipping-and-launch/SKILL.md` § Static Site Deployment — GitHub Pages auto-deploy pattern
- `~/Projects/mini-rpg-games/research/gta-v-mini-roadmap.md` — full v1.1-v5.0 plan
