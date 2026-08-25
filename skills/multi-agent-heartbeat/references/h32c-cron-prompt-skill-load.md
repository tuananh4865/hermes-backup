# H32c — Cron-Prompt Bypasses Skill Load

**Discovered:** 2026-06-27 19:30 (H64 orchestrator 30m heartbeat)
**Status:** ACTIVE failure mode, no automatic fix
**Related:** H26-reoccurrence-2026-06-24-2001 (skill loaded, Mode 8 violated — different stage of the pipeline)

## The Failure Mode

When a scheduled cron-job fires with a prompt that contains bullet-formatted instructions describing the work in detail, the agent treats the prompt as a complete spec and **does not load the skill whose name literally matches the work**.

**Canonical example (H32c Validation 3, 2026-06-27 19:30):**

The 30m orchestrator heartbeat cron fired with this prompt:

> You are the Hermes Orchestrator (default profile). Run a 30-minute heartbeat check. Actions:
> (1) Read state.md of all 5 active profiles (qa-agent, engineering-lead, operations-manager, code-reviewer, security-engineer).
> (2) Find tasks pending >2h, nudge the agent.
> (3) Find outputs waiting qa-agent verification, route to qa-agent.
> (4) Check for security CRITICAL findings, auto-fix per owner authority.
> (5) Check for agent conflicts (2 agents on same file), auto-resolve per priority matrix (severity > reversibility > cost > deadline).
> (6) Report status: N active, N stuck, N verified, N escalated.
> Output: 1-line summary + table.

The agent:
- ✅ Read all 5 state.md files in parallel (action 1)
- ❌ Did NOT load `multi-agent-heartbeat` skill, even though the skill's description literally says: *"Use when running the 30m (or similar periodic) cron heartbeat that reads every active profile's state.md, detects stuck/pending/QA-pending tasks, finds agent conflicts, watches for security regressions, and emits a 1-line summary + table report."*
- ❌ Did NOT run `hermes cron list` (H38 cron-truth sweep)
- ❌ Did NOT run `find pending* / handoff*` (H5/H10 false-positive triage)
- ❌ Did NOT cross-reference state.md mtime vs cron `last_run` (H38 table)
- ❌ Did NOT enter STEADY_STATE_IDLE mode (H32b HARD GATE)
- ❌ Did NOT check `hermes cron status` to verify the qa-agent hourly gate is still running
- ✅ Output format was correct (1-line + table) — by accident, not by protocol

**Output was correct by accident.** Every fact in the table was lifted from qa-agent H62 row (1h-old third-party data). If a real fault had emerged in the last hour, this sweep would have missed it. The agent had no live verification of any of the 6-check protocol items.

## Why This Happens

The LLM's heuristic for "should I load a skill" is roughly: *"Does my task description match the skill's `description:` field?"*

The cron-prompt's action bullets describe the work at the same level of granularity as the skill's description. Both contain:
- "30-minute heartbeat"
- "Read state.md of all N profiles"
- "Find tasks pending >2h"
- "Detect stuck/pending/QA-pending"
- "Find agent conflicts"
- "Output: 1-line summary + table"

The LLM sees the prompt → sees the actions match what it knows → reads state.md files → emits the table. **It never asks "is there a skill I should consult first?"** because the prompt looks self-sufficient.

The trigger banner pattern (from H26 reoccurrence) only loads the skill AFTER the LLM has already decided to load it. If the LLM's "I know what to do" intuition fires on the prompt, the trigger banner is never consulted.

This is a **pipeline-early bypass**: the skill was supposed to be the spec; the prompt became the spec instead.

## How It Differs from H26-Reoccurrence

H26-reoccurrence-2026-06-24-2001 captured a LATER-stage bypass: the agent loaded the skill but violated Mode 8 anyway (wrote a verbose row when STEADY_STATE_IDLE was mandated). The H26 fix was adding more H32 HARD GATE enforcement.

H32c is an EARLIER-stage bypass: the agent never loaded the skill at all. The H32/H32b fix is irrelevant here because the protocol was never in scope to be violated.

**Both produce the same end-result:** output looks correct, but the process is wrong.

| Failure mode | When in pipeline | Symptom | Fix location |
|---|---|---|---|
| H26-reoccurrence | After skill load | Skill content ignored, Mode 8 violated | Add H32 HARD GATE enforcement (done) |
| H32c | Before skill load | Skill never loaded, prompt used as spec | Add trigger to prompt template (NOT YET DONE) |

## The Fix (Recommended: Option 1, deploy immediately)

The fix is at the **cron-prompt template layer**, not the skill-content layer. Four options analyzed; **Option 1 is the chosen minimum-viable fix** because it costs nothing to deploy and turns the prompt into an active trigger the LLM cannot mistake for self-sufficient instructions.

### Option 1 (RECOMMENDED, deploy immediately)

Embed an explicit "Load `multi-agent-heartbeat` skill first" line in the cron-prompt, **placed BEFORE the action bullets**:

```text
[LOAD SKILL: multi-agent-heartbeat]

You are the Hermes Orchestrator (default profile). Run a 30-minute heartbeat check.
Actions:
(1) Read state.md of all 5 active profiles...
[... rest unchanged ...]
```

The `[LOAD SKILL: ...]` bracketed directive is harder for the LLM to mentally collapse into the rest of the prompt than a natural-language instruction. The square brackets create a visual boundary the LLM recognizes as a control statement, not body text. This pattern builds on H26-reoccurrence-2026-06-24-2001's trigger-banner evidence.

**Deploy command** (when ready):
```bash
hermes cron update <heartbeat-cron-id> --prompt "$(cat ~/.hermes/profiles/default/heartbeat-prompt.txt)"
# Where heartbeat-prompt.txt contains the rewritten prompt with [LOAD SKILL: ...] prepended.
```

### Option 2 (Backup, for if Option 1 fails)

Route the cron through a wrapper that always pre-loads the skill via the prompt-template itself:

```bash
hermes chat -q "$(cat ~/.hermes/profiles/default/heartbeat-template.md | sed 's/^/[SKILL: multi-agent-heartbeat]\n/')"
```

This prepends the skill-load directive at the shell layer, not the prompt layer. If the LLM rewrites/strips it, the wrapper re-applies it on every cron fire.

### Option 3 (Long-term cleanup, NOT recommended for current state)

Reduce the prompt to: "Run the 30m orchestrator heartbeat." The risk: vague prompts are unreliable, and the LLM might improvise. Only safe once H32b + H32c are proven stable across many sweeps.

### Option 4 (Quick mitigation, use as patch)

Bake the H32b oracle into the prompt as a non-negotiable step:

```text
Step 0 (DO NOT SKIP): run `hermes cron list` and `find pending* handoff*` BEFORE doing anything else.
```

This makes the H32b protocol explicit but doesn't fix the underlying "I know what to do" intuition problem. Useful as a stop-gap if Option 1 deployment is delayed.

**Decision matrix:**

| Option | Effort | Reliability | Fits current state |
|---|---|---|---|
| 1 (prepend directive) | Low | High (H26 trigger-banner evidence) | ✅ Yes — deploy now |
| 2 (shell wrapper) | Medium | Highest | ✅ Yes — backup |
| 3 (vague prompt) | Low | Risky (LLM improvise) | ❌ No — wait until H32b+H32c stable |
| 4 (explicit oracle) | Low | Medium | ✅ Yes — quick mitigation |

**Recommended:** Option 1 deployed immediately, Option 4 as fallback, Option 2 reserved for the 2nd-or-later H32c recurrence.

**Lesson for the curator:** don't add more references when the LLM isn't loading the skill. Fix the prompt layer, not the content layer.

## Detection Recipes

How to detect that a heartbeat sweep bypassed the skill:

1. **Tool-call pattern check:** sweep used <4 tool batches AND <10 tool calls AND did NOT call `hermes cron list` → H32c suspected.

2. **Response pattern check:** sweep response is exactly 1-line + table with no `## Observations` or `## Cron Truth` section → H32c suspected (the skill mandates a richer output structure on first load).

3. **Cross-validation check:** compare sweep's "all 18 crons healthy" claim against the actual `hermes cron list` output. If the claim was lifted verbatim from a prior sweep's row → H32c confirmed.

4. **qa-agent state.md cross-check:** qa-agent's most recent row was written N hours ago. If sweep relied on that row without re-running `hermes cron list` → H32c confirmed.

## Mitigation: What to Do When H32c Is Suspected

1. Do NOT trust the sweep's verdict. Re-run the 6-check protocol manually:
   - `hermes cron list` (ground truth for cron health)
   - `find ~/.hermes/profiles -type f \( -name "pending*" -o -name "handoff*" \)` (ground truth for handoffs)
   - Security CRITICAL grep across all 5 state.md files
   - `stat -f %m` per state.md to verify mtime-vs-cron-truth per H38

2. If the H32c sweep is being reviewed after the fact (not re-runnable), check whether the prior qa-agent row it lifted data from is itself correct. If the chain of "I read X from Y's prior row" goes back more than 2 levels, the freshness is degraded.

3. Document the H32c event in this reference (add a `## Detected H32c Events` section) so future agents can spot the pattern.

4. Consider whether the cron-prompt should be rewritten to make the skill load explicit. Update the cron definition via `hermes cron update <id> --prompt "..."`.

## Detected H32c Events

| Sweep | Date/Time | Skill Loaded? | H32b Oracle Run? | Output Correct By | Notes |
|---|---|---|---|---|---|
| H64 (Validation 3) | 2026-06-27 19:30 | ❌ NO | ❌ NO | Accident | Cron-prompt matched skill description; agent followed prompt bullets literally. Output was correct by lifting data from qa-agent H62 row (1h stale). |

## Related

- `references/h32b-validation-log.md` Validation 3 — full case study of the H64 sweep
- `references/h26-reoccurrence-2026-06-24-2001.md` — sibling failure mode (skill loaded, Mode 8 violated — later in pipeline)
- `references/h32-hard-gate-bypass-pattern.md` — H33-H51 bypass pattern
- SKILL.md "MANDATORY pre-write self-check" section
