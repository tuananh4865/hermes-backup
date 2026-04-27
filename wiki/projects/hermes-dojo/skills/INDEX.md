---
title: "Hermes Dojo Skills Index"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Hermes Dojo Skills Index

**Total skills:** 25 across 7 categories

## Behavior (3 skills) — ✅ COMPLETE

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| [[karpathy-principles]] | Four principles for professional AI behavior | 1 | ✅ Done |
| [[surgical-change-protocol]] | Prevent cascade failures when editing | 1 | ✅ Done |
| [[goal-driven-execution]] | Transform tasks into verifiable goals | 1 | ✅ Done |

## Process (4 skills) — ✅ COMPLETE

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| [[research-command]] | Understand before acting | 2 | ✅ Done |
| [[plan-command]] | Define exact path | 2 | ✅ Done |
| [[implement-command]] | Execute with verification | 2 | ✅ Done |
| [[cascade-prevention]] | Dependency tracking checklist | 2 | ✅ Done |

### Process - Additional

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| [[pre-edit-dependency-check]] | Automated dependency checking | 2 | ✅ Done |

## Memory (3 skills) — ✅ COMPLETE

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| [[memory-manage]] | 4-tier memory operations | 2 | ✅ Done |
| [[update-project-state]] | Track progress across sessions | 3 | ✅ Done |
| [[mistake-logging]] | Learn from errors | 3 | ✅ Done |

## Lifecycle (4 skills) — ✅ COMPLETE

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| [[skill-from-experience]] | Auto-create skills from patterns | 4 | ✅ Done |
| [[skill-self-improve]] | Patch-only skill updates | 4 | ✅ Done |
| [[periodic-nudge]] | Self-reflection triggers | 4 | ✅ Done |
| [[crystallization]] | Distill completed work into digest pages | 5 | ✅ Done |

## Quality (3 skills) — ✅ COMPLETE

| Skill | Description | Priority | Status |
|-------|-------------|----------|--------|
| [[wiki-quality-score]] | Score wiki content | 3 | ✅ Done |
| [[self-heal]] | Auto-fix lint issues | 3 | ✅ Done |
| [[contradiction-resolution]] | Resolve conflicting claims | 4 | ✅ Done |

## Automation (4 skills)

| Skill | Description | Priority |
|-------|-------------|----------|
| [[on-ingest]] | Auto-process new sources | 4 |
| [[on-session-start]] | Load relevant context from wiki | 3 |
| [[on-session-end]] | Compress session into observations | 4 |
| [[on-schedule]] | Periodic maintenance (lint, consolidate, decay) | 5 |

## Proactive (4 skills)

| Skill | Description | Priority |
|-------|-------------|----------|
| [[daily-review]] | Daily self-check and planning | 5 |
| [[weekly-review]] | Weekly deep dive and skill updates | 5 |
| [[stale-detection]] | Find content needing updates | 5 |
| [[pattern-discovery]] | Find useful patterns from past work | 5 |

---

## Skills by Priority

### P1 - Must Have (Week 1)
1. karpathy-principles
2. surgical-change-protocol
3. goal-driven-execution

### P2 - Should Have (Week 1-2)
4. research-command
5. plan-command
6. implement-command
7. cascade-prevention
8. memory-manage

### P3 - Important (Week 2-3)
9. update-project-state
10. mistake-logging
11. wiki-quality-score
12. self-heal
13. on-session-start

### P4 - Useful (Week 3-4)
14. skill-from-experience
15. skill-self-improve
16. periodic-nudge
17. contradiction-resolution
18. on-ingest
19. on-session-end

### P5 - Nice to Have (Week 4-5)
20. crystallization
21. on-schedule
22. daily-review
23. weekly-review
24. stale-detection
25. pattern-discovery

---

## Skill Format

```yaml
---
name: skill-name
description: Brief description
version: 1.0.0
category: behavior|process|memory|lifecycle|quality|automation|proactive
platforms: [macos, linux]
metadata:
  hermes:
    tags: [...]
    requires_toolsets: [...]
---

# Skill Name

## Purpose
What this skill does.

## When to Use
Trigger conditions.

## How to Use
Step-by-step instructions.

## Example
Usage example.
```

---

## Related

- [[AGENTS]] — Schema document
- [[SKILL]] — Project overview
