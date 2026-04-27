---
confidence: medium
last_verified: 2026-04-10
relationships:
  - 🔍 qlora (inferred)
  - 🔍 axolotl (inferred)
relationship_count: 2
---

# PEFT (Parameter-Efficient Fine-Tuning)

PEFT is a library for parameter-efficient fine-tuning of pretrained models, providing methods like LoRA, QLoRA, and other adapter-based techniques.

## Overview

PEFT enables fine-tuning large language models with minimal computational cost by only updating a small subset of parameters.

## Supported Methods

- **LoRA**: Low-Rank Adaptation
- **QLoRA**: Quantized LoRA with 4-bit base model
- **AdaLoRA**: Adaptive LoRA
- **IA³**: Infused Adapter by Inhibiting and Amplifying Inner Activations
- **Prefix Tuning**: Virtual tokens as prefixes

## Use Cases

- Domain adaptation with limited data
- Task-specific fine-tuning without full model retraining
- Efficient model personalization

## Related

- [[qlora]] — QLoRA technique combining quantization + LoRA
- [[axolotl]] — Fine-tuning workflow tool supporting PEFT
