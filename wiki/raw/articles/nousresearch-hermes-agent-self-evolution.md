---
title: "NousResearch/hermes-agent-self-evolution"
created: 2026-04-27
updated: 2026-04-27
type: article
tags: [agent, self-improvement, dspy, optimization]
sources: []
confidence: high
relationships: []
---

# NousResearch/hermes-agent-self-evolution

> Source: https://github.com/NousResearch/hermes-agent-self-evolution
> Published: 2026-03-09
> Stars: 2311 | Forks: 245

## Overview

Evolutionary self-improvement for Hermes Agent — optimize skills, prompts, and code using DSPy + GEPA.

**No GPU training required.** Everything operates via API calls — mutating text, evaluating results, and selecting the best variants. ~$2-10 per optimization run.

## Architecture

```
Read current skill/prompt/tool ──► Generate eval dataset
                                        │
                                        ▼
                                   GEPA Optimizer ◄── Execution traces
                                        │                    ▲
                                        ▼                    │
                                   Candidate variants ──► Evaluate
                                        │
                                   Constraint gates (tests, size limits, benchmarks)
                                        │
                                        ▼
                                   Best variant ──► PR against hermes-agent
```

## What It Optimizes

| Phase | Target | Engine | Status |
| --- | --- | --- | --- |
| **Phase 1** | Skill files (SKILL.md) | DSPy + GEPA | ✅ Implemented |
| **Phase 2** | Tool descriptions | DSPy + GEPA | 🔲 Planned |
| **Phase 3** | System prompt sections | DSPy + GEPA | 🔲 Planned |
| **Phase 4** | Tool implementation code | Darwinian Evolver | 🔲 Planned |
| **Phase 5** | Continuous improvement loop | Automated pipeline | 🔲 Planned |

## Quick Start

```bash
# Install
git clone https://github.com/NousResearch/hermes-agent-self-evolution.git
cd hermes-agent-self-evolution
pip install -e ".[dev]"

# Point at your hermes-agent repo
export HERMES_AGENT_REPO=~/.hermes/hermes-agent

# Evolve a skill (synthetic eval data)
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source synthetic

# Or use real session history
python -m evolution.skills.evolve_skill \
    --skill github-code-review \
    --iterations 10 \
    --eval-source sessiondb
```

## Guardrails

Every evolved variant must pass:
1. **Full test suite** — `pytest tests/ -q` must pass 100%
2. **Size limits** — Skills ≤15KB, tool descriptions ≤500 chars
3. **Caching compatibility** — No mid-conversation changes
4. **Semantic preservation** — Must not drift from original purpose
5. **PR review** — All changes go through human review

## Engines

| Engine | What It Does | License |
| --- | --- | --- |
| **DSPy + GEPA** | Reflective prompt evolution — reads execution traces, proposes targeted mutations | MIT |
| **Darwinian Evolver** | Code evolution with Git-based organisms | AGPL v3 (external CLI only) |

## Key People

- teknium1 (top contributor)
- tjp2021 (contributor)

## License

MIT — © 2026 Nous Research
