---
title: Metrics Collection
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [metrics-collection, monitoring, observability, metrics]
---

# Metrics Collection

## Overview

Metrics collection is the systematic process of gathering numerical measurements from software systems, infrastructure components, and applications to enable monitoring, alerting, and performance analysis. As systems scale in complexity, metrics collection provides the quantitative foundation for understanding behavior, diagnosing problems, and making data-driven decisions about capacity and optimization.

The practice of metrics collection transforms raw system signals into structured, queryable data points. Modern distributed systems generate enormous volumes of metrics—CPU utilization, memory consumption, request latencies, error rates, queue depths, and countless others. Without systematic collection, this data would be ephemeral, lost the moment it was generated. Metrics collection preserves this information in time-series databases, enabling historical analysis, trend identification, and correlation of events across system layers.

Effective metrics collection balances granularity against cost. Finer granularity (more frequent sampling, more metric dimensions) provides richer insight but increases storage requirements, network bandwidth, and processing overhead. Engineering teams must choose collection intervals, metric cardinalities, and retention policies that suit their operational needs and budget constraints.

## Key Concepts

Several concepts are fundamental to understanding how metrics collection works in practice.

**Metric Sources** generate the raw measurements. Applications can expose metrics explicitly through instrumentation libraries (Prometheus client, StatsD, Dropwizard Metrics). System-level sources include the operating system (CPU, memory, disk I/O), network devices, databases, load balancers, and cloud provider APIs. The diversity of sources requires collection agents that can query multiple interfaces.

**Collection Protocols** define how metrics travel from sources to storage. Prometheus uses a pull model where the monitoring server scrapes targets at regular intervals over HTTP. Other systems use push models where agents send metrics to aggregators (StatsD, Graphite protocol). Hybrid approaches exist where agents collect locally and expose for scraping, providing the benefits of both models.

**Metric Schema** structures the data. Common patterns include:
- **Counter**: A monotonically increasing value, reset only on restart (e.g., total requests)
- **Gauge**: A point-in-time measurement that can go up or down (e.g., current memory usage)
- **Histogram**: A distribution of values across configurable buckets (e.g., request latency buckets)
- **Summary**: Similar to histogram but with dynamically computed quantiles

**Label Dimensions** add metadata to metrics, enabling flexible querying and aggregation. A request latency histogram might include labels for endpoint, method, status code, and geographic region. This allows querying "p99 latency for GET requests to /api/users in US-East" without changing the metric schema.

**Scrape Intervals** determine how often metrics are collected. Shorter intervals (10 seconds) catch short-lived events but increase data volume. Longer intervals (60 seconds) may miss spikes but reduce costs. The choice depends on the metric type and how quickly changes matter.

## How It Works

A typical metrics collection pipeline involves several stages from generation to storage.

**Instrumentation** embeds metric generation into applications. Developers add explicit calls to metrics libraries at key points—recording request counts, measuring function duration, tracking resource usage. Many frameworks provide automatic instrumentation for common operations (HTTP requests, database queries), reducing the manual effort required.

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
)

active_connections = Gauge(
    'http_connections_active',
    'Number of active HTTP connections',
    ['state']  # 'reading', 'writing', 'idle'
)

# Instrument code
def handle_request(method, path, status, duration):
    http_requests_total.labels(method=method, endpoint=path, status_code=status).inc()
    http_request_duration_seconds.labels(method=method, endpoint=path).observe(duration)
```

**Collection Agents** retrieve or receive metrics from sources. Prometheus runs a server that scrapes configured targets via HTTP, parsing the exposition format (text or protobuf) and storing samples locally. Alternative architectures use agents deployed alongside applications that collect and forward metrics to central storage.

**Transport** moves metrics from collection points to storage. This might be direct (scraper writes to local TSDB) or through intermediate aggregation (agents send to gateway, gateway fans out to storage). High-throughput systems may use message queues (Kafka, RabbitMQ) to buffer and load-level metric flows.

**Storage** maintains metrics over time. Time-series databases are optimized for append-heavy workloads with time-range queries. Prometheus uses a custom TSDB with compression and down-sampling for long-term retention. Cloud options like CloudWatch, DataDog, and Grafana Cloud provide managed storage with automatic scaling.

**Querying and Alerting** consumes collected metrics. Query languages (PromQL, InfluxQL, MetricsQL) filter, aggregate, and transform metrics. Alerting rules evaluate queries continuously and fire when conditions are met. Dashboards visualize metrics through charts and graphs.

## Practical Applications

Metrics collection supports numerous operational workflows across the software lifecycle.

**Real-time Monitoring** displays current system state for operations teams. Dashboards showing request rates, error rates, and latency help engineers understand if systems are operating normally. Threshold-based alerts notify on-call teams when metrics exceed acceptable ranges.

**Capacity Planning** uses historical metrics to predict future resource needs. Analyzing growth trends in request volume, storage consumption, and connection counts informs procurement and provisioning decisions. Without metrics, capacity planning becomes guesswork.

**Anomaly Detection** establishes baselines and identifies deviations. Machine learning models trained on historical metrics can flag unusual patterns that rules-based alerts would miss—gradual drifts, correlated anomalies across metrics, or novel failure modes.

**Incident Post-Mortems** rely on metrics to reconstruct what happened during failures. Timeline analysis correlates metrics with deployments, configuration changes, and external events to identify root causes. Without metrics, post-mortems rely on memory and speculation.

**Cost Optimization** uses metrics to identify waste. Cloud spending analysis reveals underutilized instances, overprovisioned resources, and opportunities for reserved capacity. Application-level metrics expose opportunities for caching, optimization, or architectural improvements.

## Examples

A complete metrics collection setup might include:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

rule_files:
  - "alerts.yml"

scrape_configs:
  - job_name: 'web-app'
    static_configs:
      - targets: ['web-app:9090']
    metrics_path: '/metrics'
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        regex: '([^:]+):\d+'
        replacement: '${1}'
```

```yaml
# alerts.yml
groups:
  - name: web-app
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.99, 
            rate(http_request_duration_seconds_bucket[5m])
          ) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "p99 latency is {{ $value }}s"
```

## Related Concepts

Metrics collection connects to broader observability infrastructure:

- [[metrics]] — The numerical measurements being collected
- [[observability]] — The broader discipline metrics support
- [[alerting]] — Using collected metrics to trigger notifications
- [[dashboards]] — Visualizing collected metrics
- [[prometheus]] — Popular metrics collection and storage system
- [[time-series-database]] — Storage optimized for metrics
- [[instrumentation]] — Adding metric generation to applications
- [[slo]] — Service Level Objectives tracked via metrics

## Further Reading

- Prometheus Documentation
- "Time Series Databases" by Eric Lindred
- OWASP Monitoring Guidelines

## Personal Notes

Getting metrics collection right requires starting with the questions you need to answer, not the metrics you can collect. Early in a project, I instrumented everything I could think of, generating thousands of time series. When the incident happened, I couldn't find the relevant metrics in the noise. Now I start with the four golden signals—latency, traffic, errors, saturation—and add metrics only when I have a specific question they answer.
