---
title: "Pre-training"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, deep-learning, nlp, llm, training]
---

# Pre-training

## Overview

Pre-training is the initial phase of training a machine learning model on a large, diverse dataset to learn general representations, patterns, and knowledge before the model is fine-tuned on a specific downstream task. In the context of large language models (LLMs), pre-training involves self-supervised learning on massive text corpora (trillions of tokens) where the model learns language structure, world knowledge, reasoning abilities, and broad competencies—all without any task-specific labels.

Pre-training is what makes modern foundation models powerful. Instead of training from scratch for each task, models first learn general capabilities during pre-training, then acquire specialized skills during fine-tuning. This two-stage paradigm dramatically reduces the labeled data and compute required to build useful AI systems. The quality and scale of pre-training directly determines what a model can learn later—smaller or lower-quality pre-training runs produce models that fine-tune poorly regardless of how much task-specific data is used.

## Key Concepts

### Self-Supervised Learning

During pre-training, models learn without human labels by predicting masked or next tokens from context. Two dominant approaches:

**Causal Language Modeling (CLM)**: Predict the next token given all previous tokens. GPT-style models (GPT-2, GPT-3, GPT-4) use this approach.

**Masked Language Modeling (MLM)**: Predict randomly masked tokens from surrounding context. BERT-style models use this approach, where the model sees tokens on both sides of the mask.

```python
# Causal Language Modeling (next token prediction)
input_ids = tokenizer("The capital of France is", return_tensors="pt")
# Model predicts: "Paris"
logits = model(input_ids)
next_token_logits = logits[:, -1, :]

# Masked Language Modeling
masked = tokenizer("The capital of [MASK] is Paris", return_tensors="pt")
# Model predicts: "France"
masked_logits = model(masked)
```

### Scaling Laws

Model performance improves predictably with:
- **Model size** (parameters): Larger models learn faster and achieve better performance
- **Dataset size** (tokens): More diverse training data improves generalization
- **Compute** (FLOPs): More training compute enables learning harder concepts

Chinchilla scaling laws suggest model size and training tokens should scale roughly proportionally—optimal performance comes from balancing all three factors rather than inflating one at the expense of others.

### Knowledge in Pre-training

Pre-training encodes:
- **Language syntax and grammar**: Learned from billions of sentences
- **World knowledge and facts**: Encoded in transformer attention patterns
- **Reasoning patterns**: Implicit problem-solving strategies
- **Common sense**: Physical and social reasoning
- **Style and format**: Writing patterns, code conventions, etc.

## How It Works

The pre-training pipeline involves:

1. **Data Collection**: Gathering diverse text from books, websites, code, scientific papers, and other sources
2. **Data Processing**: Filtering, deduplication, quality scoring, tokenization
3. **Training Loop**: Running stochastic gradient descent on batched sequences for billions of tokens
4. **Periodic Evaluation**: Measuring loss on held-out validation sets
5. **Checkpointing**: Saving intermediate model weights for potential reuse

```python
# Simplified pre-training loop (pseudo-code)
model = TransformerModel(vocab_size=50000, dim=4096, n_layers=32)
optimizer = AdamW(learning_rate=1e-4, weight_decay=0.1)

for step in range(num_training_steps):
    # Sample batch of text sequences
    batch = sample_batch(training_corpus, batch_size=4096)
    
    # Forward pass - causal language modeling
    logits = model(batch.input_ids)
    
    # Compute next-token prediction loss
    loss = cross_entropy(logits[:, :-1], batch.input_ids[:, 1:])
    
    # Backward pass and optimization
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    
    # Log and evaluate periodically
    if step % 1000 == 0:
        val_loss = evaluate(model, validation_set)
        logger.log(step=step, train_loss=loss, val_loss=val_loss)
```

## Practical Applications

- **Foundation Models**: GPT-4, Claude, Gemini, and similar models all begin as pre-trained base models
- **Domain Adaptation**: Pre-trained models fine-tuned for medical, legal, or scientific domains
- **Multi-modal Learning**: Models pre-trained on image-text pairs (CLIP) or audio-text (Whisper)
- **Transfer Learning**: Using pre-trained representations for downstream tasks like classification or extraction

## Examples

**GPT Pre-training**: GPT-3 was pre-trained on 300 billion tokens from Common Crawl, WebText, books, and Wikipedia. This single pre-training phase gave it the ability to write text, translate languages, answer questions, and reason about novel problems.

**BERT Pre-training**: BERT was pre-trained on 3.3 billion tokens using masked language modeling, enabling bidirectional context understanding. This pre-trained model fine-tuned to achieve state-of-the-art results on sentiment analysis, question answering, and named entity recognition.

**Code Models**: Code LLMs like Codex and StarCoder pre-trained on billions of lines of code from GitHub, learning syntax patterns, API usage, and algorithmic logic that transfers to code completion and generation tasks.

## Related Concepts

- [[fine-tuning]] — Adapting pre-trained models to specific tasks
- [[large-language-models]] — The primary application of pre-training
- [[self-supervised-learning]] — The learning paradigm used in pre-training
- [[transformer-architecture]] — The neural network architecture enabling pre-training at scale
- [[instruction-tuning]] — A specific fine-tuning approach for aligning models

## Further Reading

- [Kaplan et al. (2020): Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)
- [Hoffmann et al. (2022): Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)
- [Radford et al. (2019): Language Models are Unsupervised Multitask Learners (GPT-2)](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf)

## Personal Notes

Pre-training is computationally expensive—training GPT-3 required millions of dollars of GPU time—but it's also where the magic happens. The rule of thumb: if a model capability isn't present in pre-training, fine-tuning typically can't create it from nothing. This is why frontier labs spend so much effort on data quality and curriculum design during pre-training. For practitioners: understand what your base model learned during pre-training before assuming fine-tuning will fix its limitations. Sometimes the real leverage is choosing a better pre-trained model rather than fine-tuning a weaker one.
