---
name: system-wide-mandate-enforcement
description: Enforce a system-wide mandate (rule/policy/pattern) across all Hermes SOUL.md files, profiles, plugins. Includes 3-piece enforcement (shared ref + refactor consumers + idempotent injector + CI gate + auto-check hook) and harness engineering to reduce context tokens. Always verify BEFORE mass propagation — distinguish SAFE/RISKY/NEVER. Verify upstream concept exists in official docs before scaffolding files for it.
---

# System-Wide Mandate Enforcement

When user says "make X mandatory across the entire system" or "apply X to current AND future", follow this exact workflow.

## Trigger Conditions

- User requires a rule/policy/pattern to apply BẮT BUỘC (mandatory) system-wide
- User wants harness engineering (token reduction) while maintaining quality
- User asks "đã áp dụng system-wide chưa?"

## Anti-Pattern (NEVER DO)

- Ask user "anh muốn X hay Y?" — user đã rõ ràng, tự quyết
- Apply mù quáng vào tất cả files — phải verify từng chỗ
- Touch core code (AGENTS.md cấm)
- Add to MEMORY.md khi đầy — tốn token mãi mãi
- Skip the verify step — sẽ break hệ thống
- **Build infrastructure for a concept you can't cite from official docs** — if the term isn't in the framework's canonical docs, either use the closest official concept or ask the user before scaffolding
- **Use `clarify` tool after user says "verify" or "decide for me"** — see `hermes-agent-decision-guard` skill for the meta-rule on when to ask vs decide
- **Claim "DONE" before behavior audit** — keyword presence ≠ substance. Run self-audit before claiming compliance (see Step 7 below)
- **Skip source coverage report** — when harvesting from a source doc, list SKIPPED sections explicitly, not just what you brought over
- **Claim "Done" without evidence** — Tuấn Anh has strict QA mindset. Always attach file paths, line counts, mtimes, exit codes (see Step 9)

## Step 7: Behavior Audit + Source Coverage

After your compliance gate PASSES and before reporting "DONE" to the user, run TWO audits:

**Audit A — Behavior audit (does the pattern actually change behavior?):**

```
For each pattern P in the mandate:
1. Cite 1-2 evidence points where I (or any new agent) actually applied P in a real task
2. If I CAN'T cite evidence → P is not applied, just referenced
3. If evidence is partial → report PARTIAL, not DONE
```

**Audit B — Source coverage (did you harvest everything?):**

```
Original doc sections: [list all from source]
Harvested sections: [list what I brought over]
SKIPPED sections: [list what I didn't bring over + reason]

If SKIPPED is non-empty → report it explicitly to user
```

**Rule:** Don't claim "Mandate applied system-wide" until audits A + B are done. Better to report "1/4 patterns fully applied, 3 PARTIAL, source coverage 4/11 sections" than to overclaim.

## Step 8: Idempotent Script QA Protocol (NEW, learned 2026-06-16)

**After writing any idempotent script (injector, refactor, batch), run 3-tier QA BEFORE claiming "done":**

| Tier | Test | Why |
|------|------|-----|
| **Tier 1: Fresh file** | Empty file → run script → expect CORRECT add | Verify happy path |
| **Tier 2: Re-run on modified file** | File with target content already → run script → expect SKIP | Verify idempotency |
| **Tier 3: Edge cases** | File with PARTIAL content → run script → expect CORRECT add | Verify robustness |

**Real bugs caught by this protocol (2026-06-16, fable5-injector):**

| Bug | Tier caught it | Symptom | Cause | Fix |
|-----|---------------|---------|-------|-----|
| Bug #1: Section name mismatch | Tier 2 | Main SOUL.md grew 419→457 lines on re-run | Grep matched keyword but didn't check structural element | Add AND condition: section name + shared-ref link |
| Bug #2: Fresh file re-inject | Tier 2 | Fresh file injected twice (1st: 27 lines, 2nd: 38 lines) | Case-insensitive grep matched "Fable-5" anywhere | Use case-sensitive grep for exact section name |

**Rule:** Any idempotent script MUST pass all 3 tiers. Run them as part of the verify phase, not after.

**QA script:** See `scripts/qa-injector.sh` (in this skill) for the runnable 3-tier QA template.
**Full reference:** See `references/idempotent-script-qa-protocol.md` for the 2 real bugs + 8-point checklist + bash template.

## Step 9: Evidence-Based Reporting Template (NEW, learned 2026-06-16)

**Tuấn Anh has a strict QA mindset. "Done" claims without evidence = "claimed done quá sớm" failure mode.**

**MANDATORY evidence in every "system-wide mandate applied" report:**

| Evidence type | Example | Why |
|---------------|---------|-----|
| File path | `~/.hermes/SOUL.md` | Traceability |
| Line count before/after | 419 → 457 lines | Quantifies change |
| File mtime | `2026-06-16 18:48` | Proves write happened |
| File size | `5,506 bytes` | Sanity check |
| Exit code | `exit 0` | Proves command succeeded |
| MD5 (for binary/originals) | `md5: abc123...` | Proves identity |
| Diff (for refactors) | `-5 +3` | Quantifies reduction |

**Anti-patterns:**
- ❌ "Updated X files" (no paths, no counts, no evidence)
- ❌ "All checks PASS" (no exit codes, no output)
- ❌ "Should work now" (no verification, just claim)
- ✅ "5/5 SOUL.md updated: `~/.hermes/SOUL.md` (419→457 lines, mtime 18:48), compliance check exit 0, 4/4 patterns verified"

**Self-audit questions BEFORE writing "DONE":**
1. Can I cite file paths + line counts for every claimed change?
2. Can I show exit codes for every claimed "PASS"?
3. Have I run the script in 3 tiers (fresh, re-run, edge case)?
4. Have I found any caveat, or did I claim "perfect"?

If answer to any is "no" → don't write "DONE" yet.

## Phase 0: Verify Upstream Concept (NEW, learned 2026-06-16)

**Before scaffolding anything for a new term/concept, confirm it exists in canonical source.**

For Hermes: check `hermes-agent.nousresearch.com/docs/` — search for the term, read the relevant page, confirm the concept has a real implementation path.

If the term has NO official equivalent, the user's request may have been approximate. Surface this BEFORE building 25 files of dead infrastructure.

**Rule for path proposals:**
- `~/.hermes/profiles/<name>/` → official (Profile)
- `~/.hermes/kanban/`, `~/.hermes/cron/`, `~/.hermes/skills/`, `~/.hermes/hooks/`, `~/.hermes/memories/` → official (Kanban, Cron, Skills, Hooks, Memory)
- `~/.hermes/workers/`, `~/.hermes/agents/`, `~/.hermes/nodes/`, `~/.hermes/team/` → **NOT official** — likely built on a non-canonical concept
- Anything else → verify in `hermes-agent.nousresearch.com/docs/` before using

## Workflow (3 phases)

### Phase 1: VERIFY (BẮT BUỘC — không được skip)

**Mục tiêu:** Phân loại các chỗ cần propagate thành 3 nhóm:

| Nhóm | Đặc điểm | Action |
|------|----------|--------|
| 🟢 SAFE | SOUL.md, wiki pages, hooks dir, profile configs | Apply ngay |
| 🟡 RISKY | Cron prompts đang chạy, scripts đang chạy, active workers | Verify kỹ, có thể skip |
| 🔴 NEVER | Core code, memory khi đầy, env files, .env | KHÔNG động vào |

**Bước thực hiện:**

```bash
# 1. List all files có thể chứa rule
find ~/.hermes -name "SOUL.md"  # SOUL files
find ~/.hermes/hooks -type d    # hooks
ls ~/.hermes/profiles/*/SOUL.md # profiles
ls ~/.hermes/cron/output/        # cron outputs (để check prompts)
wc -c ~/.hermes/memories/*.md    # memory size
```

**Output:** Bảng phân loại theo SAFE/RISKY/NEVER.

### Phase 2: APPLY (3-piece enforcement)

**Piece 1: Shared reference file**
- Tạo `~/.hermes/profiles/_shared/<name>.md` chứa FULL detail
- Token reduction: 1 nơi chứa full, các file khác chỉ reference

**Piece 2: Refactor consumers**
- Mỗi file (SOUL.md, etc.) thay inline 30+ dòng bằng 12 dòng reference + link
- Bảng tóm tắt 1-line cho mỗi pattern (vừa đủ keyword cho CI gate)
- Idempotent: chạy nhiều lần không break

**Piece 3: CI gate + Auto-check hook**
- Script: `~/.hermes/scripts/check-<name>-compliance.sh` — check keyword markers
- Hook: `~/.hermes/hooks/<name>-check/` — auto-run on `session:start`, **WARN only, NEVER block** (theo AGENTS.md)
- Future-proof: thêm script `add-<name>-to-<file>.sh` cho files mới

### Phase 3: VERIFY (cuối cùng)

**Báo cáo phải có (theo Step 9 Evidence-Based Reporting):**
1. List files đã update (với line count before/after + mtime + size)
2. Compliance check kết quả (PASS/FAIL + exit code)
3. Hook test result (exit code + output)
4. Idempotent script QA result (3 tiers PASS/FAIL)
5. Token reduction tổng (lines saved, % reduction)
6. List files SKIPPED (và lý do)
7. Quality verification (đủ pattern, không giảm chất lượng)
8. Audit A + B (Step 7) — behavior + source coverage

## Templates

### Template 1: Shared Reference File

```markdown
# <Name> — Detail Reference

> **Purpose:** This file holds the FULL detail of <N> patterns.
> **Why separate:** SOUL.md files reference this via 1-line link, saving ~30 lines per SOUL.md.
> **Mandate:** <user> required these patterns BẮT BUỘC on entire system (<date>).
> **Enforcement:** `~/.hermes/scripts/check-<name>-compliance.sh` checks every SOUL.md has a reference to this file.

## Source
- Origin: <source>
- Method: <method>
- Date: <date>

## Pattern 1: <Name>
... (full detail)

## Pattern 2: <Name>
... (full detail)
```

### Template 2: Compliance Check Script

```bash
#!/bin/bash
# <Name> Enforcement Checker
set -e
HERMES_ROOT="${HOME}/.hermes"
PATTERNS=(
  "PATTERN_1_KEY"
  "PATTERN_2_KEY"
  # ...
)
SOUL_FILES=$(find "$HERMES_ROOT" -name "SOUL.md" -type f -not -path "*/docker/*" 2>/dev/null)
FAILED=0
for file in $SOUL_FILES; do
  MISSING=()
  for pattern in "${PATTERNS[@]}"; do
    if ! grep -qi "$pattern" "$file"; then
      MISSING+=("$pattern")
    fi
  done
  # ...report PASS/FAIL
done
```

> **Note:** Do NOT scan arbitrary directories like `~/hermes/workers/` unless that path is part of an official framework concept.

### Template 3: Auto-Check Hook (handler.py)

```python
"""<Name> Compliance Check Hook
Runs on session:start. Verifies all <files> have the required <N> patterns.
Warns (logs) if any file is missing. NEVER blocks (per AGENTS.md).
"""
import os, sys
from pathlib import Path

HERMES_ROOT = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
PATTERNS = [...]  # keyword markers

def find_files():
    # Skip docker templates
    return [p for p in HERMES_ROOT.rglob("SOUL.md") if "docker" not in str(p)]

def main():
    files = find_files()
    issues = []
    for f in files:
        content = f.read_text(encoding="utf-8").upper()
        missing = [p for p in PATTERNS if p not in content]
        if missing:
            issues.append((f, missing))
    if issues:
        print(f"[<name>-check] ⚠️  {len(issues)} file(s) missing patterns:")
        for f, m in issues:
            print(f"  - {f}: {m}")
    else:
        print(f"[<name>-check] ✅ All {len(files)} files comply")
    return 0  # NEVER block

if __name__ == "__main__":
    sys.exit(main())
```

### Template 4: HOOK.yaml

```yaml
name: <name>-compliance-check
description: Auto-verify <name> patterns present in all SOUL.md files on session start. Warn-only, never block.
events:
  - session:start
version: "1.0"
```

## Token Reduction Math (typical)

| File type | Before (inline) | After (ref) | Saved |
|-----------|-----------------|-------------|-------|
| Main SOUL.md (4 patterns × 30 lines) | 154 lines | 22 lines | 132 (86%) |
| Profile SOUL.md (3 files) | 38 lines each | 12 lines each | 26 each (68%) |
| **Total** | **268 lines inline** | **58 lines inline + 154 lines shared** | **210 lines saved per session** |

> **Note:** This skill is for SOUL.md files only. Hermes "Worker" is NOT an official concept — use **Profile** (`hermes profile create`) or **Sub-agent** (`delegate_task`) for worker-like behavior. See Hermes docs: `hermes-agent.nousresearch.com/docs/user-guide/profiles`.

## Quality Bar

- 4 patterns phải reference đầy đủ trong mỗi file
- Full detail ở shared file (1 nơi duy nhất)
- Compliance gate đảm bảo không miss pattern
- Idempotent scripts an toàn re-run (passes 3-tier QA per Step 8)
- Hook WARN only, NEVER block
- AGENTS.md compliance: extend, don't duplicate; harness engineering; don't touch core
- Every "DONE" report includes evidence per Step 9

## Real Example: Fable-5 Mandate (2026-06-16)

**Context:** Tuấn Anh required 4 patterns from Claude Fable 5 (MCP Connector, Persistent Storage, Skills-First, Search Discipline) to apply BẮT BUỘC across all Hermes.

**Result:**
- 4 SOUL.md files updated (1 default + 3 profiles: coder, content-director, research-lead)
- 1 shared reference file (`profiles/_shared/fable5-patterns.md`)
- 2 enforcement scripts (check + add) — **failed 3-tier QA initially** (Bug #1: section name mismatch, Bug #2: case-insensitive grep). Fixed by adding AND condition + case-sensitive grep.
- 1 auto-check hook (`hooks/fable5-compliance-check/`)
- Token reduction: 210+ lines saved per session
- All compliance checks PASS
- Hook WARN only, never blocks
- Real research task validated behavior change: 4/4 patterns applied + 37/40 honest score (2 caveats reported)

**Skipped:**
- Cron job prompts (7 jobs đang chạy OK — rủi ro break automation)
- MEMORY.md (đầy 100%, sẽ tốn token mãi mãi)
- Core code (AGENTS.md cấm)

**Cleanup story (the "Worker" trap):** Initially built 3 "Worker" skeleton files based on a vague concept. When user asked to verify the concept against official docs, discovered Hermes has NO "Worker" concept — only Profile and Sub-agent. Deleted 25 files. Lesson: verify concept in upstream docs first, especially when the concept name sounds like a generic term ("worker", "agent", "node") that may not match the framework's vocabulary.

**Loop Engineering hit the same trap (2026-06-16):** Designed state files at `~/.hermes/workers/{name}/state.md` instead of `~/.hermes/profiles/{name}/state.md`. Patched the loop-engineering-deployment skill with "Hermes Profile vs Worker" section. Both skills now share the same upstream-verification discipline (see Phase 0 above).

## Related

- `~/.hermes/profiles/_shared/fable5-patterns.md` — first implementation
- `~/.hermes/scripts/check-fable5-compliance.sh` — CI gate
- `~/.hermes/scripts/add-fable5-to-soul.sh` — idempotent injector (fixed for 3-tier QA)
- `~/.hermes/hooks/fable5-compliance-check/` — auto-check hook
- `references/idempotent-script-qa-protocol.md` — 2 real bugs + 8-point checklist + bash template
- `scripts/qa-injector.sh` — runnable 3-tier QA script
- `hermes-agent-decision-guard` — meta-rule: when to ask user vs when to decide. Read this when in doubt about whether to use `clarify` tool.
