---
title: Load Balancing
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [load-balancing, networking, scalability, infrastructure]
---

# Load Balancing

Load balancing is a critical technique in distributed systems that distributes incoming network traffic across multiple servers, ensuring no single server becomes overwhelmed with requests. By spreading the workload evenly, load balancers improve application responsiveness, increase availability, and provide fault tolerance for modern web applications and services.

## Overview

In any production environment serving real users, a single server quickly reaches its capacity limits when traffic increases. Load balancing solves this problem by sitting in front of one or more servers and acting as a reverse proxy, routing client requests to available servers based on various criteria. This architectural pattern is fundamental to building scalable, highly available systems.

A load balancer performs several essential functions. First, it distributes traffic efficiently across multiple backend servers. Second, it performs health checks to detect when a server is failing or becoming unresponsive, automatically removing it from the rotation until it recovers. Third, it can terminate SSL/TLS connections, offloading cryptographic processing from application servers. Fourth, many load balancers provide caching, compression, and other optimizations that improve end-to-end performance.

Load balancers operate at different layers of the networking stack. Layer 4 (transport layer) load balancers make routing decisions based on IP addresses and port numbers, offering fast performance with minimal inspection. Layer 7 (application layer) load balancers can inspect HTTP headers, URLs, and even request content to make more intelligent routing decisions, such as directing API requests to specialized backend services.

Modern cloud environments and container orchestration platforms like Kubernetes include built-in load balancing mechanisms. However, dedicated hardware load balancers and software solutions like HAProxy, Nginx, and AWS Elastic Load Balancer remain widely used in enterprise and high-traffic scenarios.

## Algorithms

Load balancing algorithms determine how incoming requests are distributed across available servers. Different algorithms suit different use cases, and choosing the right one depends on your traffic patterns, server capabilities, and reliability requirements.

**Round Robin** is the simplest algorithm, cycling through servers in sequential order. Each new request goes to the next server in the list, then returns to the top. This works well when all servers have identical capacity, but performs poorly when servers have varying hardware specifications or existing workloads.

**Weighted Round Robin** extends the basic algorithm by assigning a weight to each server. Higher-capacity servers receive proportionally more traffic. A server with weight 3 receives three requests for every one sent to a server with weight 1.

**Least Connections** routes new requests to the server with the fewest active connections at that moment. This algorithm adapts dynamically to varying request durations and is particularly effective when requests have unpredictable or widely varying processing times.

**Weighted Least Connections** combines the connection count with server weight, ensuring busy servers are not overloaded while respecting different server capacities.

**IP Hash** uses a cryptographic hash of the client IP address to determine which server handles a request. This approach ensures the same client consistently reaches the same server, which is useful for maintaining session affinity.

**Least Response Time** is an advanced algorithm that considers both connection count and server health, directing traffic to servers that can respond fastest. This approach optimizes user experience by minimizing latency.

## Related

- [[Reverse Proxy]] — Servers that sit between clients and backend services
- [[High Availability]] — Systems designed to operate continuously without failure
- [[Horizontal Scaling]] — Adding more machines to handle increased load
- [[Health Checks]] — Mechanisms to verify server availability
- [[API Gateway]] — Centralized entry point for managing API traffic
- [[Microservices]] — Architectural style often dependent on load balancing
- [[Distributed Systems]] — The broader field of computing across multiple nodes
- [[Failover]] — Automatic switching to backup systems when primary fails
