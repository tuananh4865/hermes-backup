---
title: Hermes Dojo - Unified Implementation Plan
created: 2026-04-14
updated: 2026-04-14
type: project
tags: [hermes-dojo, agentic-workflow, self-improving-ai, implementation-plan]
description: Plan thống nhất xây dựng Hermes Dojo - hệ thống agentic tự hoàn thiện cho wiki management.
status: planning
phase: 0-skeleton
---

## Vision

**Hermes Dojo** = A self-evolving wiki agent that:
- **Learns** from every interaction and mistake
- **Remembers** across sessions with confidence scoring
- **Evolves** its own workflows and skills
- **Prevents** cascade failures through dependency tracking
- **Works proactively** without being told what to do

**Inspired by:** Hermes Agent, LLM Wiki v2 (agentmemory), Archon, Karpathy-Skills, Claude Code Agent Teams, humanlayer ACE

---

## Research Sources

| Source | Key Insights |
|--------|-------------|
| [[Agentic-Workflow-Deep-Research]] | 3-layer architecture, periodic nudges, skill self-improvement |
| [[Agentic-Codebase-Context-Management]] | Cascade prevention, dependency tracking, frequent compaction |
| [[Archon-and-Karpathy-Skills-Deep-Dive]] | Workflow engine, behavioral guidelines |
| [[LLM Wiki v2 (agentmemory gist)]] | Memory lifecycle, confidence scoring, knowledge graph, crystallization |

---

## Architecture: 6 Layers

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 0: CONTENT (Wiki Pages)                              │
│  └── Markdown files with wikilinks                          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 1: KNOWLEDGE GRAPH                                   │
│  └── Entities + Typed Relationships (SQLite)                │
├─────────────────────────────────────────────────────────────┤
│  LAYER 2: MEMORY LIFECYCLE                                  │
│  └── Working → Episodic → Semantic → Procedural            │
│  └── Confidence scoring + decay + supersession              │
├─────────────────────────────────────────────────────────────┤
│  LAYER 3: AUTOMATION (Event-Driven Hooks)                   │
│  └── On-ingest, On-session, On-schedule                     │
├─────────────────────────────────────────────────────────────┤
│  LAYER 4: QUALITY SYSTEM                                    │
│  └── Score everything + self-heal + contradiction resolution │
├─────────────────────────────────────────────────────────────┤
│  LAYER 5: BEHAVIOR (Karpathy Principles)                    │
│  └── Think Before Coding, Simplicity, Surgical, Goal-Driven │
├─────────────────────────────────────────────────────────────┤
│  LAYER 6: PROCESS ENGINE                                    │
│  └── Research → Plan → Implement + Dependency Tracking      │
└─────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
~/wiki/projects/hermes-dojo/
├── SKILL.md                           # Main entry - project overview
├── AGENTS.md                          # Schema - turns LLM into disciplined worker
├── README.md                          # Setup & usage guide
│
├── phases/
│   ├── phase-0-skeleton/              # (DONE - this document)
│   ├── phase-1-behavior/              # Karpathy principles
│   ├── phase-2-process/              # R→P→I workflow
│   ├── phase-3-dependency/           # Dependency tracking
│   ├── phase-4-memory-lifecycle/     # Confidence, decay, supersession
│   ├── phase-5-knowledge-graph/      # Entity extraction, graph
│   ├── phase-6-automation/           # Event-driven hooks
│   ├── phase-7-quality/              # Scoring, self-healing
│   └── phase-8-proactive/            # Scheduled reviews, discovery
│
├── scripts/
│   ├── dependency_tracker.py          # Map call graph
│   ├── entity_extractor.py            # Extract entities from sources
│   ├── knowledge_graph.py             # Graph storage & traversal
│   ├── confidence_scorer.py           # Score wiki content
│   ├── crystallization.py             # Distill completed work
│   ├── nudge_trigger.py               # Self-reflection triggers
│   ├── stale_detector.py              # Find stale content
│   └── wiki_hooks.py                  # Event-driven automation
│
├── memories/
│   ├── MEMORY.md                      # Global agent knowledge
│   ├── USER.md                         # User preferences
│   └── PROJECT_CONTEXT.md              # Current project state
│
├── wiki/
│   └── (spawned agents use this as workspace)
│
├── skills/
│   ├── INDEX.md                       # All skills catalog
│   ├── behavior/
│   │   ├── karpathy-principles/
│   │   ├── surgical-change-protocol/
│   │   └── goal-driven-execution/
│   ├── process/
│   │   ├── research-command/
│   │   ├── plan-command/
│   │   ├── implement-command/
│   │   └── cascade-prevention/
│   ├── memory/
│   │   ├── memory-manage/
│   │   ├── update-project-state/
│   │   └── mistake-logging/
│   ├── quality/
│   │   ├── wiki-quality-score/
│   │   ├── self-heal/
│   │   └── contradiction-resolution/
│   └── lifecycle/
│       ├── skill-from-experience/
│       ├── skill-self-improve/
│       └── crystallization/
│
└── tests/
    ├── test_dependency_tracker.py
    ├── test_entity_extractor.py
    ├── test_knowledge_graph.py
    ├── test_confidence_scorer.py
    └── test_workflows.py
```

---

## Phase 0: Skeleton (THIS PHASE)

### Goals
- [x] Create project directory structure
- [x] Create SKILL.md with overview
- [x] Create AGENTS.md schema
- [x] Create README.md
- [ ] Create placeholder for each phase
- [ ] Create scripts/ with stub implementations
- [ ] Create skills/INDEX.md
- [ ] Initialize git

### Deliverables

#### SKILL.md
```markdown
# Hermes Dojo

Self-evolving wiki agent system. Learns from every interaction.

## What It Does
- Persistent memory across sessions
- Dependency tracking prevents cascade failures
- Confidence scoring keeps knowledge fresh
- Auto-crystallization of completed work

## Architecture
6 layers: Content → Graph → Lifecycle → Automation → Quality → Behavior → Process

## Quick Start
See README.md
```

#### AGENTS.md Schema
```markdown
# Hermes Dojo Schema

## Entities
- Person: name, role, owns, opinions
- Project: name, status, depends_on
- Concept: name, definition, related_to
- File: path, type, contains

## Relationships
- uses, depends_on, caused, fixed, supersedes, owns, related_to

## Ingest Rules
1. Extract entities + relationships
2. Score confidence
3. Check for contradictions
4. Update graph

## Quality Standards
- Score ≥ 7.0 to publish
- Auto-fix what can be fixed
- Flag contradictions for review

## Consolidation Schedule
- Working → Episodic: after each session
- Episodic → Semantic: after 3+ sessions
- Semantic → Procedural: after pattern seen 3+ times
```

---

## Phase 1: Behavior (Karpathy Principles)

### Goals
- [x] karpathy-principles skill
- [x] surgical-change-protocol skill
- [x] goal-driven-execution skill

### Skills to Create

```
skills/behavior/karpathy-principles/SKILL.md
skills/behavior/surgical-change-protocol/SKILL.md
skills/behavior/goal-driven-execution/SKILL.md
```

### Key Files

#### karpathy-principles/SKILL.md
```markdown
---
name: karpathy-principles
description: Four principles for professional AI behavior
version: 1.0.0
category: behavior
---

# Karpathy's 4 Principles

## 1. Think Before Coding
- State assumptions explicitly
- Present multiple interpretations when ambiguous
- Push back when simpler approach exists
- Stop when confused, ask

## 2. Simplicity First
- Minimum code that solves problem
- No speculative features
- No abstractions for single-use code
- Rewrite if 200 lines could be 50

## 3. Surgical Changes
- Touch only what must change
- Don't improve adjacent code
- Match existing style
- Clean up only own orphans

## 4. Goal-Driven Execution
- Define success criteria before starting
- Write test first, then make pass
- Loop until verification passes
- State brief plan: "1. Step → verify: check"
```

---

## Phase 2: Process Engine (R→P→I)

### Goals
- [ ] /research command
- [ ] /plan command
- [ ] /implement command
- [ ] Research artifact template
- [ ] Plan artifact template

### Workflow

```
RESEARCH → PLAN → IMPLEMENT
    ↓         ↓         ↓
research.md  plan.md   code changes
```

### Key Files

```
skills/process/research-command/SKILL.md
skills/process/plan-command/SKILL.md
skills/process/implement-command/SKILL.md
skills/process/cascade-prevention/SKILL.md
```

---

## Phase 3: Dependency Tracking

### Goals
- [ ] dependency_tracker.py script
- [ ] pre-edit-dependency-check skill
- [ ] cascade-prevention-checklist
- [ ] PROJECT_STATE.md template

### Key Files

```
scripts/dependency_tracker.py
skills/process/pre-edit-dependency-check/SKILL.md
memories/PROJECT_CONTEXT.md.template
```

### dependency_tracker.py Features

```python
class DependencyTracker:
    def scan(self, root_path)          # Scan codebase
    def find_callers(self, func)      # Find all callers
    def find_imports(self, module)     # Find all imports
    def generate_graph_md(self)       # Output CODEBASE_GRAPH.md
    def run_pre_edit_check(self, file) # Pre-edit validation
```

---

## Phase 4: Memory Lifecycle

### Goals
- [ ] 4-tier memory system (Working→Episodic→Semantic→Procedural)
- [ ] Confidence scoring system
- [ ] Supersession mechanism
- [ ] Retention/decay curve

### Key Files

```
scripts/confidence_scorer.py
memories/MEMORY.md
memories/USER.md
memories/PROJECT_CONTEXT.md
skills/memory/memory-manage/SKILL.md
skills/memory/update-project-state/SKILL.md
skills/memory/mistake-logging/SKILL.md
```

### Confidence Formula

```
confidence = (
  source_weight * min(source_count, 5) / 5 +
  recency_weight * decay(days_since_confirm) +
  reinforcement_weight * min(reinforcement, 10) / 10 -
  contradiction_weight * contradictions
)

Decay rates:
- Architecture: half-life 180 days
- Project facts: half-life 30 days
- Transient bugs: half-life 7 days
```

---

## Phase 5: Knowledge Graph

### Goals
- [ ] Entity types definition
- [ ] entity_extractor.py
- [ ] knowledge_graph.py (SQLite storage)
- [ ] Graph-aware query skill

### Key Files

```
scripts/entity_extractor.py
scripts/knowledge_graph.py
skills/lifecycle/entity-extraction/SKILL.md
```

### Entity Types

```yaml
Person:
  attributes: name, role
  relationships: owns, has_opinions

Project:
  attributes: name, status
  relationships: depends_on, owned_by

Library:
  attributes: name, version
  relationships: uses, alternatives

Concept:
  attributes: name, definition
  relationships: related_to

File:
  attributes: path, type
  relationships: contains, modified_by

Decision:
  attributes: title, date, rationale
  relationships: superseded_by
```

### Relationship Types

```yaml
uses
depends_on
contradicts
caused
fixed
supersedes
owns
related_to
```

---

## Phase 6: Automation (Event-Driven Hooks)

### Goals
- [ ] On-ingest hook (auto-extract entities)
- [ ] On-session-start hook (load context)
- [ ] On-session-end hook (compress session)
- [ ] On-schedule hook (periodic maintenance)

### Key Files

```
scripts/wiki_hooks.py
scripts/nudge_trigger.py
scripts/stale_detector.py
skills/automation/on-ingest/SKILL.md
skills/automation/on-session-start/SKILL.md
skills/automation/on-session-end/SKILL.md
skills/automation/on-schedule/SKILL.md
skills/lifecycle/periodic-nudge/SKILL.md
```

### Hook Events

| Event | Action |
|-------|--------|
| New source | Ingest → extract → update graph → update index |
| Session start | Load relevant context from wiki |
| Session end | Compress → observations → update memory |
| Query | Check if answer worth filing back |
| Memory write | Check contradictions → trigger supersession |
| Schedule | Periodic lint, consolidation, decay |

---

## Phase 7: Quality System

### Goals
- [ ] Wiki quality scoring
- [ ] Self-healing (auto-fix lint issues)
- [ ] Contradiction resolution

### Key Files

```
skills/quality/wiki-quality-score/SKILL.md
skills/quality/self-heal/SKILL.md
skills/quality/contradiction-resolution/SKILL.md
```

### Quality Thresholds

```
Publish thresholds:
- Concept pages: score ≥ 7.0
- Tutorials: score ≥ 7.5
- Research pages: score ≥ 8.0
- Deep dives: score ≥ 8.5

Auto-fix thresholds:
- Broken links: auto-fix
- Formatting: auto-fix
- Stub content: flag for expansion
- Contradictions: flag for resolution
```

---

## Phase 8: Proactive Mode

### Goals
- [ ] Daily review skill
- [ ] Weekly deep review
- [ ] Stale content detector
- [ ] Pattern discovery
- [ ] Crystallization

### Key Files

```
skills/proactive/daily-review/SKILL.md
skills/proactive/weekly-review/SKILL.md
skills/proactive/stale-detection/SKILL.md
skills/proactive/pattern-discovery/SKILL.md
skills/lifecycle/crystallization/SKILL.md
scripts/crystallization.py
```

### Crystallization Template

```markdown
# Digest: {title}
Date: {date}
Type: {research | debug | analysis | exploration}

## Question
{What was the question?}

## Findings
{What did we find?}

## Entities Involved
{List from graph}

## Lessons Learned
{Lessons extracted}

## Related
{Link to sources, related digests}
```

---

## Skills Index

| Category | Skill | Purpose | Priority |
|----------|-------|---------|----------|
| behavior | karpathy-principles | Professional judgment | 1 |
| behavior | surgical-change-protocol | Prevent cascade | 1 |
| behavior | goal-driven-execution | Verify each step | 1 |
| process | research-command | Understand before acting | 2 |
| process | plan-command | Define exact path | 2 |
| process | implement-command | Execute with verification | 2 |
| process | cascade-prevention | Dependency tracking | 2 |
| memory | memory-manage | 4-tier memory | 2 |
| memory | update-project-state | Track progress | 3 |
| memory | mistake-logging | Learn from errors | 3 |
| lifecycle | skill-from-experience | Auto-skill creation | 4 |
| lifecycle | skill-self-improve | Patch not rewrite | 4 |
| lifecycle | periodic-nudge | Self-reflection | 4 |
| lifecycle | crystallization | Distill completed work | 5 |
| quality | wiki-quality-score | Score content | 3 |
| quality | self-heal | Auto-fix issues | 3 |
| quality | contradiction-resolution | Resolve conflicts | 4 |
| automation | on-ingest | Auto-process sources | 4 |
| automation | on-session-start | Load context | 3 |
| automation | on-session-end | Compress session | 4 |
| automation | on-schedule | Periodic maintenance | 5 |
| proactive | daily-review | Daily check | 5 |
| proactive | weekly-review | Weekly deep dive | 5 |
| proactive | stale-detection | Find stale content | 5 |
| proactive | pattern-discovery | Find patterns | 5 |

---

## Scripts Index

| Script | Purpose | Phase |
|--------|---------|-------|
| dependency_tracker.py | Map call graph | 3 |
| entity_extractor.py | Extract entities | 5 |
| knowledge_graph.py | Graph storage/traversal | 5 |
| confidence_scorer.py | Score content | 4 |
| crystallization.py | Distill work | 8 |
| nudge_trigger.py | Self-reflection | 6 |
| stale_detector.py | Find stale | 8 |
| wiki_hooks.py | Event automation | 6 |

---

## Implementation Order

```
Phase 0: Skeleton (NOW)
    └── Create directory structure, templates

Phase 1: Behavior (Week 1)
    └── Karpathy principles + surgical + goal-driven

Phase 2: Process (Week 1-2)
    └── Research → Plan → Implement workflow

Phase 3: Dependency (Week 2)
    └── dependency_tracker.py + cascade prevention

Phase 4: Memory Lifecycle (Week 2-3)
    └── Confidence scoring + decay + supersession

Phase 5: Knowledge Graph (Week 3)
    └── Entity extraction + graph storage

Phase 6: Automation (Week 3-4)
    └── Event-driven hooks

Phase 7: Quality (Week 4)
    └── Scoring + self-healing

Phase 8: Proactive (Week 4-5)
    └── Reviews + crystallization
```

---

## Success Metrics

### Week 1
- [ ] Karpathy principles loaded
- [ ] Research → Plan workflow working
- [ ] First task completed with cascade prevention

### Week 2
- [ ] Dependency tracker operational
- [ ] No cascade failures in test scenarios
- [ ] PROJECT_STATE.md tracking progress

### Week 3
- [ ] Confidence scoring active
- [ ] First supersession triggered
- [ ] Memory tiers functioning

### Week 4
- [ ] Knowledge graph populated
- [ ] Event hooks firing
- [ ] Quality scores on all pages

### Week 5+
- [ ] First skill auto-created
- [ ] First crystallization completed
- [ ] Daily/weekly reviews running
- [ ] Hermes proactively identifies work

---

## Related Documents

- [[Agentic-Workflow-Deep-Research]]
- [[Agentic-Codebase-Context-Management]]
- [[Archon-and-Karpathy-Skills-Deep-Dive]]
- [[LLM Wiki v2 Insights]]

---

## Testing Findings (2026-04-14)

### Scripts Need Real-Project Testing

Scripts verified to exist ≠ scripts work. During E2E testing:

| Script | Bug Found | Fix |
|--------|-----------|-----|
| `knowledge_graph.py` | `db_path` string not converted to `Path` → `AttributeError` | Add `Path(db_path)` conversion |
| `dependency_tracker.py` | `rglob` on file path returns nothing | Handle file vs directory: scan entire codebase first |
| `dependency_tracker.py` | `--check` scanned only that file | Always scan all first, then analyze specific file |

### Key Lesson

**QA-first waterfall for PHASES worked (8/8 passed, 0 redo). But SCRIPTS needed real testing to catch implementation bugs.**

### Testing Workflow Applied

```
1. dependency_tracker.py → Found 13 functions, `main` has 6 callers ✅
2. entity_extractor.py → Extracted 9 entities from README ✅
3. knowledge_graph.py → Added 3 entities, 2 relationships, query works ✅
4. R→P→I workflow → Expanded promql.md (31 words → 4988 bytes) ✅
5. cascade prevention → Pre-edit check works for Python ✅
6. update-project-state → Template verified ✅
```

### Pattern: Script Testing Checklist

Before marking script "working":
- [ ] Test on a REAL project (not just --help)
- [ ] Test with actual files, not just existence
- [ ] Test edge cases: file vs directory, missing args, wrong types
- [ ] Test INTEGRATION: does output feed into next tool correctly?
