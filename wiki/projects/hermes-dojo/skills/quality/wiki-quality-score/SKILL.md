---
name: wiki-quality-score
description: Score wiki content quality using knowledge quality formula - Originality, Depth, Actionability, Clarity, Completeness
version: 1.0.0
category: quality
platforms: [macos, linux]
created: 2026-04-14
tags: [quality, scoring, wiki-metrics, content-quality, assessment]
requires_toolsets: [terminal]
---

# Wiki Quality Score

**Score wiki content quality systematically.**

This skill scores wiki pages using a multi-factor formula, enabling quality gates and improvement tracking.

---

## The Quality Formula

```
Score = (Orig × 0.25 + Depth × 0.25 + Action × 0.20 + Clarity × 0.15 + Complete × 0.15) × 2

Range: 0-10
Minimum for publish:
- Concept: 7.0
- Tutorial: 7.5
- Research: 8.0
- Deep Dive: 8.5
```

---

## The Five Factors

### 1. Originality (Orig) — 25%

**What:** How unique is this content?

| Score | Description |
|-------|-------------|
| 0-3 | Generic/compile of other sources |
| 4-6 | Some original insights |
| 7-8 | Mostly original work |
| 9-10 | Highly original, novel insights |

**Assessment questions:**
- Does this teach something new?
- Is this the only page on this topic?
- Are the examples original?

### 2. Depth — 25%

**What:** How thoroughly is this covered?

| Score | Description |
|-------|-------------|
| 0-3 | Surface-level only |
| 4-6 | Good coverage of basics |
| 7-8 | Comprehensive coverage |
| 9-10 | Exhaustive, no gaps |

**Assessment questions:**
- Would a reader need more sources?
- Are edge cases covered?
- Is the topic fully explored?

### 3. Actionability (Action) — 20%

**What:** Can someone ACT on this?

| Score | Description |
|-------|-------------|
| 0-3 | Theoretical only |
| 4-6 | Some practical guidance |
| 7-8 | Clear actionable steps |
| 9-10 | Complete with examples/tests |

**Assessment questions:**
- Can someone do X after reading?
- Are there examples?
- Are there verification steps?

### 4. Clarity — 15%

**What:** How clear is the writing?

| Score | Description |
|-------|-------------|
| 0-3 | Confusing, disorganized |
| 4-6 | Understandable with effort |
| 7-8 | Clear and readable |
| 9-10 | Exceptionally clear |

**Assessment questions:**
- Is structure logical?
- Is language precise?
- Are concepts explained?

### 5. Completeness — 15%

**What:** Is anything missing?

| Score | Description |
|-------|-------------|
| 0-3 | Major gaps |
| 4-6 | Some missing pieces |
| 7-8 | Mostly complete |
| 9-10 | Fully complete |

**Assessment questions:**
- Are prerequisites covered?
- Are related topics linked?
- Is frontmatter complete?

---

## The Scoring Workflow

### Step 1: Read the Page

```
Full content read-through
Note initial impressions
```

### Step 2: Score Each Factor

```
For each factor (1-10):
- Give score based on criteria
- Note evidence for score
```

### Step 3: Calculate Total

```
Score = (Orig×0.25 + Depth×0.25 + Action×0.20 + Clarity×0.15 + Complete×0.15) × 2
```

### Step 4: Determine Action

| Score | Action |
|-------|--------|
| 9+ | Publish immediately |
| 8+ | Publish with minor polish |
| 7+ | Publish (if topic warrants) |
| 6-7 | Flag for expansion |
| 5-6 | Major revision needed |
| <5 | Rewrite or delete |

---

## Quality Score Template

```markdown
# Quality Score: {Page Name}

**Date:** {YYYY-MM-DD}
**Page:** {link}
**Type:** {concept/tutorial/research/deep dive}

## Factor Scores

| Factor | Weight | Score (1-10) | Weighted |
|--------|--------|--------------|----------|
| Originality | 0.25 | | |
| Depth | 0.25 | | |
| Actionability | 0.20 | | |
| Clarity | 0.15 | | |
| Completeness | 0.15 | | |
| **TOTAL** | | | ×2 = **{Score}** |

## Evidence

### Originality
{Score}: {Evidence}

### Depth
{Score}: {Evidence}

### Actionability
{Score}: {Evidence}

### Clarity
{Score}: {Evidence}

### Completeness
{Score}: {Evidence}

## Issues Found
- {Issue 1}
- {Issue 2}

## Recommendations
1. {Recommendation 1}
2. {Recommendation 2}

## Decision
- [ ] Ready to publish (7.0+)
- [ ] Needs revision (6.0-7.0)
- [ ] Major rewrite (<6.0)
```

---

## Integration

- Use [[self-heal]] — Fix auto-fixable issues
- Use [[crystallization]] — Distill high-quality work
- Use with [[on-schedule]] — Periodic quality review

---

## Related

- [[self-heal]] — Auto-fix quality issues
- [[contradiction-resolution]] — Resolve conflicts
- [[crystallization]] — Distill completed work
