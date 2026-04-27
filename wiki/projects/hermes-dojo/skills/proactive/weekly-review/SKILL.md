---
name: weekly-review
description: Weekly deep dive and skill updates - review week, update skills, plan next week
version: 1.0.0
category: proactive
platforms: [macos, linux]
created: 2026-04-14
tags: [proactive, weekly, review, planning, skill-updates]
requires_toolsets: [terminal]
---

# Weekly Review

**Every week, zoom out. Then zoom back in.**

This skill performs a comprehensive weekly review to maintain long-term direction and health.

---

## When to Run

**Weekly, ideally end of week:**
1. Every Friday
2. Start of new week (Monday)
3. End of sprint/cycle

---

## The Weekly Review Workflow

### Step 1: Review the Week

```
Questions:
- What were the major accomplishments?
- What didn't get done?
- What was the biggest learning?
- What was most frustrating?
```

### Step 2: Stats Collection

```
Collect:
- Pages created/updated
- Skills created/updated
- Projects progressed
- Mistakes logged
- Time spent
```

### Step 3: Skills Review

```
Questions:
- Any skills used that need updates?
- Any patterns observed that need skills?
- Any outdated skills?
```

### Step 4: Project Health

```
For each project:
- Progress this week
- Health status
- Blockers
- Confidence in completion
```

### Step 5: Plan Next Week

```
Focus areas:
1. {Area 1}
2. {Area 2}
3. {Area 3}

Key milestones:
- {Milestone 1}
- {Milestone 2}
```

---

## Weekly Review Template

```markdown
# Weekly Review: {Week of YYYY-MM-DD}

## Week Summary

**Major Accomplishments:**
- {Accomplishment 1}
- {Accomplishment 2}
- {Accomplishment 3}

**Didn't Get To:**
- {Item 1}
- {Item 2}

**Biggest Learning:**
- {Learning}

**Most Frustrating:**
- {Issue}

## Stats

| Category | Count |
|----------|-------|
| Pages Created | |
| Pages Updated | |
| Skills Created | |
| Skills Updated | |
| Mistakes Logged | |
| Projects Advanced | |

## Skills Review

### Skills Used
| Skill | Times Used | Needs Update? |
|-------|-----------|--------------|
| | | |

### New Patterns Observed
- {Pattern 1}
- {Pattern 2}

### Skills to Create
- {Skill 1}
- {Skill 2}

## Project Health

### {Project 1}
- Progress: {X}%
- Health: {Green/Yellow/Red}
- Blocker: {if any}

### {Project 2}
- Progress: {X}%
- Health: {Green/Yellow/Red}

## Next Week Plan

### Focus Areas
1. {Area 1}
2. {Area 2}

### Key Milestones
- {Milestone 1}
- {Milestone 2}

## Retro

### What Went Well
- {Item 1}

### What Could Improve
- {Item 1}

### Actions for Next Week
1. {Action 1}
2. {Action 2}
```

---

## Example Session

```
1. Weekly review triggers (Friday)

2. Review week:
   - Completed: Phases 5, 6, 7
   - Learned: Cascade prevention is behavioral, not technical
   - Frustrating: Some scripts needed bug fixes

3. Stats:
   - Skills: 8 created
   - Scripts: 3 created, 1 fixed
   - Commits: 5

4. Skills review:
   - cascade-prevention used heavily
   - Pattern: Every phase needs QA checklist
   - Skill to create: phase-qa-checklist

5. Project health:
   - Hermes Dojo: 85%, Green
   - On track for completion

6. Next week:
   - Complete Phase 8
   - Final integration testing
   - User testing

7. Retro:
   - Went well: Consistent phase-by-phase approach
   - Improve: More testing before marking done
```

---

## Integration

- Use [[daily-review]] — Daily check-ins
- Use [[skill-from-experience]] — Create skills from patterns
- Use [[skill-self-improve]] — Update skills
- Use with [[on-schedule]] — Weekly schedule

---

## Related

- [[daily-review]] — Daily check
- [[stale-detection]] — Content health
- [[pattern-discovery]] — Pattern finding
- [[on-schedule]] — Scheduled automation
