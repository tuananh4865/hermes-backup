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
- "Claim "Done" without evidence" — Tuấn Anh has strict QA mindset. Always attach file paths, line counts, mtimes, exit codes (see Step 9)
- **Nhảy vào action liền khi user yêu cầu task lớn** — User preference 17/06: *"Anh thích em RESEARCH trước khi làm"*. Research = Step 0 của bất kỳ work nào. See `project-workflow-v2` v2.1.
- **Patch a mandate that lives across 3+ files, then claim DONE without cross-file consistency audit (NEW 2026-07-30).** When a rule touches SOUL.md + umbrella skill + cross-ref skill + wiki entity together, single-file grep PASS hides internal contradictions. Real case: `evidence-gate pitfall #9` was patched correctly in its own file, but SOUL.md still had `Subagent MANDATORY cho task 🔴 LARGE` heading 30 lines below new `MỌI TASK` wording — per-file `grep "MỌI TASK"` returned 1 match, file "compliant", but rule was self-contradictory. Fix recipe in `references/coupled-artifacts-audit-2026-07-30.md`: enumerate all coupled files via `grep -rl "<old-wording>"`, patch all in one session, audit with `rule_marker AND counter_rule (±50 lines)` per file, report all-or-none.

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

**Mục tiêu:** Phân loại các chỗ cần propagate thành 4 nhóm:

| Nhóm | Đặc điểm | Action |
|------|----------|--------|
| 🟢 SAFE | SOUL.md, wiki pages, hooks dir, profile configs | Apply ngay |
| 🟡 RISKY | Cron prompts đang chạy, scripts đang chạy, active workers | Verify kỹ, có thể skip |
| 🟠 CRON | Cron job prompts (LLM jobs) | Inject mandate reminder block vào `~/.hermes/cron/jobs.json` prompts |
| 🔴 NEVER | Core code, memory khi đầy, env files, .env | KHÔNG động vào |

**Bước thực hiện:**

```bash
# 1. List all files có thể chứa rule
find ~/.hermes -name "SOUL.md"  # SOUL files
find ~/.hermes/hooks -type d    # hooks
ls ~/.hermes/profiles/*/SOUL.md # profiles
ls ~/.hermes/cron/output/        # cron outputs (để check prompts)

# 2. CRON CHECK — scan all LLM cron jobs for mandate reference
hermes cron list
# For each job with no_agent=False AND has prompt:
#   - Check if prompt contains mandate marker
#   - If NO → inject reminder block (see Cron Injection below)
```

**Output:** Bảng phân loại theo SAFE/RISKY/CRON/NEVER.

**Why CRON is a separate category (lesson 2026-06-17):** When user said "yên tâm 100% system-wide" after Fable-5 mandate, em verified SOUL.md + hooks + shared ref + scripts — all PASS. But cron jobs were missed: 0/7 LLM jobs had Fable-5 reference. If user asked "yên tâm tương lai?" the answer would have been false-positive. Cron jobs run at 2AM/3AM/7AM/7:30AM/8AM every day — they execute in fresh agent context, so a mandate applied only to current session's SOUL.md does NOT propagate. Inject the mandate reminder block into each LLM cron prompt.

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

**Piece 4: Cron job mandate injection (lesson 2026-06-17)**
Cron jobs run in fresh agent context — a mandate applied to current session's SOUL.md does NOT propagate. Inject a reminder block into each LLM cron prompt:

```python
import json, shutil
from datetime import datetime

MANDATE_REMINDER = '''

---

## 🆕 <MANDATE_NAME> (YYYY-MM-DD) — APPLY ON THIS JOB

This job must follow <N> mandatory patterns from <source> (see `~/.hermes/profiles/_shared/<name>.md`):

1. **<Pattern 1>**: <1-line rule>
2. **<Pattern 2>**: <1-line rule>
3. **<Pattern 3>**: <1-line rule>
4. **<Pattern 4>**: <1-line rule>

**Voice rule (YYYY-MM-DD):** For <user> content → <voice rule>.
**Banned phrases:** <list of TRÁHN-style banned phrases>.
'''

# Load jobs.json
jobs_path = "/Users/tuananh4865/.hermes/cron/jobs.json"
with open(jobs_path) as f:
    data = json.load(f)

# Backup
shutil.copy(jobs_path, f"{jobs_path}.pre-<mandate>-{datetime.now().strftime('%Y%m%d-%H%M')}")

# Inject into LLM jobs only
for job in data["jobs"]:
    if job.get("no_agent"):  # Skip script-only jobs
        continue
    if not job.get("prompt"):
        continue
    if "MARKER_STRING" in job["prompt"]:  # Idempotent: check first
        continue
    job["prompt"] = job["prompt"].rstrip() + "\n" + MANDATE_REMINDER

with open(jobs_path, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**Cron injection QA — verify after injection:**
```bash
# For each LLM cron job, check marker presence
hermes cron list  # Get all job IDs
# For each: jq -r '.jobs[].prompt' ~/.hermes/cron/jobs.json | grep -c "MARKER_STRING"
# Should equal count of LLM jobs (skip no_agent=True)
```

**Real numbers from 2026-06-17 Fable-5:** 5/5 LLM cron jobs got Fable-5 reminder injected (Backup, Autoresearch, X Research, Session Review, TikTok Monitor). 2/7 no_agent jobs (Wiki Health, Wiki Forget) skipped — they run scripts, not LLM.

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

def check_file(f: Path) -> list:
    """Return list of missing pattern names."""
    try:
        content = f.read_text(encoding="utf-8").upper()
    except Exception as e:
        return [f"READ_ERROR: {e}"]
    return [p for p in PATTERNS if p not in content]

def handle(event_type: str, context: dict) -> None:
    """
    Hook entry point. Called by gateway on session:start event.

    Context dict may contain:
      - session_id: str
      - platform: str
      - user_id: str
    """
    try:
        if event_type != "session:start":
            return

        files = find_files()
        issues = [(f, check_file(f)) for f in files if check_file(f)]

        if issues:
            print(f"[<name>-check] ⚠️  {len(issues)}/{len(files)} file(s) missing patterns:")
            for f, m in issues:
                print(f"  - {f}")
                for x in m:
                    print(f"      • {x}")
        else:
            print(f"[<name>-check] ✅ All {len(files)} files comply")

    except Exception as e:
        print(f"[<name>-check] Hook error (non-fatal): {e}", file=sys.stderr)

if __name__ == "__main__":
    handle("session:start", {})
    sys.exit(0)
```

**CRITICAL — Function name MUST be `handle` (lesson 2026-06-17):** Gateway hook discovery requires the entry point to be named exactly `def handle(event_type, context)`. Any other name (`main`, `on_event`, `run`, `main_with_args`, etc.) = silently rejected with log line `[hooks] Skipping YOUR_HOOK: no 'handle' function found`. The hook will work standalone (`python3 handler.py`) but NEVER fire on real events. See `self-verify-after-workaround` skill → "Gateway Hook Discovery Requires `def handle()`" for the full diagnostic recipe.

**Verification command after writing hook:**
```bash
# Did gateway discover it?
tail -50 ~/.hermes/logs/gateway.log | grep -E "Loaded|Skipping.*YOUR_HOOK"
# "Loaded" = good
# "Skipping" = function name wrong, fix it
# No output = gateway not reloaded OR hook not in ~/.hermes/hooks/
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
- 5-Layer Verification Matrix: run `scripts/verify-5-layers.sh <mandate-name>` before claiming "100% system-wide"

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

**Real Example: Project Workflow v2 → v2.1 (2026-06-17, same day 2 sessions later)**

**Context:** Built `project-workflow-v2` skill with 4-step loop (PLAN→EXECUTE→VERIFY→NEXT). User feedback at 10:50: *"kỹ năng research là một kỹ năng bắt buộc và rất quan trong nhưng sao hầu hết trong các patterns, loop và workflow lại không có bước này!"*

**Bug found:** Loop 4 bước MISSED research-first mandate. v2.0 SOUL.md/tasks có `research_refs` field optional, không required. CI gate chỉ check 6 thứ, không enforce research exists.

**Fix (3-piece enforcement, same pattern as Fable-5):**
- **Piece 1: Shared reference update** — `~/.hermes/profiles/_shared/project-loop-engine.md` 6,378b → 10,394b. Loop 4 bước → 6 bước (RESEARCH → PLAN → RESEARCH → EXECUTE → VERIFY → NEXT). Trigger conditions rõ ràng cho Step 0 (khi nào BẮT BUỘC) và Step 1.5 (khi nào conditional).
- **Piece 2: Refactor consumers** — `wiki/projects/_template/task.md` (4,018b NEW, có `research_refs` field), `task-T-01.1-...md` refactored, `~/.hermes/docs/project-workflow-v2.md` updated.
- **Piece 3: CI gate update** — `check-project-compliance.sh` 5,923b → 6,775b. Thêm 2 checks v2.1: `research_refs` field required cho active tasks, `research/` folder recommended.
- **Step 8 (3-tier QA) verified** — Created test task T-99.9 with status IN_PROGRESS but no research_refs → CI gate FAILED → bug caught → fixed → PASS.

**Real lesson:** Khi user push back về gap trong design, KHÔNG tự sửa local — phải update SHARED REFERENCE (1 nguồn truth) + refactor CONSUMERS (template + tasks) + update CI GATE (enforcement). Đây chính là 3-piece enforcement áp dụng cho non-system-wide mandate (project workflow).

**Time saved on next project:** Khi user tạo project mới (`my-new-project`), `project-workflow-v2` skill load sẽ tự động reference v2.1 với 6-step loop. Không phải re-teach.

## Profile Lifecycle: New Profile Creation Hook (lesson 2026-06-17)

**When user creates a new profile, mandate propagation is a TWO-step process that most agents miss.**

**Step 1: Hermes command**

```bash
# Common case: clone from active (auto-inherits mandate IF active has it)
hermes profile create --clone my-agent

# Fresh start (no mandate — empty SOUL.md)
hermes profile create my-agent

# Clone from a specific source
hermes profile create --clone-from <source> my-agent
```

**Step 2: Mandate injection (REQUIRED for fresh + safety check for clone)**

```bash
# Inject mandate patterns (idempotent)
bash ~/.hermes/scripts/add-<mandate>-to-soul.sh ~/.hermes/profiles/my-agent/SOUL.md

# Verify
bash ~/.hermes/scripts/check-<mandate>-compliance.sh
```

**The auto-injector wrapper (recommended for any system-wide mandate skill):**

Create `~/.hermes/scripts/auto-inject-on-profile-create.sh` (2-mode: specific profile or all profiles). Template:

```bash
#!/bin/bash
# auto-inject-on-profile-create.sh
# Usage: bash auto-inject-on-profile-create.sh [profile-name]
# Without args: inject into ALL existing profiles (idempotent safe re-run)
set -e
HERMES_ROOT="${HERMES_HOME:-$HOME/.hermes}"
PROFILE_NAME="$1"
INJECTOR="$HERMES_ROOT/scripts/add-<mandate>-to-soul.sh"

inject_to_profile() {
  local soul_file="$HERMES_ROOT/profiles/$1/SOUL.md"
  [ -f "$soul_file" ] || { echo "⏭️  Skip $1: no SOUL.md"; return; }
  if grep -q "MANDATE_MARKER" "$soul_file"; then
    echo "✅ $1: already has mandate"
  else
    echo "🔧 Injecting into $1..."
    bash "$INJECTOR" "$soul_file"
  fi
}

if [ -n "$PROFILE_NAME" ]; then
  inject_to_profile "$PROFILE_NAME"
else
  for p in "$HERMES_ROOT/profiles"/*/; do
    name=$(basename "$p")
    case "$name" in _*|.|..) continue;; esac
    inject_to_profile "$name"
  done
  # Also check main SOUL.md (default profile)
  [ -f "$HERMES_ROOT/SOUL.md" ] && bash "$INJECTOR" "$HERMES_ROOT/SOUL.md" 2>/dev/null || true
fi
```

**Why the wrapper:** Reduces 5+ commands to 1, handles "I just created 5 new profiles" in one shot. Idempotent — safe to re-run.

**User-facing documentation:** When user asks "làm sao tạo profile mới có mandate?", point them to:
- `~/.hermes/docs/creating-profile-with-fable5.md` (Vietnamese casual guide with TL;DR)
- This skill's "Profile Lifecycle" section for the engineering details

**Default profile path gotcha (Hermes-specific):**
- Default profile path = `~/.hermes/` (NOT `~/.hermes/profiles/default/`)
- `~/.hermes/profiles/default/` folder exists but only contains `state.md` (runtime state, not config)
- Always run `hermes profile show <name>` to confirm the path before scanning for SOUL.md

## 5-Layer Verification Matrix (lesson 2026-06-17 — Tuấn Anh "100%" demand)

When user demands "100% system-wide" or "yên tâm tương lai", they mean ALL 5 layers MUST be verified, not just SOUL.md files. Single-layer verification = false confidence.

**The 5 layers:**

| Layer | What | How to verify | Why this layer |
|-------|------|---------------|----------------|
| 1. **SOUL.md coverage** | All profiles have mandate in their SOUL | `check-<mandate>-compliance.sh` exit 0 | Agent sessions read SOUL on `session:start` |
| 2. **Cron job prompts** | LLM cron jobs have mandate reminder | grep each LLM job prompt for marker | Cron runs in fresh context — no SOUL propagation |
| 3. **Hook auto-check** | Hook fires on `session:start` | `tail ~/.hermes/logs/gateway.log \| grep "Loaded <hook>"` | Catches new profiles that bypass scripts |
| 4. **Shared reference** | `_shared/<mandate>.md` file exists with full detail | `wc -l ~/.hermes/profiles/_shared/<mandate>.md` | All 1-line refs point to same source of truth |
| 5. **Compliance scripts** | Both `check-*` + `add-*` scripts exist + idempotent | Run scripts, verify exit 0 | Future-proofing for new files |

**Real Fable-5 audit (2026-06-17, found 2 bugs):**
- Started at "97.5% — 1 caveat" after fixing 1 issue
- User pushed: "Sao ko làm cho chắc chắn 100% đi nhỉ??"
- Ran 5-layer audit → found 2 more bugs:
  - **Layer 2**: 0/7 cron jobs had Fable-5 reference (silent miss)
  - **Layer 3**: Hook was SKIPPED because `def main()` ≠ `def handle()` (silent failure in gateway log)
- Both fixed: cron reminder injection + hook function rename
- Final: 100% across 5 layers

**Rule:** When user says "yên tâm 100% tương lai" or similar, run the 5-layer matrix BEFORE claiming success. Layer 1 (SOUL.md) is the EASIEST — the harder ones are 2-3 where infrastructure silently misses.

**QA script template:** See `scripts/verify-5-layers.sh` in this skill.

## Layer 6: Behavior Audit on a Real Task (NEW, 2026-06-23 — Tuấn Anh's "Inject ≠ Follow" insight)

**Tuấn Anh's verbatim feedback:** *"Ban nãy anh còn thấy em không tuân thủ fable 5 systems và loop system?! Tại sao? Chẳng lẽ đã lưu system wide rồi và mỗi đầu session hoặc khi compaction sẽ vẫn được giữ lại sao?"*

**Root cause (this skill MISSED until 2026-06-23):** Injecting mandates into SOUL.md is PASSIVE. Agent SEES the rule in context but is not FORCED to apply it. Memory fact only fires when agent actively searches for it. SOUL.md injection ≠ behavior change.

**Real failure case:** Agent ran a TikTok transcript task 2026-06-22. Both Fable-5 (4 patterns) and Loop system (6 steps) were in SOUL.md. Agent did NOT load `tiktok-transcript-pipeline` skill, did NOT check MCP audio tools, did NOT run parse→deliver-all. Did 8 frames of visual analysis instead. Tuấn Anh asked: "Tại sao không tuân thủ dù đã lưu system-wide?"

**Layer 6 — Behavior audit on real task:**

```bash
# For each mandate pattern P:
# 1. Pick a real task from user's current work
# 2. EXECUTE the task WITHOUT prompting
# 3. Audit: did P actually fire during execution?
#
# If P did not fire → SOUL.md injection is decorative. P is NOT applied.

EXAMPLE_PATTERN="READ-FULL-REQUEST"
REAL_TASK="download and analyze TikTok video transcript"

# Audit question: "Did the agent run the 3-step pre-execution protocol?"
# Expected: PARSE → PLAN-DELIVERABLES → EXECUTE-ALL
# Actual (failure case): Agent went straight to visual frame analysis, skipped PARSE step entirely
# Verdict: PATTERN NOT FIRED. SOUL.md injection is decorative.
```

**Fix:** Inject ≠ Follow. Need an **active checklist** that the agent MUST run before every task, not just rules in SOUL.md.

**Active Checklist pattern (3 phases, run before EVERY task):**

| Phase | What to check |
|-------|---------------|
| 1. Parse Request | Read user's message word-by-word, identify keywords, list deliverables explicitly |
| 2. Apply Mandates | Check Fable-5 (4 patterns) + Loop system (if project > 2 weeks) + Read-Full-Request |
| 3. Execute All Deliverables | Count deliverables, deliver all, never skip "phân tích" |

**Files for active-checklist pattern:**
- Shared spec: `~/.hermes/profiles/_shared/active-checklist.md`
- CI gate: `bash ~/.hermes/scripts/check-readfullrequest-compliance.sh` (verifies active-checklist reference in all SOUL.md)

**Rule:** When deploying a system-wide mandate, ALSO create an active-checklist that triggers the mandate before each task. SOUL.md alone is decorative.

**Audit question for any mandate:** *"Can I cite 1-2 evidence points where the mandate fired in a real task this week?"* If NO → SOUL.md injection is decorative. Fix by adding active-checklist.

**Real example (Fable-5, 2026-06-23):** Tuấn Anh asked "tại sao không tuân thủ dù đã lưu system-wide?" Audit found:
- Layer 1-5: PASS (SOUL.md injection + CI gate + shared ref + scripts all in place)
- Layer 6: FAIL — Agent did NOT load `tiktok-transcript-pipeline` skill before the TikTok task. SOUL.md mentioned the skill exists but agent did not consult it.
- Fix: Created `active-checklist.md` with explicit "Phase 1: identify keywords → auto-load skill" step. CI gate extended to verify active-checklist reference in all SOUL.md.

## Layer 7: Persistence Across Compaction — VĨNH VIỄN Anti-Mất (NEW, 2026-07-19 — Tuấn Anh's verbatim mandate)

**Context:** 19/07 23:30, anh Tuấn Anh promote 3 hệ thống thành VĨNH VIỄN + BẮT BUỘC:

> *"Ok tất cả 3 cái anh nói đều là bắt buộc phải tuân theo trong bất kể task nào hoặc bất kể yêu cầu nào và toàn bộ toàn thời gian hiệu lực vĩnh viễn, nếu có compaction thì không được bỏ đi 3 cái anh nói ở trên"*

**L55 lesson:** Drift recovery — em đã drift khỏi Fable 5 + Karpathy + Loop Engineering 2 turns liên tiếp. Memory compaction đã xóa lesson L55 khỏi `learned-about-tuananh.md` (file reset từ 5605 dòng → 1259 dòng) NHƯNG concept page ở `/Volumes/Storage-1/Hermes/wiki/concepts/drift-recovery-3-systems-2026-07-19.md` VẪN CÒN (8983 bytes) — bằng chứng em chống compaction sai cách.

**The 3 anti-compaction mechanisms (Layer 7 = beyond the 5-layer verification matrix):**

| Mechanism | What | Why it works | When to activate |
|-----------|------|--------------|------------------|
| **1. Wiki Persistent Storage** | Save concept page + L-number lessons to `/Volumes/Storage-1/Hermes/wiki/concepts/` (separate volume, NOT in memory) | Volume riêng không bị Hermes memory compact, KHÔNG bị Hermes session reset | When user says "mandatory / VĨNH VIỄN / không được bỏ" |
| **2. Daily Memory Curator** | Cron 02:00 nightly re-derive lessons from concept pages → re-append to entities + learned-about | Re-create từ source-of-truth (concept page) mỗi đêm → không thể mất | When wiki has concept page + entities needs re-population |
| **3. Active-Checklist DRIFT-1** | 5 câu tự check TRƯỚC mỗi response: (1) state assumption? (2) plan? (3) load skill? (4) verify? (5) khẩu hiệu 🎯? | Agent BẮT BUỘC re-derive từng response → không thể "feel" em đã làm | Every response, every memory state |

**When to apply Layer 7 (not always — only when user explicitly upgrades):**

| User says | Trigger Layer 7? |
|-----------|-----------------|
| "apply system-wide" | ❌ No — Layer 1-6 đủ |
| "mandatory" / "bắt buộc" | ❌ No — Layer 1-6 đủ |
| "VĨNH VIỄN" / "toàn bộ thời gian" / "không bao giờ bỏ" | ✅ YES — apply all 3 mechanisms |
| "kể cả khi compaction" / "không bị mất khi reset" | ✅ YES — concept page + curator mandatory |
| "every task / bất kể task nào" | ✅ YES — DRIFT-1 active-checklist mandatory |

**The 4-command compaction-safe verify (run anytime to check mandate persistence):**

```bash
# 1. Wiki concept page còn không?
ls -la /Volumes/Storage-1/Hermes/wiki/concepts/<mandate-slug>.md

# 2. SOUL.md có section không?
grep "3 HỆ THỐNG BẮT BUỘC VĨNH VIỄN" ~/.hermes/SOUL.md  # hoặc tên section tương ứng

# 3. Lesson có trong entities không?
grep "L55\|L<num>" /Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md

# 4. Daily curator đang chạy không?
hermes cron list | grep memory-curator
```

If 4/4 PASS → mandate persists dù memory đã compact.

**DRIFT-1 Active-Checklist (operational rule for Layer 7):**

```python
# Trước MỖI response, tự check 5 câu:
drift_checklist = {
    "1_karpathy_assumption": "Em đã state assumption trước khi viết response?",
    "2_karpathy_plan": "Em có plan checklist (numbered steps)?",
    "3_fable_skills_first": "Em đã load skill liên quan qua skill_view() chưa?",
    "4_loop_verify": "Output có verify được không (ls/grep/wc evidence)?",
    "5_slogan_khau_hieu": "Em có 🎯 SYSTEMS USED line không?",
}
# If any is NO → STOP, re-do before shipping
```

**Real evidence (L55, 19/07):**
- `learned-about-tuananh.md` reset 5605 → 1259 dòng (L55 mất)
- Wiki concept page `drift-recovery-3-systems-2026-07-19.md` vẫn 8983 bytes (Mechanism 1 OK)
- Em đã re-append L55 + L55.b vào entities file (Mechanism 3 active)
- Daily curator cron 02:00 sẽ re-derive L55 từ concept page (Mechanism 2 ready)

**Anti-pattern (NEVER DO):**
- ❌ Claim "mandate applied" chỉ vì SOUL.md có keyword → Layer 6 fail
- ❌ Skip Layer 7 vì "task lớn chưa cần" → memory compact sẽ mất lesson
- ❌ Save concept page vào `~/.hermes/` thay vì `/Volumes/Storage-1/Hermes/wiki/` → same volume, vẫn bị compact
- ❌ Trust concept page 1 nơi → phải có 3 mechanism redundancy

**Connection to other skills:**
- `nightly-memory-curation` — runs Mechanism 2 (daily curator re-derive)
- `hermes-file-edit-logging` — Mechanism 1 evidence trail (file path + size + before/after)
- `loop-engineering-deployment` — Layer 5 verification matrix already covers SOUL.md + cron + hook, Layer 7 extends to "compaction safety"

## Connection to Other Skills

- `self-verify-after-workaround` — verification discipline (5-layer matrix, `def handle()` requirement, default profile path gotcha, profile create flow). Read THIS skill when deploying a mandate, read `self-verify-after-workaround` when VERIFYING a deployment.
- `loop-engineering-deployment` — broader pattern for "apply engineering pattern system-wide" (Maker→Checker→Orchestrator). Fable-5 is one instance; loop-engineering is another.
- `hermes-agent-decision-guard` — when user says "100% system-wide", DON'T ask "which 5 layers?" — just run all 6 verifications.
- `project-workflow-v2` (NEW 2026-06-17) — class-level umbrella for multi-phase projects. Loops through phases/tasks/actions with verify-gate. Auto-logs to wiki/projects/{id}/logs/. Apply when user says "manage this multi-month project" or "build a system with multiple phases".
- `qa-gate` — when user repeats a request, treat it as a Layer 6 audit failure (mandate did not fire). Read qa-gate's Read-Full-Request Mandate section for the parse→deliver-all protocol that active-checklist enforces.
- `references/coupled-artifacts-audit-2026-07-30.md` — when a mandate lives across 3+ coupled files (SOUL.md + umbrella + cross-ref skill + wiki entity), single-file grep PASS hides internal contradictions. Re-audit case study + `rule_marker AND counter_rule (±50 lines)` detector + 4-step "enumerate → patch-all → audit-cross → report-all-or-none" recipe. Load BEFORE any "system-wide mandate applied" report that touches ≥3 files.

## Scope Decision: When user says "merge" vs "system-wide" (lesson 2026-07-09)

**Anti-pattern (over-engineering trap):** This skill's title is "System-Wide Mandate Enforcement" — agent could read the title and assume every mention of "rule" = full 3-piece deployment. WRONG. The skill covers the FULL system-wide case, but user often wants lighter scope.

**Decision tree — read user's verb CAREFULLY before starting Phase 1:**

| User says | Scope | What to do | What NOT to do |
|-----------|-------|------------|----------------|
| "apply system-wide" / "áp dụng toàn hệ thống" / "yên tâm 100% tương lai" | Full system-wide | Run full 3-phase workflow (verify → apply → 5-layer verify) | Don't skip cron injection or hook auto-check |
| "merge vào SOUL.md" / "add to" / "save to memory" | **Single-file scope** (default) | Edit 1 file, backup, verify diff, done | ❌ **DON'T** auto-deploy 3-piece enforcement |
| "remember this" / "lưu lại" | Memory-only | Add to memory (subject to char limit) | ❌ **DON'T** touch SOUL.md |
| "this is the rule now" (ambiguous) | ASK ONCE | "Anh muốn em apply chỉ default SOUL.md hay full system-wide (cron jobs + profiles + hook)?" | ❌ **DON'T** assume |

**Real case (2026-07-09):** Tuấn Anh said "2" after being offered 4 options for handling Karpathy coding guidelines (CLAUDE.md @ `~/browser-harness/SKILL.md`): (1) save to wiki, (2) merge into SOUL.md, (3) apply now, (4) ignore. Option 2 = inline-merge into main SOUL.md only.

**Correct action taken:** Edit `~/.hermes/SOUL.md`, add 4-rule section with decision tree, update change log footer, backup file, verify diff. DONE. No 3-piece enforcement, no cron injection, no shared ref, no CI gate.

**Trap avoided:** Agent could have read the skill title and over-deployed Fable-5-style 3-piece infrastructure for a 1-file inline-merge. Instead, respected user's explicit scope.

**Rule:** Before starting Phase 1 (VERIFY), confirm scope by reading user's verb:
- "system-wide" / "toàn bộ" / "100% tương lai" → run full workflow
- "merge" / "add" / "save" → single-file scope, skip 3-piece enforcement
- Ambiguous → ask once, then default to single-file (lower cost of error)

**Why this matters:** Tuấn Anh has a strong "over-engineering" detector. From `learned-about-tuananh` 2026-06-23 L17: *"Nghe có vẻ hơi over engineering quá cụ!"* — emitted whenever agent fan-outs beyond what user asked. The same trap exists for system-wide mandate deployment: building cron injectors + CI gates for a 1-file edit wastes time AND erodes trust.

**What to do when in doubt:** Default to **single-file scope**. If user wanted system-wide, they would have said so. You can always scale up later if anh asks. The 5-layer matrix exists for explicit "system-wide" requests, not for casual "add this to SOUL.md".

## Mental Model: Fable-5 = Foundation, Loop = Weapon (2026-06-17)

**User's explicit mental model (Tuấn Anh 17/06 11:15):**

> *"fable cho toàn bộ và loop cho các công việc dev, hoặc em tự động nhận biết khi nào nên dùng cái nào, đại khái thì anh muốn fable 5 là cái cốt lõi và là nền tảng của hệ thống và loop là vũ khí!"*

| Concept | Role | When applied |
|---------|------|--------------|
| **Fable-5** | 🏛️ **FOUNDATION** / nền tảng | **Always on** — mọi task đều dùng |
| **Loop Engine** | ⚔️ **WEAPON** cho dev/project work | **Chỉ khi trigger** — project lớn, dev work, multi-agent |

**When to use Fable-5 (always on, no exception):**
- 1-shot task
- Quick research < 30 min
- Setup đơn lẻ
- Conversation / Q&A
- Bất kỳ agent action nào

**When to use Loop Engine (weapon for dev work):**
- ✅ Project > 2 tuần timeline
- ✅ Multi-phase + multi-agent coordination
- ✅ Build tool/feature mới (dev work)
- ❌ KHÔNG dùng: research, conversation, 1-shot task

**Architectural implication:**

```
┌─────────────────────────────────────────┐
│  🏛️ FABLE-5 (FOUNDATION)                │
│  Always on — mọi task                   │
│  4 patterns: MCP, Storage, Skills,      │
│  Search Discipline                      │
└──────────────┬──────────────────────────┘
               │ principles (WHAT)
               ▼
┌─────────────────────────────────────────┐
│  ⚔️ LOOP ENGINE (WEAPON)                │
│  Chỉ dùng cho dev/project work          │
│  6-step: RESEARCH → PLAN → RESEARCH →   │
│  EXECUTE → VERIFY → NEXT (max 3 retry)  │
└─────────────────────────────────────────┘
```

**Per-step Fable-5 mapping (khi Loop được kích hoạt):**

| Loop Step | Fable-5 patterns áp dụng |
|-----------|--------------------------|
| Step 0 RESEARCH | P1 (MCP) + P3 (skill TRƯỚC) + P4 (multi-source) |
| Step 1 PLAN | P2 (save plan) + P3 (workflow skill) |
| Step 1.5 RESEARCH | P1 + P4 |
| Step 2 EXECUTE | P1 + P2 + P3 + P4 (tất cả) |
| Step 3 VERIFY | P2 (YAML) + P4 (citation) |
| Step 4 NEXT | (orchestration only) |

**Auto-detection rule:** Em tự động nhận biết khi nào dùng cái nào. **KHÔNG cần user nhắc.** Default = Fable-5 always. Loop chỉ kích hoạt khi task đáp ứng trigger conditions.

**Why this distinction matters (lesson 17/06):**
- Trước mental model clarification: Fable-5 + Loop cùng được enforce song song → user confused
- Sau clarification: Fable-5 = layer 1 (foundation), Loop = layer 2 (weapon, opt-in)
- Single source of truth: load Fable-5 skill trước, sau đó mới quyết định có load Loop không
- Avoids duplicating "always apply Loop" guidance cho 1-shot task → wrong fit
