---
title: "MLX Apple Silicon"
created: 2026-04-18
updated: 2026-04-18
type: concept
tags: [apple-silicon, mlx, local-llm, local-ai, llm, inference]
related:
  - [[apple-silicon]]
  - [[local-llm-agents]]
  - [[llama.cpp]]
  - [[ollama]]
  - [[fishspeech]]
  - [[seavoice-stt]]
---

# MLX Apple Silicon

## Overview
MLX is Apple's machine learning framework for Apple Silicon chips (M1, M2, M3, M4, M5). It provides metal GPU acceleration for efficient LLM inference on Mac hardware — no cloud required.

**Performance**: 30-40 tokens/sec on M4 Pro for 7B models (4-bit quantization), comparable to cloud GPU instances at fraction of cost. M5 chip pushes 70B model support.

## Key Features
- **Metal GPU acceleration**: Native Apple Silicon optimization
- **Memory efficiency**: Unified memory architecture reduces overhead
- **Python + C++ APIs**: mlx-python package for easy integration
- **Model support**: Llama3, Mistral, Phi-3, Gemma, Qwen2, Staabigram
- **Quantization**: 4-bit, 8-bit GGUF support standard

## Architecture
- Unified memory: CPU/GPU share memory pool (M4 Pro: 24-48GB, M5: up to 192GB)
- KV cache optimization for long contexts
- Batch inference with configurable batch sizes
- Streaming generation with token buffering

## Comparison with llama.cpp

| Dimension | MLX | llama.cpp |
|-----------|-----|-----------|
| Apple Silicon | ✅ Native Metal | ✅ Metal support |
| CUDA (NVIDIA) | ❌ | ✅ Full CUDA |
| Ease of use | ✅ pip install mlx | ⚠️ Compile from source |
| Model variety | ✅ mlx-lm library | ✅ GGUF formats |
| Performance | 30-40 tok/s (7B M4) | 40-60 tok/s (7B M4) |
| Vietnamese models | ⚠️ Limited | ✅ More support |

## Setup

```bash
# Install mlx
pip install mlx mlx-lm

# Run a model
python -c "
from mlx_lm import load, generate
model, tokenizer = load('mlx-community/Llama-3.2-3B-Instruct-4bit')
response = generate(model, tokenizer, prompt='Hello', max_tokens=100)
print(response)
"
```

## Models for Apple Silicon

### Consumer (M4 Pro)
- **3B Q4**: Llama3.2 3B, Phi-3.5 mini
- **7B Q4**: Llama3.2 7B, Mistral 7B, Qwen2.5 7B
- **13B Q4**: Llama3.1 13B (marginal performance)

### Pro (M4 Max/M5)
- **13B Q4**: Llama3.1 13B, Command R+
- **70B Q4**: Llama3.1 70B (M5 only)

## Related
- [[apple-silicon]] — Apple Silicon overview
- [[local-llm-agents]] — Local LLM for agents
- [[llama.cpp]] — Alternative local LLM engine
- [[ollama]] — Easy local LLM setup
- [[fishspeech]] — Vietnamese TTS
- [[seavoice-stt]] — Vietnamese STT
