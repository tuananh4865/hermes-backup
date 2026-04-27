---
title: Proxy
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [proxy, networking, architecture, pattern]
---

## Overview

A proxy is an intermediary software component that sits between a client and a server, intercepting requests and forwarding them on behalf of the client. The word "proxy" literally means "acting on behalf of another," which precisely describes the role this pattern plays in software architecture. Proxies are used to add functionality such as caching, access control, logging, request transformation, and load balancing without the client or server needing to be aware of the proxy's existence.

In the proxy pattern, the client sends its request to the proxy instead of directly to the target server. The proxy evaluates the request, may modify it or apply policies, and then passes it along to the server. Similarly, responses from the server flow back through the proxy, where they can be inspected, filtered, or transformed before reaching the client. This bidirectional interception makes proxies incredibly versatile building blocks in modern system design.

Proxies operate at various levels of the network stack. Some work at the application layer (HTTP proxies), while others operate at lower layers such as TCP or even the packet level. The choice of layer depends on what kind of control and functionality is needed. Application-layer proxies understand the semantics of the protocol being proxied, while lower-layer proxies can handle raw traffic more efficiently but with less context about the actual content.

The proxy pattern is fundamental to many real-world technologies, from content delivery networks and enterprise firewalls to service meshes in microservices architectures. It provides a clean separation of concerns, allowing cross-cutting functionality to be implemented and managed independently of the core application logic.

## Types

There are three primary categories of proxies, each serving distinct purposes in network and software architecture.

**Forward Proxy**

A forward proxy acts on behalf of clients, intercepting outgoing requests and forwarding them to servers. The client configured its browser or application to use the forward proxy, which then makes requests to external services on the client's behalf. Forward proxies are commonly used for anonymity, where they hide the client's IP address from the destination server, and for content filtering, where organizations use them to block access to certain websites or monitor employee internet usage. Forward proxies can also cache frequently requested content to reduce bandwidth consumption and improve response times.

**Reverse Proxy**

A reverse proxy works in the opposite direction, acting on behalf of servers rather than clients. Incoming requests from clients arrive at the reverse proxy, which then forwards them to one or more backend servers. The client typically has no knowledge that it is communicating with a proxy rather than the actual server. Reverse proxies are widely used for load balancing, distributing incoming traffic across multiple backend servers to improve scalability and reliability. They also provide SSL termination, handling encryption and decryption so that backend servers do not need to perform these computationally intensive operations.

**Transparent Proxy**

A transparent proxy intercepts requests without the client or server being aware of its presence. Unlike forward or reverse proxies, which require explicit configuration on the client or server side, transparent proxies intercept traffic at the network level, often through routing configuration or network bridging. This makes them useful for scenarios where modifying client or server configuration is impractical, such as ISP-level content filtering or involuntary caching. Transparent proxies can implement caching, access control, or traffic monitoring without requiring any changes to existing client or server software.

## Related

- [[Load Balancer]] - Distributes traffic across multiple servers, often implemented using reverse proxy techniques
- [[API Gateway]] - Acts as a single entry point for microservices, similar to a reverse proxy with additional protocol translation
- [[Service Mesh]] - A dedicated infrastructure layer for service-to-service communication that often uses sidecar proxies
- [[Caching]] - A common proxy function that stores copies of responses to reduce latency and bandwidth usage
- [[Firewall]] - Network security systems that use proxy-like interception to filter traffic
- [[NAT]] - Network Address Translation often works alongside proxies for address hiding and network address sharing
