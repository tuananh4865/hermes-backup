---
name: surgical-change-protocol
description: Protocol for making code changes without causing cascade failures - always check dependencies before and after editing
version: 1.0.0
category: behavior
platforms: [macos, linux]
created: 2026-04-14
tags: [cascade-prevention, dependency-tracking, surgical-changes, code-quality]
requires_toolsets: [terminal]
---

# Surgical Change Protocol

**Rule #1:** Before touching any code, you must understand its dependencies.

**Rule #2:** After touching any code, you must verify nothing broke.

This protocol prevents the most common failure mode in AI-assisted coding: fixing one thing and breaking three others.

---

## The Core Problem

```
You: "Rename getUser() to fetchUser()"
Agent: *renames the function*

Later: Tests fail.
Reason: 47 files were calling getUser(). None were updated.
```

**Cascade failures happen because:**
1. Agent doesn't see all callers of a function
2. Agent doesn't track that a change affects other files
3. Agent edits base/interface but forgets callers
4. Agent doesn't verify after making changes

---

## Pre-Edit Checklist

Before editing **any** file, always do this:

### Step 1: Identify the Target

```
What file are you editing?
What function/class are you changing?
What is the change? (rename, modify signature, change behavior)
```

### Step 2: Find All Callers

```bash
# Find all Python files that call this function
grep -r "function_name" --include="*.py" .

# Find all files that import this module
grep -r "from module import" --include="*.py" .
```

### Step 3: Read Every Caller

**Read each caller file BEFORE making changes.**
You need to understand:
- How does each caller use this function?
- What would break if I change it?
- Do I need to update each caller?

### Step 4: List All Files That Need Updates

Create a complete list:

```markdown
## Files to Edit

### MUST UPDATE (direct callers)
1. `src/service/user_service.py` - calls getUser()
2. `src/api/users.py` - imports from user module
...

### NEEDS VERIFICATION (indirect callers)
3. `tests/test_user.py` - uses getUser() in mocks
...
```

### Step 5: Order the Changes

```
ORDER: Base/Interface FIRST → Then Callers LAST

1. First: Update the function definition
2. Then: Update each caller, one by one
3. Last: Verify everything works
```

**Never update callers before the base is ready.**
**Never update only the base without updating callers.**

---

## Post-Edit Checklist

After making changes, verify systematically:

### Step 1: Verify Base Change Complete

```
Did you update ALL references to the old name/signature?
Run: grep -r "old_name" --include="*.py"
If results exist → you missed something
```

### Step 2: Verify Each Caller Updated

```
For each caller in your list:
- [ ] File was opened
- [ ] Call was updated
- [ ] New call was verified
```

### Step 3: Run Tests

```bash
# Run tests for the modified code
pytest tests/test_user.py -v

# Run full test suite if available
pytest -v
```

### Step 4: Manual Verification

```
For each change:
1. I made change X in file Y
2. I verified by [check method]
3. Result: [pass/fail]
```

---

## Cascade Prevention Rules

### Rule 1: No Blind Edits

```
BAD: User asks to change X. Agent changes X without checking callers.
GOOD: User asks to change X. Agent finds all callers, lists files, then changes.
```

### Rule 2: Systematic Order

```
BAD: Change caller1.py, then base.py, then caller2.py (chaotic order)
GOOD: Change base.py first, then caller1.py, then caller2.py (systematic order)
```

### Rule 3: Verify Before Moving On

```
BAD: Change base, change caller1, change caller2, then verify
GOOD: Change base → verify. Change caller1 → verify. Change caller2 → verify.
```

### Rule 4: Complete the List

```
BAD: 5 callers exist, only 4 updated
GOOD: Found 5 callers, updated all 5, verified all 5
```

---

## Common Scenarios

### Scenario 1: Renaming a Function

```
Task: Rename getUser() to fetchUser()

Pre-edit:
1. grep -r "getUser" .
2. Found 12 files using it
3. Read each file
4. List: base.py + 11 callers

Edit Order:
1. base.py (the function itself)
2. src/service/a.py
3. src/service/b.py
...
12. src/api/users.py

Post-edit:
1. grep "getUser" → should return nothing
2. grep "fetchUser" → should return 12 files
3. pytest → all pass
```

### Scenario 2: Changing Function Signature

```
Task: Add required parameter to processPayment()

Pre-edit:
1. Find all places calling processPayment()
2. Read each caller to understand usage
3. List all files needing updates

Edit Order:
1. Function definition with new parameter
2. Each caller, updated to pass the parameter
3. Verify all call sites are correct
```

### Scenario 3: Deleting a Function/Class

```
Task: Delete LegacyProcessor (deprecated)

Pre-edit:
1. grep for "LegacyProcessor"
2. Find all usages
3. If usages exist → CANNOT DELETE until all removed
4. If no usages → safe to delete

Rule: Never delete something still being used.
```

### Scenario 4: Changing a Class Hierarchy

```
Task: Add method to BaseClass

Pre-edit:
1. Find all subclasses
2. Find all places using polymorphism (BaseClass type)
3. Understand how the new method will be inherited

Edit Order:
1. BaseClass (add method)
2. Each subclass
3. Each caller
```

---

## Template: Change Execution Log

Use this template for every significant change:

```markdown
# Change: [Brief description]
Date: [Date]
Files: [List]

## Pre-Edit Research
Callers found: [N]
Files needing updates: [List]

## Edit Order
1. [File] - [What changed]
2. [File] - [What changed]
...

## Post-Edit Verification
- [ ] grep for old name - nothing found
- [ ] grep for new name - N matches
- [ ] pytest - all pass

## Cascade Risk
- [ ] No unintended changes
- [ ] All callers updated
```

---

## Integration with Other Skills

- Use [[karpathy-principles]] before starting
- Use [[goal-driven-execution]] to define success criteria
- Use [[dependency_tracker.py]] for automated caller finding

---

## Red Flags (Stop and Re-evaluate)

1. **"I think only a few files use this"** — You don't know until you grep
2. **"I'll just change it and see what breaks"** — This causes cascade failures
3. **"I updated most of them"** — All or nothing. Partial updates cause silent breaks
4. **"Tests pass locally"** — CI might have different state

---

## Related

- [[karpathy-principles]] — The four principles
- [[goal-driven-execution]] — Verify completion
- [[dependency_tracker.py]] — Script to find callers
