---
title: "llama.cpp"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [llama-cpp, gguf, quantization, local-llm, inference]
confidence: medium
relationships:
  - 🔗 local-llm
  - 🔗 lm-studio
  - 🔗 gguf
---

# llama.cpp

## Overview

llama.cpp is a C/C++ implementation for efficient LLM inference, providing high-performance CPU and GPU inference for models in GGUF format. It enables running large language models on consumer hardware with minimal dependencies, making local AI accessible without requiring expensive GPU servers.

The project originated as a port of the LLaMA model inference but has evolved into a general-purpose inference engine supporting many model architectures. Its simple architecture, zero-configuration design, and excellent performance have made it the foundation for numerous AI applications and tools.

## Key Concepts

### GGUF Format

GGUF (GPT-Generated Unified Format) is a quantization format designed for efficient model storage and loading:

- **Single file deployment**: Everything (model weights, tokenizer, config) in one file
- **Metadata header**: Self-describing with version info, architecture, quantization type
- **Flexible quantization**: Q2_K, Q3_K, Q4_0, Q4_K, Q5_K, Q6_K, Q8_0

### Quantization Types

| Type | Size (7B) | Quality | Speed |
|------|-----------|---------|-------|
| Q8_0 | ~7GB | Highest | Slowest |
| Q6_K | ~5GB | High | Medium |
| Q5_K | ~4.5GB | Good | Good |
| Q4_K | ~4GB | Good | Fast |
| Q3_K | ~3.5GB | Medium | Fast |
| Q2_K | ~3GB | Low | Fastest |

### Inference Pipeline

llama.cpp processes tokens in stages:

1. **Tokenization**: Convert text to token IDs
2. **Context processing**: Compute attention on prompt tokens
3. **Generation loop**: Sample next token, update KV cache
4. **Decoding**: Convert tokens back to text

```bash
# CLI inference example
./llama-cli -m model.gguf -p "Explain Kubernetes in 3 sentences"
```

## Practical Applications

### LM Studio Integration

LM Studio wraps llama.cpp with a user-friendly interface:

```bash
# Download model (e.g., Qwen2.5-2B)
# Server runs at http://localhost:1234

curl http://localhost:1234/v1/models
# {"data":[{"id":"qwen2.5-2b","object":"model"}]}
```

### Python Integration with llama-cpp-python

```python
from llama_cpp import Llama

# Load quantized model
llm = Llama(
    model_path="./models/qwen2.5-2b.q4_k_m.gguf",
    n_ctx=4096,        # Context window
    n_threads=8,       # CPU threads
    n_gpu_layers=35    # Layers offloaded to GPU
)

# Generate
output = llm(
    "Explain container orchestration:",
    max_tokens=256,
    temperature=0.7,
    stop=["</s>"]
)

print(output['choices'][0]['text'])
```

### KV Cache Optimization

The KV cache stores attention keys/values for context:

```python
# Larger KV cache = longer context
llm = Llama(
    model_path="model.gguf",
    n_ctx=8192,      # Context window size
    n_kv_req=512,    # Maximum KV cache requests
)
```

### Batch Processing

Process multiple prompts efficiently:

```python
# Batch inference
results = llm.create_chat_completion_many([
    {"role": "user", "content": "What is Docker?"},
    {"role": "user", "content": "What is Kubernetes?"},
    {"role": "user", "content": "What is CI/CD?"}
])
```

## llama.cpp vs Other Backends

| Feature | llama.cpp | MLX (Apple) | vLLM (NVIDIA) |
|---------|-----------|-------------|---------------|
| GPU | Any CUDA | Apple Silicon | NVIDIA only |
| Speed | Good CPU | Excellent | Best |
| Memory | Flexible | Unified | PagedAttention |
| Dependencies | Minimal | Minimal | PyTorch + CUDA |

## Related

- [[local-llm]] — Local inference overview
- [[lm-studio]] — Model management tool
