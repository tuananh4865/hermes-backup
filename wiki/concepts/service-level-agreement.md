---
title: "Service Level Agreement"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [sla, reliability, sre, contracts, availability]
---

# Service Level Agreement

## Overview

A Service Level Agreement (SLA) is a formal contract between a service provider and a customer that defines the level of service expected, including metrics, responsibilities, and remedies for failure to meet commitments. SLAs codify expectations in concrete, measurable terms—specific percentages of availability, maximum response times, minimum throughput rates—and establish consequences when these commitments are not honored. In modern cloud-native environments, SLAs guide architectural decisions, inform on-call practices, and determine acceptable risk levels for systems design.

SLAs exist at multiple levels: between a company and its end customers, between teams within an organization, and between an engineering team and the infrastructure or platform they depend on. The specific metrics and thresholds vary widely based on the service nature, business criticality, and cost of meeting commitments. A social media platform might tolerate 99.9% uptime (about 8.7 hours of downtime yearly), while financial trading systems require 99.999% (under 5 minutes downtime).

## Key Concepts

**Availability Metrics**: The most common SLA metric is availability, typically expressed as a percentage of successful requests or uptime within a measurement window. Common tiers include 99% ("two nines"), 99.9% ("three nines"), 99.99% ("four nines"), and 99.999% ("five nines"). Each tier represents an order of magnitude reduction in allowed downtime.

| Tier | Downtime/Year | Downtime/Month | Downtime/Week |
|------|---------------|----------------|---------------|
| 99% | 3.65 days | 7.31 hours | 1.68 hours |
| 99.9% | 8.76 hours | 43.83 min | 10.08 min |
| 99.99% | 52.6 min | 4.38 min | 1.01 min |
| 99.999% | 5.26 min | 26.30 sec | 6.05 sec |

**Latency Percentiles**: Customer-facing services rarely define SLA solely on availability. Latency commitments—often p50, p95, p99 response times—ensure experiences remain fast even during tail conditions. A service might commit to p99 latency under 200ms, meaning 99% of requests complete within that threshold.

**Error Budgets**: SLOs (Service Level Objectives) within an SLA define target levels; error budgets quantify how much deviation is acceptable. A service with a 99.9% SLO has a 0.1% error budget—about 43 minutes monthly. [[error-budget-policy]] uses this budget to guide operational decisions, pausing feature development when budget is depleted to focus on reliability.

**Remediation and Remedies**: When SLAs are breached, predetermined consequences apply. These range from service credits (financial compensation) to contract termination in severe cases. Cloud providers like AWS, Azure, and GCP publish SLA documents specifying credit calculations.

## How It Works

SLAs are typically defined during contract negotiation, informed by the service's operational capabilities and the customer's requirements. The process involves:

1. **Requirements gathering**: Understanding the customer's use case, criticality, and constraints
2. **Capability assessment**: Evaluating what the service can realistically achieve given current architecture and operational maturity
3. **Risk analysis**: Determining the cost of meeting vs. not meeting commitments
4. **Contract drafting**: Formalizing metrics, measurement methodology, and remedies
5. **Operationalization**: Implementing monitoring, alerting, and runbooks to maintain SLA compliance

```yaml
# Example SLA configuration in monitoring system
sla:
  service: payment-processing
  availability_target: 99.95%
  latency_targets:
    p50: < 50ms
    p95: < 200ms
    p99: < 500ms
  measurement_window: rolling_30d
  error_budget_policy: freeze-deployments-on-exhaustion
  remedies:
    breach_above_99.9:
      service_credit: 10%
    breach_above_99.5:
      service_credit: 25%
    breach_below_99.5:
      automatic_refund + escalation
```

Monitoring systems continuously measure actual performance against SLA commitments, alerting when metrics approach breach thresholds and triggering credit calculations when breaches occur.

## Practical Applications

**Cloud Platform SLAs**: Major cloud providers publish SLAs for individual services. AWS S3 offers 99.999999999% durability (eleven nines) for objects, but 99.9% availability for standard storage. These SLAs are often combined—a system using multiple services inherits each service's SLA characteristics.

**SaaS Products**: B2B SaaS vendors negotiate SLAs with enterprise customers, typically offering tiered commitments at different price points. Higher tiers offer tighter availability guarantees and faster support response times.

**Internal Platform Teams**: Internal teams providing platform services to product teams establish SLAs to set expectations and prioritize reliability work. These internal SLAs often reference external vendor SLAs as floor constraints.

**SLA Decomposition**: Large systems decompose customer-facing SLAs into internal SLAs for each component. A 99.99% overall availability target might require each microservice to achieve 99.995% availability given some redundancy assumption, and database tier to achieve 99.999% given criticality.

## Examples

Google Cloud's Cloud Spanner exemplifies sophisticated SLA thinking:

- 99.99% availability for regional instances (single region, multi-zone)
- 99.999% availability for global instances
- Availability measured as: percentage of successful requests divided by total requests, excluding scheduled maintenance

Credit calculation: "If Availability Percentage during a calendar month is less than the Availability Target, Customer is eligible for a Service Credit equal to 10% of the charges for the affected region for the calendar month."

## Related Concepts

- [[service-level-objectives]] - Internal targets that inform SLA commitments
- [[error-budget-policy]] - Operational policy derived from SLA/SLO boundaries
- [[on-call]] - Practices for maintaining SLA compliance around the clock
- [[incident-management]] - Processes for responding to SLA-threatening situations

## Further Reading

- [Google SRE Book - Service Level Objectives](https://sre.google/sre-book/part-IV/index.html) - Comprehensive guide to defining and measuring SLOs
- [AWS SLA Documentation](https://aws.amazon.com/legal/service-level-agreements/) - Cloud provider SLA examples
- [Stripe's reliability documentation](https://stripe.com/blog/region-availability) - Example of detailed SLA transparency

## Personal Notes

I've seen organizations treat SLAs as marketing numbers rather than operational commitments, leading to inevitable trust erosion when they're repeatedly missed. The more sustainable approach is to define SLOs conservatively—something you can actually achieve with headroom—then build error budget policies that protect against SLA breaches. When an SLA is truly business-critical, the organizational response to missing it should be as clear as the SLA itself.
