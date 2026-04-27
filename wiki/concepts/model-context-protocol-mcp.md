---
title: "Model Context Protocol (MCP)"
created: 2026-04-13
updated: 2026-04-20
type: concept
tags: [ai-agents, protocols, anthropic, claude, tools]
related:
  - [[claude-code]]
  - [[anthropic]]
  - [[apple-silicon-mlx]]
  - [[local-llm-on-mac]]
  - [[agentic-ai]]
  - [[multi-agent-systems]]
  - [[tool-calling]]
sources:
  - https://www.anthropic.com/news/model-context-protocol
  - https://modelcontextprotocol.io/docs/develop/build-client
  - https://blog.premai.io/25-best-mcp-servers-for-ai-agents-complete-setup-guide-2026/
  - https://www.natecue.com/learn/ai/mcp-model-context-protocol/
---

# Model Context Protocol (MCP)

## Overview

**Model Context Protocol (MCP)** is an open standard developed by Anthropic that enables AI assistants to connect with external data sources, tools, and services in a standardized way. Think of it as "USB for AI agents" — just as USB provides a universal connection standard between devices, MCP provides a universal connection standard between AI models and the tools they use.

MCP addresses one of the biggest challenges in AI agent development: **tool integration fragmentation**. Before MCP, every AI agent had to implement custom integrations for each tool or data source. MCP standardizes this so that once an MCP server is built, any MCP-compatible client can use it.

## Core Architecture

MCP follows a **client-server architecture** with three main components:

### 1. MCP Hosts
Applications that run AI models and want to use external tools. Examples:
- **Claude Desktop** (Anthropic's desktop app)
- **Claude Code** (AI coding agent)
- **Cursor** (AI-powered IDE)
- **Custom applications** built with the MCP SDK

### 2. MCP Clients
Clients embedded within hosts that communicate with MCP servers using the protocol. The client handles:
- Service discovery
- Request/response orchestration
- Session management

### 3. MCP Servers
Lightweight programs that expose specific capabilities via the protocol. Each server typically focuses on one domain:

| Server Type | Examples |
|-------------|----------|
| **Filesystem** | Read/write files, directory operations |
| **Database** | Query relational databases |
| **Web Search** | Google, Bing, DuckDuckGo searches |
| **Version Control** | Git operations |
| **Slack/Discord** | Messaging platform integration |
| **Custom Tools** | Any API or service |

## How MCP Works

```
┌─────────────┐     MCP Protocol      ┌──────────────┐
│   AI Host   │◄────────────────────►  │  MCP Server  │
│  (Claude)   │   stdio / HTTP / SSE  │  (Filesystem)│
│             │◄────────────────────►  │  (GitHub)   │
│             │                        │  (Slack)    │
└─────────────┘                        └──────────────┘
```

**Communication**: MCP servers can communicate via:
- **stdio** (standard input/output) — most common for local tools
- **HTTP/SSE** — for remote servers
- **WebSocket** — for real-time bidirectional communication

### Protocol Flow

1. **Initialization**: Client sends `initialize` request with protocol version and capabilities
2. **Capability Exchange**: Server responds with available tools, resources, and prompts
3. **Tool Invocation**: Client calls `tools/call` with tool name and parameters
4. **Result Return**: Server executes tool and returns structured response
5. **Resource Access**: Client can also `read` or `list` resources exposed by the server

## Key Features

### Standardized Tool Schema
MCP uses JSON Schema to define tool parameters and return types. This means:
- Tools are self-documenting
- Type checking is automatic
- Clients can dynamically discover what tools are available

### Resource Abstraction
MCP provides two-way resource access:
- **Resources offered by servers**: Databases, files, APIs that servers expose
- **Resources sent by clients**: Context that clients share with servers

### Prompt Templates
Servers can define reusable prompt templates that clients can invoke with parameters.

### Safety & Permissions
- MCP servers run as separate processes (sandboxed from the AI model)
- User consent required before tool execution
- Tools can be allowlisted/denylisted

## MCP vs alternatives

| Feature | MCP | Function Calling | Tool USE |
|---------|-----|-----------------|----------|
| **Standardization** | Open protocol | Vendor-specific | Anthropic-specific |
| **Server ecosystem** | Growing (100+ servers) | N/A | Limited |
| **Discovery** | Dynamic | Static | Static |
| **Transport** | stdio, HTTP, WebSocket | API-only | API-only |
| **Bidirectional** | Yes | No | No |

MCP's main advantage is **ecosystem portability** — build once, use everywhere. Function calling is more flexible but requires per-vendor implementation.

## Popular MCP Servers

Based on community research (2026):

- **Filesystem** — Local file operations
- **GitHub** — Issues, PRs, repos
- **Slack/Discord** — Messaging
- **PostgreSQL / SQLite** — Database queries
- **Brave Search** — Web search
- **Memory** — Persistent context across sessions

The [PremAI guide](https://blog.premai.io/25-best-mcp-servers-for-ai-agents-complete-setup-guide-2026/) lists 25+ production-ready MCP servers covering everything from AWS infrastructure to Figma design tools.

## MCP in Claude Code

Claude Code uses MCP to extend its capabilities. When you run Claude Code, it can connect to local MCP servers for:

- **Filesystem access** — read/write project files
- **Git operations** — commit, branch, diff
- **Terminal commands** — execute shell scripts
- **Custom tools** — your own API integrations

Configuring MCP servers for Claude Code:
1. Install the MCP SDK in your project
2. Define server in `mcp.json` configuration
3. Claude Code auto-discovers and uses available tools

## Why MCP Matters for AI Agents

MCP solves the **N×M integration problem**:

- Without MCP: N AI agents × M tools = N×M custom integrations
- With MCP: N AI agents + M tools = N + M connections

This dramatically accelerates the AI agent ecosystem because:
1. Tool developers only build one MCP server
2. Agent developers only implement one MCP client
3. Users can mix and match any combination

## Getting Started

### Official Resources
- [Anthropic's MCP Announcement](https://www.anthropic.com/news/model-context-protocol) — why MCP was created
- [modelcontextprotocol.io](https://modelcontextprotocol.io/docs/develop/build-client) — official docs and SDKs
- [MCP skilljar Course](https://anthropic.skilljar.com/introduction-to-model-context-protocol) — structured learning

### Quick Start
```bash
# Install MCP SDK
npm install @modelcontextprotocol/sdk

# Create a simple server
npx @modelcontextprotocol/server-filesystem ./my-project

# Connect from Claude Desktop or Claude Code
```

## Related Concepts

- [[claude-code]] — Claude Code supports MCP for extended capabilities
- [[anthropic]] — MCP was created by Anthropic
- [[tool-calling]] — MCP enables standardized tool calling
- [[agentic-ai]] — MCP is infrastructure for agentic AI systems
- [[multi-agent-systems]] — Multiple agents can share MCP servers
- [[apple-silicon-mlx]] — Local LLM inference on Apple Silicon

## Personal Notes

MCP feels like the most significant standardization effort in the AI tools space since the OpenAI function calling spec. The key insight is that the protocol is transport-agnostic (works locally via stdio or remotely via HTTP) and bidirectional (both tools and context flow both ways).

The growing ecosystem of 100+ MCP servers suggests momentum. For local LLM development on Apple Silicon, MCP could enable standardized tool use across different LLM backends.

---

*Last updated: 2026-04-20*
