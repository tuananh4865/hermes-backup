---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 llm (extracted)
  - 🔗 prompt-engineering (extracted)
  - 🔗 system-prompt (inferred)
last_updated: 2026-04-11
tags:
  - LLM
  - priming
  - prompt
  - context
---

# LLM Priming

> Preparing an LLM's context to produce better outputs — the art of system prompting.

## Overview

Priming is the practice of preparing an LLM's context before asking a question. It includes:
- **System prompt**: Who the AI should be
- **Context**: Relevant information for the task
- **Examples**: Input-output pairs demonstrating desired behavior
- **Instructions**: What to do and how to do it

## Priming vs Fine-tuning

| Approach | Cost | Speed | Flexibility |
|----------|------|-------|-------------|
| **Priming** | Free | Instant | Update each query |
| **Fine-tuning** | $100-$1000s | Hours/days | Baked into model |

Rule of thumb: Try priming first. Fine-tune only when:
- You need consistent behavior across millions of calls
- You have domain-specific data that consistently improves results
- Priming isn't achieving desired consistency

## System Prompt Structure

### Basic Template
```python
system_prompt = """
You are [ROLE] with [EXPERTISE].

You help users with [DOMAIN] by [WHAT YOU_DO].

Guidelines:
1. [IMPORTANT RULE_1]
2. [IMPORTANT_RULE_2]
3. [IMPORTANT_RULE_3]

Output format:
[DESIRED_FORMAT]
"""
```

### Example: Code Reviewer
```python
system_prompt = """
You are a senior code reviewer with 15 years of experience.

You review Python code for:
- Security vulnerabilities
- Performance issues
- Maintainability
- Best practices (PEP 8)

When reviewing:
1. Start with security (SQL injection, XSS, auth issues)
2. Check performance (N+1 queries, inefficient loops)
3. Evaluate readability and documentation

Output format:
## Issues Found

### [Severity] Issue Title
- Location: [file:line]
- Description: [what's wrong]
- Fix: [how to fix]

If no issues found, say: "Code looks good. No issues detected."
"""
```

## Few-Shot Prompting

Provide examples of input-output pairs:

```python
messages = [
    {
        "role": "system",
        "content": "You classify sentiment as POSITIVE, NEUTRAL, or NEGATIVE."
    },
    {
        "role": "user",
        "content": "I love this product! It's amazing!"
    },
    {
        "role": "assistant",
        "content": "POSITIVE"
    },
    {
        "role": "user",
        "content": "It's okay, nothing special."
    },
    {
        "role": "assistant",
        "content": "NEUTRAL"
    },
    {
        "role": "user",
        "content": "Terrible experience. Never buying again."
    },
    {
        "role": "assistant",
        "content": "NEGATIVE"
    },
    {
        "role": "user",
        "content": "Works as expected for the price."
    }
]
# LLM will respond: NEUTRAL
```

## Chain of Thought

Encourage reasoning by showing work:

```python
messages = [
    {"role": "system", "content": "Solve problems step by step."},
    {"role": "user", "content": "If a train travels 60mph for 2 hours, how far does it go?"},
    {"role": "assistant", "content": """
Step 1: Identify what we know
- Speed = 60 mph
- Time = 2 hours

Step 2: Choose the formula
- Distance = Speed × Time

Step 3: Calculate
- Distance = 60 × 2 = 120 miles

Answer: 120 miles
"""},
    {"role": "user", "content": "What is 25% of 80?"}
]
# LLM will show work before answering
```

## Context Injection

Add relevant context to each query:

```python
def query_with_context(user_query, relevant_docs):
    context = "\n\n".join([
        f"Document {i+1}:\n{doc[:500]}"  # First 500 chars
        for i, doc in enumerate(relevant_docs)
    ])
    
    messages = [
        {"role": "system", "content": "Answer based on the provided context."},
        {"role": "user", "content": f"""
Context:
{context}

Question: {user_query}
"""}
    ]
    return chat(messages)
```

## Priming Techniques

### 1. Role Assignment
```
You are a senior software engineer at Google with 10+ years experience.
```

### 2. Format Specification
```
Format your response as JSON with keys: title, summary, action_items.
```

### 3. Constraint Definition
```
Never mention pricing in your response.
Always provide code examples in Python.
```

### 4. Temperature/Length Control
```
Keep responses under 200 words.
Be concise. Use bullet points.
```

## Priming Anti-Patterns

### 1. Conflicting Instructions
```
You are helpful but do not be too helpful.
Be concise but provide details.
```

### 2. Too Vague
```
Be good at everything.
```

### 3. Overstuffing
```
You are X, Y, Z, A, B, C, D, E, F, G, H...
```

### 4. Forgetting Edge Cases
```
Handle normal cases but don't say what to do for edge cases.
```

## Context Window Management

### Truncation Strategies
```python
def truncate_to_fit(messages, max_tokens):
    total = sum(len(m) for m in messages)
    while total > max_tokens:
        # Remove oldest non-system messages
        for i, m in enumerate(messages):
            if m["role"] != "system":
                messages.pop(i)
                break
    return messages
```

### Summarization
```python
def summarize_history(messages, max_messages=10):
    if len(messages) <= max_messages:
        return messages
    
    # Summarize older messages
    recent = messages[-max_messages:]
    older = messages[:-max_messages]
    
    summary = call_llm(f"Summarize this conversation: {older}")
    
    return [{"role": "system", "content": f"Earlier conversation: {summary}"}] + recent
```

## Priming for Our Wiki

### Research Mode
```
You are a research analyst synthesizing information from provided sources.

Rules:
1. Only use information from the provided context
2. Cite sources with [Source Name]
3. If information is missing, say "Not specified in sources"
4. Distinguish between facts and interpretations
```

### Writing Mode
```
You are a technical writer for our wiki.

Rules:
1. Use simple, clear language (8th grade reading level)
2. Include code examples for technical topics
3. Add wikilinks to related concepts: [[Concept Name]]
4. Keep sections under 200 words
```

## Related Concepts

- [[llm]] — Large language model basics
- [[prompt-engineering]] — Prompt techniques
- [[system-prompt]] — System prompt design
- [[context-window]] — Managing context length

## External Resources

- [OpenAI Prompting Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Anthropic Prompt Engineering](https://docs.anthropic.com/claude/docs/model-prompting)