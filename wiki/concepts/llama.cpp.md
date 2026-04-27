---
title: "llama.cpp"
created: 2026-04-14
updated: 2026-04-20
type: concept
tags: [local-llm, inference, cpp, open-source, llm]
related:
  - [[local-llm]]
  - [[apple-silicon-mlx]]
  - [[ollama]]
  - [[vllm]]
---

# llama.cpp

## Overview

**llama.cpp** is a lightweight, highly optimized C/C++ inference engine for running Large Language Models (LLMs) locally. Created by Georgi Gerganov ([`@ggerganov`](https://github.com/ggerganov)), it enables LLM inference on consumer hardware with minimal dependencies — no Python required. As of 2026, llama.cpp remains the dominant CPU-bound inference engine and the foundation for most local LLM serving solutions.

## Key Characteristics

### Pure C/C++ Implementation
- **No Python dependency** — compiles to a single binary or static library
- **Extreme portability** — runs on Linux, macOS, Windows, and even RISC-V architectures
- **Minimal memory footprint** — quantized models run in 4-16GB RAM depending on size

### Aggressive Quantization Support
llama.cpp pioneered mainstream quantization:
- **Q4_K_M** — 4-bit quantization with mixed precision, best balance of size/speed
- **Q5_K_S** — 5-bit for higher quality when memory allows
- **Q8_0** — 8-bit quantization, near-lossless but larger file sizes
- **F16** — Full 16-bit float for maximum quality on capable hardware

### Metal Support (macOS)
- Native Apple Metal GPU acceleration on M1/M2/M3/M4 chips
- Unified memory architecture eliminates PCIe bandwidth bottlenecks
- Q4_K_M at 30+ tokens/second on M3 Pro (36GB)

## Architecture

### Inference Pipeline
1. **Model loading** — Memory-mapped files for fast startup
2. **KV cache management** — Sliding window for extended context
3. **Batch processing** — Concurrent token generation
4. **Quantized matrix multiplication** — GGUF format kernels

### GGUF Format
The **GGUF (GPT-Generated Unified Format)** stores:
- Model weights with quantization metadata
- Tokenizer vocabulary
- Architecture configuration
- Metadata for seamless loading

## Use Cases

### Local Development
- Fast iteration without cloud API costs
- Privacy-sensitive codebases stay local
- Testing quantization quality before deployment

### Self-Hosted Production
- **llama.cpp Server** — OpenAI-compatible REST API
- powers **Ollama**, Jan.ai, and most local LLM UIs
- Embeddable in applications via C library

### Budget Server Inference
- Mac Mini M4 + llama.cpp = sub-$600 inference server
- CPU-bound inference for models up to 70B at reasonable speeds
- Cloud cost elimination for low-volume applications

## Comparison with Alternatives

| Engine | Strength | Best For |
|--------|----------|----------|
| llama.cpp | CPU-bound, minimal deps | Universal deployment, embedded |
| vLLM | Throughput, PagedAttention | High-volume cloud |
| Ollama | UX, model management | Non-technical users |
| MLX (Apple) | Metal acceleration | Apple Silicon native |

## Technical Notes

### Why llama.cpp Dominates CPU Inference
1. **SIMD optimizations** — AVX2/AVX512 on x86, NEON on ARM
2. **Memory bandwidth-aware** — Architecture designed for RAM→VRAM bandwidth
3. **KV cache quantization** — Reduces memory footprint for long context
4. **No Python GIL** — True parallelism without Python's limitations

### Common Command Line Usage
```bash
# Run inference
./llama-cli -m model.Q4_K_M.gguf -n 256 -p "### Instructions:..."

# Start OpenAI-compatible server
./llama-server -m model.Q4_K_M.gguf --port 8080

# Interactive mode
./llama-cli -m model.Q4_K_M.gguf -i -ins
```

## Sources
- [llama.cpp: Fast Local LLM Inference, Hardware Choices & Tuning](https://www.clarifai.com/blog/ilama.cpp)
- [Running Local AI: Mastering Llama.cpp from Zero to Production](https://atalupadhyay.wordpress.com/2026/04/01/running-local-ai-mastering-llama-cpp-from-zero-to-production/)
- [Local LLM Inference in 2026: The Complete Guide to Tools, Hardware ...](https://blog.starmorph.com/blog/local-llm-inference-tools-guide)
- [Llama.cpp - Run LLM Inference in C/C++](https://llama-cpp.com/)
- [GitHub - ggml-org/llama.cpp: LLM inference in C/C++](https://github.com/ggml-org/llama.cpp)
- [How to Run AI Models Locally in 2026: Complete Ollama & llama.cpp Guide](https://trendharvest.blog/blog/how-to-run-ai-models-locally-2026)

## Metadata
_last_updated: 2026-04-20T20:10
