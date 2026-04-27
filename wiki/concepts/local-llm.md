---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 lm-studio (extracted)
  - 🔗 models (extracted)
  - 🔗 apple-silicon-llm-optimization (extracted)
relationship_count: 3
---

# Local LLM

## Overview

Local LLM inference cho phép chạy models trên máy local (Mac M-series) thay vì cloud providers.

## Why Local AI?

### Privacy Benefits
- Data never leaves the device
- No API calls = no data collection
- Perfect for sensitive content

### Cost Benefits
- No per-token API costs
- One-time hardware investment
- Unlimited inference after setup

### Latency Benefits
- No network roundtrip
- Consistent response time
- Works offline

## Setup

### LM Studio
- **Address**: 192.168.0.187:1234
- **Default Model**: qwen3.5-2b-mlx
- **Purpose**: Content transcription, wiki operations

### MLX (Apple Silicon)
- Apple's ML framework
- Optimized for M-series chips
- Supports quantized models

## Philosophy

> Local models are for **COPYIST tasks ONLY** — reformat/transcribe content provided by user. NOT for reasoning or searching information.

## Related

- [[lm-studio]] — LM Studio server setup
- [[models]] — Model catalog
- [[apple-silicon-llm-optimization]] — Hardware optimization
