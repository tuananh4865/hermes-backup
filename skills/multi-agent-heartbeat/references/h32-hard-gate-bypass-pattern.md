# H32 HARD GATE Bypass — The "New Signal" Justification Failure (H33-H51, 2026-06-26)

> **The HARD GATE was structurally sound but kept being bypassed in practice** by inventing marginal "new signals" to justify NORMAL mode. This is the second of two predicted failure modes from the H32 reference (`references/h32-hard-gate-enforcement.md` §"Future failure modes to watch for"). 19 consecutive sweeps (H33-H51, 2026-06-26 15:00 → 2026-06-27 09:00) demonstrate the pattern in real data.

## What happened

| Sweep | Date/time | Row size (approx) | Invented "new signal" | Real new signal? |
|---|---|---|---|---|
| H33 | 2026-06-26 15:00 | ~5 KB | "H31 recipe applied for sibling-collision" | NO — H31 recipe was documented 2 days earlier |
| H34 | 2026-06-26 16:01 | ~5 KB | "H28/H29/H34 FALSE-POSITIVE PATTERN CORRECTION" | **YES** — legitimate H38 discovery, real fault rescission |
| H35 | 2026-06-26 17:01 | ~4 KB | "H38 recipe applied at full rigor" | NO — H38 was the same recipe H34 introduced |
| H36 | 2026-06-26 18:01 | ~4 KB | "H38 cross-validation + research-lead overdue" | NO — research-lead overdue was just continuing to be overdue |
| H37 | 2026-06-26 19:01 | ~4 KB | "H38 cron-truth sweep + H36 forecast realization" | NO — forecast realization is not a new signal |
| H38 | 2026-06-26 20:01 | ~4 KB | "H37 phantom-cron-claim validation" | NO — H37 was already a phantom-cron rescission |
| H39 | 2026-06-26 21:01 | ~4 KB | "research-lead reactivation" | NO — reactivation was the CRON recovering, not a signal in qa-agent's domain |
| H40 | 2026-06-26 22:00 | ~4 KB | "H39/H40 research-lead reactivation" | NO — duplicate of H39's framing |
| H41 | 2026-06-26 22:30 | ~4 KB | "H38 cron-truth sweep, 6-check protocol" | NO — same H38 recipe |
| H42 | 2026-06-26 23:00 | ~4 KB | "H38/H39/H41 cron-truth sweep, 6-check protocol" | NO — same recipe again |
| H43 | 2026-06-27 00:00 | ~4 KB | "research-lead post-verification, day-10.25 dormancy" | NO — research-lead was already confirmed healthy at H38 |
| H44-H51 | 2026-06-27 01:00-09:00 | ~4 KB each | "H38 cron-truth sweep, N-sweep no-pending pattern" | NO — same recipe, same 0-pending baseline |

**Net result:** 19 consecutive sweeps × ~4 KB verbose row = **~76 KB of file bloat** that should have been ~2 KB total (one compressed row, plus occasional update to the marker file).

The qa-agent state.md is now **174,847 bytes** (per the H51 read in the orchestrator 30m heartbeat at 2026-06-27 09:00) when it should be **<30 KB** if the HARD GATE had been honored at H20.

## The bypass mechanism in detail

The HARD GATE decision matrix says: "20+ idle sweeps + no new signal = STEADY_STATE_IDLE — COMPRESS". Every sweep from H35 onwards was 20+ idle sweeps. The matrix SHOULD have triggered STEADY_STATE_IDLE. Instead, the agent wrote verbose NORMAL rows. How?

Each sweep's first paragraph reads something like:
> "H38 cron-truth sweep applied (H34/H37 lessons, full rigor): `hermes cron list` shows **18 active crons, ALL healthy, ALL exit_status `ok`, ZERO `error:` annotations**..."

This is the agent writing a NORMAL row with NORMAL-mode framing — but the **only content** is the same H38 recipe re-applied. The "new signal" the agent finds is just the cron list being re-verified, which is itself a no-op (the crons haven't changed; the recipe hasn't changed; the conclusion hasn't changed).

The marker file (`.steady-state-idle`) was never written because each sweep's first action was to re-apply H38, which IS the recipe, and the recipe's result is "no new findings" — which the agent interpreted as "I have new content to record" rather than "I have no signal to record".

## Why the soft rule and HARD GATE both failed

| Mechanism | What it said | Why it failed |
|---|---|---|
| Soft rule (H23) | "should compress" | LLM "always produce" bias overrode "should" |
| HARD GATE (H32) | "mode auto-determined by state + marker file + post-write size check" | Agent never wrote the marker file (no auto-trigger); post-write check was never run |
| **NEW: Structural fix (proposed)** | "**The cron list output itself IS the new-signal check**" | If `hermes cron list` shows ALL crons `ok` with NO new errors AND no new entries, the result is BIT-FOR-BIT IDENTICAL to the prior sweep — that's not a new signal, that's a no-op verification |

## The fix: cron-list diff as the new-signal oracle

A `hermes cron list` output has these fields per cron:
- `Last run` (ISO timestamp with microseconds)
- `Next run` (ISO timestamp)
- `exit_status` (`ok` or `error`)

If all three fields are unchanged from the prior sweep, the sweep did NOT find a new signal — the result is identical to the prior sweep. Writing a NORMAL row in that case is a HARD GATE violation by definition.

**Concrete recipe — pre-write new-signal check (REPLACES the "any new finding" vagueness in the current matrix):**

```bash
# 1. Get current hermes cron list, hash it
CURRENT_HASH=$(hermes cron list 2>/dev/null | grep -E "Last run|Next run" | md5sum | cut -c1-12)

# 2. Compare to the hash recorded in the prior sweep row (or in the marker file)
PRIOR_HASH=$(cat ~/.hermes/profiles/qa-agent/.steady-state-idle 2>/dev/null | grep "cron_list_hash:" | cut -d' ' -f2)
# OR if no marker file:
#   PRIOR_HASH=$(grep -A 1 "H[0-9]\+ |" ~/.hermes/profiles/qa-agent/state.md | tail -1)

# 3. If hashes match → no new signal → STEADY_STATE_IDLE, write ≤200 bytes
# 4. If hashes differ → at least one cron changed → NORMAL with new-signal emphasis
if [ "$CURRENT_HASH" = "$PRIOR_HASH" ]; then
    MODE=STEADY_STATE_IDLE
else
    # Compute what changed
    DIFF=$(diff <(echo "$PRIOR_OUTPUT") <(echo "$CURRENT_OUTPUT"))
    MODE=NORMAL_WITH_NEW_SIGNAL
    # Include the diff in the new row
fi
```

## Companion fix: pending/handoff scan fingerprint

Same pattern applies to `find ~/.hermes/profiles -name "pending*" -o -name "handoff*"`:

```bash
# Hash the find output
PENDING_HASH=$(find ~/.hermes/profiles -name "pending*" -o -name "handoff*" 2>/dev/null | sort | md5sum | cut -c1-12)

# If unchanged from prior sweep → not a new signal
# If changed → document what changed (new file? deleted? renamed?)
```

## Why this fix is structural (not another soft rule)

The current HARD GATE fails because the "new signal" check is subjective — the agent gets to decide if its own writing constitutes a new signal. The cron-list-hash approach is **objective**: the SHA/MD5 of the cron list either matches or it doesn't. There's no "I found a new signal" interpretation — the system tells the agent definitively.

This pairs with H38 (which already uses `hermes cron list` as ground truth) — the new H32b fix uses the SAME source of truth to gate the row-writing decision.

## What to do in the next heartbeat

When the cron prompt matches the heartbeat trigger:

1. **First action:** `hermes cron list 2>/dev/null | grep -E "Last run|Next run" | md5sum | cut -c1-12`
2. **Compare to marker file's recorded hash (or prior row's recorded hash)**
3. **If match:** enter STEADY_STATE_IDLE, write ≤200 bytes, update marker file with new hash + timestamp
4. **If differ:** NORMAL with new-signal emphasis, document the diff in the new row
5. **If marker file doesn't exist:** write it on first entry with the current hash as baseline

The result: a system that is genuinely idle (no cron changes, no new findings) writes ONE row per N hours, not one row per cron tick. The 19-sweep verbose-loop pattern (H33-H51) becomes structurally impossible.

## Cross-references

- SKILL.md §"MANDATORY pre-write self-check (the 'no-verbose-loop' rule, H23) + HARD GATE (H32, 2026-06-26)" — the original rule
- `references/h32-hard-gate-enforcement.md` — the original H32 post-mortem; this file is the H32b post-mortem for the bypass
- `references/h38-mtime-vs-cron-truth-pattern.md` — H38 cron-truth; this H32b fix uses the same source of truth
- `references/h26-silent-kill-mode.md` — the original "deliver in response only" mode
