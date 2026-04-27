---
title: "MCP Servers — Model Context Protocol"
created: 2026-04-15
type: concept
tags: [mcp, model-context-protocol, ai-tools, anthropic, tool-integration]
related:
  - [[ai-agents]]
  - [[agent-frameworks]]
  - [[tool-calling]]
  - [[langgraph]]
---

# MCP Servers — Model Context Protocol

## What is MCP?

The **Model Context Protocol (MCP)** is an open standard introduced by Anthropic in November 2024 that standardizes how AI models connect to external tools, data sources, and services. Think of it as "USB-C for AI" — a universal interface that works across any MCP-compatible AI application and tool server.

## Why MCP Matters

Traditional tool calling requires hard-coding each AI model's tool schemas. MCP decouples this:

- **Before MCP**: Every AI app needed custom integrations for GitHub, Slack, etc.
- **With MCP**: One server implementation works with all MCP-compatible clients

## Official MCP Servers (Reference Implementation)

Anthropic maintains a [GitHub repository](https://github.com/modelcontextprotocol/servers) with 15+ official MCP servers:

| Server | Purpose | Tools |
|--------|---------|-------|
| **GitHub MCP** | Code intelligence | Read issues, PRs, code review |
| **Filesystem MCP** | Local file operations | Read/write/list directories |
| **Brave Search MCP** | Web search | Search with citations |
| **Slack MCP** | Team communication | Post messages, read channels |
| **PostgreSQL MCP** | Database queries | SQL execution |
| **Memory MCP** | Persistent agent memory | Store/recall knowledge |

## Top MCP Servers for AI Developers (2026)

Based on testing and comparison:

### 1. Taskade MCP — Best for Workspace Data
- 22+ tools, OAuth scopes, 100+ integrations
- Best for team and workspace automation
- **Use case**: Project management automation, team workflows

### 2. GitHub MCP (Official) — Best for Code
- Direct GitHub API access
- Issue tracking, PR management, code search
- **Use case**: Automated code review, issue creation

### 3. Brave Search MCP — Best for Research
- Web search with source citations
- Grounded responses with links
- **Use case**: AI research agents, fact-checking

### 4. Slack MCP — Best for Communication
- Channel reading, message posting
- Thread management
- **Use case**: Team notification agents

## MCP Architecture

```
┌─────────────┐     MCP Protocol      ┌──────────────┐
│   AI Model  │ ◄───────────────────► │  MCP Client  │
│  (Claude,   │   Tool schemas +      │  (Cursor,    │
│   GPT-4o)   │   results            │   Claude Code)│
└─────────────┘                       └──────┬───────┘
                                             │
                                    Standard protocol
                                             │
                    ┌────────────────────────┼────────────────┐
                    ▼                        ▼                ▼
             ┌──────────┐           ┌────────────┐    ┌──────────┐
             │  GitHub  │           │  Slack     │    │ Filesystem│
             │   MCP    │           │    MCP     │    │   MCP    │
             └──────────┘           └────────────┘    └──────────┘
```

## MCP vs Traditional Tool Calling

| Aspect | MCP | Traditional Tool Calling |
|--------|-----|-------------------------|
| Schema definition | Standardized JSON | Custom per model |
| Server implementation | One implementation | N×M combinations |
| Security | Sandboxed, scoped | Depends on implementation |
| Discovery | Protocol-based | Documentation-dependent |
| Use cases | Data sources, APIs | Custom functions |

## Getting Started

### 1. Install an MCP server
```bash
# Using Claude Desktop
claude mcp add github -- npx @modelcontextprotocol/server-github

# Or build your own
npm create mcp-server@latest
```

### 2. Connect to Claude Code / Cursor
MCP clients (Claude Code, Cursor) auto-discover configured servers.

### 3. Use in your AI workflow
The AI model decides when to use tools — no prompt engineering needed.

## Resources

- [Official MCP GitHub](https://github.com/modelcontextprotocol/servers)
- [MCP Wikipedia](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [Taskade MCP Comparison](https://www.taskade.com/blog/mcp-servers)

## Related Concepts

- [[ai-agents]] — AI agents that use MCP tools
- [[agent-frameworks]] — LangGraph, CrewAI, AutoGen
- [[tool-calling]] — LLM function calling mechanics
- [[langgraph]] — Graph-based agent orchestration
