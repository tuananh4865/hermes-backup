---
title: Deep Research — Karpathy LLM Knowledge Bases + Agentic Workflows
date: 2026-04-10
tags: [deep-research, llm-wiki, agentic-workflows, acp, research]
---

# Deep Research Report

**Date:** 2026-04-10  
**Topics:** Karpathy LLM Knowledge Bases, Agentic Workflows / Agentic Graphs  
**Sources:** 42 + 50 unique results via Tavily Search  
**Method:** Multi-query Tavily search (15-50 results per topic), Jina content extraction

---

## Executive Summary

Hai insights từ mạng xã hội hôm nay reveal hai xu hướng quan trọng:

1. **LLM Wiki Pattern** (Karpathy) — LLM làm compiler thay vì RAG retrieval
2. **Agentic Workflows / Agentic Graphs** (Onur/acpx) — Node-based deterministic workflows > single prompt (tránh LLM priming)

---

# Part 1: Karpathy LLM Knowledge Bases

## Tổng hợp từ 42 sources

### Core Concept

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

# Part 2: Agentic Workflows / Agentic Graphs

## Tổng hợp từ 50 sources

### Core Concept

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
- Not locked into one specific tool
- Deterministic workflows become portable

### Node-Based Workflows > Single Prompt

**Problems with single prompt:**
1. **LLM Priming** — Initial context biases model throughout
2. **No observability** — Can't monitor intermediate steps
3. **No mid-course correction** — Can't adjust based on intermediate results
4. **Hard to debug** — No structured data at each step

**Benefits of node-based:**
1. **Step-by-step revelation** — Each step revealed sequentially
2. **Structured outputs** — JSON at end of each step
3. **Observability** — Monitor thousands of agents via dashboard
4. **Mid-course correction** — Can adjust based on step outputs
5. **Deterministic** — Repeatable, auditable
6. **Workflow tuning** — Markdown/Mermaid spec → TypeScript API

### PR Triage Example (from Onur)

OpenClaw receives 300~500 PRs/day. Workflow:
```
1. Extract intent
2. Cluster by intent
3. Validate proposed changes
4. If low quality → close with feedback
5. Run AI review
6. Address review issues
7. Refactor if needed
8. Resolve conflicts
```
**Result:** Maintainer only sees PRs ready for decision (merge/feedback/takeover).

### Similar Tools Found

| Tool | Notes |
|------|-------|
| [n8n](https://n8n.io/) | General automation with AI nodes |
| [LangFlow](https://www.langflow.org/) | LangGraph-based visual workflow builder |
| [acpx](https://github.com/onurzSrl/acpx) | Node-based workflows + ACP integration |
| [LangChain Agents](https://docs.langchain.com/docs/concepts/agents/) | Multi-step agentic workflows |

---

## Key Comparisons

| Aspect | Single Prompt | Agentic Workflows |
|--------|--------------|------------------|
| LLM Priming | High risk | Eliminated |
| Observability | Low | High (structured JSON per step) |
| Debugging | Difficult | Easy (per-step logs) |
| Scalability | Limited | Dashboard for 1000s of agents |
| Repeatability | Variable | Deterministic |
| Mid-course correction | No | Yes |

---

## Implications for Our Wiki Agent

### 1. Cron Job Workflow

**Current approach (single large prompt):**
- Risk of LLM priming
- Hard to monitor progress
- Difficult to debug

**Recommended: Node-based approach**
- Phase 1: Research (separate step)
- Phase 2: Synthesis (separate step)
- Phase 3: Planning (separate step)
- Phase 4: Execution (separate step)
- Each step produces structured JSON output

### 2. ACP Integration

- Consider ACP for driving sub-agents
- Would give us structured outputs + observability
- Compatible with Claude Code, Codex, Goose

### 3. LLM Wiki Integration

- Our wiki already follows similar pattern
- Could adopt Karpathy's compiler approach
- LLM writes/maintains wiki content

---

## Action Items

- [ ] Evaluate ACP integration for our sub-agent system
- [ ] Consider node-based cron job workflow (replaces single prompt)
- [ ] Adopt LLM compiler pattern for wiki updates
- [ ] Add observability dashboard for monitoring agents

---

## Sources

### Karpathy LLM Wiki
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f (original gist)
- https://www.mindstudio.ai/blog/andrej-karpathy-llm-wiki-knowledge-base
- https://academy.dair.ai/blog/llm-knowledge-bases-karpathy
- https://medium.com/data-science-in-your-pocket/andrej-karpathys-llm-wiki-bye-bye-rag

### Agentic Workflows / ACP
- https://agentclientprotocol.com/get-started/introduction
- https://docs.langchain.com/oss/python/deepagents/acp
- https://github.com/agentclientprotocol
- https://x.com/onusoz/status/2038565725690900992 (original post)

---

*Report generated via deep-research skill with Tavily Search (42+50 unique sources)*
