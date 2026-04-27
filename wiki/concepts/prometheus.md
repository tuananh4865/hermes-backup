---
title: "Prometheus"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [monitoring, observability, time-series, metrics, cncf]
---

# Prometheus

## Overview

Prometheus is an open-source systems monitoring and alerting toolkit originally developed at SoundCloud in 2012, and later donated to the Cloud Native Computing Foundation (CNCF) where it became a graduated project. Prometheus specializes in collecting, storing, and querying metrics—numerical measurements that change over time—making it the backbone of monitoring for countless Kubernetes deployments, microservices architectures, and infrastructure stacks worldwide.

Unlike traditional monitoring systems that rely on push-based collection (where agents push metrics to a central server), Prometheus primarily uses a pull-based model. The Prometheus server scrapes metrics from configured targets at regular intervals over HTTP. This architecture offers several advantages: it requires no agent installation on target systems, makes it easy to identify misconfigured targets (a target that stops serving metrics becomes immediately obvious), and naturally handles temporary or ephemeral targets like containerized services.

Prometheus stores all metrics as time series—timestamped value pairs organized by metric name and optional key-value labels called dimensions. This multidimensional data model enables powerful querying through PromQL (Prometheus Query Language), allowing you to slice, dice, and aggregate metrics along any dimension at query time.

## Key Concepts

**Metrics and Labels**: A metric in Prometheus consists of a metric name, a set of labels (key-value pairs), and a series of timestamped values. The metric name describes what is being measured (e.g., `http_requests_total`), while labels provide context (e.g., `method="GET"`, `status="200"`, `endpoint="/api/users"`). This combination creates millions of possible metric series from a single metric definition.

**Metric Types**: Prometheus supports four core metric types:

- **Counter**: A cumulative value that only increases (e.g., total requests, total errors). Use counters for things that never decrease.
- **Gauge**: A value that can go up or down (e.g., current memory usage, temperature, queue depth). Gauges are for point-in-time measurements.
- **Histogram**: Samples observations and counts them in configurable buckets (e.g., request durations). Useful for calculating percentiles and averages.
- **Summary**: Similar to histograms but calculates percentiles server-side rather than relying on bucket configurations.

**PromQL**: The Prometheus Query Language is a flexible expression language for selecting and aggregating time-series data. PromQL supports arithmetic operations, functions (rate, increase, histogram_quantile), aggregation operators (sum, avg, min, max), and powerful filtering by label matchers.

## How It Works

Prometheus's architecture consists of several integrated components:

1. **Scraping**: The Prometheus server maintains a scrape pool with targets. For each target, it periodically makes an HTTP GET request to a `/metrics` endpoint. Targets can be static (manually configured) or dynamically discovered through service discovery mechanisms that integrate with Kubernetes, EC2, Azure, GCE, or custom systems.

2. **Storage**: Prometheus uses a custom time-series database with an on-disk storage engine optimized for storing high-volume metric data. Data is stored in 2-hour chunks, with each chunk being a separate file. This design enables efficient querying and automatic cleanup of old data through retention policies.

3. **Querying**: The query engine processes PromQL queries and returns results. Queries can be issued through the built-in web UI, the expression browser, or the HTTP API for integration with dashboards like [[Grafana]].

4. **Alerting**: AlertManager handles alert routing, grouping, and notification. Rules defined in Prometheus evaluate expressions continuously; when conditions are met, alerts fire and send to AlertManager, which then routes notifications through email, Slack, PagerDuty, or custom webhooks.

```yaml
# Example Prometheus scrape configuration
scrape_configs:
  - job_name: 'web-server'
    static_configs:
      - targets: ['web01:9100', 'web02:9100', 'web03:9100']
    metrics_path: /metrics
    scrape_interval: 15s

  - job_name: 'kubernetes-apiservers'
    kubernetes_sd_configs:
      - role: endpoints
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
```

## Practical Applications

Prometheus excels at monitoring infrastructure and application layers in dynamic, cloud-native environments.

**Kubernetes Monitoring**: In Kubernetes deployments, Prometheus operator and kube-prometheus-stack automate service discovery and metric collection across all cluster components—from kubelet and etcd to custom application pods. Metrics like `kube_pod_container_resource_limits` and `container_cpu_usage_seconds_total` provide deep visibility into resource consumption.

**Application Performance Monitoring**: Instrumenting applications with Prometheus client libraries exposes custom business metrics. A web application might expose `order_total_usd`, `active_users_gauge`, and `payment_processing_seconds` alongside infrastructure metrics, enabling correlation between business outcomes and system performance.

**SLO/SLI Monitoring**: Service Level Objectives are trackable through metrics like `node_filesystem_avail_bytes` for storage availability or `http_request_duration_seconds` for latency. Histograms enable direct calculation of error budgets and burn rates.

## Examples

A Go application exposing Prometheus metrics:

```go
import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promhttp"
    "net/http"
)

var (
    httpRequestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total",
            Help: "Total number of HTTP requests",
        },
        []string{"method", "status"},
    )
    httpRequestDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request latency",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method"},
    )
)

func init() {
    prometheus.MustRegister(httpRequestsTotal, httpRequestDuration)
}

func handler(w http.ResponseWriter, r *http.Request) {
    // ... business logic ...
    httpRequestsTotal.WithLabelValues(r.Method, "200").Inc()
}
```

## Related Concepts

- [[Grafana]] - Visualization layer commonly paired with Prometheus
- [[Alertmanager]] - Handles Prometheus alert routing and notifications
- [[PromQL]] - Prometheus Query Language for metric analysis
- [[Time Series Database]] - The storage paradigm Prometheus uses
- [[Observability]] - The discipline Prometheus enables
- [[Kubernetes]] - Container orchestration often monitored with Prometheus
- [[OpenTelemetry]] - Emerging standard for observability instrumentation

## Further Reading

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Prometheus Operator](https://prometheus-operator.dev/) - Kubernetes-native management
- [Prometheus client libraries](https://prometheus.io/docs/instrumenting/clientlibs/) - Multi-language support
- [Awesome Prometheus Alerts](https://awesome-prometheus-alerts.io/) - Community alert rule collection

## Personal Notes

Start with `rate()` and `increase()` functions rather than raw values—they handle rate calculations correctly even with scrapes that miss targets. The histogram_quantile function is powerful but requires careful bucket configuration; wider buckets at the tail end (e.g., 5s, 10s, 30s, 60s) give better resolution for high-latency events. Always set appropriate recording rules for frequently-queried complex expressions to reduce query load. For Kubernetes, the Prometheus Operator with CRDs makes configuration far more declarative than static YAML files.
