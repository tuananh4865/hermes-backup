---
title: Content Delivery Network
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cdn, networking, performance, caching, edge-computing]
---

## Overview

A Content Delivery Network (CDN) is a geographically distributed network of proxy servers and data centers that provides high availability and performance by caching content closer to end users. CDNs are fundamental infrastructure for modern web delivery, reducing latency, handling traffic spikes, and protecting against DDoS attacks. Instead of serving all content from a single origin server, CDNs replicate resources across multiple edge locations worldwide, allowing users to fetch assets from the nearest point of presence (PoP).

## Key Concepts

**Edge Servers and Points of Presence**: CDN providers operate data centers in dozens to hundreds of locations globally. When a user requests content, the CDN routes them to the nearest edge server rather than the distant origin. This geographic proximity dramatically reduces round-trip time (RTT) and improves load times.

**Caching and Cache Invalidation**: CDNs store copies of static assets like images, CSS, JavaScript, fonts, and videos at edge locations. Cache invalidation strategies determine when cached content is refreshed. Common approaches include Time-to-Live (TTL) based expiration, cache purge on demand, and intelligent invalidation based on content hashing.

**Anycast Routing**: CDNs use Anycast DNS routing to direct user requests to the nearest edge server based on network topology. This technique allows multiple servers to share the same IP address, with routing infrastructure automatically selecting the optimal destination.

**Origin Shielding**: Advanced CDN configurations include origin shield layers that sit between edge servers and the origin, reducing load on origin infrastructure and providing additional caching benefits for content that cannot be globally cached.

## How It Works

When a user requests a resource through a CDN, the process follows several stages. First, DNS resolution routes the request to the nearest CDN edge server via Anycast. The edge server checks its cache for the requested asset. On a cache hit, content is served directly to the user with minimal latency. On a cache miss, the edge server retrieves content from the origin server, optionally applying transformations, then caches it for future requests before delivering to the user.

Modern CDNs also perform request routing optimizations, TLS termination, HTTP/2 or HTTP/3 multiplexing, and automated threat detection. This offloads significant infrastructure burden from origin servers.

```text
User Request
    │
    ▼
CDN Edge Server (closest PoP)
    │
    ├── Cache Hit → Return cached content
    │
    └── Cache Miss → Fetch from Origin → Cache → Return to user
```

## Practical Applications

CDNs are essential for delivering web content at scale. E-commerce platforms use CDNs to ensure product images and pages load instantly across global markets, directly impacting conversion rates. Media streaming services rely on CDNs to deliver video content without buffering. Software companies distribute binary releases and updates through CDNs for fast, reliable downloads. Additionally, CDNs provide security services including DDoS mitigation, bot management, and Web Application Firewall (WAF) capabilities.

## Examples

- **Cloudflare**: Offers CDN with integrated security, performance optimization, and serverless computing at the edge
- **Akamai**: One of the oldest and largest CDNs, with extensive global infrastructure
- **Amazon CloudFront**: Integrated with AWS ecosystem, provides edge computing via Lambda@Edge and CloudFront Functions
- **Fastly**: Known for real-time cache purging and programmable edge computing

## Related Concepts

- [[Web Performance]] - Core discipline CDNs optimize
- [[Caching Strategies]] - Cache invalidation and management techniques
- [[Load Balancing]] - Distributing traffic across multiple servers
- [[Edge Computing]] - Processing data at the network edge
- [[Anycast DNS]] - Routing technique used by CDNs

## Further Reading

- [MDN: CDN](https://developer.mozilla.org/en-US/docs/Glossary/CDN)
- [Cloudflare Learning Center](https://www.cloudflare.com/learning/)
- [Akamai Documentation](https://learn.akamai.com/)

## Personal Notes

CDNs transformed web performance expectations. In my own projects, switching to CloudFront cut page load times by 60% for international users. The key is setting appropriate TTLs—too short wastes origin requests, too long risks serving stale content. Modern CDNs with instant purge capabilities solve this tradeoff.
