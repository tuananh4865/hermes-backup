---
title: MLX
description: Apple's ML framework for Apple Silicon — optimized for ML inference and training
tags: [apple-silicon, ml, llm, local-llm, mlx]
---

# MLX

MLX is Apple's machine learning framework designed specifically for Apple Silicon (M-series chips), providing optimized inference and training with the unified memory architecture advantages.

## Overview

MLX brings a NumPy-like API to Apple Silicon, enabling efficient execution of ML models on M1/M2/M3/M4 chips with unified memory.

## Key Components

- **MLX Core**: NumPy-compatible array operations on Apple Silicon
- **MLX-LM**: Python package for running and fine-tuning LLMs
- **MLX-Audio**: Speech processing models
- **MLX-VLM**: Vision models for multimodal tasks

## Performance Advantages

Unified memory eliminates GPU VRAM constraints:
- Models up to 70B parameters can run on 64GB M-series Macs
- No data transfer overhead between CPU/GPU memory
- M5 Neural Accelerators extend capabilities further

## Related

- [[local-llm]]
- [[llm-inference-optimization]]
- [[apple-silicon]]
