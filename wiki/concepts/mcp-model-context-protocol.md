---
confidence: high
last_verified: 2026-04-17
tags: [mcp, model-context-protocol, anthropic, ai-tools, interoperability]
related:
  - [[agentic-ai]]
  - [[n8n-agentic-ai]]
  - [[agent-frameworks]]
  - [[langgraph]]
  - [[tool-calling]]
relationship_count: 5
---

# MCP — Model Context Protocol

## Overview

**MCP (Model Context Protocol)** is an open protocol developed by Anthropic that standardizes how AI assistants and agents connect to external tools, data sources, and services. Originally introduced for Claude, MCP has evolved into a framework-agnostic standard adopted by [[agent-frameworks]] across the AI ecosystem.

Think of MCP as **USB-C for AI** — just as USB-C standardized device connections, MCP standardizes AI tool connections.

## Why MCP Matters

### The Problem MCP Solves

Before MCP, every AI agent framework required custom integrations:

- LangChain agents used their own tool format
- OpenAI Agents SDK used yet another format
- Custom agents required bespoke API connections

This meant **tools written for one framework couldn't be used by another**. MCP solves this by defining a universal language for agent-tool communication.

### The Solution: A Universal Standard

With MCP:

```
Any MCP-Compatible Agent ←→ MCP Protocol ←→ Any MCP-Compatible Tool
```

A tool built for Claude (using MCP) can be used by:
- [[crewAI]] agents
- [[n8n-agentic-ai|n8n]] workflows
- Custom LangGraph applications
- Any framework that adopts the MCP standard

## How MCP Works

### Architecture

MCP follows a client-server model:

| Component | Role |
|-----------|------|
| **MCP Host** | The AI application (Claude Desktop, n8n, etc.) |
| **MCP Client** | Mediates between host and server |
| **MCP Server** | Exposes tools/resources to clients |

### Core Capabilities

MCP provides two primary capabilities:

1. **Tools** — Functions the agent can call
   - File system operations
   - Web search
   - Code execution
   - API calls
   - Database queries

2. **Resources** — Data the agent can read
   - Local files
   - Database schemas
   - API responses
   - Configuration files

### Example MCP Server

```python
from mcp.server import MCPServer
from mcp.types import Tool

server = MCPServer("my-server")

@server.tool()
def web_search(query: str) -> str:
    """Search the web for information."""
    # Implementation
    return search_results

@server.tool()
def file_read(path: str) -> str:
    """Read a file from the local filesystem."""
    with open(path) as f:
        return f.read()
```

## MCP in the AI Agent Ecosystem

### Frameworks Supporting MCP

| Framework | MCP Support Level |
|-----------|------------------|
| Claude (Anthropic) | Native |
| [[n8n-agentic-ai|n8n]] | Native |
| [[crewAI]] | Via community plugins |
| LangGraph | Via community adapters |
| OpenAI Agents SDK | Via MCP bridges |

### Real-World MCP Server Examples

From research findings:

- **File search servers** — Index and search local files
- **Web search servers** — Google, Bing, DuckDuckGo integration
- **Code execution servers** — Run Python, JavaScript, other languages
- **Database servers** — Query PostgreSQL, MongoDB, etc.
- **Slack/Discord servers** — Send messages, read channels
- **GitHub servers** — Create issues, PRs, manage repos

## MCP vs Other Approaches

| Protocol | Scope | Adoption | Complexity |
|---------|-------|----------|------------|
| MCP | Agent ↔ Tools | Growing rapidly | Low |
| OpenAI Tool Format | Agent ↔ Tools | Wide (OpenAI ecosystem) | Low |
| LangChain Tools | Agent ↔ Tools | Wide (LangChain ecosystem) | Medium |
| Custom APIs | Varies | Per-implementation | High |

## Key Advantages of MCP

1. **Interoperability** — Write once, use everywhere
2. **Composability** — Chain MCP servers together
3. **Security** — MCP servers run locally, data stays on-device
4. **Vendor neutrality** — Not locked to one AI provider
5. **Ecosystem growth** — 100+ MCP servers available (as of April 2026)

## Resources

- **Official Documentation**: https://modelcontextprotocol.io
- **MCP GitHub**: Anthropic's official MCP implementations
- **MCP Servers**: Community-maintained list of MCP-compatible servers

## Related Concepts

- [[agentic-ai]] — The paradigm MCP enables
- [[tool-calling]] — The mechanism MCP standardizes
- [[n8n-agentic-ai]] — n8n's native MCP support
- [[agent-frameworks]] — Frameworks using MCP
