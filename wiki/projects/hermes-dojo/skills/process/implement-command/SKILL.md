---
name: implement-command
description: Execute implementation plan with step-by-step verification - prevents skipping steps and ensures completion
version: 1.0.0
category: process
platforms: [macos, linux]
created: 2026-04-14
tags: [implementation, execution, verification, steps, completion]
requires_toolsets: [terminal]
---

# Implement Command

**Follow the plan. Verify each step. Complete before claiming done.**

This skill executes an implementation plan systematically, verifying each step before moving on.

---

## When to Use

Use `/implement` or this skill when:

1. **Plan exists** — Research and plan artifacts are complete
2. **Ready to code** — Ready to start making changes
3. **Mid-implementation** — Want to continue where left off
4. **Verification** — Need to verify a plan is complete

---

## The Implementation Workflow

### Step 1: Review the Plan

```
Read the plan artifact
Confirm all steps are understood
Identify any blockers before starting
```

### Step 2: Execute Step by Step

```
For each step in order:
1. Read the current step
2. Make the change
3. Run the verification
4. If pass → proceed to next
5. If fail → fix before proceeding
```

### Step 3: Verify Each Step

```bash
# Verification methods by type

# Code change:
grep "pattern" file.py  # Check content
python -m py_compile file.py  # Syntax check

# Function rename:
grep -r "old_name" .  # Should return nothing
grep -r "new_name" .  # Should return N results

# Config change:
cat config.py | grep "key"  # Verify value

# Test:
pytest tests/test_file.py -v  # Run tests
```

### Step 4: Track Progress

```
Mark completed steps in the plan
Note any issues encountered
Update plan if reality differs
```

### Step 5: Final Verification

```
After all steps complete:
1. Run full test suite
2. Verify all success criteria
3. Update PROJECT_STATE.md
4. Commit changes
```

---

## Step Execution Template

```
═══════════════════════════════════════════════
STEP N: {Brief description}
═══════════════════════════════════════════════

PLAN SAYS:
{What the plan says to do}

MY UNDERSTANDING:
{How I interpret this step}

EXECUTION:
{Precisely what I did}
$ command run
$ another command

VERIFICATION:
{How I verified}
$ verification command
Result: {What happened}

STATUS: ✅ PASS / ❌ FAIL

If FAIL:
ERROR: {What went wrong}
FIX ATTEMPTED: {What I did}
RESULT: {Did it work?}
═══════════════════════════════════════════════
```

---

## Example Implementation Session

```
═══════════════════════════════════════════════
STEP 1: Update upload_max_size in config
═══════════════════════════════════════════════

PLAN SAYS:
File: src/config/upload.py
Change: upload_max_size = 50 * 1024 * 1024

EXECUTION:
$ cat src/config/upload.py | grep max
upload_max_size = 10 * 1024 * 1024  # OLD

$ sed -i '' 's/10 \* 1024 \* 1024/50 * 1024 * 1024/' src/config/upload.py

$ grep max_size src/config/upload.py
upload_max_size = 50 * 1024 * 1024  # NEW ✓

VERIFICATION:
$ grep "upload_max_size = 50" src/config/upload.py
upload_max_size = 50 * 1024 * 1024 ✓

STATUS: ✅ PASS
═══════════════════════════════════════════════

[Proceed to Step 2...]
```

---

## Cascade Prevention During Implementation

### Before Editing Any File

```
1. Run dependency check:
   python3 ~/.hermes/scripts/dependency_tracker.py --scan . --check path/to/file.py

2. Read all callers listed

3. Confirm you have the complete list

4. Only then: Make the edit
```

### After Editing

```
1. Verify base/interface change complete

2. For EACH caller in your list:
   - Open the file
   - Make the update
   - Verify the update

3. Run tests

4. Only then: Mark step complete
```

---

## Progress Tracking

Update the plan artifact as you go:

```markdown
## Step Status

- [x] Step 1: {Description} - ✅ PASS
- [x] Step 2: {Description} - ✅ PASS
- [ ] Step 3: {Description} - In Progress
- [ ] Step 4: {Description} - Pending
```

---

## When the Plan is Wrong

### Situation: Plan seems incorrect

```
STOP. DO NOT PROCEED.

Correct approach:
1. Note the issue in the plan
2. Explain why it seems wrong
3. Ask for clarification

Wrong approach:
1. "I'll just figure it out"
2. Deviate from plan silently
3. Hope for the best
```

### Situation: Reality differs from plan

```
Correct approach:
1. Stop
2. Update the plan with new understanding
3. Re-evaluate steps
4. Continue with corrected plan

Wrong approach:
1. Keep going despite mismatch
2. Complete the wrong implementation
```

---

## Final Checklist

Before marking implementation complete:

- [ ] All steps completed and verified
- [ ] All success criteria met
- [ ] No cascade failures (all callers updated)
- [ ] Full test suite passes
- [ ] PROJECT_STATE.md updated
- [ ] Changes committed

---

## Implementation Report Template

```markdown
# Implementation Report: {Task}

**Date:** {YYYY-MM-DD}
**Plan:** [Link to plan]
**Status:** Complete

## Steps Completed

| Step | Description | Status | Verification |
|------|------------|--------|--------------|
| 1 | | ✅ PASS | |
| 2 | | ✅ PASS | |

## Success Criteria Verification

- [✅] {Criterion 1} - {Evidence}
- [✅] {Criterion 2} - {Evidence}

## Cascade Prevention

- [✅] All callers identified
- [✅] All callers updated
- [✅] No silent breaks

## Testing

- [✅] Unit tests pass
- [✅] Integration tests pass
- [✅] Manual verification complete

## Artifacts

- [✅] Plan updated
- [✅] PROJECT_STATE.md updated
- [✅] Code committed

## Lessons Learned

{Any insights from this implementation}
```

---

## Integration

- Input from [[plan-command]] — Plan artifact
- Use [[surgical-change-protocol]] — For cascade prevention
- use [[goal-driven-execution]] — For verification
- Output to PROJECT_STATE.md — Progress tracking

---

## Related

- [[plan-command]] — Before implementation
- [[research-command]] — Before planning
- [[goal-driven-execution]] — Verify completion
- [[surgical-change-protocol]] — Cascade prevention
