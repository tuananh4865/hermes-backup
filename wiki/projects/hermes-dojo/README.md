---
title: "Hermes Dojo"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Hermes Dojo

**Self-evolving wiki agent system.** Learns from every interaction, remembers across sessions with confidence scoring, evolves its own workflows and skills.

---

## What It Does

- **Persistent Memory** — 4-tier memory system with confidence scoring and decay
- **Dependency Tracking** — Prevents cascade failures when editing code
- **Knowledge Graph** — Typed entities and relationships layered on wiki pages
- **Event-Driven Automation** — Hooks for auto-ingest, auto-lint, auto-crystallize
- **Self-Healing** — Wiki tends toward health on its own
- **Proactive** — Scheduled reviews, stale detection, pattern discovery

---

## Architecture

```
LAYER 0: Content (Wiki Pages)
LAYER 1: Knowledge Graph (Entities + Relationships)
LAYER 2: Memory Lifecycle (Working → Episodic → Semantic → Procedural)
LAYER 3: Automation (Event-Driven Hooks)
LAYER 4: Quality System (Scoring + Self-Healing)
LAYER 5: Behavior (Karpathy Principles)
LAYER 6: Process Engine (Research → Plan → Implement)
```

---

## Quick Start

### Prerequisites
- Hermes Agent running
- Wiki at `~/wiki/`

### Setup

```bash
# Clone wiki if not exists
git clone https://github.com/tuananh4865/my-llm-wiki.git ~/wiki

# Navigate to project
cd ~/wiki/projects/hermes-dojo

# Skills are in skills/ directory
# Scripts are in scripts/ directory
# Memories are in memories/ directory
```

---

## Project Structure

```
hermes-dojo/
├── SKILL.md              # Main entry - project overview
├── AGENTS.md             # Schema - turns LLM into disciplined worker
├── README.md             # This file
│
├── phases/               # Implementation phases
│   ├── phase-0-skeleton/
│   ├── phase-1-behavior/
│   ├── phase-2-process/
│   └── ...
│
├── scripts/              # Python tools
│   ├── dependency_tracker.py
│   ├── entity_extractor.py
│   ├── knowledge_graph.py
│   └── ...
│
├── memories/             # Persistent memory files
│   ├── MEMORY.md
│   ├── USER.md
│   └── PROJECT_CONTEXT.md
│
├── skills/               # Agent skills (by category)
│   ├── INDEX.md
│   ├── behavior/
│   ├── process/
│   ├── memory/
│   ├── lifecycle/
│   ├── quality/
│   ├── automation/
│   └── proactive/
│
└── tests/                # Test suite
```

---

## Skills by Category

### Behavior
| Skill | Purpose |
|-------|---------|
| karpathy-principles | Four principles for professional AI behavior |
| surgical-change-protocol | Prevent cascade failures |
| goal-driven-execution | Transform to verifiable goals |

### Process
| Skill | Purpose |
|-------|---------|
| research-command | Understand before acting |
| plan-command | Define exact path |
| implement-command | Execute with verification |
| cascade-prevention | Dependency tracking checklist |

### Memory
| Skill | Purpose |
|-------|---------|
| memory-manage | 4-tier memory operations |
| update-project-state | Track progress across sessions |
| mistake-logging | Learn from errors |

### Lifecycle
| Skill | Purpose |
|-------|---------|
| skill-from-experience | Auto-create skills from patterns |
| skill-self-improve | Patch-only skill updates |
| periodic-nudge | Self-reflection triggers |
| crystallization | Distill completed work |

### Quality
| Skill | Purpose |
|-------|---------|
| wiki-quality-score | Score wiki content |
| self-heal | Auto-fix lint issues |
| contradiction-resolution | Resolve conflicting claims |

### Automation
| Skill | Purpose |
|-------|---------|
| on-ingest | Auto-process new sources |
| on-session-start | Load relevant context |
| on-session-end | Compress session |
| on-schedule | Periodic maintenance |

### Proactive
| Skill | Purpose |
|-------|---------|
| daily-review | Daily self-check |
| weekly-review | Weekly deep dive |
| stale-detection | Find outdated content |
| pattern-discovery | Find useful patterns |

---

## Scripts

| Script | Purpose |
|--------|---------|
| dependency_tracker.py | Map call graph for cascade prevention |
| entity_extractor.py | Extract structured entities from sources |
| knowledge_graph.py | Graph storage and traversal |
| confidence_scorer.py | Score wiki content confidence |
| crystallization.py | Distill completed work into digests |
| nudge_trigger.py | Self-reflection trigger system |
| stale_detector.py | Find content needing updates |
| wiki_hooks.py | Event-driven automation engine |

---

## Memory Tiers

```
WORKING MEMORY          → Recent observations (auto-clear after session)
       ↓
EPISODIC MEMORY         → Session summaries (after each session)
       ↓
SEMANTIC MEMORY         → Cross-session facts (after 3+ confirmations)
       ↓
PROCEDURAL MEMORY       → Workflows as skills (after 3+ patterns)
```

---

## Confidence Scoring

Every fact has a confidence score (0-1) based on:

| Factor | Weight | Description |
|--------|--------|-------------|
| source_count | 0.25 | Number of independent sources |
| recency | 0.25 | How recently confirmed |
| reinforcement | 0.20 | Times accessed/confirmed |
| contradiction | 0.30 | Number of conflicting claims |

Decay rates:
- Architecture decisions: 180 days half-life
- Project facts: 30 days half-life
- Transient bugs: 7 days half-life

---

## Event Hooks

| Event | Auto Action |
|-------|-------------|
| New source | Ingest → extract → update graph |
| Session start | Load relevant context |
| Session end | Compress → observations |
| Schedule | Lint → consolidate → decay |
| Query | Check if worth filing back |

---

## Key Principles

1. **Stop re-deriving, start compiling** — RAG retrieves. Wiki accumulates.
2. **Curation over accumulation** — Not everything worth saving. Agent decides.
3. **Confidence decays** — Knowledge has lifecycle. Old facts become stale.
4. **Supersession, not deletion** — Old claims preserved, marked stale.
5. **Forgetting is healthy** — Living knowledge base vs. junk drawer.
6. **Schema is the product** — AGENTS.md evolves with domain understanding.

---

## Implementation Phases

```
Phase 0: Skeleton      → Directory structure, templates (DONE)
Phase 1: Behavior      → Karpathy principles
Phase 2: Process       → Research → Plan → Implement workflow
Phase 3: Dependency    → Dependency tracking + cascade prevention
Phase 4: Memory        → Confidence scoring + decay + supersession
Phase 5: Graph         → Entity extraction + knowledge graph
Phase 6: Automation   → Event-driven hooks
Phase 7: Quality       → Scoring + self-healing
Phase 8: Proactive     → Reviews + crystallization
```

---

## Success Metrics

- [ ] Karpathy principles loaded and followed
- [ ] Research → Plan → Implement workflow natural
- [ ] No cascade failures in test scenarios
- [ ] Confidence scoring active on all pages
- [ ] First skill auto-created from experience
- [ ] First crystallization completed
- [ ] Hermes proactively identifies work

---

## Related Documents

- [[Agentic-Workflow-Deep-Research]] — Research foundation
- [[Agentic-Codebase-Context-Management]] — Cascade prevention
- [[Archon-and-Karpathy-Skills-Deep-Dive]] — Workflow engine
- [[LLM Wiki v2 Insights]] — Memory lifecycle patterns
