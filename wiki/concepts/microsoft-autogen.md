---
title: "Microsoft AutoGen"
created: 2026-04-15
updated: 2026-04-19
type: concept
tags: [microsoft, multi-agent, agent-framework, python, .net]
related:
  - [[multi-agent-systems]]
  - [[langgraph]]
  - [[crewai]]
  - [[agent-orchestrator]]
  - [[mcp-model-context-protocol]]
  - [[semantic-kernel]]
sources:
  - https://github.com/microsoft/autogen
  - https://learn.microsoft.com/en-us/agent-framework/overview/
  - https://www.digitalapplied.com/blog/microsoft-agent-framework-1-0-dotnet-python-guide
  - https://www.openaitoolshub.org/en/blog/microsoft-agent-framework-review
---

# Microsoft AutoGen

Microsoft AutoGen is an open-source **programming framework for agentic AI** that enables multi-agent applications where AI agents can work autonomously or collaborate with humans. AutoGen was the research project that evolved into **Microsoft Agent Framework 1.0** (GA April 2026), which unifies AutoGen with Semantic Kernel into a single production-ready SDK.

## AutoGen Origins

AutoGen started as a Microsoft Research project focused on **multi-agent conversation programming**. The key insight: instead of writing a single agent prompt, build systems where multiple specialized agents negotiate, delegate, and collaborate to solve complex tasks.

**Core abstraction:** Agents that communicate via messages, with humans in the loop when needed.

## Microsoft Agent Framework 1.0 (GA April 2026)

In April 2026, Microsoft consolidated AutoGen and Semantic Kernel into the **Microsoft Agent Framework** — a unified .NET + Python SDK for building production agent systems.

**Key features (per [Microsoft Learn](https://learn.microsoft.com/en-us/agent-framework/overview/)):**
- **Unified SDK** — Single framework for both .NET and Python
- **MCP native** — Built-in Model Context Protocol support for tool calling
- **A2A (Agent-to-Agent)** — Native protocol for inter-agent communication
- **Graph-based workflows** — Define complex orchestration as directed graphs
- **Enterprise features** — Session-based state management, type safety, middleware, telemetry
- **Semantic Kernel integration** — Planning, memory, and skill management

## Architecture

### Agent Types

```python
# Basic agent setup
from autogen import ConversableAgent

# Assistant agent (LLM-powered)
assistant = ConversableAgent(
    name="assistant",
    system_message="You are a helpful coding assistant.",
    llm_config={"model": "gpt-4o"}
)

# User proxy agent (human in the loop)
user_proxy = ConversableAgent(
    name="user_proxy",
    human_input_mode="ALWAYS"  # Or "TERMINATE" for fully autonomous
)

# Start conversation
chat = assistant.initiate_chat(user_proxy, message="Write a Python quicksort.")
```

### Multi-Agent Orchestration

```python
from autogen import GroupChat, GroupChatManager

# Create specialized agents
researcher = ConversableAgent(name="researcher", system_message="You research topics thoroughly.")
writer = ConversableAgent(name="writer", system_message="You write clear, concise reports.")
critic = ConversableAgent(name="critic", system_message="You review work and provide constructive criticism.")

# Group chat with manager
group_chat = GroupChat(
    agents=[researcher, writer, critic],
    messages=[],
    max_round=10
)

manager = GroupChatManager(groupchat=group_chat)

# Run the group chat
researcher.initiate_chat(
    manager,
    message="Research the impact of AI on software development and write a 500-word report."
)
```

### Tool Use with MCP

```python
from autogen import register_function
from autogen.code_utils import create_exec_from_math

# Register tools for agents
assistant = ConversableAgent(
    name="assistant",
    llm_config={"model": "gpt-4o", "tools": [{"type": "function", "function": search}]}
)

# Agent can now use tools autonomously
```

## Comparison with LangGraph and CrewAI

| Feature | Microsoft Agent Framework | LangGraph | CrewAI |
|---------|-------------------------|-----------|--------|
| **Language** | Python + .NET | Python | Python |
| **Multi-agent** | Native group chat | Graph nodes | Role-based agents |
| **MCP support** | Native | Via LangChain MCP | Community |
| **Human-in-loop** | Built-in | Manual | Manual |
| **Enterprise** | Yes (telemetry, middleware) | No | No |
| **Learning curve** | Medium | Steep | Low |
| **GitHub stars** | 40K+ | 10K+ | 25K+ |

## Use Cases

### 1. Research Pipeline
Three agents in sequence: researcher → writer → critic.
- Researcher gathers data from web search
- Writer synthesizes into report
- Critic reviews and suggests revisions

### 2. Customer Support Agent
Single agent with MCP-connected tools:
- Knowledge base lookup (MCP server)
- Ticket creation (MCP server)
- Customer profile lookup (MCP server)

### 3. Code Review Team
Parallel agents reviewing different aspects:
- Security agent checks for vulnerabilities
- Performance agent looks for bottlenecks
- Style agent enforces linting rules

## Installation

```bash
# Python
pip install autogen

# .NET
dotnet add package Microsoft.AgentFramework
```

## Limitations

- **Complexity** — Multi-agent conversations can be hard to debug
- **Cost** — Multiple LLM calls per interaction adds up fast
- **AutoGen deprecated** — Original AutoGen is in maintenance mode; new development is in Microsoft Agent Framework
- **State management** — Requires careful design for long-running conversations

## Related Concepts

- [[multi-agent-systems]] — General multi-agent architecture
- [[langgraph]] — Graph-based agent orchestration
- [[crewai]] — Role-based AI agent framework
- [[agent-orchestrator]] — Orchestration patterns for agents
- [[mcp-model-context-protocol]] — Tool calling protocol
- [[semantic-kernel]] — Microsoft's AI SDK (now merged into Agent Framework)

## Further Reading

- [AutoGen GitHub](https://github.com/microsoft/autogen) — Official repository
- [Microsoft Agent Framework Docs](https://learn.microsoft.com/en-us/agent-framework/overview/) — Official documentation
- [Microsoft Agent Framework 1.0 Guide](https://www.digitalapplied.com/blog/microsoft-agent-framework-1-0-dotnet-python-guide) — Setup walkthrough
