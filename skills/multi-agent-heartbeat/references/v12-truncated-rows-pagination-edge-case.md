# V12 — Truncated-Rows Pagination Edge Case

**Discovered:** 2026-06-28 22:00+07:00 (orchestrator 30m heartbeat, 6th pass after V11 validation log)
**Context:** qa-agent state.md at 209KB / 120 lines, with many prior sweeps leaving rows that show `truncated: true` in the `read_file` output (file itself is intact — truncation is a display artifact of the 100K char safety limit).
**Status:** Validated in 1 sweep. Recipe is canonical for V12+ sweeps when file > 200KB with prior truncation artifacts.

## Problem

V6 pagination recipe says: 1st call `offset=1, limit=60` + 2nd call `offset=59, limit=60`.

But when a file is at 200KB+ AND prior sweeps left truncation markers in the middle of the file (which is what happens after 70+ H-rows where each row is 4-8KB), the offset-boundary `offset=59` actually lands **inside** a structural section (Recent Verdicts table header) rather than in the recent H-rows. The 2nd call returns duplicate structural content + first half of the table, not the most recent H-row.

Symptom: orchestrator reads "second half of the file" but gets section headers + table header + first few rows of `## Verdict History`, NOT the most recent H72/H71 row from the sweep log.

## Detection

After 1st call (`offset=1, limit=60`):
- If file is at the 100K char safety limit but returned `< 100K chars` (means there are short lines / lots of structure), proceed with V9 single-call recipe OR use the V12 split.
- If 1st call hit the safety limit refusal, file is >200KB. Use V12 split.

## V12 Canonical Recipe

For files in 200KB–250KB range with prior truncation artifacts:

```python
# 1st call — frontmatter + structural sections + early H-rows
read_file(path=state_md_path, offset=1, limit=60)
# Returns: frontmatter, Current Goal, Active Tasks, Recent Verdicts header,
#          first ~30 H-rows. ~50KB. Below 100K limit.

# 2nd call — recent H-rows + Verdict History table
read_file(path=state_md_path, offset=61, limit=60)
# Returns: H-rows ~50-72 (most recent sweeps), `## Verdict History` table
#          header + first ~4 rows. ~50KB. Below 100K limit.
```

**Key boundary:** `offset=61` (NOT `offset=59`) — skips past the structural section boundary (Recent Verdicts header + table header + ~2 rows) so the 2nd call lands in pure H-row territory.

## V12 vs V6 vs V9

| Recipe | File size | 1st call | 2nd call | When to use |
|---|---|---|---|---|
| V9 single | <200KB | `offset=1, limit=50` + `tail -10` | (single call) | Routine "anything new?" confirmation |
| V6 split | 200-250KB, no prior truncation | `offset=1, limit=60` | `offset=59, limit=60` | Clean files, structural comparison needed |
| **V12 split** | **200-250KB, prior truncation artifacts** | **`offset=1, limit=60`** | **`offset=61, limit=60`** | **Files with 70+ H-rows, prior sweeps left truncation** |

## Validation

V12 1st-pass (2026-06-28 22:00):
- qa-agent state.md: 209,465 chars / 120 lines / 209KB
- 1st call: `offset=1, limit=60` → returned frontmatter + structural sections + H1-H33 (~50KB). No truncation marker.
- 2nd call: `offset=61, limit=60` → returned H33-H72 + `## Verdict History` table + final sections (~50KB). No truncation marker.
- Total: ~100KB, right at the safety limit, but functional.
- Found H72 (qa-agent's most recent sweep at 21:30) — confirmed cross-validation matches operations-manager 18:00 audit + 18/18 crons OK + 0 stuck + 0 pending QA + 0 escalations.
- Tool calls: 5 parallel state.md reads (4 small + 1 split for qa-agent) — well within H32b budget of ~10.

## When V12 Becomes Insufficient

V12 fails when file > 250KB → H32 HARD GATE triggers compaction per `heartbeat-state-md-bloat.md`. Don't try to extend pagination further — that's the wrong lever. Compaction is the right response.

If 250KB compaction has not yet run but file is at 240-250KB, V12 still works but is at the edge. Monitor with `wc -c` at start of every sweep.

## Failure Modes to Avoid

- **Don't use `terminal(tail -10)` for routine sweeps** — V12 covers files up to 250KB. `tail` loses structural sections and prevents H38 cross-validation.
- **Don't try `offset=80, limit=60` "to be safe"** — skips H40-H70 territory, loses context for cadence-trigger accumulation pattern matching.
- **Don't trust `truncated: true` markers as file corruption** — they're display artifacts of the 100K char safety limit. File is intact. `wc -c` confirms.

## Pair With

- V6/V7 pagination variants (for the canonical offset logic)
- V9 token-efficient variant (for sub-200KB files)
- `qa-agent-state-md-tail-blank-false-positive.md` (for the tail-empty-content false positive)
- `heartbeat-state-md-bloat.md` (for the >250KB compaction path)