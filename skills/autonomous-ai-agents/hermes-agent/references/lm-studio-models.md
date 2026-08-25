# LM Studio Model Management

> Created: 2026-05-06 | Updated: 2026-05-06
> Tested on: macOS, LM Studio.app

## Model Storage Location

**Wrong:** `~/Library/Application Support/LM Studio/` — this is browser/UI cache data
**Correct:** `~/.lmstudio/models/` — actual model files

```
~/.lmstudio/models/
├── lmstudio-community/   # Community uploads via LM Studio UI
├── nomic-ai/            # Embedding models
├── unsloth/             # Unsloth quantized models
└── mixedbread-ai/       # Embedding models
```

## Critical: Model Format Compatibility

### What Works via API Server (localhost:1234)

Only **GGUF format** models are accessible via the LM Studio API server.

```
curl http://localhost:1234/v1/models  # Lists only GGUF models
```

### What Does NOT Work via API

**MLX format** (Apple Silicon optimized) — `.safetensors` files from MLX repos — do NOT appear in `/v1/models` and cannot be used via the API server, even if downloaded to `~/.lmstudio/models/`.

Common MLX repos that won't work via API:
- `nightmedia/Qwen3.5-2B-mxfp4-mlx` — MXFP4 Apple Silicon format
- `mlx-community/*` repos — MLX format variants

**Specific failure case (2026-05-06):**
- Downloaded `nightmedia/Qwen3.5-2B-mxfp4-mlx/model.safetensors` (1.5GB) to `~/.lmstudio/models/lmstudio-community/Qwen3.5-2B-mxfp4/`
- LM Studio API showed: `qwen3.5-2b@mxfp4` in `/v1/models`
- But: `brv curate` with `@mxfp4` → `Failed to load model: Failed to load model`
- Root cause: MXFP4 format requires MLX runtime, LM Studio API uses llama.cpp backend

**Resolution:** Always use GGUF format for API-accessible models. For Apple Silicon optimization, load MLX models directly in LM Studio UI (not via API).

### Resolution Path

For small efficient models via LM Studio API:

1. **Search HuggingFace for GGUF quantization** of the model you want
   - Look for: `Qwen3.5-2B-GGUF`, `Qwen3.5-4B-GGUF`
   - Quantization types: Q4_K_M (balanced), Q5_K_S (better quality), Q8_0 (best quality, largest)

2. **Download GGUF file** to `~/.lmstudio/models/lmstudio-community/{model-name}/`

3. **Reload LM Studio** or click "Refresh" in LM Studio UI

4. **Verify** with `curl http://localhost:1234/v1/models`

## ByteRover-Compatible LM Studio Models (Verified 2026-05-06)

| Model | Curate | Query | Status | Notes |
|-------|--------|-------|--------|-------|
| **qwen3.5-4b-awq-instruct** | **~44s** | **~46s** | **✅ BEST** | Fastest, stable |
| google/gemma-4-e2b | ~76s | ~76s | ✅ Works | Reliable |
| google/gemma-4-e4b | ~87s | ~75s | ✅ Works | Slightly more VRAM |
| QuantTrio-Qwen3.5-4B-AWQ | ~85s | — | ⚠️ Slow | Occasional empty output |
| qwen3.5-0.8B | ❌ | — | ❌ | Too small for ByteRover |
| qwen3.6-35b-a3b | ❌ | — | ❌ | Too slow for LM Studio inference |

**Recommendation: `qwen3.5-4b-awq-instruct`** — ~45s curate/query, 3× faster than gemma-4-e2b.

### Setup Command

```bash
export PATH="$HOME/.brv-cli/bin:$PATH"

brv providers connect openai-compatible \
  --base-url http://localhost:1234/v1 \
  --model qwen3.5-4b-awq-instruct \
  --api-key "no-key"

# Verify
brv status
brv curate "Test qwen awq $(date)"
```

## Finding Small Efficient GGUF Models

Search patterns for HuggingFace:

```
Qwen3.5-2B GGUF      # Small autoregressive, ~1.5GB Q4
Qwen3.5-4B GGUF      # Mid-size, ~2.5GB Q4
Phi-3-mini-GGUF      # Microsoft small model
Qwen2.5-0.5B-GGUF    # Very small
```

AWQ (Activation-Aware Weight Quantization) models tend to be faster than naive GPTQ for the same size.

## LM Studio Server Lifecycle

- **Start server:** Open LM Studio → Developer tab → Start server
- **Check if running:** `lsof -i :1234` or `curl http://localhost:1234/v1/models`
- **Server persists** while LM Studio app is open
- **Models load** on first API call, stay in memory until LM Studio closes

## Reloading Models After Download

1. Open LM Studio
2. Go to Models tab
3. The downloaded model should appear — click to load
4. Or: Close + reopen LM Studio

You cannot reload models via API alone — must use the UI.
