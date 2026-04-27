---
title: Multi-Head Attention
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [multi-head-attention, transformer, deep-learning, attention-mechanism]
---

# Multi-Head Attention

## Overview

Multi-head attention is a fundamental component of the Transformer architecture that revolutionized natural language processing and beyond. Introduced in the seminal 2017 paper "Attention Is All You Need" by Vaswani et al., multi-head attention allows models to jointly attend to information from different representation subspaces at different positions. Rather than performing a single attention function, the mechanism runs several attention mechanisms in parallel, each learning to focus on different aspects of the input.

The key insight is that different attention heads can capture different types of relationships: some might focus on syntactic dependencies, others on semantic similarities, and others on positional relationships. By combining multiple heads, the model develops a richer understanding of context than would be possible with single-head attention.

## Key Concepts

**Attention Mechanism Fundamentals**

The attention function maps a query and key-value pairs to an output. The output is computed as a weighted sum of values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key. Scaled dot-product attention computes this as:

```
Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V
```

**Linear Projections**

Rather than applying attention directly to the raw input, multi-head attention first linearly projects the queries, keys, and values `h` times (typically 8 or 16) with different learned linear weights. Each projected version undergoes the attention computation in parallel, allowing different heads to attend to different positions.

**Concatenation and Linear Transform**

The outputs of all attention heads are concatenated and linearly transformed to produce the final value. This allows the model to combine information from all heads before passing it to the next layer.

**Parameter Efficiency**

Despite increasing the computational cost (each head operates on d_model/h dimensions), multi-head attention remains parameter-efficient because the total parameters are comparable to single-head attention with full dimensionality while providing vastly more representational capacity.

## How It Works

In multi-head attention, the input consists of queries (Q), keys (K), and values (V) derived from the previous layer's output. These are each linearly projected h times with different weight matrices. For each head, the scaled dot-product attention is computed, producing h outputs of dimension d_v. These are concatenated and once more linearly transformed to produce the final output.

During training, all projection matrices are learned jointly via backpropagation. Different heads often specialize during training, with some heads learning to capture positional patterns, others syntactic structure, and others semantic relationships.

## Practical Applications

**Machine Translation**

Multi-head attention enables Transformer models to capture long-range dependencies essential for translation. Different heads can learn to align words across languages, handle different grammatical structures, and manage context from arbitrary distances.

**Text Generation**

Large language models like GPT and Claude use multi-head attention to maintain coherence over long contexts. The attention mechanism allows the model to reference any previously generated token when producing the next one.

**Image Processing**

Vision Transformers (ViT) apply multi-head attention to image patches, learning to relate different regions of an image. This has achieved state-of-the-art results on image classification and detection tasks.

**Multimodal Understanding**

Multimodal models use multi-head attention to relate tokens across modalities—connecting text tokens to image regions, audio segments, or video frames for comprehensive understanding.

## Examples

```python
import torch
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        self.depth = d_model // num_heads
        
        self.wq = nn.Linear(d_model, d_model)
        self.wk = nn.Linear(d_model, d_model)
        self.wv = nn.Linear(d_model, d_model)
        self.dense = nn.Linear(d_model, d_model)
    
    def split_heads(self, x, batch_size):
        x = x.reshape(batch_size, -1, self.num_heads, self.depth)
        return x.permute(0, 2, 1, 3)
    
    def forward(self, q, k, v, mask=None):
        batch_size = q.size(0)
        
        q = self.split_heads(self.wq(q), batch_size)
        k = self.split_heads(self.wk(k), batch_size)
        v = self.split_heads(self.wv(v), batch_size)
        
        scores = torch.matmul(q, k.transpose(-1, -2))
        scores = scores / (self.depth ** 0.5)
        
        if mask is not None:
            scores += mask * -1e9
        
        attention_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, v)
        
        output = output.permute(0, 2, 1, 3).contiguous()
        output = output.reshape(batch_size, -1, self.d_model)
        
        return self.dense(output)
```

## Related Concepts

- [[self-attention]] — The core attention mechanism
- [[transformer-architecture]] — The architecture using multi-head attention
- [[attention-mechanism]] — General attention concepts
- [[large-language-models]] — LLMs built on attention
- [[vision-transformer]] — Attention for images

## Further Reading

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Original Transformer paper
- [Annotated Transformer](http://nlp.seas.harvard.edu/annotated-transformer/) — Line-by-line implementation guide
- [GPT-2 Paper](https://d4mucfpksywv.cloudfront.net/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) — Multi-head attention in practice

## Personal Notes

Multi-head attention remains one of the most elegant architectural innovations in deep learning. The fact that different heads naturally specialize without explicit supervision is remarkable and speaks to the richness of the representation space that emerges.
