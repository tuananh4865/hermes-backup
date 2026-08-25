# GTA V Mechanics → Single-File 2D Implementation Map

> Distilled from `mini-rpg-games/research/gta-v-mechanics-deep.md` (24 cited sources, 2026-06-22). Maps Grand Theft Auto V systems to concrete 2D top-down canvas implementations. Use when building any GTA-style / open-world / crime / driving game in a single HTML file.

## Why this map exists

GTA V has 8 years of design iteration behind it. When building a "GTA-like" game, the temptation is to copy the surface (3D camera, cinematic cutscenes, 600 vehicles) — but the **engagement** comes from 5 specific systems that map cleanly to 2D. This file tells you which to copy, which to adapt, and which to skip.

## The 5 systems that carry 80% of GTA's engagement

1. **Vehicle physics with weight & drift** — even a 200-line car sim feels "GTA" if it has traction + drift + wall bounce
2. **Wanted level + police escalation** — risk/reward is the dopamine engine
3. **Missions with timers + fail conditions** — gives purpose to free roam
4. **NPC traffic/pedestrians that react** — makes the world feel alive
5. **3-zone input (foot ↔ vehicle ↔ gun)** — each zone has its own feel

Everything else (helicopter physics, property business, stock market, character switching, 8-class weapon wheel) is **diminishing returns**. Skip them unless you have >100KB of code headroom.

## Concrete mechanic → 2D code adaptations

### 1. Character movement (top-down)

| GTA V Mechanic | 2D Adaptation | Code sketch |
|----------------|---------------|-------------|
| Walk / jog / sprint | Speed tiers via input duration | `if (sprintKey && stamina > 0) speed = 200; else speed = 110;` |
| Stamina stat | Decay meter, regen out of combat | `stamina = Math.max(0, stamina - dt * 20); stamina = Math.min(100, stamina + dt * 5);` |
| Health regen to 50% | Auto-regen out of combat, full via food | `if (combatTimer <= 0) hp = Math.min(hp + dt * 5, maxHp * 0.5);` |
| Dodge roll | Dash with i-frames (0.5s) | `if (dodge) { iframes = 0.5; vx = cos(angle) * 400; vy = sin(angle) * 400; }` |
| Stealth takedown | Approach from behind + melee key | `if (dist < 30 && behindAngle < 45°) { npc.dead = true; }` |
| Cover system | Auto-snap to nearest solid tile | `if (coverKey) { snapX = nearestWallTile(player).x; player.x = snapX + coverOffset; }` |
| Melee combos | 3-hit chain with i-frame window | `comboTimer > 0 && nextMelee extends combo` |

### 2. Vehicle physics

| GTA V Mechanic | 2D Adaptation | Code sketch |
|----------------|---------------|-------------|
| Engine force curve | Linear accel with drag | `speed += accel * dt - drag * speed * Math.abs(speed) * dt;` |
| Steering scales with speed | turnRate * (speed / maxSpeed) | `v.angle += steering * 2.2 * (Math.abs(speed) / maxSpeed) * dt;` |
| Reverse = negative turn | Sign of speed | `(v.speed > 0 ? 1 : -1)` |
| Drift (handbrake) | Handbrake key + reduced grip | `if (handbrake) { v.angle += steering * 3.5 * dt; v.speed *= 0.97; }` |
| Wall collision bounce | Reflect velocity, lose 60% | `if (isSolid(newX, v.y, 20)) { v.speed *= -0.4; }` |
| Motorcycle lean | Visual sprite rotation = lean | `lean = steering * Math.min(1, speed/maxSpeed) * 0.5;` |
| Damage (4 multipliers in GTA) | Single `hp` + visual smoke/fire | `if (hp < maxHp*0.5) emitSmoke(); if (hp < maxHp*0.2) emitFire();` |
| Engine cutout at 0 HP | No acceleration | `if (hp <= 0) { accel = 0; }` |

**Vehicle handling parameters (minimum viable set):**
- `maxSpeed` (px/s)
- `accel` (px/s²)
- `brake` (px/s²)
- `drag` (coefficient)
- `turnRate` (rad/s at full speed)
- `hp` (collision capacity)

### 3. Wanted system (5 sao)

| Star | Police Response | Spawn Rate | Speed |
|------|-----------------|------------|-------|
| ★ | Patrol cars, 1-2 units | One-time, 5s delay | 250 km/h |
| ★★ | Patrol + roadblock attempt | 5s | 260 km/h |
| ★★★ | + Police Maverick helicopter | 5s | 270 km/h |
| ★★★★ | NOOSE tactical (4-door pursuit cars) | 5s | 285 km/h |
| ★★★★★ | + FBI Granger + spike strips | 3s | 300 km/h |

**Evasion mechanic** (most authentic to GTA):
- Each cop has cone of vision (forward arc, ~90°)
- If player out of all cones for X seconds → wanted drops
- **Evasion times** (GTA V actual, scale to game): ★=30s, ★★=45s, ★★★=60s, ★★★★=75s, ★★★★★=90s
- In top-down 2D: vision cone = dot product check (targetVec · forwardVec > 0)
- Lose wanted = leave all cop cones for full evasion time

**Decay rate:** 8 seconds per star when not in line of sight (gives "tension" without being punishing).

### 4. NPC AI patterns

| GTA V NPC Behavior | 2D Implementation |
|--------------------|-------------------|
| Wander (random walk) | Pick new angle every 2-3s, move 25-40 px/s |
| React to player wanted | If wanted >= 1, run from player (angle = away from player) |
| Daily schedule | Switch archetype by gameTime: worker→office, student→school, retiree→park, criminal→hideout |
| Road rage | If hit by player vehicle, exit vehicle, chase player 5s, attack |
| Run from gunfire | If hearing gunshots within 200px, run in random direction |
| Ambient dialogue | One of 3-5 voice lines per district, triggered on proximity |

**Pedestrian types (4 archetypes, 25 total NPCs per district):**
- **Worker** (suit, briefcase): walks briskly, deterministic path
- **Student** (backpack, casual): wanders, group with other students
- **Retiree** (slow, hat): slow wander, sits on benches
- **Criminal** (hoodie, hides face): flees when seen by police, attacks when cornered

### 5. Mission design

| GTA V Mission Type | 2D Implementation | Failure Conditions |
|--------------------|-------------------|--------------------|
| **Taxi/transport** | Pickup NPC → drive to marker | Timer (60s), NPC dies |
| **Delivery** | Pickup package → deliver to marker | Timer, package lost on death |
| **Eliminate** | Kill X targets | Time limit, civilian kills > 5 |
| **Race** | Checkpoint time trial | Time limit, missed checkpoint |
| **Chase** | Catch fleeing target | Distance threshold, time limit |
| **Escort** | Protect NPC following you | NPC dies, distance > 100px |
| **Heist setup** | Multi-stage mission chain | Any stage fail = restart chain |

**Mission structure formula (works in 2D):**
```js
mission = {
  title: "...",
  stages: [
    { name: "intro", type: "dialogue", duration: 3000 },
    { name: "drive", type: "go_to", target: {...}, timer: 60 },
    { name: "action", type: "eliminate", count: 5, timer: 90 },
    { name: "exit", type: "go_to", target: {...}, timer: 60 }
  ],
  reward: { money: 500, xp: 100 }
}
```

**Reward scaling** (based on GTA V):
- Easy mission: $100-$500, 30-60s
- Medium: $500-$2K, 2-5 min
- Hard: $2K-$10K, 5-10 min
- Heist finale: $10K-$50K, 10-20 min

## Visual juice patterns (10x feel upgrade)

These are NOT new features — they're micro-polish that makes the existing game feel "GTA":

1. **Hit flash** — blink entity white for 0.2s when damaged
   ```js
   if (hitFlash > 0 && Math.floor(hitFlash * 20) % 2 === 0) return; // skip render
   ```

2. **Screen shake on big hits** — `camera.x += (Math.random() - 0.5) * shakeIntensity`

3. **Speed lines at high speed** — render translucent white streaks when `speed > 200`

4. **Smoke trail from damaged vehicle** — emit particles when `hp < 50%`

5. **Knockback on hit** — `target.vx = (target.x - attacker.x) * 5; target.vy = (target.y - attacker.y) * 5;`

6. **Bullet time on player damage** — `dt *= 0.3` for 0.5s when player takes damage

7. **Money popup** — `+500$` text floats up from pickup point, fades over 1s

8. **Wanted star pop-in** — when wanted goes up, briefly scale stars 1.5x then settle

9. **Death camera** — on player death, slow zoom out + red filter + "WASTED" text

10. **Slow-mo on last kill** — during final enemy of mission, `dt *= 0.5` for cinematic effect

## Audio (Web Audio API, no assets)

GTA V has licensed radio. We can't (no licensing). But we can SYNTHESIZE:

```js
// Engine sound — pitch tracks speed
function updateEngine(v) {
  engineOsc.frequency.value = 80 + Math.abs(v.speed) * 0.4;  // 80Hz idle → ~280Hz top
  engineGain.gain.value = 0.05 + Math.abs(v.speed) * 0.0003; // louder when accelerating
}

// Gun shot — noise burst with decay
function playShot() {
  const noise = audioCtx.createBufferSource();
  // fill buffer with white noise...
  const gain = audioCtx.createGain();
  gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
  noise.connect(gain).connect(audioCtx.destination);
  noise.start();
}

// Crash — filtered noise impulse
function playCrash(impactSpeed) {
  // ...similar, with bandpass filter at 200Hz, gain scaled to impactSpeed
}
```

**3-4 radio stations** can be synthesized by:
- Layer 3 oscillators at root + fifth + octave (chord pad)
- Slow LFO modulation on filter cutoff (gives "swooshy" feel)
- Different tempo/chord per station (pop = fast major, jazz = slow 7th, lo-fi = slow minor, news = speech formant)

## Project evolution pattern (from City Drift session)

This is the proven progression from "GTA-lite" to "GTA V-lite" in 6-9 months:

| Version | Theme | Code Size | Build Time |
|---------|-------|-----------|------------|
| v1.0 | Prototype: 4 vehicles, 3 missions, wanted, combat | 40KB | 3h |
| v1.1 | Polish: audio, save, damage, drift, roadblock | 55KB | 1w |
| v1.2 | Day/night + weather | 65KB | 2w |
| v2.0 | Traffic AI + 5 districts (80×80 tiles) | 90KB | 6w |
| v2.5 | Cover + combos + abilities | 110KB | 8w |
| v3.0 | Survival (hunger/thirst/energy) + economy | 140KB | 12w |
| v4.0 | Story + heist (1 finale, 2 approaches) | 180KB | 18w |
| v5.0 | WebRTC P2P + PWA | 220KB | 24w |

**Cumulative game length:** 5 min → 15 min → 20 min → 1h → 2h → 4h → 8-12h → infinite

## What GTA V has that we SKIP (out of scope)

| Skip | Why |
|------|-----|
| Helicopter/plane physics | 3D flight sim, needs 6-DOF model, way too complex for 1 file |
| Boat buoyancy simulation | 2D top-down, water is decorative at best |
| 8-class weapon wheel | 3-4 weapons is enough for engagement loop |
| 600+ vehicles | We have 4-8. Variety comes from handling, not count |
| Stock market | Mini-game, not core to open-world feel |
| Property business management | Backend-style state, doesn't fit single-file |
| 69 story missions | 5-10 max, story is flavor not main loop |
| Multi-protagonist story | Single character, simpler narrative |
| Real water physics | Decorative water tiles only |
| Swimming/climbing | Top-down, no need |
| Character customization | Add in v3.0+ if scope allows |

## Sources (24 references)

From `gta-v-mechanics-deep.md` (mini-rpg-games repo):
- GTA Wiki — Skills in GTA V, Wanted Level, Weapons, Cover System
- Game Informer — Running and Gunning
- IGN — Increasing Stats
- GTAMods Wiki — handling.meta spec
- Gamepressure, GTA Intel, GTABoom, 1v9, Grand Theft Wiki

## When to use this file

- Starting any new GTA-style game → read this FIRST to scope
- Reviewing existing GTA-lite game → cross-check against this map
- User asks "make my game more like GTA" → identify which 5 systems are missing
- Stuck on implementation → look up the specific subsystem table
