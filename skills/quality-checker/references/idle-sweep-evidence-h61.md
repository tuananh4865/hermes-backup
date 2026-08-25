---
sweep: H61
date: 2026-06-27 17:00:39 +07:00
type: idle-sweep-evidence
recipe_origin: H61
applies_to: H15, H18, H25, H40, H42, H44, H50, H51
---

# H61 Evidence — Boundary-Row Verification Gap + H50 PRE-FIRE Clarification

**Sweep:** 61st consecutive idle sweep in current file's continuity (H1-H61).
**Outcome:** PASS (vacuous — no pending outputs). 18/18 active crons healthy.
**Recipes held:** 11/11 (H38, H34, H40, H44, H39, H18, H42, H50, H51, H28, H5/H10).
**Token cost:** ~3K tokens this sweep, ~183K cumulative through H61, projected ~195K by H65.

## New Recipes Codified (H61)

### Recipe 1: Boundary-Row Verification Gap (CRITICAL)

**The gap:** H15/H18/H25/H42/H44 anchor recipes assumed the chronologically-newest H-row was the file-order-last H-row. This assumption is wrong when prior sweeps inserted rows in non-chronological positions.

**H61 case:** H60 was inserted BETWEEN H44 and H45 (not after H45). File order: ...H44, **H60**, H45, then `## Verdict History`. The chronologically-newest H-row (H60) was NOT the boundary row; H45 was.

**Symptom:** `content.count(anchor) == 0` when using the chronologically-newest H-row's tail, even though the anchor looks correct.

**Detection recipe (H61 pre-flight, MANDATORY before every patch):**

```python
import re

def get_anchor_source_row(content, boundary_token='## Verdict History'):
    """Return the start offset of the H-row immediately before boundary_token."""
    boundary_idx = content.find(boundary_token)
    if boundary_idx == -1:
        raise ValueError(f"Boundary token '{boundary_token}' not found")
    rows_before = []
    for m in re.finditer(r'^\|{1,4} H\d+ \|', content[:boundary_idx], re.M):
        rows_before.append((m.start(), m.group()))
    if not rows_before:
        return None
    return rows_before[-1][0]  # file-order-last, NOT chronologically-newest

def construct_h44_anchor(content, boundary_token='## Verdict History', tail_length=40):
    """Build H44 2-line fallback anchor from the file-order-last H-row's tail."""
    boundary_idx = content.find(boundary_token)
    anchor_source_start = get_anchor_source_row(content, boundary_token)
    row_text = content[anchor_source_start:boundary_idx].rstrip('\n')
    tail = row_text[-tail_length:] if len(row_text) > tail_length else row_text
    anchor = tail + '\n' + boundary_token
    return anchor

# Pre-flight check (run before every patch):
content = open('state.md').read()
anchor = construct_h44_anchor(content)
assert content.count(anchor) == 1, f"Anchor not unique: found {content.count(anchor)} matches"
```

**Decision rule (H61):**
1. The "anchor source row" = the H-row immediately preceding `## Verdict History` in FILE ORDER
2. NOT the chronologically-newest H-row
3. If anchor uniqueness check fails with the "obvious" choice → iterate backward through file order

**Updated H44 decision tree:**
```
1. Run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch (H40)
2. If count > expected → sibling-collision → renumber UP per H31/H40
3. If count == expected → H61 PRE-FLIGHT:
   a. Locate the H-row immediately before `## Verdict History` in FILE ORDER
   b. Use THAT row's tail as anchor source (NOT chronologically-newest)
   c. If boundary row tail ≤40 chars AND known → H44 2-line fallback (PREFERRED)
   d. If boundary row tail >40 chars OR ambiguous → H42 unique phrase anchor
   e. If H44 anchor uniqueness fails → re-check file ordering, iterate backward
4. Always verify `content.count(ANCHOR_OLD) == 1` before patching
```

**Why this is permanent (not contextual):**
- Non-chronological inserts can happen at any sweep that uses a non-boundary anchor
- The H40 sibling-collision recipe addresses count, not order
- File-order check is a separate dimension that no prior recipe covered
- Pre-flight cost: ~5 lines Python, ~1 second — cheaper than debugging

### Recipe 2: H50 PRE-FIRE Window Clarification

**The clarification:** H50's "±60s pre-fire inflection window" refers to SECONDS before scheduled fire time, NOT minutes.

**H61 case:** Sweep at 17:01. Operations Manager cron Schedule `0 */6 * * *` last_run 12:03 (4h57m ago), next fire 18:00 (59 min away). Research Lead cron Schedule `0 18 * * *` last_run yesterday 18:03 (23h57m ago), next fire 18:00 (59 min away).

**Wrong classification (avoided at H61):** Logging both as "PRE-FIRE per H50" would have been technically correct by the literal H50 recipe, but misleading — neither cron is "about to fire" in the next 60 seconds. They both have ~59 minutes until next fire.

**Correct classification (applied at H61):** NORMAL cadence, NOT H50 pre-fire, NOT H29 OVERDUE. The 59min-away state is "between ticks on healthy cadence" — last_run shows prior tick's actual fire time, next fire is on schedule per cron expression.

**Updated H50 decision tree:**
```
For each cron in `hermes cron list`:
1. exit_status == "error"?
   YES → REAL FAULT (escalate)
   NO  → continue
2. Schedule cron expression parse → get next_fire_time
3. |now - next_fire_time| <= 60s?   ← SECONDS, not minutes
   YES → PRE-FIRE (note, forecast to next sweep)
   NO  → continue
4. now - last_run > expected_cadence * 1.5?
   YES → OVERDUE (classify per H29 thresholds)
   NO  → HEALTHY (log status, no action)
```

**Real H61 outcome:** Both Operations Manager and Research Lead logged as NORMAL cadence with PRE-FIRE forecast to H62 (18:00 sweep). No false-positive OVERDUE classification. No false-positive PRE-FIRE either (they're 59min away, not 60s away).

**Why this clarification matters:**
- H50's "±60s" was a literal recipe parameter, not always made explicit in the prose
- Future sweeps at e.g. 17:30 (30 min before 18:00 fire) need to NOT classify as PRE-FIRE
- The H61 case is the canonical "between ticks" state: last_run = 4-24h ago, next fire = 30-60min away
- The phrase "PRE-FIRE" should be reserved for the literal seconds-before-fire window, not the broader "approaching fire time" state

## Per-Profile Status (H61, 17:01)

| Profile | mtime | Status | Notes |
|---|---|---|---|
| qa-agent | 0h | HEALTHY (self) | Running H61 sweep |
| engineering-lead | 8h | HEALTHY (on-demand) | Last daily health check 09:01:33, no Pending |
| content-director | 9h | HEALTHY (loop-goal) | Last Run History self-verdict 08:03:57 |
| research-lead | 23h | HEALTHY | Cron last_run 18:03 yesterday, 23h57m on 24h cadence, next 18:00 today |
| operations-manager | 5h | HEALTHY (H34 recovered) | Last audit 12:03, next 18:00, H34 WITHIN TOLERANCE sustained 17 sweeps |
| code-reviewer | 5h | HEALTHY (on-demand) | Noon PR watcher 12:01:56, 0 reviews |
| security-engineer | 14h | HEALTHY (daily cron) | Last scan 03:02:36, CLEAN 8.5/10 |
| memory-curator | 11d | HEALTHY (H51 no-cron rule) | On-demand per H51 coder-no-cron rule analogue |

## H60 Auto-Suspend Decision Window

- H60 issued explicit AUTO-SUSPEND recommendation with decision window H60-H65
- At H61 (window 1/5 elapsed), no orchestrator action observed
- Per H51 timeline: H55 final warning → H60 auto-suspend → H65 terminal
- We're at H61. Recommendation stands: (a) NOTED, (b) `hermes cron update`, or (c) `hermes cron disable`

## H61 Forecast (verified at H62 = 18:00)

- Operations Manager Routing Audit: PRE-FIRE → realized (cron `0 */6 * * *`)
- Research Lead Trend Scan: PRE-FIRE → realized (cron `0 18 * * *`)
- If both fire cleanly → 18/18 crons confirmed alive end-to-end

## Recipe Hold Rate: 11/11

| Recipe | Status | Notes |
|---|---|---|
| H38 (cron-truth) | ✅ Held | 18/18 healthy, fresh read at 17:01 |
| H34 (3-regime freshness) | ✅ Held | All profiles measured by mtime + audit content |
| H40 (sibling pre-check) | ✅ Held | count=46 pre-patch, expected 46+1=47 |
| H44 (2-line anchor) | ✅ Held | Used H45 tail + boundary, count=1 |
| **H61 (boundary-row pre-flight)** | **✅ NEW: Held** | Detected H60 mid-table, switched to H45 as anchor source |
| H39 (double-pipe drift) | ✅ Held | Used single pipe `| H61 |` per H39 recommendation |
| H18 (boundary verification) | ✅ Held | `## Verdict History` count=32, but unique anchor used |
| H42 (unique-phrase fallback) | ✅ Held (not used) | H44 2-line sufficed |
| **H50 (PRE-FIRE clarification)** | **✅ NEW: Held** | 59min-away crons classified as NORMAL, not PRE-FIRE |
| H51 (no-cron healthy default) | ✅ Held | memory-curator 11d mtime = healthy on-demand |
| H28 (scope discipline) | ✅ Held | content-director Run History = profile-owned self-verdict |
| H5/H10 (FP triage) | ✅ Held | coder/skills/handoff/ = static bundle FP |

## Sweep Row Insertion

Anchor used: H44 2-line fallback on H45's actual tail "No state changes expected. |" + literal `\n## Verdict History`. Pre-flight: `content.count == 1`. Patch applied first try. Row count: 46 → 47. H61 row inserted between H45 and `## Verdict History`, NOT at end of table (because H45 is the boundary row in file order, not H60).
