---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 synthetic-data (extracted)
  - 🔗 apple-silicon-llm-optimization (extracted)
  - 🔗 local-llm (extracted)
relationship_count: 3
---

# Fine-tuning

## Overview

Fine-tuning is the process of taking a pre-trained model and continuing training on a specific dataset to adapt it for a particular task or domain.

## Why Fine-tune?

### Benefits
- **Specialization**: Adapt model to specific domain
- **Smaller models, better results**: Fine-tuned 0.5B > general 7B on specific tasks
- **Cost effective**: Train once, use forever

### Traditional Fine-tuning vs PEFT

**Traditional**: Train ALL parameters
- Requires massive GPU resources
- Full model duplication

**PEFT (Parameter-Efficient Fine-Tuning)**: Train only some parameters
- LoRA, QLoRA, Adapter methods
- Can fine-tune 7B model on single MacBook

## PEFT Methods

### LoRA (Low-Rank Adaptation)
- Injects trainable matrices into attention layers
- Freeze original weights
- Rank (r) typically 8-64

### QLoRA (Quantized LoRA)
- Quantizes base model to 4-bit
- Trains LoRA adapters on quantized model
- Can fine-tune 65B model on single 48GB GPU

## Fine-tuning for Anh's Wiki

### Goal
Create a model that "knows" Anh's wiki content.

### Pipeline
1. Generate Q&A pairs from wiki
2. Fine-tune with LoRA/QLoRA
3. Evaluate on knowledge retrieval tasks

### Target Models
- **SmolLM2-360M**: Smallest, fastest, baseline
- **Qwen2.5-0.5B**: Small but capable

## Related
- [[synthetic-data]] — Training data generation
- [[apple-silicon-llm-optimization]] — Hardware optimization
- [[local-llm]] — Where fine-tuned model would run
- [[index]] — Wiki index
