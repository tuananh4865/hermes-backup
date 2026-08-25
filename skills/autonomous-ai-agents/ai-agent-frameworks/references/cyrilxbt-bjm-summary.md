---
title: Cyril XBT — Builder-Judge-Manager Self-Correcting Loop
created: 2026-07-19
source: x.com/cyrilXBT/status/2077827005777588266
related_skills: [ai-agent-frameworks, adversarial-content-verifier, evidence-first-delivery, wiki-product-ground-truth]
confidence: high
---

# Cyril @cyrilXBT — Self-Correcting AI Loop (Builder-Judge-Manager)

## Source

- **Author:** Cyril @cyrilXBT (AI/Tech/Crypto educator, one-person-company stack — Obsidian + Claude Code + multi-agent loops)
- **Tweet:** `2077827005777588266` (2026-07-19)
- **Linked X Article:** "How to Build a Self-Correcting AI Loop That Catches Its Own Mistakes Before You See"
- **Snippet:** "For content tasks, ground truth is the original source..."
- **Engagement:** ~23 replies, 65 retweets, 1.2M impressions, 1.1K bookmarks
- **Cross-references:** Cyril also references "memory is not a transcript" thread (`2075623918417723502`) + Claude Code self-improving loops (`2068155877132050461`)

## Core Thesis

A self-correcting loop removes the user from the proofreading position entirely. The system generates, checks its own work against a real standard, catches what it got wrong, fixes it, and only then shows the user. By the time the user sees the output, the obvious mistakes have already been caught.

The fix is not asking better — it's **architecture**. A real self-correcting loop separates the work of producing an answer from the work of judging it, using a different pass, a different prompt, and ideally a different frame of reference entirely, so the judgment is not contaminated by the same blind spots that created the mistake.

## 3-Role Architecture

### Builder

- **Job:** Produce draft from source + brief
- **Output shape:** MUST be structured — `draft` + `confidence` (0-1) + `uncertainty_list` (claims em không chắc 100%)
- **NOT just conversational text** — Judge needs explicit fields to check, not inferred from prose

### Judge

- **Job:** Evaluate Builder's output against a specific written standard
- **MUST** access something the Builder does NOT have: original source material, test suite, actual requirements document — so it has independent ground truth
- **Output shape:** structured verdict per-check (pass/fail/needs-revision + specific reason) — NOT a paragraph of hedged prose

### Manager

- **Job:** Read structured verdict, route next action
- **Decision rules:** established in advance (not improvised judgment)
- **Per-check routing:**
  - fact-check fail → back to Builder with specific unverified claim flagged
  - brief-compliance fail → back to Builder with missing requirement named
  - scope mismatch → escalate to human immediately (judgment failure, not mechanical)
  - clean pass on all checks → final output queue
- **Hard cap:** typically 3 retries → escalate to human with complete history (don't grind a fourth alone)

## 3 Ground-Truth Sources Per Task Type

| Task type | Ground truth source | Right question |
|---|---|---|
| **Coding** | Test suite execution, lint, build status | "did it actually pass when run?" NOT "does this code look right?" |
| **Content** | Original source material + original brief, side by side with draft | "does every claim trace back to source, does it satisfy every brief requirement?" NOT "does this read well?" |
| **Research** | Actual search results + source documents the research was supposed to be based on | "can every claim be traced to a specific source, were the relevant sources searched?" NOT "does this summary sound authoritative?" |

**Rule:** If you cannot articulate what the Judge's ground truth is for your specific task, you do not have a self-correcting loop yet. You have a **rephrasing loop** — the Builder's confident mistake gets confidently rephrased by the Judge instead of actually being caught.

## 3 Per-Check Dimensions (Content Tasks)

For content drafts specifically, Judge checks 3 things with separate pass/fail:
1. **Fact-check** — does every factual claim in the draft trace back to something actually present in the source?
2. **Brief-compliance** — does the draft satisfy every specific requirement in the brief (length, tone, required sections)?
3. **Core-argument preservation** — is the core argument or hook actually present and undiluted by filler?

**Why 3 separate checks, not 1 score:** Collapsing into one overall score hides exactly which dimension failed. Manager needs to route on the SPECIFIC failed dimension.

## The Confidently-Wrong Test (Mandatory Pre-Ship)

Before shipping the loop, feed Judge an output you already know is subtly wrong — something that reads well but contains a specific factual or logical error.

- If Judge correctly catches it → loop works.
- If Judge passes it → your ground truth reference is not actually being checked, OR the check is too shallow.

## Code-Task Specifics (Judge 3 Checks)

1. **Test suite passes** — without the tests themselves being modified (Builder quietly editing a test to make it pass is a specific and surprisingly common failure worth checking for directly).
2. **Static analysis + lint clean.**
3. **Diff addresses the assigned task** — not a related but different problem the Builder decided was more interesting to solve along the way.

Each gets its own explicit pass/fail in the structured verdict.

## Anti-Patterns Cyril Explicitly Calls Out

1. **Judge sees only Builder's output, no independent reference** — single most common mistake. Silently turns correctness check into coherence check. A Judge with nothing to compare against can only tell you the output looks internally consistent, never whether it's actually right.
2. **Generic re-prompt on failure** — "double-check accuracy" is blind retry. Judge must cite SPECIFIC unverified claim + Builder must address THAT claim.
3. **Unbounded retry loop** — ALWAYS hard cap + human escalation. Looping "just one more retry" without a hard cap turns graceful degradation into a hung request under wrong input.
4. **Collapsed single score** — "verdict: 0.7" hides which dimension failed. Must be per-check pass/fail.
5. **Hedged prose verdict** — "the output seems mostly correct but has some issues" → must be structured pass/fail/needs-revision with specific reason.
6. **Builder editing tests to make them pass** — silent failure mode; check for it directly.

## Confidence Threshold Routing (Advanced)

Cyril's framework implicitly assumes Judge can express confidence. If Judge confidence < ngưỡng (typical 0.6):
- Don't loop further on borderline cases
- Route to human review queue
- Set threshold based on task stakes (research summary at 0.55 might be acceptable; medical dosage at same score should never auto-accept)

This is a missing piece in Hermes current `~/.hermes/scripts/adversarial_verify.py` — should add `< 0.6 → escalate human immediately`.

## Mapping to Existing Hermes Skills (70% Match)

| Component | Cyril đề xuất | Hermes hiện tại | Gap |
|---|---|---|---|
| **Builder** | LLM with structured output + confidence + uncertainty list | LLM | ⚠️ Add `uncertainty_list` to structured outputs |
| **Judge** | Separate LLM with source reference | `adversarial-content-verifier` skill (12/07 ship) + `~/.hermes/scripts/adversarial_verify.py` | ✅ Exists — verify Judge prompt actually references ground truth source |
| **Ground truth** | Source + brief + test suite | `wiki-product-ground-truth` (product), `transcript-first-viral-workflow` (transcript), `wiki/concepts/*.md` | ✅ Exists |
| **Manager** | Hard cap 3 retries → escalate human | Cron + manual ack/reject | ⚠️ Missing confidence threshold |
| **Confidence threshold** | Judge confidence <0.6 → human queue | None explicit | ❌ MISSING |
| **Confidently-wrong test** | Self-test with known-bad input | Adversarial verifier 3-layer (STRUCTURAL/SEMANTIC/FUNCTIONAL) | ⚠️ Add "feed known-bad" fixture |
| **Anti-fabrication** | (Implicit — Judge catches lies before user sees) | `evidence-first-delivery` skill (5-Evidence Gate, 2026-07-05) | ✅ Exists — covers agent's OWN completion claim |

## 3 Gaps to Close (Priority Order)

1. **Builder uncertainty list** — when em produces structured output for any judge-able task, append `uncertainty_list: [claim_X, claim_Y]` (claims em không chắc 100%). Cost: ~10 tokens per output, downstream Judge knows where to look hard.

2. **Confidence threshold routing** — extend Manager rule: if `verdict.confidence < 0.6` → escalate human immediately (skip remaining retries). Hardcode in `~/.hermes/scripts/adversarial_verify.py` prompt template.

3. **Confidently-wrong test pattern** — whenever em patches a skill or updates a verification script, append a `KNOWN_BAD_CASE` fixture to `references/test-fixtures/` and require the script to FAIL on it. If script PASSES the known-bad case → verification logic is broken.

## Connection to Hermes 5 Mandatory Systems (12/07 ship)

Cyril's framework reinforces 3 of the 5 SYSTEM-WIDE RULES in SOUL.md:

1. **HARD CHECK mọi thứ** = Cyril's "no Judge-without-ground-truth"
2. **VERIFY LẠI MỌI THỨ bằng tools tự động** = Cyril's "test suite execution, not 'looks right'"
3. **CHECKLIST trước khi báo "xong"** = Cyril's "structured per-check verdict, not hedged prose"

The 2 missing are NOT explicitly addressed by Cyril but are Hermes-internal: `🎯` khẩu hiệu + Loop Engineering (Maker→Checker→Orchestrator→User pipeline).

## Real Hermes Case Studies That Map

- **clip 0704 (12/07)** — em ship tiktok-video-editor V14 PASS với 5 lỗi filler/treo/lặp chưa sửa. Adversarial verifier (Judge without ground truth reference to transcript) cũng PASS. Output ra tới user, user catch. → **Confidently-wrong test failed** — Judge checked coherence, not correctness against source transcript.
- **mascot Vui Vẻ V3 (12/07)** — same pattern, Judge pass vì không reference ground truth style spec.
- **gateway path (12/07)** — em báo `bash ~/.hermes/restart-hermes-gateway.sh` exit 127, sai path thật. Judge (em self) pass vì không cross-check file system.
- **Yonex specs (07/08)** — 14 SKU em sai 1 spec số liệu. Adversarial verifier catch nhờ cross-check `yonex-specs-reference.md` (ground truth reference có).
- **ARMAF routing (07/08)** — em route ARMAF body mist vào project `tuan-anh-badminton` (sai project). Adversarial verifier không catch vì không reference project ground truth `wiki/projects/`.

**Pattern:** Case Yonex + ARMAF catch được là vì ground truth reference được explicitly wire. Case clip 0704 + mascot + gateway KHÔNG catch được vì Judge không reference ground truth. → **Confirm Cyril's thesis**: ground truth reference = make-or-break.

## Related Articles by Same Author

- `2068155877132050461` — "Self-improving loops compound every run" (Boris Cherny / Claude Code reframing)
- `2075623918417723502` — "Memory is not a transcript" (cross-session memory vs context survival)
- `2050214010541269225` — "One person no team content operation" (Cyril's own origin story)
- `2071034792288686588` — Hermes + Obsidian + Claude Code trinity (Cyril's stack)

## When NOT to Apply This Framework

- One-line cosmetic edits (no need for 3-role loop)
- Tasks where the cost of the loop exceeds the cost of the mistake (low-stakes)
- Tasks with no articulable ground truth (you don't actually have a standard to check against — Cyril's rule "if you cannot articulate what the Judge's ground truth is, you don't have a self-correcting loop yet")
- Tasks where the Builder IS the Judge (single LLM evaluating itself without external reference) — Cyril calls this out as the most common failure mode; LLM cannot reliably self-correct reasoning without external signals (Huang et al. 2024)

## Sources to Verify Against

- Cyril @cyrilXBT X profile — AI/Tech/Crypto educator, Substack "Wealth Craft", Telegram channel
- Similar frameworks:
  - **Reflexion** (NeurIPS 2023) — 91% pass@1 on HumanEval, beat GPT-4 80%
  - **Huang et al. 2024 ICLR** — "Large Language Models Cannot Self-Correct Reasoning Yet" (intrinsic self-correction fragile without grounding)
  - **Asai et al. 2024 Self-RAG** — reflection tokens `[Retrieve]`, `[IsRel]`, `[IsSup]`, `[IsUse]`
  - **Corrective Agentic RAG** (Sai Insights, Medium 2026-07-11) — explicit retrieve → grade → rewrite → generate → critique loop with MAX_ITERATIONS = 3 cap
  - **axiomlogica.com 2026-04-26** — LangGraph generator + validator + conditional edge + retry_count pattern
  - **Weights & Biases 2026-05-04** — Observe-Plan-Act-Reflect loop + 4-pillar architecture (actor/validator/memory/tooling)
- Hermes-side counterparts:
  - `~/.hermes/scripts/adversarial_verify.py` (12/07) — 3-layer check + 5-question adversarial
  - `wiki-product-ground-truth` skill — citation [N] required, no claim without wiki reference
  - `transcript-first-viral-workflow` — Whisper source as ground truth
  - `evidence-first-delivery` skill (devops) — 5-Evidence Gate for completion claims
  - `evidence-gate` skill (productivity) — per-task completion claim gate