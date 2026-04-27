---
title: Attention Mechanism
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [attention, transformer, deep-learning, neural-networks]
---

# Attention Mechanism

The attention mechanism is a fundamental technique in deep learning that allows neural networks to weigh the importance of different parts of the input when processing each element. It enables models to dynamically focus on relevant information across long sequences, solving the limitations of earlier recurrent architectures that struggled with long-range dependencies.

## Overview

Introduced in the seminal 2015 paper "Attention Is All You Need" by Vaswani et al., the attention mechanism revolutionized natural language processing and beyond. Before attention, sequence-to-sequence models relied on fixed-size context windows or suffered from vanishing gradients when processing long sequences. Attention solved this by allowing every output position to access every input position, with relevance scored by learned weights.

The mechanism computes a weighted sum of values, where weights are determined by the similarity between queries and keys. This allows the model to "attend to" the most relevant parts of the input dynamically, regardless of distance in the sequence.

## Key Concepts

### Query, Key, and Value (QKV)

The attention mechanism operates on three vectors derived from the input:
- **Query (Q)**: What the current position is looking for
- **Key (K)**: Information available at each position that helps determine relevance
- **Value (V)**: The actual content to be aggregated based on attention weights

Attention is computed as: `softmax(QK^T / √d_k) V`

### Scaled Dot-Product Attention

The most common form uses scaled dot-product attention, where:
```python
import torch
import torch.nn.functional as F

def scaled_dot_product_attention(Q, K, V, mask=None):
    d_k = Q.size(-1)
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    attention_weights = F.softmax(scores, dim=-1)
    return torch.matmul(attention_weights, V), attention_weights
```

### Multi-Head Attention

Rather than performing a single attention function, multi-head attention runs several in parallel, allowing the model to attend to different representation subspaces:
```python
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_model = d_model
        self.depth = d_model // num_heads
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def split_heads(self, x, batch_size):
        x = x.reshape(batch_size, -1, self.num_heads, self.depth)
        return x.transpose(1, 2)
```

## How It Works

1. **Linear Projections**: Input embeddings are linearly projected into Q, K, V spaces
2. **Attention Scoring**: Compute similarity between queries and keys using dot-product
3. **Scaling**: Scale by √d_k to prevent large dot products from dominating after softmax
4. **Softmax**: Apply softmax to get normalized attention weights (sum to 1)
5. **Weighted Sum**: Multiply attention weights by values and aggregate

In self-attention, Q, K, and V all come from the same source. Cross-attention uses Q from one sequence while K, V come from another.

## Practical Applications

- **Machine Translation**: Align source and target words during translation
- **Text Summarization**: Focus on key sentences while generating summaries
- **Question Answering**: Locate relevant context passages for answering questions
- **Image Captioning**: Attend to relevant image regions while generating descriptions
- **Speech Recognition**: Align audio frames with text tokens

## Examples

Transformer models use attention as their primary computation:

```python
# Simplified transformer encoder layer
class EncoderLayer(nn.Module):
    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff)
        self.layernorm1 = nn.LayerNorm(d_model)
        self.layernorm2 = nn.LayerNorm(d_model)
    
    def forward(self, x, mask):
        attn_output, _ = self.self_attn(x, x, x, mask)
        x = self.layernorm1(x + attn_output)
        ffn_output = self.ffn(x)
        return self.layernorm2(x + ffn_output)
```

## Related Concepts

- [[self-attention]] — Self-attention mechanism where Q, K, V come from same sequence
- [[transformer]] — Architecture based entirely on attention mechanisms
- [[large-language-models]] — LLMs built on transformer/attention foundations
- [[neural-network]] — Broader category of models that include attention

## Further Reading

- "Attention Is All You Need" (Vaswani et al., 2017)
- "Neural Machine Translation by Jointly Learning to Align and Translate" (Bahdanau et al., 2015)
- The Illustrated Transformer (Jay Alammar's blog)

## Personal Notes

The breakthrough of attention was realizing that we don't need recurrence at all—pure attention mechanisms can capture dependencies as well or better than RNNs, while being much more parallelizable. The quadratic complexity of attention (O(n²)) remains a challenge for very long sequences, driving research into efficient variants like linear attention and sparse attention.
