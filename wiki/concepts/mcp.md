---
confidence: medium
last_verified: 2026-04-11
relationships:
  - 🔗 agent-frameworks (extracted)
  - 🔗 anthropic (inferred)
  - 🔗 openai (inferred)
  - 🔗 tools (inferred)
last_updated: 2026-04-11
tags:
  - AI
  - agents
  - protocol
  - tools
---

# MCP (Model Context Protocol)

> An open protocol for connecting AI models to external tools and data sources.

## Overview

MCP (Model Context Protocol) is an emerging standard — championed by Anthropic and adopted by OpenAI and others — that provides a standardized way for AI models to connect to external tools, data sources, and services. In 2026, MCP is becoming the "USB-C of AI agent tool integration."

## Key Features

- **Standardized tool interface** — Any tool can be used by any LLM that supports MCP
- **Bi-directional communication** — Tools can also push data back to the model
- **Growing ecosystem** — Pre-built MCP servers for popular services (Slack, GitHub, Notion, etc.)

## Why MCP Matters

Without MCP, each AI model has its own proprietary tool integration. MCP creates a shared standard:
- Model providers don't need custom integrations per tool
- Tool builders don't need custom code per model
- Result: Cross-platform tool ecosystem

## Related

- [[agent-frameworks]] — Frameworks that use MCP
- [[tools]] — Tools that MCP connects

## Resources

- [MCP Spec](https://modelcontextprotocol.io)
- [Anthropic MCP Documentation](https://docs.anthropic.com/en/docs/model-context-protocol)
