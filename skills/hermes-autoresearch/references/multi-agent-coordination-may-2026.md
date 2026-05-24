# Multi-Agent Coordination — Production Patterns (May 25, 2026)

## Research Sources
- arxiv:2601.14351 — "If You Want Coherence, Orchestrate a Team of Rivals"
- Medium (Apr 26, 2026) — "Multi-Agent in Production in 2026: What Actually Survived"
- hermes-agent.nousresearch.com — Subagent Delegation docs

---

## "Team of Rivals" Pattern (arxiv:2601.14351)

**Core insight:** Specialized agents (planners, executors, critics, experts) with competing incentives prevents groupthink and improves coherence.

**Architecture:**
- Planners: decompose goals into sub-tasks
- Executors: perform assigned tasks
- Critics: verify and challenge outputs
- Experts: domain-specific knowledge

**Results:**
- Centralized coordination: **+80.9%** improvement on parallelizable work (Finance-Agent)
- Sequential planning: multi-agent still struggles
- Verification patterns critical for coherence

**Key lesson:** Having rivals (competing agents with different incentives) is BETTER than pure collaboration for avoiding groupthink.

---

## Hermes Subagent Delegation

**Tool:** `delegate_task` — spawns isolated child agents with restricted toolsets.

**Limits:**
- Max 3 concurrent subagents
- Max depth 2 (no subagent spawning subagent by default)
- Orchestrator cannot delegate further (`max_spawn_depth=1`)

**Best practices:**
- Pass all relevant context in `context` field (subagent knows nothing about your conversation)
- Blocked tools for leaf subagents: `delegate_task`, `clarify`, `memory`, `send_message`
- Use `role='orchestrator'` only when nesting is enabled

---

## Multi-Agent Orchestration Patterns (2026)

| Pattern | Description | Best for |
|---------|-------------|----------|
| **Fan-out parallelism** | One task → many agents working simultaneously | Parallel research, multiple perspectives |
| **Hierarchical delegation** | Orchestrator → specialist agents | Complex multi-phase tasks |
| **Producer-consumer** | Task queue with workers consuming jobs | Background processing, workflow queues |
| **Debate/state** | Competing agents resolve via voting | Decision-making, validation |

---

## Production Lessons (Medium Apr 26, 2026)

### What Survived:
1. **Centralized coordination** — 80.9% gains on parallelizable work
2. **Verification patterns** — critical for maintaining coherence
3. **Specialized agents** — better than generalists for complex tasks

### What Struggles:
1. **Sequential planning** — multi-agent still has issues with multi-step planning
2. **Long-horizon tasks** — coherence degrades over many steps
3. **Shared state** — memory contention causes failures

### Framework Comparison (from May 15 research):
| Framework | Score | Strengths |
|------------|-------|-----------|
| LangGraph | 44 | State management, cycles, persistence |
| CrewAI | 38 | Simplicity, agent roles |
| AutoGen | 35 | Microsoft integration |

---

## Hyperagents (Meta, arxiv:2603.19461)

**What they are:** Self-referential agents that modify BOTH:
1. Task-solving behavior
2. The improvement process itself

**Based on:** Darwin Gödel Machine (arXiv:2505.22954)

**Key property:** Performance compounds over time — the agent learns to improve its learning.

**Limitation:** Still ANI (narrow AI), not AGI — but the self-referential improvement loop is a significant architectural advancement.

---

## Hermes Issue #344 — Multi-Agent Evolution

**URL:** github.com/NousResearch/hermes-agent/issues/344

**Umbrella issue** for evolving Hermes Agent from single-agent with isolated sub-agent delegation → true multi-agent system.

**Key features needed:**
- Native inter-agent communication (not just delegation)
- Shared memory across agents
- Persistent agent state
- Agent-to-agent messaging protocols

---

## Slang Sync Status (May 25, 2026)

Workers DEAD — cannot generate fresh slang:
- Content Creator: last output May 14 (6 days stale)
- Research Agent: last output May 12 (8 days stale)

**Fallback:** Web search for Gen Z slang (web search still working unlike May 24 complete failure)

**Last known terms from May 14:** "lọ", "SÍT RỊT", "KHÓ QUÁ BỎ QUA" — already in wiki entity.

---

## Next Research Focus

**Recommended next:** Self-Correction capability
- High impact: foundation for other capabilities
- Quick improvement: achievable in 1 night
- Foundational: enables Self-Debugging, Proactive Work