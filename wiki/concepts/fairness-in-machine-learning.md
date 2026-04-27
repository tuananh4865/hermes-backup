---
title: Fairness in Machine Learning
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [fairness, ml, ethics, bias, ai-safety]
---

# Fairness in Machine Learning

Fairness in machine learning addresses the challenge of ensuring AI systems do not discriminate or produce biased outcomes across different demographic groups. It encompasses the study, measurement, and mitigation of unfair biases that can emerge from training data, algorithmic design, or deployment contexts.

## Overview

Machine learning models learn from historical data, which often encodes societal biases and historical inequities. When these models make consequential decisions—in hiring, lending, criminal justice, healthcare—unfair biases can perpetuate or amplify discrimination. Fairness research provides frameworks for understanding, measuring, and addressing these issues.

The field grapples with fundamental tensions: technical definitions of fairness often conflict with each other (it's mathematically impossible to satisfy all fairness criteria simultaneously in many cases), and what constitutes "fair" treatment can itself be contested. Despite these challenges, practitioners have developed practical techniques for auditing and improving model fairness.

## Key Concepts

### Types of Bias

Bias can enter ML systems at multiple stages:

| Stage | Bias Type | Example |
|-------|-----------|---------|
| Data Collection | Selection Bias | Training data over-represents certain demographics |
| Data Labeling | Labeler Bias | Human annotators impose their own assumptions |
| Feature Engineering | Proxy Bias | Using zip code as feature correlates with race |
| Model Training | Algorithm Bias | Optimization objective inadvertently favors groups |
| Deployment | Aggregation Bias | One-size-fits-all model inappropriate for subgroups |

### Fairness Metrics

**Group Fairness**: Equal outcomes across groups
```python
# Demographic parity: equal positive prediction rates
def demographic_parity(y_pred, protected_attr):
    group_0 = y_pred[protected_attr == 0].mean()
    group_1 = y_pred[protected_attr == 1].mean()
    return abs(group_0 - group_1) < epsilon

# Equalized odds: equal true positive AND false positive rates
def equalized_odds(y_true, y_pred, protected_attr):
    tpr_g0 = y_true[protected_attr == 0 & y_pred == 1].mean()
    tpr_g1 = y_true[protected_attr == 1 & y_pred == 1].mean()
    fpr_g0 = y_true[protected_attr == 0 & y_pred == 0].mean()
    fpr_g1 = y_true[protected_attr == 1 & y_pred == 0].mean()
    return abs(tpr_g0 - tpr_g1) < epsilon and abs(fpr_g0 - fpr_g1) < epsilon
```

**Individual Fairness**: Similar individuals should be treated similarly
```python
# Fairness through awareness: if x and x' are similar, predictions should be similar
def individual_fairness(model, x1, x2, epsilon):
    distance_inputs = np.linalg.norm(x1 - x2)
    distance_outputs = abs(model.predict(x1) - model.predict(x2))
    return distance_outputs <= epsilon * distance_inputs
```

**Counterfactual Fairness**: Would decision change if protected attribute changed?
```python
# Check if flipping protected attribute changes prediction
def counterfactual_fairness(model, x, protected_attr_name):
    x_flipped = x.copy()
    x_flipped[protected_attr_name] = 1 - x_flipped[protected_attr_name]
    return model.predict(x) == model.predict(x_flipped)
```

## How It Works

1. **Bias Identification**: Audit training data and model predictions for disparities
2. **Metric Selection**: Choose appropriate fairness criteria for the domain
3. **Root Cause Analysis**: Determine whether bias stems from data, features, or algorithm
4. **Mitigation Strategy**: Apply pre-processing, in-processing, or post-processing techniques
5. **Fairness-Accuracy Tradeoff**: Navigate competing objectives (fair models may sacrifice some accuracy)
6. **Continuous Monitoring**: Track fairness metrics over time as models encounter new data

## Practical Applications

- **Hiring & Recruitment**: Ensuring job recommendations don't favor particular demographics
- **Credit Lending**: Preventing discriminatory loan denials based on race, gender, or zip code
- **Criminal Justice**: Auditing risk assessment tools for racial disparities
- **Healthcare**: Verifying diagnostic models work equitably across patient populations
- **Advertising**: Preventing targeted ads from being discriminatory (housing, employment)
- **Content Moderation**: Ensuring moderation decisions don't disproportionately affect groups

## Examples

### Bias Detection with Fairlearn

```python
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference
from sklearn.metrics import accuracy_score

# Create metric frame with sensitive feature (e.g., gender)
metric_frame = MetricFrame(
    metrics={
        'accuracy': accuracy_score,
        'selection_rate': selection_rate
    },
    y_true=y_test,
    y_pred=model.predict(X_test),
    sensitive_features=X_test['gender']
)

# Print detailed metrics by group
print(metric_frame.by_group)

# Calculate disparity
dp_diff = demographic_parity_difference(y_test, model.predict(X_test), 
                                        sensitive_features=X_test['gender'])
print(f"Demographic parity difference: {dp_diff:.3f}")
```

### Pre-processing: Reweighting Data

```python
def reweight_dataset(X, y, protected_attr):
    """Reweight samples to ensure fair representation"""
    df = X.copy()
    df['label'] = y
    
    # Calculate desired weights
    weights = {}
    for group in df[protected_attr].unique():
        for label in df['label'].unique():
            mask = (df[protected_attr] == group) & (df['label'] == label)
            # Weight inversely proportional to representation
            n_group_label = mask.sum()
            n_total = len(df)
            n_group = (df[protected_attr] == group).sum()
            n_label = (df['label'] == label).sum()
            weights[mask] = (n_label * n_total) / (n_group * n_group_label + 1e-10)
    
    return weights
```

## Related Concepts

- [[ai-ethics]] — Broader ethical considerations in AI development
- [[safety]] — AI safety and risk mitigation
- [[bias-in-ai]] — Cataloging specific types of AI biases
- [[explainable-ai]] — Interpretability techniques for understanding model decisions
- [[model-evaluation]] — Evaluating model performance beyond accuracy

## Further Reading

- "Fairness and Machine Learning" (Barocas, Hardt, Narayanan - free online book)
- IBM AI Fairness 360 documentation
- Microsoft Fairlearn toolkit
- NIST TPUS (Trusted AI) guidelines

## Personal Notes

Fairness in ML is fundamentally a socio-technical challenge—purely technical solutions can't fully address it because fairness involves value judgments about what "should" happen. The math often forces uncomfortable tradeoffs: optimizing for one fairness criterion can hurt another, or fairness might reduce aggregate accuracy even if it increases individual fairness. I think the most practical approach is: (1) always audit models for disparities before deployment, (2) engage stakeholders in defining what fairness means in context, (3) treat fairness as an ongoing property requiring monitoring, not a one-time fix. There's also growing recognition that sometimes we shouldn't automate certain decisions at all—the risk of unfairness is too high.
