---
title: "Global Server Load Balancing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags:
  - infrastructure
  - networking
  - dns
  - high-availability
  - distributed-systems
---

## Overview

Global Server Load Balancing (GSLB) refers to the practice of distributing traffic across multiple geographic locations or data centers at a worldwide scale. Unlike local load balancing, which operates within a single region or data center, GSLB extends traffic management across diverse geographical boundaries, directing users to the closest or most available server based on real-time conditions. This capability is fundamental to delivering low-latency experiences in globally distributed applications, ensuring high availability during regional outages, and optimizing infrastructure costs by intelligently routing traffic away from overloaded or failing locations.

GSLB systems operate at a higher strategic level than traditional load balancers, making decisions about which data center should serve a particular user request before the connection is fully established. This DNS-based or anycast-based routing allows the system to influence the very first packet of a connection, shaping the entire subsequent interaction. The technology has become essential for enterprises operating digital services at global scale, from major e-commerce platforms to SaaS applications serving international customers.

## Key Concepts

**GeoDNS** forms the most basic layer of GSLB, returning different DNS responses based on the geographic origin of the query. This allows directing users in Europe to European data centers, users in Asia to Asian data centers, and so forth. However, pure GeoDNS cannot adapt to real-time conditions—it will continue directing traffic to a failing data center as long as DNS caches still hold the old records.

**Health checking** provides the feedback mechanism that enables GSLB to respond to failures. Each data center runs health monitors that continuously verify the availability and performance of local servers, applications, and network paths. When a health check fails, the GSLB system removes that location from its response pool, redirecting traffic to healthy alternatives. Modern GSLB implementations support application-level health checks that verify not just server availability but also that the application is actually responding correctly.

**Latency-based routing** represents a more sophisticated approach, using ongoing measurements or static latency estimates to route users to the fastest available data center. This matters because geographic proximity doesn't always guarantee the best performance—network routing anomalies, undersea cable constraints, or peering agreements can make a physically distant data center actually provide better response times.

**Anycast routing** offers an alternative to DNS-based GSLB, where the same IP address is announced from multiple locations and BGP routing naturally directs users to the nearest announcement. This approach provides extremely fast failover (seconds rather than DNS TTL minutes) but offers less control over traffic distribution.

## How It Works

The typical GSLB implementation begins with DNS resolution. When a user attempts to connect to `app.example.com`, their resolver queries the authoritative DNS server, which is actually a GSLB controller. This controller examines the source IP of the incoming query (after applying EDNS client subnet when available) to estimate the user's location. It then cross-references this location with current health and load data from its monitors.

Based on configured policies—which might prioritize lowest latency, highest availability, or weighted distribution—the GSLB returns the IP address of the "best" data center for this user. The user's resolver caches this response according to the TTL set by the GSLB, meaning subsequent requests within the TTL window go directly to the selected data center.

Real-time failover operates through shortened TTLs during degraded conditions. When a health check detects failure, the GSLB immediately begins returning addresses only for healthy locations, and it may also coordinate with CDN providers or other upstream systems to accelerate propagation. Some advanced GSLB platforms support "load shedding" mode, where they deliberately route traffic away from overloaded data centers even when those centers are technically healthy.

```yaml
# Example GSLB configuration snippet (conceptual)
datacenters:
  - name: us-east-1
    region: north-america
    weight: 100
    healthcheck:
      endpoint: /health
      interval: 10s
      timeout: 3s
      threshold: 3
  - name: eu-west-1
    region: europe
    weight: 100
    healthcheck:
      endpoint: /health
      interval: 10s
      timeout: 3s
      threshold: 3
  - name: ap-southeast-1
    region: asia-pacific
    weight: 50  # Lower weight due to fewer servers
    healthcheck:
      endpoint: /health
      interval: 10s
      timeout: 3s
      threshold: 3

rules:
  - name: geo-routing
    type: geographic
    mappings:
      north-america: us-east-1
      europe: eu-west-1
      asia-pacific: ap-southeast-1
  - name: failover
    type: health-based
    fallback:
      - us-east-1
      - eu-west-1
```

## Practical Applications

GSLB is essential for any organization running multi-region infrastructure. **Disaster recovery** represents a primary use case—when an entire data center fails due to power loss, network partition, or natural disaster, GSLB redirects traffic to surviving locations within seconds to minutes, depending on DNS TTL configuration. This automatic failover happens without human intervention, which is critical when failures occur outside business hours.

**Global content delivery** relies heavily on GSLB principles, though often implemented through CDN providers rather than custom infrastructure. When a user requests a video or downloads software, GSLB directs them to the edge server closest to their location, minimizing latency and reducing backbone traffic costs.

**Live sporting events and product launches** create massive, sudden traffic spikes concentrated in specific geographic regions. GSLB can direct this traffic away from regions with overwhelmed infrastructure, distributing the load across the global footprint and preventing any single location from becoming the bottleneck.

**Multi-cloud and hybrid architectures** use GSLB to coordinate traffic between on-premises data centers and multiple cloud providers, selecting the best destination based on cost, capacity, and performance at any given moment.

## Examples

A practical GSLB scenario for a financial trading platform might involve three data centers in New York, London, and Tokyo. During Asian market hours, GSLB directs most traffic to Tokyo with some to London for backup. When New York market hours begin, traffic shifts to New York as the primary, with London handling overflow. Health checks continuously verify that trading engines in each location are responsive—if Tokyo's matching engine becomes slow or unresponsive, GSLB immediately routes Tokyo users to London until Tokyo recovers.

An e-commerce company during Black Friday might configure GSLB with lower weights for smaller data centers that have limited capacity, reserving them only for local failover while directing most traffic to large, well-provisioned facilities. If one large facility approaches capacity limits, GSLB can shift traffic to less-utilized locations before performance degrades.

## Related Concepts

- [[Load Balancing]] - Local traffic distribution within a data center
- [[DNS]] - The naming system that GSLB operates through
- [[BGP]] - The routing protocol underlying anycast GSLB
- [[Content Delivery Network]] - Cached content distribution at the edge
- [[High Availability]] - Redundancy patterns for fault tolerance
- [[Anycast]] - Routing strategy where multiple nodes share one IP

## Further Reading

- "Global Server Load Balancing" by Klaus B. an authoritative technical deep-dive
- F5 GSLB/DNS architecture documentation
- AWS Route 53 health checking and routing policies documentation
- Cloudflare Load Balancing documentation on geo-routing

## Personal Notes

GSLB is one of those infrastructure pieces that only becomes visible when it fails—a misconfigured GeoDNS policy can silently route your entire European user base to US servers, tanking performance and going unnoticed until someone files a support ticket. TTL management is a constant balancing act: high TTLs reduce DNS query load but slow failover, while low TTLs enable fast failover but increase resolver stress and costs. I've learned to use notably shorter TTLs during high-risk periods (planned maintenance windows, severe weather in data center regions) and return to higher TTLs during stable operation.
