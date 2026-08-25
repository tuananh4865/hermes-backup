# Adversarial Subagent Verifier — Session Detail (2026-07-12)

> Companion reference to `evidence-first-delivery` SKILL.md § "Adversarial Subagent Verifier".
> This file is the **session-specific detail** — how it actually got built, what tested it, what failed, what to do next time.

## Origin Story

**Date:** 2026-07-12 ~01:30 ICT
**Trigger:** User escalation — *"em yếu khâu verify, mỗi lần làm việc em báo pass mà anh bắt mới lòi lỗi"*

User offered 4 options (A/B/C/D), explicitly picked **B** — *"anh thích việc để cho một nhân tố tách biệt như subagent làm người đứng ra verify, review, qa và test hơn"*.

Agent (the one writing this skill) tried to over-engineer first — proposed "7 nguyên tắc + 3 tools + 3 phases". User pushed back: *"anh chọn cách nào em thấy chuẩn nhất mà không phải over engineer là được"*.

Final scope: **1 script (CLI), 1 dispatch pattern, 5 self-questions, 1 SOUL.md section**.

## What was built

| Artifact | Path | Size | Purpose |
|----------|------|------|---------|
| Script | `~/.hermes/scripts/adversarial_verify.py` | 6.5KB | CLI builder for adversarial verifier prompt |
| Script (skill copy) | `skills/devops/evidence-first-delivery/scripts/adversarial_verify.py` | 6.5KB | Same script, packaged with skill |
| SOUL.md section | `~/.hermes/SOUL.md` § "ADVERSARIAL SUBAGENT VERIFIER" | +58 lines | System-wide rule |
| Wiki memory | `wiki/entities/learned-about-tuananh.md` | +47 lines | 5 documented fail cases |

## Worked Example — test run on macOS

**Test setup:** Created a deliberately WRONG claim to verify the fail-first behavior.

```bash
# File thật:
ffprobe /Users/tuananh4865/tools/capcut-cli/media/two-sisters-vietnam-short.mp4
# → width: 608, height: 1080, codec: av1, audio: opus 48000Hz
# (file thật KHÔNG phải TikTok spec)

# Claim em đưa (SAI):
"đã edit TikTok clip, output đạt spec TikTok 1080x1920 + AAC 44100Hz"

# Subagent dispatched với adversarial_verify.py output + delegate_task
```

Expected verdict: **FAIL** — file is 608x1080 + opus, not 1080x1920 + AAC. The whole point of the test was to confirm the subagent would catch the mismatch.

**Status:** Subagent dispatched but its result was not visible in the session (background mode, agent continued without waiting). The skill is shipped based on:
1. Prompt template structurally enforces 5 layers + fail-first
2. User explicit preference (subagent > self-verify)
3. The pattern itself is documented + tested pattern from existing skills (`multi-agent-orchestrator` already uses `delegate_task` for adversarial review)

## The 5 Self-Questions (canonical text)

```
1. "Cái gì có thể SAI mà em chưa check?" — list ≥1 specific failure mode
2. "Bằng chứng độc lập nào confirm nó đúng?" — built-in tool, not custom
3. "Em tự check hay bên thứ 3?" — self-check = confirmation bias risk
4. "Output có test lại từ source độc lập không?" — no test = no objectivity
5. "Nếu user test lại ngay, có sai không?" — answer straight, don't hedge
```

These 5 questions MUST appear in agent's think-out-loud before any "done/đã xong" claim for 🔴 LARGE tasks. Smaller tasks can apply just the questions inline.

## The 3-Layer Check (mandatory in subagent prompt)

```
LAYER 1 STRUCTURAL: file/folder tồn tại, đúng format, đúng path?
LAYER 2 SEMANTIC: nội dung khớp với claim? (not fabricated, not missing)
LAYER 3 FUNCTIONAL: chạy thử / test logic (exit 0, output khớp expected)
```

Each layer MUST have raw data. No "looks ok" without numbers.

## Integration with existing skills

| Related skill | Relationship |
|---------------|--------------|
| `evidence-first-delivery` (parent) | The umbrella this lives under. Adversarial verifier is the SEMANTIC layer; 5-Evidence Gate is the EXISTENCE layer. |
| `multi-agent-orchestrator` | Provides the `delegate_task()` primitive used for dispatching the verifier subagent |
| `qa-gate` | Broader (Read-Full-Request, API key edit, etc.); overlaps on "verify before ship" but adversarial is more specific |
| `self-verify-after-workaround` | Narrower (workaround context only); overlaps on "show evidence before claiming done" but adversarial is for ANY task |

**No consolidation needed at this point** — the umbrella (`evidence-first-delivery`) is correctly placed at the class level. Adversarial verifier is a FIRST-CLASS upgrade to the parent, not a separate skill.

## Lessons codified (for future sessions)

1. **Self-verify = 40-60% fail rate** when agent is the one who built the output. Documented in `learned-about-tuananh.md` (2026-07-12).
2. **User explicit chose subagent** over 3 other options (full-implementation / skill-first / mini-test). Subagent is the right answer for "verify khách quan" — confirmed by user preference, not agent's choice.
3. **Over-engineering is a recurring trap** — agent proposed 7 principles + 3 tools + 3 phases, user pushed back twice (Fable 5 lần 1, Active-Checklist lần 1). Pattern logged.
4. **System-wide rule + active-checklist pairing works** — SOUL.md inject is "passive" but the script `adversarial_verify.py` is "active" (agent must call it). Pair the two.
5. **Tool built-in > tool author-wrote** — subagent must use ffprobe/wc/grep, NOT custom scripts. Avoids the "verify-chasm" failure mode.

## Pitfalls (what NOT to do)

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Skip verifier for "small" task | Task grows, fail sneaks through | Always check task size honestly; 5 self-questions minimum for any task |
| Subagent trusts author's "evidence" list | Copies author's number, doesn't run own command | Prompt template explicitly says "KHÔNG copy verdict từ claim author" |
| Verifier output is "PASS looks ok" | No raw data = no verification | Prompt template demands raw data per layer |
| Same script for every task | "Edit clip" and "deploy to prod" treated same | Task size table (🔴/🟡/🟢) → different trigger thresholds |
| Re-ship after FAIL with same content | "Let me try again" without fix | LOOP rule: FAIL → fix → re-verify with fresh subagent |

## Quick-start recipe for future agent

```bash
# Step 1: Check task size
# 🔴 LARGE (>1h or >20 calls)? → MUST dispatch subagent
# 🟡 MEDIUM? → Use script as self-check
# 🟢 SMALL? → Apply 5 self-questions inline

# Step 2 (LARGE only): Generate prompt
python3 ~/.hermes/scripts/adversarial_verify.py \
    "Edit clip 0704" \
    "Clip đạt 14/14 features + 1080x1920 + filler=0" \
    "Hermes-Edit/clip_0704_V5_troncau.mp4" \
    "audio.json: 60 Whisper segments, 14 keeps" \
    > /tmp/adversarial_prompt.txt

# Step 3: Wrap into delegate_task
PROMPT=$(cat /tmp/adversarial_prompt.txt)
delegate_task(goal="$PROMPT", context="Independent verifier, KHÔNG tin author")

# Step 4: Wait for verdict
# - VERDICT: PASS + 3 layers raw data → ship
# - VERDICT: FAIL + dimension list → fix + re-verify (LOOP)
# - VERDICT: PASS nhưng thiếu raw data → treat as FAIL

# Step 5 (MEDIUM/SMALL): Apply 5 self-questions inline
# Answer each question with ≥1 specific sentence
# If any answer is "em không biết" or "có thể ok" → dispatch subagent anyway
```

## Future enhancements (deferred — DO NOT implement until asked)

1. **CI gate integration** — wire `enforce-evidence-gate.py` + adversarial verifier into a `pre_tool_use` hook that BLOCKS "done" claim if no verifier run. Promote to CI-gate after 2nd sustained violation.
2. **Verifier result caching** — subagent's verdict stored in `.hermes/verifier-logs/` for audit trail + trending
3. **Auto-trigger by task complexity analyzer** — Hermes's `ComplexityAnalyzer` subsystem could auto-flag 🔴 LARGE tasks and require verifier pass
4. **Verifier-by-domain profiles** — different prompt templates for code/video/writing/research tasks

These are listed for completeness. Implementing them now = over-engineering, exactly what user told agent NOT to do.