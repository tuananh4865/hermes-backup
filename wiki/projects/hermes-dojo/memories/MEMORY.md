---
title: "Hermes Dojo Global Memory"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Hermes Dojo Global Memory

## Agent Principles

### Self-Evolution
- Every interaction teaches something
- Every mistake is a learning opportunity
- Skills are created from experience, not designed upfront
- Memory is curated, not accumulated

### Cascade Prevention
- Never edit without understanding dependencies
- Always check callers before changing functions
- Update base/interface before callers
- Verify each step before proceeding

### Quality Over Speed
- Research before coding
- Plan before implementing
- Verify after each step
- Confidence decays — knowledge has lifecycle

---

## Key Patterns

### Pattern: Research → Plan → Implement
```
1. Research: Understand the problem space
2. Plan: Define exact steps with verification
3. Implement: Follow plan, verify each step
4. Verify: Run tests, check callers
5. Update: File learnings, commit
```

### Pattern: Cascade Prevention
```
Before edit:
1. Run dependency tracker
2. Find ALL callers
3. Read ALL callers
4. List ALL files needing updates
5. Update base FIRST, then callers
```

### Pattern: Skill Self-Improvement
```
When better approach found mid-task:
1. Identify what changed
2. skill_manage(patch, old, new)
3. Never full rewrite (risks breaking)
```

---

## Mistakes Learned

| Date | Mistake | Lesson |
|------|---------|--------|
| | | |

---

## Skills Created

| Skill | Created | From |
|-------|---------|-------|
| | | |

---

## Recent Updates

| Date | Change |
|------|--------|
