---
title: "Attention"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ai, llm, transformer]
---

# Attention

## Overview

The attention mechanism is a foundational technique in modern large language models (LLMs) and deep learning that allows models to dynamically weigh the importance of different parts of input data when producing output. Introduced in the 2017 paper "Attention Is All You Need" by Vaswani et al., it revolutionized natural language processing by replacing recurrent neural networks with the [[transformer]] architecture.

At its core, attention enables a model to "focus" on relevant tokens in a sequence while processing each word or sub-word. Rather than reading text sequentially from left to right, attention mechanisms compute relationships between all positions simultaneously, capturing long-range dependencies and contextual relationships efficiently.

## Key Concepts

**Query, Key, and Value (QKV):** The attention mechanism operates using three learned vectors for each input position. The Query represents what the current position is looking for, the Key represents what each position offers as relevant, and the Value contains the actual information to be aggregated. The attention score is computed by measuring compatibility between Query and Key vectors using a scaled dot-product, then using these scores to weight the Value vectors.

**Self-Attention:** In self-attention, the Query, Key, and Value all come from the same input sequence. This allows each token to attend to all other tokens in the sequence, learning contextual relationships regardless of their distance. For example, in the sentence "The cat sat on the mat because it was tired," self-attention helps the model understand that "it" refers to "cat."

**Multi-Head Attention:** Rather than computing a single attention function, multi-head attention runs several attention mechanisms in parallel, each with different learned linear projections of the QKV vectors. This allows the model to attend to different types of relationships simultaneously—syntactic, semantic, or positional—before combining results. Modern LLMs like GPT-4 and Claude use dozens or hundreds of attention heads.

**Scaled Dot-Product Attention:** The mathematical formulation computes attention scores as `softmax(QK^T / sqrt(d_k))V`, where `d_k` is the dimensionality of the key vectors. The scaling factor prevents large dot products from saturating the softmax function during training.

## Why It Matters

Attention mechanisms solved critical limitations of earlier architectures. Recurrent networks struggled with long-range dependencies due to vanishing gradients and could not parallelize efficiently across sequences. Attention enables parallel processing, faster training, and better handling of context across thousands of tokens.

In production LLMs, attention is computationally intensive—the memory and compute grow quadratically with sequence length. This is why [[inference optimization]] techniques like [[kv-cache]] and [[FlashAttention]] are essential for making large models practical. Understanding attention is also crucial for diagnosing issues like attention sinks (where models disproportionately focus on specific tokens) and developing solutions like [[streaming]] [[inference]] optimizations.

## Related

- [[transformer]]
- [[self-attention]]
- [[multi-head attention]]
- [[kv-cache]]
- [[inference optimization]]
- [[FlashAttention]]
- [[streaming]]
