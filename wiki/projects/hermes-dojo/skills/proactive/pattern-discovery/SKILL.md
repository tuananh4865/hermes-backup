---
name: pattern-discovery
description: Find useful patterns from past work - analyze session logs, identify repeated workflows, extract reusable approaches
version: 1.0.0
category: proactive
platforms: [macos, linux]
created: 2026-04-14
tags: [proactive, pattern-discovery, analysis, workflows, reusable]
requires_toolsets: [terminal]
---

# Pattern Discovery

**Find the patterns that repeat. Extract them into skills.**

This skill analyzes past work to discover patterns worth preserving as reusable knowledge.

---

## What is a Pattern?

```
A pattern is:
- A workflow repeated 3+ times
- A non-obvious solution
- A learned approach
- A successful strategy

Not:
- One-time solutions
- Obvious practices
- Unique circumstances
```

---

## The Pattern Discovery Workflow

### Step 1: Collect Evidence

```
Sources:
- Session summaries (memories/sessions/)
- Mistake logs (memories/mistakes/)
- Project states
- Git commit messages

Questions:
- What keeps coming up?
- What keeps working?
- What keeps failing?
```

### Step 2: Identify Candidates

```
Pattern candidates:
1. {workflow} - seen N times
2. {solution} - used in N situations
3. {approach} - successful repeatedly
```

### Step 3: Analyze the Pattern

```
For each candidate:
- What is the pattern?
- When does it apply?
- What are the steps?
- What makes it work?
```

### Step 4: Evaluate

```
Questions:
- Will this repeat?
- Is it non-obvious?
- Is it worth extracting?
- Can it be generalized?

If YES → Create skill
If NO → Document as lesson
```

### Step 5: Extract to Skill

```
Use [[skill-from-experience]]:
- Create skill file
- Document steps
- Add examples
- Update index
```

---

## Pattern Categories

### Workflow Patterns

```
Examples:
- R→P→I workflow
- Cascade prevention checklist
- Dependency check before edit
- Session end update
```

### Solution Patterns

```
Examples:
- Use grep before editing
- Check callers before refactoring
- Run tests after every change
```

### Anti-Patterns

```
Examples:
- Skipping the plan
- Assuming without verifying
- Editing without reading first
```

---

## Pattern Analysis Template

```markdown
# Pattern Discovery: {Pattern Name}

**Date:** {YYYY-MM-DD}
**Type:** Workflow / Solution / Anti-Pattern
**Confidence:** High / Medium / Low

## Evidence

### Where Seen
| Session/Project | Date | Context |
|-----------------|------|---------|
| | | |

### Frequency
- Seen {N} times
- Success rate: {X}%

## Pattern Description

### What
{What the pattern is}

### When
{When to apply this pattern}

### How
{Steps if workflow}

### Why
{Why this works}

## Evaluation

| Criteria | Score | Notes |
|----------|-------|-------|
| Will repeat? | High/Med/Low | |
| Non-obvious? | High/Med/Low | |
| Worth extracting? | High/Med/Low | |

## Recommendation
- [ ] Create skill: {name}
- [ ] Document as lesson
- [ ] Not worth extracting

## Skill (if created)
{Skill details}
```

---

## Example Pattern Discovery

```
1. Pattern discovery runs (weekly)

2. Collect evidence:
   Session logs show:
   - "Forgot to check callers" (3 times)
   - "Ran grep before edit" (success in 5 cases)
   - "Updated state at end" (maintained continuity)

3. Identify candidates:
   1. Pre-edit dependency check - HIGH
   2. Session state update - MEDIUM
   3. Test after every change - MEDIUM

4. Analyze:
   PRE-EDIT DEPENDENCY CHECK:
   - Seen: 8 times
   - Success: 100% when used
   - Failures: All when skipped
   
   Pattern: Always run dependency_tracker before editing

5. Evaluate:
   - Will repeat: HIGH
   - Non-obvious: HIGH
   - Worth extracting: HIGH
   
6. Extract:
   Created skill: [[pre-edit-dependency-check]]
```

---

## Discovery Sources

### Session Logs
```
Look for:
- Repeated workflows
- Decision patterns
- Recovery patterns
```

### Mistake Logs
```
Look for:
- Same mistake twice
- Recovery approaches
- Prevention strategies
```

### Project States
```
Look for:
- Repeated blockers
- Successful approaches
- Progress patterns
```

---

## Integration

- Use [[skill-from-experience]] — Extract patterns
- Use [[periodic-nudge]] — Trigger discovery
- Use [[weekly-review]] — Weekly analysis

---

## Related

- [[skill-from-experience]] — Extract patterns
- [[periodic-nudge]] — Self-reflection
- [[weekly-review]] — Weekly analysis
