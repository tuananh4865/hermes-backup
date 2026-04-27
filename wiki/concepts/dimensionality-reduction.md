---
title: "Dimensionality Reduction"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, dimensionality-reduction, feature-engineering, data-preprocessing, unsupervised-learning]
---

# Dimensionality Reduction

## Overview

Dimensionality reduction is the process of transforming high-dimensional data into a lower-dimensional representation while preserving as much of the important structure and relationships as possible. In machine learning, data with hundreds or thousands of features (dimensions) is common—image pixels, word embeddings, sensor readings, genomic data. High dimensionality creates challenges including the curse of dimensionality, computational intractability, overfitting, and difficulty interpreting results.

Dimensionality reduction addresses these challenges by finding compact representations that capture the essential patterns in the data. These reduced representations can be used for visualization, as inputs to downstream machine learning models, for data compression, or to discover latent factors that explain observed variations.

## Key Concepts

**Intrinsic Dimensionality** refers to the minimum number of dimensions needed to accurately represent the data. Real-world data often has a much lower intrinsic dimensionality than the number of raw features. For example, a dataset of face images might have tens of thousands of pixels per image, but the space of recognizable faces can be described by a much smaller number of principal components (dozens to hundreds, not thousands).

**Linear vs Non-Linear Methods**: Linear methods like [[Principal Component Analysis]] (PCA) find linear subspaces that capture maximum variance. Non-linear methods like t-SNE, UMAP, and autoencoders can capture more complex, curved manifold structures in the data.

**Variance Preservation** is the goal of PCA—finding directions of maximum variance in the data. The intuition is that high-variance directions carry more information than low-variance directions (which may just be noise).

**Local vs Global Structure**: PCA is a global method—it preserves relationships across the entire dataset. t-SNE and UMAP are local methods—they prioritize preserving neighborhood relationships (which points are close to which other points), often at the expense of global structure.

## How It Works

**Principal Component Analysis (PCA)** finds orthogonal axes (principal components) in order of decreasing variance. The first $k$ components define a $k$-dimensional subspace that captures the most variance. PCA is computed via eigendecomposition of the covariance matrix or via singular value decomposition (SVD). It's a linear projection, which means it can only find linear subspaces.

```python
# PCA example
from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
import numpy as np

iris = load_iris()
X = iris.data  # 150 samples, 4 features

# Reduce to 2 dimensions
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X)

print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
print(f"Total variance explained: {sum(pca.explained_variance_ratio_):.2%}")
# Output: ~97.77% of variance retained in 2 dimensions
```

**t-SNE** (t-Distributed Stochastic Neighbor Embedding) converts distances to probabilities. It places points in low dimensions such that the distribution of pairwise distances matches the original high-dimensional distribution. It uses a heavy-tailed Student t-distribution in the low-dimensional space to spread out clusters and avoid crowding problems.

**UMAP** (Uniform Manifold Approximation and Projection) is a newer technique that provides faster computation, better preservation of both local and global structure, and supports metric learning. It is based on topological and manifold ideas.

**Autoencoders** are neural networks trained to compress data to a low-dimensional bottleneck and then reconstruct the original input. The bottleneck layer provides a learned non-linear dimensionality reduction.

## Practical Applications

- **Data Visualization**: Reducing to 2-3 dimensions for scatter plots and visual exploration
- **Noise Reduction**: Filtering out minor variations by projecting onto principal components
- **Computational Efficiency**: Reducing feature dimensionality before training downstream models
- **Image Compression**: Storing images in compressed latent representations
- **Feature Extraction**: Creating compact features for image or text classification
- **Anomaly Detection**: Points far from the learned manifold may be anomalous
- **Bioinformatics**: Reducing genomic data dimensionality for clustering and classification

## Examples

```python
# UMAP for visualization
import umap
import numpy as np
from sklearn.datasets import load_digits

digits = load_digits()
X = digits.data  # 1797 samples, 64 dimensions

# Reduce to 2D for visualization
reducer = umap.UMAP(n_components=2, random_state=42)
X_embedded = reducer.fit_transform(X)

print(f"Original shape: {X.shape}")
print(f"Embedded shape: {X_embedded.shape}")
# Original: (1797, 64) -> Embedded: (1797, 2)
```

## Related Concepts

- [[PCA (Principal Component Analysis)]] — the most common linear dimensionality reduction
- [[Unsupervised Learning]] — the broader category to which most dimensionality reduction belongs
- [[Feature Engineering]] — the broader practice of transforming data for ML
- [[t-SNE]] — a popular non-linear method for visualization
- [[UMAP]] — a more recent non-linear method with better computational properties
- [[Autoencoder]] — neural network-based dimensionality reduction

## Further Reading

- "Elements of Statistical Learning" — Chapter on dimensionality reduction
- "Mathematics for Machine Learning" — excellent coverage of the linear algebra behind PCA
- UMAP paper: "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction"

## Personal Notes

PCA is underrated as an exploratory tool. Before jumping to complex non-linear methods, it's worth understanding what the principal components reveal about your data. I've found that even a simple PCA plot can expose outliers, clusters, and the effective rank of the data matrix. UMAP has largely replaced t-SNE for visualization in my workflow due to its speed and better preservation of global structure.
