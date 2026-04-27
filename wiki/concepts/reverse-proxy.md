---
title: "Reverse Proxy"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [networking, infrastructure, proxy, web-servers, load-balancing]
---

# Reverse Proxy

## Overview

A reverse proxy is a server that sits between clients and one or more backend servers, intercepting requests from clients and forwarding them to appropriate backend resources. Unlike a forward proxy (which acts on behalf of clients, like a VPN or content filter), a reverse proxy acts on behalf of servers — clients typically don't know they're communicating with a proxy rather than the actual origin server. The reverse proxy receives incoming requests, potentially performs processing on them, and then returns responses from the backend servers to the clients.

The reverse proxy is a fundamental piece of internet infrastructure. When you visit a popular website, the odds are excellent that your request first hits a reverse proxy (or a CDN edge node, which is a specialized reverse proxy) before being routed to origin servers. This placement enables numerous capabilities: load distribution across multiple servers, SSL/TLS termination, caching for performance, security filtering, and geographic routing. Reverse proxies are essentially the gatekeepers and traffic directors for modern web applications.

## Key Concepts

**Load Balancing** is one of the primary functions of a reverse proxy. By distributing incoming requests across multiple backend servers, a reverse proxy enables horizontal scaling — you can handle more traffic by adding servers rather than building more powerful single servers. Load balancing algorithms range from simple (round-robin, random) to sophisticated (least connections, IP hash, weighted by health metrics).

**SSL/TLS Termination** occurs when the reverse proxy handles encryption/decryption rather than backend servers. Clients connect to the proxy using HTTPS, the proxy decrypts the request, and forwards it internally to backends over plain HTTP (or encrypted, depending on setup). This reduces cryptographic load on application servers and centralizes certificate management.

**Caching** allows reverse proxies to serve frequently-requested content without hitting backend servers. Static assets (images, CSS, JavaScript), API responses that rarely change, and even full HTML pages can be cached and served directly, dramatically improving response times and reducing backend load.

**Health Checking** ensures traffic only goes to functional backend servers. Reverse proxies perform periodic checks on backend health and remove unhealthy servers from rotation until they recover, providing automatic failover without application-level awareness.

**Request/Response Manipulation** enables modifications at the proxy layer. Headers can be added, removed, or rewritten. URLs can be rewritten for path-based routing. Responses can be compressed or decompressed. This flexibility enables many infrastructure transformations without changing application code.

## How It Works

A typical reverse proxy setup involves directing DNS to point to the proxy rather than directly to application servers:

```nginx
# Nginx configuration as reverse proxy
upstream backend_servers {
    server 10.0.1.10:8080 weight=3;
    server 10.0.1.11:8080 weight=2;
    server 10.0.1.12:8080;
}

server {
    listen 443 ssl;
    server_name api.example.com;
    
    # SSL/TLS termination
    ssl_certificate /etc/ssl/certs/example.com.pem;
    ssl_certificate_key /etc/ssl/private/example.com.key;
    
    # Security headers
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header Host $host;
    
    location / {
        # Load balancing to upstream
        proxy_pass http://backend_servers;
        
        # Timeouts and buffering
        proxy_connect_timeout 30s;
        proxy_read_timeout 30s;
        proxy_buffering on;
    }
    
    # Cache static assets for 7 days
    location /static/ {
        proxy_cache static_cache;
        proxy_cache_valid 200 7d;
        expires 7d;
    }
}
```

```yaml
# Kubernetes Ingress as reverse proxy configuration
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /users
        pathType: Prefix
        backend:
          service:
            name: users-service
            port:
              number: 80
      - path: /orders
        pathType: Prefix
        backend:
          service:
            name: orders-service
            port:
              number: 80
```

## Practical Applications

Reverse proxies are ubiquitous infrastructure components:

- **Content Delivery Networks (CDNs)**: Distributed reverse proxies positioned globally close to users, caching content at edge locations
- **API Gateways**: Specialized reverse proxies for API traffic, handling authentication, rate limiting, and protocol translation
- **Web Application Firewalls (WAFs)**: Reverse proxies that filter malicious traffic (SQL injection, XSS attacks) before reaching applications
- **Microservices architecture**: Service meshes use sidecar proxies intercepting service-to-service communication
- **A/B testing and feature flags**: Routing a percentage of traffic to different backend versions based on headers or cookies

## Examples

Docker Compose with reverse proxy for local development:

```yaml
# docker-compose.yml with Traefik as reverse proxy
services:
  traefik:
    image: traefik:v2.10
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik.toml:/traefik.toml
    networks:
      - web
  
  webapp:
    image: myapp:latest
    labels:
      - "traefik.http.routers.webapp.rule=Host(`app.localhost`)"
      - "traefik.http.routers.webapp.entrypoints=web"
    networks:
      - web
    depends_on:
      - api
  
  api:
    image: myapi:latest
    labels:
      - "traefik.http.routers.api.rule=Host(`api.localhost`)"
      - "traefik.http.routers.api.entrypoints=web"
    networks:
      - web

networks:
  web:
    external: true
```

## Related Concepts

- [[Load Balancing]] - Distributing traffic across servers
- [[API Gateway]] - Specialized reverse proxy for APIs
- [[CDN]] - Content Delivery Networks as distributed reverse proxies
- [[Web Servers]] - Server software often acting as reverse proxies
- [[Nginx]] - Popular reverse proxy software
- [[Docker]] - Container orchestration where reverse proxies are common

## Further Reading

- Nginx Documentation - Comprehensive reverse proxy configuration guide
- "Reverse Proxy" Wikipedia article for historical context
- Traefik Documentation for modern container-aware proxy
- Cloudflare Learning Center on CDN and proxy fundamentals

## Personal Notes

I've configured reverse proxies in virtually every production deployment I've worked on, and they're one of those pieces of infrastructure whose importance becomes apparent only when they're missing or misconfigured. The most common issue: health checks need careful tuning. Too aggressive and you'll get flapping (servers rapidly joining and leaving the pool); too lenient and you'll route traffic to unresponsive servers. I also recommend investing time in understanding caching headers (Cache-Control, ETag, Last-Modified) and how they interact with proxy caching — misconfigured caching is how you end up serving stale data or caching sensitive information. One thing many overlook: reverse proxies are a single point of failure if you only have one. Plan for redundancy from the start.
