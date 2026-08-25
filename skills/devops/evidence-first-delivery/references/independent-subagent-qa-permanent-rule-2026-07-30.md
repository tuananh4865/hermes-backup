---
title: Independent Subagent QA - Permanent Rule (2026-07-30)
created: 2026-07-30
type: reference
tags: [subagent, qa, permanent-rule, adversarial-verifier, system-wide]
---

# Independent Subagent QA - Permanent Rule (2026-07-30)

> **First-class VINH VIEN upgrade to `evidence-first-delivery`.**
> User correction on 2026-07-30 10:48 ICT: "QA tu than khong du; luan luan phai co subagent QA cho moi task de truc quan hon."

## Rule (verbatim user escalation)

**Every task that produces an answer, output, decision, file, code, or other outcome MUST be verified by an independent subagent with fresh context. Self-QA is a pre-check, NEVER the final verdict.**

| Verdict | Action |
|---|---|
| `PASS` with raw evidence | OK to deliver |
| `PARTIAL_PASS` | Document caveat; fix failing portion; do not call done |
| `FAIL` | Do NOT ship; fix + re-verify in same session |
| `UNVERIFIED` (timeout / no evidence / subagent could not inspect) | Do NOT claim PASS; treat as unverified until re-checked |

## What changed vs prior behavior

The previous `evidence-first-delivery` skill classified subagent verification by task size:

| Task size | Trigger |
|---|---|
| LARGE (1h+ or >20 tool calls) | MANDATORY subagent QA |
| MEDIUM (10-30 min, 5-20 calls) | Recommended |
| SMALL (<10 min, <5 calls) | Apply 5 self-questions only |

The new rule eliminates the size-based gating:

| Task size | Trigger |
|---|---|
| **MOI TASK** | MANDATORY subagent QA, no exception |

## Operational recipe (verified 2026-07-30 across 5 subagent QA rounds on a single rule-promotion task)

1. **Make the change** (write_file, patch, etc.).
2. **Run 5-Evidence Gate** (existing self-QA: ls, wc, head, grep, curl).
3. **Dispatch `delegate_task(goal="...", context="")`** with fresh-context subagent.
4. **Subagent returns** `VERDICT: PASS / FAIL / PARTIAL_PASS / UNVERIFIED` + raw evidence from independent re-run.
5. **If UNVERIFIED or timeout**: redo step 3; do NOT downgrade to self-QA PASS.
6. **Reconcile findings**, fix if FAIL, re-run until PASS or PARTIAL_PASS with explicit caveats.

## Subagent transcripts may truncate at +N chars (lesson 2026-07-30)

When the subagent's `task-0.log` final summary is truncated (e.g. "+2116 chars" in the `summary:` field), this is a log-buffer limit, NOT a verdict issue. The verifier reached the same conclusion visible in earlier lines of the same transcript.

**Diagnostic recipe:**
- Grep `VERDICT:` in the live transcript.
- Count `end status=completed` count = 1 = subagent finished.
- Inspect earlier assistant segments, which contain the raw evidence table, not just the truncated tail.

If the verbatim verdict is recoverable from earlier transcript lines, treat as valid verdict. Only escalate to PARTIAL_PASS / UNVERIFIED if no verdict string is recoverable at all.

## Pitfalls observed in 5 rounds (2026-07-30 rule-promotion audit)

| Round | Verdict | Cause |
|---|---|---|
| 1 | PARTIAL_PASS | Top-of-doc mandate added; pitfall #9 still LARGE-only |
| 2 | (truncated) | Same caveat; transcript limit cut off reason |
| 3 | FAIL | "LARGE" wording remained in `SOUL.md` line 203 |
| 4 | FAIL | Same "LARGE" wording remained in Phase 0 checklist line 166 |
| 5 | PASS | Both occurrences of "LARGE" removed; rule consistent across docs |

**Lesson:** After partial-verdict, do NOT auto-claim next round. Re-dispatch subagent and explicitly tell them to check the specific dimension that failed before.

## Pitfall: "PASS-after-fix" is not enough — must re-verify the previously failed dimension

If subagent N says `FAIL on dimension X`, fixing X and asking for re-verify on round N+1 must explicitly request the verifier to re-check dimension X. Subagents default to re-running the full set of checks; if the original failure was a content contradiction, the fix may accidentally regress another dimension.

## Pitfall: subagent verdict override trap

If subagent returns `FAIL` but the assistant believes the failure is wrong, the assistant must:
1. Quote the subagent's exact wording for the failing dimension.
2. Provide independent counter-evidence (raw command output).
3. Dispatch a fresh subagent to adjudicate.

Self-override of subagent verdict = the exact confirmation-bias failure this rule exists to prevent.

## Active-checklist (run BEFORE every completion claim)

- [ ] Output has a completion claim or decision or new file?
- [ ] Subagent dispatched via `delegate_task(goal, context)` with fresh-context?
- [ ] Subagent returned `VERDICT: PASS / FAIL / PARTIAL_PASS / UNVERIFIED` + raw evidence?
- [ ] Verdict is PASS (not UNVERIFIED / timeout)?
- [ ] If FAIL / PARTIAL_PASS: fix + re-verify in same session?
- [ ] File-edit log written for each artifact?

If any answer is NO -> do NOT deliver.

## Reference

- `~/.hermes/SOUL.md` section "ADVERSARIAL SUBAGENT VERIFIER" + Phase 0 checklist line 166.
- `~/.hermes/skills/productivity/evidence-gate/SKILL.md` top-of-doc mandate + pitfall #9.
- `~/.hermes/skills/qa-gate/SKILL.md` section "Permanent Independent-Subagent QA Mandate (2026-07-30)".
- `~/.hermes/scripts/adversarial_verify.py` CLI helper.
- `/Volumes/Storage-1/Hermes/wiki/concepts/independent-subagent-qa-permanent-rule-2026-07-30.md`.
- `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md` section "Independent Subagent QA - Permanent Rule (2026-07-30)".
