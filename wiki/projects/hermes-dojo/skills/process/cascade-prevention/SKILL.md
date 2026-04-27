---
name: cascade-prevention
description: Systematic dependency checking before and after any code edit - prevents fixing one thing and breaking three others
version: 1.0.0
category: process
platforms: [macos, linux]
created: 2026-04-14
tags: [cascade-prevention, dependency-tracking, verification, safety]
requires_toolsets: [terminal]
---

# Cascade Prevention

**The #1 cause of AI coding failures: fixing one thing and breaking three others.**

This skill is a systematic checklist that MUST be followed before and after ANY code edit.

---

## The Core Problem

```
You ask: "Rename getUser() to fetchUser()"
Agent: *renames the function*

Later: Tests fail.
Why: 47 files called getUser(). None were updated.
```

**This is not a bug in the AI. This is a process failure.**

The AI doesn't automatically see all callers. YOU must enforce the process.

---

## The Golden Rule

```
BEFORE any edit:
1. Find all callers
2. List all files that need updates
3. Update base FIRST, then callers
4. Verify each caller was updated

AFTER any edit:
1. Verify no old references remain
2. Run tests
3. Update dependency graph if structure changed
```

---

## Pre-Edit Checklist

### Step 1: Identify What You're Changing

```
File: {path}
Function/Class: {name}
Change type: {rename / modify / delete / add}
```

### Step 2: Find All Callers

```bash
# Python
grep -rn "function_name" --include="*.py" .

# Also check for variations:
grep -rn "from module import" --include="*.py" .
grep -rn "class ClassName" --include="*.py" .
```

### Step 3: Read Every Caller

**Open each caller file. Read how it uses the function.**

Questions to answer:
- Does this caller pass parameters that might change?
- Does this caller depend on return value format?
- Does this caller need to be updated?

### Step 4: Create the Complete List

```markdown
## Files That MUST Update

### Direct Callers (must update)
1. src/service/user_service.py - calls getUser(id)
2. src/api/users.py - imports getUser from module
3. tests/test_user.py - mocks getUser

### Indirect (verify no impact)
4. src/service/order_service.py - calls user_service which calls getUser
```

### Step 5: Order Your Changes

```
ORDER: base/interface FIRST → callers LAST

1. src/models/user.py (the function itself)
2. src/service/user_service.py (caller 1)
3. src/api/users.py (caller 2)
...
```

---

## Post-Edit Checklist

### Step 1: Verify Base Change Complete

```bash
# For renames:
grep -rn "old_name" --include="*.py" .
# Should return: nothing

grep -rn "new_name" --include="*.py" .
# Should return: N files (all that use it)
```

### Step 2: Verify Each Caller Updated

```
For each file in your MUST UPDATE list:
- [ ] Opened the file
- [ ] Found the call/reference
- [ ] Updated it
- [ ] Verified the update looks correct
```

### Step 3: Run Tests

```bash
# Run tests for modified code
pytest tests/test_user.py -v

# Run full suite
pytest -v
```

### Step 4: Update Dependency Graph

If structure changed (new files, new functions, new imports):
```
1. Run: python3 ~/.hermes/scripts/dependency_tracker.py --scan . --output .codebase_graph.md
2. Review changes
3. Update manually if needed
```

---

## Scenario: Function Rename

```
TASK: Rename processPayment() to handlePayment()

PRE-EDIT:
$ grep -rn "processPayment" --include="*.py" .
src/service/payment.py:def processPayment(amount):
src/api/checkout.py:result = processPayment(total)
src/api/subscription.py:from payment import processPayment
tests/test_payment.py:mock.patch('payment.processPayment')

Found: 4 files using processPayment
List:
1. src/service/payment.py (the function itself)
2. src/api/checkout.py (calls it)
3. src/api/subscription.py (imports it)
4. tests/test_payment.py (mocks it)

ORDER:
1. payment.py (rename function)
2. checkout.py (update call)
3. subscription.py (update import)
4. test_payment.py (update mock)

EDIT (following order):
1. Rename in payment.py
2. Update call in checkout.py
3. Update import in subscription.py
4. Update mock in test_payment.py

POST-EDIT:
$ grep -rn "processPayment" --include="*.py" .
# Should return: nothing

$ grep -rn "handlePayment" --include="*.py" .
# Should return: 4 files ✓

$ pytest tests/test_payment.py -v
# All pass ✓
```

---

## Scenario: Changing Function Signature

```
TASK: Add required parameter to authenticate(token, scope)

PRE-EDIT:
$ grep -rn "authenticate(" --include="*.py" .
Found: 7 call sites

For each call site, read and identify:
- What arguments are currently passed?
- Which ones need the new scope parameter?

ORDER:
1. Function definition (add parameter)
2. Each call site (add argument)

EDIT:
1. authenticate(token, scope=None) ← new signature
2. login.py: authenticate(token, scope='user')
3. admin.py: authenticate(token, scope='admin')
4. api.py: authenticate(token) ← ERROR: needs scope now

POST-EDIT:
Fix remaining call sites
Run tests
```

---

## Scenario: Deleting Deprecated Code

```
TASK: Delete LegacyProcessor class

PRE-EDIT:
$ grep -rn "LegacyProcessor" --include="*.py" .
Found: 0 references

RULE: If references exist → CANNOT DELETE until removed
RULE: If no references → safe to delete

RESULT: No references. Safe to delete.
```

---

## Red Flags (STOP!)

### Flag 1: "I think only a few files use this"

```
Reality: You don't know until you grep.
Action: grep -rn "function_name" --include="*.py" .
```

### Flag 2: "I'll just change it and see what breaks"

```
Reality: This causes cascade failures.
Action: Always find all callers FIRST.
```

### Flag 3: "I updated most of them"

```
Reality: Partial updates cause silent breaks.
Action: ALL or NOTHING.
```

### Flag 4: "Tests pass locally"

```
Reality: CI might have different state.
Action: If possible, run full test suite.
```

---

## The Cascade Prevention Mindset

```
NOT: "I think this is safe to change"
BUT: "Let me verify by checking all callers"

NOT: "I updated the main file"
BUT: "I updated base, then verified each of the 12 callers"

NOT: "Tests pass, we're good"
BUT: "All success criteria met, no cascade risk identified"
```

---

## Integration

- Use [[surgical-change-protocol]] — The protocol this checklist is part of
- Use [[dependency_tracker.py]] — Script to automate caller finding
- Use [[goal-driven-execution]] — Verify completion
- Use with every [[implement-command]] — Always run before implementing

---

## Quick Reference Card

```
═══════════════════════════════════════════════
CASCADE PREVENTION CHECKLIST
═══════════════════════════════════════════════

PRE-EDIT:
[ ] 1. grep for function/class name
[ ] 2. Read ALL callers
[ ] 3. Create complete file list
[ ] 4. Order: base FIRST, callers LAST
[ ] 5. Only THEN start editing

POST-EDIT:
[ ] 1. grep for OLD name → nothing
[ ] 2. grep for NEW name → N files
[ ] 3. Verify EACH caller updated
[ ] 4. pytest → all pass
[ ] 5. Update dependency graph

═══════════════════════════════════════════════
```

---

## Related

- [[surgical-change-protocol]] — The protocol this is part of
- [[dependency_tracker.py]] — Script to automate finding
- [[implement-command]] — Execute changes with this checklist
- [[goal-driven-execution]] — Verify completion
