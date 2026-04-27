---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[llm-wiki]]
  - [[models]]
  - [[api-design-patterns]]
  - [[models]]
relationship_count: 3
---

# Structured Outputs (JSON)

> Constraining LLM generation to produce valid, machine-parseable JSON or other structured formats.

## Overview

**Structured outputs** refers to techniques that force a language model to generate text in a specific, machine-readable format — most commonly JSON. Instead of free-form prose, the model produces JSON that programs can reliably parse, validate, and use.

This is critical for production AI applications where LLM output feeds into downstream systems that expect typed data.

## Why Structured Outputs Matter

### The Parsing Problem

Standard LLM generation produces free text. Even when instructed to "return JSON," models can produce:

- Extra prose before/after the JSON
- Invalid JSON syntax (trailing commas, comments)
- Fields that don't match the expected schema
- Inconsistent types across calls

This makes output parsing brittle and error-prone.

### How Structured Outputs Work

Modern approaches include:

1. **Grammar-based generation**: Constrain the decoder to only produce valid tokens per a grammar
2. **JSON schema validation**: Generate then validate/retry if invalid
3. **Guided generation libraries**: Tools like Outlines, Guidance enforce structure at the token level
4. **Native API support**: Some providers (OpenAI, Claude) offer built-in structured output modes

## Implementation Approaches

### OpenAI Structured Outputs

```python
from openai import OpenAI

client = OpenAI()

response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "Extract the user's order details"}
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "order",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "quantity": {"type": "integer"},
                                "price": {"type": "number"}
                            },
                            "required": ["name", "quantity", "price"]
                        }
                    },
                    "total": {"type": "number"}
                },
                "required": ["order_id", "items", "total"]
            }
        }
    }
)

order = response.choices[0].message.parsed
```

### Library-Based Approaches

**Outlines library:**

```python
import outlines

@outlines.prompt
def extract_user(data):
    """Extract user info from: {{data}}"""

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"]
}

model = outlines.openai.OpenAI("gpt-4o")
generator = outlines.generate(model, schema)
result = generator("John is 25, email john@example.com")
```

**Guidance library:**

```python
import guidance

program = guidance(
    '''Extract user information:
    {{
        "name": gen.strpattern('Name: *'),
        "email": gen.strpattern('Email: *')
    }}'''
)
```

## Common Use Cases

| Use Case | Description |
|----------|-------------|
| **API data extraction** | Convert natural language to structured API payloads |
| **Form processing** | Extract fields from unstructured documents |
| **Code generation** | Produce valid code with guaranteed syntax |
| **Classification** | Return structured labels with confidence scores |
| **Data transformation** | Convert between data formats |

## Trade-offs

**Advantages:**
- Reliable, deterministic output parsing
- Type safety across LLM calls
- Reduced prompt engineering for format control
- Production-grade reliability

**Disadvantages:**
- Constrained output may reduce quality in creative tasks
- Schema must be designed carefully — changes require schema updates
- Some providers charge more for structured outputs
- Not all models support native structured outputs

## Best Practices

1. **Use native support when available** — OpenAI/Claude structured modes are most reliable
2. **Validate schema design** — Ensure required fields are minimal; optional fields reduce failures
3. **Handle parse failures gracefully** — Have fallback prompts or retry logic
4. **Test with adversarial inputs** — Verify behavior with unexpected inputs

## Related Concepts

- [[llm-wiki]] — LLM fundamentals and generation
- [[api-design-patterns]] — API design patterns for AI applications
- [[models]] — Model capabilities and constraints

## References

- [OpenAI: Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs)
- [Outlines Library](https://github.com/outlines-dev/outlines)
- [Guidance Library](https://github.com/guidance-ai/guidance)
