---
title: "Site Reliability Engineering"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [sre, devops, reliability, infrastructure, monitoring, incident-response, availability]
---

# Site Reliability Engineering

Site Reliability Engineering (SRE) is a discipline that applies software engineering principles to infrastructure and operations to create scalable, reliable systems. Originated at Google in 2003, SRE bridges the gap between development and operations by treating system reliability as a software problem rather than purely an infrastructure one. SRE teams are responsible for availability, latency, performance, efficiency, change management, monitoring, emergency response, and capacity planning.

## Core Principles

**Reliability as a Feature** — Just as we prioritize new features, reliability deserves explicit prioritization. Systems should be designed with failure in mind.

**Toil Reduction** — Manual operational work that can be automated should be automated. SREs aim to minimize repetitive manual tasks (toil) so teams can focus on engineering improvements.

**Error Budgets** — Accept that 100% reliability is impossible and counterproductive. Instead, define reliability targets (e.g., 99.9%) and treat the remaining 0.1% as an error budget to spend on new features.

**Service Level Objectives (SLOs)** — Specific, measurable targets for service reliability. SLOs define what "reliable enough" means for each service.

**Service Level Indicators (SLIs)** — Metrics that measure reliability in real-time: request latency, error rate, throughput, availability percentage.

## The SRE Toolbelt

### Monitoring and Observability

```yaml
# Example: Prometheus alerting rules for SLO tracking
groups:
  - name: web-backend-slo
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m])) 
          / 
          sum(rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate exceeds 1% SLO threshold"
```

### Incident Management

SRE uses structured incident response:
1. **Detection** — Automated alerts from monitoring
2. **Triage** — Classify severity and impact
3. **Mitigation** — Immediate actions to reduce impact
4. **Resolution** — Fix the root cause
5. **Postmortem** — blameless analysis to prevent recurrence

### Change Management

- **Progressive Rollouts** — Deploy to small percentage first
- **Canary Deployments** — Test with real traffic before full rollout
- **Rollback Procedures** — Ability to quickly revert harmful changes
- **Automation** — Reduce human error through automated deployments

## Practical Applications

SRE practices manifest in various operational scenarios:

**Capacity Planning** — Predicting resource needs based on traffic growth and seasonal patterns. Right-sizing infrastructure to balance cost and performance.

**Release Engineering** — Ensuring safe software delivery through automated testing, staging, and deployment pipelines.

**Database Reliability** — Managing database scaling, replication, and failover to maintain data availability.

**Chaos Engineering** — Intentionally introducing failures (via tools like Chaos Monkey) to test system resilience before real outages occur.

## How It Works

SRE implements a feedback loop:

1. **Define SLOs** — What reliability level do users expect?
2. **Measure SLIs** — Collect metrics against SLOs
3. **Analyze Error Budgets** — How much unreliability can we "spend"?
4. **Improve Systems** — Engineering work to reduce errors
5. **Automate Toil** — Remove manual work through tooling
6. **Repeat** — Continuous improvement cycle

## Related Concepts

- [[reliability-engineering]] — Broader discipline of building reliable systems
- [[monitoring]] — System observation and alerting
- [[incident-response]] — Handling production emergencies
- [[SRE]] — This page's abbreviation
- [[canary-deployment]] — Safe deployment strategy
- [[alerting]] — Notification systems for anomalies
- [[logging]] — Event recording for debugging

## Further Reading

- Site Reliability Engineering (O'Reilly) — Google's definitive SRE book
- Google SRE Workbook
- The Site Reliability Engineering Community

## Personal Notes

The error budget concept was transformative for me—it's a pragmatic view that chasing 100% uptime is wasteful. Instead, accept a small failure budget and invest the saved effort in features. The "blameless postmortem" culture also stands out as genuinely healthy for engineering organizations.
