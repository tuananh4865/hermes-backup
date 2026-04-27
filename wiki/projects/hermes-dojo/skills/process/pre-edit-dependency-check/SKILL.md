---
name: pre-edit-dependency-check
description: Automated dependency checking before any code edit - runs dependency_tracker.py and displays cascade risk
version: 1.0.0
category: process
platforms: [macos, linux]
created: 2026-04-14
tags: [dependency-tracking, cascade-prevention, automation, verification]
requires_toolsets: [terminal]
---

# Pre-Edit Dependency Check

**Before you touch anything, run this check.**

This skill runs the dependency tracker and presents a cascade risk assessment before any code edit.

---

## When to Use

**ALWAYS.** Before editing ANY file, run this check.

This is not optional. This is part of every edit workflow.

---

## The Pre-Edit Check Workflow

### Step 1: Identify the File

```
What file are you about to edit?
What function/class/module in that file?
```

### Step 2: Run the Dependency Tracker

```bash
# Basic check on a file
python3 ~/.hermes/projects/hermes-dojo/scripts/dependency_tracker.py /path/to/project --scan --check path/to/file.py

# Or with a specific function
python3 ~/.hermes/projects/hermes-dojo/scripts/dependency_tracker.py /path/to/project --scan --check path/to/file.py --function function_name
```

### Step 3: Read the Output

The tracker will show:

```
=== PRE-EDIT DEPENDENCY CHECK ===
File: path/to/file.py

Functions defined in this file: N
  - function1
  - function2

Checking all functions...
  function1 — 5 callers:
    - src/a.py
    - src/b.py
    
  function2 — 2 callers:
    - src/c.py

=== CASCADE PREVENTION CHECKLIST ===
Before editing:
  [ ] Read ALL callers listed above
  [ ] List ALL files that need updates
  [ ] Update base/interface FIRST, then callers
After editing:
  [ ] Verify base change complete
  [ ] Verify EACH caller updated
  [ ] Run tests for base + callers
```

### Step 4: Acknowledge and Proceed

```
I have run the dependency check.
Callers found: N
Files that need updates: [list]

I understand the cascade risk.
I will:
1. Read ALL callers before editing
2. Update base FIRST, then callers
3. Verify EACH caller was updated
4. Run tests before marking done
```

---

## Interpreting Results

### Low Risk (0-1 callers)
```
Files that need updates: 1-2
Action: Still follow the checklist, but risk is low
```

### Medium Risk (2-5 callers)
```
Files that need updates: 3-6
Action: Be extra careful. Read each caller carefully.
```

### High Risk (5+ callers)
```
Files that need updates: 6+
Action: STOP. This is a major change.
  1. Confirm the change is necessary
  2. List every single file
  3. Execute systematically
  4. Run full test suite
```

---

## Manual Alternative

If the script isn't available:

```bash
# Find function callers
grep -rn "function_name" --include="*.py" .

# Find imports
grep -rn "from module import" --include="*.py" .

# Find class usage
grep -rn "ClassName" --include="*.py" .
```

---

## Integration

- Use [[surgical-change-protocol]] — The protocol this check is part of
- Use [[cascade-prevention]] — More detailed checklist
- Use [[implement-command]] — Execute with this check
- Use [[dependency_tracker.py]] — The script that powers this

---

## The Mindset

```
NOT: "I think this is a simple change"
BUT: "Let me run the dependency check to know for sure"

NOT: "Only a few files use this"
BUT: "The dependency check says X files use this. I will update all of them."
```

---

## Quick Reference

```bash
# Every time before editing:
python3 ~/.hermes/projects/hermes-dojo/scripts/dependency_tracker.py \
  /path/to/project \
  --scan \
  --check path/to/file.py
```

---

## Related

- [[cascade-prevention]] — Full checklist
- [[surgical-change-protocol]] — Surgical change protocol
- [[implement-command]] — Execute with verification
- [[dependency_tracker.py]] — The script
