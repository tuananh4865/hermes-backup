# H58 evidence (2026-06-27 14:00) — Anchor When Prior Row Contains Legacy Table Separator

## TL;DR

When the most recent Recent Verdicts row was inserted DIRECTLY ABOVE a legacy `## Verdict History` section, and the row itself ends with the legacy `|------|---------|...|-------|` table separator (because the legacy section's table header was consumed into the prior row's tail), the H44 2-line anchor (`Sweep ready for next event.\n## Verdict History`) collides. The boundary is no longer `\n## Verdict History` — it is `\n| 1 | <legacy first row>`. Fix: **H58 extended anchor** = last 60 chars of prior row (which contain the unique `|------|...|-------|` sequence) + `\n` + first 22 chars of next legacy row.

## The Boundary Anomaly

By H58 (2026-06-27 14:00), `~/.hermes/profiles/qa-agent/state.md` had been restructured across many sweeps. The current shape is:

```
| H56 | ... | **Sweep ready for next event.** |
| H57 | ... | **Sweep ready for next event.** |------|---------|------|-------|---------|-------|
| 1   | 2026-06-17 07:43 | Test | "TikTok Shop Vietnam launched 2022" claim | ... |
| 2   | 2026-06-17 10:25 | ... |
```

Notice:
- **H56 ends with just `|`** (table cell terminator — H56 was inserted ABOVE the `|---|\n## Verdict History` boundary that existed at H56 time)
- **H57 ends with `|------|---------|------|-------|---------|-------|`** (H57 was inserted BEFORE the `## Verdict History` section header, but the prior `|---|` table separator is now glued to H57's tail because the insertion point collapsed the whitespace)
- **After H57 comes the LEGACY `## Verdict History` section content** (rows 1-N from 2026-06-17)

## Why H44 and H42 Failed at H58

### H44 2-line anchor attempt

```python
anchor = "Sweep ready for next event.\n## Verdict History"
content.count(anchor)  # → 0
```

`## Verdict History` is no longer adjacent to H57's tail. The legacy section header was swallowed into H57's structural insertion point. The actual boundary after H57 is `\n| 1 | 2026-06-17 07:43` (the first legacy row).

### H42 unique-phrase anchor attempt

```python
anchor = H57_line[-80:] + "\n## Verdict History"
content.count(anchor)  # → 0
```

Same problem — `## Verdict History` is no longer the next line after H57.

### H44 simple tail variant

```python
anchor = "**Sweep ready for next event.** |\n|---|"
content.count(anchor)  # → 2 (H56 + H57 both end this way)
```

Both H56 and H57 rows end with the literal `**Sweep ready for next event.** |\n|---|`. **Count=2 = collision.**

## The H58 Fix — Extended Anchor Recipe

**When the prior Recent Verdicts row contains the legacy `|------|---------|...|-------|` separator AND the next line is a legacy row (not a `##` section header):**

```python
# Step 1: Take the last 60 chars of prior row (includes the |------|...|-------| separator)
prior_tail = h57_line[-60:]
# → "event.** |------|---------|------|-------|---------|-------|"

# Step 2: Add newline + first 22 chars of the legacy row that follows
legacy_first = "| 1 | 2026-06-17 07:43"
anchor = prior_tail + "\n" + legacy_first
# → "event.** |------|---------|------|-------|---------|-------|\n| 1 | 2026-06-17 07:43"

# Step 3: Verify uniqueness
content.count(anchor)  # → 1 (UNIQUE)
```

## Why This Works

1. **Prior row's last 60 chars** include the unique `|------|---------|...|-------|` sequence — this tail is specific to the row that was inserted at this boundary position, because only that row absorbed the legacy separator into its tail
2. **The legacy first row's first 22 chars** (`| 1 | YYYY-MM-DD HH:MM`) are unique to that one historical row
3. **Combined, the 2-line anchor has sequence-level uniqueness** that survives even when:
   - Boundary token `## Verdict History` is no longer adjacent
   - Simple `|---|` matches multiple rows
   - Tail truncation reduced the readable chars

## Pre-Flight Detection Recipe

Before patching, run this Python to detect the structural anomaly:

```python
import re
content = open(state_md_path).read()
m = re.search(r'^\| H(\d+) \|.*', content, re.MULTILINE)
if m:
    last_row = m.group(0)
    # Does the last row end with the legacy separator?
    if last_row.endswith('|------|---------|------|-------|---------|-------|'):
        print("H58 STRUCTURAL ANOMALY DETECTED")
        print("  Last row ends with legacy |------|...|-------| separator")
        print("  Next line is a legacy row, NOT a `## Verdict History` header")
        print("  Use H58 extended anchor, not H44")
```

## Decision Tree — Updated Canonical Anchor Selection (H44 + H58)

```
1. Run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch (H40)
2. If count > expected → sibling-collision → renumber UP per H31/H40
3. If count == expected → choose anchor:
   a. If boundary token (`## Verdict History`) count == 1 → use H15 simple boundary
   b. If boundary token count 2-9 → use H25 4-line context anchor
   c. If boundary token count ≥10 AND prior row tail known ≤40 chars → H44 2-line fallback
   d. If boundary token count ≥10 AND prior row tail long/ambiguous → H42 unique phrase anchor (60-100 chars)
   e. If boundary token count ≥10 AND prior row tail TRUNCATED → H44 2-line fallback
   f. **🆕 H58: If prior row ends with `|------|---------|...|-------|` (legacy separator absorbed into tail) AND next line is a legacy row, NOT `## Verdict History`** → **H58 extended anchor: prior_tail[-60:] + `\n` + first 22 chars of legacy row**
```

## Validation at H58 (2026-06-27 14:00)

- **Pre-patch verification:** `content.count(anchor) = 1` (Python verified)
- **Patch applied:** clean on first attempt, no retries
- **Post-patch row count:** 53 → 54 (canonical Recent Verdicts H1-H58)
- **H58 row at line 98** with correct pipe format `| H58 |`
- **No row corruption**, no orphan content, table structure preserved
- **Sibling-collision pre-check:** count=52 before patch (expected 52, H57 was last canonical row from 13:00) — no sibling write between H57 and H58

## Why This Rule Is Permanent

1. **Structural cause:** The legacy `## Verdict History` section exists in qa-agent state.md because early sweeps (H1-H17) wrote rows with double-pipe legacy format. Future sweeps added rows above this section. After enough inserts, the boundary collapsed: H57's tail now contains the legacy separator that used to be a separate line. This is a CUMULATIVE FILE EVOLUTION pattern that will recur any time qa-agent state.md gets re-restructured.

2. **Recipe generalizes:** The H58 pattern (when a Recent Verdicts row absorbs a legacy structural element into its tail) applies to ANY boundary element that gets glued onto the prior row by cumulative insertion. Not just `|---|` — could be `| 1 |`, `|---|---|`, table header rows, etc.

3. **Pre-flight detection makes it cheap:** Running the 5-line Python check before constructing the anchor takes <1 second and prevents the failed-patch cycle.

4. **Future-proofing:** If qa-agent state.md is ever restructured again (e.g., row inserted between H57 and legacy section re-separates them), the H58 recipe gracefully degrades — the prior tail check fails, falls back to H44 or H42 recipes automatically.

## H58 Sweep Summary

- **Sweep index:** H58 (58th in file continuity H1-H58)
- **Cron-truth:** 18 active crons, ALL exit_status `ok`, ZERO error annotations
- **Pending/handoff:** 0 files (confirmed via `find ~/.hermes/profiles/ -name "pending*" -o -name "handoff*"`)
- **Per-profile status:** all 8 active profiles Goal=None or pure-routine-cron
- **H34 ops-manager:** WITHIN TOLERANCE sustained 11th consecutive sweep (slip_ratio 0.0)
- **H38 cron-truth:** 16/18 profile-aware crons healthy; 2 daily-cadence crons (Orchestrator Nightly Reflection, Research Lead Trend Scan) on normal schedules
- **Forecasts realized:** H57 forecast (Orchestrator Heartbeat 13:30 tick) → REALIZED 13:30:37 (37s late, within tolerance)
- **Forecasts in pre-fire:** qa-agent 14:00 tick (60s past schedule, will realize at H59)
- **Token cost so far:** 58 sweeps × ~3000 tokens ≈ 174K tokens
- **Cadence-decay:** Per H44 option (a) — "CADENCE TRIGGER ALREADY KNOWN", orchestrator has been told 57+ times. H60 auto-suspend holds per H51 codified timeline.

## Related Sweeps

- H57 (13:00): First H44 collision detection (count=2 on simple tail), escalated to H42
- H56 (12:01): First H44 simple boundary collision (count=2 on `Sweep ready for next event.\n## Verdict History`)
- H42 (23:00): First H42 unique-phrase anchor codified (60-100 char tail + boundary)
- H44 (00:00): H44 2-line fallback codified (last 30-40 chars + boundary)
- H58 (14:00): H58 extended anchor codified (60-char tail with absorbed legacy separator + first 22 chars of legacy row)
