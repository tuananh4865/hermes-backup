---
title: "IRAF — Iterative Refinement Agentic Framework"
created: 2026-04-13
updated: 2026-04-18
type: concept
tags: [ai-agents, agentic-ai, frameworks, git-native, autonomous]
related:
  - [[multi-agent-systems]]
  - [[agentic-ai]]
  - [[coding-agents]]
  - [[self-improving-ai]]
confidence: high
sources:
  - https://medium.com/@otonielrojas/the-iterative-refinement-agentic-framework-iraf-a-git-native-architecture-for-autonomous-ee84aac9139e
---

# IRAF — Iterative Refinement Agentic Framework

## Overview

IRAF (Iterative Refinement Agentic Framework) is a **Git-native architecture** for autonomous AI agents that embeds a closed-loop feedback system directly into version control. Rather than treating Git as just a storage layer, IRAF makes Git the **coordination mechanism** for iterative agent improvement cycles.

The core insight: Agents can autonomously improve their own code outputs through repeated refine → commit → review → refine cycles, with Git history providing the feedback signal.

## Core Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Git Repository                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │ Commit N-2  │→│  Commit N-1 │→│  Commit N    │ │
│  │ (v1 output) │  │ (v2 refined)│  │ (v3 best)   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘ │
│         ↑                                    │     │
│         └──────────── feedback loop ←─────────┘     │
└─────────────────────────────────────────────────────┘
```

**The loop:**
1. **Agent generates** initial output (code, document, config)
2. **Commit to Git** — stores the generation with context
3. **Review step** — agent or human evaluates quality
4. **Refine based on feedback** — agent modifies and commits again
5. **Repeat** — Git history enables the agent to learn from past iterations

## How IRAF Works

### Git as Memory

Traditional agents lose context after a session ends. IRAF uses Git commits as persistent memory:

- Every agent action is a commit with meaningful message
- `git log` becomes the agent's memory of what it tried before
- `git diff` between commits shows exactly what changed
- The agent can `git blame` to understand why something was written

### The Refinement Cycle

```python
# IRAF-style agent loop (pseudocode)
while not satisfied(output_quality):
    # Generate candidate
    candidate = agent.generate(spec)
    
    # Commit with context
    commit_msg = f"IRA: {iteration} — {improvement_goal}"
    git.commit(candidate, message=commit_msg)
    
    # Self-evaluate
    issues = agent.review(candidate, criteria)
    
    if issues:
        # Refine based on review
        candidate = agent.refine(candidate, issues)
        iteration += 1
    else:
        break
```

### Autonomous Improvement

The key differentiator from standard agents: **IRAF agents don't just generate — they iterate until quality thresholds are met**.

This is different from:
- **Single-pass generation** (generate once, return)
- **Self-reflection** (reflect on output, then return revised version)
- **IRAF** (reflect → commit → re-reflect on committed artifact → repeat until quality)

## IRAF vs Other Agent Patterns

| Aspect | IRAF | Standard Agent | Self-Reflection Agent |
|--------|------|---------------|----------------------|
| Memory | Git commits | Context window | Context window |
| Iteration | Commits enable full history | Single session | Limited by context |
| Feedback | Git diff + review comments | Immediate | Immediate |
| Persistence | Permanent across sessions | Lost when session ends | Lost when session ends |
| Human review | Git PR/review flow | None | None |

## Real-World Applications

### Code Quality Improvement

An IRAF agent can work on a buggy function:
1. Generate initial fix → commit
2. Run tests → review results
3. If tests fail: refine fix → commit
4. Repeat until tests pass

The Git history shows the entire refinement journey — useful for understanding *why* the final solution works.

### Documentation Generation

Generate docs → commit → check for completeness against source code → refine missing sections → commit again. The documentation and code evolve together in lockstep.

### Configuration Management

IAC (Infrastructure as Code) benefits from IRAF: generate Terraform → commit → validate against cloud API → refine → commit. Each commit is a checkpoint you can roll back to.

## IRAF in the Broader Agent Landscape

IRAF is part of the **agentic AI** movement — AI that doesn't just respond to prompts but **takes actions, evaluates outcomes, and iterates**. It complements:

- **[[multi-agent-systems]]** — multiple IRAF agents could coordinate via Git-based handoffs
- **[[LangGraph]]** — supervisor patterns could orchestrate IRAF refinement cycles
- **[[CrewAI]]** — role-playing agents could use IRAF for their iterative tasks

## Key Insights from IRAF

1. **Git is the missing piece** for autonomous agents — it provides both memory and coordination
2. **Iteration over generation** — the best outputs come from refining, not from prompting the perfect first draft
3. **Transparency by default** — every commit is auditable, every change is traceable
4. **Human-in-the-loop via PRs** — Git's pull request flow enables human review at any cycle point

## Further Reading

- [IRAF on Medium](https://medium.com/@otonielrojas/the-iterative-refinement-agentic-framework-iraf-a-git-native-architecture-for-autonomous-ee84aac9139e) — Original framework description
- [[multi-agent-systems]] — How IRAF fits into broader agent coordination
- [[agentic-ai]] — The agentic AI movement IRAF is part of
- [[coding-agents]] — Claude Code, Cursor, and other coding agents that could benefit from IRAF

---

*Research note: IRAF represents a shift from "generate once" to "iterate to quality" — a fundamental change in how we think about agent output quality.*
