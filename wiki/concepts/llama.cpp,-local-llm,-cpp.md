---
title: "Llama.cpp — Local LLM Inference Engine"
created: 2026-04-13
updated: 2026-04-19
type: concept
tags: [llama.cpp, local-llm, cpp, inference, quantization, apple-silicon, metal]
sources:
  - https://github.com/ggerganov/llama.cpp
  - https://github.com/ggerganov/llama.cpp/tree/master/examples
related:
  - apple-silicon-mlx
  - local-llm-agents
  - ollama
  - quantization
---

# Llama.cpp — Local LLM Inference Engine

## Overview

**llama.cpp** is an open-source C/C++ inference engine for running LLM models (LLama, Mistral, Qwen, Phi, and hundreds of others) locally on consumer hardware. Created by Georgi Gerganov ([@ggerganov](https://github.com/ggerganov)), it prioritizes maximum hardware utilization and minimum dependencies — no CUDA, no PyTorch, no Python required. Just compiled C binaries and model files.

llama.cpp made local LLM inference accessible to everyone. Before it, running a 7B model locally required complex PyTorch setups. After it, you download a binary and a quantized model file and run inference on a MacBook, gaming laptop, or even a Raspberry Pi.

## Core Technical Design

### Pure C/C++ Implementation

Every component is written in C/C++ for maximum portability:
- **No external ML dependencies**: No PyTorch, no TensorFlow, no CUDA runtime
- **Minimal dependencies**: Just standard C libraries
- **Hardware acceleration**: CUDA (NVIDIA), Metal (Apple), OpenCL (multi-platform), Vulkan
- **Quantization kernels**: Hand-optimized SIMD kernels for AVX2/AVX512 on x86, NEON on ARM

### Quantization

llama.cpp pioneered widespread GGUF (formerly GGML) quantization. The key insight: you don't need 16-bit floats to get good LLM quality. 4-bit or 8-bit quantized models fit in dramatically less RAM while retaining 95-99% of model quality.

| Format | Bits | Memory (7B) | Memory (70B) | Quality |
|--------|------|-----------|-------------|---------|
| FP16 | 16 | ~14GB | ~140GB | 100% |
| Q8 | 8 | ~7GB | ~70GB | ~99% |
| Q5 | 5 | ~4.5GB | ~45GB | ~98% |
| Q4 | 4 | ~3.5GB | ~35GB | ~97% |
| Q3 | 3 | ~2.8GB | ~28GB | ~95% |
| Q2 | 2 | ~2.2GB | ~22GB | ~93% |

The [llama.cpp repository](https://github.com/ggerganov/llama.cpp) is the definitive reference with examples for every platform.

### KV Cache and Context Management

llama.cpp implements paged attention (via `kqv` kernels) for efficient KV cache management. The context window is managed with sliding attention — older tokens are evicted as new ones enter.

## Performance Comparison

### Apple Silicon

On Apple Silicon, llama.cpp runs via Metal GPU acceleration. Performance varies by chip:

| Chip | Suggested Model | Tokens/sec (Q4) |
|------|----------------|-----------------|
| M1 Pro | 7B | ~30-40 t/s |
| M2 Pro | 13B | ~25-35 t/s |
| M3 Pro | 13B | ~35-45 t/s |
| M4 Pro | 13B | ~50-60 t/s |
| M4 Max | 70B | ~40-50 t/s |

### vs MLX

MLX (Apple's own framework) is 20-30% faster than llama.cpp on Apple Silicon for equivalent model sizes. MLX has the advantage of tighter Metal integration and Apple's official optimization. llama.cpp remains more portable across chip generations and non-Apple hardware.

### vs Ollama

Ollama wraps llama.cpp (among other backends) in a user-friendly package with:
- `ollama run mistral` — one-command model loading
- Built-in API server
- Model library with one-command downloads

llama.cpp is the engine; Ollama is the UX layer. For development, Ollama is faster to set up. For production optimization, llama.cpp gives more control.

## Key Commands

```bash
# Inference
./llama-cli -m model.gguf -p "The capital of France is"

# Server (REST API)
./llama-server -m model.gguf --port 8080

# Batch inference
./llama-bench -m model.gguf

# Convert models to GGUF
python3 convert.py /path/to/model --outfile model.gguf
```

## llama.cpp in AI Agents

For [[local-llm-agents]], llama.cpp is the backbone of the local inference stack:

1. **Agent reasoning**: Local model generates tool calls and reasoning
2. **Memory**: Long conversations via extended context
3. **Tool execution**: Shell commands, code execution, file operations
4. **Privacy**: Everything runs locally — no data leaves the machine

Popular local agent stacks using llama.cpp:
- **Ollama + LangChain/LangGraph**: Full Python stack
- **llama.cpp server + custom agent**: Minimal Rust/Go wrapper
- **LM Studio**: GUI + API server over llama.cpp

## Limitations

- **No attention optimizations**: No Flash Attention v2+ optimizations (unlike vLLM)
- **Single-GPU focus**: No tensor parallelism across multiple GPUs
- **Quantization quality**: Very low-bit (Q2, Q3) can degrade complex reasoning
- **API surface**: Much simpler than vLLM's OpenAI-compatible API

## Related Concepts

- [[apple-silicon-mlx]] — Apple's competing framework
- [[local-llm-agents]] — Local LLM agents architecture
- [[ollama]] — User-friendly wrapper around llama.cpp
- [[quantization]] — Model quantization techniques
- [[llama-cpp]] — Related llama.cpp pages
