---
title: Deep Research — Karpathy LLM Knowledge Bases + Agentic Workflows / Agentic Graphs
created: 2026-04-10
updated: 2026-04-10
type: concept
tags: [deep-research, llm-wiki, agentic-workflows, acp, research]
---

# Deep Research Report

**Date:** 2026-04-10  
**Topics:** Karpathy LLM Knowledge Bases, Agentic Workflows / Agentic Graphs  
**Sources:** 42 + 50 unique results via Tavily Search  
**Method:** Multi-query Tavily search (15-50 results per topic), Jina content extraction

## Executive Summary

Hai insights từ mạng xã hội hôm nay reveal hai xu hướng quan trọng:

1. **LLM Wiki Pattern** (Karpathy) — LLM làm compiler thay vì RAG retrieval
2. **Agentic Workflows / Agentic Graphs** (Onur/acpx) — Node-based deterministic workflows > single prompt (tránh LLM priming)

---

## Part 1: Karpathy LLM Knowledge Bases

### Tổng hợp từ 42 sources

#### Core Concept

Karpathy's LLM Wiki = LLM "compiles" raw documents vào markdown wiki structure thay vì dùng RAG retrieval.

**Stack:**
- Raw data: articles, papers, repos, datasets, images trong `raw/`
- LLM compiler: biến raw → compiled wiki (.md files)
- Obsidian: IDE frontend để view
- LLM tự viết và maintain wiki, human hiếm khi touch trực tiếp

### Key Implementations Found

| Source | Content |
|--------|---------|
| [Dume AI Blog](https://www.dume.ai/blog/what-is-andrej-karpathys-llm-wiki-how-to-get-the-same-results) | Complete guide đến Karpathy's workflow |
| [MindStudio](https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base) | Step-by-step implementation |
| [Medium - Balu Kosuri](https://medium.com/@k.balu124/i-used-karpathys-llm-wiki-to-build-a-knowledge-base-that-maintains-itself-with-ai) | Case study: building self-maintaining KB |
| [Karpathy GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Original idea file (442 stars) |
| [DAIR.AI Academy](https://academy.dair.ai/blog/llm-knowledge-bases-karpathy) | Educational breakdown |

### Why LLM Wiki > Traditional RAG

> "Instead of repeatedly searching raw documents, the idea behind LLM Wiki is: Let the LLM do the compilation work ahead of time." — Mehul Gupta, Medium

**RAG problems LLM Wiki solves:**
- Semantic search limitations
- Context window constraints
- Retrieval quality degradation
- No synthesis/inference on raw data

**LLM Wiki advantages:**
- LLM maintains index files và brief summaries
- Auto-generates backlinks và cross-references
- Queries answered from compiled wiki (not raw docs)
- Wiki "grows" through use — explorations always "add up"

### Implementation Steps (from research)

1. **Collect raw data** — articles, papers, repos, images
2. **LLM compile** — convert raw → .md wiki structure
3. **Auto-maintain** — LLM updates index, summaries, links
4. **Query** — ask complex questions against wiki
5. **Output** — markdown, slides (Marp), matplotlib images
6. **File back** — outputs enhance wiki for future queries

### Obsidian Integration

- [Obsidian Web Clipper](https://obsidian.md/) — convert web articles
- Download images locally cho LLM reference
- Plugins: Marp for slides, various visualization plugins
- View raw data + compiled wiki + visualizations in one place

---

## Part 2: Agentic Workflows / Agentic Graphs

### Tổng hợp từ 50 sources

#### Core Concept

**"Agentic Graphs"** = Node-based workflows on top of ACP (Agent Client Protocol) để drive coding agents qua deterministic steps.

**Key insight từ Onur:**
> "LLMs are prone to PRIMING. Putting all steps in the same prompt at the beginning gives suboptimal results compared to revealing intention step by step."

### ACP (Agent Client Protocol)

| Resource | URL |
|----------|-----|
| Official Docs | https://agentclientprotocol.com |
| LangChain Implementation | https://docs.langchain.com/oss/python/deepagents/acp |
| GitHub | https://github.com/agentclientprotocol |

**What ACP is:**
- Open standard for communication between code editors and AI coding agents
- Like LSP (Language Server Protocol) but for AI agents
- Enables interoperability between editors (Zed, VS Code, JetBrains) và agents (Codex, Claude Code, Goose)

**Why it matters:**
- Agents built on ACP can work with ANY editor that supports it
- Not locked into one