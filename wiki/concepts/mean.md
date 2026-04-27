---
title: "Mean"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [statistics, mathematics, data-analysis, averages]
---

# Mean

## Overview

The mean (arithmetic mean, commonly called "average") is the sum of a collection of values divided by the count of values. It is the most widely used measure of central tendency—a single number representing the typical magnitude of a dataset. The mean summarizes a distribution with one number, enabling comparison between distributions and serving as the foundation for more sophisticated statistical analysis.

Despite its simplicity, the mean has important statistical properties that make it indispensable: it minimizes squared error (the sum of squared deviations from the mean is always less than from any other point), it permits algebraic manipulation (the mean of combined datasets can be computed from component means), and it arises naturally in many mathematical contexts.

The mean is distinct from the median (middle value) and mode (most frequent value). For symmetric distributions without outliers, these coincide. For skewed distributions—like income (where few high values pull the mean above most observations), the mean can be misleading, and the median often better represents typical experience.

## Key Concepts

### Arithmetic Mean

The arithmetic mean is the sum divided by count:

$$\bar{x} = \frac{1}{n} \sum_{i=1}^{n} x_i$$

In plain terms: add all values, divide by how many there are.

### Geometric Mean

The geometric mean multiplies values and takes the nth root. It is appropriate for multiplicative processes or values with different scales:

$$\bar{x}_{geometric} = \left(\prod_{i=1}^{n} x_i\right)^{1/n}$$

Growth rates, ratios, and percentages are better summarized with geometric mean. A fund returning 10%, then losing 10%, has a geometric mean return of 0% (not 0% arithmetic), correctly indicating you end up where you started.

### Harmonic Mean

The harmonic mean is the reciprocal of the arithmetic mean of reciprocals. It is appropriate for rates and ratios:

$$\bar{x}_{harmonic} = \frac{n}{\sum_{i=1}^{n} \frac{1}{x_i}}$$

For averaging speeds: traveling 60 mph for 1 hour and 30 mph for 1 hour gives an average speed of 40 mph (harmonic), not 45 mph (arithmetic).

### Weighted Mean

The weighted mean assigns different importance to values:

$$\bar{x}_{weighted} = \frac{\sum_{i=1}^{n} w_i x_i}{\sum_{i=1}^{n} w_i}$$

This appears in [[RICE scoring|RICE]] where reach, impact, confidence, and effort are weighted differently, in grade calculations where exams count more than homework, and in financial indexing where market-cap weighting reflects actual economic significance.

## How It Works

The mean's mathematical properties make it algebraically convenient:

**Additivity**: The mean of combined datasets equals the weighted average of component means. If dataset A (n=10, mean=50) combines with dataset B (n=20, mean=70), the combined mean is (10×50 + 20×70)/30 = 65.

**Sensitivity to outliers**: A single extreme value dramatically shifts the mean. This is feature for some applications (detecting anomalies in fraud detection) and bug for others (typical salary representation).

**Minimization property**: The mean minimizes the sum of squared errors. This is why least squares regression fits the mean of y given x, why variance is computed around the mean, and why the mean is so prevalent in estimation theory.

## Practical Applications

### Performance Metrics

System [[performance optimization]] often uses mean latency, mean throughput, or mean error rates. But means hide distribution shape—[[Tail Latency]] at the 99th percentile often matters more than mean latency.

### A/B Testing

[[ab-testing]] uses means to compare treatment and control groups. The test statistic (often a t-test) evaluates whether observed mean differences are statistically significant or attributable to random variation.

### Scientific Measurement

Repeated measurements are summarized by mean ± standard deviation. The mean represents the best estimate of true value; standard deviation represents measurement precision.

### Financial Returns

Portfolio returns are typically summarized as annualized mean returns for comparison, though this obscures volatility and path dependency.

## Examples

Computing means in Python:

```python
from statistics import mean, geometric_mean, harmonic_mean

values = [10, 20, 30, 40, 50]

# Arithmetic mean
arithmetic = sum(values) / len(values)
print(f"Arithmetic: {arithmetic}")  # 30.0

# Geometric mean (for positive values)
geom = geometric_mean(values)
print(f"Geometric: {geom:.2f}")  # 24.49

# Harmonic mean (for non-zero positive values)
harm = harmonic_mean(values)
print(f"Harmonic: {harm:.2f}")  # 20.00

# Weighted mean
weights = [0.1, 0.2, 0.3, 0.3, 0.1]
weighted = sum(v * w for v, w in zip(values, weights)) / sum(weights)
print(f"Weighted: {weighted}")  # 31.0

# Handling outliers
outlier_values = [10, 20, 30, 40, 1000]
print(f"Mean with outlier: {mean(outlier_values)}")  # 220 (very high)
print(f"Median with outlier: {median(outlier_values)}")  # 30 (representative)
```

## Related Concepts

- [[Median]] - The middle value, robust to outliers
- [[Mode]] - The most frequent value
- [[Variance]] - Measure of spread around the mean
- [[Standard Deviation]] - Square root of variance, in original units
- [[Statistics]] - The broader field of data analysis

## Further Reading

- *Statistics* by Freedman, Pisani, Purves — Accessible introduction to descriptive statistics
- Khan Academy: Statistics and Probability — Visual explanations of mean, median, mode

## Personal Notes

The mean is a powerful summary but often misused. I see people compute mean salaries or mean house prices in regions with extreme inequality and wonder why the number feels wrong. The mean represents the mathematical center of a distribution, not the typical person. Always visualize the distribution before trusting the mean—histograms or box plots reveal skew and outliers that make the mean misleading. The median is often what people actually want when they ask for "average."
