---
title: "CNCF"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [cncf, cloud-native, kubernetes, foundation]
---

# CNCF

The Cloud Native Computing Foundation (CNCF) is a non-profit organization that serves as the governing body for a vast ecosystem of open-source cloud-native technologies. Founded in 2015 as a part of the Linux Foundation, CNCF's primary mission is to establish and maintain a vendor-neutral hub for the development, promotion, and standardization of technologies that power modern distributed systems. The foundation provides governance, legal support, financial backing, and community stewardship to projects ranging from container orchestration to observability, networking, and security. By fostering collaboration among developers, enterprises, and cloud providers, CNCF has become the central authority driving the evolution of cloud-native computing.

## Overview

Cloud-native computing represents a paradigm shift in how software is built, deployed, and operated. It emphasizes the use of containers, microservices architecture, declarative APIs, and immutable infrastructure to create systems that are scalable, resilient, and loosely coupled. CNCF was established to steward this approach by providing a neutral home for the projects and specifications that define the cloud-native ecosystem.

The foundation hosts over 170 open-source projects and members from across the technology industry, including major cloud providers, independent software vendors, and thousands of individual contributors. CNCF's governance model ensures that projects evolve through community consensus rather than corporate control, which helps maintain interoperability and prevents vendor lock-in. The foundation also runs certification programs for Kubernetes and other technologies, ensuring consistency and quality across implementations.

CNCF's influence extends beyond software development. It publishes the Cloud Native Interactive Landscape, a comprehensive map of the cloud-native ecosystem that helps organizations navigate available tools and technologies. The foundation also organizes KubeCon + CloudNativeCon, one of the largest gatherings of cloud-native practitioners in the world, bringing together thousands of developers and operators to share knowledge and shape the future of the ecosystem.

## Key Projects

CNCF supports a diverse portfolio of projects that address every layer of the cloud-native stack.

**Kubernetes** is the foundation's most prominent project and the de facto standard for container orchestration. Originally developed by Google and donated to CNCF in 2015, Kubernetes automates the deployment, scaling, and management of containerized applications across clusters of machines. It provides a declarative configuration model, self-healing capabilities, horizontal scaling, and a rich ecosystem of extensions. Kubernetes has become the backbone of modern cloud infrastructure, running everything from small startups to massive global deployments at companies like Netflix, Airbnb, and Spotify.

**Prometheus** is a systems monitoring and alerting toolkit originally built at SoundCloud and donated to CNCF in 2016. Prometheus collects and stores metrics as time series data, enabling real-time visibility into application and infrastructure performance. Its powerful query language, dynamic service discovery, and alerting capabilities make it a cornerstone of observability in cloud-native environments. Prometheus formed the basis for the OpenMetrics specification and integrates closely with Kubernetes for auto-discovery of monitoring targets.

**Envoy** is a high-performance edge and service proxy designed for cloud-native applications. Developed at Lyft and donated to CNCF in 2017, Envoy provides advanced traffic management, observability, and security features for service mesh architectures. Envoy's filter chain architecture allows extensible customization of proxy behavior, while its mature implementation of L7 networking makes it ideal for building resilient, observable distributed systems. Envoy serves as the data plane for Istio, one of the most widely used service mesh implementations.

## Related

- [[Kubernetes]] - Container orchestration platform and CNCF's flagship project
- [[Prometheus]] - Systems monitoring and alerting toolkit
- [[Envoy]] - Edge and service proxy for cloud-native applications
- [[Service Mesh]] - Architectural pattern for managing service-to-service communication
- [[Containers]] - Lightweight, portable packaging for applications
- [[Microservices]] - Architectural style structuring applications as service collections
- [[Observability]] - Ability to understand internal system state from external outputs
- [[Cloud Native]] - Approach to building and running applications in modern distributed environments
- [[Linux Foundation]] - Parent organization of CNCF
