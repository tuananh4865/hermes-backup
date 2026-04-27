---
title: "LLM Agents"
created: 2026-04-13
updated: 2026-04-15
type: concept
tags: [llm, agents, autonomous, tool-calling, reasoning, multi-agent]
relationships:
  - 🔗 claude-code
  - 🔗 langgraph
  - 🔗 crewai
  - 🔗 mcp-model-context-protocol
  - 🔗 agent-memory
  - 🔗 rag-(retrieval-augmented-generation)
  - 🔗 tool-calling
---

# LLM Agents

## Overview

An LLM Agent is an autonomous system that uses a large language model to reason, plan, and execute tasks — often by calling external tools, interacting with APIs, or delegating subtasks to other agents. Unlike a standard LLM that produces a single response, an agent maintains state, pursues goals across multiple steps, and can improve its behavior based on feedback.

The agentic AI paradigm — where models don't just answer questions but take actions — has become the dominant research direction in 2026, with self-improving multi-agent systems leading to breakthroughs in coding, scientific discovery, and workflow automation.

## Core Components

### 1. Reasoning Engine
The LLM serves as the "brain" — given a goal, it reasons through the steps needed to achieve it:

```
Goal → Decompose → Execute Step → Observe Result → Repeat until done
```

This loop is called the **agentic loop**. Modern agents use chain-of-thought, ReAct (Reason + Act), or tree-of-thoughts prompting to plan effectively.

### 2. Tool Calling
Agents interact with the world through tools:

| Tool Type | Examples |
|-----------|----------|
| **Code execution** | Write/run Python, Bash, JavaScript |
| **Web search** | Search, fetch pages, extract content |
| **File operations** | Read, write, edit files |
| **API calls** | REST, GraphQL, webhooks |
| **External agents** | Delegate subtasks to other agents |

The Model Context Protocol ([[mcp-model-context-protocol]]) standardizes how agents connect to external tools and data sources.

### 3. Memory
Agents persist information across interactions:

- **Short-term**: Conversation context, current task state
- **Long-term**: Retrieved facts, learned patterns, past successes/failures
- **RAG** ([[rag-(retrieval-augmented-generation)]]): Hybrid of memory + retrieval

### 4. Multi-Agent Architecture
Complex tasks are distributed across specialized agents:

```
Orchestrator Agent
├── Research Agent (web search, fact-checking)
├── Coding Agent (write/edit code, run tests)
└── Review Agent (quality gate, critique)
```

Frameworks like [[langgraph]] and [[crewai]] provide orchestration patterns for multi-agent systems.

## Agent Frameworks (2026)

### LangGraph
Builds stateful, cyclic workflows on top of LangChain. Best for:
- Complex multi-step reasoning with branching
- Agents that need to loop, branch, or backtrack
- Production-grade agent pipelines

```python
from langgraph.graph import StateGraph

graph = StateGraph(AgentState)
graph.add_node("research", research_node)
graph.add_node("act", act_node)
graph.add_edge("research", "act")
```

### CrewAI
Role-based multi-agent framework. Best for:
- Pipeline with clear role separation (researcher, writer, reviewer)
- Simpler workflows that don't need fine-grained control
- Fast prototyping of agent teams

### OpenAI Agents SDK
OpenAI's lightweight agent framework (2026):
- Built-in streaming, tool calling, handoffs
- Tight integration with OpenAI models
- Best for agents that use OpenAI as the backbone

### Claude Code / Claude Code Skills
Anthropic's CLI agent for autonomous coding:
- Executes in repository context
- Skills system for extensibility
- Terminal-based, no GUI

## The Agentic Loop

```
┌─────────────────────────────────────────────────────┐
│ 1. GOAL RECEIVED                                     │
│    "Build a REST API for my todo app"               │
├─────────────────────────────────────────────────────┤
│ 2. PLAN                                              │
│    - Design API endpoints                            │
│    - Set up project structure                        │
│    - Write code                                      │
│    - Add tests                                       │
├─────────────────────────────────────────────────────┤
│ 3. EXECUTE (tool calls)                              │
│    - Write server.py                                 │
│    - Write routes.py                                 │
│    - Install dependencies                            │
├─────────────────────────────────────────────────────┤
│ 4. OBSERVE / REFLECT                                │
│    - Check: Does it compile?                         │
│    - Self-correct if needed                          │
├─────────────────────────────────────────────────────┤
│ 5. REPEAT until goal achieved                        │
└─────────────────────────────────────────────────────┘
```

## Key Research Findings (2026)

### Self-Improving Agents
Agents that learn from their own failures:
- **Reflection**: Agents critique their own outputs (similar to Reflexion paper)
- **Self-correction loops**: Generate → Test → Fix → Repeat
- **Knowledge accumulation**: Store successful strategies for reuse

### Agent Memory Patterns
The most effective memory architectures combine:
1. **Semantic memory**: Vector embeddings of past experiences (RAG)
2. **Procedural memory**: Learned workflows and tool sequences
3. **Episodic memory**: Log of what worked/didn't in specific contexts

### Tool Calling Evolution
- **Function calling**: Structured tool invocation via OpenAI function schema
- **Computer use agents**: Agents that literally control a desktop environment
- **MCP standardization**: [[mcp-model-context-protocol]] enables tool sharing across frameworks

## Apple Silicon + Local LLM Agents

Running agents locally on MacBook (Apple Silicon) is increasingly viable:

- **MLX models** (via [[apple-silicon-mlx]]): 4-bit quantized models run at 30+ tokens/sec on M3
- **llama.cpp**: GGUF format enables CPU inference with good throughput
- **Ollama**: Single-command local deployment with OpenAI-compatible API
- **LM Studio**: GUI + API server for local model management

### Benchmarks (2026, M3 Max 128GB)

| Model | Quant | Tokens/sec | Best For |
|-------|-------|------------|----------|
| Llama 3.1 8B | Q4_K | 45 | Fast coding assistance |
| Mistral 7B | Q5_K | 32 | Balanced reasoning |
| Phi-4 4B | Q8 | 78 | Lightweight tasks |
| DeepSeek-R1 8B | Q4_K | 28 | Reasoning/math |

## Practical Applications

### Coding Agents
- **Claude Code**: Autonomous Git operations, code writing, PR creation
- **Cursor AI**: IDE with embedded agent for pair programming
- **Devin** (Cognition): Full software engineer agent

### Research Agents
- Multi-agent teams that divide: web search → synthesis → critique → write
- Agents that read papers, extract insights, maintain literature databases

### Workflow Automation
- Chain-of-thought agents that use [[n8n]] or similar to orchestrate: email → summarization → task creation → calendar

## Related Concepts

- [[agent-memory]] — How agents store and retrieve information
- [[tool-calling]] — Structured function invocation from LLMs
- [[langgraph]] — Framework for building agent workflows
- [[crewai]] — Role-based multi-agent framework
- [[mcp-model-context-protocol]] — Standard protocol for agent-tool connectivity
- [[claude-code]] — Anthropic's autonomous coding agent
- [[apple-silicon-mlx]] — Local MLX inference on Mac

## Further Reading

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI GitHub](https://github.com/crewAI/crewAI)
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [Anthropic's Agent Introduction](https://www.anthropic.com/research/building-effective-agents)
