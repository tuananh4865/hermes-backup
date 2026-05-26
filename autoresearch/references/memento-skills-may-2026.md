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

## Architecture

```
Frozen LLM + Skill Library (editable)
         ↓
Task arrives → Select relevant skills → Compose into agent
         ↓
Execute → Failure? → Refine skill → Update library
         ↓
Success? → Add to Memento (memory of successful skill patterns)
```

**Key insight:** The frozen LLM doesn't change — but its *skill library* grows and improves over time, giving it effectively "learned" capabilities without any gradient updates.

## Results

| Metric | Memento-Skills | Human-Designed | Improvement |
|--------|---------------|----------------|-------------|
| Task Success | 80% | 45% (baseline) | +78% |
| Tool Use Accuracy | 73% | 38% | +92% |
| Novel Task Generalization | 67% | 29% | +131% |

## Relevance to Hermes

Hermes already has a skill system (`~/.hermes/skills/`) — but skills are **static markdown files** that require human editing to improve.

**Memento-Skills pattern could enable:**
- Hermes writing/iterating its own `SKILL.md` files based on failure traces
- Self-generated skill improvements from session failures (Self-Correction capability)
- Automated skill verification before deployment

## Implementation Approaches

### Approach 1: Skill Self-Write (High Complexity)
Let Hermes write executable Python skills (not just markdown) that it can test and refine.

### Approach 2: Skill Composition (Medium Complexity)
Hermes selects and chains existing skills dynamically based on task type, writing a "skill invocation plan" rather than modifying skills directly.

### Approach 3: Skill Evaluation Loop (Low Complexity — Recommended)
Hermes evaluates skill effectiveness after each session and flags low-performing skills for human review, prioritizing improvements automatically.

## Sources
- arXiv:2603.18743 (March 2026)
- VentureBeat article (April 2026)
- YouTube: "Memento-Skills: How Agents Rewrite Their Own Skill Libraries" (May 3, 2026)
