# H55 Evidence (2026-06-27 11:00) — Boundary-Structure-Drift Anchor Recipe

**Headline finding:** The H44 2-line anchor recipe (H<N> tail + `\n## Verdict History`) silently FAILS when the file's structural layout has been disturbed — i.e., when the last H<N> row no longer sits IMMEDIATELY ABOVE the `## Verdict History` section header.

## Context

At H55, the file `~/.hermes/profiles/qa-agent/state.md` had been structurally disturbed by H53 (orchestrator 30m heartbeat cron at 10:01) and H54 (qa-agent hourly gate at 10:03). Both rows were inserted BELOW the legacy `## Verdict History` header (line 89) rather than above it, leaving the boundary AFTER the H54 row as a legacy `|---|` table separator (line 94), NOT the `## Verdict History` header.

```
Line 87: | H51 | ... (last row in canonical Recent Verdicts section)
Line 88: [truncated] marker
Line 89: ## Verdict History   ← legacy section header
Line 90: ||| # | Time | ...   ← legacy table header (triple pipe)
Line 91: ||| H53 | ...        ← orchestrator's row, inserted BELOW legacy header
Line 92: |---|------|...|     ← legacy table separator
Line 93: | H54 | ...          ← qa-agent's H54 row
Line 94: |---|------|...|     ← boundary AFTER H54 = legacy table separator
Line 95+: legacy 2026-06-17 test rows, then ## What Worked, etc.
```

## Symptom

- `content.count("**Sweep ready for next event.** |\n## Verdict History")` returned **0** (H44 anchor does not exist in the file at any position)
- The H42/H44 recipes both fail pre-patch uniqueness check
- Naive application of H44 would have either: (a) failed to find a match → patcher error, or (b) matched a different position (e.g., a row body containing both phrases) → silent data corruption

## Detection recipe (H55 — Permanent)

BEFORE constructing the patch anchor, ALWAYS verify the actual line that follows the last H<N> row. Do NOT assume it's `## Verdict History` just because prior rows were anchored there.

```python
import re
content = open(state_md_path).read()
# Find the last H<N> row
last_h_match = None
for m in re.finditer(r'^\|{1,4} H(\d+) \|', content, re.MULTILINE):
    last_h_match = m
last_h_end = last_h_match.end()
# What is the next non-blank line after the H<N> row?
rest = content[last_h_end:].lstrip('\n')
next_line = rest.split('\n')[0]
print(f'Boundary line after H{last_h_match.group(1)}: {next_line[:100]}')
```

## Anchor construction when boundary is NOT `## Verdict History`

1. Identify the actual boundary line (e.g., `|---|------|---------|------|-------|---------|-------|` for legacy table separator, or any other line that appears EXACTLY ONCE in the file at the boundary).
2. Use a 2-line or 3-line anchor with a SHORT unique phrase from the prior row's tail + `\n` + the actual boundary line.
3. Verify with `content.count(anchor) == 1` before patching.
4. If the boundary line is the legacy table separator `|---|...|` AND the file has multiple `|---|` rows (e.g., a current Recent Verdicts table header AND a legacy Verdict History separator), use a LONGER phrase from the prior row's tail to disambiguate. At H55, the anchor was: `No state changes expected. **Sweep ready for next event.** |\n|---|` (count=1) — the disambiguating phrase "No state changes expected." before the shared tail ensured uniqueness.

## Why this rule is permanent

The file structure of `~/.hermes/profiles/qa-agent/state.md` is NOT invariant. Patches anchored on `## Verdict History` since H1 have all placed new rows in the "Recent Verdicts" section (above `## Verdict History`). But when:

- A sibling cron (orchestrator 30m heartbeat) writes its row at a different anchor point
- A row is inserted via a DIFFERENT mechanism (e.g., manual edit, git checkout, file merge)
- The file has been restructured (e.g., section renames, header additions)

...the H44 anchor assumption breaks silently. A future sweep at H55+ that blindly applies H44 would either:
- Patch with `count == 0` → patcher fails with "Could not find a match"
- Patch with a non-unique anchor that happens to match elsewhere → silent data corruption

## H55 unified anchor decision tree (FINAL — supersedes H44 tree when boundary is non-standard)

```
1. Run `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch (H40)
2. If count > expected → sibling-collision → renumber UP per H31/H40
3. If count == expected → choose anchor:
   a. Inspect the line IMMEDIATELY after the last H<N> row. What is it?
      - Is it `## Verdict History`? → Use H44 2-line recipe (H<N> tail + `\n## Verdict History`)
      - Is it `|---|...|`? → File has been restructured. Use H55 boundary-drift recipe
      - Is it something else (e.g., a section header, a table row, blank)? → Use H55 recipe with that line
   b. If boundary line is non-unique (appears multiple times in file), use the FULL disambiguating
      tail phrase (e.g., "No state changes expected. **Sweep ready for next event.** |") + boundary
   c. Always verify with `content.count(ANCHOR_OLD) == 1` before patching
4. If pre-patch verification FAILS at any step → run the H19 truncated-tail recovery
   (terminal `awk NR==<row_line>` to find the true row tail) → retry with corrected tail
```

## H55 mitigation steps applied (reference for future)

1. Ran `python3` heredoc to enumerate boundary positions: confirmed `\n## Verdict History` appeared 28 times in file (1 actual section header + 27 inline references inside prior row bodies).
2. Found the actual boundary AFTER H54: the legacy `|---|` table separator at line 94.
3. Discovered the H44 anchor `H54 tail + \n## Verdict History` had count=0 (didn't exist in file).
4. Disambiguated with the H55 row's signature phrase: `No state changes expected. **Sweep ready for next event.** |` (unique to H54's conclusion) + `\n|---|` (the actual boundary).
5. Verified with `content.count(anchor) == 1` before patching.
6. Patch applied cleanly on first attempt.

## H55 outcome

- 12/12 recipes held (H38, H34, H40, H44, H39, H18, H31, H50, H51, H52, H36, H42)
- New H55 boundary-structure-drift recipe operationalized
- Patch applied first try with new 3-line anchor (signature phrase + newline + boundary)
- Row count: 53 → 54 (H55 inserted cleanly)
- 0 outputs awaiting verification; 0 escalations

## Forecast for H56 (12:00)

At H56, expect 3 pre-fire windows to be captured or realized:
- Operations Manager Routing Audit (`0 */6 * * *`): next 12:00 today
- Code Reviewer PR Watcher (`0 12 * * *`): next 12:00 today
- qa-agent Quality Gate (`0 * * * *`): next 12:00 today

If the file structure is unchanged (no other crons have inserted rows between H55 and H56), the H44 anchor recipe will be SAFE again (because the new H55/H56 rows will be appended after the legacy `|---|` boundary, making `## Verdict History` the boundary after H56). If another cron writes into a different anchor position, the H55 recipe will need to be re-applied.

## Related recipes

- H15 (boundary anchor): original `## Verdict History` recipe, fails when boundary is non-unique
- H18 (boundary collision): use multi-line context when boundary appears in row bodies
- H25 (4-line context anchor): robust but verbose, works for most cases
- H42 (unique phrase anchor): 60-char tail + boundary, works at high boundary count
- H44 (2-line fallback): short tail + boundary, PREFERRED when prior row tail is known
- **H55 (boundary-structure-drift):** detect actual boundary line, use it instead of `## Verdict History`
