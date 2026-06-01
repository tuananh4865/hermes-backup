# Harness Engineering — AI Agent Framework Design (2026)

> **Status:** Active research area (2026)
> **Source:** Deep research via Exa web search, NxCode guide, Medium, Reddit discussions

## What is Harness Engineering?

**Harness Engineering** = discipline thiết kế systems, constraints, feedback loops wrap quanh AI agents để chúng reliable trong production.

**Metaphor:**
- AI model = con ngựa (mạnh, nhanh)
- Harness = dây cương, yên, bàn đạp (kìm hãm và kiểm soát)
- Engineer = người cưỡi (ra chỉ thị)

**Không có harness** = agent chỉ là demo, hoạt động tốt trong lab nhưng fail trong production.

## 5 Core Pillars

| Pillar | Mô tả | Hermes Support |
|--------|-------|----------------|
| **1. Tool Orchestration** | Định nghĩa tools nào available, permissions, invocation flow | ✅ 60+ built-in tools, MCP integration |
| **2. Guardrails & Safety** | Permission boundaries, validation checks, rate limiting | ✅ `approvals.mode`, secret redaction, security plugins |
| **3. Error Recovery** | Retry logic, fallback strategies, self-verification loops | ✅ Checkpoints, hallucination recovery, zombie detection |
| **4. Observability** | Logging, token tracking, decision recording | ✅ Logs, session_search, `/usage`, insights |
| **5. Human-in-the-Loop** | Approval checkpoints, intervention points | ✅ `/approve`, `/deny`, checkpoint system |

## Key Insight

> "More constraints often yield more reliability" — OpenAI Codex team

**Proof:** LangChain coding agent: **52.8% → 66.5%** on Terminal Bench 2.0 **chỉ bằng cách improve harness** (self-verification loop + loop detection), KHÔNG thay đổi model.

## Problems Harness Engineering Solves

| Problem | Without Harness | With Harness |
|---------|-----------------|--------------|
| **Memory** | Agent forgets everything between sessions | 3-layer persistent memory |
| **Confident Mistakes** | Silent error propagation | Verification loops |
| **Unrestricted Access** | Agent can delete files, leak credentials | Permission boundaries + guardrails |
| **Scale** | 10 parallel agents = cascading failures | Structured environment + progress tracking |

## The Evolution (2022-2026)

```
2022: Prompt Engineering — craft perfect prompt
2023: Context Engineering — optimize context window
2024-2026: Harness Engineering — wrap agents để reliable
```

## Hermes Agent = Harness Engine

Hermes Agent v0.15+ là một harness engine hoàn chỉnh:

- **Memory 3 layers** — persistent identity, session FTS5, auto-generated skills
- **Worker agents** — Content-Creator, Research (multi-agent orchestration)
- **Cron jobs + heartbeat** — scheduled automation with monitoring
- **Checkpoints + rollback** — state persistence between sessions
- **Tool Search** (v0.15+) — progressive schema disclosure, accuracy 49% → 74% on Opus 4

## Related Concepts

- [[agentic-ai]] — Agentic AI levels and patterns
- [[multi-agent-orchestrator-patterns-deep-research]] — Multi-agent orchestration
- [[hermes-agent]] — Hermes as a harness engine

## Sources

- NxCode: "What Is Harness Engineering? Complete Guide for AI Agent Development (2026)" — March 26, 2026
- Philschmid: "The importance of Agent Harness in 2026" — January 5, 2026
- Bits-Bytes-NN: "From Prompts to Harnesses — Four Years of AI Agentic Patterns" — April 5, 2026
- Medium/Visrow: "Harness Engineering for AI Agents in 2026" — May 18, 2026