---
title: "Containers"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [containers, virtualization, docker, devops, cloud-computing, software-deployment]
---

# Containers

## Overview

Containers are lightweight, standalone executable packages that include everything needed to run a piece of software: code, runtime, libraries, system tools, and settings. They provide consistency across different environments from development through production, solving the "works on my machine" problem that has plagued software deployment for decades. Containerization technology, popularized by [[Docker]], has become a cornerstone of modern [[DevOps]] practices and [[cloud computing]] infrastructure.

Unlike traditional [[virtualization|virtual machines]] that include a full operating system, containers share the host system's kernel and isolate processes at the application level. This makes them significantly more efficient in terms of resource usage and startup time. A container can start in seconds while a VM might take minutes, and multiple containers can run on a single host with minimal overhead.

## Key Concepts

**Images** are read-only templates used to create containers. An image contains the application code, dependencies, and configuration needed to run. Images are built in layers, allowing efficient storage and sharing. Base images provide the operating system foundation, while custom images add application-specific components.

**Registries** are repositories for storing and distributing container images. [[Docker Hub]] is the default public registry, while organizations often run private registries for proprietary software and faster deployment. Image tags help version control, with "latest" being the default tag.

**Orchestration** manages multiple containers across multiple hosts, handling scaling, load balancing, and deployment rolling updates. [[Kubernetes]] has emerged as the dominant container orchestration platform, providing automated container deployment, scaling, and management.

## How It Works

Containers use operating system-level virtualization features to isolate processes. Linux containers leverage namespaces for process isolation (PID, network, mount, IPC, UTS) and control groups (cgroups) for resource limiting. Each container sees its own isolated view of the system,以为自己拥有独立的进程树、网络 interfaces, and filesystem.

When a container runs, it creates a writable layer on top of the read-only image layers. All changes are written to this container layer, which is specific to that container instance. This copy-on-write mechanism allows multiple containers to share the same base image while maintaining their own state.

```dockerfile
# Example: Multi-stage Dockerfile for a Node.js application
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Practical Applications

Containers power many modern software deployment scenarios:

- **Microservices Architecture**: Each microservice runs in its own container, enabling independent scaling and deployment
- **CI/CD Pipelines**: Consistent build and test environments accelerate development velocity
- **Hybrid Cloud Deployments**: Containerized applications run identically across on-premises and cloud infrastructure
- **Local Development**: Developers run the same containers locally as in production
- **Serverless Computing**: Functions as a Service (FaaS) often use containers under the hood

## Examples

Common containerization tools and platforms include:

- **Docker**: The most popular container runtime and platform
- **Podman**: Daemonless container engine compatible with Docker images
- **Kubernetes**: Container orchestration for production deployments
- **Amazon ECS/EKS**: AWS container orchestration services
- **Google Kubernetes Engine (GKE)**: Managed Kubernetes on Google Cloud

## Related Concepts

- [[Docker]] - Leading container platform and image format
- [[Kubernetes]] - Container orchestration system
- [[Virtualization]] - Technology for creating virtual computing environments
- [[Microservices]] - Architectural style often using containers
- [[DevOps]] - Development practices enhanced by containerization

## Further Reading

- Docker Documentation: https://docs.docker.com
- Kubernetes Documentation: https://kubernetes.io/docs
- "The Docker Book" by James Turnbul
- Container networking concepts and best practices

## Personal Notes

Containers have fundamentally changed how software is deployed and managed. The standardization they bring to build, test, and production environments reduces deployment friction and improves reliability. However, container security remains a concern, as shared kernels can potentially be exploited. Understanding container networking, storage, and resource management is essential for anyone working in modern cloud infrastructure. The ecosystem continues to evolve, with tools like [[Docker Compose]] simplifying local multi-container development and service mesh technologies adding sophisticated traffic management capabilities.
