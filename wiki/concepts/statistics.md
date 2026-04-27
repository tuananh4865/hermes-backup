---
title: "Statistics"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [mathematics, data-science, probability, inference]
---

# Statistics

## Overview

Statistics is the discipline of collecting, organizing, analyzing, interpreting, and presenting data. It provides the mathematical framework for making informed decisions in the presence of uncertainty. Statistics underpins modern data science, machine learning, scientific research, business intelligence, and virtually any field where data-driven decisions matter.

The field can be broadly divided into two branches. **Descriptive statistics** summarizes and organizes data using measures like mean, median, mode, variance, and standard deviation. **Inferential statistics** uses sample data to make predictions or generalizations about a larger population, employing techniques like hypothesis testing, confidence intervals, and regression analysis.

Statistics bridges pure mathematics and practical application—it provides rigorous methods for extracting signal from noise and quantifying uncertainty in findings.

## Key Concepts

### Descriptive Measures

**Central Tendency**: Values that represent the center of a distribution

- **Mean**: Arithmetic average, sum of values divided by count
- **Median**: Middle value when data is sorted (robust to outliers)
- **Mode**: Most frequently occurring value

**Variability**: Spread of data around central values

- **Variance**: Average squared deviation from the mean
- **Standard Deviation**: Square root of variance (same unit as data)
- **Range**: Difference between maximum and minimum
- **Interquartile Range (IQR)**: Range of middle 50% of data

### Probability Distributions

Understanding how data is distributed enables appropriate analysis:

- **Normal Distribution**: Symmetric, bell-shaped; central to many statistical methods
- **Binomial Distribution**: Outcomes of yes/no experiments
- **Poisson Distribution**: Counting events in fixed intervals
- **Exponential Distribution**: Time between events

### Hypothesis Testing

A formal procedure for making decisions about populations based on sample data:

1. State null (H0) and alternative (H1) hypotheses
2. Choose significance level (α, typically 0.05)
3. Calculate test statistic from sample data
4. Compute p-value—probability of observing results if H0 is true
5. Reject H0 if p-value < α

## How It Works

```python
import numpy as np
from scipy import stats

# Example: Descriptive statistics and hypothesis testing
data = np.array([23, 25, 28, 30, 32, 35, 37, 40, 42, 45, 50, 55, 60])

# Descriptive statistics
mean = np.mean(data)
median = np.median(data)
std_dev = np.std(data, ddof=1)  # Sample std dev
variance = np.var(data, ddof=1)

# One-sample t-test: Is mean significantly different from 35?
t_stat, p_value = stats.ttest_1samp(data, 35)
# If p_value < 0.05, reject null hypothesis

# 95% confidence interval for the mean
se = stats.sem(data)  # Standard error
ci = stats.t.interval(0.95, len(data)-1, loc=mean, scale=se)

# Linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(
    x=data, y=data * 0.7 + np.random.normal(0, 5, len(data))
)
```

## Practical Applications

Statistics is fundamental across all quantitative fields:

- **Clinical Trials**: Determining drug efficacy with rigorous significance testing
- **A/B Testing**: Comparing product versions to make release decisions
- **Quality Control**: Monitoring manufacturing processes for defects
- **Financial Analysis**: Risk assessment, portfolio optimization
- **Sports Analytics**: Player performance evaluation, strategy optimization
- **Climate Science**: Modeling temperature trends and weather patterns

## Examples

Consider an e-commerce company testing a new checkout flow. They randomly show the new design to 1000 users and the old to 1000 users. Statistics enables them to determine:

- Did conversion rate increase significantly?
- What is the range of plausible improvement?
- Is the result likely due to chance (random variation)?

This rigorous approach prevents intuition-driven decisions that ignore natural randomness.

## Related Concepts

- [[Probability Theory]] - Mathematical foundation of statistics
- [[Hypothesis Testing]] - Formal framework for statistical inference
- [[Regression Analysis]] - Technique for modeling relationships
- [[Machine Learning]] - Modern extension building on statistical foundations
- [[Data Science]] - Field that heavily uses statistical methods

## Further Reading

- "Statistics for Business and Economics" by McClave et al.
- "Think Stats" by Allen Downey (free online)
- NIST Engineering Statistics Handbook

## Personal Notes

Common statistical mistakes: confusing correlation with causation, ignoring confounding variables, multiple comparisons without correction, and overinterpreting p-values. Statistical significance doesn't always mean practical significance. Building intuition for uncertainty is more valuable than memorizing formulas.
