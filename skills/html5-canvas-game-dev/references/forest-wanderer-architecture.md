# Forest Wanderer — Top-Down RPG Reference Architecture

> **Source:** `~/Desktop/forest-wanderer.html` (early prototype, 27KB, single file)
> **Status:** v1.0.0 prototype — REMOVED from mini-rpg-games repo on 2026-06-22 in favor of GTA V Mini
> **Verdict:** Approved by Tuấn Anh as a "good starter" template before City Drift

The reference for the **simpler side** of the html5-canvas-game-dev family: top-down pixel RPG, 4-direction movement, NPC dialogue, melee combat, slime AI. No vehicles, no wanted system — just slash + explore.

## When to use this pattern (not City Drift)

Use Forest Wanderer patterns when:
- Game is **exploration + combat** (no driving)
- Map is **< 50×50 tiles** (don't need minimap)
- NPCs have **dialogue trees** (text-based, not interactive)
- Combat is **melee-only** or simple ranged (no cover system)

If you need vehicles, wanted level, or missions → use `city-drift-architecture.md` instead.

## Full architecture

### Pattern 1: Procedural forest generation (40×30 tiles)

```js
function generateWorld() {
  for (let y = 0; y < WORLD_H; y++) {
    world[y] = [];
    for (let x = 0; x < WORLD_W; x++) {
      let t = 0;
      // Border trees (immersion boundary)
      if (x === 0 || x === WORLD_W-1 || y === 0 || y === WORLD_H-1) t = 1;
      // Sparse random trees
      else if (Math.random() < 0.08) t = 1;
      // Flowers for visual variety
      else if (Math.random() < 0.03) t = 5;
      world[y][x] = t;
    }
  }
  // Carve a path for player to follow
  for (let x = 5; x < 35; x++) world[15][x] = 3;
  for (let y = 15; y < 25; y++) world[y][20] = 3;
  // Lake as natural obstacle
  for (let y = 5; y < 10; y++)
    for (let x = 28; x < 35; x++)
      world[y][x] = 2;
}
```

**Key insight:** Border trees (always 1) hide the world edge. Sparse random (8% density) feels natural. Path carving gives player implicit direction.

### Pattern 2: 4-direction movement + dash

```js
let dx = 0, dy = 0;
if (keys['w'] || keys['arrowup']) dy -= 1;
if (keys['s'] || keys['arrowdown']) dy += 1;
if (keys['a'] || keys['arrowleft']) dx -= 1;
if (keys['d'] || keys['arrowright']) dx += 1;

// Dash (shift held while moving)
const dashing = keys['shift'] && player.dashCooldown <= 0 && (dx !== 0 || dy !== 0);
const speedMul = dashing ? 2.2 : 1;
if (dashing) player.dashCooldown = 1.2;

if (dx !== 0 || dy !== 0) {
  const len = Math.sqrt(dx*dx + dy*dy);
  dx /= len; dy /= len;
  // Direction for animation/aiming
  if (Math.abs(dx) > Math.abs(dy)) player.dir = dx > 0 ? 'right' : 'left';
  else player.dir = dy > 0 ? 'down' : 'up';
}

// Axis-separated collision
const moveSpeed = player.speed * speedMul * dt;
const newX = player.x + dx * moveSpeed;
if (!isBlocked(newX, player.y)) player.x = newX;
const newY = player.y + dy * moveSpeed;
if (!isBlocked(player.x, newY)) player.y = newY;
```

**Why dash feels good:** 2.2× speed + 1.2s cooldown = use sparingly, high impact. Animation frame rate doubles during dash for extra juice.

### Pattern 3: Slime AI (chase + wander with timer)

```js
e.dirTimer -= dt;
if (e.dirTimer <= 0) {
  e.dirTimer = 1 + Math.random() * 1.5;
  const d = distance(e, player);
  if (d < 200) {
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

**Distance threshold (200px)** is the magic number — switch between aggressive vs passive creates rhythm. Too close (50px) = always chase = overwhelming. Too far (500px) = never chase = boring.

### Pattern 4: NPC dialogue system

```js
const npcs = [
  { id: 'npc1', x: ..., y: ..., name: 'Cô Bán Hoa',
    dialogue: ['Chào mừng con vợ!', 'Tui bán hoa tươi nè.', 'Mua 5 bó tặng 1 bó!'] },
  // ...
];

// In update loop
for (const npc of npcs) {
  const d = distance(player, npc);
  if (d < 36) {  // interaction radius
    if (consume('e') || consume(' ')) {
      startDialogue(npc.name, npc.dialogue);
    }
  }
}

function startDialogue(speaker, lines) {
  dialogQueue = lines.slice();
  currentDialog = { speaker, index: 0 };
  document.getElementById('dialog').style.display = 'block';
  document.getElementById('dlg-speaker').textContent = speaker;
  document.getElementById('dlg-text').textContent = lines[0];
}
```

**Dialogue tips:**
- 3 lines per NPC is the sweet spot (intro + info + call-to-action)
- Space = advance, Esc = close
- Queue system (rather than single line) lets you write multi-step conversations

### Pattern 5: XP curve + level-up

```js
player.exp += 5;
if (player.exp >= player.lv * 20) {
  player.lv++;
  player.exp = 0;
  player.maxHp += 10;
  player.hp = player.maxHp;  // Full heal on level up = positive feedback
  showToast(`⬆ Lv ${player.lv}! HP tăng!`, 2);
}
```

**Why `lv * 20`:** Exponential growth (Lv1: 20xp, Lv2: 40xp, Lv3: 60xp). Player feels progression slow down, motivating exploration. The full-heal on level up is HUGE dopamine — keep this pattern.

### Pattern 6: Hit-flash + invuln frames

```js
if (d < 22 && player.invuln <= 0) {
  player.hp -= e.atk;
  player.invuln = 0.8;  // 0.8s i-frames
  player.hitFlash = 0.3;  // visual feedback
  // Knockback
  const ang = Math.atan2(player.y - e.y, player.x - e.x);
  player.x += Math.cos(ang) * 30;
  player.y += Math.sin(ang) * 30;
}

// In render
if (player.invuln > 0 && Math.floor(player.invuln * 10) % 2 === 0) return;
// = player "blinks" out for 5 frames per 0.1s
```

**Why blink invuln:** The blink makes i-frames OBVIOUS to player. Without it, player feels like they took damage twice (bug-like). With it, they understand "I just got hit, can't be hit again yet."

### Pattern 7: Building interaction (mock interior)

```js
for (const b of buildings) {
  if (player.x > b.x*TILE && player.x < (b.x+b.w)*TILE &&
      player.y > b.y*TILE && player.y < (b.y+b.h)*TILE) {
    if (!b._entered) {
      b._entered = true;
      showToast('🛒 SHOP — Bán đồ (coming soon)', 1.5);
    }
  } else {
    b._entered = false;  // reset on exit
  }
}
```

**Why this is smart:** The "coming soon" pattern lets you add building types WITHOUT coding interiors yet. Each building is just a tile region that triggers a toast. Add real interiors later (v2.0).

## Line count breakdown (1268-line file)

| Section | Lines | Notes |
|---------|-------|-------|
| CSS | 1-100 | HUD + dialog + title screen |
| Input handlers | 175-185 | keys{}, justPressed{}, consume() |
| World generation | 195-243 | generateWorld() + createBuilding() |
| Player + entities | 245-330 | player, npcs, enemies, pickups |
| Update loop | 526-863 | Movement, AI, combat, missions |
| Render loop | 872-1100 | drawTile, drawPlayer, drawNPC, drawEnemy |
| Minimap + HUD | 1100-1260 | Real-time overlays |

## Common pitfalls (and fixes)

| Pitfall | Fix |
|---------|-----|
| Player gets stuck in corner when walking diagonally | Axis-separated collision (see Pattern 2) |
| NPC walks into wall | Same `isBlocked` check, smaller radius (6-8px) |
| Attack misses because enemy moved | Use fixed-radius hit detection (range 28px) not tracking |
| Level up feels unrewarding | Full heal on level up (Pattern 5) |
| Death with no respawn | Auto-respawn at start with 50% gold loss |

## Reuse for new game in this class

1. Copy `forest-wanderer.html` → rename to `your-game.html`
2. Replace `generateWorld()` with your terrain algorithm
3. Replace NPC + enemy arrays with your cast
4. Adjust player stats (speed, hp, atk range)
5. Add new patterns as needed (NO need to remove old)
6. Commit + push to `games/` folder

The structure scales: 27KB → 50KB → 100KB without architectural changes.

## Why this game was retired

Anh decided to focus on GTA V Mini (City Drift evolution) on 2026-06-22. The patterns are preserved here as reference for simpler top-down RPGs. If Anh wants a non-vehicle top-down game in the future, this is the template to start from.
