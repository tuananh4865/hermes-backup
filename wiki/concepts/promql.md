---
title: PromQL
description: Prometheus Query Language - query time-series metrics for monitoring, alerting, and dashboards
tags: [prometheus, monitoring, promql, sre, time-series]
created: 2026-04-13
updated: 2026-04-14
type: concept
quality_score: 7.2
---

# PromQL (Prometheus Query Language)

PromQL is the query language for [Prometheus](https://prometheus.io). It lets you select and aggregate [time-series data](concepts/time-series-databases.md) in real-time.

## Why PromQL

PromQL is designed for monitoring:
- **Simple to start** — Basic queries are one line
- **Powerful for alerting** — Supports aggregations and predictions
- **Built into Prometheus** — Native, no extra setup

If you use Prometheus, you write PromQL.

## Core Concepts

### Metric Name + Labels

```
http_requests_total{method="GET", status="200"}
│            │          │                │
│            │          └── Labels (key=value pairs)
│            └── Metric name
└── Timeseries identifier
```

### Instant Vector

Single value per metric at one point in time. Most common.

```
# All HTTP requests
http_requests_total

# Only GET requests
http_requests_total{method="GET"}

# GET requests with 2xx status
http_requests_total{method="GET", status=~"2.."}
```

### Range Vector

Values over a time window. Used for rate calculations.

```
# Last 5 minutes of requests
http_requests_total[5m]
```

### Selectors

| Selector | Meaning |
|----------|---------|
| `=` | Exact match |
| `!=` | Not equal |
| `=~` | Regex match |
| `!~` | Regex not match |

```
# Not GET requests
{method!="GET"}

# 4xx errors
{status=~"4.."}
```

## Common Queries

### Rates (Most Important)

```promql
# Requests per second (rate over 5 minutes)
rate(http_requests_total[5m])

# Requests per minute
rate(http_requests_total[1m]) * 60
```

### Aggregations

```promql
# Total requests by method
sum by(method) (http_requests_total)

# Average response time
avg by(service) (http_request_duration_seconds)

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

### Combining

```promql
# Error rate (4xx + 5xx) as percentage
100 * sum by(status) (rate(http_requests_total{status=~"4.."}[5m]))
  /
sum(rate(http_requests_total[5m]))
```

## Offset Modifier

Get value from the past:

```promql
# Compare to yesterday
rate(http_requests_total[5m]) / rate(http_requests_total[5m] offset 1d)

# This time yesterday
http_requests_total offset 1d
```

## Key Operators

| Operator | Use |
|----------|-----|
| `rate()` | Per-second rate of change |
| `increase()` | Total increase over time |
| `irate()` | Instantaneous rate (for spikes) |
| `histogram_quantile()` | Percentile from histogram |
| `predict_linear()` | Predict future values |

## Common Patterns

### Service Latency

```promql
# P50 latency
histogram_quantile(0.50, sum by(le) (rate(http_request_duration_seconds_bucket[5m])))

# P99 latency  
histogram_quantile(0.99, sum by(le) (rate(http_request_duration_seconds_bucket[5m])))
```

### Error Rate

```promql
# 5xx errors per second
rate(http_requests_total{status=~"5.."}[5m])

# Error percentage
100 * sum(rate(http_requests_total{status=~"5.."}[5m]))
  /
sum(rate(http_requests_total[5m]))
```

### Saturation

```promql
# CPU usage percentage
100 * (1 - avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])))

# Memory usage
100 * (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)
```

## PromQL vs SQL

| SQL | PromQL |
|-----|--------|
| `SELECT *` | `metric_name` |
| `WHERE` | `{labels}` |
| `GROUP BY` | `sum by(label)` |
| `time BETWEEN` | `[duration]` |

## Common Mistakes

### 1. Forgetting rate()

```promql
# WRONG - raw counter keeps growing
http_requests_total

# RIGHT - rate gives per-second
rate(http_requests_total[5m])
```

### 2. Short Window for Low Traffic

```promql
# WRONG - too short for sparse metrics
rate(http_requests_total[1m])

# RIGHT - use longer window
rate(http_requests_total[15m])
```

### 3. Missing Cardinality Awareness

```promql
# High cardinality warning - every unique value becomes a series
{cardinality="high"}
```

## Tools

- **Prometheus UI** — Built-in at `:9090/graph`
- **Grafana** — Dashboards use PromQL
- **PromLens** — PromQL editor with explanations
- **instant-Query** — Chrome extension

## Related Concepts

- [Prometheus](concepts/prometheus.md) — The monitoring system
- [Infrastructure Monitoring](concepts/infrastructure-monitoring.md) — The practice
- [SLO/SLA](concepts/slo.md) — What PromQL often measures
- [Time Series Databases](concepts/time-series-databases.md) — Data storage

## References

- [Prometheus Docs: PromQL](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [PromQL Tutorial for Beginners](https://valyala.medium.com/promql-tutorial-for-beginners-9ab455142085)
- [Chronosphere: Understanding PromQL](https://chronosphere.io/learn/understanding-promql-and-its-quirks/)
