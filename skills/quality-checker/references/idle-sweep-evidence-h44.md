---
sweep_id: H44-lesson
sweep_time: 2026-06-27T00:00:39+07:00
triggering_sweep: H43
profile: qa-agent
type: idle-sweep-evidence + recipe-refinement
---

# H44 Evidence — H42 Recipe Refinement + Cadence Boilerplate Decay

## Context

H43 was the 43rd consecutive idle sweep in current file's continuity (H1-H43), running on the qa-agent hourly cron at the 00:00 day-rollover boundary. The session produced two new learnings that warranted documentation in the quality-checker skill.

## Finding 1: H42 unique-phrase-anchor recipe breaks on read_file truncation

### Symptom
First patch attempt at H43 failed:
```
Could not find a match for old_string in the file
```

The H42 recipe (per skill section "H42 Unique Phrase Anchor Recipe") required:
1. Pick last 60-100 chars of prior row's tail
2. Append `\n## Verdict History`
3. Verify `content.count(phrase) == 1` before patching
4. Apply patch

The recipe failed at step 4 (verification) because the prior row's tail I had was **truncated mid-sentence** by `read_file(limit=2000)`. The wrapper showed `[truncated]` marker, but the cell body shown to me ended with "H42 continues the idle pattern but with research-lead reactivation providing first real signal since H1. Sweep ready for next event." — which is the END of a sentence but NOT the end of the row. The row continues after that sentence with "**H42 FORECAST REALIZATION CHECK:**" and additional content. My "tail" was a mid-row cutoff.

### Root cause
- H42 row at H43 was ~7KB in length (long Notes column)
- `read_file(limit=2000)` truncates at ~3KB silently
- The H42 recipe's pre-condition ("you've just read the prior row's tail") is not always met after truncation
- Constructing an anchor from truncated content produces a phrase that exists in my view but NOT in the file

### Recovery
1. Ran `awk 'NR==78' state.md | tail -c 250` via terminal to get the ACTUAL row tail
2. Discovered the truncation had cost me precision
3. Abandoned the H42 60-char-tail approach entirely
4. Fell back to a 2-line literal anchor: `Sweep ready for next event.\n## Verdict History`
5. This worked first try because:
   - "Sweep ready for next event." appears in exactly one cell (H42's Notes column)
   - `\n## Verdict History` immediately after it is a one-of-one boundary
6. Patch succeeded, row count went 42 → 43

### Why the 2-line anchor is better than H42 in truncation conditions
- H42 requires 60+ chars of TRUE tail + boundary + uniqueness check
- 2-line fallback requires ~20-40 chars of KNOWN tail + boundary + uniqueness check
- When you only have a truncated tail, the 2-line fallback is strictly more robust
- The 2-line anchor IS what H42 reduces to at the limit case — it just formalizes it

## Finding 2: Cadence trigger boilerplate has become noise at 43+ idle sweeps

### Pattern observed
Across H1-H42 (and now H43), the same boilerplate appears in 43 consecutive rows:
> "CADENCE TRIGGER PERSISTS: N consecutive idle sweeps — recommendation to reduce qa-agent cron from hourly to 6h is now URGENT/CRITICAL"

### Why this is now noise
- The recommendation has been made 43 times without action
- At H1, the signal was "first time" — high information value
- At H10, the signal was "persists" — moderate value
- At H20, the signal was "URGENT" — escalation, still valuable
- At H30+, the signal is "I have nothing new to say about cadence" — zero marginal value
- Each repeat dilutes the new evidence (cron truth, sibling-collision detection, research-lead reactivation) that the row DOES contain

### Recommended fix
Replace the cadence boilerplate in H44+ rows with one of:
1. **Status-quo acknowledgment:** "CADENCE TRIGGER ALREADY KNOWN — 43 rows have stated 'URGENT' without action. Defer to Orchestrator." (saves ~30 chars per row)
2. **Cost-projection escalation:** "43 sweeps × ~3000 tokens/sweep = ~129K tokens on idle sweeps. If not actioned by H50, recommend auto-suspending qa-agent cron entirely." (provides NEW evidence)
3. **Token-economy mode switch:** At 30+ idle sweeps, the row itself should be SHORTER (per H22 token-economy recipe) — currently each row is ~7KB of mostly repeated analysis. Reducing to 2-3KB per row would save ~4KB × 30 rows = ~120KB of cumulative context.

## Pre-append anchor selection decision tree (H44 codification)

```
1. Run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch (H40)
2. If count > expected → sibling-collision → renumber UP per H31/H40
3. If count == expected → choose anchor:
   a. If boundary token (`## Verdict History`) count == 1 → use H15 simple boundary
   b. If boundary token count 2-9 → use H25 4-line context anchor
   c. If boundary token count ≥10 AND prior row's true tail is known (read via terminal/awk, NOT truncated read_file) → use H42 unique phrase anchor
   d. If boundary token count ≥10 AND prior row's tail is TRUNCATED in your read → use H44 2-line fallback (shortest known tail + boundary)
4. Always verify with `content.count(ANCHOR_OLD) == 1` before patching
```

## Recipe comparison (anchor patterns)

| Pattern | Boundary count | Requires true tail? | Multi-line? | Worked at H43? |
|---|---|---|---|---|
| `\n\n## Verdict History` (H15) | 1 | No | No | Yes (low boundary count, but boundary count was 23+) |
| 4-line context anchor (H25/H26) | 2-15 | Yes (3+ lines) | Yes | Could have worked |
| **Unique phrase anchor (H42)** | 10+ | Yes (60 chars) | No | **NO** (truncation broke it) |
| **2-line fallback (H44)** | any | Yes (1 line, 20-40 chars) | No (2 lines) | **YES** (first try) |

## Lesson learned
- Recipes that assume "you've just read the prior row's tail" need a fallback for when that read was truncated
- The H44 2-line fallback is strictly SIMPLER than H42 (no 60-char-tail construction) AND works in more conditions (truncation-safe)
- Recommend deprecating H42 in favor of H44 going forward — H44 IS what H42 reduces to at the limit case
- Sibling-collision check (H40) and the H44 anchor selection should be the only TWO mandatory pre-patch checks going forward

## Cross-references
- H15: First boundary anchor recipe (sweep 2026-06-25)
- H18: Boundary-token collision in row bodies
- H19: read_file truncation pitfall (first documented)
- H25: Multi-line context anchor
- H26: First prospective application of H25, 4-line anchor
- H31: Sibling-collision detection
- H40: Pre-patch check (must run twice, IMMEDIATELY BEFORE patch)
- H42: Unique phrase anchor (broke at H43 due to truncation)
- **H44: Truncation-safe fallback + cadence boilerplate decay lesson**

## Patch verification (H43 actual)
- Pre-patch: `grep -cE "^\|{1,4} H[0-9]+ \|"` = 42 (expected 42, no sibling collision)
- Pre-patch: H42 read with `awk NR==78 | tail -c 250` to find true tail
- Anchor chosen: 2-line fallback (H44) — `Sweep ready for next event.\n## Verdict History`
- Pre-verify: `content.count(ANCHOR_OLD) == 1` (confirmed)
- Patch applied: success on first attempt
- Post-patch: row count = 43, no orphan content, H43 row at correct position
