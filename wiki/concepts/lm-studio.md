---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 local-llm (extracted)
  - 🔗 apple-silicon-llm-optimization (extracted)
  - 🔗 topic-workflow (extracted)
relationship_count: 3
---

# LM Studio

## Overview

LM Studio is a desktop application for running LLMs locally on Mac/Windows/Linux. It provides:
- Model download and management
- Local inference server (OpenAI-compatible API)
- Chat interface for testing
- GPU acceleration support

## Anh's Setup

### Connection
- **URL**: http://192.168.0.187:1234
- **API Key**: lm-studio (dummy)
- **Protocol**: OpenAI-compatible

### Models Available

| Model | Size | Type | Use Case | Notes |
|-------|------|------|----------|-------|
| mlx-qwen3.5-0.8b-claude-4.6-opus-reasoning-distilled | 0.8B | Reasoning distilled | Fallback | SLOW - all output goes to reasoning |
| mlx-qwen3.5-2b-claude-4.6-opus-reasoning-distilled | 2B | Reasoning distilled | ⚠️ Deprecated | Unstable - content output inconsistent |
| mlx-qwen3.5-4b-claude-4.6-opus-reasoning-distilled | 4B | Reasoning distilled | ⚠️ Deprecated | Same issues as 2B |
| huihui-qwen3.5-4b-claude-4.6-opus-abliterated | 4B | Abliterated | Code tasks | |
| qwen3.5-9b-sushi-coder-rl-mlx | 9B | RL fine-tuned | Code generation | |
| qwen3.5-2b-distilled-opus-heretic-mlx-vlm | 2B | VLM | Multimodal | |
| gemma-4-e4b-it | 4B | Instruction tuned | General | |
| qwen3.5-0.8b-mlx | 0.8B | Base instruct | Light tasks | |
| **qwen3.5-2b-mlx** | **2B** | **Base instruct (non-reasoning)** | **✅ WIKI AGENT (DEFAULT)** | Fast, reliable, 0 reasoning tokens |

### Model Comparison: Reasoning vs Non-Reasoning

| Metric | Reasoning Distilled (old) | qwen3.5-2b-mlx (new) |
|--------|---------------------------|----------------------|
| Content output | Unstable (often empty) | ✅ Always present |
| Reasoning tokens | 300-999 | **0** |
| Finish reason | Usually `length` (truncated) | **Always `stop`** |
| Speed | Slow (overthinking) | Fast (direct output) |
| Reliability | Poor for copywriting | **Excellent** |
| Recommended use | ❌ Not for wiki | **✅ Wiki agent default** |

### Wiki Agent Model Selection

**Selected**: `qwen3.5-2b-mlx`
- Source: `mlx-community/Qwen3.5-2B-MLX-4bit`
- Format: MLX 4-bit quantized (Apple Silicon optimized)
- Size: ~1.6GB on disk
- Why: Direct content output, no reasoning overhead, stable performance

## Using LM Studio API

### Python Example
```python
import requests

response = requests.post(
    "http://192.168.0.187:1234/v1/chat/completions",
    headers={"Authorization": "Bearer lm-studio"},
    json={
        "model": "qwen3.5-2b-mlx",
        "messages": [{"role": "user", "content": "Your prompt"}],
        "max_tokens": 512,
        "temperature": 0.3
    }
)
```

### Wiki Agent Integration
See `scripts/lmstudio_wiki_agent.py` for the script that uses this API.

## Troubleshooting

### Gemma 4 MLX fails to load: "Model type gemma4 not supported"

**Error:**
```
🥲 Failed to load the model
Error when loading model: ValueError: Model type gemma4 not supported
```
Hoặc:
```
ValueError: Gemma 4 support is not ready yet, stay tuned!
```

**Fix** (2026-04-10):
1. Symlink gemma4 từ @21 sang @20 nếu @20 thiếu:
   ```bash
   MLX_20="$HOME/.lmstudio/extensions/backends/vendor/_amphibian/app-mlx-generate-mac14-arm64@20"
   MLX_21="$HOME/.lmstudio/extensions/backends/vendor/_amphibian/app-mlx-generate-mac14-arm64@21"
   ln -sf "$MLX_21/lib/python3.11/site-packages/mlx_vlm/models/gemma4" \
      "$MLX_20/lib/python3.11/site-packages/mlx_vlm/models/gemma4"
   ```
2. Xóa hard-coded guard trong mlx_engine:
   - File: `.../app-mlx-generate-mac14-arm64@21/.../mlx_engine/generate.py`
   - Xóa 3 dòng (dòng 168-170):
     ```python
     if model_type == "gemma4":
         raise ValueError("Gemma 4 support is not ready yet, stay tuned!")
     ```
   - Xóa bytecode cache:
     ```bash
     rm -f ".../mlx_engine/__pycache__/generate.cpython-311.pyc"
     ```
3. Restart LM Studio

**Nguồn:** [Issue #1741](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues/1741)

## Related
- [[local-llm]] — Local AI context
- [[apple-silicon-llm-optimization]] — Apple Silicon optimization
- [[topic-workflow]] — Topic research workflow
- [[index]] — Wiki index
