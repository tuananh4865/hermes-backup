---
title: FlashAttention
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [attention, transformer, optimization, gpu, neural-network]
---

# FlashAttention

## Overview

FlashAttention is an efficient attention algorithm that computes exact self-attention (matching the mathematically exact result of standard attention) while being significantly faster and more memory-efficient. Published in 2022 by Tri Dao and colleagues, FlashAttention introduced a fundamental insight: by exploiting the specific access patterns of attention computation and using tiling to keep data in fast on-chip SRAM rather than slow off-chip HBM (High Bandwidth Memory), it achieves the same mathematical result as standard attention but with drastically reduced memory usage—enabling transformers to process much longer sequences.

Standard attention has quadratic memory complexity in sequence length (O(N²) in memory) because the attention matrix (the N×N matrix of attention weights for sequence length N) must be materialized. For a sequence of length 4096, this matrix contains over 16 million values. FlashAttention avoids materializing this full matrix by computing attention in blocks, using online softmax computation, and accumulating the exact result through successive passes. This reduces memory to O(N) while maintaining near-optimal computational complexity.

FlashAttention matters because attention is the fundamental computational bottleneck in [[transformer-architecture]] models. It enables training of transformers with 4-8x longer context windows than would otherwise be feasible, and dramatically speeds up both training and inference. The algorithm has been rapidly adopted across the AI industry—it's now a standard component in PyTorch, JAX, and all major LLM frameworks.

## Key Concepts

**Attention Mechanism**: The core operation in transformers where each position attends to all other positions. For input sequence X of shape (N, d), standard attention computes:
```
Attention(Q, K, V) = softmax(QK^T / √d)V
```
Where Q, K, V are query, key, value matrices derived from X.

**Memory Hierarchy**: Modern GPUs have slow, high-capacity HBM (High Bandwidth Memory, ~2TB/s but high latency) and fast, low-capacity on-chip SRAM (~20TB/s but only ~100MB). Standard attention's materialization of the N×N attention matrix constantly moves data between these, creating a memory bandwidth bottleneck.

**Tiling**: FlashAttention divides the N×N attention computation into smaller blocks that fit in SRAM. It processes one block at a time, dramatically reducing HBM traffic.

**Online Softmax**: Computing softmax requires knowing all values to normalize properly. FlashAttention uses an online/trick form of softmax that computes normalization incrementally as blocks are processed, enabling block-wise computation without losing accuracy.

**SRAM**: Static Random-Access Memory on the GPU chip—extremely fast but limited in size. FlashAttention strategically keeps working data here.

**HBM**: High Bandwidth Memory—the main GPU memory that's large but slower to access than SRAM.

**Kernel**: A GPU kernel is a function executed on the GPU by many parallel threads. FlashAttention is implemented as a custom fused kernel that orchestrates the attention computation to minimize memory movement.

## How It Works

FlashAttention's algorithm can be understood by walking through the block-wise computation:

**Standard Attention (Naive)**:
1. Compute Q, K, V matrices from input X
2. Compute S = QK^T (N×N matrix) — materializes full attention matrix
3. Compute softmax(S) row-wise
4. Compute O = softmax(S)V

This requires O(N²) memory just for S and has to read/write this massive matrix multiple times.

**FlashAttention Algorithm**:
1. **Initialization**: Load Q (N×d) into SRAM. Divide K and V into T blocks of size B.

2. **Outer Loop**: For each block j of K and V:
   - Load block Q_i, K_j, V_j into SRAM
   - Compute partial attention scores S_ij = Q_i K_j^T
   - Compute online softmax statistics (row-wise max and sum)
   - Update running softmax normalization
   - Accumulate partial results into output O_i

3. **Online Softmax Trick**: For numerical stability, softmax(x) is computed as:
   ```
   m(x) = max(x)  # max for numerical stability
   exp(x - m(x)) / sum(exp(x - m(x)))
   ```
   The online version maintains running m and normalization sums that can be updated incrementally as new blocks contribute.

4. **Final Result**: After processing all K/V blocks, each output row O_i is the exact attention-weighted sum of all V values, computed without ever materializing the full N×N matrix.

**Memory Savings**: FlashAttention uses O(N) additional memory rather than O(N²). For N=4096, this is 16K vs 16M values—a 1000x reduction in memory for the attention matrix.

**FlashAttention-2** improved on the original with better parallelism across sequence length dimension, better work partitioning for different tensor shapes, and support for sequence length > 8192. **FlashAttention-3** further improved throughput using asynchronous execution and hardware-aware optimizations for H100 GPUs.

## Practical Applications

**Training Longer Context Models**: FlashAttention enables training on sequences of 16K, 32K, or more tokens without memory explosion. This is essential for tasks requiring long documents, codebases, or conversation history.

**Inference Acceleration**: Both prefill (processing prompt) and decode (generating tokens) phases benefit. FlashAttention's block-wise computation maps well to the autoregressive generation pattern.

**Memory-Limited Environments**: Running large transformers on consumer GPUs becomes feasible when attention doesn't require O(N²) memory.

**Long Context Applications**: Applications like analyzing entire codebases, processing full documents, or working with extended conversations rely on FlashAttention to make long contexts tractable.

**State-Space Models**: The efficiency techniques pioneered by FlashAttention have influenced efficient architectures like Mamba that aim to match attention performance with subquadratic complexity.

## Examples

```python
# FlashAttention usage in PyTorch 2.0+
import torch
from torch.nn.functional import scaled_dot_product_attention

# This uses FlashAttention automatically when available
# (requires PyTorch 2.0+ with CUDA and FlashAttention compiled)
q = torch.randn(1, 8, 512, 64, device='cuda')  # (batch, heads, seq, dim)
k = torch.randn(1, 8, 512, 64, device='cuda')
v = torch.randn(1, 8, 512, 64, device='cuda')

# scaled_dot_product_attention uses FlashAttention automatically
output = scaled_dot_product_attention(q, k, v, is_causal=True)
```

```python
# Direct FlashAttention usage (flash_attn package)
# Install: pip install flash-attn --no-build-isolation
from flash_attn import flash_attn_func

# flash_attn_func expects (batch, seq, nheads, headdim) format
q = torch.randn(16, 256, 12, 64, device='cuda').half()  # half precision recommended
k = torch.randn(16, 256, 12, 64, device='cuda').half()
v = torch.randn(16, 256, 12, 64, device='cuda').half()

# Returns attention output
output = flash_attn_func(q, k, v, causal=True)  # causal=True for autoregressive
```

**Benchmark comparison** (approximate, from original paper):

| Sequence Length | Standard Attention Memory | FlashAttention Memory | Speedup |
|-----------------|---------------------------|----------------------|---------|
| 512 | 256 MB | 32 MB | 1.7x |
| 1024 | 1 GB | 64 MB | 2.3x |
| 2048 | 4 GB | 128 MB | 3.0x |
| 4096 | 16 GB | 256 MB | 3.5x |

## Related Concepts

- [[self-attention]] — The mechanism FlashAttention accelerates
- [[multi-head-attention]] — How multiple attention heads work together
- [[transformer-architecture]] — The larger architecture context
- [[kv-cache]] — Caching keys/values during autoregressive generation
- [[inference-optimization]] — Broader inference acceleration field
- [[quantization]] — Complementary memory reduction technique
- [[ssm]] — State-space models as potential attention alternative

## Further Reading

- [FlashAttention Paper (Dao, 2022)](https://arxiv.org/abs/2205.14135) — Original publication
- [FlashAttention-2](https://arxiv.org/abs/2307.08691) — Improved version
- [FlashAttention-3](https://arxiv.org/abs/2404.05117) — Latest optimizations
- [FlashAttention GitHub](https://github.com/Dao-AILab/flash-attention) — Implementation and benchmarks
- [GPU Architecture for Deep Learning](https://courses.cs.ashington.edu/courses/csep524/+) — Understanding memory hierarchy

## Personal Notes

The first time I ran a model with FlashAttention enabled, I was genuinely surprised—attention memory dropped so dramatically that a model I thought required 48GB of GPU memory suddenly ran on 24GB. The mathematical equivalence to standard attention is key: there's no approximation tradeoff. The online softmax trick is elegant—I remember reading the paper and appreciating how such a theoretical insight had immediate practical impact. FlashAttention-3's async execution and H100-specific optimizations show how hardware-software co-design continues to push performance. One thing to watch: FlashAttention's block-wise nature makes some attention visualizations harder (you can't just dump the full matrix), which matters for interpretability research. The technique has essentially become infrastructure—it's in PyTorch, JAX, and optimized for every major model.
