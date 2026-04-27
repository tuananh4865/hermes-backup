---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[llm-wiki]]
  - [[karpathy-llm-wiki]]
  - [[models]]
relationship_count: 3
---

# Context Window (Language Models)

> The maximum number of tokens an LLM can process in a single forward pass, defining the boundary of accessible context.

## Overview

The **context window** (also called *context length* or *context size*) is a fundamental parameter of language models that determines how many tokens can be fed into the model at once — both as input prompt and as generated output combined. It is the effective "working memory" of an LLM.

When you send a message to an LLM, your entire conversation history must fit within the context window. Once the accumulated conversation exceeds this limit, earlier messages must be truncated, summarized, or managed via techniques like [[llm-wiki|context management strategies]].

## Key Concepts

### Context Length by Model

| Model | Context Window |
|-------|---------------|
| GPT-4o | 128K tokens |
| Claude 3.5 Sonnet | 200K tokens |
| Gemini 1.5 Pro | 2M tokens |
| Llama 3.1 8B | 128K tokens |
| GPT-3.5 Turbo | 16K tokens |

### Token Counting

- A token is roughly 4 characters of English text, or ~0.75 words
- A page of text is approximately 500–1000 tokens
- The context window includes: system prompt + conversation history + current input + output

### Implications of Context Window Size

**Large context windows enable:**
- Processing entire documents, codebases, or books in a single prompt
- Long-document analysis and summarization
- Complex multi-turn conversations without memory loss
- [[karpathy-llm-wiki|RAG-style]] retrieval over large corpora

**Narrow context windows force:**
- Aggressive conversation truncation
- Chunking strategies for large documents
- Summarization of earlier context
- Careful prompt engineering to fit within limits

## Practical Considerations

### Context Overflow Management

When context approaches its limit, common strategies include:

1. **Truncation**: Drop the oldest messages
2. **Summarization**: Condense earlier conversation into a summary
3. **Semantic chunking**: Keep only the most relevant exchanges
4. **External memory**: Store conversation state in a database

### Cost and Performance Implications

- Longer context windows generally increase computation cost per token
- Some models (e.g., Gemini 1.5) charge differently for context length
- [[models]] with large contexts may have higher latency

### Position Extrapolation and RoPE

Modern models use position encoding methods like [[karpathy-llm-wiki|RoPE (Rotary Position Embedding)]] to handle long contexts efficiently without quadratic scaling.

## Related Concepts

- [[llm-wiki]] — Language model fundamentals
- [[karpathy-llm-wiki]] — Andrej Karpathy's LLM educational content
- [[models]] — LLM model comparisons and specs

## References

- [Anthropic: Context Windows](https://docs.anthropic.com/)
- [OpenAI: Tokenizer](https://platform.openai.com/tokenizer)
