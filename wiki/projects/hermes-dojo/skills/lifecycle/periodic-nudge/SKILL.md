---
name: periodic-nudge
description: Self-reflection triggers at key moments - prompts Hermes to review and improve without human prompting
version: 1.0.0
category: lifecycle
platforms: [macos, linux]
created: 2026-04-14
tags: [self-reflection, nudges, periodic-review, self-improvement]
requires_toolsets: [terminal]
---

# Periodic Nudge

**Self-reflection without human prompting.**

This skill triggers internal self-reflection at key moments, prompting Hermes to review recent actions and improve.

---

## Trigger Conditions

A nudge fires when:

1. **Every 10 tool calls** — Context getting full
2. **On error** — Something went wrong
3. **On user correction** — User corrected the approach
4. **On complex task complete** — Task with 5+ steps finished
5. **On session end** — Session is ending

---

## The Nudge Response

When a nudge fires, Hermes receives:

```
[NUDGE - Self-Reflection Triggered: {type}]

{Message}

## Recent Activity Summary
- Tool calls: {N}
- Last error: {if any}
- User corrections: {N}

## Reflection Questions
1. What worked well?
2. What could be improved?
3. Is there a pattern worth documenting?
4. Should any new information be added to memory?

## Actions Available
- Add to MEMORY.md
- Create new skill
- Update existing skill
- Log mistake
- Update PROJECT_STATE.md
```

---

## How to Respond to a Nudge

### Step 1: Review Recent Actions

```
Look back at the last N tool calls.
What happened?
What was the context?
What was the goal?
```

### Step 2: Answer Reflection Questions

```
1. What worked well?
   - Identify successes
   - Note what made them work

2. What could be improved?
   - Identify failures or inefficiencies
   - Note what caused them

3. Is there a pattern worth documenting?
   - Repeated workflow?
   - Non-obvious success?
   - Recovery pattern?

4. Should any new information be added to memory?
   - User preference discovered?
   - Decision made?
   - Mistake logged?
```

### Step 3: Take Action

```
Based on answers:
- MEMORY.md: Add if important insight
- SKILL: Create or update if pattern found
- MISTAKE: Log if error occurred
- PROJECT_STATE: Update if task in progress
```

---

## Trigger Details

### Trigger 1: Every 10 Tool Calls

```
Purpose: Prevent context overflow
Context: 40-60% utilization recommended

Action:
1. Compact recent work into summary
2. Identify worth-saving information
3. Update memory if needed
4. Clear working context
```

### Trigger 2: On Error

```
Purpose: Learn from failures
Context: An action failed or produced wrong result

Action:
1. What was the error?
2. What caused it?
3. How was it fixed (if fixed)?
4. Should this be logged as a mistake?
5. Can this be prevented?
```

### Trigger 3: On User Correction

```
Purpose: Capture correct approaches
Context: User said "no, do it this way"

Action:
1. What was my approach?
2. What was the correct approach?
3. Why was mine wrong?
4. Create skill or update existing?
5. Add to MEMORY.md?
```

### Trigger 4: On Complex Task Complete

```
Purpose: Extract reusable patterns
Context: Task with 5+ steps completed successfully

Action:
1. What was the task?
2. What workflow was used?
3. Was this done before?
4. Should this become a skill?
5. Any lessons worth saving?
```

### Trigger 5: On Session End

```
Purpose: Ensure continuity
Context: Session is ending

Action:
1. Update PROJECT_STATE.md
2. Log any decisions made
3. Note any in-progress work
4. Define next steps
5. Add learnings to MEMORY.md
```

---

## Nudge Response Template

```markdown
## Nudge Response: {type}

**Date:** {YYYY-MM-DD}

### Recent Summary
{Brief summary of what happened}

### What Worked
-

### What Could Improve
-

### Pattern Detected
-

### Actions Taken
- [ ] Added to MEMORY.md
- [ ] Created skill: {name}
- [ ] Updated skill: {name}
- [ ] Logged mistake: {name}
- [ ] Updated PROJECT_STATE.md
- [ ] No action needed
```

---

## Mindset

```
NOT: "The user will tell me if I made a mistake"
BUT: "I should reflect and catch issues myself"

NOT: "I'll remember what happened"
BUT: "I should save what's worth remembering"

NOT: "The work is done when the task is done"
BUT: "The work is done when learnings are captured"
```

---

## Integration

- Use [[skill-from-experience]] — Create skills from patterns
- Use [[skill-self-improve]] — Improve skills
- Use [[mistake-logging]] — Log errors
- Use [[update-project-state]] — Update project state
- Use [[memory-manage]] — Manage memory tiers

---

## Related

- [[skill-from-experience]] — Create skills
- [[skill-self-improve]] — Improve skills
- [[mistake-logging]] — Log mistakes
- [[update-project-state]] — Update state
- [[memory-manage]] — Memory management
