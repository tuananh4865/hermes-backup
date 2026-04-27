---
title: "Reinforcement Learning from Human Feedback"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [rlhf, reinforcement-learning, fine-tuning, alignment, training]
confidence: medium
relationships:
  - 🔗 fine-tuning
  - 🔗 dpo
  - 🔗 training
---

# Reinforcement Learning from Human Feedback (RLHF)

## Overview

RLHF is a technique for training AI models to align with human preferences by incorporating human feedback into the training process. It combines reinforcement learning with human guidance to improve model outputs, particularly for generating more helpful, harmless, and honest responses.

The technique gained prominence through InstructGPT and ChatGPT, demonstrating that human feedback could dramatically improve model utility while reducing harmful outputs. RLHF addresses the fundamental limitation of next-token prediction: models trained purely on text don't inherently understand what humans want.

## Key Concepts

### The Three-Stage Pipeline

**Stage 1: Supervised Fine-Tuning (SFT)**
Fine-tune base model on high-quality demonstration data:

```python
# SFT training loop
for batch in sft_dataloader:
    outputs = model(input_ids=batch.input_ids, labels=batch.labels)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
```

**Stage 2: Reward Model Training**
Train a model to predict human preferences:

```python
# Reward model: takes prompt + response, outputs scalar reward
reward_model = RewardModel(policy_model)

# Preference pairs: chosen > rejected
loss = -log(sigmoid(reward(chosen) - reward(rejected)))
```

**Stage 3: RL Fine-Tuning**
Optimize policy using reward model as signal:

```python
# PPO algorithm maximizes expected reward with KL penalty
for batch in rl_dataloader:
    responses = policy.generate(prompts)
    rewards = reward_model(prompts, responses)
    
    # KL divergence penalty prevents policy drift
    kl_penalty = kl_divergence(new_policy, old_policy)
    
    ppo_loss = -min(
        rewards * advantage,
        clip * advantage
    ) + beta * kl_penalty
```

### Reward Hacking

A critical failure mode where the model finds ways to maximize the reward signal without achieving the intended goal:

- **Rewarding incomplete answers**: Model learns to give short but "confident-sounding" responses
- **Gaming the reward model**: Exploiting patterns invisible to human raters
- **Mitigation**: Conservative reward bounds, iterative red-teaming

### KL Divergence Constraint

The KL penalty prevents the RL policy from diverging too far from the SFT model:

```
Final objective = Expected reward - beta * KL(pi_RL || pi_SFT)
```

Where beta controls how much the model can change during RL.

## Practical Applications

### Training a Preference Model

```python
from transformers import AutoModelForSequenceClassification

# Load base model and add reward head
reward_model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen2.5-0.5B",
    num_labels=1  # Scalar reward
)

# Preference data format
preference_data = [
    {
        "prompt": "What is Kubernetes?",
        "chosen": "Kubernetes is an open-source container orchestration platform...",
        "rejected": "K8s is a thing that does stuff with containers."
    }
]
```

### Implementing PPO

Modern LLM frameworks handle PPO complexity:

```python
from trl import PPOTrainer, AutoModelForCausalLMWithValueHead

config = PPOConfig(
    learning_rate=1.4e-5,
    batch_size=1,
    ppo_epochs=4,
    kl_penalty="kl"
)

ppo_trainer = PPOTrainer(config, model, ref_model, tokenizer)

for batch in ppo_dataloader:
    # Generate responses
    query_tensors = [tokenize(q) for q in batch["queries"]]
    response_tensors = [gen(q) for q in query_tensors]
    
    # Compute rewards
    texts = [q + r for q, r in zip(batch["queries"], batch["responses"])]
    rewards = reward_model(texts)
    
    # PPO step
    ppo_trainer.step(query_tensors, response_tensors, rewards)
```

### Comparison with Other Alignment Methods

| Method | Training Signal | Complexity | Quality |
|--------|----------------|------------|--------|
| SFT | Expert demonstrations | Low | Good |
| RLHF | Human preferences | High | Best |
| DPO | Preference pairs (no RL) | Medium | Comparable |
| RLAIF | AI preferences | Medium | Varies |

## Related

- [[fine-tuning]] — General fine-tuning techniques
- [[dpo]] — Direct Preference Optimization (RLHF alternative)
- [[training]] — ML training infrastructure
