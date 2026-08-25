---
sweep: H40
date: 2026-06-26 22:00 +07:00
trigger: qa-agent hourly gate
---

# H40 Evidence — Sibling-Collision Overwrite Bug (CRITICAL)

## What happened

The H40 qa-agent hourly sweep (2026-06-26 22:00:44 +07:00) **overwrote** the orchestrator 30m heartbeat's H40 row at 21:30 instead of renumbering to H41. This is a regression of the H31 sibling-collision recipe — the recipe was followed at H31/H33 but **missed at H40**.

## Timeline

| Time | Event |
|---|---|
| 22:00:00 | qa-agent hourly cron fires (cron `QA Agent Quality Gate`) |
| 22:00:01 | qa-agent reads state.md → sees H39 as latest (expected H40) |
| 22:00:05 | qa-agent runs profile reads (8 profiles in parallel via execute_code) |
| 22:00:10 | qa-agent runs `hermes cron list` → 18 crons all healthy |
| ~21:30 (in parallel, before H40 patch) | **Orchestrator 30m heartbeat writes H40 row at 21:30** to state.md |
| 22:01:30 | qa-agent patches state.md using H39-tail anchor → overwrites orchestrator's H40 row |

## Root cause

The H31 sibling-collision recipe says: "Before patching, count current rows... If `actual_count > expected`, a parallel cron sweep wrote a row between your dispatch and your read."

**The bug**: I ran the row-count check **at sweep start** (count = 39 rows, H39 latest, expected = H40). I did NOT re-run the check **immediately before the patch**. By the time I patched ~1.5 minutes later, the orchestrator had already written H40 in the gap.

The orchestrator's H40 row was overwritten with my own H40 row, which had different content (orchestrator's was an "all clear" heartbeat summary; mine was the full H38 cron-truth sweep with research-lead reactivation observation).

## Why this matters

- Silent data loss of the orchestrator's audit record at 21:30
- H40 lost its dual perspective (orchestrator heartbeat + qa-agent hourly)
- The H33 worked example was followed correctly there but missed at H40 — indicates the recipe needs stronger emphasis on **timing**, not just logic

## H31 vs H40 deviation

| Aspect | H31 (correct) | H33 (correct) | H40 (BUG) |
|---|---|---|---|
| Pre-append row count check | Done at sweep start | Done at sweep start | Done at sweep start |
| Pre-patch row count re-check | **Done** | **Done** | **Not done** |
| Sibling row detected | No | Yes (H32 sibling) | Yes (H40 sibling at 21:30) |
| Action taken | N/A | Renumbered to H33 | **Overwrote** sibling row |

## Correct procedure (now codified in SKILL.md)

The H40 patch to `quality-checker/SKILL.md` adds a sub-section under the H31 sibling-collision detection bullet:

> ⚠️ H40 SIBLING-COLLISION OVERWRITE BUG (CRITICAL — 2026-06-26 22:00): The H31 recipe's row-count check must be run IMMEDIATELY BEFORE THE PATCH — not at sweep start. At H40, I read state.md at sweep start (saw H39 = expected H40), then spent ~5 minutes running profile reads + cron list. The orchestrator 30m heartbeat cron wrote H40 at 21:30 during that gap. When I patched with the H39-tail anchor, I overwrote the orchestrator's H40 row instead of renumbering to H41.
>
> Correct procedure (mandatory):
> - Run `grep -cE "^\|{1,2} H[0-9]+ \|" state.md` **right before constructing the patch**, not just at sweep start.
> - If a sibling row appeared since sweep start, **renumber YOUR sweep to the next available integer** (H41 in this case), re-anchor on the actual highest `H<N>` row's tail.
> - Default behavior on detected collision: **RENUMBER UP, NEVER OVERWRITE**. Even if your content is "better" than the sibling's, the sibling got there first and their row deserves to stay.
> - Token cost of renumbering: zero. Token cost of overwriting: silent data loss of sibling's audit record.

## Mitigation for future sweeps

1. **Always run `grep -cE "^\|{1,2} H[0-9]+ \|" state.md` immediately before patch** (not just at sweep start).
2. **If sibling row appeared since sweep start** → renumber to H<N+1> + re-anchor on actual tail.
3. **Default to renumber-up, never overwrite.**
4. The 1.5-minute window between "sweep start read" and "patch" is exactly the orchestrator 30m heartbeat cadence. Any sweep that takes >30 minutes has a non-zero probability of overlapping with a heartbeat.

## Forecast for H41

H41 should:
- Run the row-count check immediately before patch (not at sweep start).
- If sibling row appeared (e.g., another orchestrator 30m heartbeat), renumber to H42.
- Verify the orchestrator's H40 row was actually overwritten (it should be missing — log the data loss in H41's notes column).
- Apply the H40 fix retroactively if possible (append a "H40-SIBLING-OVERWRITE-NOTICE" row noting the data loss for audit trail).

## Lessons learned

- The H31/H33 sibling-collision recipe is correct in principle but **requires explicit timing guidance** (when to run the check, not just how).
- Reading state.md at sweep start and patching at sweep end with no intermediate re-check creates a race window during which any concurrent cron writer can introduce a sibling row.
- The orchestrator 30m heartbeat cadence (every 30 minutes from 08:00-22:00) means **any sweep taking >30 minutes is guaranteed to overlap** with a sibling write. Token-economized sweeps (4 reads vs 8 reads) help reduce this window.
- **Always count rows twice**: once at sweep start (sanity), once immediately before patch (correctness).

## Related

- `references/idle-sweep-evidence-h31.md` — First sibling-collision detection (H30 vs H31)
- `references/idle-sweep-evidence-h33.md` — Worked example of renumber-upward (H32 vs H33)
- SKILL.md § "Mode B sweep row insertion recipe" → step 7 → "H40 SIBLING-COLLISION OVERWRITE BUG"