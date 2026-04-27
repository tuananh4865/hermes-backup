---
title: "MCP — Model Context Protocol"
created: 2026-04-18
updated: 2026-04-19
type: concept
tags: [mcp, model-context-protocol, ai-agents, tool-calling, standards, agentic-ai]
sources:
  - https://github.com/modelcontextprotocol/servers
  - https://github.com/modelcontextprotocol/specification
related:
  - langgraph
  - crewai
  - agentic-ai
  - tool-calling
---

# MCP — Model Context Protocol

## Overview

The **Model Context Protocol (MCP)** is an open standard developed by Anthropic (with community contributions) that enables AI applications to connect to external tools, data sources, and services through a standardized interface. Think of it as "USB for AI agents" — a universal protocol that lets any MCP-compatible agent discover and use any MCP-compatible tool without custom integration code.

MCP addresses the fundamental problem: every AI agent framework historically required custom integrations for every tool. An agent built on LangChain needed different code to use Slack than an agent built on CrewAI. MCP creates a shared language so tools and agents can speak to each other universally.

## Core Architecture

MCP follows a client-server model:

```
┌─────────────┐      MCP Protocol      ┌──────────────┐
│  AI Agent   │◄─────────────────────►│  MCP Server  │
│  (Client)   │                       │  (Tool Host) │
└─────────────┘                       └──────────────┘
```

- **MCP Client**: Embedded in the AI agent/framework (e.g., Claude Code, LangGraph, CrewAI)
- **MCP Server**: Exposes a specific tool or data source (e.g., Slack server, filesystem server, GitHub server)
- **Communication**: Via JSON-RPC over stdio or HTTP/SSE

### Server Types

| Type | Description | Example |
|------|-------------|---------|
| **Filesystem** | Read/write local files | `mcp-server-filesystem` |
| **GitHub** | Repository, PR, issue operations | `mcp-server-github` |
| **Slack** | Messaging and channel operations | `mcp-server-slack` |
| **Database** | SQL query execution | `mcp-server-postgres` |
| **Browser** | Web browsing and scraping | `mcp-server-browser` |
| **Custom** | Any REST/GraphQL API | User-defined |

## The Official Server Registry

The [Model Context Protocol Servers repository](https://github.com/modelcontextprotocol/servers) is the canonical source for reference implementations. As of April 2026, it contains 1000+ community-contributed servers covering every major tool category.

The registry provides:
- **Discovery**: Find servers by category, capability, or language
- **Verification**: Official servers are tested and maintained
- **Community servers**:扩展 ecosystem beyond Anthropic's official offerings

## MCP vs Other Approaches

### MCP vs Custom Tool Integrations

| Aspect | MCP | Custom Integration |
|--------|-----|-------------------|
| **Setup time** | Minutes | Days to weeks |
| **Framework portability** | Works everywhere | Framework-specific |
| **Maintenance** | Protocol update → server update | Re-write each integration |
| **Discovery** | Central registry | Custom research |

### MCP vs LangChain Tool Integration

LangChain has adopted MCP as a first-class integration path. You can now use any MCP server within LangChain's agent framework without custom code:

```python
from langchain_mcp import MCPTool
# Works with any MCP-compatible tool
```

### MCP vs OpenAI's Function Calling

OpenAI's native function calling is model-specific. MCP is model-agnostic — the protocol abstracts tool communication regardless of which LLM powers the agent. This means the same MCP server works with Claude, GPT-4, Gemini, and local models.

## Key Features

### 1. Dynamic Tool Discovery

Agents can query available tools at runtime rather than having them hardcoded. This enables:
- **Runtime capability discovery**: "What tools do I have access to?"
- **Conditional tool loading**: Load tools based on task requirements
- **Tool sandboxing**: Run untrusted tools in isolation

### 2. Standardized Schema

Every tool follows the same JSON schema for inputs and outputs:
```json
{
  "name": "search_codebase",
  "description": "Search code in repository",
  "input_schema": {
    "type": "object",
    "properties": {
      "query": {"type": "string"},
      "file_pattern": {"type": "string"}
    }
  }
}
```

### 3. Streaming Support

MCP supports streaming responses for long-running operations, enabling real-time feedback during tool execution.

## Production Considerations

### When MCP Works Well

- **Multi-framework environments**: Teams using different agent frameworks can share MCP servers
- **Tool reuse**: Build once, use across all agents
- **Ecosystem leverage**: Tap into 1000+ pre-built community servers
- **Standardization**: Organizations with existing tool infrastructure

### When MCP May Be Overkill

- **Single framework locked-in**: If you're committed to one framework, native integrations may be simpler
- **Highly custom tools**: Complex tools with non-standard interfaces may not fit MCP's schema
- **Latency-sensitive**: MCP adds ~50-100ms per call vs in-process function calls

## The Ecosystem Play

The real value of MCP isn't the protocol — it's the ecosystem. The [community registry](https://modelcontextprotocol.github.io/servers) means:

1. **For tool builders**: Build once, reach all frameworks
2. **For agent developers**: Access thousands of pre-built tools
3. **For enterprises**: Standardize on one tool integration layer

This mirrors how USB became successful: the protocol was secondary to the ecosystem of compatible devices.

## Related Concepts

- [[model-context-protocol]] — This page (redirect)
- [[crewai]] — CrewAI framework with MCP support
- [[langgraph]] — LangGraph with MCP integration
- [[agentic-ai]] — Agentic AI paradigm that MCP enables
- [[tool-calling]] — Function calling vs tool calling
- [[autogen]] — Microsoft's multi-agent framework with MCP
