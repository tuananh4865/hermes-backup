---
title: AI Engineering Roadmap
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ai-engineering, roadmap, career, learning, llm]
sources: [raw/articles/ai-engineering-roadmap-6-months-deronin.md]
confidence: high
relationships: [[AI-Agents], [Prompt-Engineering], [RAG], [LLM-Engineering], [FastAPI], [Docker], [LangChain]]
---

# AI Engineering Roadmap

## Overview

A comprehensive 6-month learning path for becoming a hireable AI engineer, written by [@deronin_](https://x.com/deronin_) and [@andy_ai0](https://x.com/andy_ai0). The roadmap focuses on **building real products with existing LLMs**, not training models from scratch.

The core philosophy: learn by building every single month. Tutorials without projects = surface-level knowledge that doesn't transfer to real jobs.

## Core Distinction: AI Engineer vs ML Researcher

| ML Researcher | AI Engineer |
|--------------|-------------|
| Train models from scratch | Build products on top of existing LLMs |
| Heavy math/theory focus | Practical shipping focus |
| Rare role | High demand role |

AI engineers sit between software engineering, product engineering, automation, and applied AI.

## The 6-Month Path

### Month 1: Python & Fundamentals

Goal: Functional Python developer who can write clean code, use Git, navigate terminal, call APIs.

**Resources:**
- [[Python]] — Python for Everybody (Coursera), freeCodeCamp, CS50P
- [[Git]] — GitHub Skills, Learn Git Branching
- [[FastAPI]] — official tutorial (one of the best framework docs ever written)
- CLI basics, JSON/HTTP/APIs, basic SQL + Pandas

**Key insight:** AI engineering is first and foremost software engineering. This month is the foundation everything else builds on.

### Month 2: LLM App Development

Goal: Build real AI-powered apps with OpenAI and Anthropic APIs.

**Core skills:**
- [[Prompt Engineering]] — specificity, chain-of-thought, few-shot
- Structured Outputs (JSON schemas via Instructor/Pydantic)
- [[Function Calling|Tool Calling]] — the skill that transforms LLMs into agents
- Streaming responses (word-by-word vs waiting for full response)
- Conversation state (LLMs are stateless — you manage history)

**Resources:** Anthropic prompt engineering tutorial, OpenAI docs, PromptingGuide.ai, Instructor library

### Month 3: Backend, Data, and RAG

Goal: Build complete AI-powered backend systems with your own data.

**Core skills:**
- [[RAG]] — Retrieval Augmented Generation: chunking, indexing, retrieval, synthesis
- Vector databases: Chroma, Qdrant, Pinecone
- Embedding models
- [[LangChain]] (use with caution — understand what's underneath)
- LlamaIndex
- SQL + relational data with AI

**Key insight:** Most real AI products need access to specific data. RAG is how you give LLMs that access without fine-tuning.

### Month 4: AI Agents

Goal: Build systems that autonomously take actions using tools.

**Core skills:**
- [[AI Agents]] loop: perception → reasoning → action
- Writing good tool descriptions (determines whether agents select correctly)
- Multi-agent systems
- [[LangGraph]] for stateful agent orchestration
- Failure modes in agent systems (infinite loops, tool call errors, hallucinated function names)
- Evaluating agents: RAGAs, DeepEval, LLM-as-judge

**Key insight:** Agents are just loops — the hard part is making them reliable and handling failures gracefully.

### Month 5: Production & Reliability

Goal: Ship apps that survive real traffic, real users, real failures.

**Core skills:**
- [[FastAPI]] production: Gunicorn workers, health checks, CORS, async DB sessions
- [[Docker]] containerization
- Background jobs (Celery) — LLM calls are slow, don't block responses
- Auth + API key security (OWASP API Security Top 10)
- Observability: Langfuse, LangSmith for tracing every LLM call
- Prompt versioning + rollback
- Cost monitoring (Helicone, LiteLLM)
- Caching: Redis, GPTCache for semantic caching

**Key insight:** Demo-quality is easy. Production-quality is what companies pay for. This month separates hobbyists from professionals.

### Month 6: Specialization

Choose one of three directions based on your goals:

**1. AI Product Engineer** — startups, consumer/developer tools
- Vercel AI SDK, Streamlit, Gradio
- Product UX for AI (handling errors, loading states, probabilistic output)
- Focus: ship products people use

**2. Applied ML / [[LLM-Engineering]]** — deeper technical roles
- Fine-tuning (when to use vs prompt engineering + RAG)
- Open-source models: Ollama, [[vLLM]], HuggingFace
- Inference optimization: quantization, batching, KV-cache
- Focus: model performance and efficiency

**3. AI Automation Engineer** — business operations, consulting
- n8n, [[LangGraph]], Temporal
- Business process automation
- CRM, docs, email, support automation
- Focus: solving specific expensive business problems

## Salary Data (US, March 2026)

| Level | Salary |
|-------|--------|
| Junior | $90K-$130K |
| Mid (3-5yr) | $155K-$200K |
| Senior | $195K-$350K+ |
| **Average** | **$184,757** |

**Freelance rates:** $125-$300/hour depending on specialization

**Consulting:** $300-$5,000 per AI agent setup, $500-$4,000/month for ongoing automation

## Key Principles

1. **Build, don't just study** — every month should produce a working project on GitHub
2. **Share publicly** — opportunities come from visibility, not job applications
3. **Don't wait to be "ready"** — the gap between "learning" and "building" is where people get stuck
4. **Ship imperfect products** — the market rewards people who ship, not perfectionists
5. **Evals are not optional** — every prompt change or model swap without evals is a gamble

## Related Concepts

- [[AI Agents]] — autonomous systems that perceive, reason, and act
- [[Prompt Engineering]] — crafting instructions for consistent LLM outputs
- [[RAG]] — giving LLMs access to external knowledge
- [[Function Calling|Tool Calling]] — enabling LLMs to use external tools and APIs
- [[LangChain]] — orchestration framework (use with caution)
- [[LangGraph]] — stateful agent workflows
- [[FastAPI]] — the standard API framework for LLM apps
- [[Docker]] — containerization for production deployments
- [[LLM-Engineering]] — the broader discipline this roadmap feeds into
