---
title: "Your Harness, Your Memory"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [agent, memory, langchain, harness, vendor-lock-in]
sources:
  - raw/articles/your-harness-your-memory.md
confidence: high
relationships:
  - entities/harrison-chase
  - karpathy-llm-wiki-architecture
  - agentic-graphs-workflows
  - ai-agent-infrastructure-2026
---

# Your Harness, Your Memory

**Author**: [[harrison-chase]] (CEO of LangChain)
**Date**: April 11, 2026
**Source**: https://blog.langchain.dev/your-harness-your-memory/

---

## Summary

Agent harnesses (framework như LangChain, LangGraph) đang trở thành cách dominant để build agents. Memory không phải là separate service — nó là integral part của harness. **Closed harness + proprietary memory = vendor lock-in thực sự.**

---

## Core Arguments

### 1. Harness ≠ Model

Khi OpenAI/Anthropic build web search vào API của họ, đó không phải "part of the model". Đó là lightweight harness ngồi sau API, orchestrate model với tool calling. **Model providers đang lấn sân vào harness territory.**

### 2. Memory Is Part of the Harness

Memory = một form của context:
- **Short-term memory**: Messages in conversation, large tool call results → handled by harness
- **Long-term memory**: Cross-session memory → needs to be updated and read by harness

> "Ultimately, how the harness manages context and state in general is the foundation for agent memory." — Sarah

### 3. The Lock-In Problem

| Level | Lock-In | Risk |
|-------|---------|------|
| Mildly bad | Stateful API (OpenAI Responses API, Anthropic server-side compaction) | Can't swap models and resume threads |
| Bad | Closed harness (Claude Agent SDK) | Zero visibility into memory, don't know data structure, don't own memory |
| Worse | Model provider builds memory into API | Loss leader — get you in via model, lock you in via memory |

### 4. Why Model Providers Want Lock-In

- Memory tạo proprietary dataset: user interactions + preferences
- Dataset này = competitive advantage
- Switch model = lose all memory = lose everything built up over time
- Stateless model APIs dễ switch, nhưng stateful (có memory) thì không

### 5. Industry Is Still Early

- Memory as a concept: still in infancy
- Long-term memory thường NOT part of MVP
- Chưa có well-known abstractions cho memory
- Vẫn đang figure out best practices

---

## The Email Assistant Story

Harrison có một email assistant được build trên Fleet (no-code platform). Nó có memory tích lũy theo thời gian — preferences, tone, habits.

Agent bị xóa accident → tạo lại từ same template → experience tệ hơn nhiều. Phải re-teach mọi thứ.

**Insight**: Khi mất memory, mới realize được nó valuable và sticky như thế nào.

---

## Key Takeaways

1. **Chọn open harness** — có visibility và control vào memory architecture
2. **Own your memory** — đừng để third-party control agent's memory
3. **Memory = competitive moat** — proprietary dataset của user interactions
4. **Watch for lock-in** — model providers incentivized để build lock-in qua memory
5. **Wiki-based memory** (như Karpathy approach) = một cách để own memory

---

## Implications for Wiki-Based Agent Memory

[[karpathy-llm-wiki-architecture]] approach align với Harrison's argument:
- Wiki = open, owned memory system
- Không phụ thuộc proprietary harness
- Memory layer tách rời khỏi model provider

---

## Related

- [[harrison-chase]] — Author (CEO of LangChain)
- [[karpathy-llm-wiki-architecture]] — Wiki-based open memory
- [[agentic-graphs-workflows]] — LangGraph agent patterns
- [[ai-agent-infrastructure-2026]] — Agent infrastructure stack
