---
title: "Multi-Agent Coordination Patterns"
created: 2026-04-16
updated: 2026-04-19
type: concept
tags: [multi-agent, coordination, orchestration, agentic-ai, crewai, langgraph, patterns]
sources:
  - https://arxiv.org/abs/2601.11044 (AgencyBench)
  - https://github.com/crewAIInc/crewAI
  - https://www.aicompetence.org (Why Multi-Agent Systems Fail In Production)
related:
  - multi-agent-systems
  - crewai
  - langgraph
  - agentic-ai
  - agent-orchestrator
---

# Multi-Agent Coordination Patterns

## Overview

Multi-agent systems distribute tasks across multiple AI agents that must collaborate, coordinate, and sometimes compete to accomplish complex goals. Unlike single-agent systems where one agent handles everything, multi-agent architectures decompose problems into specialized roles and orchestrate their interactions.

The key insight: **coordination overhead is the primary failure mode**. A system of 5 agents that communicate poorly will underperform a single agent on most tasks. Getting coordination right is 80% of the multi-agent design problem.

## Coordination Patterns

### 1. Hierarchical (Supervisor-Worker)

A supervisor agent decomposes tasks and delegates to specialized workers:

```
         [Supervisor]
            │ ▲
      ┌─────┴─────┐
      │           │
  [Worker A]  [Worker B]
      │           │
      └─────▲─────┘
            │
        [Result]
```

**Best for**: Tasks that decompose cleanly into independent subtasks
**Frameworks**: LangGraph (directed graph), AutoGen (group chat with manager)

**Failure mode**: Supervisor becomes bottleneck; workers sit idle waiting for tasks

### 2. Collaborative (Crew/Swarm)

Agents work together on the same problem with different perspectives:

```
    [Researcher] ──┐
                   ├──► [Synthesis] ──► Output
    [Critic] ─────┘
```

**Best for**: Complex reasoning requiring multiple viewpoints (research + analysis + review)
**Frameworks**: CrewAI (role-based crews), LangGraph (state graph with merging)

### 3. Sequential Pipeline

Output of one agent feeds into the next:

```
[Ingest] → [Process] → [Analyze] → [Report]
```

**Best for**: Linear workflows where each stage builds on the previous
**Frameworks**: LangGraph (chain), n8n (visual workflow)

### 4. Parallel + Merge

Multiple agents work simultaneously, results merge:

```
      ┌──────────┐
      │  Input   │
      └────┬─────┘
      ┌────┴─────┐
      │         │
  [Agent A] [Agent B]  ← parallel
      │         │
      └────┬─────┘
      ┌────┴─────┐
      │  Merge   │
      └────┬─────┘
   [Consensus / Vote / Select Best]
```

**Best for**: Tasks with multiple valid approaches (research 5 sources → synthesize best findings)

### 5. Competitive / Debate

Agents argue positions and converge via debate:

```
[Agent A: "Yes"] ←──→ [Agent B: "No"]
       │                  │
       └────────┬─────────┘
                ▼
         [Arbiter/Judge]
```

**Best for**: Complex decisions with trade-offs
**Research insight**: [Multi-Agent Collaborative Filtering (arXiv:2511.18413)](https://arxiv.org/abs/2511.18413) shows that structured debate improves reasoning on ambiguous problems

## Why Multi-Agent Systems Fail (Production)

Per [AI Competence](https://www.aicompetence.org), 90%+ of enterprise multi-agent deployments fail for these reasons:

### 1. Coordination Overhead

Adding agents doesn't scale linearly. Each new agent adds:
- Communication latency
- State synchronization complexity
- Potential for contradictory outputs

**Rule of thumb**: Start with 2 agents. Only add more when you've proven the coordination pattern works.

### 2. Memory Fragmentation

Agents in distributed systems lose shared context. Each agent has its own view of the problem. Without shared memory architecture, you get:

- Agent A works on outdated information from Agent B
- Contradictory outputs because agents didn't share reasoning
- Duplicated work

**Solution**: Shared vector store or knowledge graph for persistent context

### 3. Trust Boundaries

In production, you need:
- **Authentication**: Which agents can call which tools
- **Authorization**: Can Agent B instruct Agent A to delete data?
- **Audit trail**: Who made which decision?

No framework has standardized this yet. It's the frontier problem.

### 4. Observability Gaps

Debugging a single agent is hard. Debugging 5 agents interacting is exponentially harder. When something goes wrong, you need:

- Per-agent logging with correlation IDs
- Visualization of agent-to-agent messages
-Replay capability to reproduce failures

## Framework Comparison for Coordination

| Pattern | Best Framework | Why |
|---------|----------------|-----|
| Hierarchical | LangGraph | Explicit graph structure |
| Collaborative | CrewAI | Role-based with memory |
| Sequential | n8n | Visual workflow builder |
| Parallel + Merge | LangGraph | Fan-out/fan-in pattern |
| Debate | AutoGen | Built-in group chat |

## Designing Multi-Agent Systems

### Decision Tree: Do You Need Multiple Agents?

```
Does task decompose into independent subtasks?
├── NO → Single agent
└── YES → Do agents need different tools/expertise?
    ├── NO → Parallel single agents (ensemble)
    └── YES → Do agents need to communicate?
        ├── NO → Pipeline (sequential)
        └── YES → Is there a natural supervisor?
            ├── YES → Hierarchical
            └── NO → Collaborative/Debate
```

### Anti-Patterns

1. **Agent soup**: 20 agents with no clear coordination pattern — debugging nightmare
2. **Monolithic agent split**: Taking a working single agent and splitting it into "agents" without clear role boundaries
3. **Synchronous everything**: Every agent waits for every other — deadlocks and latency

## Real Production Patterns

### GitHub Issue Triage (3 agents)
```
[Ingest Agent] → classify issue → [Router Agent] → assign to domain
                                                    ├── [Code Agent] → implement
                                                    └── [Docs Agent] → update docs
```

### Research Pipeline (4 agents)
```
[Web Search Agent] → collect sources
[Reading Agent] → extract key findings
[Analysis Agent] → synthesize patterns
[Writing Agent] → produce report
```

### Code Review (3 agents)
```
[Author Agent] → submit code change
[Reviewer Agent] → critique approach
[Verifier Agent] → check tests + lint
```

## Related Concepts

- [[multi-agent-systems]] — Broader multi-agent systems
- [[crewai]] — CrewAI framework for role-based teams
- [[langgraph]] — LangGraph for graph-based orchestration
- [[agent-orchestrator]] — Orchestrator pattern
- [[autogen]] — Microsoft's AutoGen framework
- [[agentic-ai]] — Agentic AI paradigm
