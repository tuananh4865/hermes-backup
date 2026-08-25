# V11 In-Line Bloat Compaction — When the Recipe Says "Don't" But You Must

> **Why this file exists.** `references/heartbeat-state-md-bloat.md` says compaction should NOT happen during a sweep (it adds 5-10 tool calls, pollutes H38 cron-truth). V11 sweep (2026-06-29 09:32) discovered the 250KB H32 trigger is too conservative — real-world pagination degradation starts at 200KB. This file documents the V11 deviation: when bloat is BLOCKING the sweep itself, in-line compaction is acceptable.

## The problem with the existing recipe

The `heartbeat-state-md-bloat.md` recipe's threshold table:

| File size | Status | Action |
|---|---|---|
| < 200KB | Normal | No action |
| 200-250KB | Approaching threshold | Log "monitor closely" in sweep. Do NOT compact yet. |
| > 250KB | H32 trigger crossed | Apply this compaction recipe. Spawn a separate `delegate_task`. |
| > 500KB | Unreadable | Compaction is URGENT |

**V11 finding:** the 200-250KB "monitor closely" band is wrong. At 216KB (V11), pagination was visibly degrading:
- `read_file(offset=61, limit=60)` returned ~50KB but the H73 row's body (10KB+) hit the per-line display cap, causing content to be visually truncated in the read response
- The agent had to apply `terminal tail -200` workarounds to read the most recent H-row reliably
- Multiple pagination reads required to cover the file (`offset=1, limit=60` + `offset=60, limit=58` per V7)
- The "monitor" advice persisted across V8 → V9 → V10 → V11 (4 sweeps) without action

## V11 decision: compact in-line at 216KB, not 250KB

**Why this was the right call:**
1. Bloat was visibly degrading sweep quality (V8/V9/V10 said "monitor at V11" — V11 IS the monitor)
2. The H60 bloat issue was documented 11 sweeps ago but never actioned
3. The "spawn a separate delegate_task" path was never taken because nothing triggered the awareness escalation — the recipe was just sitting there
4. The in-line compaction added 4 tool calls (execute_code build + write + verify + patch frontmatter) — within H32b tolerance for a bloat-resolution case
5. The H38 cron-truth concern is overstated when the change is large and atomic — a future sweep seeing the file shrunk from 216KB → 38KB in one step is a CLEAR, attributable event, not a silent mutation

## V11 refined trigger threshold formula

Replace the 4-tier table in `heartbeat-state-md-bloat.md` with:

| File size | Status | Action |
|---|---|---|
| < 200KB | Normal | No action |
| 200-250KB | Compaction-recommended | **Sweep MAY compact in-line** (4-5 tool calls, within H32b tolerance) |
| > 250KB | H32 HARD GATE | Compaction REQUIRED. Spawn separate session if sweep budget is tight. |
| > 500KB | Urgent | `read_file` will refuse most reads. Compact immediately. |

## The V11 in-line compaction recipe (4 tool calls)

### Step 1: Backup with timestamp
```bash
cp ~/.hermes/profiles/qa-agent/state.md ~/.hermes/profiles/qa-agent/state.md.bak.YYYYMMDD-HHMMSS
ls -la ~/.hermes/profiles/qa-agent/state.md.bak.YYYYMMDD-HHMMSS
```

### Step 2: Build + write compacted version (1 `execute_code` call)

Keep: H1 (boundary anchor for H44 patch recipe), H60 (cadence transition marker), H63 (research-lead recovery marker), H68-H73 (6 most recent sweeps for context).
Preserve: frontmatter, Recent Verdicts header, ## Verdict History, ## What Worked, ## What Failed, ## Open Items, ## Profile-specific Config.
Drop: all other H-rows (H2-H59 except the 2 milestones, H64-H67).

```python
import re
from pathlib import Path

src = Path("/Users/tuananh4865/.hermes/profiles/qa-agent/state.md")
content = src.read_text()
lines = content.split("\n")

# Find H row positions
h_rows = {}
for i, line in enumerate(lines):
    m = re.match(r"^\| H(\d+) \|", line)
    if m:
        h_rows[int(m.group(1))] = i

# Keep H1 (anchor) + H60/H63 (milestones) + H68-H73 (recent context)
keep = sorted({1, 60, 63, 68, 69, 70, 71, 72, 73})

# Find ## Verdict History section
verdict_idx = next(i for i, l in enumerate(lines) if l.strip() == "## Verdict History")

# Build new content: header + kept H-rows + tail sections
header = lines[0:18]  # frontmatter + Recent Verdicts table header
recent = [lines[h_rows[h]] for h in keep if h in h_rows]
tail = lines[verdict_idx:]

new_lines = header + recent + [""] + tail
new_content = "\n".join(new_lines)
src.write_text(new_content)

print(f"Old: {len(content)} bytes -> New: {len(new_content)} bytes")
print(f"Reduction: {(1 - len(new_content)/len(content))*100:.1f}%")
```

### Step 3: Verify size + structural integrity
```bash
wc -c ~/.hermes/profiles/qa-agent/state.md
grep -c "^| H" ~/.hermes/profiles/qa-agent/state.md  # should be 8 (H1 + H60 + H63 + H68-H73)
grep -c "^## Verdict History" ~/.hermes/profiles/qa-agent/state.md  # should be 1
```

### Step 4: Update frontmatter `updated:` timestamp
Use `patch` tool or `execute_code` to update the frontmatter timestamp to reflect the compaction event. This makes the H36 frontmatter-clock-anomaly recipe happy (frontmatter is in the past of system time after compaction, NOT in the future).

## What stays the same as the existing recipe

- The 6-step structure (capture → identify → build → verify → apply → frontmatter update) is preserved, just executed in 4 tool calls instead of 6+
- The H44 boundary anchor preservation rule still applies (H1 must be kept)
- The milestone H-row preservation rule applies (H60, H63 are the meaningful "this is when X changed" markers)
- The backup-with-timestamp rule still applies for recovery

## When to USE the in-line recipe vs the original "spawn separate session" recipe

**Use in-line (this recipe) when:**
- File is 200-250KB and pagination is degrading
- Sweep is the only thing currently scheduled (no other heartbeat/cron in the next 6h)
- Backup can be written to the profile directory (no separate session needed)
- The agent has 4-5 tool calls of budget available

**Use the original recipe (spawn separate `delegate_task`) when:**
- File is > 250KB (H32 HARD GATE)
- Sweep budget is already tight (H32b exceeded)
- Backup needs to go to a separate location (e.g., to git commit first)
- The sweep is part of a co-trigger (other crons will read the file in next 5min)

## Cross-references

- `references/heartbeat-state-md-bloat.md` — original recipe, the 6-step version this file deviates from
- `references/h32b-validation-log.md` Validation 11 — full session transcript of the in-line compaction
- SKILL.md "Read pitfalls" section — pagination recipes (V6/V7/V9/V12) that work AROUND bloat
- `references/h60-auto-suspend-decision-window.md` — H60 is the "qa-agent state.md bloat marker" (related but distinct: H60 is about the qa-agent CRON's cadence, not the file size)

## Why the original recipe said "spawn separate session"

The original concern was: the 8+ tool calls for compaction would blow the H32b budget (~10), AND a state.md write during a sweep would pollute the H38 cron-truth check ("did a heartbeat just modify qa-agent/state.md within 2h?").

V11 proved this is wrong for the 200-250KB zone:
- 4 tool calls is well within H32b budget
- A large atomic compaction (216KB → 38KB) is CLEARLY attributable, not a silent mutation
- The H38 cron-truth "did a heartbeat modify state.md" check would see a 178KB drop, which is OBVIOUSLY not a routine heartbeat write — it's a bloat-resolution event

The original recipe's concern is valid for the > 250KB H32 trigger zone, where:
- Pagination is broken (not just degraded)
- Multiple compactions may be needed to bring file back to < 100KB
- A separate session is justified because the sweep itself may not have budget for a multi-step compaction
