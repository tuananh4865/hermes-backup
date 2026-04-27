---
title: "Dify"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [ai-agents, open-source, langchain, workflow-automation]
related:
  - [[langgraph]]
  - [[crewai]]
  - [[open-source-ai-agents]]
  - [[agent-frameworks]]
  - [[n8n-workflow-automation]]
---

# Dify

> Dify is an open-source LLM app development platform combining AI workflow, RAG pipeline, agent capabilities, model management, and observability. Positioned as a self-hosted alternative to closed SaaS AI platforms.

## Overview

Dify (langgenius/dify on GitHub) is a production-ready platform for building LLM applications. It differentiates from framework-only approaches (LangGraph, CrewAI) by providing a complete application platform: visual workflow builder, built-in RAG pipeline, multi-agent orchestration, model gateway, and integrated observability via Opik and Langfuse.

**Key differentiator:** Unlike LangGraph (code-first) or CrewAI (role-based YAML), Dify provides a GUI-first experience suitable for teams that want to prototype AI workflows without heavy coding. The open-source model means you self-host — no vendor lock-in.

## Core Capabilities

### AI Workflow
Visual workflow builder for chaining LLMs, tools, and data transformations. Supports branching, loops, and parallel execution nodes.

### RAG Pipeline
Built-in retrieval-augmented generation pipeline with document ingestion, chunking strategies, and multiple retrieval modes (semantic search, hybrid, keyword).

### Agent Capabilities
Define agents with tools, memory, and decision-making logic through configuration rather than code. Supports function calling, ReAct patterns, and custom agent types.

### Model Management
Unified model gateway that connects to OpenAI, Anthropic, local LLMs (via Ollama/LM Studio), and custom providers. Switch models without changing application code.

### Observability
Integrated Opik (for tracing) and Langfuse (for evaluation) — critical for production monitoring of agentic systems.

## GitHub Status

- **Repository:** [langgenius/dify](https://github.com/langgenius/dify)
- **Status:** Active, growing community
- **License:** Apache 2.0
- **Self-hosted:** ✅ Yes — full control, no data leaving your infrastructure

## Comparison

| Dimension | Dify | LangGraph | CrewAI | n8n AI |
|-----------|------|-----------|--------|--------|
| Interface | GUI + Code | Code-first | YAML-first | GUI |
| Open Source | ✅ Full | ✅ Partial | ✅ Full | ❌ Closed |
| RAG Built-in | ✅ | ❌ | ❌ | Via nodes |
| Agent Types | Multiple | Flexible | Role-based | Tool-based |
| Self-host | ✅ | ✅ | ✅ | ❌ |
| Enterprise | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

## When to Use Dify

- **Teams without strong engineering** — GUI workflow builder lowers barrier
- **Self-hosted requirement** — full control, no data exposure
- **RAG-heavy applications** — built-in pipeline saves integration effort
- **Prototype to production** — visual prototyping with code export capability

## When to Prefer Alternatives

- **Complex custom logic** → LangGraph (code-first flexibility)
- **Business automation with roles** → CrewAI (role-based paradigm)
- **Workflow automation (non-LLM)** → n8n (broader automation ecosystem)

## Related Concepts

- [[open-source-ai-agents]] — broader landscape of open source AI agent platforms
- [[langgraph]] — code-first graph-based agent framework
- [[crewai]] — role-based multi-agent framework
- [[n8n-workflow-automation]] — general workflow automation (non-LLM-focused)
- [[agent-frameworks]] — comparison of all major frameworks

---

*Updated: 2026-04-16 — Research from AI Agent Trends 2026-04-16 deep research*
