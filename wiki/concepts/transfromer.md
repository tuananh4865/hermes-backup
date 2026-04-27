---
title: "Transfromer"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, deep-learning, neural-networks, nlp]
---

# Transfromer

## Overview

The Transformer architecture is a neural network design introduced in the 2017 paper "Attention Is All You Need" by Vaswani et al. It revolutionized natural language processing and eventually became the foundation for modern large language models. The key innovation was replacing recurrent neural networks with a mechanism called self-attention, enabling parallel processing of sequences and capturing long-range dependencies more effectively.

Transformers process input sequences in parallel by attending to all positions simultaneously through multi-head attention. This architectural shift enabled training on vastly larger datasets and achieved state-of-the-art results across translation, text generation, sentiment analysis, and eventually virtually every NLP task. The architecture has since expanded beyond text to vision (Vision Transformers), audio, and multimodal tasks.

## Key Concepts

**Self-Attention**: The core mechanism allowing each position in a sequence to attend to all other positions. It computes attention weights based on learned query, key, and value representations, enabling the model to dynamically focus on relevant context regardless of distance.

**Multi-Head Attention**: Instead of performing a single attention function, Transformers run multiple attention heads in parallel, each learning different aspects of the relationships between tokens. This allows capturing diverse syntactic and semantic relationships simultaneously.

**Positional Encoding**: Since self-attention is inherently order-agnostic, positional encodings are added to input embeddings to inject sequence position information. These can be sinusoidal functions or learned embeddings.

**Feed-Forward Layers**: After each attention block, position-wise feed-forward networks process the representations, typically consisting of two linear transformations with a non-linear activation.

**Layer Normalization and Residual Connections**: Stabilize training and enable gradient flow through deep networks by normalizing layer outputs and adding skip connections.

## How It Works

A Transformer encoder processes input as follows:

1. **Input Embedding**: Tokens are converted to vectors via learned embeddings
2. **Positional Encoding**: Position information is added to embeddings
3. **Multi-Head Self-Attention**: Each position attends to all positions within the sequence
4. **Add & Norm**: Residual connection followed by layer normalization
5. **Feed-Forward**: Position-wise transformation processing
6. **Add & Norm**: Another residual and normalization step
7. **Output**: Final representation for each input position

```python
# Simplified self-attention in PyTorch
import torch
import torch.nn.functional as F
import math

def self_attention(query, key, value, mask=None):
    """
    Scaled dot-product attention.
    query, key, value: (batch, seq_len, d_k)
    """
    d_k = query.size(-1)
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    attention_weights = F.softmax(scores, dim=-1)
    return torch.matmul(attention_weights, value), attention_weights

# Multi-head attention combines multiple attention heads
class MultiHeadAttention(torch.nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        self.W_q = torch.nn.Linear(d_model, d_model)
        self.W_k = torch.nn.Linear(d_model, d_model)
        self.W_v = torch.nn.Linear(d_model, d_model)
        self.W_o = torch.nn.Linear(d_model, d_model)
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # Linear projections and reshape for multi-head
        Q = self.W_q(query).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(key).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(value).view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # Apply attention
        x, attn_weights = self_attention(Q, K, V, mask)
        
        # Concatenate heads and final linear
        x = x.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        return self.W_o(x)
```

## Practical Applications

The Transformer architecture powers virtually all modern language models and many vision systems:

- **Large Language Models**: GPT, BERT, Claude, and Gemini all build on Transformer foundations
- **Machine Translation**: Replaced sequence-to-sequence RNNs with superior performance
- **Text Classification**: Sentiment analysis, spam detection, topic classification
- **Question Answering**: Extractive and generative QA systems
- **Vision Transformers**: Image classification, object detection, image generation
- **Multimodal Models**: Combining text, images, audio through Transformer-based architectures

## Examples

**BERT for Text Classification**: Google's BERT (Bidirectional Encoder Representations from Transformers) pretrained on large corpora and fine-tuned for specific tasks:

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

inputs = tokenizer("Transformers revolutionized NLP!", return_tensors="pt")
labels = torch.tensor([1]).unsqueeze(0)  # Positive sentiment

outputs = model(**inputs, labels=labels)
loss = outputs.loss
logits = outputs.logits
```

## Related Concepts

- [[Self-Attention]] - The core mechanism underlying Transformers
- [[Neural Networks]] - The broader class of models Transformers belong to
- [[Large Language Models]] - Modern LLMs built on Transformer architecture
- [[BERT]] - Bidirectional Encoder representation from Transformers
- [[GPT]] - Generative Pretrained Transformer models
- [[Machine Learning]] - The broader field Transformers operate within

## Further Reading

- "Attention Is All You Need" (Vaswani et al., 2017)
- "The Illustrated Transformer" by Jay Alammar
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/)

## Personal Notes

The elegant simplicity of attention—"all you need" was an intentional statement against RNNs—is remarkable. What strikes me is how the same architecture scales from translation to image classification to protein structure prediction. The universality suggests attention is tapping into something fundamental about how complex systems represent relationships. The quadratic complexity of full attention remains a practical challenge for very long sequences.
