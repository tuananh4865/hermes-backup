---
confidence: medium
last_verified: 2026-04-10
relationships:
  - 🔍 lora (inferred)
  - 🔍 fine-tuning (inferred)
  - 🔍 peft (inferred)
  - 🔍 axolotl (inferred)
  - 🔍 local-llm (inferred)
relationship_count: 5
---

# QLoRA (Quantized Low-Rank Adaptation)

## Overview

**QLoRA** (Quantized Low-Rank Adaptation) is an efficient fine-tuning technique that combines 4-bit quantization with Low-Rank Adaptation (LoRA) to enable training of massive language models on consumer-grade hardware. Published in paper [2305.14314](https://arxiv.org/abs/2305.14314) by Tim Dettmers et al. (2023).

## The Problem: Fine-Tuning is Expensive

Full fine-tuning a 65B parameter model requires ~780GB of VRAM (16-bit weights + gradients + optimizer states). That's impossible on any consumer GPU.

## How QLoRA Works

QLoRA combines two memory-saving techniques:

```
Full Fine-tune:     65B params × 16-bit = 130GB base model
                         + gradients + optimizers = 780GB total VRAM

LoRA:               65B frozen params + tiny adapter (few MB)
                         + gradients + optimizers for adapters only

QLoRA:              65B frozen params quantized to 4-bit (~33GB)
                         + tiny adapter (16-bit, few MB)
                         + gradients + optimizers for adapters only
                         = ~48GB total VRAM ✓
```

### Key Components

1. **4-bit Quantization (NF4)**
   - Normal Float 4-bit (NF4) data type
   - Stores weights in 4-bit instead of 16-bit
   - Reduces model size by 4x with minimal accuracy loss

2. **Low-Rank Adaptation (LoRA)**
   - Freezes base model weights
   - Adds small trainable adapter matrices (A and B)
   - Only trains ~0.1% of parameters

3. **Quantization Forward Pass**
   - Dequantizes weights on-the-fly during forward pass
   - No accuracy loss during inference

## Memory Comparison

| Method | 7B Model | 13B Model | 33B Model | 65B Model |
|--------|----------|-----------|-----------|-----------|
| **Full Fine-tune** | ~140GB | ~260GB | ~660GB | ~1300GB |
| **LoRA** | ~14GB | ~26GB | ~66GB | ~130GB |
| **QLoRA** | ~6GB | ~12GB | ~30GB | ~48GB |

QLoRA can fine-tune a 65B model on a single 48GB GPU (like RTX 4090 or A100 48GB).

## Implementation with PEFT + BitsAndBytes

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="bfloat16"
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-70b-hf",
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# LoRA config
lora_config = LoraConfig(
    r=64,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Add LoRA adapters
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 33,507,520 || all params: 33,507,520 || trainable%: 0.0980
```

## LoRA Hyperparameters

| Parameter | Description | Typical Values |
|-----------|-------------|----------------|
| `r` | Rank of decomposition | 8, 16, 32, 64 |
| `lora_alpha` | Scaling factor | 2×r or 1×r |
| `target_modules` | Which layers to adapt | q_proj, v_proj (attention) |
| `lora_dropout` | Dropout for regularization | 0.05 - 0.1 |

Higher `r` = more capacity but more parameters to train.

## QLoRA vs LoRA vs Full Fine-tuning

| Aspect | Full Fine-tune | LoRA | QLoRA |
|--------|---------------|------|-------|
| **VRAM** | Highest | Medium | Low |
| **Trainable Params** | 100% | 0.1-1% | 0.1-1% |
| **Accuracy** | Best | ~95% of full | ~99% of full |
| **Speed** | Slowest | Fast | Fast |
| **Hardware** | Multi-GPU cluster | 1× high-end GPU | 1× consumer GPU |
| **Cost** | $1000s | $100s | $10s |

## Use Cases

- **Domain adaptation**: Medical, legal, financial specialized models
- **Instruction tuning**: Converting base models to chatbots
- **Character/persona training**: Teaching models specific speaking styles
- **Multi-task adapters**: Different LoRA adapters for different tasks on one base model

## Training Tips

1. **Use `prepare_model_for_kbit_training()`** — Essential for proper gradient flow
2. **Gradient checkpointing** — Saves more memory: `model.gradient_checkpointing_enable()`
3. **Use bf16** — Better for training than fp16
4. **Learning rate scheduling** — Cosine decay works well with LoRA
5. **Adapter merging** — Merge adapters for faster inference: `model.merge_and_unload()`

## Tools & Libraries

| Library | Purpose |
|---------|---------|
| **PEFT** (HuggingFace) | LoRA/QLoRA adapters |
| **BitsAndBytes** | 4-bit quantization |
| **Trl** | Training utilities |
| **Axolotl** | Full fine-tuning pipeline |
| **Unsloth** | 2× faster training, 50% less memory |

## Fine-tuning on Wiki Content

For fine-tuning on Anh's wiki content:

```python
# QLoRA on Hermes wiki corpus
base_model = "meta-llama/Llama-3-8B"
output_dir = "~/wiki/fine-tuned-wiki/"

# Training config optimized for wiki content
training_args = TrainingArguments(
    output_dir=output_dir,
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    optim="paged_adamw_32bit",
    learning_rate=2e-4,
    weight_decay=0.01,
    fp16=False,
    bf16=True,
    logging_steps=10,
    save_steps=100,
)
```

## Related

- [[lora]] — LoRA foundation concept
- [[fine-tuning]] — Full fine-tuning comparison
- [[peft]] — Parameter-efficient fine-tuning library
- [[axolotl]] — Fine-tuning workflow tool
- [[local-llm]] — Running models locally