---
title: "Hierarchical Clustering"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, unsupervised-learning, clustering, data-science]
---

## Overview

Hierarchical clustering is an unsupervised machine learning technique that builds a hierarchy of clusters. Unlike flat clustering algorithms (like k-means) that produce a single partition of the data, hierarchical clustering creates a dendrogram—a tree-like structure that represents nested groupings at multiple scales. This approach is particularly valuable when the natural number of clusters is unknown or when exploring hierarchical relationships within data.

The technique has roots in taxonomy and biology, where scientists have long classified organisms into taxonomic ranks (kingdom, phylum, class, order, family, genus, species). Hierarchical clustering extends this thinking to any numerical data, revealing structure at multiple granularity levels.

Hierarchical clustering is widely used in bioinformatics (gene expression analysis), document organization, customer segmentation, anomaly detection, and exploratory data analysis. Its ability to produce interpretable dendrograms makes it valuable when understanding cluster relationships matters as much as the clusters themselves.

## Key Concepts

**Agglomerative (Bottom-Up) Clustering** starts with each data point as its own cluster and iteratively merges the closest pairs of clusters until only one cluster remains. This builds the dendrogram from leaves to root. Most hierarchical clustering implementations use agglomerative approach.

**Divisive (Top-Down) Clustering** starts with all points in a single cluster and recursively splits clusters until each point is in its own cluster. This approach is less common but can be computationally efficient for certain scenarios.

**Linkage Methods** determine how distance between clusters is calculated:

- **Single Linkage** - Minimum distance between any two points in different clusters. Can produce elongated, chain-like clusters.
- **Complete Linkage** - Maximum distance between any two points in different clusters. Tends to produce compact, spherical clusters.
- **Average Linkage (UPGMA)** - Mean distance between all pairs of points in different clusters. A good compromise between single and complete linkage.
- **Ward's Method** - Minimizes the increase in total within-cluster variance. Tends to find compact clusters of similar sizes.

**Distance Metrics** measure similarity between points. Common choices include:
- Euclidean distance (L2 norm)
- Manhattan distance (L1 norm)
- Cosine similarity (angle between vectors)
- Mahalanobis distance (accounting for correlation)

**Dendrogram** is the tree diagram showing the hierarchical relationships. Cutting the dendrogram at different heights produces different numbers of clusters. The height of each merge represents the dissimilarity at which that merge occurred.

## How It Works

Agglomerative hierarchical clustering follows this algorithm:

```
1. Start with N clusters (each point is its own cluster)
2. Compute pairwise distance matrix for all clusters
3. Repeat until only one cluster remains:
   a. Find the pair of clusters with minimum distance
   b. Merge these two clusters into one
   c. Update distance matrix
4. Record merge distance at each step (for dendrogram)
```

The complexity is O(N² log N) for most implementations, making it computationally expensive for large datasets. Optimizations exist using data structures like nearest-neighbor chains.

```python
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from scipy.spatial.distance import pdist
import matplotlib.pyplot as plt

# Generate sample data: three distinct groups
np.random.seed(42)
cluster1 = np.random.randn(30, 2) + [0, 0]
cluster2 = np.random.randn(30, 2) + [5, 5]
cluster3 = np.random.randn(30, 2) + [0, 5]

data = np.vstack([cluster1, cluster2, cluster3])

# Compute pairwise distances (Euclidean by default)
distances = pdist(data)

# Perform hierarchical clustering using Ward's method
linkage_matrix = linkage(distances, method='ward')

# Plot dendrogram
plt.figure(figsize=(10, 6))
dendrogram(linkage_matrix, truncate_mode='level', p=5)
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('Sample Index or Cluster Size')
plt.ylabel('Distance (Ward)')
plt.show()

# Extract clusters at a specific distance threshold
# (cutting where we expect 3 clusters)
cluster_labels = fcluster(linkage_matrix, t=3, criterion='maxclust')
print(f"Cluster assignments: {cluster_labels}")
```

## Practical Applications

**Biology and Bioinformatics** - Phylogenetic analysis, gene expression clustering (e.g., TCGA cancer data), protein sequence analysis, and species classification.

**Document Organization** - Clustering news articles, organizing research papers by topic, organizing large document repositories for navigation.

**Customer Segmentation** - Identifying customer groups with similar behavior for targeted marketing, without requiring advance knowledge of segment count.

**Image Analysis** - Object recognition, image compression through palette clustering, and medical image segmentation.

**Anomaly Detection** - Points that don't fit any cluster or join at very high levels (far from root) may be anomalies.

## Examples

**Gene Expression Analysis (simplified):**
```python
# Gene expression matrix: rows = genes, columns = samples
# Each value represents expression level

from scipy.cluster.hierarchy import dendrogram, linkage
import pandas as pd

# Load gene expression data
expression_data = pd.read_csv('gene_expression.csv', index_col=0)

# Compute sample-wise clustering (columns)
sample_linkage = linkage(expression_data.values.T, method='average')

# Visualize sample relationships
dendrogram(sample_linkage, labels=expression_data.columns)
```

**Cutting the Dendrogram:**
```python
# Different ways to extract flat clusters

# Fixed number of clusters
clusters_k3 = fcluster(linkage_matrix, t=3, criterion='maxclust')

# Distance threshold (clusters merged above this distance)
clusters_t5 = fcluster(linkage_matrix, t=5.0, criterion='distance')

# Inconsistency-based (accounts for local density)
clusters_inconsistent = fcluster(linkage_matrix, depth=7)
```

## Related Concepts

- [[Unsupervised Learning]] - Machine learning without labeled responses
- [[K-Means Clustering]] - Flat clustering alternative
- [[DBSCAN]] - Density-based clustering that finds arbitrary shapes
- [[Principal Component Analysis]] - Dimensionality reduction often used before clustering
- [[Machine Learning]] - The broader field containing clustering techniques
- [[Data Mining]] - Pattern discovery where clustering is a key technique

## Further Reading

- [SciPy Hierarchical Clustering Documentation](https://docs.scipy.org/doc/scipy/reference/cluster.hierarchy.html)
- ["The Elements of Statistical Learning" - Chapter on Clustering](https://web.stanford.edu/~hastie/ElemStatLearn/)
- [Hierarchical Clustering Explained (StatQuest)](https://www.youtube.com/watch?v=ijUM7nK6-W0)

## Personal Notes

Hierarchical clustering's main advantage over k-means is the dendrogram—visualizing cluster structure without pre-specifying the number of clusters. The choice of linkage method significantly impacts results; Ward's method often works well for continuous data, while average linkage is more robust to noise. For large datasets (>10K points), consider using approximate methods or sampling first. The dendrogram height interpretation is intuitive: higher merges indicate more dissimilar clusters being forced together.
