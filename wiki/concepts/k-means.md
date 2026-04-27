---
title: K-Means Clustering
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, clustering, unsupervised-learning, algorithms, data-science]
---

## Overview

K-Means is one of the most widely used unsupervised machine learning algorithms for partitioning a dataset into K distinct, non-overlapping clusters. Given a set of N data points in D-dimensional space and an integer K, the algorithm assigns each point to exactly one of K clusters, minimizing the within-cluster variance (the sum of squared distances from each point to its cluster's centroid).

The algorithm is simple, fast, and scalable—making it a workhorse for exploratory data analysis, customer segmentation, image compression, anomaly detection, and many other applications. Despite its simplicity, K-Means has a rich theoretical foundation and continues to be relevant as a building block in more sophisticated pipelines.

The name "k-means" was coined by James MacQueen in 1967, though the algorithm's underlying ideas had been used earlier by Stuart Lloyd at Bell Labs in 1957 (though Lloyd's work wasn't published until 1982).

## Key Concepts

**Centroids** are the center points of each cluster, calculated as the mean (average) of all data points assigned to that cluster. The algorithm iteratively refines these centroids until convergence.

**Within-Cluster Sum of Squares (WCSS)** is the objective function K-Means minimizes. For each cluster k, it computes the sum of squared Euclidean distances between every point and the cluster's centroid. The total WCSS is the sum across all clusters. Lower WCSS means tighter clusters.

**Random Initialization** is a major source of variability in K-Means results. Because the algorithm converges to a local optimum (not necessarily the global optimum), different initial placements of centroids can produce dramatically different final clusters. The **K-Means++** initialization method (Arthur & Vassilvitskii, 2007) addresses this by spreading initial centroids apart, dramatically improving both the quality of results and convergence speed.

**The Elbow Method** is a heuristic for choosing K. You run K-Means for a range of K values, plot the WCSS (or total inertia) for each K, and look for the "elbow"—the point where adding more clusters yields diminishing returns. This is often where the curve bends sharply.

**Silhouette Score** is a more principled alternative to the elbow method. For each point, it measures how similar the point is to its own cluster compared to the nearest other cluster, ranging from -1 to +1. Higher values indicate better-defined clusters.

## How It Works

The algorithm proceeds in two alternating steps that repeat until convergence:

1. **Assign** each data point to the nearest centroid (using Euclidean distance in the standard formulation).
2. **Update** each centroid by recomputing it as the mean of all points assigned to that cluster.

The algorithm terminates when no points change cluster assignments (convergence) or a maximum number of iterations is reached.

```python
import numpy as np
from sklearn.cluster import KMeans

# Example: segmenting customers by behavior
# X is a numpy array of shape (n_customers, n_features)
# e.g., features might be: avg_monthly_spend, days_since_last_purchase

kmeans = KMeans(n_clusters=5, init='k-means++', n_init=10, random_state=42)
clusters = kmeans.fit_predict(X)

# View cluster centroids (5 x n_features matrix)
print(kmeans.cluster_centers_)

# Assign new customers to existing clusters
new_customer = np.array()  # $450/month, 12 days since last purchase
cluster_id = kmeans.predict(new_customer)
```

The `n_init=10` parameter tells sklearn to run the algorithm 10 times with different initializations and keep the best result (lowest WCSS). This is important because a single run can converge to a poor local optimum.

## Practical Applications

**Customer Segmentation** is the canonical business use case. A retailer might use K-Means to group customers by purchasing behavior, demographics, and engagement patterns. Each segment then receives targeted marketing—for example, high-frequency high-value customers get exclusive offers, while dormant customers get win-back campaigns.

**Image Compression** treats each pixel's color as a 3D point (R, G, B). K-Means quantizes these colors to K cluster centroids, replacing each pixel's color with its centroid's color. This reduces the number of unique colors and can achieve significant compression, especially for photographs with large uniform regions.

**Document Clustering** converts text documents into TF-IDF vectors (or embeddings), then applies K-Means to group them by topic. This is the approach behind automated news aggregation and spam filtering.

**Anomaly Detection** in sensor data: normal operating conditions form tight clusters; data points far from any centroid represent anomalies. This is used in industrial IoT for equipment health monitoring.

## Examples

A complete K-Means workflow with the elbow method:

```python
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# Generate synthetic data
X, _ = make_blobs(n_samples=500, centers=4, cluster_std=1.0, random_state=42)

# Evaluate different K values using inertia (WCSS)
inertias = []
silhouette_scores = []
K_range = range(2, 11)

from sklearn.metrics import silhouette_score

for k in K_range:
    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    kmeans.fit(X)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X, kmeans.labels_))

# Plot the elbow curve
plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Inertia (WCSS)')
plt.title('Elbow Method')

plt.subplot(1, 2, 2)
plt.plot(K_range, silhouette_scores, 'go-')
plt.xlabel('Number of clusters (K)')
plt.ylabel('Silhouette Score')
plt.title('Silhouette Analysis')
plt.tight_layout()
plt.savefig('kmeans_evaluation.png')
```

Running this typically shows K=4 as the natural choice—the elbow in the inertia curve and the peak in the silhouette score both point to 4 clusters, matching the ground truth used in `make_blobs`.

## Related Concepts

- [[clustering-algorithms]] — The broader family of unsupervised clustering methods
- [[unsupervised-learning]] — Machine learning without labeled targets
- [[k-nearest-neighbors]] — A related but supervised classification algorithm
- [[principal-component-analysis]] — Often used to reduce dimensionality before clustering
- [[machine-learning]] — The broader field containing K-Means

## Further Reading

- "Least Squares Quantization in PCM" by Stuart Lloyd (1982) — the original paper
- "k-means++: The Advantages of Careful Seeding" by Arthur & Vassilvitskii (2007)
- Scikit-learn's K-Means documentation — excellent practical reference

## Personal Notes

I always use `init='k-means++'` and `n_init=10` (or higher) when using sklearn's KMeans. The default initialization in sklearn is already k-means++, but many tutorials show explicit initialization steps that aren't necessary. I've found that running K-Means 10-20 times with different seeds and keeping the best result almost always outperforms a single run, especially when K is large or the data has high variance. Also remember: K-Means assumes clusters are spherical and of roughly equal size, which is rarely true in practice—it's a useful baseline but not the last word on clustering.
