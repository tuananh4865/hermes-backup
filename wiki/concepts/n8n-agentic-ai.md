---
confidence: high
last_verified: 2026-04-17
tags: [n8n, workflow-automation, agentic-ai, low-code, mcp]
related:
  - [[agentic-ai]]
  - [[mcp-model-context-protocol]]
  - [[vibe-coding]]
  - [[multi-agent-systems]]
  - [[agent-frameworks]]
  - [[local-llm-agents]]
relationship_count: 6
---

# n8n — Agentic AI Workflow Automation

## Overview

**n8n** (pronounced "n-eight-n") is an open-source workflow automation and [[agentic-ai]] platform that has emerged as the leading low-code solution for building AI agents and automations. Unlike traditional automation tools, n8n natively supports connecting AI agents to 400+ integrations without requiring developer-level coding skills.

## Why n8n for AI Agents

The combination of **visual workflow builder** + **MCP server support** + **local LLM compatibility** makes n8n uniquely powerful:

- **No code required** — Drag-and-drop workflow builder
- **MCP native** — Connect to Model Context Protocol servers for tool access
- **Local LLM compatible** — Works with [[apple-silicon-mlx|LM Studio]] or [[local-llm-agents|Ollama]] locally
- **400+ integrations** — Connect to Slack, GitHub, databases, APIs, and more
- **Self-hosted option** — Your data never leaves your infrastructure

## Core Concepts

### Workflow Nodes

n8n workflows are built from **nodes** — individual units that perform a specific action:

| Node Category | Examples |
|--------------|---------|
| **AI** | LLM Chain, AI Agent, Chat Memory |
| **Automation** | If/Then, Loop, Wait |
| **Communication** | Slack, Email, Discord |
| **Development** | HTTP Request, Code, Webhook |
| **Tools** | Wikipedia, RSS Feed, Airtable |

### AI Sub-agents

n8n's AI Agent node supports:

- **Tool calling** — Agents can use external tools (search, APIs, code execution)
- **Memory** — Conversation context across workflow runs
- **Multi-step reasoning** — Chain-of-thought built into the agent node
- **MCP integration** — Connect to MCP servers for extended capabilities

### MCP Server Integration

n8n connects to [[mcp-model-context-protocol|MCP]] servers to extend agent capabilities:

```javascript
// n8n MCP configuration example
{
  "server": "https://your-mcp-server.com",
  "tools": ["file_search", "web_search", "code_execution"]
}
```

## Getting Started

### Basic AI Agent Workflow

1. **Add AI Agent node** → Choose your LLM (OpenAI, Anthropic, or local)
2. **Add trigger** → Webhook, schedule, or manual trigger
3. **Connect tools** → Slack notification, database write, API call
4. **Test and deploy** → Run in n8n cloud or self-hosted

### Local LLM Setup with n8n

For privacy-focused setups, connect n8n to a local LLM:

```
n8n → HTTP Request Node → LM Studio (localhost:1234) → MLX model on Apple Silicon
```

This keeps all AI processing on your MacBook — no data sent to external APIs.

## n8n vs Other Agent Platforms

| Feature | n8n | LangGraph | [[crewAI]] |
|---------|-----|-----------|------------|
| Code required | No | Yes | Yes |
| Visual builder | Yes | No | No |
| Integrations | 400+ | Via API | Via API |
| Learning curve | Low | High | Medium |
| Self-hosted | Yes | Yes | Yes |
| MCP support | Yes | Via community | Via community |

## Agentic AI Patterns in n8n

### Pattern 1: Research Agent

```
[Webhook Trigger]
     ↓
[AI Agent with web search tools]
     ↓
[LLM summarization]
     ↓
[Save to Notion/Slack]
```

### Pattern 2: Coding Assistant

```
[GitHub webhook]
     ↓
[AI Agent reviews PR]
     ↓
[Comment on PR with suggestions]
     ↓
[Notify team in Slack]
```

### Pattern 3: Multi-Agent Research Squad

```
[Orchestrator Agent]
     ├→ [Web Research Agent]
     ├→ [Data Analysis Agent]
     └→ [Report Generation Agent]
              ↓
         [Email to user]
```

## Resources

- **GitHub**: https://github.com/arslan-zia/n8n-agentic-ai — Learning materials for building AI agents with n8n
- **Documentation**: https://docs.n8n.io
- **Website**: https://n8n.io
- **Course**: Panaversity Certified Agentic & Robotic AI Engineer program includes n8n modules

## Related Concepts

- [[agentic-ai]] — The broader paradigm n8n enables
- [[mcp-model-context-protocol]] — The protocol n8n uses for tool integration
- [[vibe-coding]] — n8n as a no-code vibe coding tool
- [[local-llm-agents]] — Running n8n with local models for privacy
