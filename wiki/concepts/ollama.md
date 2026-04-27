---
title: Ollama
description: Open-source tool for running local LLMs on Mac, Linux, and Windows with simple commands. Supports Ollama with MLX backend for Apple Silicon.
tags:
  - local-llm
  - inference
  - apple-silicon
  - mlx
  - open-source
created: 2026-04-20
---

# Ollama

Ollama is an open-source tool for running large language models (LLMs) locally on Mac, Linux, and Windows with a single command. It abstracts away the complexity of model management, quantization, and inference serving, making local LLM accessible to developers and enthusiasts.

## Installation

```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Or via Homebrew
brew install ollama

# Windows (preview)
winget install Ollama.Ollama
```

### Apple Silicon Setup

On Mac with Apple Silicon, Ollama automatically uses the best available backend:

```bash
# Pull a model
ollama pull llama3.2:3b-instruct-q4_K_M

# Run interactively
ollama run llama3.2:3b "Explain quantum computing"

# List available models
ollama list
```

## Ollama v0.19 — MLX Backend (March 2026)

The March 2026 release of Ollama v0.19 introduced **MLX backend support** for Apple Silicon, delivering up to **93% faster decode speeds** compared to previous versions on M-series chips.

### Enabling MLX Backend

```bash
# Set environment variable before running
export OLLAMA_FLATTEN_WEIGHTS=1

# Run with MLX optimization
ollama run llama3.2:3b-instruct-q4_K_M
```

### Benchmark: Before vs After MLX

| Model | Without MLX (tokens/sec) | With MLX (tokens/sec) | Speedup |
|-------|-------------------------|----------------------|---------|
| Llama 3.2 3B | ~30 | ~58 | 1.93x |
| Llama 3.2 8B | ~18 | ~35 | 1.94x |
| Mistral 7B | ~15 | ~29 | 1.93x |

### Hardware Requirements

MLX backend works on:
- M1 Pro/Max/Ultra
- M2 Pro/Max/Ultra  
- M3 Pro/Max/Ultra
- M4 Pro/Max/Ultra
- M5 Pro/Max (optimal)

Minimum 16GB unified memory recommended for comfortable 7B model usage.

## Model Management

### Pulling Models

```bash
# From Ollama library
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull phi:latest

# From Hugging Face (with GGUF)
ollama pull hf.co/owner/modelname
```

### Creating Custom Models

```bash
# Create a Modelfile
cat > Modelfile << 'EOF'
FROM llama3.2:3b-instruct-q4_K_M
TEMPLATE \"\"\"{{ if .System }}<<SYS>>{{ .System }}<</SYS>>
{{ end }}{{ .Prompt }}<|im_end|>\"\"\"
PARAMETER temperature 0.7
PARAMETER top_p 0.9
EOF

# Create the model
ollama create my-custom-llama -f Modelfile
```

### Importing Existing Models

```bash
# Convert and import from safetensors
ollama create mistral-custom -- ModelFile ./Modelfile

# Or use the import script for Hugging Face models
python3 -m llama_tag --import ./models/mistral-7b/
```

## API and Integration

Ollama exposes a REST API for integration with agent frameworks:

### Local API

```bash
# Chat completions
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2:3b",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}'

# Generate completion
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:3b",
  "prompt": "The capital of France is"
}'

# Embeddings
curl http://localhost:11434/api/embeddings -d '{
  "model": "llama3.2:3b",
  "prompt": "The recipe for soup"
}'
```

### Integration with Agent Frameworks

```python
# LangChain
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3b", temperature=0.7)
response = llm.invoke("What is retrieval-augmented generation?")

# CrewAI
from crewai import Agent, Task, Crew

agent = Agent(
    role="Researcher",
    backstory="You are an expert researcher.",
    llm=ChatOllama(model="llama3.2:3b")
)

# OpenAI-compatible endpoint for Claude Code, etc.
# Set base_url to http://localhost:11434/v1
```

### Claude Code Integration

Ollama v0.19 added Hermes and GitHub Copilot CLI integrations:

```bash
# Configure Claude Code to use Ollama
claude code --tool-ollama

# Or set environment
export OPENAI_BASE_URL=http://localhost:11434/v1
```

## Comparing Ollama vs Alternatives

| Feature | Ollama | LM Studio | llama.cpp (CLI) | vLLM |
|---------|--------|-----------|-----------------|------|
| **Ease of use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **Apple Silicon** | ✅ MLX | ✅ MLX | ✅ Metal | 🔜 |
| **Model variety** | Good | Good | Best | Good |
| **API compatibility** | OpenAI | OpenAI | Custom | OpenAI |
| **GPU sharing** | ❌ | ❌ | ❌ | ✅ |
| **Pricing** | Free | Freemium | Free | Free |

## Troubleshooting

### High Memory Usage

```bash
# Check running models
ollama list

# Stop specific model
ollama stop llama3.2:3b

# Or stop all
pkill -f ollama && ollama serve
```

### Slow Inference on Apple Silicon

1. Ensure MLX backend is enabled: `export OLLAMA_FLATTEN_WEIGHTS=1`
2. Use quantized models (Q4_K_M recommended)
3. Close other memory-intensive applications
4. Check model is loaded in memory (`ollama ps`)

### Import Errors

Ollama requires GGUF-formatted models. Convert from safetensors:

```bash
# Use llama.cpp tools
python3 -m llama_cpp_caravel --help
```

## See Also

- [[apple-silicon]] — Apple M-series chips for local LLM
- [[llama.cpp]] — C/C++ inference engine beneath Ollama
- [[MLX]] — Apple's ML framework powering Ollama MLX backend
- [[local-llm]] — Overview of running LLMs locally
