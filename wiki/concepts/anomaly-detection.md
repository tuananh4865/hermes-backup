---
title: "Anomaly Detection"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, unsupervised-learning, outlier-detection, data-science]
---

## Overview

Anomaly detection (also called outlier detection) is the task of identifying data points, events, or observations that deviate significantly from the expected pattern or normal behavior. These anomalies—also called outliers, novelties, or intrusions depending on the domain—often represent critical information such as fraud, system failures, security breaches, or manufacturing defects.

The challenge of anomaly detection is fundamentally different from supervised learning because anomalies are often rare, their exact characteristics are unknown in advance, and labeling large datasets of normal versus anomalous behavior is typically impractical. This makes anomaly detection primarily an unsupervised or semi-supervised problem.

Anomaly detection has become increasingly important in the era of big data, IoT, and cybersecurity. Modern systems generate massive volumes of operational data, and manually monitoring all of it is impossible. Automated anomaly detection enables organizations to identify problems in real-time, often before they escalate into outages or security incidents.

## Key Concepts

**Types of Anomalies:**

- **Point Anomalies** - Individual data points that are anomalous relative to the rest of the data. Example: a credit card transaction of $50,000 when most transactions are under $100.
  
- **Contextual Anomalies** - Points that are anomalous in a specific context but normal elsewhere. Example: a temperature of 30°C is normal in summer but anomalous in winter.
  
- **Collective Anomalies** - A collection of data points that together constitute an anomaly, even if individual points appear normal. Example: a rapid sequence of login attempts, each seemingly legitimate, but the pattern indicates a brute-force attack.

**Detection Approaches:**

- **Statistical Methods** - Assume a underlying distribution for normal data and flag points with low probability. Examples: Z-score, Grubbs' test, chi-squared test, Gaussian Mixture Models.
  
- **Proximity-Based Methods** - Flag points that are far from their neighbors or from cluster centers. Examples: k-NN distance, Local Outlier Factor (LOF), Isolation Forest.
  
- **Linear Models** - Learn a reconstruction of normal data and flag high reconstruction error. Example: Principal Component Analysis (PCA) for high-dimensional data.
  
- **Deep Learning Methods** - Learn complex representations of normal data. Examples: Autoencoders, Variational Autoencoders (VAE), LSTM-based models for time series.

**Evaluation Metrics** are tricky for anomaly detection since labeled anomalies are rare. Common metrics include:
- Precision, Recall, F1-score at various thresholds
- Area Under ROC Curve (AUC-ROC)
- Area Under Precision-Recall Curve (AUC-PR) — preferred when anomalies are rare
- Mean Time to Detect (MTTD) for operational metrics

## How It Works

A typical anomaly detection workflow:

```python
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Generate synthetic data with anomalies
np.random.seed(42)
normal_data = np.random.randn(1000, 2) * 0.5 + [0, 0]
anomalies = np.random.randn(20, 2) * 2 + [5, 5]  # Outliers far from normal
X = np.vstack([normal_data, anomalies])

# Standardize features (important for many algorithms)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Isolation Forest (unsupervised)
iso_forest = IsolationForest(contamination=0.02, random_state=42)
iso_forest.fit(X_scaled)

# Predict: -1 for anomalies, 1 for normal
predictions = iso_forest.predict(X_scaled)
anomaly_scores = iso_forest.score_samples(X_scaled)

# Visualize
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(X[:, 0], X[:, 1], c=predictions, cmap='coolwarm', alpha=0.6)
plt.title('Isolation Forest Predictions')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')

plt.subplot(1, 2, 2)
plt.hist(anomaly_scores, bins=50, edgecolor='black')
plt.axvline(x=-0.1, color='r', linestyle='--', label='Threshold')
plt.title('Anomaly Score Distribution')
plt.xlabel('Anomaly Score')
plt.legend()

plt.tight_layout()
plt.show()
```

## Practical Applications

**Cybersecurity** - Network intrusion detection, malware detection, insider threat identification, and anomaly-based antivirus systems. SIEM (Security Information and Event Management) tools heavily rely on anomaly detection.

**Financial Fraud Detection** - Credit card fraud, insurance claim fraud, money laundering detection. Transaction monitoring systems flag unusual spending patterns.

**Industrial Monitoring** - Detecting equipment failures from sensor data, predictive maintenance, quality control in manufacturing. Sensors on machines can detect vibrations, temperatures, and sounds that precede failures.

**Healthcare** - Identifying unusual patient vital signs, detecting hospital-acquired infections, flagging potential medical errors.

**Log Analysis** - Automated monitoring of system logs to detect operational issues, security events, or performance degradation.

## Examples

**Time Series Anomaly Detection with Z-Score:**
```python
import pandas as pd
import numpy as np

def detect_anomalies_zscore(series, threshold=3):
    """Detect anomalies using rolling Z-score."""
    mean = series.rolling(window=30, center=True).mean()
    std = series.rolling(window=30, center=True).std()
    z_scores = (series - mean) / std
    
    return np.abs(z_scores) > threshold

# Apply to sensor data
df = pd.read_csv('sensor_readings.csv', parse_dates=['timestamp'])
df['is_anomaly'] = detect_anomalies_zscore(df['temperature'])
anomalies = df[df['is_anomaly']]
```

**One-Class SVM for Novelty Detection:**
```python
from sklearn.svm import OneClassSVM

# Train only on normal data (semi-supervised approach)
normal_samples = X[predictions == 1]

ocsvm = OneClassSVM(kernel='rbf', nu=0.01)
ocsvm.fit(normal_samples)

# Predict on new data
new_predictions = ocsvm.predict(X_new)
```

**Isolation Forest for High-Dimensional Data:**
```python
# Works well with many features and mixed data types
iso_forest = IsolationForest(
    n_estimators=200,
    contamination='auto',  # Don't assume anomaly rate
    max_samples=min(256, len(X)),
    random_state=42
)
```

## Related Concepts

- [[Unsupervised Learning]] - Machine learning without labeled responses
- [[Supervised Learning]] - Classification with labeled data (for when you have labeled anomalies)
- [[Machine Learning]] - The broader field containing anomaly detection
- [[Time Series Analysis]] - Anomaly detection in temporal data
- [[Statistical Process Control]] - Industrial application of anomaly detection
- [[Fraud Detection]] - Practical application domain

## Further Reading

- [Scikit-learn Outlier Detection Documentation](https://scikit-learn.org/stable/modules/outlier_detection.html)
- [PyOD Library](https://pyod.readthedocs.io/) - Comprehensive Python outlier detection library
- ["Outlier Analysis" by Charu Aggarwal](https://www.springer.com/gp/book/9781461463955)

## Personal Notes

The choice of algorithm depends heavily on the data characteristics and use case. For low-dimensional tabular data, Isolation Forest and LOF often work well. For time series, consider Prophet, LSTM-autoencoders, or statistical methods. For high-dimensional data, consider PCA-based methods or deep autoencoders. Always understand your false positive tolerance—flagging too many normal events as anomalies creates alert fatigue. A useful exercise is to plot the anomaly score distribution; a bimodal distribution often indicates good separation, while a unimodal distribution suggests either no anomalies or the need for a different approach.
