---
title: "Apple M5"
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [apple-silicon, hardware, ml, chips, 2026]
related:
  - [[apple-silicon-mlx]]
  - [[local-llm-agents]]
  - [[mlx]]
---

# Apple M5

## Overview

The **Apple M5** chip family represents Apple's next-generation silicon, expected to bring significant improvements to on-device ML and local LLM inference. Based on current trajectory and industry analysis, M5 will feature enhanced Neural Engine capabilities combined with High Bandwidth Memory (HBM).

## Expected Specifications

| Component | M5 Expected | M4 Current |
|-----------|-------------|------------|
| Process | 3nm/2nm class | 3nm N3E |
| Neural Engine | 50+ TOPS | 38 TOPS |
| Memory | HBM + Unified | Unified only |
| Max Memory BW | 500+ GB/s | 273 GB/s |
| CPU Cores | 24 performance | 16 performance |
| GPU Cores | 40 | 32 |

## Why HBM Matters for Local AI

High Bandwidth Memory is a game-changer for local LLM inference:

1. **Model size**: Current unified memory limits to ~200B parameter models on M4 Max. HBM could push to 500B+
2. **Throughput**: Memory bandwidth is the primary bottleneck for transformer inference. Doubling bandwidth = near-linear throughput gains
3. **Quantization tolerance**: Higher bandwidth means you can use larger, less-quantized models without sacrificing speed

## M5 for Local AI Inference

With M5, Apple Silicon becomes competitive with discrete GPUs for local inference:

- **70B models**: Run at 30+ tokens/second at INT4 on M5 Pro
- **130B models**: Viable on M5 Max with aggressive quantization
- **200B+ models**: Possible on M5 Ultra with HBM

## Neural Engine Role

The M5 Neural Engine handles:
- **Transformer attention** — Hardware acceleration for attention layers
- **Quantized inference** — INT4/INT8 operations optimized
- **Memory-bandwidth tasks** — Streaming inference for long contexts

## Software Stack (M5 Ready)

The Apple Silicon ML ecosystem is already preparing for M5:

| Framework | M5 Support | Notes |
|-----------|------------|-------|
| MLX | Native | Already optimized for Apple Neural Engine |
| Ollama | MLX backend | Seamless M5 support expected |
| llama.cpp | Metal backend | Apple GPU optimization |
| vLLM | Competing backends | Two Apple Silicon options |

## See Also

- [[apple-silicon-mlx]] — MLX framework on Apple Silicon
- [[local-llm-agents]] — Running AI agents on local models
- [[mlx]] — Apple's ML framework

---

*Sources: [Ars Technica: Apple M5 Family Chiplets](https://arstechnica.com/civis/threads/apple-m5-family-chiplets.1507391/), [MLX Benchmark GitHub](https://github.com/TristanBilot/mlx-benchmark), [Native LLM Inference on Apple Silicon (arXiv 2601.19139)](https://arxiv.org/abs/2601.19139)*
