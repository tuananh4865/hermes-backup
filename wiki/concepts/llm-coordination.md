---
title: "LLM Coordination — Multi-Agent Communication Protocols"
created: 2026-04-13
updated: 2026-04-18
type: concept
tags: [ai-agents, multi-agent-systems, llm, coordination, communication, protocols]
related:
  - [[multi-agent-systems]]
  - [[multi-agentbench]]
  - [[agentic-ai]]
  - [[langgraph]]
  - [[crewai]]
confidence: high
sources:
  - https://arxiv.org/abs/2310.03903
---

# LLM Coordination — Multi-Agent Communication Protocols

## Overview

LLM Coordination refers to the protocols, patterns, and challenges involved in getting **multiple Large Language Model agents to communicate, collaborate, and align on shared tasks**. It's the engineering discipline that makes [[multi-agent-systems]] actually work in practice.

**Foundational paper:** [LLM-Coordination: Evaluating and Analyzing Multi-agent Coordination Abilities in Large Language Models](https://arxiv.org/abs/2310.03903) (arXiv:2310.03903)

**Authors:** Saaket Agashe, Yue Fan, Anthony Rey et al.

This research established that coordination is a **distinct skill** from individual LLM capability — you can't just combine capable LLMs and expect good teamwork.

## The Coordination Problem

When multiple LLM agents work on a shared task, several failure modes emerge:

### 1. Goal Misalignment

Agent A optimizes for metric X, Agent B optimizes for metric Y. Neither tells the user that X and Y conflict.

**Example:** Code generation agent wants the most elegant solution. Testing agent wants the most thorough tests. They fight over the same function.

### 2. Redundant Work

Two agents independently research the same thing, wasting computation and producing conflicting information.

**Example:** Research agent and competitor analysis agent both Google the same company, return different facts.

### 3. Communication Overhead

Agents spend more time describing what they did than doing useful work.

**Example:** Agent A describes its entire reasoning chain. Agent B has to parse this to understand what it needs. Time × 2 agents.

### 4. Authority Conflicts

When agents disagree, there's no mechanism to resolve it except human intervention.

**Example:** Agent A says use approach X. Agent B says use approach Y. Neither defers to the other.

## Coordination Patterns

Based on [[multi-agentbench]] findings, these patterns work:

### Pattern 1: Supervisor/Hierarchy

```
User Request
     ↓
┌──────────────┐
│  Supervisor  │ ← Has full context, makes final decisions
└──────┬───────┘
       ↓
  ┌────┴────┐
  ↓         ↓
┌──────┐ ┌──────┐
│Agent │ │Agent │ ← Specialized, stateless
│   A  │ │   B  │
└──┬───┘ └──┬───┘
   ↓         ↓
   └────┬────┘
        ↓
   Supervisor synthesizes
```

**Best for:** Task decomposition where subtasks are independent.

**[[LangGraph]] implements this via supervisor edges** — the supervisor node decides which agent runs next.

### Pattern 2: Round-Robin Reporting

Agents take turns contributing to a shared output. Each agent builds on the previous one's work.

```
Agent A: writes outline
Agent B: expands section 1
Agent C: reviews and revises
Agent A: final polish
```

**Best for:** Sequential tasks where each step depends on the previous.

### Pattern 3: Debate/Synthesis

Agents take opposing positions, then a synthesis agent combines the best of each.

```
┌──────────┐
│ Agent A  │ → "Use approach X"
└────┬─────┘
     ↓ debate
┌──────────┐
│ Agent B  │ → "Use approach Y"  
└────┬─────┘
     ↓ synthesis
┌──────────┐
│  Synth   │ → "Use X for A, Y for B, because..."
└──────────┘
```

**Best for:** Complex decisions with legitimate tradeoffs.

## Communication Protocols

### Structured Output (Recommended)

Agents communicate via **typed schemas**, not free-form text:

```python
# Agent A sends:
{
    "type": "task_complete",
    "task_id": "research_competitor",
    "findings": [...],
    "confidence": 0.85,
    "requires_review": True
}

# Agent B receives:
# Can immediately parse, no ambiguity
```

**Benefits:**
- Unambiguous interpretation
- Validates fields exist before processing
- Enables type checking at boundaries

### Shared Context Protocol

Agents share a **shared memory store** rather than passing messages:

```
┌─────────────────────────────────┐
│      Shared Context (Redis)     │
│  - Current task state           │
│  - Agent A's findings          │
│  - Agent B's findings          │
│  - Pending actions             │
└─────────────────────────────────┘
      ↑ read/write
┌─────────┐  ┌─────────┐  ┌─────────┐
│ Agent A │  │ Agent B │  │ Agent C │
└─────────┘  └─────────┘  └─────────┘
```

**Benefits:**
- Agents don't need direct communication
- Natural audit trail
- Easy to add new agents

### Tool-Mediated Communication

Agents communicate **only through tools** — they don't talk to each other directly:

```
Agent A: writes to database
Agent B: reads from database
Agent A: triggers webhook
Agent B: processes webhook
```

**This is how [[MCP]] works** — agents access tools, not each other.

## Key Research Findings

From the LLM-Coordination paper (arXiv:2310.03903):

### Finding 1: Not All LLMs Coordinate Equally

Some LLMs are better at coordination than others, independent of their individual task performance. Properties that help:
- Better instruction following
- Longer context windows
- Lower hallucination rate
- More coherent long-range reasoning

### Finding 2: Prompting for Coordination

"Think step by step" doesn't just help reasoning — it helps agents communicate their reasoning to each other.

Coordinating prompts:
- "Before acting, describe your current understanding of the task"
- "Explicitly state what you're about to do and why"
- "Note any assumptions you're making"

### Finding 3: Coordination Overhead is Real

Adding a second agent doesn't give 2x throughput. There's coordination overhead:
- Communication time
- Context-switching
- Conflict resolution

**The paper found ~30% overhead for well-designed coordination.** Badly designed coordination can give negative returns.

### Finding 4: Hierarchy Beats Flat Structures

Supervisor patterns outperform equal-agent collaboration by significant margins.

## Implementing LLM Coordination

### With LangGraph

```python
from langgraph.graph import StateGraph

# Define agent states
class AgentState(TypedDict):
    messages: list
    current_task: str
    agent_assignments: dict

# Supervisor decides who runs next
def supervisor(state):
    if "research" in state["current_task"]:
        return "research_agent"
    elif "write" in state["current_task"]:
        return "writer_agent"
    else:
        return "END"
```

### With CrewAI

```python
from crewai import Agent, Task, Crew

researcher = Agent(role="Researcher", goal="Find accurate info")
writer = Agent(role="Writer", goal="Create clear content")

crew = Crew(agents=[researcher, writer], tasks=[...])
crew.kickoff()
```

## Common Failures and Fixes

| Failure | Cause | Fix |
|---------|-------|-----|
| Agents talk past each other | No shared context protocol | Use structured output schemas |
| One agent dominates | No authority hierarchy | Implement supervisor pattern |
| Redundant work | No task tracking | Shared task board or state |
| Silent failures | No error propagation | Explicit error codes in output |
| Infinite loops | No termination criteria | Explicit exit conditions in prompts |

## Further Reading

- [LLM-Coordination Paper (arXiv:2310.03903)](https://arxiv.org/abs/2310.03903) — Foundational research
- [[multi-agentbench]] — The benchmark that quantifies coordination quality
- [[multi-agent-systems]] — The systems that need coordination
- [[langgraph]] — Framework implementing supervisor coordination
- [[crewai]] — Framework implementing role-based coordination
- [[mcp-model-context-protocol]] — Tool-mediated agent communication

---

*LLM Coordination is the discipline that turns "multiple agents" into "a team." Without it, you're just running several expensive, confused processes in parallel.*
