# Sibling-Collision Pattern (H32+ lesson, 2026-06-26)

**Real failure mode (2026-06-26 14:32 → 15:00 → 16:01 → 22:00 → 22:30):** Two cron jobs write to the SAME `qa-agent/state.md` file at overlapping times:

- **qa-agent hourly gate** (cron `QA Agent Quality Gate`, fires at `0 * * * *`) writes H-rows to its own state.md
- **Orchestrator 30m heartbeat** (cron `Orchestrator Heartbeat`, fires at `*/30 8-22 * * *`) ALSO writes a "H-row"-shaped entry to qa-agent/state.md as part of its 6-check protocol

When both fire within minutes of each other (e.g. qa-agent at 15:00:30, orchestrator at 14:32 or 15:30), the second writer hits a state where the file's `## Verdict History` table has already been updated. A naive patch anchored on the prior row's tail can:

1. Match an UNEXPECTED prior row (the sibling's row, not the one this agent remembers)
2. Duplicate the H-number (both agents write H32)
3. Overwrite the sibling's row when the anchor substring matches both

**Real transcripts where this fired:**

| Sweep | Time | Conflict | Resolution |
|---|---|---|---|
| H32 | 2026-06-26 14:32 | Orchestrator wrote H32 between qa-agent's dispatch (15:00:30) and patch attempt (15:01:30) | qa-agent renumbered to H33, re-anchored on sibling's tail |
| H34 | 2026-06-26 16:01 | Orchestrator 30m heartbeat wrote H34 row to qa-agent state.md after qa-agent's H33 at 15:01 | qa-agent's next sweep at 17:01 had to renumber to H35 and use UNIQUE 4-line anchor |
| H41 | 2026-06-26 22:30 | Orchestrator 30m heartbeat (this sweep) writing H41 after qa-agent's H40 at 22:00 | Pre-append scan detected H40 present, used 4-line anchor on H40 tail |

## Why this is its own reference (not just a note in SKILL.md)

The H18/H25 lesson covers **single-writer boundary anchoring** — when ONE agent writes to a growing file, use the last row's tail + `## Verdict History` as a unique anchor. That works fine when only one writer exists.

The sibling-collision pattern is a **different problem**: TWO writers with **independent clocks** both legitimately want to append. The fix is not "stop one of them" — it's "detect the collision and renumber" — because both rows carry real audit value.

## Detection recipe (mandatory pre-write step)

Before ANY patch on `qa-agent/state.md`, scan for sibling collisions:

```bash
# 1. Count current H-rows in the file
H_COUNT=$(grep -cE '^\| H[0-9]+ \|' ~/.hermes/profiles/qa-agent/state.md)

# 2. Compute the expected next H-number based on this agent's last known write
#    (from your session memory or your prior sweep's row)
EXPECTED_H_NEXT=$((LAST_KNOWN_H + 1))

# 3. If H_COUNT >= EXPECTED_H_NEXT → a sibling wrote between your reads
#    → grep for the actual highest H<N> in the file
HIGHEST=$(grep -oE '^\| H[0-9]+ \|' ~/.hermes/profiles/qa-agent/state.md | \
          grep -oE 'H[0-9]+' | sort -V | tail -1 | tr -d 'H')

# 4. Set THIS sweep's H-number to HIGHEST + 1 (not LAST_KNOWN + 1)
THIS_H=$((HIGHEST + 1))
```

**The detection happens BETWEEN read_file and patch.** If your read happened at 14:31 and your patch lands at 14:33, a sibling may have written in the 2-minute window. Always re-scan before patching.

## Renumbering + re-anchoring recipe

When sibling-collision is detected:

```python
# Pseudocode for the patch operation
old_string = <tail of the sibling's H<N> row that you found in step 3>
# e.g. last 120 chars of "...H32 ... (orchestrator 30m heartbeat — H38/H37 cron-truth sweep)"

new_string = (
    old_string
    + "\n"  # preserve the sibling's row terminator
    + f"||| H{THIS_H} | <current ISO> | N/A | N/A | 0 | (<your role> — <reason>) | <your content> |"
)
```

**Key points:**

1. **Use the SIBLING's row tail as anchor, not your own prior row's tail.** The sibling wrote between your reads; your prior tail may no longer be at the file boundary.
2. **Renumber to HIGHEST + 1, never overwrite the sibling.** Overwriting destroys their audit value.
3. **Cite the sibling in your new row's Notes column.** Format: "Sibling-collision: <your role> H<THIS_H-1> row already present from <sibling role> at <HH:MM> — re-anchored on actual highest H<N> tail."
4. **Verify the anchor is unique.** The H18/H25 lesson's `grep -c` check (counting `## Verdict History` occurrences) STILL applies — that header appears 1x per file, but inline refs accumulate. For files with 15+ inline refs, use a 4-line context anchor (last 120 chars of prior row + blank line + section header + table header).

## Sibling-collision matrix (which profiles can collide on qa-agent/state.md)

| Cron | Profile | Cadence | Writes to | Can collide with |
|---|---|---|---|---|
| QA Agent Quality Gate | qa-agent | hourly | qa-agent/state.md | (self only) |
| Orchestrator Heartbeat | orchestrator | 30m | qa-agent/state.md (H-rows as cross-validation log) | qa-agent hourly gate |
| Operations Manager Routing Audit | operations-manager | 6h | operations-manager/state.md (NOT qa-agent) | No collision with qa-agent |
| QA Agent Quality Gate | qa-agent | hourly | qa-agent/state.md | Orchestrator 30m heartbeat |

**Key insight:** Only **TWO** crons write to qa-agent/state.md. If you find yourself dealing with a 3-way collision, something is structurally wrong (a 3rd cron was added without updating this matrix).

## Sibling-aware report delivery

The orchestrator 30m heartbeat ALSO delivers its report to the Telegram cron delivery target. If both qa-agent and orchestrator write the same minute, the user gets 2 near-identical messages.

**Mitigation (defer until 2nd collision in 1h):**

- Track sibling-collision count in qa-agent/state.md frontmatter
- If 2+ collisions in 1h → emit ONE combined Telegram message per sweep cycle instead of per-writer
- Below threshold → accept the duplicate, it's noise but not corruption

## Why H32 was the FIRST real collision (and why it took 33 sweeps to manifest)

Before H32, the system had been idle for 10+ days. The orchestrator 30m heartbeat had been firing all that time but `qa-agent/state.md` had been QUIET (since the orchestrator writes its H-row AS the parent sweep, the qa-agent hourly gate ALSO writes its own H-row). When both were in steady-state idle, they were writing near-identical content with identical H-numbers because there was nothing new to report.

**The first real collision happened when qa-agent woke up to write H33 (15:00) right after orchestrator wrote H32 (14:32).** That's when the renumbering pattern was discovered.

**Forward implication:** Sibling-collision is **most likely during dormancy wake-up transitions**, not during steady-state idle. If you see the system transitioning out of dormancy (any maker state.md mtime < 2h), expect a collision in the next 30m.

## Hard rule: never rely on LAST_KNOWN_H from session memory

Session memory is wrong by definition after a sibling writes. The only safe H-number is the one computed from the actual file state at patch time. This is structurally similar to the H38 lesson ("don't trust mtime, verify with hermes cron list") — both say "verify against the actual system state, not against your memory of it".

## Pair with H18/H25 (boundary anchor uniqueness) and H38 (cron-truth verification)

These three patterns together cover the full file-integrity defense:

1. **H18/H25** — use a unique boundary anchor when the file is large (mode-deformed boundary line)
2. **H38** — verify cron truth before classifying any profile as faulted
3. **Sibling-collision** — detect sibling writes between your reads, renumber accordingly

Without all three, the heartbeat can corrupt state.md or propagate false-positive fault classifications. With all three, the heartbeat is structurally robust against the 3 most common silent-failure modes.