# Session 2026-06-17 — Loop Engine v2.0 → v2.2 + Fable-5 Combination + Auto-Log System

> **Context:** User asked 3 sequential questions in one session, each triggering a new version of Loop Engineering. This document captures the iteration loop, key lessons, and the final v2.2 + Fable-5 combination.

## Session Timeline

| Time (ICT) | Event | Trigger phrase |
|------------|-------|----------------|
| 10:00 | Loop Engine v2.0 designed | "Tưởng tượng em làm một dự án lớn nhiều ngày nhiều tháng..." |
| 10:30 | Auto-log hook v2 deployed | "Anh cũng nghĩ nên có một quy trình auto log lại..." |
| 10:50 | Loop Engine v2.1 (research-first) | "kỹ năng research là một kỹ năng bắt buộc..." |
| 11:00 | Loop Engine v2.2 (retry policy) | "If fail thì phải lặp lại loop từ bước 3 trở đi. Nếu vẫn fail đến lần thứ 3 thì report lại..." |
| 11:10 | Fable-5 + Loop Engine combined | "Có thể kết hợp 2 concept fable 5 và loop engineering không?" |

## Key Lessons (each iteration added 1 lesson)

### v2.0 → v2.1: Research-First Mandate

**User correction:** Loop 4 bước (PLAN→EXECUTE→VERIFY→NEXT) MISSED research — the single most important capability per user.

**Fix:**
- Added Step 0 (RESEARCH) before PLAN — mandatory for project/phase creation
- Added Step 1.5 (RESEARCH) before EXECUTE — conditional on decision points
- New `research/` folder in project structure
- New `research_refs` field in task YAML frontmatter
- CI gate enforces `research_refs` field for non-TODO tasks

**3-piece enforcement applied:**
1. Shared ref updated: `project-loop-engine.md` (v2.0 → v2.1)
2. Consumer refactored: task template + content-creator project
3. CI gate updated: `check-project-compliance.sh` checks `research_refs`

**Verification (3-layer):**
- Layer 1 (code): shared ref + template + CI gate updated ✓
- Layer 2 (behavior): Created T-99.9 test task missing research_refs → CI gate FAILED ✓
- Layer 3 (future-proof): All new tasks require research_refs field ✓

### v2.1 → v2.2: Retry Policy

**User correction:** Step 4 (NEXT) was too simplistic — needed explicit max-retry count + escalate behavior.

**Fix:**
- Retry flow: FAIL → fix → re-verify (loop from Step 3, max 3 attempts)
- After 3 failures → ESCALATE → 🚨 BLOCKED → Telegram → CHỜ LỆNH
- New YAML fields: `verify_attempts`, `last_failure_reason`, `escalated_at`
- Trigger conditions: when to retry (fixable) vs when to escalate (structural)

**3-piece enforcement:**
1. Shared ref updated (v2.1 → v2.2): state machine expanded, 3 new YAML fields documented
2. Consumer refactored: task template + T-01.1 + user guide
3. CI gate updated: `check-project-compliance.sh` checks `verify_attempts` field

### Fable-5 + Loop Engine Combination

**User question:** Can these 2 concepts be combined?

**Answer:** YES — they're complementary, not overlapping:
- **Fable-5** = principles (WHAT to do) — applies to ALL tasks
- **Loop Engine v2.2** = procedure (HOW to do) — applies to projects > 2 weeks

**Per-step Fable-5 mapping:**
| Loop Step | Fable-5 patterns |
|-----------|------------------|
| 0 RESEARCH | P1 (MCP) + P3 (skill TRƯỚC) + P4 (multi-source) |
| 1 PLAN | P2 (save plan) + P3 (workflow skill) |
| 1.5 RESEARCH | P1 + P4 |
| 2 EXECUTE | P1 + P2 + P3 + P4 (ALL FOUR) |
| 3 VERIFY | P2 (YAML) + P4 (citation) |
| 4 NEXT | (orchestration only) |

**Implementation:**
1. Shared refs cross-reference each other (added "Relationship" section in both)
2. Created unified CI gate: `check-all-compliance.sh`
3. Verified: both gates PASS

## Files Created/Modified (12 total)

### Wiki (Content Creator project — applied workflow v2.2)
1. `/wiki/projects/content-creator/hub.md` (4,097b) — project hub
2. `/wiki/projects/content-creator/phases/phase-01-foundation.md` (2,582b)
3. `/wiki/projects/content-creator/tasks/task-T-01.1-research-slang-sounds.md` (5,144b)
4. `/wiki/projects/_template/task.md` (4,018b) — template with v2.2 fields

### Hermes config
5. `~/.hermes/profiles/_shared/project-loop-engine.md` (v2.0 → v2.2, ~14KB final)
6. `~/.hermes/profiles/_shared/fable5-patterns.md` (+relationship section)
7. `~/.hermes/hooks/session-auto-log/handler.py` v2 (6,962b) — project tracking
8. `~/.hermes/scripts/check-project-compliance.sh` (5,923b → ~7KB, +v2.1 +v2.2 checks)
9. `~/.hermes/scripts/check-all-compliance.sh` (NEW, 1,412b) — unified gate

### Docs
10. `~/.hermes/docs/project-workflow-v2.md` (6,837b) — user guide v2.2

### Wiki log
11. `/wiki/log.md` (39,282b, +5 entries for this iteration)

## Patterns Established

### Pattern: Research-First Mandate
Any project workflow MUST include research steps (before PLAN and optionally before EXECUTE). The user explicitly said this is a HARD requirement, not optional.

**Anti-pattern:** Loop engines that skip research and go straight to PLAN → "research is a non-negotiable skill" per user.

### Pattern: Retry with Escalation Gate
Multi-attempt workflows need explicit max retry count + escalation trigger conditions. Avoids both "retry forever" and "fail immediately" extremes.

**Anti-pattern:** "IF FAIL → return to Step 2 with specific issues" (vague, no max count, no escalate behavior).

### Pattern: Concept Complementarity
Fable-5 (principles) + Loop Engine (procedure) don't overlap — they address different abstraction levels. Cross-reference, don't merge.

**Anti-pattern:** Creating a mega-skill that tries to be both principles AND procedure.

## Verification Highlights

```bash
# All 3 CI gates passing after v2.2 + combination:
$ bash check-fable5-compliance.sh
✅ PASS — All 9 SOUL.md files comply with Fable-5 mandate

$ bash check-project-compliance.sh content-creator
✅ PASS: content-creator complies with workflow v2

$ bash check-all-compliance.sh content-creator
🏁 UNIFIED CHECK COMPLETE — Both Fable-5 + Loop Engine PASS
```

## Related References

- `references/session-2026-06-17-fable5-100-percent.md` — earlier 5-layer verification matrix (complements this iteration)
- `references/session-2026-06-16-self-verify.md` — original self-verify pattern
- `references/session-2026-06-16-idempotent-injector.md` — injector verification recipe

## Lessons for Future Sessions

1. **Always audit before designing** — list existing hooks, scripts, skills first
2. **3-piece enforcement pattern** — shared ref + consumer refactor + CI gate is the standard
3. **Loop version is real** — v2.0 → v2.1 → v2.2 each had meaningful changes, document each transition
4. **Concept complementarity** — when user asks "combine X and Y", check if they overlap or complement first
5. **Honest 97.5% > fake 100%** — even after CI passes, note caveats (e.g. cron jobs in this session weren't verified end-to-end)