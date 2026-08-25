---
title: Memento-Skills Tool Creation
created: 2026-05-26
updated: 2026-05-26
type: concept
tags: [self-improving-agents, tool-creation, arxiv]
confidence: high
relationships: [self-improving-agents-may-2026, hermes-autoresearch]
---

# Memento-Skills: Let Agents Design Agents (arXiv:2603.18743)

## Overview
**Memento-Skills** (March 2026, UC Berkeley/Allen Institute) enables a frozen language model to continuously construct, edit, and refine its own executable skill library — WITHOUT retraining the core model.

## Key Mechanism

Unlike prior approaches relying on human-designed agents, Memento-Skills lets agents **design agents end-to-end** for new tasks:

1. **Skill Synthesis** — Agent writes executable skill code from natural language task description
2. **Skill Verification** — Agent tests skill in sandbox before adding to library
3. **Skill Selection** — Agent chooses which skills to compose for new tasks
4. **Skill Refinement** — Poor skills get iteratively improved based on failure traces

## Results

| Metric | Memento-Skills | Human-Designed | Improvement |
|--------|---------------|----------------|-------------|
| Task Success | 80% | 45% (baseline) | +78% |
| Tool Use Accuracy | 73% | 38% | +92% |
| Novel Task Generalization | 67% | 29% | +131% |

## Relevance to Hermes

Hermes skill system (`~/.hermes/skills/`) has **static markdown files** — requires human editing to improve. Memento-Skills enables agents to write/tune their own skills without retraining.

## Sources
- arXiv:2603.18743 (March 2026)
- VentureBeat (April 2026)
- YouTube: "Memento-Skills: How Agents Rewrite Their Own Skill Libraries" (May 3, 2026)
