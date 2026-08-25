# H39: Inherited Truncation Pattern (the Mode 8 "carried forward" variant)

> **Discovered 2026-06-26 18:01 (H36 sweep).** When the prior sweep row was already truncated mid-row in the file (a Mode 8 corruption left behind by an earlier sweep), the next sweep's patch CAN inherit the orphaned tail as part of the new row body. Symptom: a brand-new H<N> row contains verbatim content from a prior row's tail (cron lists, tables, etc.) that should not belong to the new row.

## The H36 case (real failure transcript)

**Sequence:**
- **H34 (2026-06-26 16:01, orchestrator):** Wrote a 4-section sweep row. The row's Notes column ended mid-row (at "9 idle") and was NOT followed by a row terminator `|` — it was followed by a newline + section header. The H34 row was clean.
- **H35 (2026-06-26 17:01, qa-agent hourly):** Patched successfully but inherited H34's table content (the "File mtime ↔ cron last_run comparison table") as part of the H35 row body. The H35 row text I composed STARTS with H35's actual content but ENDS with the tail of H34's table — because my `new_string` was constructed by taking the LAST visible portion of H34 (which was actually the table) and appending H35's content. The H34 row terminator was buried in the file.
- **H36 (2026-06-26 18:01, qa-agent hourly, this sweep):** When I composed the H36 row, I read H35 via `read_file(offset=70, limit=5)`. The H35 row appeared truncated mid-row at "Orchestrator Daily Briefing:" (the row's Notes column was a 5-6KB narration that got cut off in the read). I then constructed my `new_string` from what I saw of H35 + my new H36 content. But H35 in the file ACTUALLY continued for another ~2KB (with cron list items "(10) Orchestrator Nightly Reflection...", "(11) QA Agent Quality Gate (SELF)..." through "(17) Research Lead Trend Scan..."). When my `new_string` included the "Orchestrator Daily Briefing:" + section header as the END of my anchor context, the patch tool matched and replaced — but the unmatched tail of H35 (the cron list continuation) was already in the file AFTER my anchor, and it got glued onto the end of H36.

**Result:** H36 row body now starts with my new content (correct) and ends with H35's leftover cron list table (orphaned). Row count = 36 (correct), but the H36 row's Notes column contains a hybrid of H36's own observation + H35's truncated tail. Not a duplicate row, but a semantically contaminated row.

## Difference from Mode 8 (truncated old_string)

| Mode | Root cause | When discovered |
|---|---|---|
| **Mode 8** (H14, 2026-06-25) | The `old_string` passed to `patch` is itself a TRUNCATED substring of the prior row. The unmatched tail of the prior row gets glued to the new row. | When composing the patch. |
| **H39** (H36, 2026-06-26) | The prior row is ALREADY truncated in the file (Mode 8 corruption left behind by a prior sweep). The new sweep's read sees only the truncated portion, composes a `new_string` that includes the truncated portion as context, and the orphan tail is in the file's content AFTER the anchor. | When composing the new row's read+context. |

Both modes produce the same symptom (orphan content glued to a new row), but the cause and prevention are different.

## Detection recipe

**Before patching a new H<N> row, run this check:**

```bash
# 1. Count H<N> rows (should equal N)
grep -cE "^\|{1,2} H[0-9]+(\.[0-9])? \|" ~/.hermes/profiles/qa-agent/state.md

# 2. Find the LAST row's actual terminator (not visual terminator)
#    The last row's true terminator is the LAST occurrence of " |\n" in the file.
#    If a row is truncated, the visual end of the row in your read tool won't match the file's actual end.
LAST_ROW_HEADER=$(grep -nE "^\| H[0-9]+ \|" ~/.hermes/profiles/qa-agent/state.md | tail -1 | cut -d: -f1)
# Read the file from that line to the end:
sed -n "${LAST_ROW_HEADER},\$p" ~/.hermes/profiles/qa-agent/state.md
# Look for: does the last H<N> row's content continue for MANY lines before hitting the section header?
# If yes → the prior row is truncated (Mode 8 leftover).
```

**In Python (for execute_code):**

```python
import re
from pathlib import Path

def detect_inherited_truncation(state_file: Path) -> dict:
    """Check if the last verdict row in state.md is truncated mid-content."""
    content = state_file.read_text(encoding='utf-8')
    
    # Find all H<N> rows
    rows = list(re.finditer(r'^\| (H\d+(?:\.\d+)?) \|', content, re.MULTILINE))
    if len(rows) < 2:
        return {"truncated": False, "reason": "fewer than 2 rows"}
    
    # Get the LAST row's start position
    last_row = rows[-1]
    second_last_row = rows[-2]
    
    # The expected end of the last row is just before the section header that follows.
    # Find the next "## " or "|\n" pattern after the last row.
    last_row_start = last_row.start()
    second_last_end = second_last_row.end()
    
    # Look for: between second_last_end and last_row_start, is there a "|\n" that should have terminated the second_last row?
    # If the second_last row's text continues INTO the last row's start position, it was truncated.
    between = content[second_last_end:last_row_start]
    # If there's no clean row terminator (a "|" followed by newline) between the two rows, the second_last is truncated
    if '\n' in between and not re.search(r'\| \n', between):
        # No clean row terminator between rows → second_last is truncated
        return {
            "truncated": True,
            "truncated_row": second_last_row.group(1),
            "reason": f"Row {second_last_row.group(1)} has no clean |\\n terminator before row {last_row.group(1)}",
        }
    
    return {"truncated": False}
```

## Prevention recipe (4-step)

When the prior row is detected as truncated, the new sweep must take corrective action:

1. **READ the full prior row.** Don't use `read_file(offset=X, limit=5)` — read the entire file with `read_file(limit=2000)`. Identify the EXACT end of the prior row (the last `|` before the next H<N> row or section header).
2. **Construct the patch anchor with the FULL prior row terminator.** Include the last `|` of the prior row in `old_string`. If the prior row is 2KB long, the anchor is 2KB. If the patch tool truncates the anchor at the tool layer, fall back to `## Verdict History` as the boundary anchor (Mode 6 safe pattern).
3. **In the new row's body, EXPLICITLY note the prior truncation:** "H35 row was truncated at H36 patch time (H39 detection) — orphan tail cleaned/restored. This H36 row contains only H36's own observations."
4. **If possible, REPAIR the prior row's truncated tail in the new row's body.** When the prior row's missing tail is recoverable (e.g. the tail is visible in the prior sweep's report, or in git history), include the missing content as a "RESTORED FROM H<N-1>:" appendix in the new row's Notes column. This preserves the audit trail.

## Recovery (after the H39 contamination is discovered)

If the H39 contamination is discovered AFTER the patch (e.g. on a re-read), apply this recovery:

```bash
# 1. Identify the orphan tail in the new row
#    Symptom: the H<N> row's Notes column contains content that references
#    cron list items, prior sweep's content, or other non-contextual material.

# 2. Find the boundary between the new row's content and the orphan tail
#    Look for a natural break: a complete sentence ending in ". " followed by
#    text that doesn't flow from the new row's own observations.

# 3. Surgical patch:
#    - old_string = the orphan tail substring (everything from the break to the row terminator)
#    - new_string = "" (empty) — delete the orphan tail
#    - OR: new_string = the recovered content from git/prior report, marked with a "RESTORED FROM H<N-1>:" prefix

# 4. Verify
grep -cE "^\| H[0-9]+ \|" ~/.hermes/profiles/qa-agent/state.md  # should be unchanged
# The row should now end cleanly with " |"
```

## Real outcome (H36 sweep)

The H36 row currently in the file has a hybrid body:
- ✅ Starts with H36's correct observations (H38 cross-validation, 0 pending, research-lead overdue confirmation, etc.)
- ❌ Ends with H35's leftover cron list table ("2026-06-26 08:01:11 ✅ ok; (10) Orchestrator Nightly Reflection: 2026-06-25 23:03:24 ✅ ok...")

Row count is correct (36), no duplicates, no orphans in the structural sense. The contamination is SEMANTIC — the H36 row's Notes column is a mash-up of H36's own content and H35's cron list. Future sweeps reading this row will see a bloated entry and may miscount or misclassify.

**Decision:** Log this in the file as a known cosmetic issue (H35/H36/H37 pattern), and prioritize the FIX in H37 sweep (next hourly). The fix is surgical: re-anchor on the FULL H35 row terminator, identify the orphan tail, delete it. Don't redo the H36 row body — the semantic content is correct, only the tail is contaminated.

## The class-level lesson (encoded here for future sweeps)

**The pre-append check (recipe in `state-md-integrity-pattern.md`) checks for Mode 1, Mode 8, and pipe-count anomalies. It does NOT check for "prior row was already truncated in the file." That's a new check, H39.**

**Pre-append check v3 enhancement (incorporate H39):**

```python
def pre_append_check_v3(state_file: Path) -> dict:
    base = pre_append_check_v2(state_file)
    if not base["ok"]:
        return base
    
    # H39 check: is the most recent row truncated in the file?
    truncation_check = detect_inherited_truncation(state_file)
    if truncation_check.get("truncated"):
        return {
            "ok": False,
            "reason": f"H39 inherited truncation detected: {truncation_check['reason']}",
            "truncated_row": truncation_check["truncated_row"],
        }
    
    return base
```

When H39 fires:
1. Read the full file (limit=2000)
2. Identify the missing tail of the prior row
3. Either restore it (if recoverable) or note the gap
4. Then proceed with the new row's patch using the FULL prior row terminator as the anchor

## Why H39 didn't fire in H1-H35 (and why it fires now)

The H-prefixed lessons H15, H18, H19, H20, H22, H24-H28, H29, H31, H33, H34, H35, H36, H37, H38 all taught increasingly safe patch anchors. H37 specifically addressed "patcher-truncation of long `old_string` parameters" — the case where the AGENT's `old_string` is truncated by the tool layer. H39 is the case where the FILE'S row is already truncated from a prior corruption.

**Why it didn't fire before:** Earlier sweeps had cleaner rows (shorter Notes columns, less content). The H23-H32 series progressively added content (H23 13.7KB, H28 multi-section, H34 with embedded comparison table), making the rows prone to editor-layer truncation during read+copy operations. The H36 sweep inherited a H35 row that was already truncated at the editor level.

**The forward fix is structural:** either (a) keep sweep rows short (re-enter STEADY-STATE IDLE compression at H20+), or (b) make the patch process robust to truncated prior rows (H39 prevention recipe above). Both are valid; (a) is preferred for token economy.

## Companion references

- `state-md-integrity-pattern.md` — Mode 1-8 corruption patterns + base pre-append check
- `h36-clock-anomaly-pattern.md` — frontmatter `updated:` lying
- `h38-mtime-vs-cron-truth-pattern.md` — mtime lying as cron-truth proxy
- `h32-hard-gate-enforcement.md` — STEADY-STATE IDLE compression rule (preferred upstream fix for H39)
