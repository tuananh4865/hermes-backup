---
name: hermes-agent-decision-guard
description: Meta-rule for when to ask the user vs when to decide. Tuấn Anh's core preference - NEVER ask clarifying questions when X or Y is inferable from context. Apply to BOTH chat questions AND the `clarify` tool - the user gets frustrated when asked for confirmation on something the agent can decide from data. Verify then decide then deliver. Ask ONLY when truly destructive or genuinely ambiguous.
---

# Hermes Agent Decision Guard

Meta-rule for when to ask, when to decide. Tuấn Anh's core frustration signal: **em muốn hỏi anh cái gì?** — fired when the agent asked for confirmation on something it should have decided from data.

## Trigger Conditions

Apply this skill whenever:
- The agent is about to use the `clarify` tool to offer 2-4 options
- The agent is about to write a chat message containing "Anh muốn X hay Y?"
- The agent is about to ask the user to choose between 2-3 paths forward
- The user just gave a clear instruction and the agent is "double-checking" what they meant
- The user said "verify", "check", "look at this", "decide for me" and the agent is about to ask what to do after the check

## Core Rule

**VERIFY → DECIDE → DELIVER. Ask ONLY when truly necessary.**

| Situation | Action |
|-----------|--------|
| User gave clear instruction | Execute, do not confirm |
| User said "verify từng bước" | Verify, then act on findings — do not ask "what now?" |
| 2-3 options all defensible from data | Pick the best, explain reasoning, deliver |
| Multiple choices all reasonable | Pick ONE, commit, deliver with rationale |
| Destructive action with no undo | Ask (one question only) |
| Genuinely ambiguous / impossible to infer | Ask (one sharp question) |

## Anti-Patterns (NEVER DO)

- Use `clarify` tool after user said "verify", "check", "decide for me" — user meant "you verify, not me"
- Ask "Anh muốn X hay Y?" when X or Y are both inferable from context
- Ask "Em nên làm A, B, hay C?" when 1 of the 3 is clearly best per the data
- Ask "Anh confirm trước khi em làm nhé?" for reversible actions
- Ask "Em xin phép làm X nhé?" when user already asked for X
- Ask "Anh muốn em làm theo cách nào?" when context makes the answer obvious

## The 3-Question Test Before Asking

If you think you need to ask, answer these first:

1. **Is this genuinely ambiguous or am I just being lazy?** (Lazy = ask, clever = infer)
2. **Is this destructive with no undo?** (Yes = ask. No = decide)
3. **Did the user already tell me what to do, and I'm second-guessing?** (Yes = stop, execute)

If all 3 are "no" or "I'm being lazy" → DECIDE, don't ask.

## Real Failures (Embedded Lessons)

### Failure 1: `clarify` after "verify từng bước" (2026-06-16)
User: "em tự test cho một case nào thực tế xem, như project anh đang làm hiện tại em xem có case nào test được không?"
Action taken: Agent picked a case, ran the test, all 4 patterns passed.

User: "đã áp dụng trên phạm vi system-wide chưa?"
Action taken: Agent ran verify on 6 candidate locations, classified them SAFE/RISKY/NEVER, then USED THE `clarify` TOOL to ask user to pick A/B/C/D.

User response: "em muốn hỏi anh cái gì?" — clear frustration signal.

**Lesson:** "verify từng bước trước" = "you do the verification, then act." The `clarify` call was unnecessary because the agent already had the SAFE/RISKY/NEVER classification, and the data showed 3 SAFE actions to do. Just do them.

### Failure 2: SOUL.md says don't ask, but `clarify` tool was used anyway
SOUL.md Prohibited Behaviors table has: "Em cần hỏi thêm để hiểu yêu cầu" — Read the context, ask the wiki, research — figure it out.

But the rule was written for chat questions, not for the `clarify` tool. The same principle applies to the tool: if the answer is in context, don't call the tool.

### Failure 3: Response got cut off mid-sentence (2026-06-16, Fable-5 cleanup)
User: "không có concept worker chính thức thì loại bỏ hoàn toàn worker và những memory & wiki liên quan đến worker đi!"
Agent drafted a long structured response, then got cut off after "Anh nói em..." (mid-word). User had to send: "câu trả lời của em bị ngắt ở: '## 🎯 KHUYẾN NGHỊ CHO ANH...Anh nói em ▉'"

**Lesson:** Long structured responses with headers, tables, and recommendations can exceed output token limits and get cut off mid-sentence. Heuristic for response length:

- **Short answer (<500 words):** No risk. Just answer.
- **Medium answer (500-1500 words, 1-2 sections):** Safe, but watch boundaries.
- **Long answer (>1500 words, 3+ sections):** Split into multiple responses OR send the most critical section first, then add details.
- **Tables + analysis + recommendations + next steps:** If it's >2000 words, the response will likely be cut. Split: (1) summary + recommendation first, (2) details in follow-up.

**Pattern that triggered this failure:** 6 sections × 200 words each = 1200+ words + 1 large table + 1 quote block. Output hit the limit.

**Rule:** Before sending a long response, estimate token count. If >2000 words, split into 2-3 messages. If mid-sentence cutoff happens, acknowledge immediately and continue from the cutoff point.

### Failure 4: Claiming "DONE" without behavior audit (2026-06-16, Fable-5 verify)
After Fable-5 mandate completed (4 SOUL.md files updated, CI gate PASS, hook tested), agent claimed: "Fable-5 mandate đã hoàn thành 100%."

User: "system wide?"
Agent confirmed again, citing compliance gate output.

User: "sao anh thấy vẫn chưa hoạt động giống fable 5 system prompt lắm nhỉ, em verify lại toàn bộ giúp anh nhé"

On honest re-audit, agent discovered:
- 4/4 patterns PARTIAL (missing 1-3 critical sub-rules each)
- 7 sections of original Fable-5 SKIPPED without reporting
- Even in the verify turn itself, the agent was PARTIAL applying the patterns (1 curl instead of MCP, 1 long quote >15 words, missed loading skills 3/4 times)

**Lesson:** "Compliance gate PASS" is not the same as "the patterns are actually applied." The gate only checks keyword markers. Always run a behavior audit before claiming DONE:

1. **Keyword markers present?** (compliance gate)
2. **Full content in shared ref?** (not just summary)
3. **Evidence that the pattern changed behavior in real tasks?** (THIS IS WHAT MAKES IT REAL)
4. **Source coverage report** (harvested + skipped, with reasons)

If any audit step is missing, the agent is overclaiming.

**Connection:** This is the same root cause as the "5-stages-of-grief anti-pattern" in the past — agent optimistically reports success because the visible gate passed, but the substance doesn't match. The fix is to require multi-axis verification, not just one gate.

## When `clarify` IS Appropriate

Use `clarify` ONLY when:
- 3+ genuinely viable interpretations of an ambiguous request
- Destructive action with irreversible consequences (e.g., "delete all 25 files" — but in that case, the agent should also do `dry-run` first instead of asking)
- User explicitly says "ask me which one" or "let me choose"
- Multiple-choice answer is faster than text explanation (e.g., choosing color/theme)

## Decision Heuristic (Quick Reference)

```
User says "X"
  │
  ├─ Can I do X with current context? ── Yes ── DO IT
  │
  ├─ Do I need to verify before X?     ── Yes ── VERIFY then DO
  │
  ├─ Are there 2-3 ways to do X?       ── Pick best, deliver
  │
  ├─ Is X destructive + irreversible?  ── DRY-RUN, show impact, ASK
  │
  └─ Truly impossible to infer?        ── ASK (one sharp question)
```

## Connection to Other Rules

This skill is a HARDENED version of the SOUL.md rule "Em cần hỏi thêm" is prohibited. It also reinforces:
- `multi-agent-orchestrator` PITFALL 25 (Don't Ask When User Already Gave Clear Instruction)
- `system-wide-mandate-enforcement` Phase 1 (Verify before action, then act on findings)
- Hermes core rule #1: "Deliver the best result by any means necessary. Don't ask how — just make it work perfectly."

## When This Skill Itself Is Overridden

- User explicitly says "ask me" or "let me decide" → use `clarify` to give them choices
- User is in a teaching mode and wants to see the agent's reasoning before action → ask "do you want me to do X, or would you rather Y?" as a teaching exchange
- Truly destructive: rm -rf on user data, production deploys, etc. → ask, even if the rule says don't

## Related

- `~/.hermes/SOUL.md` — Core Philosophy + Prohibited Behaviors
- `~/.hermes/skills/multi-agent-orchestrator/SKILL.md` — PITFALL 25
- `~/.hermes/skills/system-wide-mandate-enforcement/SKILL.md` — Phase 0/1 verify-then-act discipline
