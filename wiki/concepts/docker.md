---
title: "Docker"
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [docker, containers, devops, virtualization, ci-cd]
confidence: medium
relationships:
  - 🔗 ci-cd
  - 🔗 kubernetes
  - 🔗 container
---

# Docker

## Overview

Docker is a platform for developing, shipping, and running applications in containers - lightweight, standalone executable packages that include everything needed to run software: code, runtime, libraries, and settings.

Containers differ from virtual machines by sharing the host OS kernel while maintaining process-level isolation. This makes them significantly more efficient and faster to start than VMs, enabling modern deployment patterns like microservices and serverless functions.

## Key Concepts

### Images and Containers

**Docker Images** are read-only templates used to create containers:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

**Containers** are running instances of images:

```bash
# Build image
docker build -t myapp:latest .

# Run container
docker run -d -p 8000:8000 --name myapp myapp:latest

# List running containers
docker ps
```

### Layers and Caching

Docker images consist of stacked layers:

```
FROM ubuntu:22.04       # Base layer
RUN apt-get update      # Layer 1
RUN apt-get install...  # Layer 2
COPY . .                 # Layer 3
CMD                      # Layer 4
```

Each layer is cached and reused when possible, making rebuilds fast.

### Networking

Docker provides several networking modes:

```bash
# Bridge (default)
docker run --network bridge myapp

# Host (skip network isolation)
docker run --network host myapp

# Custom network (for inter-container communication)
docker network create mynet
docker run --network mynet myapp
```

### Volumes

Persist data outside container lifecycle:

```bash
# Named volume
docker run -v mydata:/var/data myapp

# Bind mount (host directory)
docker run -v $(pwd):/app myapp

# Read-only mount
docker run -v $(pwd):/app:ro myapp
```

## Practical Applications

### Docker Compose

Define multi-container applications:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - DATABASE_URL=postgresql://db/app

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD=secret

  redis:
    image: redis:7-alpine

volumes:
  postgres_data:
```

```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f app

# Stop all services
docker compose down
```

### Multi-stage Builds

Reduce final image size:

```dockerfile
# Build stage
FROM golang:1.21 AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM alpine:3.19
COPY --from=builder /app/myapp /myapp
CMD ["/myapp"]
```

This produces a tiny image without the Go toolchain.

### CI/CD Integration

```yaml
# GitHub Actions example
- name: Build and push Docker image
  uses: docker/build-push-action@v5
  with:
    push: ${{ github.event_name != 'pull_request' }}
    tags: ghcr.io/user/myapp:${{ github.sha }}
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

### Security Best Practices

```dockerfile
# Use specific base version, not 'latest'
FROM python:3.11.4-slim

# Create non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser
USER appuser

# Read-only filesystem
docker run --read-only myapp

# No privileged mode
docker run --cap-drop=ALL myapp
```

## Related

- [[ci-cd]] — Continuous integration pipelines
- [[kubernetes]] — Container orchestration
- [[docker]] — Container technology overview
