---
title: "Google Agent-to-Agent Protocol"
created: 2026-04-09
updated: 2026-04-17
type: concept
tags: [ai-agents, protocol, google, interop, 2026]
related:
  - [[mcp-model-context-protocol]]
  - [[multi-agent-systems]]
  - [[agent-frameworks]]
  - [[agentic-ai]]
---

# Google Agent-to-Agent Protocol

## Overview

Google's **Agent-to-Agent Protocol** (A2A) is an open specification for enabling AI agents to communicate and collaborate across different frameworks, cloud platforms, and organizational boundaries. Launched April 9, 2025, it celebrated its **1-year anniversary** on April 9, 2026 with strong adoption metrics.

## Key Metrics (April 2026)

| Metric | Value |
|--------|-------|
| GitHub Stars | 22,000+ |
| Participating Organizations | 150+ |
| Cloud Platform Support | Azure, Google Cloud, AWS |
| Status | Production-ready |

## Why A2A Matters

The agent ecosystem is fragmented — CrewAI agents can't natively talk to LangGraph agents, and enterprise agents are locked to their platforms. A2A solves this by defining a **common communication protocol** that any agent framework can implement.

## How It Works

A2A defines:
- **Agent Cards** — JSON descriptors that advertise an agent's capabilities, endpoints, and authentication requirements
- **Task Exchange** — Standard format for passing tasks between agents, including context, instructions, and expected outputs
- **Capability Negotiation** — Agents can discover each other's capabilities at runtime and delegate appropriately
- **State Synchronization** — Mechanisms for keeping task state consistent across agent boundaries

## Comparison with MCP

| Aspect | MCP | A2A |
|--------|-----|-----|
| Purpose | Connect agents to tools/data | Connect agents to agents |
| Focus | Tool calling | Agent-to-agent collaboration |
| Origin | Anthropic (Claude) | Google |
| Ecosystem | 150+ servers | 150+ orgs |

## Production Deployments

A2A is now in production at:
- **Azure** — Microsoft integration for enterprise agent workflows
- **Google Cloud** — Vertex AI agent marketplace
- **AWS** — Bedrock multi-agent orchestration

## See Also

- [[mcp-model-context-protocol]] — Tool/data connection protocol
- [[multi-agent-systems]] — Multi-agent architecture patterns
- [[agent-frameworks]] — LangGraph, CrewAI, AutoGen

---

*Source: [AI Weekly: Agents, Models, and Chips — April 9-15, 2026](https://dev.to/alexmercedcoder/ai-weekly-agents-models-and-chips-april-9-15-2026)*
