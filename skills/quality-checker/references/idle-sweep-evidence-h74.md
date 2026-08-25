---
evidence_id: idle-sweep-evidence-h74
sweep: H74
date: 2026-06-29 12:01:42 +07:00
trigger: qa-agent 6h gate cron (Schedule `0 */6 * * *`)
related: H44 (2-line anchor), H42 (unique-phrase anchor), H57 (generalized boundary recipe), H40 (sibling-collision pre-check)
status: PERMANENT PATTERN — codified for future sweeps
---

# H74 Evidence — H44 2-Line Anchor Double-Newline Boundary Pitfall

## Summary

The H44 2-line anchor recipe (`last short unique tail + boundary section header`) silently produced a DUPLICATE section header at H74 because the file's natural boundary is `\n\n## Verdict History` (double-newline) and the `new_string` included the section header text. The duplicate was caught by post-patch verification and fixed in-sweep. No data loss, but ~30s wasted work + 1 extra patch round-trip. Recipe is now formal: **always inspect the file's actual newline structure between prior row and boundary before constructing `new_string`**, and **always verify `real_headers == 1` post-patch**.

## Case Study (H74 Sweep, 2026-06-29 12:00)

### Setup
- Prior row (H73) ended with: `sweep ready for next event. |`
- File content after H73 row: `\n\n## Verdict History\n|| # | Time | Subject | Task | Score | Verdict | Notes |\n|---|...`
- Boundary style: **double-newline** (`\n\n` between row and `## Verdict History`)

### What Happened

```python
# Constructed anchor per H44 recipe (treating boundary as single-newline case)
old_string = "sweep ready for next event. |\n"  # row-end + single newline
new_string = "...H74 sweep ready for next event. |\n\n## Verdict History\n"  # row-end + DOUBLE newline + header
```

The patch succeeded (the `old_string` matched), but the **result was a duplicate header**:
- Before patch: `...| \n\n## Verdict History\n|| # | Time...`
- After patch:  `...| \n\n## Verdict History\n## Verdict History\n|| # | Time...`

The `new_string` emitted `\n## Verdict History` (single new), and the file's existing content after my `old_string` was `\n## Verdict History` (single new, from the `\n\n` after the first `## Verdict History` consumed the prior newline). Combined: two adjacent `## Verdict History` headers.

### Detection

Post-patch Python verification caught it:
```python
content = open(state.md).read()
print(content.count("## Verdict History"))  # → 13 (expected 12: 1 real header + 11 inline refs)
print(content.count("\n## Verdict History"))  # → 2 (expected 1)
# Then check real headers (own-line, not inside row bodies)
import re
print(len(re.findall(r'^## Verdict History\s*$', content, re.MULTILINE)))  # → 2 (expected 1) ← DUPLICATE
```

### Recovery (Same Sweep)

Follow-up patch removed the duplicate:
```python
patch(old_string="H74 sweep ready for next event. |\n\n## Verdict History\n## Verdict History\n|| # | Time | Subject",
      new_string="H74 sweep ready for next event. |\n\n## Verdict History\n|| # | Time | Subject")
```

Final state: `real_headers = 1` ✅.

## The Recipe (H74 — Permanent)

### Pre-Construction: Inspect the Boundary

```python
import re
content = open(state_md_path).read()
prior_row = re.search(r'^\| H<N-1> \|.*$', content, re.MULTILINE)
idx = prior_row.end()
post_row_text = content[idx:idx+200]
# Identify boundary style
if post_row_text.startswith('\n\n## '):
    boundary_style = 'DOUBLE_NEWLINE'  # blank line between row and header
elif post_row_text.startswith('\n## '):
    boundary_style = 'SINGLE_NEWLINE'  # header immediately after row
elif post_row_text.startswith('## '):
    boundary_style = 'NO_NEWLINE'  # header on same logical line
else:
    boundary_style = 'OTHER'
print(f'Boundary style: {boundary_style}')
print(f'Post-row text: {post_row_text[:50]!r}')
```

### Construction Rules by Boundary Style

| Style | old_string | new_string |
|---|---|---|
| **SINGLE_NEWLINE** (H44 original case) | `...row tail. \|\n` | `...row tail. \|\n## Verdict History\n` + H<N> row |
| **DOUBLE_NEWLINE** (H74 case) | `...row tail. \|\n\n## Verdict History` | `...row tail. \|\n\n` + H<N> row + `\n\n## Verdict History` |
| **NO_NEWLINE** (rare) | `...row tail. \|## Verdict History` | `...row tail. \|\n` + H<N> row + `\n## Verdict History` |

**The cleaner approach (recommended for DOUBLE_NEWLINE case):** extend `old_string` to include the FULL boundary text (up to and including the section header), so `new_string` can re-emit it exactly once without duplication.

### Post-Patch Verification (mandatory)

```python
content = open(state_md_path).read()
import re
real_headers = len(re.findall(r'^## Verdict History\s*$', content, re.MULTILINE))
assert real_headers == 1, f'Expected 1 real section header, found {real_headers} — DUPLICATE BOUNDARY'
# Also check row count
rows = re.findall(r'^\|{1,2} H\d+ \|', content, re.MULTILINE)
assert len(rows) == expected_count, f'Expected {expected_count} rows, found {len(rows)}'
print(f'Post-patch verification PASS: {real_headers} real header, {len(rows)} rows')
```

If `real_headers > 1` → duplicate boundary → fix with a follow-up patch removing one duplicate.

## H44 Decision Tree — Extended (H74)

```
1. Run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch (H40)
2. If count > expected → sibling-collision → renumber UP per H31/H40
3. If count == expected → choose anchor:
   a. If boundary token (`## Verdict History`) count == 1 → use H15 simple boundary
   b. If boundary token count 2-9 → use H25 4-line context anchor
   c. If boundary token count ≥10 AND prior row's true tail is ≤40 chars AND known → use H44 2-line fallback
   d. If boundary token count ≥10 AND prior row's tail is >40 chars or ambiguous → use H42 unique phrase anchor
   e. If boundary token count ≥10 AND prior row's tail is TRUNCATED in your read → use H44 2-line fallback
4. **H74 NEW: Inspect boundary style** (SINGLE_NEWLINE / DOUBLE_NEWLINE / NO_NEWLINE) per pre-construction recipe
5. Construct `old_string`/`new_string` per boundary style table
6. Always verify with `content.count(ANCHOR_OLD) == 1` before patching
7. **H74 NEW: Post-patch verification** — run `real_headers == 1` assertion + row count check
```

## Why This Rule Is Permanent

- The H44 recipe is now used in 8+ consecutive sweeps (H67-H74) — high enough frequency that even rare failure modes are encountered regularly
- Silent duplicate headers (cosmetic at first glance) cause downstream parsing issues: any tool that counts section headers (state.md auditors, future H44 recipes using `## Verdict History` as anchor) gets confused by duplicates
- The H42/H57 candidate-list approach (`["\n## Verdict History", "\n|---|", "\n---\n"]`) partially mitigates this by offering alternative boundary tokens, but the cleanest fix is to construct `old_string` to include the full boundary
- Adding the boundary style check + post-patch verification adds ~10 seconds to sweep time but eliminates an entire class of mid-sweep fixup
- The H18 boundary-token-collision pitfall was about boundary tokens appearing INSIDE row bodies; H74 is about boundary tokens being DUPLICATED by patcher new_string emission — related but distinct failure mode

## Related Evidence

- H15 sweep evidence — first H44 anchor recipe validation
- H18 sweep evidence — boundary-token-collision pitfall (different failure mode)
- H19 sweep evidence — mid-row truncation anchor pitfall
- H42 sweep evidence — H42 unique-phrase anchor recipe
- H43 sweep evidence — H44 truncation-safe fallback
- H44 sweep evidence — H44 2-line anchor preference validation
- H57 sweep evidence — H42 boundary-token generalization
- H70 sweep evidence — H70 awk-Tail Pitfall (separate anchor extraction pitfall)
- H73 sweep evidence — H73 token-economy profile read recipe

## H74 Sweep Other Findings (for context)

H74 was a 6h-cadence sweep (74th in current file's continuity) that:
- Confirmed H23 cross-validation regime with ops-manager 06:00 audit (5h57m old, on cadence)
- Verified all 18 crons healthy via fresh `hermes cron list` at 12:01:42 +07:00
- Updated H73 forecast check: H73 forecast "H74 next 2026-06-29T06:00" was wrong per H46 lesson; actual H74 fired at 12:00 (cron last_run 06:00:28 was the trigger fire for the 12:00 tick)
- 0 pending outputs, 0 escalations, system HEALTHY
- Recipe hold rate 10/10

The H74 boundary bug was the only issue, caught and fixed in the same sweep.
