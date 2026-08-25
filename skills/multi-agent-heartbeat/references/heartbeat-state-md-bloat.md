# qa-agent state.md Bloat — Compaction Recipe

> **Why this file exists.** The qa-agent `state.md` accumulates H-sweep rows on every cron-driven sweep. At 1 row per hour (pre-H60) or 1 row per 6h (post-H60), with each row averaging 3-10KB of text, the file grows ~16-100KB/day. Without intervention, it crosses the `read_file` 100K char safety limit (~110KB-130KB), the 250KB H32 trigger threshold, and eventually the 500KB "unreadable" boundary. Compaction is a separate operation from the sweep itself — it should NOT be performed in-line during a sweep (it adds 5-10 tool calls, blowing the H32b budget of ~10).

## When to trigger compaction

| File size | Status | Action |
|---|---|---|
| < 200KB | Normal | No action. Sweep continues normally. |
| 200-250KB | **Compaction-recommended** (V11 update) | Sweep MAY compact in-line (4-5 tool calls, within H32b tolerance). See `references/v11-in-line-bloat-compaction.md`. |
| > 250KB | H32 trigger crossed | Apply this compaction recipe. Spawn a separate `delegate_task` to compact. |
| > 500KB | Unreadable | Compaction is URGENT — `read_file` will refuse most reads. Compact immediately. |

**V11 update (2026-06-29):** the original 4-tier table had "200-250KB = monitor closely, do NOT compact". V11 sweep discovered that the practical pagination degradation starts at 200KB, not 250KB. The new "compaction-recommended" band at 200-250KB allows the sweep to compact in-line when the bloat is actively blocking the sweep. See `references/v11-in-line-bloat-compaction.md` for the in-line recipe and decision criteria.

**H32 trigger formula:** `wc -c ~/.hermes/profiles/qa-agent/state.md` should be checked once per sweep. If > 250000 bytes, trigger.

## Why the H32 trigger is 250KB and not the read_file limit (~110KB)

- The `read_file` 100K char safety limit means reads fail at ~110KB-130KB (depends on row density)
- The H32 HARD GATE threshold was set at 250KB to give buffer for the V6/V7 pagination recipes (`offset=1, limit=60` + `offset=60, limit=58` = ~118 lines ≈ 100KB)
- The 250KB threshold = roughly 2x the safety limit, giving buffer for: (a) one more H-row write before pagination breaks, (b) any emergency investigation read, (c) the row that triggers compaction itself can be written

## Compaction recipe (run in a SEPARATE session, NOT during sweep)

### Step 1: Capture what MUST be preserved

```bash
# Frontmatter (always preserve)
head -8 ~/.hermes/profiles/qa-agent/state.md

# Recent H-rows (last 20-30, ~3-4KB each = ~60-120KB)
grep -n "^| H[0-9]" ~/.hermes/profiles/qa-agent/state.md | tail -30

# Structural sections (always preserve)
grep -n "^## " ~/.hermes/profiles/qa-agent/state.md
```

### Step 2: Identify rows to drop

- **Keep:** H-rows from the last 20-30 sweeps (chronological most-recent)
- **Drop:** All older H-rows (H1 through H_N-30, where N is the current H-number)
- **Keep:** Frontmatter, Current Goal section, Active/Pending/Blocked Tasks tables (even if empty), Recent Verdicts table header, Profile-specific Config, Routing Log
- **Keep:** Any open items, handoff history, work-in-progress notes

### Step 3: Build the compacted file

```bash
# Extract the parts to keep
python3 << 'EOF'
import re
from pathlib import Path

src = Path.home() / ".hermes/profiles/qa-agent/state.md"
content = src.read_text()

# Split into structural sections and H-row table
sections = []
h_rows = []
in_h_table = False

for line in content.split("\n"):
    if line.startswith("## Verdict History"):
        in_h_table = True
        sections.append(line)
        continue
    if in_h_table:
        if line.startswith("| H"):
            h_rows.append(line)
        elif line.startswith("|---"):
            sections.append(line)  # keep table separator
        elif line.startswith("## "):
            # Next section — exit H-table mode
            in_h_table = False
            sections.extend(h_rows[-30:])  # keep last 30 H-rows
            sections.append("")  # blank line
            sections.append(line)
        else:
            # End of H-table (e.g., blank line, Profile-specific Config)
            in_h_table = False
            sections.extend(h_rows[-30:])  # keep last 30 H-rows
            sections.append("")
            sections.append(line)
    else:
        sections.append(line)

# Write compacted version
Path("/tmp/qa-agent-state-compacted.md").write_text("\n".join(sections))
print(f"Compacted: {src.stat().st_size} bytes → /tmp/qa-agent-state-compacted.md")
EOF
```

### Step 4: Verify the compacted file

```bash
# Check size reduction
wc -c /tmp/qa-agent-state-compacted.md ~/.hermes/profiles/qa-agent/state.md

# Check structural integrity
grep -c "^## " /tmp/qa-agent-state-compacted.md  # should match structural sections preserved
grep -c "^| H" /tmp/qa-agent-state-compacted.md   # should be ~30

# Check frontmatter
head -10 /tmp/qa-agent-state-compacted.md
```

### Step 5: Apply the compacted file (DESTRUCTIVE — confirm with backup first)

```bash
# Backup current file (in case compaction breaks something)
cp ~/.hermes/profiles/qa-agent/state.md ~/.hermes/backups/qa-agent-state-pre-compact-$(date +%Y%m%d-%H%M%S).md

# Replace with compacted version
cp /tmp/qa-agent-state-compacted.md ~/.hermes/profiles/qa-agent/state.md

# Verify
wc -c ~/.hermes/profiles/qa-agent/state.md
# Should be ~50-100KB (down from 250KB+)
```

### Step 6: Update the frontmatter `updated` field

```bash
# Update the frontmatter to reflect compaction timestamp
python3 -c "
from pathlib import Path
import datetime
src = Path.home() / '.hermes/profiles/qa-agent/state.md'
content = src.read_text()
new_ts = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+07:00')
content = content.replace(
    'updated:', f'compacted_at: {new_ts}\nupdated:', 1
)
src.write_text(content)
"
```

## Why compaction must NOT happen during a sweep

The H32b HARD GATE budget is ~10 tool calls per sweep. Compaction requires:
1. `wc -c` to check size
2. `read_file` (paginated) to capture current content
3. `python3` heredoc to build compacted version
4. `wc -c` to verify reduction
5. `cp` to backup
6. `cp` to apply
7. Frontmatter update
8. Verification

That's 8+ tool calls just for compaction — almost the entire sweep budget. And it produces a side effect (qa-agent/state.md rewrite) that pollutes the H38 cron-truth check ("did a heartbeat just modify qa-agent/state.md within 2h?" → YES, this sweep, by compaction → false-positive cron fault detection).

**Solution:** when compaction is needed, the sweep itself emits a "compaction-needed" flag in its response. The flag triggers a SEPARATE `delegate_task` (or scheduled cleanup) that runs the recipe above. The sweep continues at normal tool-call budget; compaction happens later in isolation.

## Compaction frequency (estimated)

With qa-agent cron on `0 */6 * * *` (post-H60 option b) and each H-row averaging ~3KB:
- 4 rows/day × 3KB = 12KB/day growth
- 200KB → 250KB in ~4 days
- Compaction needed ~once per week on healthy cadence

Before H60 option b was applied (qa-agent hourly), growth was ~24KB/day = compaction needed every 4 days. The cadence reduction was a major improvement; weekly compaction is sustainable.

## Historical precedent

- **2026-06-28:** file at 211KB-212KB (V8-V9 territory). V8 said "monitor closely at V9", V9 said "monitor at V10". This file was created at V10 (2026-06-28 21:01) BEFORE 250KB threshold was crossed, so no compaction needed yet.
- **Compaction will be triggered when file crosses 250KB.** At current growth rate (~10KB/week with H32b HARD GATE holding), that's expected in ~4 weeks.

## Cross-references

- `references/qa-agent-state-md-tail-blank-false-positive.md` — read failure modes that the compaction fixes
- `references/h32-hard-gate-enforcement.md` — the H32 trigger that requires this compaction recipe
- `references/h32b-validation-log.md` — V7 noted "if file >210KB, apply compaction recipe" — this file is the answer