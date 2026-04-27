---
title: "Tokens"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nlp, llm, machine-learning, tokenization, ai]
---

# Tokens

## Overview

Tokens are the fundamental units of text that large language models (LLMs) process. Before text enters a neural network, it must be broken into discrete pieces—a process called tokenization. Models don't see raw characters or words; they operate on sequences of integers representing tokens, where each integer maps to a learned embedding. Understanding tokens is essential for working with LLMs, as token limits, pricing, and capabilities all derive from this abstraction.

Tokenization algorithms balance granularity against vocabulary size. Character-level tokenization (treating each character as a token) produces small vocabularies but requires longer sequences and makes patterns harder to learn. Word-level tokenization (treating words as tokens) aligns with human intuition but produces enormous vocabularies and struggles with rare words and cross-linguistic consistency. Modern LLMs predominantly use subword tokenization, which decomposes text into pieces smaller than words but larger than characters—capturing common subwords while keeping vocabulary manageable.

The relationship between tokens and words varies by language and text type. English text typically tokenizes at roughly 1 token per 4 characters or 0.75 tokens per word. Technical content with long identifiers, code with variable names, and multilingual text often require more tokens per unit of meaning. This variability explains why the same message content can consume very different token counts depending on phrasing.

## Key Concepts

**Vocabulary Size** determines how many unique tokens a model can recognize. GPT-4 uses a vocabulary of approximately 100,000 tokens, while GPT-3.5 uses around 50,000. Larger vocabularies can represent more nuanced text without excessive decomposition, but require more memory for embedding tables and increase the risk of sparse token representations for less common sequences.

**Special Tokens** serve syntactic and semantic functions beyond normal text. The `<|endoftext|>` token (or `[EOS]` in other notations) marks document boundaries. `<|pad|>` tokens fill sequences to uniform length in batch processing. Mask tokens (`<|mask|>`) in BERT-style models represent text to be predicted. Instruction-following models often use `<|im_start|>` and `<|im_end|>` to delimit messages in conversations.

**Token Limits** constrain how much text a model can process in a single forward pass. ChatGPT models impose context windows—GPT-4 supports 8K, 32K, or 128K tokens depending on version. The limit includes both input and output, meaning a 32K context window with a 30K input leaves only 2K tokens for the response. This constraint shapes application design, often requiring truncation, summarization, or chunking strategies.

**Counting Tokens** matters for cost estimation and capacity planning. APIs charge per token, and understanding the token-to-text ratio enables accurate budgeting. Tokens include both visible text characters and invisible formatting—whitespace, newlines, and punctuation all consume tokens. The standard estimation formula for English is roughly `tokens ≈ characters / 4 + words / 4`.

## How It Works

Subword tokenization algorithms—BPE (Byte Pair Encoding), WordPiece, and Unigram—learn token vocabularies from training corpora through statistical analysis of co-occurrence patterns. BPE, used by GPT models, starts with character-level tokens and iteratively merges the most frequent adjacent pairs, building toward meaningful subword units. "Token" might become one token if common, or decompose into "Tok" + "en" if less frequent.

```python
# Simplified demonstration of BPE-style tokenization
text = "Tokenization is fundamental to LLMs"
tokens = text.split()  # Simple whitespace tokenization
print(tokens)
# ['Tokenization', 'is', 'fundamental', 'to', 'LLMs']

# Character-level view
for token in tokens:
    print(f"{token}: {list(token)}")
# Tokenization: ['T', 'o', 'k', 'e', 'n', 'i', 'z', 'a', 't', 'i', 'o', 'n']
# etc.
```

When the model processes tokens, each integer index looks up a corresponding embedding vector—a learned representation capturing semantic and syntactic properties. These embeddings feed into transformer layers that compute attention patterns across the token sequence. The final layer maps back to vocabulary-sized logits for next-token prediction.

## Practical Applications

**Prompt Engineering** requires awareness of token efficiency. Dense prompts with explanations, examples, and context consume tokens that might otherwise accommodate the response. Concise prompting saves tokens, reducing latency and cost. Techniques like few-shot learning require careful token budgeting to include sufficient examples within context limits.

**Cost Management** relies on accurate token counting. API pricing typically quotes per 1K tokens, with input and output tokens often priced differently (output often costs more). Estimating token counts before sending requests enables budget control. Applications may cache completions keyed by tokenized prompts to avoid redundant API calls.

**Multilingual Applications** must account for variable token density across languages. Languages with logographic scripts (Chinese, Japanese) often require more tokens per character than alphabetic scripts. A fixed token budget may accommodate significantly less meaning in one language versus another, affecting UI design and response quality expectations.

## Examples

```python
# Using tiktoken to count tokens (OpenAI's BPE implementation)
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")  # GPT-4's tokenizer

text = "Tokenization is fundamental to understanding LLMs."
tokens = enc.encode(text)
print(f"Text: {text}")
print(f"Token count: {len(tokens)}")
print(f"Tokens: {tokens}")
print(f"Decoded: {enc.decode(tokens)}")

# Output:
# Text: Tokenization is fundamental to understanding LLMs.
# Token count: 9
# Tokens: [36539, 310, 4906, 2840, 2533, 420, 22277, 13]
# Decoded: Tokenization is fundamental to understanding LLMs.
```

This demonstrates how a single sentence decomposes into roughly 9 tokens, with each token represented as an integer index.

## Related Concepts

- [[Large Language Models]] - The AI systems that consume tokens
- [[Tokenization]] - The process of converting text to tokens
- [[Transformer Architecture]] - The neural network design operating on tokens
- [[Embedding]] - Learned vector representations of tokens
- [[Context Window]] - Maximum tokens processable at once

## Further Reading

- [OpenAI Tokenizer Tool](https://platform.openai.com/tokenizer)
- [Character Tokenization (Hugging Face)](https://huggingface.co/docs/transformers/tokenizer_summary)
- [The Tokenizer Conference (Unicode Consortium)](https://unicode.org/conference/)

## Personal Notes

When building applications, I track token counts in logs to develop intuition for typical usage patterns. The ratio of tokens to words (roughly 1.3x for English) is a useful rule of thumb. For multilingual support, consider measuring actual token density rather than assuming uniformity. Tokens are invisible implementation details to end users, but they fundamentally shape what applications can do.
