---
name: daily-review
description: Daily self-check and planning - review progress, identify next actions, maintain wiki health
version: 1.0.0
category: proactive
platforms: [macos, linux]
created: 2026-04-14
tags: [proactive, daily, review, planning, self-check]
requires_toolsets: [terminal]
---

# Daily Review

**Every day, take stock. Then act.**

This skill performs a daily self-check to maintain momentum and catch issues early.

---

## When to Run

**Daily, ideally at start of session:**
1. Morning start
2. After returning from break
3. Before ending session

---

## The Daily Review Workflow

### Step 1: Check Project States

```
For each active project:
- Read PROJECT_STATE.md
- Note current status
- Note blockers
```

### Step 2: Review Yesterday

```
Questions:
- What was accomplished?
- What didn't get done?
- What was learned?
```

### Step 3: Plan Today

```
Focus: 1-3 key items
Break down: First action for each
Identify: Any blockers?
```

### Step 4: Quick Health Check

```
Wiki health:
- Any broken links noticed?
- Any pages need updates?
- Any contradictions?
```

### Step 5: Update State

```
Update PROJECT_STATE.md with:
- Yesterday's progress
- Today's plan
- Any blockers
```

---

## Daily Review Template

```markdown
# Daily Review: {YYYY-MM-DD}

## Active Projects
| Project | Status | Progress |
|---------|--------|----------|
| | | |

## Yesterday's Accomplishments
- {Accomplishment 1}
- {Accomplishment 2}

## Yesterday's Learnings
- {Learning 1}
- {Learning 2}

## Today's Focus
1. **{Priority 1}**
   - First action: {action}
   - Success criteria: {criteria}
2. **{Priority 2}**
   - First action: {action}
3. **{Priority 3}** (if time)

## Blockers
- {Blocker 1}
- {Blocker 2}

## Health Check
- [ ] No broken links noticed
- [ ] No contradictions
- [ ] Wiki state up-to-date

## Notes
{Any other notes}
```

---

## Example Session

```
1. Daily review triggers

2. Check project states:
   Hermes Dojo: Phase 8 (Proactive)
   Progress: 80%
   Last: Phase 7 Quality complete

3. Review yesterday:
   - Phase 6 Automation complete
   - Phase 7 Quality complete
   - Started Phase 8 Proactive

4. Plan today:
   - Complete Phase 8 Proactive
   - QA Phase 8
   - Write final project summary

5. Quick health:
   - All phases documented
   - Skills indexed
   - Ready for final push

6. Update state:
   PROJECT_STATE.md updated
```

---

## Integration

- Use [[update-project-state]] — Update state
- Use [[periodic-nudge]] — Self-reflection
- Use with [[on-schedule]] — Daily schedule

---

## Related

- [[weekly-review]] — Weekly deep dive
- [[stale-detection]] — Find stale content
- [[pattern-discovery]] — Find patterns
- [[on-schedule]] — Scheduled automation
