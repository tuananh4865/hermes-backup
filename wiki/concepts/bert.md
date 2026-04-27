---
title: BERT
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [bert, nlp, transformer, language-model, google]
---

# BERT

## Overview

BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based language model developed by Google in 2018 that revolutionized natural language processing. Unlike previous unidirectional language models that read text left-to-right or right-to-left, BERT processes the entire sequence of tokens simultaneously, capturing full context from both directions. This bidirectional approach allows BERT to understand word meaning based on surrounding context—a capability that enabled state-of-the-art performance on a wide range of NLP benchmarks when released.

## Key Concepts

**Transformer Architecture** forms the foundation of BERT. The transformer uses self-attention mechanisms to weigh the importance of different tokens in a sequence when encoding each token. BERT specifically uses only the encoder portion of the original transformer architecture (as opposed to [[GPT]] which uses decoders).

**Bidirectional Context** is what distinguishes BERT from earlier models. Traditional language models like [[LSTM]] networks processed text in one direction, limiting their context understanding. BERT's bidirectional attention allows each word to attend to all other words in the sequence, capturing richer contextual relationships.

**Pre-training and Fine-tuning** is BERT's two-stage learning approach. During pre-training, the model learns general language understanding from large unlabeled corpora through two self-supervised tasks: Masked Language Modeling (MLM) and Next Sentence Prediction (NSP). The model is then fine-tuned on a specific task with labeled data, adapting its knowledge to particular applications.

**Tokenization** in BERT uses WordPiece, breaking text into subword tokens that balance between meaningful units and manageable vocabulary size. The special `[CLS]` token accumulates aggregate representation for classification tasks, while `[SEP]` tokens separate segments.

## How It Works

During pre-training, BERT randomly masks approximately 15% of input tokens and trains the model to predict these masked tokens. This task, called Masked Language Modeling, forces the model to understand full context since a masked word's representation must capture both left and right context. The NSP task trains BERT to understand sentence relationships, useful for tasks involving multiple sentences like question answering.

For fine-tuning, pre-trained weights are initialized, and a small task-specific output layer is added. The entire model is then trained on labeled data for the target task, allowing the general language knowledge to transfer to the specific problem. This transfer learning approach dramatically reduces the amount of labeled data needed for good performance.

## Practical Applications

BERT and its variants power numerous Google products and services. Search engines use BERT to better understand search queries and match them with relevant content. Question-answering systems leverage BERT to extract answers from documents. Sentiment analysis applications classify opinions in text. Named entity recognition systems identify people, organizations, and locations. Content classification and spam detection also benefit from BERT's language understanding capabilities.

## Examples

Using the Hugging Face Transformers library, applying BERT for sentiment analysis looks like this:

```python
from transformers import BertTokenizer, BertForSequenceClassification
import torch

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')

inputs = tokenizer("I love using BERT for NLP tasks!", return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=-1)
```

This loads a pre-trained BERT model, tokenizes input text, runs inference, and produces a classification prediction—all with just a few lines of code thanks to the abstraction provided by modern deep learning frameworks.

## Related Concepts

- [[transformer]] — The underlying architecture BERT is built upon
- [[gpt]] — Autoregressive language model family (GPT uses decoder instead of encoder)
- [[attention-mechanism]] — Self-attention that enables BERT's bidirectional context
- [[natural-language-processing]] — The broader field BERT operates within
- [[word-embeddings]] — Dense vector representations of words that BERT produces
- [[transfer-learning]] — The pre-train then fine-tune approach BERT uses

## Further Reading

- "Attention Is All You Need" (Vaswani et al., 2017) - Original transformer paper
- "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding" (Devlin et al., 2018)
- Hugging Face Transformers Documentation

## Personal Notes

BERT's impact on NLP cannot be overstated. The paper's demonstration that pre-trained language models could be fine-tuned for specific tasks with relatively small datasets changed how practitioners approach NLP problems. The code and pre-trained weights released by Google enabled rapid experimentation and adoption across the research community. Understanding BERT remains foundational for anyone working in modern NLP, even as newer models like GPT-4 and Claude push capabilities further.
