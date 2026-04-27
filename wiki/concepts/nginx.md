---
title: "Nginx"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nginx, web-server, reverse-proxy, load-balancer, http]
---

# Nginx

## Overview

Nginx (pronounced "engine-x") is a high-performance, open-source web server and reverse proxy server created by Igor Sysoev in 2004. It was designed from the ground up to handle the C10K problem—serving 10,000+ concurrent connections—a challenge that traditional synchronous web servers struggled with. Nginx uses an event-driven, non-blocking architecture that makes it exceptionally efficient at handling large numbers of simultaneous connections with minimal memory footprint.

Beyond serving static content, Nginx functions as a reverse proxy, load balancer, HTTP cache, and TLS terminator. It powers a significant portion of the internet's busiest websites, including Netflix, Airbnb, WordPress.com, and GitHub. Its configuration language is declarative and focused on request processing pipelines, making it both powerful and—once you understand its model—relatively straightforward to reason about.

Nginx processes are organized with a master process (which reads and evaluates configuration, and manages worker processes) and multiple worker processes (which handle actual request processing). This architecture allows configuration reloads without downtime and enables worker processes to be isolated from each other for security and reliability.

## Core Configuration Model

Nginx's configuration lives in `nginx.conf` (and optionally includes other files via `include` directives). The configuration is structured as a hierarchy of context blocks that apply to different scopes.

The main contexts are:

- **main**: Global settings that affect the entire server.
- **http**: Settings for HTTP/HTTPS traffic, applies to all virtual servers.
- **server**: A virtual server definition (like a virtual host in Apache), defined by `listen` and `server_name`.
- **location**: Rules for matching request URIs within a server.

```nginx
# /etc/nginx/nginx.conf

worker_processes auto;
error_log /var/log/nginx/error.log warn;

events {
    worker_connections 1024;
    use epoll;        # Linux-specific event polling
    multi_accept on;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    # Logging format with response time
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent" '
                    'rt=$request_time uct=$upstream_connect_time';

    access_log /var/log/nginx/access.log main;

    # Performance optimizations
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    gzip on;

    # Rate limiting zone
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;

    # Upstream backend servers
    upstream api_backend {
        least_conn;              # Load balancing method
        server 10.0.1.10:8000 weight=3;
        server 10.0.1.11:8000 weight=2;
        server 10.0.1.12:8000 backup;
        keepalive 32;
    }

    server {
        listen 80;
        server_name example.com www.example.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name example.com;

        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers on;

        root /var/www/html;
        index index.html;

        # Static file serving
        location /static/ {
            alias /srv/static files/;
            expires 30d;
            add_header Cache-Control "public, immutable";
        }

        # Proxy to API backend
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_connect_timeout 5s;
            proxy_read_timeout 30s;
        }

        # WebSocket support
        location /ws/ {
            proxy_pass http://api_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }

        # Health check endpoint (no logging)
        location /health {
            access_log off;
            return 200 'OK';
            add_header Content-Type text/plain;
        }
    }
}
```

## Key Concepts

**Event-Driven Architecture**: Unlike Apache's thread-per-connection model, Nginx uses an event loop with non-blocking I/O. A small number of worker processes (typically equal to the number of CPU cores) can handle tens of thousands of connections each by multiplexing I/O operations. This makes Nginx extremely memory-efficient under high concurrency.

**Reverse Proxying**: Nginx sits between clients and backend servers, forwarding requests and responses. As a reverse proxy, it can:
- Load balance across multiple backends using methods like round-robin, least-connections, or IP-hash
- Terminate SSL/TLS connections, offloading cryptographic work from backends
- Cache responses from backends to serve repeated requests instantly
- Compress responses to reduce bandwidth

**Load Balancing Methods**:
- **round-robin** (default): Requests distributed evenly in order
- **least_conn**: Routes to server with fewest active connections
- **IP hash**: Consistent hashing based on client IP (useful for session affinity)
- **weighted**: Manual weight allocation for unequal backend capacity

## Practical Applications

**Serving Static Websites**: Nginx excels at serving HTML, CSS, JavaScript, images, and other static assets directly from the filesystem, often orders of magnitude faster than application servers.

**API Gateway**: Nginx can serve as a lightweight API gateway, routing requests to different microservices based on URL paths, applying rate limiting, authentication checks, and request transformations.

**TLS Termination**: By terminating SSL/TLS at Nginx, backend application servers are freed from cryptographic overhead. Nginx supports modern protocols (TLS 1.3), hardware acceleration, and OCSP stapling.

**Docker Registry Frontend**: Many organizations use Nginx in front of Docker Registry to provide authentication, rate limiting, and TLS termination for their container image storage.

## Examples

### Basic Static Site
```nginx
server {
    listen 80;
    server_name mysite.com;
    root /var/www/mysite;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Load Balancer with Health Checks
```nginx
upstream backend {
    server 192.168.1.10:8080 max_fails=3 fail_timeout=30s;
    server 192.168.1.11:8080 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    location / {
        proxy_pass http://backend;
        proxy_next_upstream error timeout invalid_header;
    }
}
```

## Related Concepts

- [[Reverse Proxy]] — The concept of forwarding client requests to backend servers
- [[Load Balancer]] — Distributing traffic across multiple servers
- [[HTTP]] — The protocol Nginx primarily serves
- [[tls]] — Cryptographic protocols for secure communication that Nginx terminates
- [[Docker]] — Container platform where Nginx is commonly deployed
- [[Kubernetes]] — Container orchestrator that often uses Nginx as an Ingress controller

## Further Reading

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Nginx Performance Tuning Guide](https://docs.nginx.com/nginx/admin-guide/)
- [Understanding Nginx Configuration](https://www/nginx.com/resources/wiki/start/)

## Personal Notes

Nginx's configuration model took me a while to fully internalize. The `location` matching algorithm—with its prefixes, exact matches, and regex modifiers—has specific precedence rules that aren't always obvious. Also worth noting: `proxy_set_header` defaults drop some headers, so you often need to explicitly set `Host`, `X-Real-IP`, and `X-Forwarded-For` when proxying. The `try_files` directive is incredibly useful for single-page apps.
