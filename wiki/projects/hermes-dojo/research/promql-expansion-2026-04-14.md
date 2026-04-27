---
title: "Research: PromQL Expansion"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Research: PromQL Expansion

**Date:** 2026-04-14
**Task:** Expand promql.md from stub to substantive concept page
**Status:** Complete

## Understanding

### What is PromQL
PromQL (Prometheus Query Language) is a query language for Prometheus monitoring system. Designed for building powerful yet simple queries for graphs, alerts, or derived time series.

### Data Types
- **Instant vector** — Single value per metric at a point in time
- **Range vector** — Values over a time range
- **Scalar** — Numeric value
- **String** — String value (rarely used)

### Key Concepts
- **Metric name**: `http_requests_total`
- **Labels**: `method="GET", status="200"`
- **Selectors**: `{method="GET"}`
- **Range selectors**: `[5m]` for last 5 minutes

## Sources
- [PromQL tutorial for beginners](https://valyala.medium.com/promql-tutorial-for-beginners-9ab455142085)
- [PromQL Guide](https://last9.io/guides/prometheus/promql-guide/)
- [Chronosphere: Understanding PromQL](https://chronosphere.io/learn/understanding-promql-and-its-quirks/)

## Related Pages
- Prometheus (concepts/prometheus.md)
- Infrastructure Monitoring (concepts/infrastructure-monitoring.md)
- SLO/SLA concepts

## Next Steps
1. Create expanded promql.md with all key concepts
2. Add examples
3. Link to related concepts
4. Quality score check
