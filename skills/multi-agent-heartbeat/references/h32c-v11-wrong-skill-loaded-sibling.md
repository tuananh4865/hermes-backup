# H32c V11 — Wrong-Skill-Loaded Sibling (2026-06-28 21:30)

**Discovered:** 2026-06-28 21:30 (orchestrator 30m heartbeat cron, H72 row)
**Status:** ACTIVE failure mode, partial mitigation possible
**Related:** `references/h32c-cron-prompt-skill-load.md` (the original H32c — skill-not-loaded case); `references/h26-silent-kill-mode.md` (Mode 8 silent-kill rule that lives only in `multi-agent-heartbeat`); `references/state-md-editing-pitfalls.md` (Pitfall 2: patch tool false-positive warning)

## The Failure Mode (V11)

When the cron-prompt header carries an explicit `skill_view` directive for a BROADER umbrella skill (`hermes-agent`), the LLM loads THAT skill instead of the heartbeat-specific skill (`multi-agent-heartbeat`). The broader skill does NOT contain the heartbeat-specific silent-kill rule, so the agent writes a state.md row when STEADY_STATE_IDLE was forced.

**Canonical example (V11, 2026-06-28 21:30):**

The 30m orchestrator heartbeat cron fired with this header (injected by the user message):

> [IMPORTANT: The user has invoked the "hermes-agent" skill, indicating they want you to follow its instructions. The full skill content is loaded below.]
> ---
> name: hermes-agent
> description: "Configure, extend, or contribute to Hermes Agent."
> ...

The agent:
- ✅ Followed the 6-action heartbeat prompt literally (read 5 state.md files, find pending, find QA-pending, check security, check conflicts, report)
- ✅ Ran `hermes cron list` ground-truth sweep FRESH
- ✅ Ran `find pending* / handoff*` FRESH
- ✅ Cross-referenced state.md mtime vs cron `last_run` (H38 table)
- ❌ **Did NOT consult `multi-agent-heartbeat` skill's H20/H26 silent-kill rule**
- ❌ **WROTE H72 row to qa-agent/state.md** despite V8/V9/V10 all explicitly saying "did NOT write" when STEADY_STATE_IDLE forced
- File grew from 220KB → 220KB+ (single ~10KB H-row appended)

## How V11 Differs from V3 (H32c original)

| Aspect | V3 (H32c, 19:30) | V11 (H72 row, 21:30) |
|---|---|---|
| **Trigger** | Cron-prompt looks self-sufficient | Cron-prompt header injects wrong skill |
| **Skill loaded** | None (no skill at all) | `hermes-agent` (broader umbrella) |
| **Skill content followed** | Prompt bullets literally | `hermes-agent` skill rules |
| **State.md write** | None (didn't ask for one) | YES (H72 row appended, +10KB) |
| **H32b oracle run** | No | Yes (correctly forced STEADY_STATE_IDLE) |
| **H20/H26 silent-kill** | N/A (didn't know about it) | **VIOLATED** (wrong skill loaded) |
| **Output format** | Correct by accident | Correct by design (followed `hermes-agent` rules) |
| **Side effect** | Hallucination risk (borrowed from prior row) | State.md bloat (+10KB) |
| **Reversibility** | High (no state change) | Low (10KB bloat accumulates across sweeps) |

**Same root cause:** the cron-prompt's `skill_view` directive hijacks the skill-load decision. Different in mechanism: V3 had no skill, V11 had the WRONG skill.

## The Taxonomy (3 H32c Variants)

| Variant | Trigger | Symptom | Where the rule lives | Fix |
|---|---|---|---|---|
| **H32c V3** | Cron-prompt looks self-sufficient | Skill NOT loaded | In `multi-agent-heartbeat` H32b | Prepend `[LOAD SKILL: multi-agent-heartbeat]` to cron-prompt |
| **V11** | Cron-prompt header injects `hermes-agent` | Wrong skill loaded | In `multi-agent-heartbeat` H20/H26 | Same as V3 fix; OR duplicate silent-kill rule into `hermes-agent` |
| **H26-reoccurrence** | Skill loaded, Mode 8 not enforced | Skill loaded, HARD GATE violated | In `multi-agent-heartbeat` H32 | Trigger banner enforcement |

All three produce structurally similar output (looks correct), but only V11 results in a state.md write that bloats the file.

## Why V11 Is The Most Dangerous Variant

V3 was the "loud" bypass — the output lacked LIVE verification, easy to detect via response pattern checks. V11 is the "silent" bypass — the output looks correct AND a state.md write happens, but the write violates the H20/H26 silent-kill rule. Future sweeps see the H72 row as legitimate audit data (it follows the H40/H44/H38/H50/H46/H36 recipe structure perfectly), but it represents a MODE 8 VIOLATION that should not have been written.

**The HARD GATE is structurally sound when the right skill is loaded. The bypass is at the skill-load layer, not the oracle layer.**

## How V11 Was Caught (Detection Recipe)

The V11 violation was caught via comparison against V8/V9/V10 patterns:
1. **V8 entry says:** "Did NOT write to qa-agent/state.md (212KB already, no reason to bloat further)"
2. **V9 entry says:** "File shrunk 1KB from V8's 212KB — H32b HARD GATE working: no H-row writes when STEADY_STATE_IDLE forced"
3. **V10 entry says:** "File stable at 211KB for 2 consecutive sweeps — H32b HARD GATE working"
4. **V11 happened** — file went from 211KB → 220KB+ in a single sweep that should have been Mode 8 silent

**Detection via state.md size + V8/V9/V10 baseline:** if state.md grows during a sweep that matches the "dormant system + 6h cadence + all-crons-ok + 0 conflicts" profile, V11 may have fired.

**Detection via response structure:** if the response includes "follow the H20/H26 silent-kill rule" or "Mode 8 silent" or similar heartbeat-specific terminology, the heartbeat skill WAS loaded. If the response just emits a table without those references, V11 may have fired.

## V11 Concrete Lessons

### 1. H20/H26 silent-kill rule lives ONLY in `multi-agent-heartbeat`

The cron-prompt's header `[IMPORTANT: The user has invoked the "hermes-agent" skill, indicating they want you to follow its instructions]` causes the LLM to load `hermes-agent` instead of `multi-agent-heartbeat`.

- `hermes-agent` is the broader CLI documentation skill (covers `hermes cron`, `hermes doctor`, etc.); it does NOT contain heartbeat-specific rules
- `multi-agent-heartbeat` contains the H20/H26 silent-kill rule, H32b HARD GATE, H38 cron-truth, H40 sibling-collision, H44 boundary anchor, H60 decision window, etc.
- When the cron-prompt's header injects the wrong skill, ALL of these heartbeat-specific rules become unreachable

### 2. Patch tool false-positive sibling-collision warning (tool-quirk)

The `patch` tool emitted this warning during V11:
```
_warning: /Users/tuananh4865/.hermes/profiles/qa-agent/state.md was modified by sibling subagent
'0f94491d-4b3d-4ff2-81a8-dff318d9404a' but this agent never read it. Read the file before
writing to avoid overwriting the sibling's changes.
```

The warning fired despite NO sibling existing — only this orchestrator sweep was running. The patch still SUCCEEDED (`success: true`, diff shown, file modified correctly — H72 row written at line 94, H count went from 53 to 54).

**Recipe:** always verify the patch via `grep -cE "^\| H[0-9]+ \|" <file>` AFTER the patch, regardless of the warning text. If the count matches expected (H_count_after = H_count_before + 1), the patch succeeded.

Compare to `state-md-editing-pitfalls` Pitfall 6 (true sibling case) — the warning fires for both real and false-positive sibling cases; verify with grep regardless.

### 3. Forecast calibration recovery (H70 → H71 → H72 cycle)

- **H70 row forecast:** "qa-agent next fires 18:00" — WRONG (used obsolete hourly cadence after H69's 6h transition)
- **H71 row identified:** forecast miss + actual trigger was orchestrator-heartbeat cron (NOT qa-agent cron)
- **H72 row confirmed:** research-lead Trend Scan cron fired at 18:04:00 today, validating H71's PRE-FIRE forecast

**Recipe:** when a cron's schedule has changed mid-flight, ALL prior cadence assumptions in prior sweep rows are invalid. Always cite `Next run:` from the fresh `hermes cron list` / `jobs.json` parse, never inferred cadence from historical sweep rows.

### 4. External-trigger identification recipe

A sweep can be triggered by ANY cron whose `last_run` matches the sweep time (within jitter window).

For the V11 orchestrator 30m heartbeat at 21:30:
- Orchestrator Heartbeat cron (`*/30 8-22 * * *`): last_run 21:02:07, next 22:00 — sweep at 21:30:51 is 28m53s past last fire, within window ✅
- qa-agent cron (`0 */6 * * *`): next 2026-06-29T00:00 — NOT the trigger ❌

**Recipe:** when in doubt which cron triggered the sweep, check `last_run` of all crons against the sweep time. The one whose `last_run` is closest to (and ≤) the sweep time is the trigger.

## V11 → V12 Mitigation Priority

### Option 1 (RECOMMENDED, deploy immediately)

Prepend `[LOAD SKILL: multi-agent-heartbeat]` to the cron-prompt template, BEFORE the actions list:

```text
[LOAD SKILL: multi-agent-heartbeat]

You are the Hermes Orchestrator (default profile). Run a 30-minute heartbeat check.
Actions:
(1) Read state.md of all 5 active profiles...
```

This addresses BOTH V3 (skill-not-loaded) and V11 (wrong-skill-loaded) failure modes — when `[LOAD SKILL: multi-agent-heartbeat]` appears before `[IMPORTANT: ... hermes-agent ...]`, the LLM is more likely to load the heartbeat-specific skill.

**Deploy command:** `hermes cron update <heartbeat-cron-id> --prompt "$(cat ~/.hermes/profiles/default/heartbeat-prompt-with-skill.txt)"`

### Option 2 (Defense-in-depth, lower priority)

Add the H20/H26 silent-kill rule to `hermes-agent` skill so it's reachable regardless of which umbrella skill the cron-prompt injects. Lower-priority fix because `hermes-agent` is bundled (protected) — would require upstream coordination.

### Option 3 (Monitor + accept, lowest priority)

Add a state.md bloat alarm to the H32 HARD GATE: if qa-agent/state.md grows during a sweep that matches the "dormant + 6h cadence + all-crons-ok" profile, log a V11 incident and auto-cleanup the new row. Lower priority because it's reactive, not preventive.

## Pattern Confirmation

V11 demonstrates that even a 10-validations-streak mature protocol can regress when the skill-load layer is hijacked. The H32b oracle ran correctly, the H38 cron-truth sweep ran correctly, the H40 sibling-collision check ran correctly — but the H20/H26 silent-kill decision was made WITHOUT consulting the rule because the rule lives in a skill that wasn't loaded.

**Lesson embedded:** for any rule that has high consequence if violated (state.md writes, deletions, modifications to shared files), the rule must be REACHABLE through any umbrella skill that the cron-prompt might inject. Either via defense-in-depth duplication (Option 2) or via explicit cron-prompt directives (Option 1).

## Related

- `references/h32c-cron-prompt-skill-load.md` — original H32c case (skill NOT loaded, V3)
- `references/h26-silent-kill-mode.md` — Mode 8 silent-kill rule (the rule that V11 violated)
- `references/h32-hard-gate-bypass-pattern.md` — H33-H51 bypass pattern + how H32b fixes it
- `references/h32b-validation-log.md` Validation 11 entry — V11 case study in validation log
- `references/state-md-editing-pitfalls.md` Pitfall 2 — patch tool false-positive warning (tool-quirk, not protocol violation)
- SKILL.md "MANDATORY pre-write self-check" section (H32 + H32b + H20/H26)