---
title: "Ollama with MLX"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [ollama, mlx, apple-silicon, local-llm, inference, apple]
related:
  - [[apple-silicon-mlx]]
  - [[metalrt]]
  - [[local-llm-agents]]
  - [[llama-cpp]]
sources:
  - https://ollama.com/blog/mlx
  - https://9to5mac.com/2026/03/31/ollama-adopts-mlx-for-faster-ai-performance-on-ap
  - https://iphonewired.com/common-problems/1127341/
---

# Ollama with MLX

Ollama adopted Apple's MLX framework in **March 2026**, releasing **v0.19** with full MLX support. The update delivers **2x faster performance** on Apple Silicon compared to its previous llama.cpp Metal backend, making Ollama+MLX the recommended path for local LLM inference on Mac.

## Overview

Ollama is a popular local LLM runtime that provides a simple API for downloading and running models. Previously it used llama.cpp's Metal backend, which treats the GPU as a discrete accelerator — data moves between CPU memory and GPU memory across the bus. With MLX, Ollama now leverages Apple's unified memory architecture where the GPU accesses memory directly.

## v0.19 — March 31, 2026: MLX Integration

The March 31, 2026 release of Ollama v0.19 fundamentally changed local LLM performance on Apple Silicon:

- **2x faster decode** compared to previous Metal backend
- **GPU Neural Accelerators** on M5, M5 Pro, M5 Max chips accelerate both time-to-first-token (TTFT) and throughput
- **Unified memory architecture** eliminates CPU↔GPU memory copies that previously bottlenecked Metal
- **MLX preview** as of March 30 showed the fastest way to run Ollama on Apple Silicon

The v0.19 preview (March 30) illustrated Ollama standing beside a fast car — "both a daily driver and go on to win races" — reflecting the dual-use nature of local LLMs: casual chat AND serious inference workloads.

## Performance Gains

The benchmark results are dramatic:

| Metric | Before (llama.cpp Metal) | After (MLX) | Improvement |
|--------|-------------------------|-------------|-------------|
| Decode speed (M1 Max, 30B) | 3.19 tok/s | ~16 tok/s | **~5x** |
| M4 Mac Mini (7B) | baseline | ~30 tok/s | **93% faster** |

The 93% improvement comes from:
1. **Unified memory** — no CPU↔GPU memory copies
2. **MLX optimization** — Apple's framework optimized for Apple Silicon
3. **Better batch handling** — MLX's batch inference improvements

## Setup

```bash
# Install Ollama (auto-includes MLX on Apple Silicon)
brew install ollama

# Or update if already installed
brew upgrade ollama

# Pull a model (automatically uses MLX on Apple Silicon)
ollama pull llama3.3
ollama pull qwen3

# Run with API
ollama run qwen3 "Explain MetalRT in simple terms"
```

## Architecture

```
Ollama (model downloads, API server)
    ↓
 MLX (Apple Silicon optimization layer)
    ↓
 Metal / MetalRT (GPU acceleration)
    ↓
 Unified Memory (CPU/GPU shared)
```

## Supported Models

Ollama with MLX supports:
- **Llama 3.3** — strong all-around, 70B available
- **Qwen 3** — excellent reasoning, multilingual
- **Mistral** — good balance of speed and quality
- **DeepSeek** — cost-effective, strong coding
- **Phi** — small models for resource-constrained setups

## Ollama vs MetalRT

| Aspect | Ollama + MLX | MetalRT |
|--------|-------------|---------|
| **Ease of use** | ⭐⭐⭐⭐⭐ Simple API | ⭐⭐⭐ Technical |
| **Performance** | ⭐⭐⭐⭐ Very fast | ⭐⭐⭐⭐⭐ Fastest |
| **Model formats** | GGUF via Ollama | Custom |
| **API** | REST, ready to use | Custom integration |
| **Best for** | Developers, agents | Maximum performance |

For [[local-llm-agents]], Ollama+MLX is the practical choice — the 7-10% performance difference between MLX and MetalRT rarely matters when API simplicity and model management are factored in.

## For Agents

Ollama's HTTP API makes it ideal for agent frameworks:

```bash
# Start Ollama server
ollama serve

# Query via HTTP
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3",
  "prompt": "List 5 Apple Silicon advantages for local LLMs",
  "stream": false
}'
```

This enables [[multi-agent-systems]] running on MacBook with zero API costs.

## Related Concepts

- [[apple-silicon-mlx]] — Apple's MLX framework overview
- [[metalrt]] — fastest decode engine (1.35-2.14x faster than llama.cpp)
- [[local-llm-agents]] — local LLM agents that run on Mac
- [[llama-cpp]] — the previous Metal backend Ollama used
