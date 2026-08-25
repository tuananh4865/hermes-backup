---
name: subagent-driven-development
description: "Execute plans via delegate_task subagents (2-stage review)."
version: 1.1.0
author: Hermes Agent (adapted from obra/superpowers)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [delegation, subagent, implementation, workflow, parallel]
    related_skills: [writing-plans, requesting-code-review, test-driven-development]
---

# Subagent-Driven Development

## Overview

Execute implementation plans by dispatching fresh subagents per task with systematic two-stage review.

**Core principle:** Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration.

## When to Use

Use this skill when:
- You have an implementation plan (from writing-plans skill or user requirements)
- Tasks are mostly independent
- Quality and spec compliance are important
- You want automated review between tasks

**vs. manual execution:**
- Fresh context per task (no confusion from accumulated state)
- Automated review process catches issues early
- Consistent quality checks across all tasks
- Subagents can ask questions before starting work

## The Process

### 1. Read and Parse Plan

Read the plan file. Extract ALL tasks with their full text and context upfront. Create a todo list:

```python
# Read the plan
read_file("docs/plans/feature-plan.md")

# Create todo list with all tasks
todo([
    {"id": "task-1", "content": "Create User model with email field", "status": "pending"},
    {"id": "task-2", "content": "Add password hashing utility", "status": "pending"},
    {"id": "task-3", "content": "Create login endpoint", "status": "pending"},
])
```

**Key:** Read the plan ONCE. Extract everything. Don't make subagents read the plan file — provide the full task text directly in context.

### 2. Per-Task Workflow

For EACH task in the plan:

#### Step 1: Dispatch Implementer Subagent

Use `delegate_task` with complete context:

```python
delegate_task(
    goal="Implement Task 1: Create User model with email and password_hash fields",
    context="""
    TASK FROM PLAN:
    - Create: src/models/user.py
    - Add User class with email (str) and password_hash (str) fields
    - Use bcrypt for password hashing
    - Include __repr__ for debugging

    FOLLOW TDD:
    1. Write failing test in tests/models/test_user.py
    2. Run: pytest tests/models/test_user.py -v (verify FAIL)
    3. Write minimal implementation
    4. Run: pytest tests/models/test_user.py -v (verify PASS)
    5. Run: pytest tests/ -q (verify no regressions)
    6. Commit: git add -A && git commit -m "feat: add User model with password hashing"

    PROJECT CONTEXT:
    - Python 3.11, Flask app in src/app.py
    - Existing models in src/models/
    - Tests use pytest, run from project root
    - bcrypt already in requirements.txt
    """,
    toolsets=['terminal', 'file']
)
```

#### Step 2: Dispatch Spec Compliance Reviewer

After the implementer completes, verify against the original spec:

```python
delegate_task(
    goal="Review if implementation matches the spec from the plan",
    context="""
    ORIGINAL TASK SPEC:
    - Create src/models/user.py with User class
    - Fields: email (str), password_hash (str)
    - Use bcrypt for password hashing
    - Include __repr__

    CHECK:
    - [ ] All requirements from spec implemented?
    - [ ] File paths match spec?
    - [ ] Function signatures match spec?
    - [ ] Behavior matches expected?
    - [ ] Nothing extra added (no scope creep)?

    OUTPUT: PASS or list of specific spec gaps to fix.
    """,
    toolsets=['file']
)
```

**If spec issues found:** Fix gaps, then re-run spec review. Continue only when spec-compliant.

#### Step 3: Dispatch Code Quality Reviewer

After spec compliance passes:

```python
delegate_task(
    goal="Review code quality for Task 1 implementation",
    context="""
    FILES TO REVIEW:
    - src/models/user.py
    - tests/models/test_user.py

    CHECK:
    - [ ] Follows project conventions and style?
    - [ ] Proper error handling?
    - [ ] Clear variable/function names?
    - [ ] Adequate test coverage?
    - [ ] No obvious bugs or missed edge cases?
    - [ ] No security issues?

    OUTPUT FORMAT:
    - Critical Issues: [must fix before proceeding]
    - Important Issues: [should fix]
    - Minor Issues: [optional]
    - Verdict: APPROVED or REQUEST_CHANGES
    """,
    toolsets=['file']
)
```

**If quality issues found:** Fix issues, re-review. Continue only when approved.

#### Step 4: Mark Complete

```python
todo([{"id": "task-1", "content": "Create User model with email field", "status": "completed"}], merge=True)
```

### 3. Final Review

After ALL tasks are complete, dispatch a final integration reviewer:

```python
delegate_task(
    goal="Review the entire implementation for consistency and integration issues",
    context="""
    All tasks from the plan are complete. Review the full implementation:
    - Do all components work together?
    - Any inconsistencies between tasks?
    - All tests passing?
    - Ready for merge?
    """,
    toolsets=['terminal', 'file']
)
```

### 4. Verify and Commit

```bash
# Run full test suite
pytest tests/ -q

# Review all changes
git diff --stat

# Final commit if needed
git add -A && git commit -m "feat: complete [feature name] implementation"
```

## Task Granularity

**Each task = 2-5 minutes of focused work.**

**Too big:**
- "Implement user authentication system"

**Right size:**
- "Create User model with email and password fields"
- "Add password hashing function"
- "Create login endpoint"
- "Add JWT token generation"
- "Create registration endpoint"

## Verification Patterns After Sub-Agent Returns

Sub-agents are excellent at focused work but they lie about success ~10% of the time (silently dropped steps, wrong files, partial completion). The parent MUST verify before trusting.

### Required verifications after any sub-agent task

| What sub-agent claims | What to actually run |
|----------------------|----------------------|
| "Created N files" | `find <path> -type f -name "*.md" | wc -l` |
| "File has N sections" | `grep -c "^### " <file>` (line-based) OR `grep -oE "^### " <file> | wc -l` (match-based) |
| "Added wikilinks" | `grep -oE '\[\[[^]]+\]\]' <file> | wc -l` — NOT `grep -c "[["` (counts lines) |
| "YAML frontmatter valid" | `head -1 <file> | grep -q "^---"` AND check required fields present |
| "Tests pass" | Run the actual test command yourself |
| "Skill loaded" | `ls ~/.hermes/skills/<skill-name>/SKILL.md` to confirm exists |
| "File size ~N bytes" | `wc -c <file>` |
| "Done" | Re-read a sample of the file via `read_file` |

### Grep counting gotcha (very common)

```bash
# WRONG: counts LINES containing at least one match (returns 1 even with 10 matches on one line)
grep -c "PATTERN" file.txt

# CORRECT: counts all MATCHES regardless of line
grep -oE "PATTERN" file.txt | wc -l
```

When verifying wikilinks, citations, tags, or any countable pattern where multiple can occur on one line, **always use `grep -oE | wc -l`**. Sub-agents routinely use `grep -c` and report inflated "1 match" when there are many.

### Parallel sub-agent file modification

When dispatching multiple sub-agents that may touch the same project, files modified by sibling sub-agents between your read and write will cause patches to fail or silently overwrite.

**Pattern:**
1. Read file X for context
2. Dispatch sub-agents A and B in parallel
3. Sub-agent B modifies file X
4. You try to patch file X using old `old_string` from step 1 → fails or overwrites B's changes

**Fix:** Before patching any file modified by sub-agents, re-read it (via `head -N file` or full `read_file`) to get fresh `old_string`.

## If Sub-Agent Reports Skill Not Found

Sub-agents may report "skill X doesn't exist, used skill Y instead." This is acceptable as a workaround IF you:

1. Verify Y actually exists: `ls ~/.hermes/skills/Y/SKILL.md`
2. Log the substitution explicitly in the action log
3. Update the task spec to reference Y (so future tasks align)
4. Note in dashboard under "Issues & Blockers" → Resolved

Don't let silent substitutions accumulate — they compound into plan-vs-reality drift.

## Red Flags — Never Do These

- Start implementation without a plan
- Skip reviews (spec compliance OR code quality)
- Proceed with unfixed critical/important issues
- Dispatch multiple implementation subagents for tasks that touch the same files
- Make subagent read the plan file (provide full text in context instead)
- Skip scene-setting context (subagent needs to understand where the task fits)
- Ignore subagent questions (answer before letting them proceed)
- Accept "close enough" on spec compliance
- Skip review loops (reviewer found issues → implementer fixes → review again)
- Let implementer self-review replace actual review (both are needed)
- **Start code quality review before spec compliance is PASS** (wrong order)
- Move to next task while either review has open issues
- **Trust subagent's self-reported PASS without independent verification** (always re-run grep/commands yourself)
- **Use `grep -c "PATTERN"` to count multiple matches per line** — `grep -c` counts LINES, not matches. If multiple matches can be on one line, use `grep -oE 'PATTERN' | wc -l` instead. Common pitfall when verifying wikilinks, citations, tags, etc.
- **Patch files after parallel subagents wrote to them without re-reading first** — sibling subagents can modify files the parent read earlier, causing patches to fail or overwrite changes. Always re-read files modified by subagents between read and write, especially in parallel flows.
- **Accept "skill not found, used substitute" without updating task spec** — silent skill substitution breaks alignment between plan and execution. Update the task spec to reference the correct skill name and log the substitution in the action log.
- **Pass a relative path like `research/foo.md` to a sub-agent on macOS with external storage (e.g. `/Volumes/Storage-1/...`)** — sub-agents will resolve it against their own CWD and silently write to the wrong location (commonly `~/wiki/` instead of `/Volumes/Storage-1/Hermes/wiki/`). ALWAYS pass the full absolute path in the sub-agent context, and verify the parent directory exists before delegating. After sub-agents return, run `find` at the expected absolute path to confirm files landed where you said they would. If they didn't, move them — don't pretend the work happened. (Hit this 2026-06-18 with 3 parallel content-director sub-agents writing 15 scripts; had to move files from `~/wiki/` → `/Volumes/Storage-1/Hermes/wiki/` after the fact.)

## Concurrent Sub-Agent Fan-Out (Tuấn Anh mandate 18/06)

For multi-track parallel work (e.g. "write 5 scripts per trụ × 3 trụ = 15 scripts in parallel"), use the batch form of `delegate_task`:

```python
delegate_task(tasks=[
    {"goal": "...EDIT scripts...", "toolsets": ["file", "web"]},
    {"goal": "...SETUP scripts...", "toolsets": ["file", "web"]},
    {"goal": "...ÁNH SÁNG scripts...", "toolsets": ["file", "web"]},
])
```

**Defaults to know** (config keys in `~/.hermes/config.yaml` under `delegation:`):
- `max_concurrent_children` — ceiling on parallel sub-agents (default 3). For long/heavy batches, raise to 8 (verified working 2026-06-18 with 3 sub-agents × 18 API calls each, completed in ~9 min).
- `max_spawn_depth` — default 1 (flat). Leaves are always default; orchestrator role requires raising this.
- `subagent_auto_approve` — default false (every tool call requires manual approval). For batch fan-out, set true to avoid being a bottleneck. Risk: less human-in-the-loop; mitigate via CI gate + audit logs.

**Verification after batch fan-out is NON-NEGOTIABLE** — sub-agent self-reports routinely undercount (e.g. claim "5 scripts" but use `## EDIT-NN` (H2) not `### EDIT-NN` (H3), so `grep -c '^### '` returns 0). Always re-count with the right pattern yourself:

```bash
# If sub-agent used H2 (##) for script headers:
grep -cE "^## (EDIT|SETUP|ANH-SANG)-" research/T-01.4-scripts-*.md

# If H3 (###):
grep -c "^### " research/T-01.4-scripts-*.md
```

Always cross-check both: existence (`ls`), size (`wc -c`), and structural counts (`grep -oE | wc -l`).

## Handling Issues

### If Subagent Asks Questions

- Answer clearly and completely
- Provide additional context if needed
- Don't rush them into implementation

### If Reviewer Finds Issues

- Implementer subagent (or a new one) fixes them
- Reviewer reviews again
- Repeat until approved
- Don't skip the re-review

### If Subagent Fails a Task

- Dispatch a new fix subagent with specific instructions about what went wrong
- Don't try to fix manually in the controller session (context pollution)

## Efficiency Notes

**Why fresh subagent per task:**
- Prevents context pollution from accumulated state
- Each subagent gets clean, focused context
- No confusion from prior tasks' code or reasoning

**Why two-stage review:**
- Spec review catches under/over-building early
- Quality review ensures the implementation is well-built
- Catches issues before they compound across tasks

**Cost trade-off:**
- More subagent invocations (implementer + 2 reviewers per task)
- But catches issues early (cheaper than debugging compounded problems later)

## Integration with Other Skills

### With writing-plans

This skill EXECUTES plans created by the writing-plans skill:
1. User requirements → writing-plans → implementation plan
2. Implementation plan → subagent-driven-development → working code

### With test-driven-development

Implementer subagents should follow TDD:
1. Write failing test first
2. Implement minimal code
3. Verify test passes
4. Commit

Include TDD instructions in every implementer context.

### With requesting-code-review

The two-stage review process IS the code review. For final integration review, use the requesting-code-review skill's review dimensions.

### With systematic-debugging

If a subagent encounters bugs during implementation:
1. Follow systematic-debugging process
2. Find root cause before fixing
3. Write regression test
4. Resume implementation

## Example Workflow

```
[Read plan: docs/plans/auth-feature.md]
[Create todo list with 5 tasks]

--- Task 1: Create User model ---
[Dispatch implementer subagent]
  Implementer: "Should email be unique?"
  You: "Yes, email must be unique"
  Implementer: Implemented, 3/3 tests passing, committed.

[Dispatch spec reviewer]
  Spec reviewer: ✅ PASS — all requirements met

[Dispatch quality reviewer]
  Quality reviewer: ✅ APPROVED — clean code, good tests

[Mark Task 1 complete]

--- Task 2: Password hashing ---
[Dispatch implementer subagent]
  Implementer: No questions, implemented, 5/5 tests passing.

[Dispatch spec reviewer]
  Spec reviewer: ❌ Missing: password strength validation (spec says "min 8 chars")

[Implementer fixes]
  Implementer: Added validation, 7/7 tests passing.

[Dispatch spec reviewer again]
  Spec reviewer: ✅ PASS

[Dispatch quality reviewer]
  Quality reviewer: Important: Magic number 8, extract to constant
  Implementer: Extracted MIN_PASSWORD_LENGTH constant
  Quality reviewer: ✅ APPROVED

[Mark Task 2 complete]

... (continue for all tasks)

[After all tasks: dispatch final integration reviewer]
[Run full test suite: all passing]
[Done!]
```

## Remember

```
Fresh subagent per task
Two-stage review every time
Spec compliance FIRST
Code quality SECOND
Never skip reviews
Catch issues early
```

**Quality is not an accident. It's the result of systematic process.**

## Further reading (load when relevant)

When the orchestration involves significant context usage, long review loops, or complex validation checkpoints, load these references for the specific discipline:

- **`references/context-budget-discipline.md`** — Four-tier context degradation model (PEAK / GOOD / DEGRADING / POOR), read-depth rules that scale with context window size, and early warning signs of silent degradation. Load when a run will clearly consume significant context (multi-phase plans, many subagents, large artifacts).
- **`references/gates-taxonomy.md`** — The four canonical gate types (Pre-flight, Revision, Escalation, Abort) with behavior, recovery, and examples. Load when designing or reviewing any workflow that has validation checkpoints — use the vocabulary explicitly so each gate has defined entry, failure behavior, and resumption rules.

Both references adapted from gsd-build/get-shit-done (MIT © 2025 Lex Christopherson).
