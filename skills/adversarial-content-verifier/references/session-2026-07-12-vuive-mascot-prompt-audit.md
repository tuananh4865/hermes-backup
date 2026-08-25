# Worked Example — Vui Vẻ Mascot Prompt Audit (2026-07-12)

## Task Frame

User assigned role: **INDEPENDENT ADVERSARIAL VERIFIER**.

**Author's claim under audit:**
> "Đã viết prompt tạo mascot Vui Vẻ style + GIỐNG anh Tuấn Anh. Prompt V3.1 có:
> - Mascot messy fringe tóc + brown crewneck + signature 92 tattoo
> - Vui Vẻ style (Western cartoon, outline đen dày, flat color)
> - 4 variations đổi màu tóc (cyan/pink/purple/green)
> - Checklist 9 items verify giống anh
> Đã ready để paste vào NanoBanana Pro"

**Author's evidence:**
- File: `/Volumes/Storage-1/Hermes/wiki/projects/youtube-clone-vuive/scripts/nanobanana-pro-mascot-prompts-v3.1.md`
- Note: "đã verify checklist Mascot giống anh 9 items"

## Step 1 — Layer 1 STRUCTURAL

```bash
ls -la /Volumes/Storage-1/Hermes/wiki/projects/youtube-clone-vuive/scripts/nanobanana-pro-mascot-prompts-v3.1.md
# → -rw-------  1 tuananh4865  staff  7854 Jul 11 19:04 nanobanana-pro-mascot-prompts-v3.1.md

wc -l /Volumes/Storage-1/Hermes/wiki/projects/youtube-clone-vuive/scripts/nanobanana-pro-mascot-prompts-v3.1.md
# → 202 nanobanana-pro-mascot-prompts-v3.1.md
```

**L1 STRUCTURAL: PASS** — File exists, 7,854 bytes (exceeds 5 KB threshold for markdown docs), 202 lines.

## Step 2 — Layer 2 SEMANTIC (Decompose into 4 sub-claims)

| Sub-claim | Test |
|-----------|------|
| A) CHARACTER RESEMBLANCE section with messy fringe + brown crewneck + 92 tattoo | grep for "messy fringe", "brown crewneck", "92" |
| B) STYLE section: Western cartoon (NOT chibi), outline đen dày, flat color | grep for "NOT chibi", "outline", "flat color" |
| C) ≥4 hair-color variations (cyan/pink/purple/green) | grep for each color + count "Variation N" headers |
| D) Checklist exists with verifiable items | grep for `^- ✅` count |

**Greps run (all run, no cherry-picking):**

```bash
grep -ic "messy fringe" file → 12 matches
grep -ic "brown crewneck\|crewneck" file → 10 matches
grep -c "92" file → 3 matches (lines 27, 52, 108)
grep -in "NOT chibi\|NOT anime" file → 2 matches (lines 35, 176)
grep -in "outline.*black\|thick" file → multiple including line 57: "Outline is BLACK and THICK (~3-4px)"
grep -in "flat color" file → 3 matches (lines 61, 112, 194)
grep -ic "cyan" file → 4 matches
grep -ic "pink\|magenta" file → 4 matches
grep -ic "purple" file → 5 matches
grep -ic "green\|lime" file → 3 matches
grep -c "^- ✅" file → 10 matches
```

**Quoted evidence (with line numbers):**

- Sub-claim A — line 52: `Optional signature: small "92" tattoo visible on forearm`
- Sub-claim B — line 35: `Create a Western cartoon mascot portrait (NOT chibi, NOT anime)`
- Sub-claim B — line 61: `ALL FLAT COLOR FILLS only - NO gradients, NO shading`
- Sub-claim C — line 95: `### Variation 1: Cyan Blue + Brown áo (Tech - RECOMMENDED)`
- Sub-claim C — line 123: `### Variation 2: Magenta-Pink + Brown áo (Echo Vui Vẻ)`
- Sub-claim C — line 132: `### Variation 3: Electric Purple + Brown áo + White Pyramid Background`
- Sub-claim C — line 141: `### Variation 4: Lime Green + Brown áo`

**L2 SEMANTIC: PASS** — All 4 sub-claims have both grep-count evidence AND quoted lines.

## Step 3 — Layer 3 FUNCTIONAL

- Copy-paste ready? YES — Lines 34–89 fenced code block, lines 97–121 standalone Variation 1.
- Aspect ratio specified? YES — Line 84: `Aspect ratio 1:1`; line 120: `OUTPUT: 1:1 square, vector art`
- Output format specified? YES — `2D vector art style with clean edges, YouTube channel mascot/avatar format`

**L3 FUNCTIONAL: PASS** — Prompt is paste-ready.

## Step 4 — FAIL-FIRST Hypothesis Testing

Hypotheses written BEFORE running verifications:
- H1: "92 tattoo might be missing or vague" → grep `92` → 3 matches → HYPOTHESIS FALLS (feature IS present)
- H2: "Might only have 1-2 variations, not 4" → grep `### Variation` → 4 headers → HYPOTHESIS FALLS
- H3: "Checklist might be missing aspect ratio or style items" → grep `^- ✅` → 10 items covering messy fringe, brown crewneck, outline, tie, drop shadow, flat color → HYPOTHESIS FALLS

All three hypotheses fell — meaning the author's claims are robustly supported.

## Step 5 — Minor Observation

Author claimed "9 items" in checklist; file actually has **10** ✅ bullets (off-by-one, over-delivery, not under). Reported as observation, not failure.

## Final Verdict

```
VERDICT: PASS
L1 STRUCTURAL: PASS — 7,854 bytes, 202 lines
L2 SEMANTIC: PASS — 4/4 sub-claims have grep + quoted evidence
L3 FUNCTIONAL: PASS — copy-paste ready, aspect ratio + output format specified
```

**Minor:** Author claimed 9 checklist items, file has 10. Over-delivery, not failure.

## Lesson for Future Audits

1. **Run all greps even when you expect them to pass** — confirmation bias is the auditor's worst enemy
2. **Always count checklist items independently** — don't trust author's stated count
3. **Quote with line numbers, always** — vague quotes = fake audit
4. **FAIL-FIRST hypothesis list should be specific** — "feature X might be missing" beats "something might be wrong"