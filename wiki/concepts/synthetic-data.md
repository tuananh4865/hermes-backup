---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 fine-tuning (extracted)
  - 🔗 karpathy-llm-knowledge-base (extracted)
relationship_count: 2
---

# Synthetic Data

## Overview

Synthetic data is artificially generated data that mimics real-world data. In LLM context, it means using AI to generate training data for fine-tuning.

## Why Synthetic Data?

### Privacy
- No real user data needed
- Can generate unlimited training examples
- GDPR/privacy compliant

### Cost
- Cheaper than human annotation
- No labeling workforce needed
- Scale to millions of examples

### Control
- Precise control over data distribution
- Can generate edge cases
- Balance dataset composition

## Synthetic Data Generation Methods

### 1. LLM Self-Generation
Use a capable model to generate training data from wiki content.

### 2. Backtranslation
Generate variations of existing data.

### 3. Rule-Based Generation
Use templates and dictionaries.

### 4. Context Window Sampling
- Sample random chunks from documents
- Generate Q&A from each chunk

## Quality Considerations

### Quality Metrics
- **Diversity**: Are responses varied?
- **Accuracy**: Do answers match source?
- **Format**: Consistent with training format?

### Filtering
- Remove low-quality generations
- Human eval for spot checking

## Related
- [[fine-tuning]] — How synthetic data is used
- [[karpathy-llm-knowledge-base]] — Wiki as knowledge source
