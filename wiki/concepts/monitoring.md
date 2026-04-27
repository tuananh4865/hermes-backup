---
title: Monitoring
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [monitoring, observability, devops, reliability]
---

## Overview

Monitoring is the practice of continuously observing a system's health, performance, and behavior to ensure it operates as expected. It involves collecting data from various sources such as applications, infrastructure, and networks, then analyzing that data to detect issues, track trends, and inform operational decisions. Effective monitoring is foundational to maintaining reliable services and enabling rapid response to problems before they impact users.

In modern software engineering, monitoring is a critical component of [[observability]] and [[DevOps]] workflows. It moves beyond simple uptime checks to provide deep insight into how systems behave under different conditions. The goal is not just to know when something breaks, but to understand the state of the system at any given time and to catch anomalies early. This proactive approach reduces downtime, improves user experience, and supports data-driven decision making for capacity planning and feature development.

Monitoring serves multiple audiences within an organization. Engineers use it to debug issues and understand system behavior. Site Reliability Engineers rely on it to maintain [[reliability]] targets and manage incident response. Product managers track key performance indicators to assess how well the system meets user needs. Executive stakeholders may view business-level metrics to evaluate overall health and growth. Each audience requires different views and aggregations of the same underlying data.

## Metrics

Metrics are the quantitative measurements collected during monitoring activities. They represent specific aspects of system behavior such as response times, error rates, throughput, CPU utilization, memory consumption, and custom business indicators. Metrics are typically aggregated over time intervals and stored in time-series databases, allowing historical analysis and trend identification.

A well-designed metrics strategy distinguishes between different types of metrics. Counter metrics track the total number of occurrences for events like page requests or database queries. Gauge metrics capture current values at a point in time, such as the number of active connections or current memory usage. Histogram metrics distribute values into buckets to analyze distributions, useful for understanding percentile performance beyond simple averages.

Organizations typically build metrics pipelines to collect, process, and store telemetry data at scale. These pipelines ingest metrics from multiple sources, normalize them into a common format, and route them to storage and visualization systems. Popular open-source solutions for metrics pipelines include Prometheus for collection and alerting, Graphite for time-series storage, and Grafana for visualization. Cloud providers also offer managed monitoring services that handle ingestion, storage, and querying without requiring infrastructure management.

## Alerting

Alerting is the process of notifying appropriate personnel when monitored metrics exceed defined thresholds or when specific conditions are met. Effective alerting transforms raw monitoring data into actionable information that drives response to issues. An alert typically includes context about what triggered it, the severity level, and links to relevant dashboards or runbooks for investigation.

Alerting systems work by evaluating rules against incoming metrics data. When a rule condition becomes true, such as error rate exceeding five percent for five consecutive minutes, the system generates an alert. This alert then routes to the appropriate notification channel, whether that is email, instant messaging, paging systems, or ticketing workflows. Sophisticated alerting setups include deduplication logic to prevent alert fatigue from repeated notifications for the same ongoing issue.

Designing good alerts requires balancing sensitivity and specificity. Alerts that fire too easily create noise and erode trust in the monitoring system, while alerts that are too conservative may miss genuine incidents. Best practices recommend alerting on symptoms rather than causes, keeping alert definitions simple and testable, and regularly reviewing alert logic to ensure relevance as systems evolve. This discipline supports healthy on-call practices and reduces burnout among engineering teams.

## Related

- [[Observability]] - The broader discipline of understanding system state from external outputs
- [[DevOps]] - The cultural and technical practices that integrate development and operations
- [[Reliability]] - The quality attribute referring to consistent performance and uptime
- [[Metrics Pipeline]] - Systems that collect and process telemetry data at scale
- [[Alerting]] - The process of notifying personnel when issues are detected
- [[SLO]] - Service Level Objectives that define targets for reliability metrics
- [[Incident Response]] - The procedures for managing and resolving production issues
