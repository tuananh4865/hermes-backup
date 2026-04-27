---
title: "Harrison Chase"
created: 2026-04-12
updated: 2026-04-12
type: entity
tags: [person, langchain, ai-agent]
sources:
  - raw/articles/your-harness-your-memory.md
---

# Harrison Chase

## Overview

**Full Name**: Harrison Chase
**Twitter**: [@hwchase17](https://x.com/hwchase17)
**Role**: CEO of LangChain
**Bio**: MLOps ∪ Generative AI ∪ sports analytics

LangChain is the company behind LangGraph and LangSmith — major frameworks for building agentic applications.

## Key Work

### Your Harness, Your Memory (2026-04-11)

- **Source**: https://blog.langchain.dev/your-harness-your-memory/
- **Summary**: Agent harnesses đang trở thành dominant way to build agents. Memory không phải separate service — nó integral part của harness. Closed harness + proprietary memory = vendor lock-in thực sự.

**Core Arguments**:
1. Harness ≠ Model — model providers đang lấn sân vào harness territory
2. Memory Is Part of the Harness — short-term và long-term memory đều do harness quản lý
3. Lock-In Problem — mildly bad (stateful API) → bad (closed harness) → worse (memory in API)
4. Why Providers Want Lock-In — memory = proprietary dataset = competitive moat
5. Industry Is Still Early — long-term memory thường NOT part of MVP

**Key Quote**: "Memory - and therefor harnesses - should be open, so that you own your own memory"

### Generative Agents (2023)

LangChain implementation của "Generative Agents" paper (Park et al.) — tập trung vào long-term, reflection-based memory system.

### Deep Agents (2025)

Release 0.2 với "backend" abstraction — cho phép swap filesystem (local, database, remote VM, anything).

## Relationships

- Works at: [[langchain]] (company)
- Related concepts: [[your-harness-your-memory]], [[agentic-graphs-workflows]]

## References

- https://x.com/hwchase17
- https://blog.langchain.dev/your-harness-your-memory/
