---
title: CDN
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [cdn, performance, networking, infrastructure]
---

# CDN

## Overview

A Content Delivery Network (CDN) is a geographically distributed network of servers that work together to deliver web content to users with high performance and reliability. The primary purpose of a CDN is to reduce latency by serving content from servers that are physically closer to the end user, rather than forcing all requests to travel back to a single origin server located in one physical location.

CDNs have become a critical component of modern web infrastructure. They sit between the origin server (where the website's static assets and often dynamic content reside) and the end users who request that content. When a user visits a website that uses a CDN, the request is routed to the nearest CDN edge server rather than the origin, dramatically improving load times and user experience.

The concept behind CDNs is straightforward: instead of a user in Tokyo waiting 200+ milliseconds for a response from a server in New York, that user can often retrieve content from a CDN point of presence (PoP) in Japan or nearby, reducing response time to just a few milliseconds. This proximity advantage applies globally, making CDNs essential for any service with an international audience.

## How It Works

The CDN infrastructure consists of three main components working in coordination: the origin server, the CDN's core network, and edge servers distributed across multiple geographic locations.

**Origin Server**: This is the primary server where the original content resides. When content is first published or when it needs to be refreshed, the CDN fetches it from the origin server and distributes it to edge locations throughout its network.

**Points of Presence (PoPs)**: CDNs maintain hundreds of edge server locations worldwide. Each PoP contains multiple edge servers optimized for content delivery. When a CDN receives a request, its [[dns]] routing system directs the user to the optimal PoP based on factors such as geographic proximity, server load, and network conditions.

**Cache Mechanism**: When content is first requested from a CDN edge server, it is fetched from the origin and stored (cached) at that edge location. Subsequent requests for the same content are served directly from the cache, eliminating the need to round-trip to the origin server. CDNs use cache expiration policies (TTL - Time To Live) to determine how long content remains stored before being refreshed from the origin.

The request flow typically follows these steps: the user requests a resource, [[dns]] resolution identifies the optimal CDN edge server, the request is routed to that edge server, and if the content is cached, it is delivered immediately. If not cached, the CDN fetches it from the origin, delivers it to the user, and caches a copy for future requests.

## Benefits

**Reduced Latency**: The most significant benefit of a CDN is the dramatic reduction in content delivery latency. By serving content from edge servers geographically closer to users, round-trip times can be reduced from hundreds of milliseconds to single digits. This improvement directly translates to faster page load times, improved user engagement, and higher conversion rates for commercial websites.

**High Availability and Reliability**: CDNs provide built-in redundancy and fault tolerance. If one edge server fails, requests are automatically routed to the next nearest server. CDNs also implement [[load balancing]] across their networks to distribute traffic evenly and prevent any single server from becoming overwhelmed. This infrastructure resilience ensures content remains accessible even during traffic spikes or partial network failures.

**DDoS Protection**: CDNs are positioned to absorb and mitigate distributed denial-of-service attacks. Because user requests hit CDN edge servers rather than the origin directly, malicious traffic is dispersed across a large network. Most CDN providers offer dedicated [[ddos-protection]] services that can identify and filter attack traffic while allowing legitimate requests through.

**Origin Offload**: By caching content at the edge, CDNs significantly reduce the load on origin servers. This not only improves origin server performance but also reduces bandwidth costs, as a large percentage of content requests are served entirely from CDN infrastructure without ever reaching the origin.

**Improved Security**: Beyond DDoS protection, CDNs provide additional security layers including SSL/TLS termination, web application firewall capabilities, and bot management. They can also enforce consistent security policies across all content delivery points.

**Scalability**: CDN infrastructure can handle sudden traffic spikes without requiring proportional scaling of origin resources. During high-profile events or viral content moments, the distributed CDN network can absorb massive traffic increases that would overwhelm traditional server architectures.

## Related

- [[Load Balancing]] - Distributing traffic across multiple servers for optimal performance
- [[Caching]] - The mechanism of storing content for faster subsequent access
- [[dns]] - The domain name system that routes user requests to appropriate servers
- [[ddos-protection]] - Safeguards against distributed denial-of-service attacks
- [[Edge Computing]] - Processing data closer to end users, related to CDN edge capabilities
- [[web-performance]] - The broader discipline of optimizing website speed and responsiveness
- [[anycast]] - A network routing method CDNs use to direct traffic to the nearest server
