---
title: "Edge Caching"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [networking, cdn, performance, distributed-systems, web-performance]
---

# Edge Caching

## Overview

Edge caching is a content delivery technique that stores copies of web content, media files, API responses, and other digital assets at geographically distributed servers positioned close to end users. By caching content "at the edge" of the network—meaning at points-of-presence (PoPs) that are physically nearer to users than origin servers—edge caching dramatically reduces latency, decreases bandwidth costs, and improves overall user experience for web applications and services.

The fundamental principle is simple: instead of every user request traveling across the internet to a centralized data center, content is replicated to dozens, hundreds, or even thousands of edge locations worldwide. When a user requests cached content, the nearest edge server can serve it directly, often in milliseconds compared to hundreds of milliseconds or seconds for a round-trip to a distant origin. This architecture forms the backbone of modern Content Delivery Networks (CDNs) like Cloudflare, Akamai, Amazon CloudFront, and Fastly.

Edge caching becomes particularly important for static assets like images, videos, stylesheets, JavaScript bundles, and fonts that don't change frequently. However, modern edge platforms have expanded to cache dynamic API responses, authenticated content, and even executable code that runs at the edge. The key challenge is maintaining cache consistency—ensuring users receive fresh content when the origin updates—while still benefiting from high cache hit rates.

## Key Concepts

**Cache Hit** occurs when an edge server has a valid copy of requested content and can serve it directly without contacting the origin. Cache hit ratio, the percentage of requests served from cache, directly impacts performance and origin load. High cache hit rates (80-95%+) indicate effective caching strategy.

**Cache Miss** happens when requested content is not available at the edge server, requiring the request to proxy back to the origin server. Cache misses introduce latency and increase origin load. Strategies like cache prefetching, stale-while-revalidate patterns, and cache warming attempt to minimize misses.

**Time-to-Live (TTL)** defines how long content should be cached before considered stale. TTL is typically set via HTTP Cache-Control headers. Longer TTLs improve cache efficiency but risk serving stale content. TTLs must balance content freshness requirements against cache efficiency.

**Cache Invalidation** ensures users receive updated content when origins change. Challenges include the "thundering herd" problem (many requests simultaneously hitting expired cache) and distributed cache purging across thousands of edge nodes. Strategies include purge-on-update, TTL-based expiration, and content versioning through URL fingerprints.

**Edge Compute** extends traditional caching to include executing code at edge locations. Platforms like Cloudflare Workers, AWS Lambda@Edge, and Fastly Compute allow developers to run JavaScript, Rust, or WebAssembly at the edge, enabling dynamic personalization, A/B testing, authentication, and real-time data processing without origin round-trips.

## How It Works

When a user requests content through an edge-enabled delivery path, the flow proceeds as follows: DNS resolution returns the IP address of the nearest edge server rather than the origin. The edge server checks its local cache for the requested URL. If found and not expired, the cached content is returned immediately (cache hit). If not found or expired (cache miss), the edge server fetches content from the origin, stores a copy in its cache (respecting TTL), and returns it to the user.

CDN providers maintain extensive global infrastructure with edge servers in Internet Exchange Points (IXPs), carrier hotels, and data centers worldwide. These locations are chosen based on network topology, peering relationships, and population density to minimize latency. Edge server software (nginx, Varnish, or proprietary solutions) implements caching logic, header manipulation, and request routing.

Modern CDNs support sophisticated request routing through Anycast routing, where multiple edge locations announce the same IP address via BGP. User traffic is automatically directed to the geographically closest or least-loaded edge location. This provides built-in DDoS protection since attack traffic is distributed across many edge nodes.

Cache key construction determines how requests map to cached objects. By default, the full URL is the cache key, but CDNs allow customization to normalize parameters, strip query strings, or include/exclude headers. This enables scenarios like caching based on device type or ignoring tracking parameters that shouldn't create unique cache entries.

## Practical Applications

1. **Static Website Delivery**: Global caching of HTML pages, images, CSS, and JavaScript dramatically improves page load times for content-heavy sites. Combined with HTTP/2 or HTTP/3 multiplexing, this enables fast, reliable web experiences globally.

2. **Video Streaming**: Platforms like YouTube, Netflix, and Twitch use edge caching to stream video segments from nearby servers, reducing buffering and enabling adaptive bitrate streaming based on real-time network conditions.

3. **API Acceleration**: REST and GraphQL APIs can cache responses at the edge, reducing database load and improving response times for read-heavy endpoints. Cache-Control headers guide CDN caching behavior.

4. **Software Distribution**: Large file downloads (OS images, software installers, game patches) benefit from edge caching to reduce origin bandwidth costs and download times for users worldwide.

```nginx
# Example: NGINX configuration for edge caching
proxy_cache_path /data/nginx/cache levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m use_temp_path=off;

server {
    location / {
        proxy_cache my_cache;
        proxy_cache_valid 200 60m;
        proxy_cache_valid 404 1m;
        proxy_cache_lock on;
        add_header X-Cache-Status $upstream_cache_status;
        proxy_pass http://origin_server;
    }
}
```

## Examples

**Cloudflare Workers** run JavaScript at edge locations in over 300 cities, enabling developers to intercept requests, modify responses, authenticate users, and generate dynamic content without origin round-trips. Workers use the Service Workers API, making web development skills directly applicable to edge computing.

**Amazon CloudFront Functions** provide lightweight edge compute for request manipulation. Unlike Lambda@Edge (which runs in full Lambda environments in specific regions), CloudFront Functions executes at all CloudFront edge locations with sub-millisecond startup times.

**Varnish Configuration Language (VCL)** demonstrates backend cache server configuration:

```vcl
sub vcl_recv {
    if (req.url ~ "\.(jpg|png|gif|css|js)$") {
        unset req.http.Cookie;
        return(hash);
    }
}

sub vcl_backend_response {
    if (bereq.url ~ "\.(jpg|png|gif|css|js)$") {
        set beresp.ttl = 30d;
        set beresp.http.Cache-Control = "max-age=2592000";
    }
}
```

## Related Concepts

- [[Content Delivery Network]] - Broader infrastructure for content delivery
- [[Cache Invalidation]] - Strategies for maintaining freshness
- [[HTTP Caching]] - Cache-Control headers and caching semantics
- [[Load Balancing]] - Distributing requests across multiple servers
- [[CDN Configuration]] - Setting up and optimizing CDN performance
- [[Anycast Routing]] - Network-level request routing
- [[Web Performance]] - Optimizing user-facing performance metrics

## Further Reading

- "Web Performance" by Steve Souders - Classic guide to frontend performance
- MDN HTTP Caching documentation
- Cloudflare Cache documentation
- "High Performance Browser Networking" by Ilya Grigorik

## Personal Notes

Edge caching configuration is deceptively complex. The interaction between CDN TTLs, origin Cache-Control headers, and browser cache creates subtle caching hierarchies where debugging "why is this content stale?" requires understanding the full chain. Implementing cache versioning through content hashes in URLs (like `app.a1b2c3.js`) is more reliable than purging since it guarantees consistency and enables aggressive long-term caching.
