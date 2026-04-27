---
title: Agent Protocols
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [agent-protocols, mcp, a2a, standardization]
---

# Agent Protocols

## Overview

**Agent protocols** are standardized communication standards that define how AI agents interact with each other, external tools, and infrastructure. They establish common message formats, capability negotiation mechanisms, and interaction patterns that enable agents to work together without custom integration code for every connection.

In practical terms, an agent protocol acts as a universal adapter. Rather than building specific code for each agent-to-agent or agent-to-tool connection, developers implement the protocol once and gain interoperability with everything else that speaks the same language. This transforms a chaotic landscape of one-off integrations into a composable ecosystem where agents and tools can be mixed and matched dynamically.

The need for these protocols has grown urgently as AI agents become more capable and numerous. Modern agentic systems often require dozens of tools, multiple specialized agents, and various data sources to work in concert. Without standardized protocols, each component becomes an isolated silo.

## Key Protocols

### MCP (Model Context Protocol)

Developed by Anthropic, the **Model Context Protocol** has emerged as the leading open standard for connecting AI models to external tools and data sources. MCP standardizes how agents discover available tools, how they request actions, and how results are returned. Its JSON-RPC-based architecture works independently of any specific LLM provider, making it vendor-neutral and widely adoptable. MCP defines three core concepts: hosts (the AI application), clients (the connection from host to server), and servers (the provider of tools and resources).

### A2A (Agent-to-Agent) Protocol

The **A2A Protocol** addresses a different challenge: how agents delegate tasks to other agents. Where MCP connects agents to tools, A2A connects agents to agents. It handles capability discovery (what can another agent do?), task handoff (here is a task with context), and status tracking (how is it going?). This protocol is essential for building multi-agent systems where specialized agents collaborate on complex workflows.

### Supporting Protocols

Beyond MCP and A2A, the ecosystem includes framework-specific protocols like ACP (Agent Client Protocol) used in LangChain, and proprietary protocols from major providers such as OpenAI's Assistants API and Google's Vertex AI Agent Builder. The trend, however, clearly moves toward open standards that ensure vendor lock-in does not fragment the ecosystem.

## Why It Matters

Standardization through agent protocols delivers four fundamental benefits. First, **composability**: teams can build specialized agents once and reuse them across countless applications without modification. Second, **discoverability**: agents can programmatically find and understand what other agents and tools are capable of, enabling dynamic orchestration. Third, **reduced integration overhead**: a single protocol implementation connects to an entire ecosystem rather than requiring custom code for each connection. Fourth, **vendor neutrality**: organizations avoid lock-in by building on open standards rather than proprietary interfaces.

Without protocols, the agent ecosystem fragments into isolated systems that cannot communicate. With protocols, a future emerges where agents from different providers collaborate seamlessly, tools are reusable across frameworks, and developers focus on unique capabilities rather than reintegration.

## Related

- [[mcp]] — Model Context Protocol details
- [[a2a-protocol]] — Agent-to-Agent protocol specifics
- [[agentic-workflows]] — Multi-agent orchestration patterns
