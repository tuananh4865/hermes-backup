---
title: DPO (Direct Preference Optimization)
description: Direct Preference Optimization — stable, efficient method for aligning language models with human preferences without training a separate reward model.
tags:
  - alignment
  - fine-tuning
  - reinforcement-learning
  - llm
  - training
  - rl
created: 2026-04-20
---

# DPO (Direct Preference Optimization)

Direct Preference Optimization (DPO) is a stable and efficient method for aligning large language models (LLMs) with human preferences without requiring a separate reward model or reinforcement learning. It was introduced in the paper *"Direct Preference Optimization: Your Language Model is Secretly a Reward Model"* (Rafailov et al., 2023).

## Why DPO

Traditional RLHF (Reinforcement Learning from Human Feedback) requires:

1. **Training a reward model** from preference data
2. **Running RL optimization** (PPO) against that reward model
3. **Complex infrastructure** with separate reward and policy models

DPO simplifies this by directly fine-tuning the model on preference pairs, treating the reward model as a latent variable that can be optimized implicitly.

## How DPO Works

### The Core Insight

Instead of training a separate reward model, DPO recognizes that the policy model itself can serve as the reward signal through its log ratio of logits:

```python
# DPO Loss
def dpo_loss(policy_logps, ref_logps, chosen_logps, rejected_logps, beta=0.1):
    """
    policy_logps: log probabilities from the policy model
    ref_logps: log probabilities from the reference model
    chosen_logps: log probs for preferred response
    rejected_logps: log probs for dispreferred response
    beta: temperature controlling deviation from reference
    """
    # Compute implicit reward under DPO formulation
    chosen_rewards = beta * (chosen_logps - ref_logps)
    rejected_rewards = beta * (rejected_logps - ref_logps)

    # Bradley-Terry preference model
    loss = -torch.log_sigmoid(chosen_rewards - rejected_rewards)

    return loss.mean()
```

### Preference Data Format

DPO requires pairs of responses with human preference labels:

```json
{
  "prompt": "Explain quantum entanglement to a 10-year-old.",
  "chosen": "Imagine you and your friend have two magical coins...",
  "rejected": "Quantum entanglement is a phenomenon in quantum mechanics..."
}
```

## DPO vs RLHF vs PPO

| Aspect | DPO | RLHF (PPO) |
|--------|-----|------------|
| **Reward model** | Implicit (in policy) | Separate model required |
| **Stability** | ✅ Stable | ⚠️ Complex tuning |
| **Training time** | ~1x | ~3-5x |
| **Memory** | 2x model size | 3-4x model size |
| **Hyperparameters** | Fewer | Many (KL penalty, PPO clips, etc.) |
| **Convergence** | Direct | Iterative |
| **Implementation** | Simple fine-tuning loop | Complex RL loop |

## Implementing DPO

### Using Hugging Face TRL

```python
from trl import DPOTrainer
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B")

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    beta=0.1,
    train_dataset=dataset,
)

trainer.train()
```

### Using Microsoft Foundry SDK

```python
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model

# DPO fine-tuning with Azure ML
dpo_config = {
    "beta": 0.1,
    "learning_rate": 1e-6,
    "epochs": 3,
    "batch_size": 4
}

# Prepare preference dataset
dataset = prepare_preference_dataset(
    data_path="./preference_data.json",
    tokenizer=tokenizer
)

result = ml_client.jobs.create(
    name="dpo-finetune-llama",
    experiment="llm-alignment",
    inputs={"preference_data": dataset},
    compute="gpu-cluster"
)
```

## When to Use DPO

### Good Fit For

- **Response style tuning** — Make outputs more helpful, concise, or creative
- **Safety alignment** — Reduce harmful outputs without full RLHF
- **Domain adaptation** — Align with professional/domain-specific preferences
- **Iterative improvement** — Easy to run multiple rounds of preference feedback

### Limitations

- **Requires quality preference data** — Garbage in, garbage out
- **Not for complex reasoning tasks** — Less effective than PPO for multi-step reasoning
- **Reference model dependency** — Needs a strong reference to stay close to

## DPO Variants (2025-2026)

| Variant | Paper | Key Improvement |
|---------|-------|---------------|
| **DPO** | Rafailov et al. 2023 | Original formulation |
| **IPO** | Azar et al. 2024 | Identity preference optimization — no label annealing |
| **cDPO** | 2024 | Contrastive DPO — emphasize margin between chosen/rejected |
| **KTO** | 2024 | Kahneman-Tversky optimization — loss as human utility |
| **R-DPO** | 2025 | Recursive DPO — multi-turn preference alignment |

## Creating Preference Data

### Human Annotation

```json
[
  {
    "id": "sample_001",
    "prompt": "Write a haiku about autumn.",
    "responses": [
      {"id": "A", "text": "Leaves fall to the ground\nGolden colors all around\nAutumn's gentle breath"},
      {"id": "B", "text": "Autumn leaves descend, painting earth in amber hues, a fleeting dance"}
    ],
    "preference": "A"
  }
]
```

### LLM-as-Judge Generation

```python
from anthropic import Anthropic

def generate_preference(model_a_response, model_b_response, prompt):
    client = Anthropic()

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=50,
        messages=[{
            "role": "user",
            "content": f"""Given this prompt: {prompt}

Response A: {model_a_response}
Response B: {model_b_response}

Which response is better? Answer only A or B."""
        }]
    )

    return response.content[0].text.strip()
```

## DPO + LoRA

Combining DPO with LoRA for parameter-efficient alignment:

```python
from peft import LoraConfig
from trl import DPOTrainer

lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    beta=0.1,
    train_dataset=dataset,
    peft_config=lora_config,  # Apply LoRA
)

trainer.train()
# Only LoRA adapters are trained, not full model
```

## Evaluation

### MT-Bench with DPO Models

```python
from evalplus import evaluate

results = evaluate(
    model=finetuned_model,
    dataset="mt-bench",
    method="chat"
)

print(f"MT-Bench Score: {results['score']}")
```

## See Also

- [[alignment]] — AI alignment fundamentals
- [[fine-tuning]] — LLM fine-tuning methods
- [[RLHF]] — Reinforcement Learning from Human Feedback
- [[LoRA]] — Parameter-efficient fine-tuning
- [[llm-training]] — LLM training pipeline overview
