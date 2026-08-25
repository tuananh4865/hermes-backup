# Session 2026-07-12 — 4-Case Adversarial Validation + SOUL.md Self-Audit

> Companion to `adversarial-subagent-2026-07-12.md`. This file captures the FOUR-case validation that proved the protocol stable across domains, AND the lesson that the verifier can audit AGENT POLICY (SOUL.md) — not just outputs.

## Why this session matters

Previous reference (2026-07-12 first batch) documented 1 tested case (clip-0704 file spec FAIL). This file documents:
- **2 more test cases** (Mascot Vui Vẻ V3.1 PASS + 14 SKU Yonex PARTIAL_PASS)
- **1 meta-test** (verify SOUL.md itself — agent's own policy file)

The 4-case validation establishes the protocol as **stable across 4 distinct failure modes**:
1. **File spec** (ffprobe) — binary claim
2. **Content text** (grep + quote) — natural language claim
3. **Numeric data** (math computation) — financial/tabular claim
4. **System config** (multi-dim audit) — policy/process claim

If the verifier catches fail in each domain with different verification tools, the protocol generalizes — not a 1-trick pattern tied to video specs.

## 4 cases summary

| # | Case | Domain | Verdict | Tool | Key finding |
|---|------|--------|---------|------|-------------|
| 1 | Clip 0704 V5 | File spec | **FAIL** | ffprobe | 4/6 specs sai (width 608≠1080, height 1080≠1920, codec opus≠AAC, sr 48000≠44100) |
| A | Mascot Vui Vẻ V3.1 | Content text | **PASS** | grep + cat + quote | 4 sub-components (character/style/variations/checklist) all present; off-by-one noted (9 claimed → 10 actual = over-delivered) |
| B | 14 SKU Yonex | Numeric data | **PARTIAL_PASS** | awk/python math | Total 37,108,000 VND = 0% lệch (PASS) + 14 SKU = PASS + Margin rule: 2/14 SKU giày dùng MARKUP thay vì MARGIN (inconsistency) |
| C | SOUL.md (agent policy) | System config | **FAIL** | grep + 5-dim audit | 3 conflicts trực tiếp (Karpathy #1 vs Core #3), 6 redundant concepts, 4 outdated refs, 4 missing edge cases, 4 subjective rules |

## Case A — Mascot Vui Vẻ V3.1 (PASS with minor note)

**Author claim:** Prompt V3.1 có mascot giống anh + 4 variations + checklist 9 items.

**Verifier result:**
- L1 STRUCTURAL: file 7,854 bytes (7.85KB > 5KB threshold) ✅
- L2 SEMANTIC: 4 sub-components ALL present with quoted evidence:
  - CHARACTER RESEMBLANCE: messy fringe × 12 occurrences, brown crewneck × 10, "92" tattoo × 3
  - STYLE: "Western cartoon" + "outline BLACK and THICK (~3-4px)" + "ALL FLAT COLOR FILLS"
  - 4 variations: V1 Cyan, V2 Pink, V3 Purple, V4 Green (lines 95/123/132/141)
  - Checklist: present
- L3 FUNCTIONAL: aspect 1:1 specified, copy-paste ready
- **Verdict: PASS** with minor note: "Author claimed '9 items' but file has 10 ✅ bullets — off-by-one, but content is over-delivered"

**Key insight:** Verifier distinguished major fail vs minor off-by-one. Off-by-one in the FAVORABLE direction (over-delivered, not under) = PASS with note, not FAIL. **This is verifier quality signal** — false positive avoidance.

## Case B — 14 SKU Yonex (PARTIAL_PASS — margin vs markup confusion)

**Author claim:** "14 SKU + tổng 37,108,000 VND + margin rule đúng 100% (Play/Tour 30%, Pro 12-20%, Giày 25%)"

**Verifier result:**
- L1 STRUCTURAL: file `products-inventory.md` 3,207 bytes, 14 rows ✅
- L2 SEMANTIC:
  - A) Total 37,108,000 VND: computed sum = 0% lệch ✅
  - B) 14 SKU: counted rows = 14 ✅
  - C) Margin rule: **PARTIAL FAIL** — inconsistent formula in same file
    - 12 vợt rows: %LN/giá bán = MARGIN (đúng convention cho e-commerce)
    - 2 giày rows (#9, #10): %LN/giá nhập = **MARKUP** (different convention, unlabeled)
    - Giày 65z4: file shows 25.0% but margin (LN/giá bán) thực = 20.0%
    - Giày Subaxia: file shows 25.1% but margin (LN/giá bán) thực = 20.1%
- L3 FUNCTIONAL: format markdown chuẩn, Tier column rõ ràng
- **Verdict: PARTIAL_PASS** — không auto-FAIL vì chỉ 2/14 rows affected, nhưng flag terminology inconsistency

**Key insight:** Verifier catch "terminology drift" mà author không tự thấy. Author's claim "margin rule đúng 100%" đúng nếu hiểu "margin = LN/giá nhập" (markup), sai nếu hiểu "margin = LN/giá bán" (retail convention). **Verifier không quyết định convention đúng — author phải quyết — nhưng flag inconsistency để author biết.**

## Case C — SOUL.md Self-Audit (FAIL — agent policy audit)

**Author claim:** "SOUL.md đã cover tất cả edge case, 6 systems merged."

**Verifier result (5-dimensional audit):**

| Dim | Verdict | Evidence |
|-----|---------|----------|
| **1. Internal conflict** | **FAIL** | 3 conflicts: Karpathy #1 ("STOP, name confusion") vs Core #3 ("no follow-up question") — direct, unresolved |
| **2. Over-engineering** | **FAIL** | 6 redundant "QA everything" rules + 18 FIRST-CLASS sections + 69 total headers |
| **3. Outdated refs** | **FAIL** | 4 outdated paths: `Hermes-Edit/clip_0704...` (folder không tồn tại), `universal-verify/SKILL.md` (skill chưa tạo), `wiki/concepts/universal-verify-...` (page chưa tạo), `restart_gateway.sh` (script path sai) |
| **4. Missing edge case** | **FAIL** | 4 cases: 2 user requests conflict, 2 crons trùng giờ, no-input Telegram, cancel mid-task |
| **5. Execution risk** | **FAIL** | 4 subjective rules: "concise" (no threshold), "perfect" (no metric), "senior engineer" (rhetorical), "pass" (no exit criteria) |

**Top 3 fixes author applied (12/07/2026):**
1. **Resolve Karpathy #1 vs Core #3:** Changed line 76 from "STOP, name confusion" → "State assumption rõ + proceed with best guess"
2. **Cleanup 4 outdated paths:** Generic placeholder + bash command thật
3. **Consolidate 🎯 khẩu hiệu:** From "MỖI TOOL CALL" → "1 dòng SYSTEMS USED per task"

## Meta-lesson: Agent CAN verify its own policy

**The big win:** Verifier này không chỉ verify OUTPUT (clip/file/prompt/table) — nó verify cả **CHÍNH SÁCH CỦA AGENT** (SOUL.md). Đây là class mới:

| Verification class | What it audits | Example |
|-------------------|----------------|---------|
| File content | Text/markdown truthfulness | Mascot prompt V3.1, wiki page |
| File spec | Binary file metadata | Clip 0704 ffprobe |
| Numeric data | Tabular/computed claims | 14 SKU Yonex totals + margins |
| **Agent policy** | **Rule sets + system prompts** | **SOUL.md 5-dim audit** |

The 5-dim audit (Conflict / Over-engineer / Outdated / Missing / Subjective) is the right framework for any policy/prompt file. It catches failure modes that 3-layer alone misses — a file can pass all 3 layers (file exists / content matches / runs) but still have a broken rule set.

## Failure mode catalog (4 domains × their tools)

| Domain | Best tool | What it catches | Reference |
|--------|-----------|-----------------|-----------|
| File content | `grep -c` + `cat` + quote | Fabricated/missing text | Case A |
| File spec | `ffprobe -show_entries ...` | Wrong codec/dimensions/sr | Case 1 |
| Numeric data | `awk` or `python` math | Margin/markup confusion, total mismatch | Case B |
| Agent policy | `grep` paired rules + count `##` headers + check outdated paths | Internal conflict, redundancy, outdated refs | Case C |

**Rule of thumb:** Each domain has its OWN built-in inspector. Verifier MUST use the right tool for the domain. Custom scripts em viết = verify-chasm bias risk.

## What this session proved

1. **Protocol generalizes across 4 domains.** Not a 1-trick for video specs.
2. **Verifier distinguishes major from minor.** Case A: off-by-one = PASS with note, not FAIL.
3. **Verifier can audit AGENT POLICY.** 5-dim audit catches rule-set failures that 3-layer alone misses.
4. **Terminology drift is a real failure mode.** Case B: "margin" vs "markup" — author không tự thấy, verifier catch.
5. **Subagent rejects vacuous PASS.** Prompt template demands raw data — subagent returns verdict with concrete numbers, không nói "looks good".

## Cross-reference

- `references/session-2026-07-12-file-spec-fail-claim.md` — Original Case 1 detail
- `references/adversarial-subagent-2026-07-12.md` — Prompt template + worked example
- `references/incident-2026-07-05.md` — Original fabrication incident
- `skills/media/tiktok-verify-protocol/SKILL.md` — Domain-specific verify (TikTok video)
- SOUL.md § "ADVERSARIAL SUBAGENT VERIFIER (FIRST-CLASS)" — System-wide rule

## Future enhancements (deferred — DO NOT implement until asked)

1. **Auto-trigger 5-dim audit on policy changes** — whenever SOUL.md is patched, auto-dispatch verifier to check 5 dims. Prevents the agent from over-confidently self-patching policy without independent review.
2. **Margin/markup convention linter** — domain-specific tool for inventory/pricing tables. Suggests formula labels based on table context.
3. **Cross-domain verifier dispatch** — when task spans multiple domains (e.g. "edit video + write content + update pricing"), dispatch separate subagent for each domain. Prevents 1 subagent trying to verify everything.

Listed for completeness. Implementing now = over-engineering, exactly what user told agent NOT to do.