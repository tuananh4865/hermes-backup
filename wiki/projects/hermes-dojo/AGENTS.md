---
title: "Hermes Dojo Schema (AGENTS.md)"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Hermes Dojo Schema (AGENTS.md)

## What This Is

**This is the most important file in the system.** This schema turns a generic LLM into a disciplined knowledge worker for Hermes Dojo.

Co-evolved between human and LLM over time. First version is rough. After iterations, this reflects how the domain actually works.

---

## Domain: Intelligent Wiki Management

### Core Problem We Solve
- Wiki accumulates knowledge but becomes stale/noisy
- Cascade failures when editing (fix here, break there)
- Agent forgets project state between sessions
- Knowledge doesn't compound (same mistakes repeated)

### Core Solution
- Persistent memory with confidence scoring
- Dependency tracking prevents cascade
- Event-driven automation keeps wiki healthy
- Crystallization turns completed work into reusable knowledge

---

## Entity Types

### Person
```yaml
attributes:
  - name: string
  - role: string
relationships:
  - owns: Project, Decision
  - has_opinions_about: Concept, Library
```

### Project
```yaml
attributes:
  - name: string
  - status: active | paused | completed | abandoned
  - created: date
relationships:
  - depends_on: Project, Library
  - owned_by: Person
  - produces: File, Concept
```

### Library
```yaml
attributes:
  - name: string
  - version: string (optional)
  - language: string (optional)
relationships:
  - uses: Library, Concept
  - alternative_to: Library
  - documented_in: File
```

### Concept
```yaml
attributes:
  - name: string
  - definition: string
  - confidence: float (0-1)
relationships:
  - related_to: Concept
  - defined_by: File, Decision
  - used_by: Project, Library
```

### File
```yaml
attributes:
  - path: string
  - type: markdown | python | yaml | json | etc
  - size: int (optional)
relationships:
  - contains: Concept, Decision
  - modified_by: Person
  - referenced_by: File
```

### Decision
```yaml
attributes:
  - title: string
  - date: date
  - rationale: string
  - status: active | superseded | rejected
relationships:
  - made_by: Person
  - supersedes: Decision (optional)
  - documented_in: File
  - affects: Project, Library, Concept
```

---

## Relationship Types

| Type | Direction | Description |
|------|-----------|-------------|
| `uses` | A → B | A uses B (project uses library) |
| `depends_on` | A → B | A depends on B (breaking change impact) |
| `contradicts` | A → B | A contradicts B (claims conflict) |
| `caused` | A → B | A caused B (root cause chain) |
| `fixed` | A → B | A fixed B (bug → resolution) |
| `supersedes` | A → B | A is newer than B (info update) |
| `owns` | Person → Project/Decision | Ownership |
| `related_to` | A → B | General relationship |
| `documented_in` | A → File | Where A is documented |

---

## Confidence Scoring

### Factors
```yaml
source_count:
  description: Number of independent sources supporting this claim
  weight: 0.25
  max: 5

recency:
  description: How recently was this confirmed
  weight: 0.25
  decay_halflife:
    architecture_decision: 180 days
    project_fact: 30 days
    transient_bug: 7 days

reinforcement:
  description: Times accessed and confirmed
  weight: 0.20
  max: 10

contradiction:
  description: Number of contradicting claims
  weight: 0.30
  penalty: -0.1 per contradiction
```

### Formula
```
confidence = (
  0.25 * min(source_count, 5) / 5 +
  0.25 * decay(days_since_confirm, half_life) +
  0.20 * min(reinforcement_count, 10) / 10 -
  0.30 * contradiction_count * 0.1
)
```

### Thresholds
```yaml
confidence_excellent: >= 0.8
confidence_good: >= 0.6
confidence_fair: >= 0.4
confidence_poor: < 0.4
```

---

## Ingest Rules

### When Processing a New Source

1. **Extract entities**
   - Identify Person, Project, Library, Concept, File, Decision
   - Assign attributes
   - Map relationships

2. **Score confidence**
   - Calculate initial confidence based on source type
   - (article: 0.7, conversation: 0.5, guess: 0.3)

3. **Check for contradictions**
   - Query graph for existing claims about same topic
   - If contradiction found → trigger supersession

4. **Update graph**
   - Add new entities and relationships
   - Link supersessions
   - Update confidence scores

5. **Update index**
   - Add to wiki index if new page needed
   - Update existing pages if updating

---

## Quality Standards

### Publishing Thresholds

| Page Type | Minimum Score |
|-----------|---------------|
| Concept | 7.0 |
| Tutorial | 7.5 |
| Research | 8.0 |
| Deep Dive | 8.5 |

### Auto-Fixable Issues

```yaml
auto_fix:
  - broken_wikilinks: auto-repair or flag
  - formatting_errors: auto-fix
  - missing_frontmatter: add template
  - orphan_pages: flag for linking

flag_only:
  - stub_content: needs expansion
  - outdated_info: needs review
  - contradictions: needs resolution
```

### Self-Healing Rules

1. **Broken links**: Attempt repair → if fail, flag and list alternatives
2. **Stale claims**: Mark with timestamp, reduce confidence
3. **Contradictions**: Propose resolution based on recency + authority
4. **Orphan pages**: Attempt to find related pages → if fail, flag

---

## Workflow Rules

### Research Before Code

**For any non-trivial task:**
1. Create research artifact
2. Map dependency graph
3. Identify all affected files
4. Plan exact steps
5. Get human review (if complex)

### Dependency Tracking

**Before any edit:**
1. Run dependency check
2. Find ALL callers/importers
3. Read ALL affected files
4. List ALL files needing updates
5. Update base/interface FIRST, then callers

**After any edit:**
1. Verify base change complete
2. Verify EACH caller updated
3. Run tests
4. Update graph if structure changed

### Project State

**After each session:**
1. Update PROJECT_CONTEXT.md
2. Log decisions made
3. Note blockers and next steps
4. Commit with code changes

---

## Memory Tiers

### Working Memory
- Recent observations, not yet processed
- Uncompressed, high fidelity
- Auto-cleared after session

### Episodic Memory
- Session summaries, compressed
- Created: end of each session
- Promoted to Semantic: after 3+ related sessions

### Semantic Memory
- Cross-session facts, consolidated
- Created: from episodic promotions
- Promoted to Procedural: after pattern confirmed 3+ times

### Procedural Memory
- Workflows and patterns
- Created: from repeated semantic
- Stored as skills

---

## Consolidation Schedule

| From | To | Trigger | Action |
|------|----|---------|--------|
| Working | Episodic | Session end | Compress observations |
| Episodic | Semantic | 3+ sessions confirm same fact | Merge facts |
| Semantic | Procedural | Same workflow seen 3+ times | Create skill |

---

## Retention Decay

### Ebbinghaus Curve
```
retention = initial_confidence * (0.5 ^ (days_elapsed / half_life))
```

### Actions Based on Retention

| Retention | Action |
|------------|--------|
| >= 0.5 | Full priority in queries |
| 0.3 - 0.5 | Deprioritized |
| 0.1 - 0.3 | Archived (can restore) |
| < 0.1 | Hidden (require explicit access) |

### Reinforcement
- Access to fact: reset decay timer
- Confirmation from new source: boost confidence

---

## Privacy Scoping

### Private (Personal)
- User preferences (USER.md)
- Personal notes
- Session observations before compression

### Shared (Project)
- Wiki pages
- Knowledge graph
- Skills
- AGENTS.md (this file)

---

## When to Create vs Update

### Create New Page When
- New topic not covered
- Existing page score < 5.0
- Content diverges significantly from existing

### Update Existing When
- Same topic covered
- Existing score >= 5.0
- Update adds value without divergence

### Supersede When
- New information contradicts old
- New source is more authoritative
- Old information is clearly wrong

---

## Key Principles

1. **Stop re-deriving, start compiling** — RAG retrieves and forgets. Wiki accumulates.

2. **Curation over accumulation** — Not everything worth saving. Agent decides.

3. **Confidence decays** — Knowledge has lifecycle. Old facts become stale.

4. **Supersession, not deletion** — Old claims preserved, marked stale.

5. **Forgetting is healthy** — Junk drawer vs. living knowledge base.

6. **Schema is the product** — AGENTS.md evolves with domain understanding.

---

## Recent Updates

| Date | Change |
|------|--------|
| 2026-04-14 | Initial schema from unified research |

---

## Related

- [[Hermes Dojo SKILL]]
- [[Hermes Dojo Phases]]
