---
title: "Feature Engineering"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, data-science, preprocessing, feature-engineering, ml-pipeline]
---

# Feature Engineering

## Overview

Feature engineering is the process of transforming raw data into features that better represent the underlying problem to predictive models. It involves selecting, modifying, and creating variables (features) from raw data to improve machine learning model performance. The quality of features profoundly impacts model accuracy more than the choice of algorithm itself—a principle often summarized as "better data beats better algorithms."

Feature engineering sits at the intersection of domain expertise and data science. It requires understanding the specific problem domain, the characteristics of the dataset, and the requirements of the learning algorithm. Effective feature engineering can dramatically improve model performance, reduce computational costs, and make models more interpretable.

The process is typically iterative and exploratory. Data scientists examine distributions, correlations, and relationships in data; create hypotheses about informative features; test those features; and refine based on model performance. Domain experts often provide invaluable insights about which transformations might capture meaningful patterns.

## Key Concepts

**Feature Selection**: Identifying the most relevant features for a model while removing redundant or irrelevant ones. Techniques include correlation analysis, mutual information, recursive feature elimination, and tree-based importance scores. Selection reduces overfitting, improves model interpretability, and decreases training time.

**Feature Transformation**: Converting features into formats more suitable for modeling. This includes normalization (scaling values to a standard range), standardization (rescaling to have zero mean and unit variance), log transformations for skewed distributions, and power transforms like Box-Cox.

**Feature Encoding**: Converting categorical variables into numerical representations. One-hot encoding creates binary columns for each category; label encoding assigns integer labels; target encoding uses the mean target value per category. More advanced methods like weight of evidence encoding are used in credit scoring and similar domains.

**Feature Creation**: Generating new features from existing ones through domain-informed calculations. For timestamps, extracting hour-of-day, day-of-week, or month. For text, creating word counts, TF-IDF scores, or embedding vectors. For transactions, calculating aggregates like running totals, averages, or ratios.

**Handling Missing Values**: Strategies include imputation (filling with mean, median, mode, or predicted values), indicator columns showing which values were missing, and algorithms that handle missingness natively.

## How It Works

A typical feature engineering pipeline processes raw data through several stages:

1. **Data Cleaning**: Removing duplicates, correcting inconsistencies, handling outliers
2. **Exploratory Analysis**: Understanding distributions, relationships, and patterns
3. **Feature Creation**: Generating new variables based on domain knowledge
4. **Feature Encoding**: Converting categorical variables
5. **Feature Scaling**: Normalizing or standardizing numerical features
6. **Feature Selection**: Choosing the most informative subset
7. **Validation**: Testing engineered features with cross-validation

```python
# Example feature engineering pipeline
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Create features from raw data
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday']).astype(int)
df['log_amount'] = np.log1p(df['amount'])  # Log transform for skewed data

# Define preprocessing for different column types
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), ['amount', 'log_amount', 'hour']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['category', 'region'])
    ])
```

## Practical Applications

**Credit Scoring**: Financial institutions engineer features from transaction histories, combining recency, frequency, monetary values with derived ratios like debt-to-income. They create behavioral features like payment consistency scores and spending pattern changes.

**Recommendation Systems**: E-commerce platforms create user features from browsing history, purchase patterns, and demographic data. Item features include category embeddings, price tiers, and popularity metrics. Interaction features capture user-item affinity patterns.

**Fraud Detection**: Transactional data is enriched with velocity features (transactions per minute), geographic features (distance from last transaction), device fingerprints, and temporal patterns. Behavioral biometrics features capture typing speed and mouse movement patterns.

**Natural Language Processing**: Text is transformed into numerical representations through TF-IDF weighting, word embeddings (Word2Vec, GloVe, BERT), and document embeddings. Character-level features capture writing style for authorship attribution.

## Examples

Creating time-based features for a sales prediction model:

```python
import pandas as pd
import numpy as np

def engineer_time_features(df, timestamp_col='transaction_date'):
    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    
    # Cyclical encoding for periodic features
    df['hour_sin'] = np.sin(2 * np.pi * df[timestamp_col].dt.hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df[timestamp_col].dt.hour / 24)
    df['day_of_month_sin'] = np.sin(2 * np.pi * df[timestamp_col].dt.day / 31)
    df['day_of_month_cos'] = np.cos(2 * np.pi * df[timestamp_col].dt.day / 31)
    
    # Binary features
    df['is_month_start'] = df[timestamp_col].dt.is_month_start.astype(int)
    df['is_month_end'] = df[timestamp_col].dt.is_month_end.astype(int)
    df['is_quarter_start'] = df[timestamp_col].dt.is_quarter_start.astype(int)
    
    # Aggregation features
    df['day_of_week_name'] = df[timestamp_col].dt.day_name()
    df['month_name'] = df[timestamp_col].dt.month_name()
    
    return df
```

## Related Concepts

- [[Machine Learning]] - The broader discipline this technique serves
- [[Data Preprocessing]] - Cleaning and organizing raw data
- [[Feature Selection]] - Choosing relevant features
- [[Regularization]] - Techniques to prevent overfitting
- [[Cross-Validation]] - Testing model generalization
- [[Scikit-learn]] - Python library for ML preprocessing
- [[Pandas]] - Data manipulation library

## Further Reading

- [Feature Engineering for Machine Learning (O'Reilly)](https://www.oreilly.com/library/view/feature-engineering-for/9781491953235/)
- [Kaggle Feature Engineering Tutorial](https://www.kaggle.com/feature-engineering-and-data-preprocessing)
- [A Practical Guide to Feature Engineering](https://towardsdatascience.com/feature-engineering-guide)

## Personal Notes

The most impactful feature engineering work I've done came from deep domain immersion. When building a demand forecasting model, simply spending time with the supply chain team revealed patterns like holiday-adjacent demand spikes and promotional calendar effects that weren't visible in raw data. No amount of automated feature generation replaces domain intuition. That said, automated feature engineering tools (like Featuretools) can discover interactions that humans miss, especially in domains where we lack prior knowledge. The best approach combines human insight with systematic exploration—I use automated methods to generate candidate features, then apply business logic to filter and refine them.
