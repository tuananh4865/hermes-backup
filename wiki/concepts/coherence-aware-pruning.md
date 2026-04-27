---
title: Coherence-Aware Pruning
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ML, neural-networks, pruning, coherence]
---

# Coherence-Aware Pruning

## Summary
Coherence-aware pruning is a technique for removing redundant or "dead" attention heads in transformer models while maintaining the model's coherence (internal consistency). The approach is based on research from the "Coherence-Guided Dead-Head Identification" repository.

## Key Concepts

### Dead Heads in Transformers
Research shows that ~30-47% of attention heads in large language models can be "dead" — heads that contribute minimal useful computation to the model's outputs. Identifying these heads allows targeted pruning without performance degradation.

### BKT Phase Transition
The technique uses concepts from the Broken Knot Theory (BKT) phase transition model, originally developed for analyzing phase transitions in complex systems, applied to the analysis of attention head behavior in neural networks.

### Kuramoto Model
The Kuramoto model is used to analyze synchronization patterns in attention heads, helping identify which heads are truly essential for model coherence versus which can be pruned.

### Coherence Metrics
The approach measures "coherence" as the internal consistency of the model's representations. When dead heads are removed, coherence metrics help ensure the remaining network maintains proper information flow.

## Technical Approach

### SVD Spectral Filtering
Singular Value Decomposition (SVD) is used to analyze the spectral properties of attention matrices, identifying heads with minimal contribution to the model's representation capacity.

### Rotation Compensation
When pruning attention heads, rotation-based compensation helps preserve the model's output quality by adjusting the remaining weights to compensate for removed heads.

### LoRA Compensation
Low-Rank Adaptation (LoRA) can be applied post-pruning to recover any lost performance from removed heads, effectively fine-tuning the remaining network.

## Related Concepts
- [[github-coherence-guided-dead-head-identification]]
- [[apple-silicon-llm-optimization]]
- [[fine-tuning]]
