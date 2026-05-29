# ACE: Agentic Context Engineering (arXiv:2510.04618)

**Researched:** 2026-05-30 (autoresearch)
**Source:** arXiv:2510.04618

## Overview

ACE treats contexts as **evolving playbooks** that accumulate, refine, and organize agent experience over time. Unlike static context windows, ACE frames context management as a dynamic, self-improving system where past interactions shape future behavior.

## Core Insight

```
Context = not just "what was said"
       = "evolving playbook" that gets written, revised, and re-read
```

## Key Principles

1. **Context accumulation** — context grows selectively, not infinitely
2. **Context refinement** — old context is re-summarized when superseded
3. **Context organization** — structured retrieval, not just semantic search

## Connection to Other Patterns

| Pattern | Relationship |
|---------|-------------|
| Trajectory Memory (arXiv:2603.10600v1) | Both address how agents learn from experience — ACE is the architecture, Trajectory Memory is the implementation |
| ERL (Experience-Reinforcement-Learning) | ACE can serve as the "experience" layer for ERL |
| MOSS (source-level self-rewriting) | ACE operates at context level; MOSS at source code level — complementary |

## Hermes Applicability

**HIGH** — ACE directly applies to:
- `Context Management` capability (16 Hermes capabilities)
- Session continuity gap (context loss → context accumulation)
- Memory optimization (WikiMemoryProvider could use ACE pattern)

## Sources

- arXiv:2510.04618 (October 2025)
- Yohei Nakajima: "Better Ways to Build Self-Improving AI Agents" (Dec 2025)
