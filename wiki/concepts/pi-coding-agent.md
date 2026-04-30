---
title: Pi Coding Agent
created: 2026-04-30
updated: 2026-04-30
type: concept
tags: [agent, coding-agent, open-source, terminal]
confidence: high
relationships: [openclaw, claude-code, terminus, ai-agent-trends-2026-05]
---

# Pi Coding Agent

**Pi** là minimal terminal coding harness — một CLI agent được tạo bởi Mario Zechner (creator libGDX). Nổi tiếng vì là engine runtime của OpenClaw.

## Key Facts

- **Repo:** `badlogic/pi-mono` — 42K stars
- **npm downloads:** 2.3M/week (Apr 2026)
- **Growth:** 4K → 1.3M → 2.3M weekly downloads trong 6 tháng
- **License:** MIT
- **Language:** TypeScript

## Design Philosophy

**4 core tools:** read, write, edit, bash. System prompt <1,000 tokens.

Mario's thesis: *"All frontier models have been RL-trained up the wazoo, so they inherently understand what a coding agent is."*

Pi **không có built-in:** sub-agents, plan mode, permission popups, MCP, background bash. Tất cả có thể được build thông qua TypeScript extensions.

## Why Pi Went Viral

1. **OpenClaw engine** — Pi là runtime của OpenClaw (358K stars, fastest-growing GitHub repo)
2. **Minimalism** — counter-trend với bloat của Claude Code và competitors
3. **Extensibility** — TypeScript extensions with hot-reload, agent có thể tự viết extensions
4. **Model freedom** — 15+ providers, 324 models, bao gồm MiniMax

## Architecture

- **Monorepo:** pi-ai (LLM API), pi-agent-core (runtime), pi-coding-agent (CLI), pi-tui (UI library)
- **Modes:** Interactive, Print/JSON, RPC, SDK
- **Sessions:** Tree-structured với branching, forking, compacting

## Providers Supported

Anthropic, OpenAI, Google, xAI, Mistral, Groq, Cerebras, Hugging Face, OpenRouter, Ollama, Azure, Bedrock, **MiniMax**, Kimi For Coding.

## Related

- [[openclaw]] — Viral project sử dụng Pi làm engine
- [[claude-code]] — Agent đối thủ, "batteries included" approach
- [[terminus]] — Minimal terminal harness competitor on Terminal-Bench
- [[ai-agent-trends-2026-05]] — Agent landscape trends 2026
