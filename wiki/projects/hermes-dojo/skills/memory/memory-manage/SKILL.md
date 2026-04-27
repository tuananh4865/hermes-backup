---
name: memory-manage
description: 4-tier memory system operations - Working, Episodic, Semantic, Procedural - manage knowledge lifecycle
version: 1.0.0
category: memory
platforms: [macos, linux]
created: 2026-04-14
tags: [memory, knowledge-lifecycle, tier-management, curation]
requires_toolsets: [terminal]
---

# Memory Manage

**Memory is curated, not accumulated. Know which tier to use.**

This skill manages the 4-tier memory system that keeps knowledge fresh and actionable.

---

## The 4 Tiers

### Tier 1: Working Memory
- **What:** Recent observations, unprocessed
- **Where:** Current session context
- **Lifetime:** End of session → auto-discard or compress to Episodic
- **Rule:** Don't let this grow unbounded

### Tier 2: Episodic Memory
- **What:** Session summaries, compressed
- **Where:** `memories/` directory
- **Lifetime:** Until pattern confirmed 3+ times → promote to Semantic
- **Rule:** Compress sessions to key learnings

### Tier 3: Semantic Memory
- **What:** Cross-session facts, consolidated
- **Where:** Knowledge graph + wiki pages
- **Lifetime:** Decays over time unless reinforced
- **Rule:** Confidence scoring determines priority

### Tier 4: Procedural Memory
- **What:** Workflows and patterns as skills
- **Where:** `~/.hermes/skills/`
- **Lifetime:** Permanent until superseded
- **Rule:** Extract patterns, not just facts

---

## Memory Operations

### Operation 1: Compress Session to Episodic

**When:** End of session

```
1. Identify key learnings from this session:
   - What worked?
   - What didn't?
   - What decisions were made?

2. Write to session summary:
   ```
   # Session Summary: {YYYY-MM-DD}
   
   ## Task
   {What we worked on}
   
   ## Key Learnings
   - {Learning 1}
   - {Learning 2}
   
   ## Decisions
   - {Decision} → {Rationale}
   
   ## Next Steps
   - {Next action}
   ```

3. Store in memories/ with date stamp
```

### Operation 2: Promote to Semantic

**When:** Same fact confirmed in 3+ sessions

```
1. Find episodic entries with same fact
2. Consolidate into single semantic fact:
   - Remove redundant details
   - Add confidence based on reinforcement
   - Link to source episodes
   
3. Write to wiki or knowledge graph
4. Mark episodic entries as "promoted"
```

### Operation 3: Extract to Procedural

**When:** Same workflow pattern seen 3+ times

```
1. Identify repeated workflow:
   - Check: Is this a 5+ step process?
   - Check: Has it been done 3+ times?
   
2. Extract to skill:
   - Create skills/{category}/{name}/SKILL.md
   - Include: steps, triggers, examples
   
3. Update relevant episodic entries
```

### Operation 4: Decay Check

**When:** Periodic (daily/weekly)

```
For each semantic memory:
1. Calculate retention score
2. If retention < 0.3:
   - Deprioritize (still keep)
   - Mark as "archived" in index
   
3. If reinforced (accessed/confirmed):
   - Reset decay timer
   - Increment confidence
```

### Operation 5: Curate (Don't Accumulate)

**Rule: Not everything worth saving. Agent decides.**

```
Ask before saving:
1. Is this a one-time occurrence or pattern?
2. Will this be useful in 6 months?
3. Is this already documented elsewhere?

If pattern: Save to Episodic
If reusable workflow: Extract to skill
If decision with rationale: Add to Semantic
If transient: Don't save
```

---

## Memory File Locations

```
~/.hermes/
├── memories/
│   ├── MEMORY.md              # Global agent memory (Tier 1-2)
│   ├── USER.md                # User preferences (Tier 1)
│   ├── PROJECT_CONTEXT.md     # Current project (Tier 1)
│   ├── sessions/
│   │   └── {date}_{summary}.md  # Episodic memories
│   └── mistakes/
│       └── {date}_{issue}.md    # Mistake logs
├── skills/
│   └── {category}/
│       └── {skill}/SKILL.md   # Procedural memories (Tier 4)
└── knowledge_graph.db         # Semantic memories (Tier 3)
```

---

## Quality Thresholds

### What to Save

```
YES:
- Pattern that will repeat
- Decision with rationale
- Mistake with lesson
- User preference/constraint
- Project state for continuation

NO:
- One-time observations
- Things easily re-discovered
- Raw data dumps
- Temporary state
```

### When to Delete

```
Delete when:
- Fact proven false
- Pattern no longer relevant
- Superseded by better knowledge
- User requests deletion

Never delete:
- Mistake logs (mark as resolved, keep for reference)
- Decision history (mark as superseded, keep for audit)
```

---

## Integration

- Use [[update-project-state]] — After each session
- Use [[mistake-logging]] — Log errors separately
- Use [[skill-from-experience]] — Extract to procedural
- Use [[crystallization]] — Distill completed work

---

## Quick Reference

| Operation | When | Where |
|-----------|------|-------|
| Compress session | End of session | memories/sessions/ |
| Promote to semantic | 3+ confirmations | wiki or graph |
| Extract to skill | 3+ workflow repetitions | skills/ |
| Decay check | Daily/weekly | graph, update confidence |
| Curate | Before saving | N/A |

---

## Related

- [[update-project-state]] — Session state tracking
- [[mistake-logging]] — Error learning
- [[skill-from-experience]] — Procedural extraction
- [[crystallization]] — Work distillation
