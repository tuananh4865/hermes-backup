---
title: "macMLX"
created: 2026-04-19
updated: 2026-04-19
type: concept
tags: [macmlx, apple-silicon, local-llm, mlx, native-app, openai-compatible, gui]
related:
  - [[mlx-lm]]
  - [[mlx-studio]]
  - [[local-llm]]
  - [[apple-silicon-mlx]]
  - [[ollama]]
---

# macMLX

## Overview

**macMLX** is a native macOS application for running local large language models (LLMs) on Apple Silicon, built entirely with SwiftUI and backed by Apple's MLX framework. It provides a graphical interface, a command-line tool, and a running OpenAI-compatible API server — all in one app. No API keys, no subscriptions, no data leaving the machine.

## Key Features

### Native macOS Experience

- **SwiftUI GUI** — uses native macOS controls, follows Apple's Human Interface Guidelines
- **Menu bar presence** — runs as a menu bar app (like iStat Menus or Rectangle), minimal footprint
- **System-level integration** — shares models with other MLX apps (MLX Studio, LM Studio MLX), uses Keychain for model credentials if needed

### Three Ways to Use

**1. GUI (Graphical Interface)**
Open the app window, select a model from the dropdown, start chatting. The GUI supports:
- Model selection from local cache or Hugging Face download
- Chat history persistence
- Configurable generation parameters (temperature, max tokens, top-p)
- Streaming responses

**2. CLI (Command-Line Interface)**
```bash
# Install CLI tools
brew install macmlx

# Chat in terminal
macmlx chat --model Llama-3.2-3B-Instruct-4bit

# Generate from file
macmlx generate --model Llama-3.2-3B-Instruct-4bit --prompt "$(cat prompt.txt)"
```

**3. OpenAI-Compatible API Server**
```bash
# Start the server
macmlx serve --model Llama-3.2-3B-Instruct-4bit --port 8080

# Use with any OpenAI-compatible client
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.2", "messages": [{"role": "user", "content": "Hello"}]}'
```

The API accepts the standard OpenAI Chat Completions format and returns streaming or non-streaming responses.

## Model Management

### Hugging Face Integration

macMLX downloads models directly from Hugging Face Hub:
- Browse available MLX models in-app
- One-click download with progress indicator
- Model caching in `~/.cache/mlx-community/`
- Automatic quantization during download

### Supported Model Formats

| Format | Description | Notes |
|--------|-------------|-------|
| MLX native | `.mlx` files from `mlx-community/` | Fastest, recommended |
| Hugging Face safetensors | Standard HF format | Automatically converted to MLX on first load |
| GPTQ/GGUF | Quantized formats | MLX has native GPTQ support |

### Recommended Models for Apple Silicon

For M1/M2 (16GB unified memory):
- Llama 3.2 1B Instruct 4-bit (~2GB) — fast, decent quality
- Phi-3 mini 4-bit (~2.5GB) — strong reasoning for size

For M3/M4 (24-48GB unified memory):
- Llama 3.2 3B Instruct 4-bit (~6GB) — best balance
- Mistral 7B Instruct 4-bit (~4GB) — excellent quality
- Gemma 2 2B IT 4-bit (~1.5GB) — Google's efficient model

For M4 Max/M5 (64-128GB unified memory):
- Llama 3.2 7B Instruct 4-bit (~14GB) — high quality
- Mistral 22B 4-bit (~12GB) — very capable
- Qwen 2.5 7B Chat 4-bit (~4GB quantized)

## Architecture

macMLX uses MLX as its inference engine, which means:

- **Unified memory access** — models load into unified memory, all cores access without copying
- **Metal acceleration** — every MLX operation runs on the GPU via Metal
- **Memory-efficient** — MLX's memory management reduces fragmentation vs llama.cpp
- **Streaming** — token generation streams in real-time via the API

## Comparison with Alternatives

| Feature | macMLX | Ollama | LM Studio | MLX Studio |
|---------|--------|--------|-----------|------------|
| Native macOS app | ✅ SwiftUI | ❌ Electron | ✅ Qt | ✅ Electron |
| MLX-native | ✅ | ⚠️ v0.19+ | ⚠️ MLX branch | ✅ |
| OpenAI-compatible API | ✅ | ✅ | ✅ | ✅ |
| GUI | ✅ | ❌ (web UI) | ✅ | ✅ |
| CLI | ✅ | ✅ | ✅ | ❌ |
| Fine-tuning support | Via mlx-lm | ❌ | ❌ | ❌ |
| Price | Free | Free | Free | Free |

## Use Cases

### Privacy-Sensitive Work

When working with confidential documents, code, or conversations that cannot leave your machine:
- Run a local model via macMLX API
- Point your apps (Notion, Linear, Slack) at `localhost:8080`
- Zero data transmission to external servers

### Development

Local coding models for development:
- Pull a code-specialized model (e.g., DeepSeek Coder 6.7B MLX)
- Use as a drop-in for Claude API in your editor
- No API costs for development and testing

### Learning and Experimentation

- Download smaller models (1B-3B) to experiment with prompting strategies
- No rate limits, no costs, no internet required
- Compare model outputs on sensitive or domain-specific queries

## Limitations

- **Apple Silicon only** — requires M1 or later; Intel Macs not supported
- **Model size limited by memory** — largest model you can run = total unified memory minus macOS overhead
- **No vision support** — image input requires separate configuration with MLX-VLM
- **No multi-modal** — voice, video input not supported in macMLX

## Related Concepts

- [[mlx-lm]] — Apple's Python package for MLX inference and fine-tuning
- [[mlx-studio]] — All-in-one macOS app with more features (chat, code, image generation)
- [[local-llm]] — Running LLMs on your own hardware
- [[apple-silicon-mlx]] — Apple's ML framework overview
- [[ollama]] — Popular model management tool with MLX support since v0.19

---

_metadata: quality=7.4 | updated=2026-04-19
