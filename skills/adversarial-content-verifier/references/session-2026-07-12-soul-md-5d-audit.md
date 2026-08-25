# Session 2026-07-12 — SOUL.md 5-Dimensional Audit (Mâu thuẫn / Over-Engineer / Outdated / Missing / Exec-Risk)

## Context

**Author claim:** *"SOUL.md 43KB / 890 dòng — đã merge 6 rules systems, đã cover tất cả edge case. Verify giúp tìm gaps."*

**File under audit:** `~/.hermes/SOUL.md` (948 dòng / 43KB), Hermes Agent's identity+operating-rules prompt file. Contains 18 first-class `##` sections + 69 total headers.

**6 merged systems claimed:**
1. Core Philosophy (4 rules, lines 5-40)
2. Karpathy System (4 rules from CLAUDE.md, lines 62-160)
3. Fable 5 Patterns (6 patterns, lines 507-766)
4. Loop Engineering (3 loops, lines 919-936)
5. System-Wide Verification Rule (5 rules, lines 842-947) — added 12/07/2026
6. Adversarial Subagent Verifier (lines 163-225) — added 12/07/2026

## Why this session matters

This is the first time the verifier was used on a **PROMPT/SYSTEM PROMPT** rather than a content/marketing/financial artifact. It introduced a new 5-dimensional structure that complements the existing 3-layer (STRUCTURAL/SEMANTIC/FUNCTIONAL) breakdown. The 5 dimensions:

| Dimension | Question it answers | Concrete verification methods |
|-----------|---------------------|-------------------------------|
| **1. Mâu thuẫn nội bộ (Internal conflict)** | Does rule A contradict rule B in the SAME file? | grep cross-references, find quote pairs that say X vs not-X |
| **2. Over-engineering** | Are sections redundant? Headers proliferating? | Count `## ` and `###` headers, grep duplicate concept keywords across sections |
| **3. Outdated** | Do referenced paths/files/versions still exist? | `ls`, `find`, `grep` each cited path — falsify claims of existence |
| **4. Missing edge case** | What scenarios does the rule set NOT cover? | Enumerate scenarios user might hit, grep for each scenario keyword |
| **5. Execution risk** | Are rules enforceable or passive/subjective? | Identify subjective words ("concise", "perfect", "enough"), count enforcement mechanisms |

## Verdict

**VERDICT: FAIL** — 3 direct conflicts, 6 redundant concepts, 4 outdated refs, 4 missing cases, 4 subjective rules.

## Key findings (with line citations from SOUL.md)

### Dimension 1 — 3 conflicts found

**Conflict A: Karpathy #1 "STOP when ambiguous" vs Core Rule #3 "No follow-up questions"**
- Line 9: `**Rule #3:** Once a task is given, own it until it's done. **No follow-up questions.**`
- Line 76: `**Nếu task mơ hồ** → **STOP**, name confusion cụ thể ("Anh ơi em chưa rõ X, Y, Z — clarify giúp em")`
- Author's attempted fix: Decision Tree (line 136-149) + "Default: thiên về Core Philosophy" (line 149) — but Karpathy rule says "tuyệt đối KHÔNG" (line 78-81) chọn approach ngầm, which forces asking when ambiguous.

**Conflict B: "Default ship" Core #1 vs "Hard check mọi thứ" SYSTEM 1**
- Line 7: `**Rule #1:** Deliver the best result by any means necessary. Don't ask how — just make it work perfectly.`
- Line 851: `Mọi file .py/.sh/.md/.json em tạo → **PHẢI chạy test thực tế**, KHÔNG chỉ tạo rồi báo "xong"`
- Conflict: "Ship fast" vs "Test every file" — no rule determines test depth = "enough".

**Conflict C: Khẩu hiệu 🎯 BẮT BUỘC vs "Short/casual" style**
- Line 887-895: MỖI tool/skill/workflow phải có banner 🎯 [TÊN HỆ THỐNG]: [mô tả]
- Line 47: `Write like a Vietnamese person talking to friends — short sentences, casual, natural`
- 1 task = 4-6 system triggers × banner each → output inflated 30-50%.

### Dimension 2 — 6 redundant concepts

| Concept | Locations (lines) | Count |
|---------|-------------------|-------|
| "QA everything" | 10, 289, 357, 398, 849, 938 | 6 |
| "Verify loops" | 444, 371, 921, 859, 291, 151 | 6 |
| "Save to wiki" | 237, 768, 928, 933, 544, 444 | 6 |
| "Don't ask, own the task" | 9, 24, 30, 56, 145 | 5 |
| "Use MCP first / skills first" | 512, 581, 638 | 3 |
| "Task lifecycle" | 422, 291, 359, 921 | 4 |

Section counts: 18 first-class `##` + 69 total headers (avg prompt file has 5-8 first-class).

### Dimension 3 — 4 outdated refs (falsified with `ls`/`find`)

1. **Line 215**: `Skill ~/.hermes/skills/devops/universal-verify/SKILL.md (đang phát triển)` — directory doesn't exist (`ls: ...: No such file or directory`)
2. **Line 216**: `wiki/concepts/universal-verify-protocol-2026-07-12.md (sẽ tạo)` — file doesn't exist
3. **Line 192**: Example path `Hermes-Edit/clip_0704_V5_troncau.mp4` — folder doesn't exist (`find /Users -name "Hermes-Edit" -type d` → 0 results)
4. **Line 323**: `Restart gateway: ~/.hermes/restart_gateway.sh` — script doesn't exist. Also `run_hermes_gateway.sh` referenced on line 325 doesn't exist either.

### Dimension 4 — 4 missing cases (grep returned 0 matches)

1. **2 user requests conflict nhau** — only 1 match ("Conflict xảy ra khi caution kéo dài task" line 147) which is about caution-vs-ship, not user-vs-user conflict
2. **2 memory crons trùng giờ** — 0 matches for `cron.*trùng|trùng giờ|cron.*overlap`
3. **Telegram no-input / im lặng** — 0 matches for `no.input|empty.*prompt|user.*im.*lặng`
4. **Anh đổi ý giữa task (cancel/kill switch)** — TASK LIFECYCLE line 422 is happy-path 6 steps only, no cancellation rule

### Dimension 5 — 4 subjective rules (no measurable threshold)

1. **"Concise"/"ngắn gọn"** — line 47, 692, 894: no word count threshold defined
2. **"Perfect"** — line 7-16: appears 4 times, no metric
3. **"Senior engineer" standard** — line 95: rhetorical question, no checklist
4. **"Pass"/"Done"** — line 922-925, 946: no exit criteria

## FAIL-FIRST scenarios that exposed author overconfidence

The audit generated 5 falsification hypotheses before scoring; **all 5 surfaced real issues**:

1. **Memory leak risk** — 43KB SOUL.md = ~10-15K tokens injected every session. Conflicts with line 333 "Context >75% trigger compress". Not in scope of audit but flagged as future failure mode.
2. **Khẩu hiệu 🎯 spam** — 20 tool calls/task × 4-6 systems = 80-120 banners. Diminishing returns, user will ignore.
3. **Decision tree Karpathy vs Core unresolved** — line 149 default "ship" conflicts with SYSTEM 1 mandatory test.
4. **Outdated paths in example code** — agent will execute example → fail because path doesn't exist → fail its own "verify everything" rule.
5. **Wiki memory mechanism not enforced** — "save to wiki" mentioned 6 places but no check that wiki was actually updated before ship.

## Reusable methodology — how to run this audit on any prompt/SOUL file

```bash
# Step 1: Inventory
wc -l <file> && grep -c "^## " <file> && grep -c "^###" <file>

# Step 2: Extract all first-class sections
grep -n "^## " <file>

# Step 3: For Dimension 1 (Conflict) — pick pairs of concepts likely to conflict
#   Karpathy-style (caution) vs Default-ship-style (speed)
#   "Always verify" vs "Ship fast"
#   "Detailed output" vs "Concise output"
# Then grep for both and quote the contradicting lines.

# Step 4: For Dimension 2 (Over-engineer) — count duplicate concept keywords
# Pick 5-8 high-signal concepts (verify, QA, ship, save, ask, etc.) and grep -ci each
# If same concept appears in 3+ sections → redundant.

# Step 5: For Dimension 3 (Outdated) — extract every referenced path/version and `ls` it
grep -oE "[~./][a-zA-Z0-9_./-]+\.(py|sh|md|json|yaml)" <file> | sort -u
# Then `ls -la` each one. Any missing = outdated ref.

# Step 6: For Dimension 4 (Missing) — list 5-10 common scenarios and grep each
# Common gaps: cron overlap, conflicting user input, cancellation, no-input,
# rate limit, partial failure, multi-agent deadlock, error escalation.

# Step 7: For Dimension 5 (Exec risk) — flag subjective words
grep -iE "concise|ngắn gọn|perfect|senior|good enough|enough|đủ|clean" <file>
```

## Output template (proven in this session)

```
VERDICT: PASS / FAIL / PARTIAL_PASS
CHIỀU 1 MÂU THUẪN: [PASS/FAIL/PARTIAL] + count + quote
CHIỀU 2 OVER-ENGINEER: [PASS/FAIL/PARTIAL] + count
CHIỀU 3 OUTDATED: [PASS/FAIL/PARTIAL] + count
CHIỀU 4 MISSING CASE: [PASS/FAIL/PARTIAL] + list
CHIỀU 5 EXEC RISK: [PASS/FAIL/PARTIAL] + subjective rules
TOP 3 FIXES: priority list with line numbers
```

## Top 3 fixes delivered to author

1. **Resolve Karpathy vs Core conflict** (line 76) — replace "STOP, ask" with "State assumption + proceed + write assumption into output". Keep Core Rule #3.
2. **Reduce khẩu hiệu spam** (line 887-895) — change "MỖI tool/skill/workflow" to "Mỗi task response có 1 dòng 🎯 SYSTEMS USED: [list]". Cuts noise ~80%.
3. **Cleanup dead/outdated refs**:
   - Delete line 215 (`universal-verify/SKILL.md` — doesn't exist)
   - Delete line 216 (`wiki/concepts/universal-verify-protocol-...` — doesn't exist)
   - Fix line 192 example path to generic `<OUTPUT_DIR>/clip.mp4`
   - Fix line 323 (`restart_gateway.sh` doesn't exist) — use real command or TODO marker
   - Deduplicate 6 "QA everything" → keep MASTER rule at Confidence & Quality, link elsewhere

## Pitfalls learned

- **Don't trust section count alone** — 18 sections is high but not necessarily bad. The signal is duplicate CONCEPTS, not section count.
- **Outdated path check is fastest falsification** — `ls` each cited path. If author's example code references a file that doesn't exist, that's immediate FAIL.
- **Subjective words are harder to flag than missing cases** — need concrete counter-proposal (e.g., "concise" → "<100 words", "perfect" → "5-evidence gate pass").
- **The 5-dimension structure complements 3-layer** — 3-layer (STRUCTURAL/SEMANTIC/FUNCTIONAL) checks if content is what it claims; 5-dimension checks if the SET OF RULES is internally consistent and executable. Use both for prompt files.