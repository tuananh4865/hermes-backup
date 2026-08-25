---
name: state-md-editing-pitfalls
description: "Pitfalls when editing profile state.md files (operations-manager, qa-agent, etc.) during routing audits. Anchor uniqueness, patch tool pagination warning, large file refusal workarounds. Load when a routing audit or heartbeat needs to write/edit state.md."
---

# state.md Editing Pitfalls

**Class:** Operations Manager / QA Agent (state.md writers) — **plus any large wiki/entity/cron file edited with patch()**
**Codified:** 2026-06-28 (12:00 routing audit). Generalized 2026-06-30 to cover large non-state.md files (entity files >50KB, cron state files).
**Status:** ACTIVE — every state.md AND large-entity-file edit hits these traps

## Why this exists

Profile `state.md` files accumulate audit summary blocks + verdict rows over weeks. When you try to INSERT a new block or ROW, naive anchor strings collide with existing content. The patch tool either refuses (ambiguous match) or silently writes the wrong location. This reference codifies the anchor-uniqueness recipe + the patch tool's hidden pagination warning.

## Pitfall 1: Repeated "H50 PRE-FIRE" / "Verdict" lines cause 7+ match collisions

**Symptom:** `patch()` returns `Found 7 matches for old_string. Provide more context to make unique, or use replace_all=True.`

**Root cause:** Operations-manager state.md has 6+ identical "## Audit Summary — 2026-06-27/28 HH:MM" headers and each ends with similar verdict lines like `**H50 PRE-FIRE:** Operations Manager (this cron, ...`. A single-line anchor matches all of them.

**Fix:** Use a **multi-line context anchor** that includes the line BEFORE the target + blank line + the new section header. Example for inserting a new audit summary BEFORE the most recent:

```python
# ❌ 7-match collision:
old_string = "**H50 PRE-FIRE:** Operations Manager (this cron, 06:00 — pre-realized by THIS audit) + 12:00 next tick. Orchestrator Heartbeat off-hours until 08:00 ✅.\n\n## Audit Summary — 2026-06-28 00:00 (cron 6h, on-cadence ✅)"

# ✅ Unique multi-line anchor — include the SPECIFIC time that distinguishes the
# block, and the line BEFORE the target:
old_string = "**H50 PRE-FIRE:** Operations Manager (this cron, 06:00 — pre-realized by THIS audit) + 12:00 next tick. Orchestrator Heartbeat off-hours until 08:00 ✅.\n\n## Audit Summary — 2026-06-28 00:00 (cron 6h, on-cadence ✅)"
new_string = """**H50 PRE-FIRE:** Operations Manager (this cron, 06:00 — pre-realized by THIS audit) + 12:00 next tick. Orchestrator Heartbeat off-hours until 08:00 ✅.

## Audit Summary — 2026-06-28 12:00 (cron 6h, on-cadence ✅)
<new block here>

## Audit Summary — 2026-06-28 00:00 (cron 6h, on-cadence ✅)"""
```

**General rule:** anchor must include ONE fully-distinctive line (e.g., the specific timestamp like `06:00` vs `12:00`). If a single timestamp appears in 6+ places, use 2-3 lines of context to disambiguate.

**Alternative: use a directional anchor.** If you're inserting ABOVE a section, your anchor should END with the section header (not just text). If replacing a block, your anchor should include both opening AND closing context.

## Pitfall 2: `patch()` warns about offset/limit pagination when state.md was last read with pagination

**Symptom (post-patch warning):**
```
_warning: /path/to/state.md was last read with offset/limit pagination
(partial view). Re-read the whole file before overwriting it.
```

**Scope:** This warning fires for ANY file edited with patch() after a paginated read_file, not just state.md. Confirmed on `wiki/entities/learned-about-tuananh.md` (92KB, patched 2026-06-30 evening trend scan cron) and `wiki/cron/evening-trend-scan-state.md` (3KB but still triggered after paginated read). The pattern is the patch tool's local cache, not the file type.

**What it means:** You previously read the file with `offset=N, limit=M` (paginated), so the patch tool's local cache only has that partial view. Your patch may collide with content you haven't seen.

**What to do:**
1. **Don't ignore the warning** — the patch may have written to a stale anchor and the file is now inconsistent.
2. **Verify** with `grep` or `tail` to confirm the new content is in the right place.
3. **For subsequent patches**, re-read the relevant section before patching again.
4. **For entity files specifically (the evening trend scan target):** after patching, run `grep -n "^## " <file>` to verify section headers are still in chronological order. A real bug pattern (hit 2026-06-30): the patch inserts a new section between a prior section's HEADER and its BODY, leaving the body as an orphan list floating below the new section. The data is preserved, but the file structure is now confusing.

**Prevention:** When planning multiple sequential edits to a state.md OR entity file, do a `read_file` with no offset/limit (or large enough limit) FIRST so the patch tool has full context. Even if the file is 100KB+, the patch tool's safety check is different from read_file's 100K refusal.

## Pitfall 3: `read_file` refuses files >100K bytes with 117 lines

**Symptom:** `Read produced N characters which exceeds the safety limit (100,000 chars). Use offset and limit to read a smaller range. The file has 117 lines total, file_size: 195660`

**What it means:** qa-agent/state.md hit 195,660 bytes. `read_file` won't open it fully.

**Fix:** See `references/state-md-bloat-detection.md` for full recipe. Quick reference:

```bash
# Get the latest H rows only
grep -E '^\| H[0-9]+ \|' ~/.hermes/profiles/qa-agent/state.md | tail -5

# Or: last 120 lines
tail -120 ~/.hermes/profiles/qa-agent/state.md
```

**Before any `read_file` on a state.md, do a size check:**

```bash
stat -f "%z  %N" /Users/tuananh4865/.hermes/profiles/*/state.md | sort -rn
```

If the largest is >100K, skip read_file and go straight to grep/tail.

### Pitfall 4 (CORRECTED 2026-06-29): Inserting audit summary blocks — APPEND-AT-END is the actual convention

**The original recipe was wrong.** Operations-manager state.md does NOT prepend new audit summaries at the top — it APPENDS them at the bottom in a paired structure. This was verified across 7+ recent audits (12:00, 06:00, 00:00, 18:00, 12:00, 06:00, 00:00 entries from 2026-06-27/28/29).

**Actual convention:**
- A `## Routing Log (continued N)` block is APPENDED to the bottom of the file, with the previous-most-recent routing log entry as the anchor.
- A `## Audit Summary — <newest>` block immediately follows, also at the bottom.
- The number N increments (`continued`, `continued 2`, `continued 3`, ...) as the file grows. Each "Routing Log" header is itself appended — there is no central Routing Log section that the new entry gets inserted into.

**Recipe for state.md update (corrected 4-step):**
1. `read_file(path, offset=<last-10-lines>, limit=10)` — confirm exact last line as the anchor
2. `patch()` — APPEND new `## Routing Log (continued N)` + `## Audit Summary — <newest>` at the END of file. Anchor = last 1-2 lines of the previous-most-recent Audit Summary verdict (the trailing `**Sustained recovery update:** ...` line is usually unique per audit because it cites the specific sweep count).
3. `patch()` — UPDATE frontmatter `updated: YYYY-MM-DDTHH:MM:SS+07:00` + `goal: 6h routing audit (cron YYYY-MM-DD HH:MM)`
4. `stat -f "%Sm %z %N" <file>` — verify mtime updated + size grew

**Why the original "PREPEND" recipe fails in practice:**
- The previous-most-recent Audit Summary at the TOP of the section is the OLDEST, not the newest — inserting above it would bury the most recent.
- The Routing Log section has multiple `## Routing Log` / `## Routing Log (continued N)` headers stacked vertically (line 32, 182, 216, ...). Anchoring "before the most recent" requires knowing which `## Routing Log (continued N)` is the current one — fragile.
- Anchor uniqueness: the "most recent" verdict line has many cousins (similar H50 PRE-FIRE structure across 5+ prior audits) → 7+ match collision per Pitfall 1.

**The tail-anchor strategy sidesteps ALL of these.** Last verdict line of file is unique because it cites the specific sweep count (e.g., "16 sweeps sustained"). Anchor there, append after, done.

**Pitfall 4a (NEW 2026-06-29): The "end-of-file tail-anchor" pattern for 50KB+ state.md**

When patching a 50KB+ state.md file, the `patch()` tool returns this warning on every call:
```
_warning: /path/to/state.md was last read with offset/limit pagination
(partial view). Re-read the whole file before overwriting it.
```

This warning is **INFORMATIONAL, not blocking**. The patch still succeeds as long as:
- Your `old_string` is the actual last line of the file (verify with `terminal(command="tail -3 <file>")` or `read_file(offset=<last-10>, limit=10)` BEFORE patching)
- Your `old_string` is unique in the file (tail-anchor lines are usually unique because they cite specific sweep counts like "17 sweeps sustained", "H74 sweep 6h ago", etc.)

**Recipe:**
```bash
# Step 1: Confirm exact last 3 lines
tail -3 ~/.hermes/profiles/operations-manager/state.md

# Step 2: Use the LAST unique line as your old_string anchor
# (e.g., the trailing "**Sustained recovery update:** ... sweep count ..." line)

# Step 3: patch() with that anchor
# The warning will fire but the patch will succeed.
```

**Why this is better than the original multi-line context approach (Pitfall 1):**
- Tail-anchor lines are naturally unique (sweep count + date + time).
- No 7-match collision risk.
- No need to read the full 50KB+ file (which would itself hit read_file's 100K char refusal per Pitfall 3).
- Works whether the file is 5KB or 200KB.

**Anti-pattern:** DO NOT trust the "warning: was last read with offset/limit" message to mean the patch is unsafe. The patch tool has its own local cache; the warning is asking you to re-read for SUBSEQUENT patches, not invalidating the current one. Verify with `tail -3` and continue.

## Pitfall 5: Frontmatter `updated` field timestamp drift vs file mtime

**Symptom:** Frontmatter says `updated: 2026-06-28T00:00:00+07:00` but file mtime is `Jun 28 06:01:17`.

**Root cause:** Frontmatter records the "intended audit run time" (the cron tick that fired this audit), NOT the actual file write time. A 6h audit's frontmatter says 00:00, 06:00, 12:00, or 18:00 — these are the cron tick times, even if the actual write happened 0-60s later.

**H36 lesson:** This is harmless cosmetic drift. Use file mtime for freshness calculations, frontmatter for "which audit tick this is". Do NOT auto-correct frontmatter to match file mtime — the cron-tick label is more meaningful.

## Pitfall 6: Sibling-collision with qa-agent's hourly gate

**The rule:** Don't write to `qa-agent/state.md` from a routing audit sweep. qa-agent's hourly gate writes via `patch()`. Concurrent writes to the same file cause data loss.

**Safe to write to:**
- `operations-manager/state.md` (this profile's own file)
- Other profiles' state.md IF the user explicitly requested it (e.g., the user said "update content-director state.md")

**UNSAFE to write to:**
- `qa-agent/state.md` — write-only by qa-agent's hourly gate
## Related

- `../SKILL.md` — main routing-audit skill
- `references/state-md-bloat-detection.md` — bloat detection (Pitfall 3 root cause)
- `references/cadence-decision-windows.md` — H50 + H60 + H51 (frontmatter timestamp drift context)
- `references/30min-heartbeat-pattern.md` — read-only sweep convention (Pitfall 6)

## Pitfall 7 (NEW 2026-06-30): Entity file "orphan list" bug when patching after paginated read

**Symptom (post-patch structural issue):** Entity file (e.g., `wiki/entities/learned-about-tuananh.md`) has a new dated section that was successfully inserted, BUT a previous section's BODY now appears as an "orphan list" floating between the new section and the next anchor — its section header is gone (or separated from its body), and the body is still there.

**Root cause:** When `patch()` is called on a file that was last read with `offset=N, limit=M` pagination, the patch tool's local cache is only the paginated view. If your `old_string` anchor is the LAST line of a section (or includes the section's closing line), the patch tool may insert the new content in the WRONG place — specifically, between the previous section's HEADER and its body, if the anchor's surrounding context in the cached view places it that way.

**Hit in production:** 2026-06-30 evening trend scan cron — patched `learned-about-tuananh.md` to add a "#### NEW June 30, 2026" section anchored to the previous run's "#### NEW June 28, 2026" header + first bullet. The patch tool inserted the new section BETWEEN the June 28 header and June 28's body, leaving the body as an orphan list below the new section. The data was preserved but the file structure is now visually broken (header gone, body dangling).

**Recipe to avoid (entity files >50KB):**
1. Before patching, run `grep -n "^## \|^#### " <file>` to map all section headers and confirm the structure
2. Pick an anchor that includes the SECTION-CLOSING line of the prior section, not just the section header. Section-closing lines are usually `**Opportunities cho Tuấn Anh (DD/MM):**` or `**Recommend sounds cho kênh Setup/Edit/Ánh sáng:**` — they're naturally unique and unambiguous
3. After patching, run `grep -n "^## \|^#### " <file>` AGAIN to verify the section order is still correct
4. If an orphan list appears: don't try to fix with another patch (it'll just move the bug). Re-read the full file with `read_file(path, offset=1, limit=2000)` (large enough to span), then patch the orphan back into its original section

**Alternative for very large files (>100K):** switch to `write_file` for the FULL entity file rewrite. The file is 92KB as of 2026-06-30, still under write_file's tolerance, and full rewrites sidestep the anchor collision entirely. Cost: you have to read the whole file once with `read_file` (which itself hits the 100K refusal for >100K files — so this only works while the file is under 100K).

**General principle:** for any file that accumulates content over time (state.md, entity files, log files), prefer the **tail-anchor pattern** (Pitfall 4a) over the **header-anchor pattern**. Tail anchors are unique because they cite specific run details (sweep count, date, slang count). Header anchors are NOT unique because they all look like `## Audit Summary — YYYY-MM-DD HH:MM`.

---

## Quick reference: full state.md update sequence

```python
# Step 1: Read current state to identify anchor points
import subprocess
subprocess.run(["stat", "-f", "%Sm %z %N", 
    "/Users/tuananh4865/.hermes/profiles/operations-manager/state.md"])

# Step 2: Find the "previous most-recent audit" anchor
# Use grep to locate it precisely:
# grep -n "^## Audit Summary" ~/.hermes/profiles/operations-manager/state.md | head -3

# Step 3: patch() APPEND new audit summary at END of file
# Tail-anchor = last 1-2 lines of previous-most-recent Audit Summary verdict
# (typically the trailing "**Sustained recovery update:** ... sweep count ..." line)
# Use read_file(offset=last-10, limit=10) to confirm exact anchor BEFORE patching.

# Step 4: patch() APPEND new routing log entry ABOVE the new audit summary
# Use the same tail-anchor + insert the new routing log block first, audit summary second.

# Step 5: patch() UPDATE frontmatter
# Anchor = "updated: YYYY-MM-DDTHH:MM:SS+07:00"

# Step 6: Verify
subprocess.run(["stat", "-f", "%Sm %z %N",
    "/Users/tuananh4865/.hermes/profiles/operations-manager/state.md"])
```
