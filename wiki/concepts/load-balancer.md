---
title: Load Balancer
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [infrastructure, networking, scalability, microservices]
---

## Overview

A load balancer is a critical infrastructure component that distributes incoming network traffic across multiple servers to ensure no single server bears too much demand. By spreading requests across a pool of resources, load balancers optimize availability, maximize throughput, minimize response time, and provide fault tolerance. They act as traffic cops directing requests to the most appropriate backend based on various algorithms and health metrics.

Load balancers are fundamental to building scalable, resilient web applications and API services. Modern applications serve millions of users simultaneously, and a single server cannot handle this volume. Load balancers solve this horizontal scaling challenge by enabling multiple server instances to work together as a single logical unit.

## Key Concepts

### Layer 4 vs Layer 7 Load Balancing

**Layer 4 (Transport Layer)** load balancing operates on TCP/UDP packets, making routing decisions based on source and destination IP addresses and ports without inspecting message content. This approach is faster and more scalable due to minimal processing overhead but offers limited traffic management capabilities.

**Layer 7 (Application Layer)** load balancing examines HTTP/HTTPS headers and content to make routing decisions. This enables sophisticated features like URL-based routing, cookie-based session affinity, and content-aware request handling. Layer 7 load balancers can inspect, modify, and route traffic based on the actual request content.

### Health Checking

Load balancers continuously monitor backend server health through periodic probe requests. When a server fails health checks or becomes unresponsive, the load balancer automatically removes it from the pool and redistributes traffic to healthy instances. Once the server recovers and passes health checks, it is reinstated.

### Load Balancing Algorithms

Common algorithms include:

- **Round Robin**: Sequentially distributes requests across all servers
- **Least Connections**: Routes to the server with the fewest active connections
- **IP Hash**: Routes requests from the same client IP to the same server (session affinity)
- **Weighted**: Distributes traffic proportionally based on server capacity

## How It Works

When a client sends a request to an application, the request first reaches the load balancer's virtual IP address. The load balancer's software (or hardware) evaluates the request against configured rules, selects an appropriate backend server based on the chosen algorithm, and forwards the request.

Modern load balancers operate as reverse proxies—clients connect to the load balancer without knowledge of the backend servers. This architecture provides several benefits:

**High Availability**: If a backend server fails, traffic is automatically redirected to healthy instances without service interruption.

**Horizontal Scalability**: Backend servers can be added or removed dynamically without disrupting service.

**Security**: Load balancers can implement DDoS protection, rate limiting, and SSL termination, offloading these concerns from application servers.

**Geographic Distribution**: Global server load balancing (GSLB) routes users to the nearest datacenter, reducing latency.

## Practical Applications

In microservices architectures, load balancers enable service discovery and dynamic routing. When combined with service registries, load balancers can automatically route traffic to newly deployed service instances, supporting zero-downtime deployments and auto-scaling.

API gateways often incorporate load balancing alongside authentication, rate limiting, and request transformation. Cloud providers offer managed load balancer services like AWS Application Load Balancer (ALB), Google Cloud Load Balancing, and Azure Load Balancer that integrate with their respective ecosystems.

## Examples

A typical NGINX load balancer configuration:

```nginx
upstream backend {
    least_conn;  # Least connections algorithm
    
    server 10.0.1.1:8080 weight=3;
    server 10.0.1.2:8080 weight=2;
    server 10.0.1.3:8080 weight=1;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

This configuration creates a load-balanced backend pool using the least connections algorithm with weighted server capacities.

## Related Concepts

- [[API-Gateway]] - API management layer that often includes load balancing
- [[microservices]] - Architecture pattern that relies heavily on load balancing
- [[CDN]] - Content delivery networks with built-in load balancing
- [[Caching]] - Request caching at the load balancer layer
- [[scalability]] - Horizontal scaling enabled by load balancers
- [[reliability]] - Fault tolerance through load distribution

## Further Reading

- "Load Balancing: Concepts, Algorithms and Systems" - Comprehensive technical overview
- NGINX Load Balancer Documentation - Practical configuration guide
- AWS Application Load Balancer Documentation - Cloud-native load balancing patterns

## Personal Notes

Load balancers are deceptively simple yet critically important. When designing distributed systems, I often start by thinking about load balancing strategy because it affects nearly every aspect of the architecture—how services discover each other, how deployments work, how failures are handled. The choice between Layer 4 and Layer 7 depends on your needs: if you need content-aware routing or API gateway features, go Layer 7; if raw performance is paramount, Layer 4 may be better.
