---
name: crystallization
description: Distill completed work into structured digest pages - captures question, findings, entities, and lessons
version: 1.0.0
category: lifecycle
platforms: [macos, linux]
created: 2026-04-14
tags: [crystallization, distillation, digest, completed-work, lessons]
requires_toolsets: [terminal]
---

# Crystallization

**Transform completed work into lasting knowledge.**

Crystallization extracts the essence of completed work into structured digest pages.

---

## What is Crystallization?

```
Research → Exploration → Work → Outcome

Crystallization extracts:
- What was the question?
- What did we find?
- What entities were involved?
- What lessons emerged?
```

**Not a full summary.** A distillation. The 10% that matters from the 90% of work.

---

## When to Crystallize

**Trigger when:**

1. **Complex task complete** — 5+ hours of work
2. **Research complete** — Deep dive finished
3. **Major decision made** — With learnings
4. **Mistake recovered** — With insight gained
5. **Pattern discovered** — From multiple sessions

---

## The Crystallization Workflow

### Step 1: Review the Work

```
Questions:
- What was the original goal?
- What did we actually do?
- What was the outcome?
- What decisions were made?
```

### Step 2: Extract Key Elements

```
For each significant piece:
- Question: What were we trying to solve?
- Findings: What did we discover?
- Entities: What was involved?
- Lessons: What did we learn?
```

### Step 3: Structure the Digest

```
Use digest template:
- Brief context
- Key question
- Key findings
- Entities involved
- Lessons learned
- Related sources
```

### Step 4: File the Digest

```
Location: memories/digests/{date}_{slug}.md

Also:
- Link from related pages
- Update relevant indexes
```

---

## Digest Template

```markdown
---
title: Digest: {Topic}
date: {YYYY-MM-DD}
type: digest
tags: [digest, {category}]
related: [{links}]
---

# {Topic}

**Date:** {YYYY-MM-DD}
**Duration:** {Approximate time spent}
**Type:** {research|debug|analysis|exploration|decision}

## The Question

{What were we trying to solve or understand?}

## Key Findings

### Finding 1
{Brief description}
- Evidence: {source or reasoning}
- Implication: {why it matters}

### Finding 2
{Brief description}
- Evidence: {source or reasoning}
- Implication: {why it matters}

## Entities Involved

| Entity | Type | Role |
|--------|------|------|
| | | |

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| | |

## Lessons Learned

### Lesson 1
{What we learned}
Why: {Why this was valuable}

### Lesson 2
{What we learned}
Why: {Why this was valuable}

## Process Used

{How we approached this}

What worked:
- {What worked}

What didn't:
- {What didn't work}

## Related

- [Research: {link}](if applicable)
- [Plan: {link}](if applicable)
- [Skills created: {links}](if applicable)

## Summary

{2-3 sentence summary of the entire piece}
```

---

## Crystallization Examples

### Example 1: Research Digest

```
TASK: Deep research on context overflow solutions

CRYSTALLIZED:
---
title: "Digest: Context Overflow Solutions"
date: 2026-04-14
type: digest
tags: [digest, research, context-management]
---

# Context Overflow Solutions

## The Question
How do we prevent cascade failures caused by context overflow?

## Key Findings
1. Frequent compaction (40-60% target) is critical
2. Pre-edit dependency checks prevent cascade
3. Project state tracking enables session continuity

## Entities Involved
- Hermes Agent
- Wiki Memory System
- Dependency Tracker

## Lessons Learned
- Context window is the ONLY lever affecting output quality
- Cascade failures are process failures, not AI bugs

## Related
- Research: [[Context-Management-Research]]
- Implementation: [[Hermes-Dojo-Plan]]
```

### Example 2: Mistake Recovery Digest

```
TASK: Fixed cascade failure from renaming getUser()

CRYSTALLIZED:
---
title: "Digest: Cascade Failure from Function Rename"
date: 2026-04-14
type: digest
tags: [digest, mistake-recovery, cascade-prevention]
---

# Cascade Failure from Function Rename

## The Question
Why did renaming getUser() break 47 files?

## Key Findings
1. Dependency check was skipped
2. Agent assumed "few files use this"
3. Without grep, no way to know actual count

## Entities Involved
- dependency_tracker.py
- surgical-change-protocol

## Lessons Learned
- ALWAYS run dependency_tracker before ANY edit
- Assumption without verification = bug

## Related
- Skill: [[surgical-change-protocol]]
- Skill: [[cascade-prevention]]
```

---

## Quality Checklist

- [ ] Title is specific (not generic)
- [ ] Question clearly stated
- [ ] Findings are specific (not vague)
- [ ] Lessons are actionable (not obvious)
- [ ] Related links included
- [ ] Brief summary at end

---

## Integration

- Use [[skill-from-experience]] — Creates skills from patterns
- Use with [[on-session-end]] — After complex sessions
- Use [[self-heal]] — Quality check on digest

---

## Related

- [[skill-from-experience]] — Pattern extraction
- [[on-session-end]] — Session compression
- [[self-heal]] — Quality check
