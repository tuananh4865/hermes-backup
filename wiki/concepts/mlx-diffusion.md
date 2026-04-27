---
title: MLX Diffusion — Image Generation on Apple Silicon
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [mlx, apple-silicon, image-generation, stable-diffusion, diffusionkit]
related:
  - [[apple-silicon-mlx-llm]]
  - [[diffusion-models]]
---

# MLX Diffusion — Image Generation on Apple Silicon

MLX brings high-performance image generation to Apple Silicon, enabling local Stable Diffusion and diffusion models without cloud dependencies.

## DiffusionKit

DiffusionKit (argmaxinc/DiffusionKit) is a core library for on-device image generation on Apple Silicon:

- **Native MLX implementation** — Optimized for Apple Neural Engine
- **Stable Diffusion support** — SD 1.5, SDXL, SD 3.x families
- **LoRA fine-tuning** — Customize styles locally
- **Image-to-image** — Variation and editing pipelines

## mlx.studio

mlx.studio provides an all-in-one interface for Mac AI:

- **Chat interface** — Conversational AI (MLX-LM)
- **Code assistance** — Coding with local models
- **Image generation** — Stable Diffusion via MLX
- **Privacy-first** — Everything runs on-device

## Performance on Apple Silicon

| Hardware | Model | Images/min |
|----------|-------|-----------|
| MacBook Pro M3 | SD 1.5 (512x512) | 3-5 |
| Mac Studio M2 Ultra | SDXL (1024x1024) | 2-4 |
| Mac Pro M4 | SD 3.x (1024x1024) | 4-6 |

## Use Cases

1. **Personalized art** — Fine-tune on personal photos for custom styles
2. **Product mockups** — Generate product images locally
3. **Design iteration** — Rapid visual exploration without cloud costs
4. **Privacy-sensitive imaging** — Medical, legal, or personal images never leave device

## Related

- [[apple-silicon-mlx-llm]] — LLMs on Apple Silicon
- [[diffusion-models]] — Diffusion model fundamentals
