---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 local-llm (extracted)
  - 🔗 lm-studio (extracted)
relationship_count: 2
---

# Apple Silicon LLM Optimization

## Overview

Apple Silicon (M1/M2/M3/M4 chips) offers exceptional performance for local LLM inference through:
- Unified memory architecture (CPU + GPU share memory)
- Neural Engine (16-core NPU on M3)
- High bandwidth memory (up to 800GB/s on M3 Max)
- MLX framework optimized for Apple Silicon

## MLX Framework

Apple's MLX is a machine learning array framework specifically designed for Apple Silicon.

### Key Features
- **Unified memory**: No need to move data between CPU/GPU
- **Memory efficient**: Can run 7B models on 24GB MacBook Pro
- **Python-first API**: Easy integration with existing code

## Optimization Techniques

### 1. Quantization
Reduce model size while maintaining quality:
- **4-bit quantization**: 50% size reduction, minimal quality loss
- **GGUF format**: llama.cpp's quantized format works with MLX

### 2. Pruning
Remove unnecessary attention heads to reduce model size and improve inference speed.

### 3. Speculative Decoding
- Draft model predicts next tokens
- Verify with larger model
- 2-3x speedup on Apple Silicon

## Performance Benchmarks (M3 Max)

| Model | Context | Tokens/sec |
|-------|---------|------------|
| Qwen2.5-0.5B | 4K | ~80 |
| Qwen2.5-1.5B | 4K | ~45 |
| SmolLM2-360M | 4K | ~150 |

## Related
- [[local-llm]] — Local inference in general
- [[lm-studio]] — Tool for local model management
