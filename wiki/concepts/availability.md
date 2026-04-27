---
title: Availability
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [availability, reliability, uptime, infrastructure]
---

## Overview

Availability is a fundamental metric in system design that measures the proportion of time a system or service remains operational and accessible to users. It is a critical aspect of [[reliability engineering]] and forms one of the pillars of the [[CAP theorem]], alongside consistency and partition tolerance. In practical terms, high availability means that users can access a service when they need it, without unexpected interruptions or downtime.

Availability is often expressed as a percentage of uptime over a given period, typically one year. A system that is available 99.9% of the time, for example, experiences only about 8.76 hours of downtime per year. The distinction between planned maintenance windows and unplanned outages is important: true availability metrics usually account only for unexpected failures, while planned downtime may be scheduled during low-traffic periods and negotiated with stakeholders.

In modern cloud-native and distributed architectures, achieving high availability is a design goal that influences decisions at every level, from infrastructure provisioning to application logic. Systems that serve critical functions, such as financial transaction processing, healthcare information systems, or communication platforms, are held to extremely stringent availability standards because failures can result in significant financial loss, reputational damage, or even risks to human safety.

## Measurement

The most common way to quantify availability is through uptime percentage, calculated as the ratio of actual uptime to total time in a measurement period. This simple formula becomes powerful when applied consistently across organizational reporting and service level agreements (SLAs).

The "nines" notation is the industry standard for expressing availability targets. Each additional nine represents an order-of-magnitude improvement in downtime tolerance:

- **99% (two nines)** allows approximately 3.65 days of downtime per year
- **99.9% (three nines)** allows about 8.76 hours of downtime per year
- **99.99% (four nines)** allows about 52.6 minutes of downtime per year
- **99.999% (five nines)** allows about 5.26 minutes of downtime per year

The effort required to move from four nines to five nines is substantial, often requiring architectural changes, automated monitoring, and self-healing systems. For most consumer-facing applications, three to four nines is a practical target. Mission-critical systems may demand five nines or higher.

Availability is closely tied to [[mean time to recovery]] (MTTR) and [[mean time between failures]] (MTBF). Together, these metrics provide a comprehensive picture of both how often failures occur and how quickly systems recover.

## Strategies

Achieving high availability requires deliberate architectural choices and operational practices. Several proven strategies form the foundation of highly available systems.

**Redundancy** involves deploying multiple instances of critical components so that the failure of any single instance does not cause system-wide outage. This can be implemented at the hardware level (multiple servers, power supplies, network paths) or at the application level (multiple service instances across different geographic regions). Redundant systems are designed to eliminate single points of failure.

**Failover** is the automated process of transferring operations from a failed component to a healthy standby. Active-passive failover maintains a secondary system that takes over when the primary fails. Active-active configurations run multiple replicas simultaneously, distributing load and providing immediate fault tolerance. Failover mechanisms rely on health checks, heartbeat signals, and orchestration software to detect failures and reroute traffic within seconds or milliseconds.

**Geographic distribution** places system components in multiple data centers or cloud regions to protect against localized disasters, network outages, or infrastructure failures. Traffic routing mechanisms such as [[DNS]]-based load balancing and anycast routing direct users to the nearest available endpoint.

**Monitoring and alerting** are essential for maintaining availability. Real-time visibility into system health enables rapid detection of degraded states before they escalate into full outages. Combined with automated remediation workflows, monitoring systems can trigger restarts, scaling events, or failover procedures without human intervention.

**Graceful degradation** allows a system to maintain partial functionality when some components fail, rather than experiencing complete outage. For example, a content delivery platform might serve cached content when origin servers are unreachable, preserving user experience even at reduced capability.

## Related

- [[Reliability Engineering]] - The discipline focused on building systems that consistently perform correctly
- [[Mean Time to Recovery]] - Metric measuring average recovery duration after failures
- [[Mean Time Between Failures]] - Metric measuring average interval between system failures
- [[Failover]] - The process of switching to a redundant system upon primary failure
- [[Redundancy]] - Duplication of critical components to ensure continued operation
- [[Service Level Agreement]] - Formal commitment defining availability and performance targets
- [[CAP Theorem]] - Theoretical framework describing trade-offs in distributed systems
