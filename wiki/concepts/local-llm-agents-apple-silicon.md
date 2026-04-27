---
title: "Local LLM Agents — Run AI Agents on Your Mac"
created: 2026-04-15
type: concept
tags: [local-llm, apple-silicon, mlx, llama.cpp, privacy, agents]
related:
  - [[local-llm-agents]]
  - [[apple-silicon-mlx]]
  - [[ai-agents]]
  - [[ollama]]
---

# Local LLM Agents — Run AI Agents on Your Mac

## Why Run Agents Locally?

**Privacy-first AI**: All agent processing happens on your machine. No data leaves. No subscription. No rate limits.

**Cost savings**: Once you own the hardware, running local agents is free. Cloud API costs disappear.

**Offline capability**: Agents work without internet connection.

## Apple Silicon: Best Hardware for Local Agents

### Why Apple Silicon Wins for Local Agents

**Unified memory architecture** — GPU and CPU share the same memory pool:
- No VRAM bottleneck
- Models that fit in RAM run at full speed
- M4 Max with 128GB = run 70B models at 30 tok/s

**MLX library** — Apple's optimized ML framework:
- 2x faster than llama.cpp on Apple Silicon
- Hardware-aware optimizations
- Easy Python integration via `mlx-lm` package

### Performance Comparison

| Hardware | Memory | Model Size | Token/sec | Power |
|----------|--------|------------|-----------|-------|
| M4 Max | 128GB | 70B | ~30 | 70W |
| M2 Ultra | 192GB | 70B | ~25 | 100W |
| RTX 4090 | 24GB | 13B max | ~45 | 450W |
| M4 Pro | 64GB | 30B | ~35 | 30W |

**Key insight**: For 7-13B models (optimal for agents), Apple Silicon matches or beats CUDA at 1/6th the power.

## MLX: The Apple Silicon ML Framework

### What is MLX?

Apple's machine learning framework optimized for Apple Silicon:
- **Unified API**: NumPy-like API for ML
- **Lazy computation**: Memory-efficient graph execution
- **Metal backend**: GPU acceleration on Apple GPUs
- **Python + Swift**: Official support for both

### Best MLX Models for Agents

From Hugging Face MLX model hub:

| Model | Size | Best For | Source |
|-------|------|----------|--------|
| **Llama 3.1 8B** | 8B | General agent tasks | Official Meta |
| **Mistral 7B** | 7B | Reasoning, code | Community |
| **Qwen2.5 14B** | 14B | Long context tasks | Alibaba |
| **Phi-3.5 3.8B** | 3.8B | Fast, low-memory | Microsoft |

### MLX-VLM: Vision + Language on Mac

MLX-VLM (Vision Language Models) gained **343 GitHub stars in one day** (April 5, 2026):
- Run multimodal models (image + text) locally
- Useful for document understanding agents
- `pip install mlx-vlm` to get started

## llama.cpp: The Cross-Platform Alternative

### Why llama.cpp Still Matters

- Works on ANY hardware (Mac, Linux, Windows)
- Broader model support than MLX
- Quantization: 4-bit = 4GB for 7B model
- **Best for**: Older Macs, Windows users, exotic models

### Performance Tuning

```bash
# Using Ollama (wraps llama.cpp)
ollama run llama3.2 --verbose

# Native llama.cpp
./llama-cli -m model.gguf -p "You are a helpful agent" \
  --temp 0.7 --ctx-size 4096 -t 8
```

## Ollama: Easiest Local LLM

### Ollama + MLX = Best Combo

Ollama now supports MLX models natively:
```bash
# Install Ollama
brew install ollama

# Run MLX-optimized model
ollama run llama3.2:3b

# Or use Ollama's own library
ollama run llama3.2
```

**Ollama MLX** announcement (April 2026): 2x faster local AI on Apple Silicon.

## Agent Architectures for Local LLMs

### Memory-First Design

Local agents need different memory architecture than cloud agents:

```
┌─────────────────────────────────────────────────────┐
│  Short-term: LLM context window (8K-128K tokens)   │
├─────────────────────────────────────────────────────┤
│  Session: SQLite/vector store (per-project)       │
├─────────────────────────────────────────────────────┤
│  Long-term: File-based knowledge base              │
└─────────────────────────────────────────────────────┘
```

### Recommended Stack for Local Agents

| Component | Choice | Reason |
|-----------|--------|--------|
| **Model** | Llama 3.2 3B via MLX | Fast, good reasoning |
| **Framework** | LangGraph + local adapter | Graph orchestration |
| **Memory** | SQLite + embeddings | No external services |
| **Tools** | MCP servers | Standard protocol |
| **UI** | CLI or web | Privacy-preserving |

## Use Cases for Local Agents

1. **Code assistant**: Code review, refactoring, testing — all local
2. **Writing assistant**: Drafting, editing, research — no cloud
3. **Data analysis**: CSV/JSON processing, visualization
4. **Personal knowledge management**: RAG on your notes
5. **Automation**: n8n + local agent for workflows

## Setup Guide

### Quick Start (macOS)

```bash
# 1. Install Ollama
brew install ollama

# 2. Install MLX model
ollama pull llama3.2:3b

# 3. Install mlx-lm for Apple Silicon optimization
pip install mlx-lm

# 4. Test locally
python -c "from mlx_lm import load; model, tokenizer = load('mlx-community/Llama-3.2-3B-Instruct-4bit')"
```

### Full Agent Setup

```bash
# Clone example agent
git clone https://github.com/langchain-ai/local-gpt-agent.git
cd local-gpt-agent

# Install dependencies
pip install -r requirements.txt

# Configure .env
echo "MODEL_NAME=mlx-community/Llama-3.2-3B-Instruct-4bit" > .env

# Run
python agent.py
```

## Resources

- [Apple MLX Research](https://machinelearning.apple.com/research/exploring-llms-mlx-m5)
- [Hugging Face MLX Models](https://huggingface.co/models?library=mlx)
- [Ollama MLX Announcement](https://byteiota.com/ollama-mlx-2x-faster-local-ai-on-apple-silicon-2026/)
- [mlx-lm PyPI](https://pypi.org/project/mlx-lm/)

## Related Concepts

- [[local-llm-agents]] — Existing local agents wiki page
- [[apple-silicon-mlx]] — Apple Silicon MLX details
- [[ai-agents]] — General AI agent concepts
- [[ollama]] — Ollama local LLM runner
