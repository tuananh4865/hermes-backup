---
name: contradiction-resolution
description: Resolve conflicting claims in wiki - find contradictions, propose resolutions based on recency and authority
version: 1.0.0
category: quality
platforms: [macos, linux]
created: 2026-04-14
tags: [contradiction, conflict-resolution, knowledge-quality, claims]
requires_toolsets: [terminal]
---

# Contradiction Resolution

**When facts conflict, resolve systematically.**

This skill identifies and resolves contradictory information in the wiki.

---

## The Problem

```
Page A says: "Use method X for authentication"
Page B says: "Method X is deprecated, use Y"

These contradict each other.
Left unresolved, users get conflicting guidance.
```

---

## The Contradiction Resolution Workflow

### Step 1: Detect Contradiction

```
Signs of contradiction:
- Two pages make opposing claims
- Same claim made with different facts
- Outdated info contradicts current info

Detection:
- During research, check for existing claims
- During ingest, check knowledge graph
- During quality check, flag conflicts
```

### Step 2: Identify the Contradicting Claims

```
Document both claims:
Claim A: {from Page A}
Claim B: {from Page B}

Evidence for each:
- Source
- Date
- Confidence
```

### Step 3: Analyze

```
Questions:
1. Which is more recent?
2. Which source is more authoritative?
3. Which has higher confidence?
4. Is one factually provable?

Factors:
- Recency: newer usually better for evolving topics
- Authority: official docs > articles > guess
- Confidence: higher confidence wins
- Evidence: verifiable > unverifiable
```

### Step 4: Propose Resolution

```
Resolution types:
1. Supersession: New replaces old (linked, both preserved)
2. Context: Both correct in different contexts
3. Correction: Old was wrong, new is correct
4. Uncertainty: Flag as "disputed" pending verification
```

### Step 5: Implement Resolution

```
For supersession:
1. Update old page: mark as superseded
2. Add link to new info
3. Update new page with supersession link

For context:
1. Add context clause to both
2. Clarify when each applies

For correction:
1. Mark old as incorrect
2. Explain why it was wrong
3. Add correct information
```

---

## Resolution Template

```markdown
# Contradiction Resolution

**Date:** {YYYY-MM-DD}
**Status:** Proposed / Resolved

## Contradicting Claims

### Claim A
**Source:** {Page A}
**Content:** {What it says}
**Date:** {YYYY-MM-DD}
**Confidence:** {X}

### Claim B
**Source:** {Page B}
**Content:** {What it says}
**Date:** {YYYY-MM-DD}
**Confidence:** {X}

## Analysis

| Factor | Claim A | Claim B |
|--------|---------|---------|
| Recency | | |
| Authority | | |
| Confidence | | |
| Evidence | | |

## Resolution

**Type:** Supersession / Context / Correction / Disputed

**Decision:**
{Explanation}

## Implementation

- [ ] Old claim marked as: {superseded/incorrect/context}
- [ ] New claim: {status}
- [ ] Links added: {Y/N}
- [ ] Related pages updated: {Y/N}

## Resolution Summary
{Markdown explaining the resolution for readers}
```

---

## Example: Supersession

```
CLAIM A: "Use SQLite for local storage (2024)"
CLAIM B: "PostgreSQL is better for production (2026)"

ANALYSIS:
- Claim A: older, less specific
- Claim B: newer, more authoritative

RESOLUTION: Supersession
- Claim B supersedes Claim A for production
- Claim A still valid for local development
- Add context to both pages
```

---

## Decision Factors

### Recency
```
Recent usually wins (especially for tech)
Exception: architectural principles don't change
```

### Authority
```
Official docs > Blog posts > Community posts > Guess
For tech: language docs > framework docs > tutorials
```

### Confidence
```
Higher confidence wins
Low confidence + high recency → might beat high confidence + old
```

### Evidence
```
Verifiable claims > Unverifiable claims
Code examples > Verbal descriptions
```

---

## Red Flags

1. **Ignoring contradictions** — "They can figure it out"
2. **Deleting the old claim** — Preserve history
3. **Not documenting resolution** — Future agents need context
4. **Forcing one perspective** — Sometimes both are valid in context

---

## Integration

- Use [[wiki-quality-score]] — Detect contradictions
- Use [[knowledge_graph.py]] — Query for conflicts
- Use [[self-heal]] — Implement resolution

---

## Related

- [[wiki-quality-score]] — Detect issues
- [[self-heal]] — Apply fixes
- [[knowledge_graph.py]] — Graph query
