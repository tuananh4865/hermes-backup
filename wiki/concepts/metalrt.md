---
title: "MetalRT"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [apple-silicon, local-llm, inference, performance, mlx]
related:
  - [[apple-silicon-mlx]]
  - [[ollama-mlx]]
  - [[local-llm-agents]]
sources:
  - https://www.runanywhere.ai/blog/metalrt-fastest-llm-decode-engine-apple-silicon
---

# MetalRT

MetalRT is the **fastest LLM decode engine for Apple Silicon**, developed by the team behind the "We Built the Fastest LLM Decode Engine for Apple Silicon" project. It delivers 1.10-1.19x faster performance than mlx-lm and **1.35-2.14x faster than llama.cpp** across all model sizes.

## Overview

MetalRT is a Metal-based inference runtime that optimizes LLM decoding on Apple Silicon GPUs. Unlike llama.cpp's Metal backend (which treats the GPU as a discrete accelerator with CPU-GPU memory transfer overhead), MetalRT leverages Apple's unified memory architecture more efficiently — the GPU accesses memory directly without copying between CPU and GPU address spaces.

## Performance Benchmarks

| Model Size | vs mlx-lm | vs llama.cpp |
|-----------|-----------|--------------|
| 7B | 1.10x faster | 1.35x faster |
| 13B | 1.15x faster | 1.65x faster |
| 30B | 1.19x faster | 2.14x faster |

The performance gap widens with larger models where memory bandwidth becomes the bottleneck — exactly where unified memory architecture shines.

## Technical Details

MetalRT builds on Apple's Metal Performance Shaders (MPS) framework but with custom decode kernels optimized for autoregressive generation:

- **KV cache optimization** — minimizes memory fragmentation in unified memory
- **Speculative decoding** — predicts multiple tokens ahead when headroom allows
- **Batched inference** — processes multiple sequences concurrently
- **Memory planning** — pre-allocates GPU memory to avoid runtime allocation overhead

## Comparison with Alternatives

| Runtime | Strengths | Best For |
|---------|-----------|---------|
| **MetalRT** | Fastest decode, unified memory optimal | Production Apple Silicon inference |
| **mlx-lm** | Apple's official, good integration | Apple MLX ecosystem |
| **llama.cpp** | Most model formats, mature | Broad compatibility |
| **Ollama (MLX)** | Easiest API, model management | Developer experience |

## Use Cases

MetalRT is ideal when:
- Running local LLMs on M-series Macs in production
- Latency-sensitive applications (real-time chat, coding assistants)
- Batch processing with multiple concurrent users
- Large models (30B+) where every token/second matters

## Related Concepts

- [[apple-silicon-mlx]] — Apple's MLX framework that MetalRT competes with
- [[ollama-mlx]] — Ollama with MLX backend (easier API, slightly slower)
- [[local-llm-agents]] — local LLM agents that can use MetalRT for inference
