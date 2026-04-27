---
title: "MLX-LM"
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [mlx, apple-silicon, local-llm, python, hugging-face, inference]
related:
  - [[apple-silicon-mlx]]
  - [[local-llm]]
  - [[llama-cpp]]
  - [[ollama]]
  - [[macmlx]]
  - [[mlx-studio]]
  - [[hugging-face]]
---

# MLX-LM

## Overview

**MLX-LM** is Apple's official Python package for running large language models (LLMs) and performing inference and fine-tuning on Apple Silicon using the MLX framework. It is maintained by Apple's ML Research team and serves as the primary Python interface for MLX-based LLM workloads.

## Key Features

### Hugging Face Hub Integration

MLX-LM integrates directly with the Hugging Face Hub, enabling access to thousands of open-weights LLMs with a single command:

```python
from mlx_lm import load, generate

# Load a model from Hugging Face
model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

# Generate text
response = generate(model, tokenizer, prompt="Explain quantum entanglement")
print(response)
```

Supported operations:
- 4-bit and 8-bit quantization
- LoRA fine-tuning with a few examples
- Streaming generation
- OpenAI-compatible chat template enforcement
- Upload fine-tuned models back to Hugging Face

### Model Support

MLX-LM supports a broad range of model architectures:

| Model Family | Examples | Notes |
|-------------|---------|-------|
| Llama | Llama 3.2, Llama 3.1 | 1B to 70B |
| Qwen | Qwen 2.5, Qwen 3 | Vision variants may be broken on MLX |
| Gemma | Gemma 3, Gemma 2 | Google's open models |
| Mistral | Mistral 7B, Mixtral | MoE architecture |
| Phi | Phi-3, Phi-4 | Microsoft's efficient models |
| Nemotron | Nemotron 4 | NVIDIA's open model |

### Fine-Tuning with LoRA

MLX-LM supports parameter-efficient fine-tuning via LoRA (Low-Rank Adaptation), enabling users to adapt open-weights models to specific tasks on a Mac:

```python
from mlx_lm import load, train
from mlx_lm.utils import generate

# Fine-tune on custom data
trainer = train.MLXOLoRAMetricLM(
    model="mlx-community/Llama-3.2-1B-Instruct-4bit",
    train_data_path="./my-training-data.jsonl",
    batch_size=1,
    lora_rank=8,
    epochs=3,
)
trainer.train()
```

Requirements for fine-tuning:
- Apple Silicon Mac (M1 or later)
- Single GPU fine-tuning with LoRA: ~10GB unified memory for 7B models
- Full fine-tuning: requires larger unified memory configurations

### Quantization

MLX-LM supports multiple quantization levels to fit models into available memory:

| Quantization | Memory (7B model) | Quality |
|-------------|-------------------|---------|
| FP16 | ~14GB | Highest |
| 8-bit | ~7GB | Near-lossless |
| 4-bit | ~3.5GB | Good for most tasks |
| 2-bit | ~1.8GB | Experimental |

### OpenAI-Compatible Server

MLX-LM includes an OpenAI-compatible chat completions endpoint:

```bash
# Start the server
python -m mlx_lm.server --model mlx-community/Llama-3.2-3B-Instruct-4bit --port 8080
```

Then use it as a drop-in OpenAI replacement:

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080", api_key="none")
response = client.chat.completions.create(
    model="llama-3.2",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Performance

### Benchmark Comparison

On M4 Max (128GB unified memory), MLX-LM vs other runtimes:

| Runtime | tokens/sec | Notes |
|---------|-----------|-------|
| llama.cpp | 62.4 | Fastest raw throughput |
| MLX-LM | 58.7 | Near llama.cpp, better memory management |
| Ollama | 51.3 | Includes model management overhead |
| LM Studio | ~55 | GUI + server |

MLX-LM's advantage is not raw speed but the combination of speed + native Apple Silicon optimization + easy Python integration.

### Why MLX Beats llama.cpp on Apple Silicon

MLX was designed from scratch for Apple's unified memory architecture, while llama.cpp was built for NVIDIA GPUs and ported to Metal. Key advantages:

1. **Unified memory access** — MLX tensors live in unified memory and are accessed directly by all compute cores without copying
2. **Memory layout** — MLX's array layout is optimized for the memory bandwidth of M-series chips
3. **Neural Engine** — On M5 chips with Neural Engine accelerator, MLX can leverage it; llama.cpp cannot
4. **KV cache optimization** — MLX has specialized kernels for attention that reduce memory fragmentation

### ArXiv Benchmark (2026)

From [ArXiv 2601.19139](https://arxiv.org/html/2601.19139): Comparing vLLM-MLX, mlx-lm, and llama.cpp across models from 0.6B to 30B parameters (Qwen3, Llama 3.2, Gemma 3, Nemotron):

- MLX achieves **21% to 87% higher throughput** than llama.cpp on Apple Silicon
- Performance gap widens for larger models and heavier quantization
- Memory efficiency: MLX uses 15-30% less peak memory than llama.cpp for equivalent throughput

## Installation

```bash
# Install via pip
pip install mlx-lm

# Upgrade
pip install mlx-lm --upgrade

# Verify installation
python -c "from mlx_lm import load; print('MLX-LM installed successfully')"
```

## Common Workflows

### Quick Inference

```python
from mlx_lm import load, generate

# Load smallest quantized Llama model
model, tokenizer = load("mlx-community/Llama-3.2-1B-Instruct-4bit")

# Generate
result = generate(model, tokenizer, prompt="Write a haiku about AI", max_tokens=50)
print(result)
```

### Conversational Chat

```python
from mlx_lm import load, chat_template

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

# Apply chat template
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
prompt = tokenizer.apply_chat_template(messages, tokenize=False)
response = generate(model, tokenizer, prompt=prompt)
```

## Limitations

- **Vision models on Qwen**: Qwen2.5-VL and Qwen3.5-Vision tool calling are broken as of March 2026 on MLX
- **Non-Apple hardware**: MLX only runs on Apple Silicon — no Windows/Linux support
- **Fine-tuning scale**: Full fine-tuning of 70B models requires 512GB+ unified memory (M4 Ultra or dual-M4 Max Mac Pro)
- **Flash Attention**: Some models require Metal kernel patches for optimal attention performance

## Related Tools

- [[macmlx]] — Native macOS app with MLX support
- [[mlx-studio]] — All-in-one macOS app with chat, code, image generation
- [[llama-cpp]] — C/C++ inference engine, cross-platform, slightly faster raw
- [[ollama]] — Model management CLI, easy setup, includes MLX since v0.19
- [[apple-silicon-mlx]] — Apple ML framework overview

---

_metadata: quality=7.8 | updated=2026-04-19
