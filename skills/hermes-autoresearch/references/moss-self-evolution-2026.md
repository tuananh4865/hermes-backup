# MOSS: Source-Level Self-Rewriting — May 2026

**arXiv:2605.22794** | Published: May 22, 2026

## What It Does

Enables autonomous agent systems to self-evolve by rewriting their own **source code** — not just text-mutable artifacts (skill files, prompts, memory).

## Why It Matters

All prior self-evolving agents (DGM-H, SICA) are limited to modifying text-mutable elements. MOSS pushes evolution to the source level:

| Approach | What it modifies | Limitation |
|---------|-----------------|------------|
| DGM-H | Meta-level procedures | Domain-specific initially |
| SICA | Scaffolding code | Text-level only |
| **MOSS** | **Source code directly** | **Most general, deterministic** |

## Key Innovation

- **Source-level rewriting = deterministic adaptation** — no randomness from LLM generation
- More general than text-mutable approaches
- Natural checkpoint/rollback via git

## Hermes Applicability: HIGH

Where MOSS could apply in Hermes:
1. `gateway/hooks.py` — failure detection hooks could self-patch
2. `plugins/memory/wiki_memory_provider.py` — evolve its own retrieval strategy
3. Skill loading pipeline — optimize routing

**Implementation path:** failure detected → MOSS analyzes root cause → generates source patch → validates in sandbox → git checkpoint → applies → tests

## Sources
- https://arxiv.org/abs/2605.22794
- https://arxiv.org/html/2605.22794v1
- https://news.ycombinator.com/item?id=48233155
