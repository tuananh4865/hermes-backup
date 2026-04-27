---
title: "Large Language Model"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [llm, ai, machine-learning, nlp]
---

# Large Language Model

A Large Language Model (LLM) is a neural network trained on vast amounts of text data to understand, generate, and manipulate human language. LLMs are characterized by their massive scale—billions of parameters—and their ability to perform a wide variety of language tasks without task-specific training. They represent a fundamental breakthrough in [[natural-language-processing]] and have become the foundation for modern AI applications ranging from chatbots to code assistants.

## Architecture

The dominant architecture underlying modern LLMs is the [[transformer]], introduced in the 2017 paper "Attention Is All You Need." Transformers replaced recurrent neural networks with a mechanism called [[attention-mechanism]] that allows the model to weigh the importance of different parts of the input text when generating each output token.

The transformer architecture consists of an encoder and decoder stack built from layers of multi-head attention and feed-forward neural networks. Multi-head attention enables the model to jointly attend to information from different representation subspaces at different positions. The self-attention mechanism computes relationships between all tokens in a sequence, capturing long-range dependencies that were difficult for earlier architectures to model.

Modern LLMs typically use a decoder-only architecture (like [[GPT]]) or encoder-only architecture (like [[BERT]]) depending on their primary use case. Scale is a defining characteristic—models range from hundreds of millions to hundreds of billions of parameters, with larger models generally exhibiting more capable and nuanced behavior.

## Training

Training an LLM occurs in two main phases: [[pre-training]] and [[fine-tuning]].

During pre-training, the model learns to predict the next token in a sequence from massive corpora of text from the internet, books, and other sources. This self-supervised learning objective allows the model to acquire broad knowledge about language, facts, reasoning patterns, and even some world knowledge without explicit labels. Pre-training requires enormous computational resources and typically takes weeks or months on clusters of GPU hardware.

[[Fine-tuning]] adapts a pre-trained model to specific tasks or behaviors through additional training on smaller, curated datasets. This may involve supervised fine-tuning (SFT), where human annotators provide example inputs and desired outputs, or reinforcement learning from human feedback (RLHF), which aligns model responses with human preferences. Fine-tuning is much cheaper than pre-training and allows a single base model to be adapted for many different applications.

## Capabilities

LLMs exhibit remarkable capabilities across diverse language tasks. They can generate coherent, contextually appropriate text for summarization, translation, creative writing, and technical documentation. They demonstrate strong performance on question answering, extracting information from unstructured documents, and reasoning through complex problems step-by-step.

Emergent capabilities appear at scale, meaning certain abilities only manifest in larger models without explicit training—such as multi-step arithmetic, code generation, and abstract reasoning. LLMs can be used as reasoning engines when combined with prompting techniques like chain-of-thought prompting, which encourages the model to articulate intermediate steps.

However, LLMs also have limitations. They can generate plausible but incorrect information (hallucination), perpetuate biases present in training data, and have limited ability to verify facts independently. They lack true understanding of meaning and grounded experience, operating purely on statistical patterns learned during training.

## Related

- [[Transformer]] - The foundational architecture for modern LLMs
- [[Attention Mechanism]] - The key innovation enabling transformers
- [[Natural Language Processing]] - The broader field LLMs operate within
- [[Pre-training]] - The first phase of LLM training
- [[Fine-tuning]] - The adaptation phase for specific tasks
- [[GPT]] - OpenAI's decoder-only LLM family
- [[BERT]] - Google's encoder-only LLM family
- [[Self-Healing Wiki]] - The system that generated this article
