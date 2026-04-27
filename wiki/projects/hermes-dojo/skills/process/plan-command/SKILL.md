---
name: plan-command
description: Define exact implementation steps before coding - creates plan artifact with verification criteria
version: 1.0.0
category: process
platforms: [macos, linux]
created: 2026-04-14
tags: [planning, implementation, steps, verification, artifacts]
requires_toolsets: [terminal]
---

# Plan Command

**A task without a plan is just a wish.**

This skill transforms research into an actionable implementation plan with exact steps and verification criteria.

---

## When to Use

Use `/plan` or this skill when:

1. **After research** — Research artifact exists, now define the path
2. **Before implementation** — Turn understanding into action
3. **Complex tasks** — Multi-step work needs coordination
4. **Any non-trivial change** — Single file changes might not need full plan

**Rule:** If a task has more than 3 steps, it needs a plan.

---

## The Planning Workflow

### Step 1: Review Research

```
Read the research artifact
Confirm understanding
Note any gaps before proceeding
```

### Step 2: Define Success Criteria

```
What must be true when this is complete?
How will we know it worked?
```

### Step 3: Design the Solution

```
What files need changes?
What is the change in each file?
What order should changes happen?
```

### Step 4: List Implementation Steps

```
For each step:
1. What to do
2. What file(s)
3. How to verify it worked
```

### Step 5: Identify Risks

```
What could go wrong?
How to mitigate?
What to do if it breaks?
```

### Step 6: Document the Plan

Create a plan artifact (see template below).

---

## Plan Artifact Template

```markdown
# Plan: {Task Name}

**Date:** {YYYY-MM-DD}
**Research:** [Link to research artifact]
**Status:** Draft / Approved / In Progress / Complete

## Success Criteria

- [ ] {Criterion 1}
- [ ] {Criterion 2}
- [ ] {Criterion 3}

## Files to Modify

| File | Change Type | Lines | Description |
|------|------------|-------|-------------|
| | | | |
| | | | |

## Implementation Order

### Phase 1: Foundation
{Steps that must happen first, usually base/interface changes}

### Phase 2: Core Changes
{Main implementation steps}

### Phase 3: Integration
{Steps that depend on Phase 2 completing}

### Phase 4: Verification
{Testing and validation steps}

## Step-by-Step Implementation

### Step 1: {Brief description}
**File:** {File path}
**Change:** {What to change}
**Verification:** {How to verify}

```
# Commands to run
command1
command2
```

### Step 2: {Brief description}
**File:** {File path}
**Change:** {What to change}
**Verification:** {How to verify}

...

## Cascade Prevention

### Files That Will Be Updated
- [ ] File 1
- [ ] File 2

### Files to Verify
- [ ] File 1 (verify update)
- [ ] File 2 (verify update)

## Risk Mitigation

| Risk | Likelihood | Impact | Mitigation | Contingency |
|------|------------|--------|------------|-------------|
| | | | | |

## Testing Plan

### Unit Tests
- {Test 1}
- {Test 2}

### Integration Tests
- {Test 1}

### Manual Verification
- {Step 1}
- {Step 2}

## Rollback Plan

If this plan breaks things:
1. {Step 1}
2. {Step 2}

## Sign-off

- [ ] Plan reviewed
- [ ] User approved (if complex)
- [ ] Implementation started
```

---

## Example Plan

```
Task: Fix file upload size limit bug

SUCCESS CRITERIA:
- [ ] Files up to 50MB upload successfully
- [ ] User sees clear error if file too large
- [ ] No regression on small files

FILES TO MODIFY:
1. src/config/upload.py - change limit
2. src/api/upload.py - add error handling
3. src/services/storage.py - add validation

IMPLEMENTATION STEPS:

Step 1: Update config
File: src/config/upload.py
Change: upload_max_size = 50 * 1024 * 1024
Verification: grep shows 50MB

Step 2: Add error handling
File: src/api/upload.py
Change: if size > limit: return 413 with message
Verification: curl with 60MB file returns 413

Step 3: Test
Verification: pytest tests/upload/ -v
```

---

## Plan Quality Checklist

- [ ] Success criteria are specific and testable
- [ ] Every step has a verification method
- [ ] Files are listed with change descriptions
- [ ] Implementation order is logical (base → callers)
- [ ] Risks are identified with mitigations
- [ ] Rollback plan exists
- [ ] Testing plan is defined

---

## Common Mistakes

### Mistake 1: Vague Steps

```
BAD: "Update the config file"
GOOD: "Change upload_max_size in src/config/upload.py from 10MB to 50MB"
```

### Mistake 2: Missing Verification

```
BAD: "Step 1: Make change" → then nothing
GOOD: "Step 1: Make change → verify: grep shows new value"
```

### Mistake 3: Wrong Order

```
BAD: Update caller → Update base → Update another caller
GOOD: Update base → Update caller1 → Update caller2
```

### Mistake 4: No Success Criteria

```
BAD: "Goal: fix the bug"
GOOD: "Goal: files up to 50MB upload, user sees clear error over limit"
```

---

## Integration

- Input from [[research-command]] — Research artifact
- Output feeds into [[implement-command]] — Execute the plan
- Use [[surgical-change-protocol]] — For cascade prevention
- Use [[goal-driven-execution]] — For verification

---

## Related

- [[research-command]] — Before planning
- [[implement-command]] — Execute the plan
- [[goal-driven-execution]] — Verify completion
- [[surgical-change-protocol]] — Cascade prevention
