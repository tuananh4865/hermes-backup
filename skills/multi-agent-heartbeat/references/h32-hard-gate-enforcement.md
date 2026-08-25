# H32 HARD GATE Enforcement — STEADY-STATE IDLE Compression Failure (2026-06-26)

> **The 12-sweep post-mortem that motivated the HARD GATE.** From H21 (2026-06-24 16:01) through H32 (2026-06-26 14:32), the multi-agent heartbeat skill was loaded on every sweep, the soft "compress to ≤200 bytes" rule was clearly stated, AND the agent wrote verbose 3-13 KB rows every time. The HARD GATE exists because the soft rule failed.

## What happened

| Sweep | Date/time | Row size (approx) | Mode | Compliance |
|---|---|---|---|---|
| H20 | 2026-06-24 ~15:00 | ~3.5 KB | NORMAL (boundary set) | ✅ Rule definition |
| H21 | 2026-06-24 16:01 | ~3.6 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose |
| H22 | 2026-06-26 06:00 | ~3.5 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose |
| H23 | 2026-06-26 13:00 | ~3.5 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose (H23 self-check rule added) |
| H24-H27 | 2026-06-26 | ~3-5 KB each | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose |
| H28 | 2026-06-26 12:00 | ~3.5 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose |
| H29 | 2026-06-26 13:00 | ~5 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose |
| H30 | 2026-06-26 14:01 | ~3.5 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose (orchestrator 30m) |
| H31 | 2026-06-26 14:02 | ~5 KB | SHOULD-BE STEADY_STATE_IDLE | ❌ Verbose |
| **H32** | **2026-06-26 14:32** | **~13.7 KB** | SHOULD-BE STEADY_STATE_IDLE | ❌❌❌ **4× the prior baseline** |

**Cumulative damage:** ~50-60 KB of file bloat across H21-H32 that should have been ~2 KB (one compressed row). The `qa-agent/state.md` file is now 90+ KB when it should be ~30-40 KB.

## Why the soft rule failed

The skill said "should compress" + "marker file's existence is the single source of truth for mode". The LLM's default behavior is to produce verbose output that mirrors prior rows. Without an enforcement mechanism, "should" gets ignored because:

1. **No physical constraint on row size** — the patch tool accepts any size
2. **No auto-check of marker file existence before writing** — the rule depends on agent remembering
3. **Verbose rows copy-paste from prior rows** — the LLM's default pattern is "expand on prior context", not "compress"
4. **No post-write verification** — once written, no mechanism catches the violation

## The HARD GATE fix (encoded in SKILL.md)

Three structural changes:

1. **Decision matrix (mode auto-determined by state, not by agent choice):**
   - 20+ idle sweeps + no new signal = **STEADY_STATE_IDLE — COMPRESS** (≤200 bytes)
   - 20+ idle sweeps + new signal = NORMAL with new-signal emphasis
   - <20 idle sweeps = NORMAL

2. **Marker file write IS the entry trigger** — bash condition auto-writes the marker on first transition into STEADY_STATE_IDLE. Agent doesn't have to remember to write it.

3. **Post-write size check** — after patching the row, immediately check row byte size. If > 500 bytes in STEADY_STATE_IDLE, the rule was violated → compress in-place.

## What the agent should do differently on next heartbeat

When the cron prompt matches the heartbeat trigger and the agent loads this skill:

1. **First action:** compute idle sweep count and check for new signals
2. **Auto-determine mode** per the decision matrix
3. **If STEADY_STATE_IDLE:** write the marker file (or update its mtime), then write a ≤200 byte row
4. **If NORMAL:** write the full row, but only after explicitly checking "do I have a new signal that the prior row didn't?"
5. **Post-write:** verify row size matches mode

The HARD GATE removes the "should compress" ambiguity. The agent CAN'T write a verbose row in STEADY_STATE_IDLE without explicitly bypassing the gate (which is itself a visible signal that the gate wasn't followed).

## Future failure modes to watch for

- **HARD GATE bypass via marker deletion:** agent deletes `.steady-state-idle` to "justify" writing a verbose row. Symptom: marker file disappears, file grows. Fix: log "marker deleted, re-entering NORMAL mode" in the new row.
- **HARD GATE bypass via "new signal" justification:** agent invents a fake "new signal" to justify NORMAL mode. Symptom: row says "new signal: ops-manager frontmatter clock-anomaly" when this has been ongoing for 7+ sweeps. Fix: NEW-SIGNAL checklist requires the signal to be <2h old AND not previously recorded.
- **HARD GATE bypass via compressed-but-still-verbose rows:** agent writes 199-byte rows that are still semantically verbose ("0 stuck. 0 pending. 0 conflicts. CRON FAULT H28 H29 H34 PERSISTING. ops-manager recovering. security within tolerance. code-reviewer persistent."). Fix: post-write check should also verify semantically — no repeated multi-sentence content.

## Cross-references

- SKILL.md §"MANDATORY pre-write self-check (the "no-verbose-loop" rule, H23) + HARD GATE (H32, 2026-06-26)" — the rule itself
- `references/h26-silent-kill-mode.md` — the H26 failure that motivated this; HARD GATE is the structural fix
- `references/h26-reoccurrence-2026-06-24-2001.md` — the first re-occurrence proof that soft rules aren't enough
- `references/idle-escalation-recipe.md` — what STEADY-STATE IDLE actually looks like in practice
