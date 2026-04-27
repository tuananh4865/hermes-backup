---
title: "Service Level Agreements"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [sla, cloud-computing, devops, compliance, business]
---

# Service Level Agreements

## Overview

A Service Level Agreement (SLA) is a formal contract between a service provider and a client that defines the expected level of service, measurable metrics, and remedies for failing to meet those standards. SLAs are foundational documents in cloud computing, managed services, and enterprise IT outsourcing. They transform vague promises of "reliable service" into quantifiable commitments that can be monitored, audited, and enforced.

SLAs emerged as a best practice in the 1990s alongside the growth of IT outsourcing and telecommunications. Today they are ubiquitous—every major cloud provider (AWS, Azure, Google Cloud) publishes default SLAs for their services, and enterprise customers negotiate custom SLAs for mission-critical workloads. A well-crafted SLA protects both parties: the provider by setting clear boundaries, and the client by establishing accountability.

## Key Concepts

### Availability Metrics

The most common SLA metric is **availability**, expressed as a percentage of uptime over a billing period:

| Availability % | Downtime per Year | Downtime per Month |
|----------------|-------------------|-------------------|
| 99%            | 3.65 days         | 7.31 hours        |
| 99.9%          | 8.76 hours        | 43.83 minutes     |
| 99.95%         | 4.38 hours        | 21.92 minutes     |
| 99.99%         | 52.60 minutes     | 4.38 minutes      |

### Service Credits

When providers fail to meet SLA commitments, they typically compensate clients with **service credits**—deductions from future bills. Credits are usually proportional to downtime severity, often escalating for longer outages. For example, Azure offers credits starting at 10% for uptime below 99.9% and reaching 100% (free month) for uptime below 95%.

### Exclusions and Limitations

SLAs contain carve-outs defining what they don't cover. Common exclusions:
- Planned maintenance (with advance notice)
- Force majeure events (natural disasters, pandemics)
- Client-side issues (misconfiguration, traffic spikes from client apps)
- Third-party software or internet connectivity

## How It Works

SLAs operate through a continuous cycle of **definition → measurement → enforcement**.

**Definition** involves negotiating metrics like uptime, latency, throughput, and error rates. Each metric needs precise measurement methodology—who measures, how often, from what vantage points.

**Measurement** relies on monitoring systems. Modern SLAs use automated tooling that continuously pings services, measures response times, and logs incidents. Both parties typically retain measurement data for dispute resolution.

**Enforcement** triggers when measurements show a breach. The SLA specifies the credit formula, claim process, and dispute resolution mechanism. Some enterprise SLAs include financial penalties beyond credits.

```yaml
# Example SLA Document Structure
sla_version: "2.0"
effective_date: "2026-01-01"
services:
  - name: "API Gateway"
    uptime_target: "99.95%"
    latency_p99: "< 200ms"
    error_rate: "< 0.1%"
credits:
  99.9% - 99.95%: "10% monthly credit"
  99% - 99.9%: "25% monthly credit"
  < 99%: "100% monthly credit"
```

## Practical Applications

- **Cloud Infrastructure**: AWS, Azure, and GCP all publish SLAs for compute, storage, networking, and database services. Customers should calculate composite risk when relying on multiple services.
- **SaaS Applications**: CRM, HRIS, and communication platforms offer SLAs for application availability and data durability.
- **Managed Services**: MSPs provide SLAs covering network uptime, help desk response times, and security monitoring.
- **Telecommunications**: ISPs commit to bandwidth, latency, and outage resolution times.

## Examples

**Single-Service SLA Example**: A video streaming service signs an SLA with a CDN provider guaranteeing 99.9% uptime. When a fiber cut causes a 4-hour outage, the CDN provider issues a 25% service credit on that month's bill.

**Composite SLA Example**: A three-tier web application uses Azure Load Balancer (99.99% SLA), Azure Virtual Machines (99.9% SLA), and Azure SQL Database (99.99% SLA). The composite availability is approximately 99.88%, not 99.99%.

**Response-Time SLA Example**: A managed security provider commits to Level 1 support response within 15 minutes, Level 2 within 2 hours, and critical incident escalation within 30 minutes.

## Related Concepts

- [[cloud-computing]] — The primary domain where SLAs are most relevant
- [[devops]] — Practices that help organizations meet SLA commitments through automation
- [[compliance]] — Regulatory requirements often mandate SLA-like commitments
- [[azure-virtual-machines]] — Azure's compute SLA structure
- [[business-continuity]] — Planning for SLA breaches and disasters

## Further Reading

- [AWS SLA Documentation](https://aws.amazon.com/legal/service-level-agreements/)
- [Microsoft Azure SLA Overview](https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements)
- [Google Cloud Platform SLA](https://cloud.google.com/terms/sla/)

## Personal Notes

I always recommend reading the exclusions section of any SLA before signing. Many organizations discover too late that their "99.99% SLA" doesn't cover the scenarios that actually cause outages. For critical workloads, negotiate custom SLAs with penalties that actually hurt the provider—service credits alone rarelyincentivize investment in resilience. Calculate composite SLAs for multi-service architectures and ensure your business continuity plan accounts for the residual risk.
