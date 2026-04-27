---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 local-llm (extracted)
relationship_count: 1
---

# Deep Learning Theory

## Core Concepts

### Neural Networks as Function Approximators

A neural network approximates a function f(x) → y by composing many simple transformations. Each layer applies:

```
output = activation(W @ input + b)
```

Where:
- `W` is the weight matrix
- `b` is the bias
- `activation` is a non-linear function (ReLU, GELU, etc.)

### The Universal Approximation Theorem

Any continuous function can be approximated by a sufficiently large neural network with one hidden layer. In practice, depth (many layers) is more efficient than width (many neurons per layer).

### Backpropagation

The algorithm for training neural networks:

1. **Forward pass**: Compute output and loss
2. **Backward pass**: Compute gradients via chain rule
3. **Update weights**: Adjust parameters in direction opposite to gradient

```python
loss.backward()  # Compute gradients
optimizer.step()  # Update weights
```

## Key Optimization Concepts

### Gradient Descent Variants

| Method | Update Rule | Notes |
|--------|-------------|-------|
| SGD | θ = θ - lr * ∇L | Simple, needs tuning |
| Adam | Adaptive moments | Default for most tasks |
| AdamW | Adam + weight decay | Better regularization |

### Learning Rate Scheduling

- **Cosine annealing**: Smooth decay following cosine curve
- **Warmup**: Start small, increase, then decay
- **Reduce on plateau**: Lower LR when loss plateaus

### Regularization

Techniques to prevent overfitting:
- **Dropout**: Randomly zero activations during training
- **Weight decay**: L2 penalty on weights
- **Early stopping**: Stop when validation loss increases
- **Data augmentation**: Increase effective dataset size

## Transformers

The dominant architecture for sequence modeling:

```
Input → Embedding → [Attention + FFN] × N → Output
```

### Attention Mechanism

```
Attention(Q, K, V) = softmax(QK^T / √d) V
```

- Q (Query): What am I looking for?
- K (Key): What do I contain?
- V (Value): What information do I have?

### Why Multi-Head Attention?

Multiple attention heads allow the network to attend to different aspects of the sequence simultaneously:

```
MultiHead = concat(head_1, ..., head_h) W_O
```

Where each head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)

## Training Dynamics

### Loss Landscapes

Neural network losses are non-convex. Key phenomena:

- **Saddle points**: Local minima in one direction, maxima in another
- **Wide minima generalize better**: Flat solutions transfer better
- **Exploding/vanishing gradients**: Managed by normalization (BatchNorm, LayerNorm)

### Underfitting vs Overfitting

```
        Loss
          │
   train  │────/
          │   /
          │  /
          │ /
          │/
          └──────────→ Model capacity
               ^
          optimal
```

- **Underfitting**: Model too simple, can't learn the pattern
- **Overfitting**: Model memorizes training data, fails on new data

## For Wiki Context

See also:
- [[local-llm]] — Transformer-based language models
