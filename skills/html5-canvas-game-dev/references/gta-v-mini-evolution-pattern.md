---
title: GTA V Mini Evolution Pattern — single-file → open world RPG
created: 2026-06-23
type: case-study
tags: [gta, open-world, evolution, research-driven, roadmap]
applies_to: html5-canvas-game-dev
---

# GTA V Mini — Evolution Pattern (verified 22-23/06)

> How a 40KB single-file prototype evolved into a research-backed 7-version roadmap for a full GTA V-lite open world RPG. Total trajectory: 40KB → 220KB over 6-9 months.

## The pattern (3 phases)

### Phase 1 — Prototype (v1.0, 40KB, 3 hours)

**Shipped:** `city-drift.html` with:
- 4 vehicles (Sedan, Sports, Truck, Motor)
- 5-star wanted system + police AI chase
- 3 mission types (taxi, delivery, chase)
- 25 NPCs + 40 parked cars
- Top-down shooting + melee
- Minimap with player/vehicles/police

**Method:** Build first, ask questions later. Tối ưu polish trên từng mechanic trước khi mở rộng.

### Phase 2 — Deep research (1 day)

**Trigger:** User said "loại bỏ game khác, tập trung nghiên cứu và lên plan chi tiết để phát triển GTA V Mini".

**Method:** Dispatch 3 parallel research subagents covering 15 topics across 3 domains:
- **Subagent 1:** Gameplay mechanics (movement, vehicle physics, combat, wanted, missions)
- **Subagent 2:** World building (open world, NPC AI, traffic, day/night, economy)
- **Subagent 3:** UX & audio (HUD, audio, interaction, minigames, multiplayer)

**Output:** ~16KB synthesis document with 24 sources cited (GTA Wiki, Game Informer, IGN, GTAMods, etc.), concrete numbers (DPS values, evasion times 30s-90s, heist payouts $41.7M), formulas (G-force traction, slip-angle curve).

### Phase 3 — 7-version roadmap (synthesized same day)

**Critical decision:** Which GTA V features to REPLICATE vs SKIP for 1-file HTML scope.

**Decision matrix (from session 22/06):**

| GTA V Mechanic | Replicate? | Why |
|----------------|-----------|-----|
| Stamina, lung capacity | ✅ Yes | Simple meter, big feel |
| Cover system | ✅ Yes | Auto-snap to wall edge |
| Melee combos | ✅ Yes | 3-hit chain, low complexity |
| Dodge roll | ✅ Yes | Dash + i-frames |
| Weapon wheel (8 classes) | ❌ Simplify → 3-4 | Scope creep |
| Helicopter/plane physics | ❌ Skip | 3D flight too complex |
| Boat buoyancy | ❌ Skip | Same |
| 600+ vehicles | ❌ Skip → 4-8 | Already have 4 |
| Stock market | ❌ Skip | Out of scope |
| Property business mgmt | ❌ Skip | Same |
| 69 story missions | ❌ Skip → 5-10 | Scope |
| Multi-protagonist | ❌ Skip → 1 char | Scope |
| Real water physics | ❌ Skip | Same |

**7-version roadmap:**
- v1.0 ✅ (40KB) — Foundation
- v1.1 (55KB, 1-2 weeks) — Polish & juice (audio, save, damage, drift)
- v1.2 (65KB, 1 week) — Day/night + weather
- v2.0 (90KB, 3-4 weeks) — AI + 5 districts
- v2.5 (110KB, 2 weeks) — Combat depth (cover, combos, abilities)
- v3.0 (140KB, 3-4 weeks) — Survival + economy
- v4.0 (180KB, 4-6 weeks) — Story + heists
- v5.0 (220KB, 4-6 weeks) — Multiplayer + PWA

## Lessons learned

### 1. Build prototype FIRST, research SECOND

Don't research for 3 days before writing any code. Ship a 40KB prototype in 3 hours → play it → identify what's missing → THEN research what to add.

### 2. Use parallel subagents for deep research

3 subagents in parallel = ~3 minutes wall time, vs ~9 minutes sequential. Each subagent got 5 specific topics, returned ~2500 words synthesized. Parent agent integrated results.

### 3. Concrete numbers > vague ideas

Research returned specific values: stamina scales 1% per 18 yards, pistol DPS 70, evasion 30s-90s per star. These become concrete plan items like "Audio: oscillator.frequency = 80 + 200*speed_ratio" not "add audio".

### 4. "Implementation mapping" is the bridge

For every GTA V feature, decide: replicate, simplify, or skip. This prevents scope creep while preserving the most impactful mechanics.

### 5. Working backward from total budget

If final v5.0 = 220KB, plan each version's size budget: v1.1 +15KB, v1.2 +10KB, etc. Don't ship v2.0 at +50KB if budget only allows +25KB.

### 6. Polish phase is non-negotiable

Anh's mandate: "điều khiển và tương tác phải được trau chuốt kĩ trước". This means v1.1 = pure polish (no new content), not "v1.1 adds 5 new features". Order matters.

## Files in this case study

- **Repo:** https://github.com/tuananh4865/mini-rpg-games
- **Live prototype:** https://tuananh4865.github.io/mini-rpg-games/games/city-drift.html
- **Research synthesis:** `research/gta-v-mechanics-deep.md` (16KB, 24 sources)
- **Roadmap:** `docs/ROADMAP.md` (10KB, 7 versions with concrete tasks)
- **Wiki project hub:** `wiki/projects/mini-rpg-games/` (proper folder structure)

## When to apply this pattern

- User wants to build a "GTA-style" / "open world" / "sandbox" game
- User has a working prototype and wants to scale it up
- User wants a "real" game, not a 1-hour jam entry
- User is willing to commit 6-9 months of incremental work

## When NOT to apply

- User wants a 1-shot prototype (just use the prototype skill)
- User wants a different genre (platformer, puzzle, etc.) — use the basic skill patterns
- User has no interest in single-file constraint (suggest they use a real engine)

## Related

- `references/gta-v-mechanics-implementation.md` — 2D adaptation map (50+ concrete code patterns)
- `references/city-drift-architecture.md` — v1.0 prototype architecture
- `hermes-project-workflow-system` — The workflow used to manage this project
- `project-init-resume-workflow` — 4-step setup that was applied retroactively
