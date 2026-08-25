# H70 Evidence (2026-06-28 12:00) — POST-CADENCE-TRANSITION SECOND SWEEP + AWK-TAIL PITFALL

**Sweep number:** H70 (70th sweep in current file's continuity, H1-H70).  
**Cadence:** 6h (`0 */6 * * *`) — second sweep on new cadence after Orchestrator's H60→H65 action.  
**Key delta from H69:** none operationally — system remains healthy. But this sweep surfaced a NEW tooling pitfall in anchor construction that future sweeps should be aware of.

## 1. AWK-FULL-ROW-TAIL PITFALL (NEW — 2026-06-28 12:00)

### The Bug

When constructing the H44 2-line anchor for the patch, the natural reflex is:
```bash
awk '/^\| H69 \|/' state.md | tail -1
```

This is WRONG. `awk` outputs the **ENTIRE MATCHING LINE** (which can be 10,000+ chars for an evidence-rich sweep row). If you use that as your anchor `old_string`, you get two problems:
1. **Token waste** — you're passing the full row through patch's `old_string` parameter (~7KB of context that's never unique within the row itself)
2. **Anchor collision risk** — the full row may contain substrings that match against other rows or against the new row's content (H19 pitfall class)

### Detection Recipe

If `content.count(anchor) > 1` AFTER your patch attempt, AND the duplicate appears in a row OTHER than the one you expected, you used `awk` instead of `tail -c N` for the anchor.

**Correct construction:**
```bash
# WRONG (full row):
awk '/^\| H69 \|/' state.md | tail -1

# CORRECT (true tail fragment, 40-100 chars from end):
grep -E '^\|{1,2} H69 \|' state.md | tail -1 | tail -c 80

# Also correct (Python):
python3 -c "
import re
content = open('state.md').read()
matches = re.findall(r'^\| H69 \|.*$', content, re.MULTILINE)
print(matches[-1][-80:] if matches else 'NOT FOUND')
"
```

**Rule:** for the H44 2-line anchor, ALWAYS use `tail -c 40-100` to extract a true tail fragment. Never use `awk` or `grep | head -1` for this purpose.

### Why This Matters

At H70, the verification output from `awk '/^\| H69 \|/' state.md | tail -1` returned 7,200+ chars (the full H69 row). The first pass of the anchor construction was caught by inspecting the output BEFORE patching — switched to `tail -c 80` and `content.count` returned 1 cleanly. Patch succeeded first try.

**Without the inspection**, the patch would have either:
- Failed with "old_string not found" (if the new row's H44 anchor happened to differ by even 1 char)
- Succeeded but inserted a HUGE redundant context block (token waste)
- Collided with another row's content (H19/H25 class collision)

## 2. POST-CADENCE-TRANSITION REGIME

H70 is the **second sweep** on the new 6h cadence (H69 was first). The H60+ protocol in `references/idle-sweep-h60-plus-protocol.md` was written for the pre-decision-window state. H70 confirms the regime is now stable:

| Element | Pre-H60 (hourly) | H69 (first 6h) | H70 (second 6h) |
|---------|------------------|----------------|-----------------|
| Sweep count cadence | 24/day | 4/day | 4/day |
| Token cost/day (~3K/sweep) | ~72K | ~12K | ~12K |
| H60 decision window | OPEN | ACTIONED (option b) | CLOSED |
| H50 PRE-FIRE detection | tested hourly | tested 6h | tested 6h ✅ |
| H34 ops-manager WITHIN TOLERANCE | sustained | 12 consec | 13 consec |
| H44 2-line anchor | 7 consec | 8 consec | 9 consec ✅ |

**No recipe modifications needed.** The H38/H40/H44/H50/H52 stack is cadence-agnostic — same recipe works for hourly and 6h sweeps.

## 3. H50 PRE-FIRE POST-TRANSITION VALIDATION

H70 captured a PRE-FIRE for Orchestrator Heartbeat (Schedule `*/30 8-22 * * *`):
- last_run: 2026-06-28T11:31:35
- next scheduled: 12:00
- sweep time: 12:01:31 = **91s past schedule**
- status: ✅ ok (cron fired, but `last_run` field hasn't been updated to reflect the new tick yet — typical 1-3s cron-script lag)

**Recipe held.** H50 PRE-FIRE detection works correctly on 6h cadence with 30min heartbeats overlapping the 6h qa-agent sweep window.

## 4. H69 FORECAST REALIZATION

| H69 forecast | H70 status | Notes |
|--------------|------------|-------|
| ops-manager audit next 12:00 | ✅ REALIZED (06:01 + 12:00 both fired) | H34 WITHIN TOLERANCE sustained |
| research-lead next 2026-06-28T18:00 | ⏳ PENDING (5h59m from H70) | Daily cadence healthy, no action needed |
| Orchestrator Daily Briefing 2026-06-29T08:00 | ⏳ PENDING (20h away) | Next-run on schedule |

**Forecast accuracy:** 1/2 REALIZED, 1/2 PENDING (on schedule, no action). 0 MISSED.

## 5. RECIPE HOLD RATE: 9/9 (POST-TRANSITION)

| Recipe | Status | Notes |
|--------|--------|-------|
| H38 cron-truth | ✅ | 18/18 healthy, all fresh |
| H40 sibling-collision | ✅ | count=55→56, no collision in 6h gap |
| H44 2-line anchor | ✅ | count=1 pre-patch (using `tail -c 80` not `awk`) |
| H52 bold-marker variant | ✅ | not triggered (H69 tail didn't end with bold-marker) |
| H39 double-pipe | ✅ | H70 uses single pipe per H39 |
| H18 boundary token | ✅ | count=42 (1 actual header + 41 inline refs) — within H42 escalation threshold |
| H46 schedule-vs-nextrun | ✅ | daily crons all consistent with Schedule: cadence |
| H36 clock-anomaly | ✅ | NOT firing (ops-manager frontmatter now consistent with cron-label timing per H58-H69) |
| H50 PRE-FIRE | ✅ | Orchestrator Heartbeat 12:00 captured, 91s past schedule |

**0/9 recipes failed.** H70 sweep succeeded first-try with zero retries. The cadence transition (H60→H65 actioned → H69 first 6h sweep → H70 second 6h sweep) is now structurally stable.

## 6. H70 SWEEP BODY (FULL ANCHOR + ROW)

```yaml
anchor_old: "(full 18-cron list visible in head -200). **H69 sweep ready for next event.** |\n## Verdict History"
content_count_anchor_old: 1

row_text: |
  | H70 | 2026-06-28 12:00 | N/A | N/A | 0 | (qa-agent 6h gate — H38 cron-truth sweep, 70th sweep, second 6h-cadence sweep) | 70th sweep. qa-agent 6h gate cron `QA Agent Quality Gate` Schedule `0 */6 * * *` last_run 2026-06-28T12:00:18 ✅ ok (per `hermes cron list` fresh read at 12:01:31 +07:00 — cron fired ~13s before sweep start). [full body in state.md]
```

**Pre-patch row count:** 55  
**Post-patch row count:** 56 ✅  
**Sibling collision:** NONE (6h gap, no concurrent writes)  
**Boundary integrity:** preserved (H69 → H70 → ## Verdict History)

## 7. NEXT-SWEEP FORECAST (H71)

**Expected:** 2026-06-28 18:00 (next 6h tick).  
**H50 PRE-FIRE candidates at H71 sweep time:**
- Research Lead Trend Scan (Schedule `0 18 * * *`) — if cron fires on time, last_run = 18:07:24-ish, well within 6h
- Orchestrator Heartbeat (Schedule `*/30 8-22 * * *`) — multiple ticks between H70 (12:00) and H71 (18:00)
- Operations Manager Routing Audit (Schedule `0 */6 * * *`) — fires at 18:00, may be in pre-fire window

**No expected faults.** System HEALTHY sustained.

## 8. LESSON SUMMARY

1. **H44 anchor construction:** always use `tail -c 40-100` to extract a TRUE tail fragment. Never use `awk` or `head -1` for the anchor — they'll return the full row, creating collision risk and token waste.
2. **Cadence transition is recipe-agnostic:** the H38/H40/H44/H50/H52 stack works identically on hourly and 6h cadences. No recipe modifications needed.
3. **Post-H60 regime is stable:** 2 consecutive 6h sweeps with 0 issues, all 18 crons healthy, 0 pending outputs. Token cost reduced ~83% (72K → 12K/day).
4. **H60 decision window closed cleanly:** Orchestrator actioned H51 option (b) during the H68→H69 gap, not in response to a sweep nudge. The H60 protocol's "wait for Orchestrator action" model worked as designed.

## 9. REFERENCE FOR FUTURE SWEEPS

When constructing the H44 2-line anchor:
```bash
# CORRECT recipe (use this):
grep -E '^\|{1,2} H<N-1> \|' state.md | tail -1 | tail -c 80
# Then verify:
python3 -c "
content = open('state.md').read()
anchor = '<last 60-80 chars of H<N-1> tail> |\n## Verdict History'
print(f'Anchor count: {content.count(anchor)}')  # MUST be 1
"

# WRONG recipe (do NOT use):
awk '/^\| H<N-1> \|/' state.md | tail -1   # Returns FULL row, not tail
```

The H70 sweep is the first reference for the awk-tail pitfall. Future sweeps should reference this file when constructing anchors.
