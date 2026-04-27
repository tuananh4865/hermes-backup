---
title: "Online Learning"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [machine-learning, online-learning, streaming-algorithms, incremental-learning, ai]
---

# Online Learning

## Overview

Online learning is a machine learning paradigm where a model learns from a sequence of data points one at a time (or in small batches), updating its predictions and parameters incrementally as new data arrives. Unlike batch learning, which trains on a fixed dataset in one go, online learning processes data continuously, adapting to drift and changes in the data distribution over time. This makes it essential for applications where data arrives in streams, where computational resources are limited, or where the problem itself evolves.

The defining characteristic of online learning is that each data point is seen only once (or briefly) before being discarded. The algorithm must balance learning from the new observation with not overfitting to it. This creates a fundamental tension between adaptability and stability—the "exploration-exploitation" tradeoff in the learning algorithm itself.

## Key Concepts

**Mistake-Bounded Learning** is a theoretical framework where online learning algorithms are analyzed by the number of mistakes they make. An algorithm is considered good if it makes a bounded number of mistakes even over arbitrarily long sequences of data. The Perceptron algorithm is a classic example—it can learn any linearly separable function with a finite number of mistakes.

**Regret** is the standard performance measure for online learning. Regret compares the cumulative loss of the online algorithm to the cumulative loss of the best fixed hypothesis in hindsight. Good online learning algorithms achieve sublinear regret, meaning their average mistake rate decreases over time.

**Stochastic Gradient Descent (SGD)** is the workhorse of online learning. In online SGD, we process one example at a time, computing the gradient of the loss on that example and taking a small step in the direction of steepest descent. The learning rate (step size) must be carefully tuned—it typically decreases over time to ensure convergence.

**Concept Drift** occurs when the underlying data distribution changes over time. Online learning algorithms must detect and adapt to drift. Strategies include monitoring prediction accuracy and triggering retraining, using sliding windows of recent data, or maintaining ensemble models with different "ages."

## How It Works

An online learning loop processes data sequentially:

1. Receive a data point $(x_t, y_t)$ (or just $x_t$ in prediction-only scenarios)
2. Make a prediction $\hat{y}_t$ using the current model
3. Receive the true label $y_t$ (in supervised learning)
4. Compute the loss $\ell(\hat{y}_t, y_t)$
5. Update the model parameters using the loss gradient
6. Discard the data point and move to the next

For classification, this might mean updating a linear classifier after each example. For regression, updating the coefficients. For neural networks, doing a single step of stochastic gradient descent on each minibatch.

The key advantage over batch learning is that online algorithms can adapt in real-time to changes. The downside is that they typically cannot leverage complex interactions between examples that batch algorithms can find through multiple passes over the data.

## Practical Applications

- **Recommendation Systems**: Updating user preference models as new interactions arrive
- **Financial Trading**: Adapting to changing market conditions in real-time
- **Network Intrusion Detection**: Detecting novel attack patterns as they emerge
- **IoT Sensor Processing**: Analyzing streams of sensor data where memory is limited
- **Advertising Bidding**: Adjusting bids based on real-time auction outcomes
- **Search Ranking**: Adapting to changes in query distributions and content
- **Chatbots and对话系统**: Updating responses based on ongoing conversations

## Examples

```python
# Online linear regression with SGD
import numpy as np

class OnlineLinearRegression:
    def __init__(self, n_features, learning_rate=0.01):
        self.weights = np.zeros(n_features)
        self.bias = 0.0
        self.lr = learning_rate
    
    def predict(self, x):
        return np.dot(x, self.weights) + self.bias
    
    def update(self, x, y, y_pred):
        # Compute gradients
        error = y - y_pred
        self.weights += self.lr * error * x
        self.bias += self.lr * error
        return error ** 2  # squared loss

# Simulate streaming data
np.random.seed(42)
n_features = 5
model = OnlineLinearRegression(n_features, learning_rate=0.01)

cumulative_loss = 0
n_updates = 1000

true_weights = np.array([1.5, -0.5, 2.0, 0.0, 1.0])
true_bias = 0.5

for t in range(n_updates):
    # Generate streaming data point
    x = np.random.randn(n_features)
    y = np.dot(x, true_weights) + true_bias + 0.1 * np.random.randn()
    
    # Predict
    y_pred = model.predict(x)
    
    # Update with true label (supervised)
    loss = model.update(x, y, y_pred)
    cumulative_loss += loss
    
    if t % 200 == 0:
        print(f"Step {t}: avg cumulative loss = {cumulative_loss / (t+1):.4f}")

print(f"\nLearned weights: {model.weights}")
print(f"True weights:    {true_weights}")
```

```python
# Using river library for online learning with concept drift detection
# (Concept drift example: accuracy drops when distribution shifts)

# from river import linear_model, drift, evaluate

# model = linear_model.LogisticRegression()
# detector = drift.ADWIN()  # Adaptive Windowing drift detector

# for xi, yi in data_stream:
#     y_pred = model.predict_one(xi)
#     model.learn_one(xi, yi)  # online update
#     detector.update(y_pred != yi)  # update with prediction error
#     if detector.change_detected:
#         print("Drift detected! Resetting model...")
#         model = linear_model.LogisticRegression()
```

## Related Concepts

- [[Machine Learning]] — the broader discipline
- [[Stochastic Gradient Descent]] — the optimization algorithm underlying online learning
- [[Batch Learning]] — learning from fixed datasets, the alternative paradigm
- [[Reinforcement Learning]] — also sequential decision making, often in online settings
- [[Concept Drift]] — changes in data distribution that online learning must handle
- [[Ensemble Methods]] — online ensembles can maintain diversity over time

## Further Reading

- "Online Learning and Online Convex Optimization" by Shai Shalev-Shwartz — comprehensive survey
- "Understanding Machine Learning: From Theory to Algorithms" — theoretical foundations
- River library documentation — practical Python toolkit for online learning

## Personal Notes

Online learning is fundamentally different from batch learning in that it trades off the ability to do complex optimization (multiple passes, second-order methods) for the ability to adapt continuously. In practice, for problems where data arrives in streams and the distribution might drift, online learning is essential. For static problems with abundant data, batch learning with careful validation is usually more effective. I've used online learning primarily for recommendation systems where user preferences shift over time.
