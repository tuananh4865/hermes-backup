---
confidence: high
last_verified: 2026-04-18
relationships:
  - [[mcp-servers]]
  - [[mcp-model-context-protocol]]
  - [[agent-frameworks]]
  - [[agentic-ai]]
  - [[tools]]
  - [[anthropic]]
  - [[langgraph]]
  - [[crewai]]
  - [[n8n-agentic-ai]]
  - [[apple-silicon-local-llm-agents-2026]]
relationship_count: 11
sources: 10
---

# Model Context Protocol (MCP)

## What is MCP?

**Model Context Protocol (MCP)** is Anthropic's open standard for connecting AI agents to external tools, data sources, and services. Think of it as **"USB-C for AI agents"** — a standardized interface that lets any MCP-compatible agent connect to any MCP-compatible server, regardless of who built either side.

MCP addresses a fundamental problem: every AI agent framework historically required custom integrations for each tool. An agent built in LangGraph couldn't easily use tools built for CrewAI. MCP creates a universal adapter layer.

> "Model Context Protocol is an open standard that enables AI models to connect with external tools and data sources in a standardized way." — Anthropic documentation

---

## Core Architecture

### Three Components

1. **MCP Hosts** — AI applications that run agents and need to connect to tools
   - Examples: Claude Desktop, LangGraph agents, CrewAI crews, custom agents
   - Consumes: MCP clients that implement the protocol

2. **MCP Clients** — Protocol clients embedded within hosts
   - Maintains 1:1 connection with MCP servers
   - Handles protocol negotiation, message routing

3. **MCP Servers** — Lightweight programs that expose specific tools via MCP
   - Each server exposes one domain (e.g., GitHub, Slack, filesystem)
   - Communicate via JSON-RPC over stdio or HTTP+SSE

### Communication Pattern

```
┌─────────────┐     MCP Protocol      ┌──────────────┐
│ MCP Host    │◄───────────────────►│ MCP Server   │
│ (Agent app) │   JSON-RPC messages  │ (GitHub etc) │
└─────────────┘                       └──────────────┘
```

**Transport options:**
- **stdio** — Local processes, simple setup
- **HTTP + SSE** — Remote servers, better for production

---

## Official MCP Servers

The `modelcontextprotocol/servers` GitHub repo (github.com/modelcontextprotocol/servers) provides official server implementations:

| Server | Purpose | Repository |
|--------|---------|-----------|
| **Filesystem** | Read/write local files | modelcontextprotocol/servers |
| **GitHub** | Issues, PRs, repos | modelcontextprotocol/servers |
| **Slack** | Messaging integration | modelcontextprotocol/servers |
| **PostgreSQL** | Database queries | modelcontextprotocol/servers |
| **Google Maps** | Location services | modelcontextprotocol/servers |
| **Memory** | Persistent agent memory | modelcontextprotocol/servers |

**Universal availability:** MCP servers run on macOS, Linux, and Windows.

---

## MCP vs Traditional Tool Integration

| Aspect | MCP | Custom Tool Integration |
|--------|-----|------------------------|
| **Standardization** | Universal protocol | Per-framework |
| **Tool reuse** | Any MCP server with any MCP client | Framework-specific only |
| **Discovery** | Protocol-based | Manual configuration |
| **Security** | Sandboxed, permission-based | Varies |
| **Ecosystem** | Growing rapidly (2024-2026) | Established but fragmented |

### Key Advantages

- **Vendor neutrality** — Built by Anthropic but usable by any AI provider
- **Tool composability** — Chain MCP servers together (GitHub + Slack = automated PR summaries)
- **Security model** — Servers run locally, explicit permission grants
- **Debugging** — Protocol is inspectable, JSON-RPC is human-readable

---

## MCP in Agent Frameworks

### LangGraph + MCP

LangGraph agents can connect to MCP servers for tool access. The pattern:

```python
from langgraph.prebuilt import create_react_agent
from langchain_mcp import MCPToolPool

# Connect to MCP filesystem server
mcp_tools = MCPToolPool(["python -m langchain_mcp.servers.filesystem"])

# Use in agent
agent = create_react_agent(model, mcp_tools)
```

### CrewAI + MCP

CrewAI supports MCP as a tool source via `crewai.tools` integration.

### n8n + MCP

n8n's agentic AI nodes support MCP for workflow automation — agents can trigger n8n workflows via MCP protocol.

---

## MCP and the Agent Ecosystem

### Why MCP Matters for AI Agents

1. **Interoperability** — LangGraph agent can use a CrewAI tool without rewriting
2. **Tool marketplace** — One MCP server works with Claude, LangChain, CrewAI, etc.
3. **Security** — Sandboxed execution with explicit permissions
4. **Simplicity** — Tool developers write one server, not one per framework

### Growing Adoption (2025-2026)

- **Anthropic** — Primary sponsor, MCP built into Claude API
- **LangChain** — First-class MCP support in LangChain tools
- **CrewAI** — MCP tool integration in official docs
- **OpenAI** — Considering MCP in Agents SDK roadmap
- **n8n** — MCP nodes in workflow automation
- **GitHub** — Official MCP server for GitHub API access

---

## Setting Up MCP Servers

### Quick Start

```bash
# Install a popular MCP server
npm install -g @modelcontextprotocol/server-filesystem

# Or use Python servers
pip install mcp-server-filesystem
```

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "/path/to/dir"]
    }
  }
}
```

### Security Model

- **Local execution** — MCP servers run as local processes
- **Permission prompts** — Claude Desktop prompts before tool use
- **Sandboxing** — Each server has limited filesystem/API access
- **No remote code** — Servers cannot execute arbitrary code on your machine

---

## MCP Server Development

### Minimal MCP Server (Python)

```python
from mcp.server import MCPServer
from mcp.types import Tool

server = MCPServer(name="my-server")

@server.tool()
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"The weather in {city} is sunny."

server.run()
```

### Tool Definition Schema

MCP uses a typed schema for tools:

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  "inputSchema": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "City name"
      }
    },
    "required": ["city"]
  }
}
```

---

## Resources

- **Official:** github.com/modelcontextprotocol
- **Specification:** modelcontextprotocol.io
- **Servers:** github.com/modelcontextprotocol/servers
- **SDKs:** Python, TypeScript, Rust official SDKs

---

## Related Concepts

- [[mcp-servers]] — MCP server implementations
- [[mcp-model-context-protocol]] — Alternative reference page
- [[agent-frameworks]] — LangGraph, CrewAI, AutoGen
- [[agentic-ai]] — Agent architecture and patterns
- [[anthropic]] — MCP origin/primary sponsor
- [[tools]] — Agent tools in general
- [[langgraph]] — LangGraph + MCP integration
- [[crewai]] — CrewAI + MCP integration
- [[n8n-agentic-ai]] — n8n workflow automation + MCP

---

*Research compiled: 2026-04-18 | Sources: 10 web sources*
