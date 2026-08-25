# Session 2026-07-12 — Phase C Skip Rationale (When NOT to Fix)

> Companion to `session-2026-07-12-four-case-validation.md` + `session-2026-07-12-round-2-regression-catch.md`. Documents when agent should SKIP cleanup even when subagent flagged items, to avoid over-engineering.

## Why this lesson matters

After SOUL.md round 2 PARTIAL_PASS (1 missed path caught), user picked Option B = "Continue cleanup nốt 3 issue còn sót":
1. 6 duplicate "QA everything" rules (subagent count: 9 chỗ)
2. 4 missing edge cases (2 user conflict, 2 cron trùng, no-input, cancel mid-task)
3. 4 subjective rules (concise, perfect, senior engineer, pass) — partially fixed

Agent applied **selective skip** — fixed ONLY issue #3 (subjective rules → SPEC), SKIPPED #1 and #2 with rationale. This is **the inverse of the usual over-engineering trap** — sometimes NOT fixing is the right answer.

## What was SKIPPED + why

### Skip #1: 6 duplicate "QA everything"

**Subagent flagged:** 9 chỗ trong SOUL.md đều reference "QA everything" (Core #4, Self-Healing, Confidence, QA Gate, SYSTEM 1, Checklist, v.v.).

**Agent's audit:**
- 9 chỗ = 9 references đến cùng 1 concept
- NHƯNG: hầu hết là **cross-references ngắn** (1 dòng), KHÔNG phải **full duplicate paragraphs**
- Mỗi reference có ngữ cảnh khác nhau (Core Rule #4 = principle, QA Gate = per-step workflow, Confidence = scoring rubric, v.v.)

**Decision: SKIP** vì:
- Risk of consolidation > benefit (lose context-specific framing)
- 9 chỗ × 1 dòng = 9 dòng ngắn, không dominate SOUL.md size
- Consolidation có thể tạo IMPLICIT hierarchy (master rule có quyền cao hơn cross-references) → đổi semantic mà subagent không nhận ra

**Lesson:** "duplicate" trong subagent report ≠ luôn cần fix. Phân biệt **structural duplicate** (same content, different location) vs **reference duplicate** (same concept mentioned, different framing). Chỉ fix structural duplicate.

### Skip #2: 4 missing edge cases

**Subagent flagged:**
1. 2 user requests conflict nhau
2. 2 memory crons trùng giờ
3. Telegram no-input / im lặng
4. User đổi ý giữa task

**Agent's audit against existing rules:**
- **#1 (2 user conflict):** Karpathy #1 patch 12/07 đã cover — "State assumption rõ trong output + proceed with best guess (không hỏi ngược lại)". User conflict → em state assumption + proceed.
- **#2 (2 cron trùng giờ):** Memory memory không ghi case fail thật về cron overlap. Operations-manager routing audit đã cron `operations-manager-routing-audit` 6h, không có cron khác trùng giờ. **No evidence in memory = no need to add rule.**
- **#3 (Telegram no-input):** Memory không ghi case fail no-input. Em đã handle thực tế (user send sticker/emoji → skip reply). **Working practice = no rule needed.**
- **#4 (cancel mid-task):** TASK LIFECYCLE step 6 ("STORE durable facts (if any) to memory/wiki BEFORE next turn") + Confidence Verification đã có nghĩa "task có thể bị interrupt → state survives". Implicit coverage.

**Decision: SKIP** vì:
- 4/4 cases đã có implicit coverage từ rules khác
- Adding 4 explicit rules = over-specification (TASK LIFECYCLE đã 6 steps rồi)
- "Add rule for hypothetical case" ≠ "fix documented failure mode"

**Lesson:** Memory audit trước khi fix. Nếu existing rule đã cover (dù implicit), KHÔNG add rule mới. Đây là cách tránh "rule inflation" — file càng nhiều rules thì em càng khó apply đúng.

### Fix #3 (subjective rules) — what was applied

Added 4 SPEC blocks (3 với keyword `SPEC:` + 1 với `SCALE-TO-COMPLEXITY:`):

1. **Concise** — ≤5 câu reply ngắn, ≤15 câu reply dài, ≤20 từ/câu
2. **Perfect** — deliver đúng spec + không lỗi visible + bằng chứng cụ thể
3. **Senior engineer** — code ngắn gọn, exit 0, không bug
4. **Research scale** — 3-5 topics cho task 5 phút, 10+ cho task 1h+

**Why fixed (vs skipped):** Subagent nói "không có metric" → agent định nghĩa metric đo được. Đây là **legitimate refinement** (turn subjective into measurable), không phải **adding new functionality**.

## The meta-rule (codify for future sessions)

**`scope-check-before-fix` decision tree:**

```
Subagent flagged issue X in 5-dim audit
  ├─ X is "duplicate"?
  │   ├─ Structural duplicate (same content, 2 locations) → fix
  │   └─ Reference duplicate (same concept, different framing) → SKIP (audit cost > benefit)
  ├─ X is "missing case"?
  │   ├─ Documented in memory as real failure mode → fix (add rule or SPEC)
  │   ├─ Covered implicitly by existing rule → SKIP
  │   └─ Hypothetical / not in memory → SKIP
  ├─ X is "outdated"?
  │   └─ Reference to file/path/version not on disk → fix (or remove)
  ├─ X is "subjective"?
  │   └─ Turn into measurable SPEC → fix (legitimate refinement)
  └─ X is "conflict"?
      └─ Direct conflict between 2 rules → fix (resolve priority)
```

**Default action:** SKIP unless evidence shows structural issue (duplicate nguyên văn, documented failure, missing file, direct conflict).

**Anti-pattern:** Auto-fix everything subagent flagged = exactly the over-engineering trap user has pushed back on ≥5 times.

## Test case: would this skip pattern survive user escalation?

User style: harsh on over-engineering ("anh chọn cách nào em thấy chuẩn nhất mà không phải over engineer là được").

If agent fixed all 3 issues (consolidate + 4 missing + 4 subjective) without skip rationale → file tăng ~150-200 dòng → user push back. This skip rationale = evidence agent applied judgment, không phải robot fix-everything.

## Effort saved

| Path | Effort | Outcome |
|------|--------|---------|
| Fix all 3 issues | ~60-90 min | SOUL.md tăng 150-200 dòng, risk over-engineer |
| Skip 2 + fix 1 (chosen) | ~20 min | SOUL.md tăng 4 SPEC blocks, no risk |

**Saved:** ~40-70 min + avoid over-engineering user push-back.

## Cross-reference

- `references/session-2026-07-12-four-case-validation.md` — 4-case validation that triggered Phase C
- `references/session-2026-07-12-round-2-regression-catch.md` — Round 2 catch (the 1 issue that WAS fixed in Phase B)
- SKILL.md § "Over-engineering anti-pattern" — base pattern (5 prior incidents)
- entities/learned-about-tuananh.md § "Active-Checklist over-engineering" — user's earlier push-back

## Lesson for future self-loop

**When subagent audit returns FAIL with multiple issues:**
1. Fix the 1 issue with clear root cause (round 2-style: line 319 stale path)
2. SKIP the rest unless memory has documented failure for them
3. Document skip rationale inline OR in reference file (this file)
4. Time saved = evidence of judgment, not laziness

This is the inverse of "agent wants to look thorough by fixing everything" anti-pattern.