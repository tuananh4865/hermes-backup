---
name: mistake-logging
description: Log mistakes systematically to learn from errors - creates mistake entry with root cause and prevention
version: 1.0.0
category: memory
platforms: [macos, linux]
created: 2026-04-14
tags: [mistakes, error-learning, root-cause, prevention]
requires_toolsets: [terminal]
---

# Mistake Logging

**Every mistake is a learning opportunity. If not logged, it's repeated.**

This skill creates structured mistake logs that prevent the same errors from recurring.

---

## When to Log

**Log a mistake when:**

1. **Bug took > 30 min to fix** — Time lost is evidence of systemic issue
2. **Same bug appeared before** — Recurring mistake
3. **User expressed frustration** — "Lỗi này sao lặp lại"
4. **Review feedback caught issue** — External catch
5. **Assumption proven wrong** — What you thought was correct was wrong

---

## The Mistake Log Template

```markdown
# Mistake: {Brief Title}

**Date:** {YYYY-MM-DD}
**Project:** {project name}
**Severity:** Minor / Moderate / Major / Critical

## What Happened
{Detailed description of the mistake}

## Root Cause
{Why did this happen?}

## Impact
- Time lost: {N} minutes/hours
- User impact: {description}
- Technical impact: {description}

## Lesson Learned
{What should be done differently?}

## Prevention Actions
1. {Action 1}
2. {Action 2}

## Related Mistakes
- {link to related mistake if any}

## Resolution
{How it was fixed}
```

---

## The Logging Workflow

### Step 1: Identify the Mistake

```
Questions:
- What went wrong?
- How long did it take to fix?
- Has this happened before?
- Did the user express frustration?

If bug took > 30 min OR same bug repeated → Log it
```

### Step 2: Document the Mistake

```
1. Create mistake file:
   memories/mistakes/{date}_{slug}.md

2. Fill in template:
   - What happened (be specific)
   - Root cause (dig deep)
   - Impact (time, user, technical)
   - Lesson learned (the key insight)
   - Prevention actions (concrete steps)
```

### Step 3: Update Relevant Skills

```
Did the mistake reveal a gap in a skill?
→ Update the skill to prevent recurrence
Use [[skill-self-improve]] for patch updates
```

### Step 4: Add to MEMORY.md

```
In MEMORY.md, add to Mistakes Learned table:
| {date} | {brief description} | {lesson} |
```

---

## Mistake Examples

### Example 1: Cascade Failure

```markdown
# Mistake: Cascade failure - renamed function without updating callers

**Date:** 2026-04-14
**Severity:** Major

## What Happened
User asked to rename `getUser()` to `fetchUser()`. 
Renamed the function but didn't check callers.
Tests failed. 47 files needed updates.

## Root Cause
Didn't run dependency check before editing.
Assumed "only a few files use this."

## Impact
- Time lost: 45 minutes
- 12 tests failing
- User frustrated with broken build

## Lesson Learned
Always run dependency tracker BEFORE any edit.
Never assume caller count.

## Prevention Actions
1. Run dependency_tracker.py before every edit
2. Create complete caller list before starting
3. Verify ALL callers updated before marking done

## Resolution
Ran grep to find all callers. Updated all 47 files.
Added `pre-edit-dependency-check` to every edit workflow.
```

### Example 2: Wrong Tool for Job

```markdown
# Mistake: Used web_extract for JavaScript-heavy page

**Date:** 2026-04-14
**Severity:** Minor

## What Happened
Tried to extract content from a React-rendered page.
web_extract returned almost nothing.
Had to switch to browser automation.

## Root Cause
Didn't check if page was JavaScript-rendered.
Assumed web_extract worked like curl.

## Impact
- Time lost: 15 minutes
- Had to redo research

## Lesson Learned
web_extract works for static HTML only.
JavaScript-rendered pages need browser automation.

## Prevention Actions
1. Check if page is React/Vue/Angular before choosing tool
2. If dynamic content suspected, use browser tool instead
3. For unknown pages, test with quick browser_snapshot first

## Resolution
Switched to browser_navigate + browser_snapshot.
Successfully extracted content.
```

---

## Common Mistakes to Watch For

| Mistake Type | Signs | Prevention |
|--------------|-------|------------|
| Cascade failure | Fix A breaks B | Dependency check before edit |
| Context overflow | Forgets early instructions | Periodic compaction |
| Wrong tool | Tool doesn't work | Check page type first |
| Skipping steps | "Done" but doesn't work | Verify each step |
| Assumption | "I think it works" | Verify with evidence |

---

## Severity Levels

| Level | Criteria | Example |
|-------|----------|---------|
| Minor | < 5 min fix | Wrong flag used |
| Moderate | 5-15 min fix | Simple bug |
| Major | 15-60 min fix | Complex cascade |
| Critical | > 60 min or user frustrated | Major regression |

---

## The Anti-Pattern

```
NOT: "Mistakes happen, move on"
BUT: "Every mistake is a data point. Log it. Fix the system."

NOT: "I figured it out, that's enough"
BUT: "The next agent will make the same mistake. Log it."

NOT: "It was a one-time thing"
BUT: "If it happened once, it might happen again. Log it."
```

---

## Integration

- Use [[skill-self-improve]] — Update skills to prevent recurrence
- Use [[periodic-nudge]] — Nudges can trigger mistake logging
- Use [[memory-manage]] — Updates MEMORY.md with mistake
- Use [[update-project-state]] — Mistakes affect project state

---

## Related

- [[skill-self-improve]] — Update skills from mistakes
- [[periodic-nudge]] — Nudge triggers mistake logging
- [[memory-manage]] — Memory updates
- [[MEMORY]] — Stores mistake table
