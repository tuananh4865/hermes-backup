# Vision Model Benchmarks (LM Studio via localhost:1234)

**Last updated:** 2026-05-03
**Context:** Hermes Agent auxiliary.vision with LM Studio custom endpoint

## Benchmark Results

| Model | Time (seconds) | Notes |
|-------|---------------|-------|
| `google/gemma-4-e2b` | ~20 | **WINNER** — fastest + good quality |
| `google/gemma-4-e4b` | N/A | Larger variant, same quality as e2b |
| `qwen3.5-0.8b` | ~27 | Slower despite being "smaller" |

## Key Insight: Cross-Architecture Comparison

**"Smaller = faster" only holds within the same architecture family.**

Cross-architecture comparisons are dominated by:
1. **Quantization level** — Q4 (4-bit) model can be faster than Q8 (8-bit) model with more params
2. **Architecture optimization** — Gemma may have hardware acceleration benefits in LM Studio
3. **Vision-specific tuning** — gemma-4-e2b is a VL model; qwen3.5-0.8b is a general model used for vision
4. **KV cache / batching efficiency** — model fits cache differently

## Current Config

```yaml
auxiliary:
  vision:
    provider: custom
    model: google/gemma-4-e2b
    base_url: http://localhost:1234/v1
    api_key: none
    timeout: 120
```

## LM Studio Models Available

```
http://localhost:1234/v1/
├── google/gemma-4-e2b       ← currently active
├── google/gemma-4-e4b
├── qwen3.5-0.8b-mlx
└── qwen3.6-35b-a3b
```

## How to Benchmark

```bash
# 1. Switch model
hermes config set auxiliary.vision.model "google/gemma-4-e4b"

# 2. Open browser + capture
browser_navigate(url="https://example.com")
browser_vision(annotate=false, question="Describe this image in detail")

# 3. Note time from response timestamp delta

# 4. Switch back to preferred model
hermes config set auxiliary.vision.model "google/gemma-4-e2b"
```
