---
title: "vLLM on Apple Silicon (vllm-mlx)"
created: 2026-04-17
type: concept
tags: [local-llm, apple-silicon, mlx, vllm, inference-server]
related:
  - [[local-llm-agents]]
  - [[apple-silicon-mlx]]
  - [[mlx-bitnet]]
---

# vLLM on Apple Silicon (vllm-mlx)

## Overview

**vllm-mlx** (by [waybarrios/vllm-mlx](https://github.com/waybarrios/vllm-mlx)) brings native Apple Silicon GPU acceleration to vLLM by integrating MLX (Apple's ML framework) with unified memory and Metal kernels. The result: an OpenAI and Anthropic API-compatible inference server that runs efficiently on M-series chips.

## Key Value

The primary value of vllm-mlx is **drop-in compatibility** with existing agent tooling:

- LangChain, CrewAI, and LangGraph work without modification
- OpenAI-compatible endpoints (`/v1/chat/completions`, `/v1/completions`)
- Anthropic-compatible endpoints (`/v1/messages`)
- HuggingFace `transformers`-compatible model loading

This means you can run a local inference server on your MacBook that your existing Python agent code talks to, without any changes to the agent framework itself.

## Architecture

```
┌─────────────────────────────────────────────┐
│  Agent Framework (LangChain, CrewAI, etc.)  │
└─────────────────┬───────────────────────────┘
                  │ OpenAI/Anthropic API
┌─────────────────▼───────────────────────────┐
│         vllm-mlx Server                    │
│  ┌─────────────────────────────────────┐   │
│  │  vLLM Engine + MLX Backend          │   │
│  │  - Metal GPU kernels                 │   │
│  │  - Unified memory (shared CPU/GPU)   │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
                  │
        ┌─────────▼─────────┐
        │  Apple Silicon   │
        │  M3/M4 Pro/Max   │
        │  Unified Memory   │
        └───────────────────┘
```

## Performance on M-Series

| Chip | Memory | Model Size | Tokens/sec (FP16) | Tokens/sec (Q4) |
|------|--------|------------|-------------------|-----------------|
| M4 Air | 32GB | 7B | ~20 | ~45 |
| M3 Pro | 36GB | 13B | ~15 | ~35 |
| M4 Max | 128GB | 70B | ~8 | ~20 |

*Based on local-llm-bench-m4-32gb findings and vllm-mlx benchmarks*

## Setup

```python
# Install vllm-mlx
pip install vllm-mlx

# Run server
python -m vllm_mlx.entrypoints.openai.api_server \
    --model meta-llama/Llama-3-8b-Instruct \
    --gpu-memory-utilization 0.9
```

## vs Ollama

| Dimension | vllm-mlx | Ollama |
|-----------|----------|--------|
| API | OpenAI/Anthropic | REST |
| Customization | High | Low |
| MLX-native | Yes | Preview only |
| Community | Growing | Large |
| Update frequency | Active | Stable |

Ollama is simpler for quick local experiments. vllm-mlx is better for production deployments where you need the OpenAI SDK compatibility and fine-grained performance control.

## Related

- [[local-llm-agents]] — Agents running on local models
- [[apple-silicon-mlx]] — MLX framework overview
- [[mlx-bitnet]] — 1-bit quantization on Apple Silicon
