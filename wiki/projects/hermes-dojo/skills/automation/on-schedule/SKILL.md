---
name: on-schedule
description: Periodic maintenance hooks - daily lint, weekly deep review, stale detection, consolidation
version: 1.0.0
category: automation
platforms: [macos, linux]
created: 2026-04-14
tags: [automation, scheduled, maintenance, lint, consolidation, hooks]
requires_toolsets: [terminal]
---

# On-Schedule Hook

**Triggered on a periodic schedule.**

This hook performs regular maintenance to keep the wiki healthy.

---

## Schedule Types

| Type | Frequency | Actions |
|------|-----------|---------|
| Daily | Every day | Quick health check, backup |
| Weekly | Once a week | Deep review, skill updates |
| Monthly | Once a month | Full consolidation, stats |

---

## Daily Schedule

### Triggers: Every 24 hours

### Actions

1. **Quick Lint**
```
- Check for broken links
- Check for orphaned pages
- Check for missing frontmatter
```

2. **Stale Check**
```
- Find pages not updated in 30+ days
- Flag for review if still relevant
```

3. **Backup**
```
- git add -A
- git commit (if changes)
- git push (if remote configured)
```

---

## Weekly Schedule

### Triggers: Once per week

### Actions

1. **Deep Review**
```
- Review all project states
- Check for stalled projects
- Update progress indicators
```

2. **Skill Updates**
```
- Review skill usage stats
- Update outdated skills
- Create new skills from patterns
```

3. **Consolidation**
```
- Merge similar pages
- Archive outdated content
- Update indexes
```

4. **Stats Report**
```
- Pages created this week
- Knowledge graph growth
- Skills added
- Mistakes logged
```

---

## The On-Schedule Workflow

### Step 1: Determine Schedule Type

```
Check: Is this daily, weekly, or monthly?
Set: Appropriate actions based on type
```

### Step 2: Run Scheduled Actions

```
For each action in schedule:
1. Execute the action
2. Log results
3. Report issues
```

### Step 3: Update Monitoring

```
Record:
- Last run: {timestamp}
- Actions completed: {list}
- Issues found: {list}
```

### Step 4: Report

```
Summary to user (if active):
- Schedule type ran
- Actions completed
- Issues found
```

---

## Schedule Report Template

```markdown
# Schedule Report: {type}

**Date:** {YYYY-MM-DD HH:MM}
**Type:** {daily/weekly/monthly}

## Actions Completed

| Action | Status | Result |
|--------|--------|--------|
| | | |

## Issues Found

| Issue | Severity | Action Needed |
|-------|----------|---------------|
| | | |

## Stats
- Pages created: {N}
- Pages updated: {N}
- Skills created: {N}
- Knowledge graph: +{N} entities

## Next Scheduled
- {next run date}
```

---

## Integration

- Use [[stale_detector.py]] — Find stale content
- Use [[wiki_hooks.py]] — The hook engine
- Use [[skill-self-improve]] — Update skills
- Use [[memory-manage]] — Consolidate memories

---

## Related

- [[on-session-start]] — Session context loading
- [[on-session-end]] — Session compression
- [[on-ingest]] — Source processing
- [[wiki_hooks.py]] — Hook engine
- [[stale_detector.py]] — Stale detection
