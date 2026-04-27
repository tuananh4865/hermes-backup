---
title: KV Cache
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [kv-cache, inference, transformer, llm, attention-mechanism]
---

# KV Cache

## Overview

The KV cache (Key-Value cache) is a critical optimization in modern [[large language model]] inference that stores the key and value tensors from the self-attention mechanism across decoding steps. During [[transformer]] autoregressive generation, each new token depends on all previously generated tokens. Without caching, the model would need to recompute attention over the entire context for every single new token, resulting in quadratic compute complexity and severe performance degradation. The KV cache eliminates this redundancy by storing and reusing these tensors, reducing the effective computation per new token to linear complexity in the context length.

This optimization was popularized by the original [[GPT]] models and is now fundamental to virtually every production LLM deployment, including systems built on [[Llama]], [[Mistral]], [[GPT-4]], and [[Claude]]. Understanding KV cache behavior is essential for optimizing [[inference]] throughput, managing memory usage, and designing efficient LLM-powered applications.

## Key Concepts

### Transformer Attention Recap

In a [[transformer architecture]], each token is projected into three vectors: Query (Q), Key (K), and Value (V). Self-attention computes `softmax(QK^T / sqrt(d)) * V` to produce weighted sums of values based on token similarity. During autoregressive generation, when generating token N, the model must attend over tokens 1 through N-1.

### Cache Structure

The KV cache stores, for each attention layer and each previously processed token:
- **Key tensor**: The K projection for that token, used to compute attention scores
- **Value tensor**: The V projection for that token, used to compute weighted values

These are stored in GPU memory (or CPU memory for CPU inference) as the context grows. When generating token N+1, instead of recomputing K and V for all tokens 1 through N, the model:
1. Computes Q, K, V for the new token N+1 only
2. Retrieves cached K and V for tokens 1 through N from memory
3. Computes attention using the new Q with all cached K/V pairs
4. Writes the new K and V to the cache

### Memory overhead

The KV cache memory footprint grows linearly with context length. For a model with:
- `layers` attention layers
- `batch_size` sequences
- `seq_len` context length
- `heads` attention heads
- `head_dim` dimension per head

The cache size per sequence is approximately: `2 * layers * seq_len * heads * head_dim * bytes_per_float`

For a 70B parameter model like Llama 3 with 80 layers, 8K context, this can be hundreds of gigabytes for a single long context. This is why [[context-window]] size is often limited and why techniques like [[Flash Attention]] are essential—they reduce both compute and memory bandwidth requirements.

### Multi-Query Attention (MQA) and Grouped-Query Attention (GQA)

Standard multi-head attention stores K and V for every head independently. [[Multi-head attention]] (MHA) can be memory-heavy. MQA reduces K/V heads to one shared set, dramatically cutting cache size. GQA, used in [[Llama 2]] and [[Mistral]], splits heads into query groups that share K/V heads—trading off some quality for significant memory savings.

## How It Works

The typical KV cache lifecycle during autoregressive generation:

```
Input: "The cat sat on the"
Step 1: Encode all tokens → Cache[K,V] for tokens 1-5
Step 2: Generate token 6 ("mat") → Use Cache + new token Q
Step 3: Append token 6 K,V to Cache
Step 4: Generate token 7 (".") → Use full Cache
... repeat until EOS token
```

At each step, the KV cache grows by one token's worth of K/V data. The `past_key_values` tuple in many LLM frameworks (Hugging Face Transformers) holds this cached state between generation calls.

Key implementation details:
- Cache is stored in [[KV cache]] format: a tuple of `(k_cache, v_cache)`, one per layer
- During [[inference]], the cache lives in GPU HBM (High Bandwidth Memory) for fast access
- Prefix caching (caching the KV of system prompts) is an emerging optimization to avoid recomputing for repeated prefixes across requests

## Practical Applications

KV cache optimization is central to many LLM deployment strategies:

- **Continuous Batching**: Multiple requests share the GPU compute, but each has its own KV cache entries
- **Prompt Caching**: Storing KV of static system prompts reduces per-request compute
- **Speculative Decoding**: The draft model generates candidates, the KV cache accelerates the verification step
- **Context Length Extension**: PagedAttention ([[vLLM]]) manages KV cache like virtual memory, enabling longer contexts with less fragmentation

## Examples

Using Hugging Face Transformers KV cache:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# First pass: encode prompt, cache is built automatically
input_ids = tokenizer("The capital of France is", return_tensors="pt")
output = model(**input_ids, use_cache=True)
# past_key_values is now populated with K,V tensors

# Second pass: generate next token using cache
input_ids = tokenizer("The capital of France is Paris", return_tensors="pt")
output = model(**input_ids, use_cache=True)
# New token's Q is computed, K,V retrieved from cache + new K,V appended

print(tokenizer.decode(output.logits.argmax(-1)))
```

Viewing cache size in vLLM:

```python
from vllm import LLM, SamplingParams
llm = LLM(model="meta-llama/Llama-2-7b-hf")
# vLLM automatically manages KV cache as paging memory
# You can inspect cache stats via llm.llm_engine.model_runner
```

## Related Concepts

- [[transformer]] — The architecture that uses KV caching
- [[inference]] — LLM inference in general
- [[inference-optimization]] — Broader inference optimization techniques
- [[Flash Attention]] — Algorithm that accelerates attention with/without KV cache
- [[context-window]] — Context length limits and management
- [[Large Language Model]] — The models using KV cache
- [[Multi-head Attention]] — The attention variant that produces K and V tensors
- [[vLLM]] — Inference engine with advanced KV cache management (PagedAttention)
- [[Llama]] — Model family using GQA

## Further Reading

- [Flash Attention paper (Dao et al.)](https://arxiv.org/abs/2205.14135) — Foundation for efficient attention
- [Hugging Face Transformers KV Cache documentation](https://huggingface.co/docs/transformers/en/kv_cache_concept)
- [vLLM PagedAttention paper](https://www.vllm.ai/) — OS-style KV cache management
- [GPTCache](https://github.com/ShawnIU/GPTCache) — Semantic KV cache for LLM responses

## Personal Notes

I initially underappreciated how much the KV cache limits maximum context length. When running models on limited GPU memory, the KV cache is often the first thing to bite you—fill up GPU memory with cache and you can't even load the model weights. PagedAttention from vLLM was a game changer for me: treating the KV cache like virtual memory pages lets you pack far more concurrent sequences into the same GPU memory. For applications with repeated system prompts, implementing a prefix cache store (e.g., using Redis or an in-memory LRU) can cut latency dramatically.
