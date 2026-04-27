---
title: Information Theory
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [mathematics, computer-science, communications, entropy]
---

## Overview

Information theory is a mathematical framework for quantifying, storing, and communicating information. Founded by Claude Shannon in his seminal 1948 paper "A Mathematical Theory of Communication," it provides the theoretical basis for understanding how information can be measured, compressed, transmitted, and protected from errors. The theory introduces the concept of entropy as a measure of uncertainty or information content, revolutionizing how we think about communication systems and data representation.

At its core, information theory addresses fundamental questions: What is information? How can it be measured? What are the limits of compressing and transmitting it reliably? These questions have profound implications across disciplines—from telecommunications and data storage to machine learning, cryptography, and neuroscience.

## Key Concepts

### Entropy

Shannon entropy measures the average uncertainty or information content in a random variable. For a discrete random variable X with possible values {x₁, x₂, ..., xₙ} and probabilities {p₁, p₂, ..., pₙ}, the entropy H(X) is defined as:

```
H(X) = -Σ p(x) * log₂(p(x))
```

Entropy is measured in bits when using log base 2. Higher entropy means more uncertainty and thus more information is needed to describe the outcome. A fair coin flip has entropy of 1 bit; a fair dice roll has entropy of approximately 2.585 bits.

### Channel Capacity

Channel capacity C represents the maximum rate at which information can be reliably transmitted over a noisy communication channel. Shannon's noisy channel coding theorem states that reliable communication is possible at any rate below capacity, given appropriate encoding. This fundamental limit guides the design of everything from WiFi protocols to satellite communications.

### Source Coding

Source coding deals with compressing data to remove redundancy. The source coding theorem establishes that the average length of any lossless compression scheme cannot be less than the entropy of the source. This means entropy sets a lower bound on how much data can be compressed.

## How It Works

Information theory provides mathematical tools that quantify information in terms of bits—fundamental units representing whether a received signal answers a binary question. When you learn that an event occurred that you were uncertain about, you receive information measured by how surprised you were.

**Mutual information** measures how much knowing one random variable reduces uncertainty about another. It quantifies the correlation between variables and is essential in feature selection for machine learning.

**KL Divergence** (Kullback-Leibler divergence) measures how one probability distribution differs from another. It appears prominently in machine learning, appearing in loss functions for variational autoencoders and in reinforcement learning algorithms.

**Rate-Distortion Theory** extends information theory to lossy compression, establishing fundamental limits on how much data can be compressed given an acceptable level of distortion.

These concepts interlink through the central role of entropy. Compression algorithms aim to represent data using as few bits as possible while preserving essential information. Error-correcting codes add controlled redundancy to protect against noise. Cryptographic systems leverage entropy to ensure unpredictability.

## Practical Applications

Information theory principles underpin modern digital communications. Every cellular network, WiFi connection, and satellite link uses error-correcting codes based on Shannon's theorems to achieve reliable communication despite noise.

Data compression formats like JPEG, MP3, and H.264 exploit statistical redundancies in images, audio, and video using information-theoretic principles. Machine learning algorithms, particularly in natural language processing and computer vision, leverage concepts like perplexity (related to entropy) to evaluate model quality.

Search algorithms use information-theoretic measures like TF-IDF and mutual information for relevance ranking and feature selection. Recommendation systems apply these principles to quantify how much knowing user preferences reduces uncertainty about content relevance.

## Examples

Consider predicting the next word in a sentence. If the vocabulary has 10,000 words and each is equally likely, entropy is log₂(10,000) ≈ 13.3 bits per word. But in practice, language has structure—some words are far more likely than others. A language model that assigns higher probabilities to common words reduces the average bits needed, and its perplexity measures this improvement.

```python
import math

def entropy(probabilities):
    """Calculate Shannon entropy from a list of probabilities."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

# Example: entropy of a biased coin (90% heads, 10% tails)
probabilities = [0.9, 0.1]
h = entropy(probabilities)
print(f"Entropy: {h:.4f} bits")  # Output: ~0.4690 bits
```

## Related Concepts

- [[algorithms]] - Computational procedures that process information
- [[data-compression]] - Reducing storage/transmission size using redundancy removal
- [[cryptography]] - Information-theoretic security and entropy in key generation
- [[machine-learning]] - Entropy-based objectives in learning algorithms
- [[neural-networks]] - Information flow in deep learning architectures
- [[natural-language-processing]] - Perplexity and language modeling

## Further Reading

- "Elements of Information Theory" by Cover and Thomas - The definitive textbook
- "A Mathematical Theory of Communication" by Claude Shannon - The original paper
- "Information Theory, Inference, and Learning Algorithms" by David MacKay - Comprehensive treatment

## Personal Notes

Information theory's elegance lies in its generality—the same mathematical framework applies equally to neural spikes in the brain and packets traversing the internet. Understanding entropy fundamentally changes how you think about data, uncertainty, and communication. It's remarkable that Shannon's 1948 paper remains so relevant in our age of deep learning and massive data streams.
