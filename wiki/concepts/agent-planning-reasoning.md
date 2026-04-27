---
confidence: medium
last_verified: 2026-04-16
type: concept
tags: [agent, planning, reasoning, llm-architecture]
related:
  - [[agentic-ai]]
  - [[agent-memory-architecture]]
  - [[multi-agent-systems]]
---

# Agent Planning and Reasoning

> This page is a stub. The content below is a starting point — please expand with real knowledge.

## Overview

Agent planning and reasoning enables LLMs to decompose complex goals into actionable steps. 2026 saw significant advances with architectures like MAP (Modular Agentic Planner).

## Key Architectures

### MAP — Modular Agentic Planner
Published in Nature (2026): Brain-inspired architecture where planning is performed via recurrent interaction between specialized modules.

**Key insight:** Inspired by prefrontal cortex organization — modular planning outperforms monolithic approaches.

### Continuous Memory Architecture (CMA)
arXiv paper 2601.09913v1 formalizes CMA as an architectural class for persistent memory in LLM agents.

### AMA-Bench
arXiv paper 2602.22769v1 evaluates long-horizon memory for LLMs in real agentic applications.

## Planning Patterns

### ReAct (Reasoning + Acting)
Combines reasoning traces with action execution for iterative problem solving.

### Chain-of-Thought
Enables step-by-step reasoning for complex problems.

### Tree of Thoughts
Explores multiple reasoning paths simultaneously.

## Related Concepts

- [[agentic-ai]]
- [[agent-memory-architecture]]
- [[multi-agent-systems]]
- [[reasoning-patterns]]
