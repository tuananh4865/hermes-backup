---
title: Inference
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [inference, llm, machine-learning, deployment, optimization]
---

# Inference

## Overview

Inference in machine learning refers to the process of running a trained model to generate predictions or outputs on new, unseen data. This contrasts with training, where the model learns patterns from a dataset. Once a model is trained, inference is how it's actually used in production to make predictions—whether that's classifying an email as spam, translating a sentence, or generating the next token in a [[large-language-models|LLM]] response.

In the context of [[large-language-models]], inference specifically means running the model to generate text given an input prompt. This is computationally intensive because modern LLMs have billions of parameters, and each token generation requires performing matrix multiplications through the entire network. The inference process involves feeding tokens through the model's layers, producing a probability distribution over the next token, then sampling from that distribution (or using techniques like greedy decoding or beam search).

Inference matters enormously in practical ML because while training is done once (or periodically), inference happens continuously for every user request. The cost, latency, and throughput of inference often dominate the total cost of ownership for ML systems. Optimizing inference—making it faster, cheaper, and more efficient—is one of the most active areas of ML research and engineering, involving techniques like quantization, batching, caching, and specialized hardware.

## Key Concepts

**Forward Pass**: The process of propagating input data through the neural network layers to produce an output. Each layer applies matrix multiplications and activation functions, transforming the input representation until reaching the final output layer.

**Token**: The basic unit of text in an LLM. Tokens can be characters, subwords (like Byte-Pair Encoding), or words. LLMs typically use subword tokenization for efficiency. For example, "learning" might be tokenized as ["learn", "ing"].

**Sampling**: The process of selecting the next token from the model's probability distribution. Techniques include:
- **Greedy Decoding**: Always selecting the highest probability token (deterministic)
- **Temperature Sampling**: Adjusting the distribution sharpness before sampling
- **Top-K Sampling**: Restricting sampling to the K most likely tokens
- **Top-P (Nucleus) Sampling**: Sampling from the smallest set of tokens whose cumulative probability exceeds P

**Context Window**: The maximum number of tokens the model can process in a single inference call. Modern LLMs have context windows ranging from 4K to 200K+ tokens.

**Beam Search**: A search algorithm that maintains multiple candidate sequences (beams) at each step, exploring several likely token sequences in parallel rather than just one.

**Streaming**: Generating and returning tokens incrementally as they're produced, rather than waiting for the entire completion. This reduces perceived latency dramatically.

## How It Works

LLM inference involves several stages, each contributing to latency and computational cost:

**Tokenization**: The input text is converted to token IDs using the model's tokenizer (BPE, WordPiece, or similar). This is a lookup operation but requires the text to be processed.

**Embedding Lookup**: Each token ID is mapped to a dense vector embedding—a learned representation of that token's meaning.

**Transformer Layers**: The core of the LLM. Each layer performs:
1. **Self-Attention**: Each token attends to all other tokens, computing attention weights via scaled dot-product attention. This is where the [[kv-cache]] becomes important.
2. **Feed-Forward Network**: A two-layer MLP applied independently to each token position.
3. **Layer Normalization**: Stabilizing transformations between layers.

**Logits Computation**: The final layer transforms the hidden states into logits—one logit per token in the vocabulary.

**Softmax and Sampling**: The logits are passed through a softmax to produce a probability distribution over the vocabulary for the next token. The actual token is then selected via the chosen sampling strategy.

**De-Tokenization**: The selected token ID is converted back to text characters.

**Autoregressive Generation**: For each new token, the process repeats—but now includes all previous tokens. This sequential nature makes LLM inference fundamentally different from feed-forward networks and limits parallelism.

### The KV Cache

During autoregressive generation, the key and value matrices for all previous tokens are cached after first computation. Without [[kv-cache]], each token generation would recompute attention over all previous tokens from scratch—a massive waste. The KV cache stores these values, allowing new tokens to attend to the full context without recomputation. Memory for the KV cache scales with batch size, sequence length, and model size.

## Practical Applications

**Chatbots and Assistants**: Products like ChatGPT, Claude, and Gemini are pure inference applications. User prompts go in, model generates responses token by token.

**Code Completion**: GitHub Copilot uses inference to predict and suggest code completions as developers type. Latency is critical here—fast suggestions feel more natural.

**Content Generation**: Summarization, translation, and creative writing applications all rely on inference.

**Embedding Models**: Sentence transformers and other embedding models run inference to convert text to vector representations used in RAG (Retrieval-Augmented Generation) systems.

**Inference as a Service**: Cloud providers (OpenAI, Anthropic, AWS, Azure) offer API access to models, charging per token. Optimizing prompt length directly reduces costs.

## Examples

```python
# Example: Simple inference with transformers library
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2"  # Small example model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Tokenize input
input_text = "The future of AI is"
inputs = tokenizer(input_text, return_tensors="pt")

# Run inference
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    
# Get predicted next token
last_token_logits = logits[0, -1, :]
next_token_id = last_token_logits.argmax().item()

# Decode and append
next_token = tokenizer.decode([next_token_id])
print(f"Next token: {next_token}")
```

```python
# Example: Streaming inference implementation concept
import asyncio

async def stream_generate(model, tokenizer, prompt: str, temperature: float = 1.0):
    """
    Simulated streaming inference that yields tokens as they're generated.
    Real implementations use model.forward() in a loop with KV cache.
    """
    input_ids = tokenizer.encode(prompt)
    generated = list(input_ids)
    
    while True:
        # Get logits for next token
        logits = await model.predict_next(torch.tensor([generated]))
        probs = softmax(logits / temperature)
        
        # Sample next token (simplified)
        next_token = torch.multinomial(probs, 1).item()
        generated.append(next_token)
        
        # Yield token and check for stop condition
        token_text = tokenizer.decode([next_token])
        yield token_text
        
        if next_token == tokenizer.eos_token_id:
            break
```

**Performance Comparison of Inference Strategies**:

| Strategy | Latency | Quality | Use Case |
|----------|---------|---------|----------|
| Greedy | Lowest | Good | Fast batch processing |
| Beam Search (k=5) | Medium | Higher | Translation |
| Temperature=0.7 | Low | Creative | Chat |
| Top-P=0.9 | Variable | Balanced | General generation |

## Related Concepts

- [[inference-optimization]] — Techniques to improve inference efficiency
- [[kv-cache]] — Caching mechanism critical for efficient autoregressive inference
- [[large-language-models]] — The models being run during inference
- [[quantization]] — Reducing model size for faster/cheaper inference
- [[transformer-architecture]] — The underlying neural network architecture
- [[prompt-engineering]] — Crafting inputs to get better inference outputs
- [[batch-inference]] — Processing multiple requests together for efficiency

## Further Reading

- [Hugging Face Inference Documentation](https://huggingface.co/docs/transformers/en/main_classes/model)
- [LLM Inference Guide](https://docs.anyscale.com/tutorials/run-llms) — Production inference patterns
- [Streaming LLMs](https://arxiv.org/abs/2309.08633) — Attention sink technique for streaming
- [Optimizing LLM Inference](https://lm.inf.ethz.ch/) — Research on inference optimization

## Personal Notes

My first encounter with inference optimization was when running open-source models locally and being shocked by how slow token generation felt compared to API calls. The difference is that API services have optimized inference stacks with batch scheduling, tensor parallelism, and custom hardware. Understanding the KV cache was an "aha" moment—explaining why memory rather than compute often seems to be the bottleneck. I've become interested in speculative decoding as a way to get some parallelism back in the autoregressive generation process. The quantization wave (4-bit, 8-bit) has made running large models locally much more accessible.
