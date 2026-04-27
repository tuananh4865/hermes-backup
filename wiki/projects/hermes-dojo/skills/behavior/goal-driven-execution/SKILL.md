---
name: goal-driven-execution
description: Transform any task into verifiable goals with plan-verify loop - prevents vague completion and ensures actual results
version: 1.0.0
category: behavior
platforms: [macos, linux]
created: 2026-04-14
tags: [goal-setting, verification, planning, execution, tdd]
requires_toolsets: [terminal]
---

# Goal-Driven Execution

**The biggest trap in AI-assisted work:** Saying "done" without actually completing the goal.

This skill transforms vague tasks into verifiable goals, then ensures every step is proven before moving on.

---

## The Problem

```
User: "Set up auth"
Agent: *does stuff* "Done! Auth is set up."
User: *tries to login* "It doesn't work."
```

**What went wrong:**
- "Set up auth" was never defined
- No success criteria were established
- No verification happened

**Goal-driven execution prevents this by:**
1. Defining "done" before starting
2. Creating a verifiable plan
3. Checking each step
4. Proving completion

---

## The Framework

### Step 1: Define Success Criteria

**Before touching anything, ask:**

```
"What does success look like?"
"Specifically, what should be true when this is complete?"
"How will we know it's working?"
```

**Turn vague into specific:**

| Vague | Specific |
|-------|----------|
| "Set up auth" | "User can login with email/password and receive JWT token |
| "Fix the bug" | "When user submits form with empty email, they see inline error 'Email required'. No crash. |
| "Add caching" | "GET /api/users returns in <50ms for cached data. Cache invalidates on POST/PUT/DELETE |

**Template:**
```markdown
SUCCESS CRITERIA:
- [ ] [Specific outcome 1]
- [ ] [Specific outcome 2]
- [ ] [Specific outcome 3]
```

---

### Step 2: Create a Verifiable Plan

**For each step, define:**
1. What to do
2. How to verify it worked

```markdown
PLAN:
1. [Step] → verify: [how to check this worked]
2. [Step] → verify: [how to check this worked]
3. [Step] → verify: [how to check this worked]
```

**Rules:**
- Each step must have a verification method
- "Verify by running tests" is acceptable
- "Verify by checking" is not — specify what to check

**Good:**
```markdown
1. Add email validation regex → verify: grep for "email.*regex", confirm pattern matches test@ex.com but not invalid
2. Create error state in form → verify: inspect element, class "error" present
```

**Bad:**
```markdown
1. Add email validation → verify: done
2. Create error state → verify: looks good
```

---

### Step 3: State Your Plan

**Before starting, say:**

```
My understanding of the goal:
- [What success looks like]

My plan:
1. [Step] → verify: [check]
2. [Step] → verify: [check]

I'll start now.
```

**This catches misunderstandings early** — if the user corrects your plan, you haven't wasted time.

---

### Step 4: Execute with Verification

**For each step:**
1. Do the step
2. Run the verification check
3. If verification fails → fix before moving on
4. If verification passes → proceed

```
1. Add email validation → verify: run test_email_validation.py
   Result: PASS ✓
2. Add error state → verify: manual test with empty form
   Result: PASS ✓
```

**Never skip verification because "it probably works."**

---

### Step 5: Confirm Completion

**When done:**

```markdown
COMPLETE.

Success Criteria Verification:
- [✓] User can login with email/password — tested with testuser@test.com / password123
- [✓] JWT token returned — decoded payload contains user_id, exp > now
- [✓] Invalid credentials return 401 — confirmed with wrong password

All criteria met. Task complete.
```

---

## The Verification Loop

```
EXECUTE → VERIFY → PASS? → YES → NEXT STEP
                         ↓ NO
                      FIX → RE-VERIFY
```

**Never:**
- Execute 5 steps then verify
- Mark done without checking criteria
- Assume success without proof

**Always:**
- Verify each step
- Fix failures immediately
- Prove completion with evidence

---

## Common Patterns

### Pattern 1: Bug Fix

```
Goal: "Fix the login bug"

1. Define success:
   - Empty email shows error message
   - Invalid email shows error message
   - Valid email+password logs in
   - Wrong password shows error

2. Create plan:
   1. Reproduce bug → verify: empty email crashes
   2. Add validation → verify: empty email shows error
   3. Test all cases → verify: pytest passes

3. Execute and verify each step
```

### Pattern 2: Feature Add

```
Goal: "Add dark mode"

1. Define success:
   - Toggle in settings switches theme
   - Preference persists on reload
   - Both light and dark themes look correct

2. Create plan:
   1. Add theme context → verify: console.log shows current theme
   2. Add toggle component → verify: click toggles theme
   3. Persist to localStorage → verify: reload preserves theme
   4. Add dark CSS → verify: dark theme applies

3. Execute and verify each step
```

### Pattern 3: Refactor

```
Goal: "Clean up auth module"

1. Define success:
   - All existing auth tests pass
   - No changes to external API
   - New structure is more logical

2. Create plan:
   1. Document current exports → verify: list matches current usage
   2. Create new structure → verify: imports work
   3. Migrate one function → verify: tests pass
   4. Migrate remaining → verify: full suite passes

3. Execute and verify each step
```

---

## Verification Methods

| Method | When to Use |
|--------|-------------|
| `pytest` | Code has tests |
| `grep` | Checking for presence/absence of strings |
| `curl` | API endpoints |
| Manual test | UI changes, things without tests |
| Inspect element | DOM changes |
| Read file | Confirmation of content |
| Diff | Comparing before/after |

---

## Failure Modes

### Failure 1: Skipping Definition

```
Wrong: Proceeding without defining success criteria
Right: "What does 'done' look like for this task?"
```

### Failure 2: Vague Verification

```
Wrong: "verify: looks good"
Right: "verify: pytest tests/test_auth.py -v shows 5/5 pass"
```

### Failure 3: Deferred Verification

```
Wrong: "I'll verify at the end"
Right: Verify after each step. Catch failures early.
```

### Failure 4: Claiming Completion Prematurely

```
Wrong: "Done!" after only step 1 of 5
Right: "Step 1 complete. Starting step 2."
```

---

## Integration

- Use with [[karpathy-principles]] — Think before coding
- Use with [[surgical-change-protocol]] — Change systematically
- Use with [[plan-command]] — Formal plan artifact

---

## Quick Reference

```
GOAL: [specific outcome]

PLAN:
1. [Step] → verify: [check]
2. [Step] → verify: [check]

EXECUTE:
1. Do → Check → Pass? → Next
2. Do → Check → Pass? → Next

COMPLETE:
- [✓] Criteria 1 - evidence
- [✓] Criteria 2 - evidence
```

---

## Related

- [[karpathy-principles]] — Think before coding
- [[surgical-change-protocol]] — Change systematically
- [[plan-command]] — Formal plan artifact
