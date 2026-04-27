---
title: "Agent"
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [ai-agents, autonomous-ai, llm]
related:
  - [[agentic-ai]]
  - [[multi-agent-systems]]
  - [[agent-memory-architecture]]
  - [[agent-frameworks]]
---

# Agent

An **AI Agent** (or **agent**) is an LLM-powered system that **perceives, decides, and acts autonomously** to accomplish tasks without continuous human intervention. Unlike a simple LLM prompt-response, an agent maintains state, uses tools, plans multi-step workflows, and can improve its own performance over time.

## Core Components

Every production agent has these building blocks:

1. **Language Model** — The reasoning engine (GPT-4o, Claude 3.5, Gemini 2.5, Llama 3.1 405B, or local models like Llama 3.3 70B via llama.cpp)
2. **Tool Layer** — APIs, functions, search, code execution, file I/O that extend what the agent can do beyond text generation
3. **Memory** — Architecture for retaining context across turns and sessions:
   - **Working memory**: Current context window
   - **Episodic memory**: Past interactions and outcomes
   - **Knowledge memory**: RAG over external documents
4. **Planning/Reasoning** — Chain-of-thought, ReAct, or other reasoning loops that decompose tasks
5. **Orchestration** — How the agent coordinates sub-agents or sub-tasks (supervisor pattern, sequential pipeline, parallel debate)

## Agent vs. Tool

| Aspect | Traditional Tool | AI Agent |
|--------|-----------------|----------|
| **Input** | Fixed parameters | Natural language goal |
| **Output** | Single response | Multi-step plan + execution |
| **State** | Stateless | Stateful (remembers context) |
| **Adaptation** | None | Learns from feedback |
| **Use case** | Compute/lookup | Complex, multi-step tasks |

## Agent Taxonomy (2026)

### By Autonomy Level
- **Reactive** — Responds to each input, no memory between sessions (simple chatbots)
- **Stateful** — Maintains conversation context, uses tools (most production agents)
- **Self-Evolving** — Modifies its own prompts, strategies, and workflows based on outcomes (frontier of 2026, per Karpathy)

### By Architecture
- **Single-agent** — One LLM handles everything
- **Multi-agent** — Multiple specialized agents coordinate (LangGraph, CrewAI, AutoGen)
- **Agentic RAG** — RAG pipeline with agentic planning and tool-calling
- **Hierarchical** — Manager agents supervising sub-agents

## Key Frameworks

- **LangGraph** — Graph-based workflow engine with Agent Protocol support
- **CrewAI** — Role-based multi-agent team framework
- **AutoGen** — Microsoft framework for multi-agent conversations
- **MCP (Model Context Protocol)** — USB-C-style protocol for connecting agents to tools (open standard, 2026)

## Self-Evolution Pattern

The 2026 frontier: agents that improve themselves via real LLM training loops:

```
Action → Outcome → Self-Reflection → 
Strategy Update → Prompt Refinement → Re-trial
```

**Karpathy (March 2026)**: "Give an agent a small but real LLM training setup and let it experiment."

## Related Concepts

- [[agentic-ai]] — The paradigm of agents as first-class autonomous entities
- [[multi-agent-systems]] — Coordination of multiple agents
- [[agent-memory-architecture]] — How agents retain context
- [[agent-frameworks]] — LangGraph, CrewAI, AutoGen deep dives
- [[vibe-coding]] — Human-AI collaborative coding with agent tools
