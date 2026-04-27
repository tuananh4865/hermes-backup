---
title: "Open Felix"
description: "Free, open source local AI agent for Apple Silicon powered by MLX. No cloud, no subscription, no limits."
tags: [apple-silicon, mlx, local-ai, open-source, agent]
sources: [openfelix.com]
created: 2026-04-15
type: concept
status: active
score: 8.0
updated: 2026-04-18
---

# Open Felix

**Open Felix** is a free, open source local AI agent for Apple Silicon Macs, powered by [[MLX]]. It provides a complete local AI agent experience with no cloud dependency, no subscription, and no usage limits.

## Overview

Open Felix targets users who want a dedicated local AI agent application running natively on Apple Silicon. Unlike API-based agents that send data to external servers, Open Felix runs entirely on-device, making it attractive for privacy-sensitive use cases.

## Key Features

- **100% local** — no cloud, no data leaving your machine
- **Apple Silicon native** — powered by MLX for efficient inference
- **Free and open source** — no subscription, no usage caps
- **Menu bar app** — press Option+Space anywhere to invoke Felix
- **Voice-first** — speak or type requests, Felix acts immediately
- **Calendar + web search + messaging** — reads calendar, searches web, sends messages natively
- **Menu bar residence** — lives in the Mac menu bar, always accessible

## How It Works

Open Felix operates entirely on-device:

1. **Activation**: Press Option+Space from any application
2. **Input**: Speak or type your request
3. **Action**: Felix reads your calendar, searches the web, or sends messages
4. **No internet required** — all inference runs locally via MLX on Apple Silicon

The architecture uses a local MLX model as the brain, with tool-calling capabilities for calendar, web search, and messaging integrations.

## Comparison with Alternatives

| Feature | Open Felix | Rapid MLX | LM Studio |
|---------|-----------|-----------|-----------|
| Focus | AI Agent | Inference Engine | GUI + Inference |
| Cost | Free | Free | Free |
| Open Source | Yes | Yes | Partial |
| OpenAI Compatible | Via Rapid MLX | Yes | Yes |
| Apple Silicon | Native MLX | Native MLX | MLX support |
| Agent Capabilities | Full agent | Inference only | Inference only |
| Voice Input | Native | No | No |

## Related Concepts

- [[Rapid-MLX]] — inference engine that works alongside Open Felix
- [[mlx]] — Apple's MLX framework
- [[local-llm]] — Local LLM running on hardware
- [[apple-silicon-mlx]] — Apple Silicon MLX guide
- [[llama.cpp]] — Alternative inference engine

## External Resources

- [Open Felix Official Site](https://openfelix.com/)

---

*Expanded: 2026-04-15 | Source: openfelix.com*
