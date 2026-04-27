---
title: Self-Attention
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [attention, transformer, nlp, deep-learning, neural-networks]
---

# Self-Attention

## Overview

Self-attention, also known as scaled dot-product attention, is a mechanism that allows elements in a sequence to interact with and depend on each other regardless of their positional distance. Introduced in the "Attention Is All You Need" paper (Vaswani et al., 2017), self-attention became the foundational building block of the Transformer architecture, revolutionizing natural language processing and eventually spreading to computer vision, audio processing, and multimodal AI. Unlike recurrent neural networks that process sequences step-by-step, self-attention computes relationships between all pairs of positions in a sequence simultaneously, making it highly parallelizable and effective at capturing long-range dependencies.

The key innovation of self-attention is its ability to dynamically weight the importance of different parts of the input when processing each element. When processing the word "bank" in "I deposited money at the bank by the river," self-attention allows the model to attend to "deposited" and "money" to determine that "bank" refers to a financial institution, rather than a riverbank. This dynamic weighting mechanism enables the model to contextually understand each element based on its relationships with all other elements, rather than relying on fixed positional embeddings or rigid hierarchical structures.

## Key Concepts

### The Attention Mechanism

At its core, self-attention computes a weighted sum of values, where the weights are determined by the compatibility between queries and keys:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

Where:
- **Q (Query)** - What am I looking for?
- **K (Key)** - What do I contain?
- **V (Value)** - What information should I provide?

The scaling factor `√d_k` prevents the dot products from growing too large in high dimensions, which would push softmax into regions with extremely small gradients.

### Multi-Head Attention

Rather than performing a single attention function, multi-head attention runs several attention mechanisms in parallel:

```python
class MultiHeadAttention(torch.nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = torch.nn.Linear(d_model, d_model)
        self.W_k = torch.nn.Linear(d_model, d_model)
        self.W_v = torch.nn.Linear(d_model, d_model)
        self.W_o = torch.nn.Linear(d_model, d_model)
    
    def forward(self, x):
        batch_size = x.size(0)
        
        # Linear projections and split into heads
        Q = self.W_q(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(x).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Scaled dot-product attention
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        attn_weights = F.softmax(scores, dim=-1)
        attn_output = torch.matmul(attn_weights, V)
        
        # Concatenate heads and project
        concat = attn_output.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        return self.W_o(concat)
```

Each attention head can learn to focus on different aspects of the relationships:
- One head might focus on syntactic relationships (subject-verb)
- Another might focus on coreference (what does "it" refer to?)
- Another might focus on semantic similarity

### Computational Complexity

A key advantage of self-attention is that its computational complexity scales quadratically with sequence length:

| Sequence Length | Self-Attention | Recurrent (RNN) |
|-----------------|----------------|-----------------|
| Per-layer | O(n² · d) | O(n · d²) |
| Long sequences | Expensive | Linear growth |

While O(n²) seems expensive, self-attention's parallelizability and lack of sequential dependency often makes it faster than RNNs in practice for reasonable sequence lengths. For very long sequences, various efficient attention variants (sparse attention, linear attention, flash attention) have been developed.

## How It Works

### Step-by-Step Attention Computation

1. **Project inputs** - The input sequence is linearly transformed into query, key, and value matrices.

2. **Compute similarity scores** - For each position i, compute dot products between query i and all keys:
   ```
   score(i,j) = Q[i] · K[j]^T
   ```

3. **Scale** - Divide scores by √d_k to prevent large dot products.

4. **Apply softmax** - Convert scores to probabilities (attention weights):
   ```
   attn_weight(i,j) = softmax(score(i,j))
   ```

5. **Weighted sum** - For each position i, compute weighted sum of all values:
   ```
   output[i] = Σ attn_weight(i,j) * V[j]
   ```

### Positional Encoding

Since self-attention is inherently position-agnostic (it treats the input as a set, not a sequence), positional information must be injected:

```python
class PositionalEncoding(torch.nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        # Precompute positional encodings
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len).unsqueeze(1).float()
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        return x + self.pe[:x.size(1)]
```

## Practical Applications

### When to Use Self-Attention

Self-attention excels when:
- Long-range dependencies are important
- The relationships between all pairs of positions matter
- Parallel computation is available (GPUs/TPUs)
- Interpretability of attention patterns is desired

### Common Architectures Using Self-Attention

| Architecture | Attention Type | Use Case |
|--------------|---------------|----------|
| Original Transformer | Full self-attention | Translation, text generation |
| BERT | Bidirectional self-attention | Text classification, NER |
| GPT | Causal (masked) self-attention | Text generation |
| Vision Transformer | Image patches attention | Image classification |
| Perceiver IO | Cross-attention | Multimodal tasks |

## Examples

### Minimal Self-Attention Implementation

```python
import torch
import torch.nn.functional as F
import math

def self_attention(Q, K, V, mask=None):
    """
    Q, K, V: (batch, seq_len, d_k)
    mask: (batch, seq_len, seq_len) - optional attention mask
    """
    d_k = Q.size(-1)
    
    # Compute attention scores
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    
    # Apply mask if provided (e.g., causal mask for GPT)
    if mask is not None:
        scores = scores.masked_fill(mask == 0, float('-inf'))
    
    # Softmax to get attention weights
    attn_weights = F.softmax(scores, dim=-1)
    
    # Weighted sum of values
    output = torch.matmul(attn_weights, V)
    
    return output, attn_weights

# Example usage
batch_size, seq_len, d_model = 2, 10, 64
d_k = d_model  # In practice, d_k often equals d_model / num_heads

Q = torch.randn(batch_size, seq_len, d_k)
K = torch.randn(batch_size, seq_len, d_k)
V = torch.randn(batch_size, seq_len, d_k)

output, weights = self_attention(Q, K, V)
print(f"Output shape: {output.shape}")      # (2, 10, 64)
print(f"Attention weights: {weights.shape}")  # (2, 10, 10)
```

### Causal (Unidirectional) Attention

For text generation, we need causal attention to prevent attending to future tokens:

```python
def create_causal_mask(seq_len):
    """Create a mask that prevents attending to future positions"""
    mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1).bool()
    return mask.unsqueeze(0)  # (1, seq_len, seq_len)

seq_len = 5
mask = create_causal_mask(seq_len)
print(mask)
# tensor([[[ True, False, False, False, False],
#          [ True,  True, False, False, False],
#          [ True,  True,  True, False, False],
#          [ True,  True,  True,  True, False],
#          [ True,  True,  True,  True,  True]]])
# True = masked (cannot attend), False = allowed
```

## Related Concepts

- [[transformer]] — The architecture built on self-attention
- [[multi-head-attention]] — Parallel attention heads
- [[attention-mechanism]] — General attention in neural networks
- [[positional-encoding]] — Injecting position information
- [[bert]] — Bidirectional transformer model
- [[gpt]] — Generative pre-trained transformer
- [[vision-transformer]] — Self-attention for images

## Further Reading

- [Attention Is All You Need (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer - Jay Alammar](http://jalammar.github.io/illustrated-transformer/)
- [FlashAttention Paper](https://arxiv.org/abs/2205.14135)
- [BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805)

## Personal Notes

Self-attention's elegance lies in its simplicity—the same operation repeated for every position. When I first implemented it from scratch, the key insight was understanding that attention weights are data-dependent: they're not fixed patterns but computed dynamically based on content. This is what makes self-attention so powerful compared to fixed convolutional kernels or static positional encodings. I've also found attention visualizations invaluable for debugging—when a model behaves unexpectedly, looking at attention patterns often reveals what relationships it's actually learning to capture.
