---
title: AI Agent Frameworks Comparison 2026
created: 2026-05-15
type: reference
tags: [ai-agent, langchain, crewai, autogen, comparison, benchmark]
confidence: high
---

# AI Agent Frameworks Comparison 2026

*Research from May 15, 2026 session. Sources: agntdev.com, bananalabs.io, fungies.io, dasroot.net, multiple blog posts.*

## Overall Scores

| Framework | Score | GitHub Stars | Latency | Token Overhead | Best For |
|-----------|-------|-------------|---------|----------------|----------|
| **LangGraph** | 44/50 | ~130K | ~1.2s | ~5% | Complex workflows, enterprise RAG |
| **CrewAI** | 38/50 | ~46K | ~1.8s | ~18% | Rapid prototyping, startups |
| **AutoGen** | 35/50 | ~55K | ~2.1s | ~24% | Research, conversational agents |

> **AutoGen warning**: 6 months since last stable release (Sep 2025), 684 open issues. Microsoft pushing toward Agent Framework.

## Key Benchmarks

| Metric | LangGraph | CrewAI | AutoGen |
|--------|-----------|--------|---------|
| Task Success Rate | 87% | 82% | 85% |
| Lines of Code (minimal) | ~80 | ~35 | ~40 |
| Memory per Agent | ~45MB | ~90MB | ~85MB |
| Cost per Query | ~$0.10 | ~$0.12 | ~$0.35 |
| Concurrent Agents | 100+ | 10-20 | Excellent |

## When to Use Each

| Use Case | Recommendation |
|----------|---------------|
| Complex stateful workflows | LangGraph |
| Fast MVP / business automation | CrewAI |
| Research / code execution | AutoGen |
| Production enterprise + LangSmith | LangGraph |
| Startups / SMBs | CrewAI |
| Conversational multi-agent | AutoGen |

## Self-Improving Agent Tools Found

### 1. Cognify (GenseeAI)
Auto-tunes LangChain/LangGraph/DSPy programs.
- **2.8x quality improvement**
- **10x cost reduction**
- **2.7x latency reduction**

```bash
cognify optimize /your/ai/agent.py
```

### 2. autoresearch-agents (hwchase17)
Karpathy-style autonomous agent optimization using LangSmith.
- agent.py + run_eval.py + dataset.json → autonomous iteration
- Edit agent code → run evals → keep improvements

### 3. self-evolving-codegen (tathadn)
5-agent pipeline with self-evolution engine:
- Evaluator (Haiku) → scores each test
- Analyzer (Sonnet) → diagnoses failure patterns
- Evolver (Sonnet) → rewrites Tester prompt
- Tracker → JSON persistence with rollback

**Gen 0→Gen 1: 0.506→0.921** overall score.

### 4. Autogenesis (DVampire)
RSPL (Resource Substrate Protocol Layer) + SEPL (Self Evolution Protocol Layer).
- Explicit versioning + rollback for agent systems
- Models prompts/agents/tools/memory as protocol-registered resources

## Key Insights

1. **All frameworks converging on MCP** for tool integration
2. **LangGraph wins on raw score** but CrewAI's 38/50 is more useful for small teams
3. **AutoGen maintenance risk is real** — 6 months silent, 684 open issues
4. **Cognify** offers biggest ROI for workflow optimization (2.8x quality, 10x cheaper)
5. **Self-evolution patterns** (evaluator→analyzer→evolver→tracker) are mature enough to apply to Hermes skills

## Sources
- agntdev.com/langchain-vs-crewai-vs-autogen-2026-honest-comparison
- bananalabs.io/blog/langchain-vs-crewai-vs-autogen
- fungies.io/ai-agent-frameworks-comparison-2026-langchain-crewai-autogen
- dasroot.net/posts/2026/04/llm-agent-frameworks-langchain-crewai-autogen-comparison
- github.com/hwchase17/autoresearch-agents
- github.com/tathadn/self-evolving-codegen
- github.com/DVampire/Autogenesis
- tinyurl.com/2tp9bndr (Cognify)
