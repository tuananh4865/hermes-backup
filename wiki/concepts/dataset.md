---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 training-data (extracted)
  - 🔗 fine-tuning (extracted)
  - 🔗 rag (inferred)
last_updated: 2026-04-11
tags:
  - data
  - machine-learning
  - datasets
---

# Dataset

> Collections of data used for training, evaluating, and fine-tuning machine learning models.

## Overview

A dataset is a structured collection of data used to train AI models, evaluate performance, or fine-tune existing models. Datasets come in many forms:
- **Text corpora**: Books, articles, code
- **Image datasets**: Photos, diagrams, scanned documents
- **Audio datasets**: Speech recordings, music
- **Multimodal**: Paired images and text, video with captions

## Types of ML Datasets

### Pre-training Datasets
Massive text collections for training base models:

| Dataset | Size | Description |
|---------|------|-------------|
| **The Pile** | 825GB | Diverse text from 22 sources |
| **Common Crawl** | Petabytes | Web scrape, filtered |
| **C4** | 806GB | Cleaned Common Crawl |
| **RedPajama** | 1.2TB | C4 subset, deduplicated |

### Fine-tuning Datasets
Smaller, curated datasets for specific tasks:

| Dataset | Purpose | Size |
|---------|---------|------|
| **SFT (Supervised Fine-tuning)** | Instruction following | 10K-100K examples |
| **DPO pairs** | Preference learning | 10K-100K pairs |
| **RLHF feedback** | Reward modeling | 10K-50K comparisons |

### Evaluation Datasets
Benchmarks for measuring model capabilities:

| Benchmark | What It Tests |
|-----------|--------------|
| **MMLU** | Multi-task language understanding |
| **HumanEval** | Code generation |
| **GSM8K** | Math word problems |
| **TruthfulQA** | Truthfulness |

## Dataset Formats

### JSONL (Most Common)
```jsonl
{"text": "The capital of France is Paris."}
{"text": "Python is a programming language."}
{"text": "The moon orbits the Earth."}
```

### Chat Format
```jsonl
{"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

### Preference Pairs (DPO)
```jsonl
{"prompt": "...", "chosen": "...", "rejected": "..."}
```

## Creating Datasets

### Web Scraping
```python
import requests
from bs4 import BeautifulSoup

def scrape_wiki(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()
```

### Synthetic Data Generation
```python
from transformers import AutoTokenizer

# Use LLM to generate training data
def generate_synthetic(path, count=1000):
    prompt = f"Generate a diverse dataset of {count} examples..."
    return call_llm(prompt)
```

### Data Filtering
```python
# Remove low-quality examples
def filter_quality(examples, min_length=50, max_length=2000):
    return [
        ex for ex in examples
        if min_length <= len(ex) <= max_length
    ]
```

## Dataset Curation

### Quality Criteria
1. **Accuracy**: Facts are correct
2. **Relevance**: Matches target use case
3. **Diversity**: Covers variety of inputs
4. **Balance**: No heavy bias toward one class
5. **Clean**: No toxic or harmful content

### Deduplication
```python
# Remove near-duplicates
from sklearn.feature_extraction.text import TfidfVectorizer

def deduplicate(dataset, threshold=0.8):
    vectors = TfidfVectorizer().fit_transform(dataset)
    # Keep only unique examples
    ...
```

## Dataset Storage

### Local
```bash
# Store in data/ directory
data/
├── train.jsonl
├── val.jsonl
└── test.jsonl
```

### Cloud Storage
- **Hugging Face Hub**: `datasets` library
- **AWS S3**: Large file storage
- **Google Cloud Storage**: GCP ecosystem

## Hugging Face Datasets

```python
from datasets import load_dataset

# Load a dataset
ds = load_dataset("wikipedia", "20220301.en")

# Use in training
for batch in ds["train"].batch(32):
    ...
```

## Dataset Ethics

### Licensing
- Check dataset license (CC, GPL, etc.)
- Some prohibit commercial use
- Some require attribution

### Content Filtering
- Remove personally identifiable information (PII)
- Filter toxic/harmful content
- Review for biases

## Related Concepts

- [[training-data]] — Data used in model training
- [[fine-tuning]] — Adapting models with datasets
- [[rag]] — RAG uses datasets as knowledge bases
- [[embedding]] — Text represented as vectors

## External Resources

- [Hugging Face Datasets](https://huggingface.co/datasets)
- [The Pile](https://arxiv.org/abs/2201.07311)
- [Common Crawl](https://commoncrawl.org/)