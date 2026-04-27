---
title: Cloud Native
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [cloud-native, cncf, containers, kubernetes]
---

## Overview

Cloud Native is an approach to building and running applications that fully exploits the advantages of cloud computing platforms. It encompasses a complete software development and delivery methodology centered on containerization, microservices architecture, continuous delivery, and DevOps practices. Cloud Native applications are designed from the ground up to thrive in dynamic, distributed environments where resources are provisioned elastically, failure is a first-class concern, and scaling happens automatically.

The Cloud Native Computing Foundation (CNCF) defines Cloud Native technologies as those that enable organizations to build and run scalable applications in modern, dynamic environments such as public, private, and hybrid clouds. Key characteristics include container-packaged applications, dynamically managed workloads, and loosely coupled architectures. This stands in contrast to traditional monolithic applications that are typically deployed on static infrastructure and require manual scaling and maintenance operations.

At its core, Cloud Native represents a fundamental shift in how software is constructed, deployed, and operated. Applications are decomposed into small, independent services called [[microservices]], each owning its data and communicating through lightweight protocols. These services are packaged in [[containers]], which provide consistent behavior across development, testing, and production environments. The entire stack is orchestrated by platforms like [[Kubernetes]], which handle scheduling, scaling, healing, and updates automatically.

## 12-Factor Apps

The [[12-Factor App]] methodology, originally published by Heroku in 2011, provides a blueprint for building software-as-a-service applications that are suited for Cloud Native deployment. It outlines twelve best practices that address common problems in modern application development, including configuration management, dependency handling, backing services, and logging.

The twelve factors are: codebase (one repo per app), dependencies (explicitly declared and isolated), configuration (store config in environment variables), backing services (treat databases and caches as attached resources), build/release/run (strict separation of build and run stages), processes (execute the app as stateless processes), port binding (export services via port binding), concurrency (scale via process model), disposability (maximize robustness with fast startup and graceful shutdown), parity between development and production (keep environments as similar as possible), logs (treat logs as event streams), and admin processes (run administrative tasks as one-off processes).

These principles ensure that applications are portable across different Cloud Native environments, maintain consistency between deployments, and can scale horizontally without modification. Modern container orchestration platforms like Kubernetes implement many of these principles natively, making 12-Factor compliance a natural fit for Cloud Native deployments.

## CNCF Ecosystem

The [[CNCF]] (Cloud Native Computing Foundation) is a Linux Foundation project that serves as the open source governance hub for Cloud Native technologies. Founded in 2015, CNCF hosts and nurtures a broad ecosystem of projects spanning the entire Cloud Native stack, from low-level container runtimes to end-user applications.

Key CNCF projects include [[Kubernetes]] (the de facto standard for container orchestration), [[Prometheus]] (for monitoring and alerting), [[Grafana]] (for visualization), [[Envoy]] (for service mesh and networking), [[Istio]] (for service mesh traffic management), [[Helm]] (for package management), [[ Argo CD]] (for continuous delivery), and [[OPA]] (Open Policy Agent for policy enforcement). CNCF also maintains a Certified Kubernetes Conformance program that ensures interoperability between different Kubernetes distributions.

The CNCF Landscape organizes projects into categories including App Definition and Development, Orchestration and Management, Runtime, and Miscellaneous. This structured approach helps organizations navigate the Cloud Native ecosystem and select appropriate technologies for their needs. CNCF also provides educational resources, certification programs for professionals (KCSP, CKA, CKD), and organizes KubeCon, the world's largest Cloud Native conference.

## Related

- [[Containers]] - Lightweight, portable packaging for applications and their dependencies
- [[Kubernetes]] - Open source container orchestration platform
- [[Microservices]] - Architectural style decomposing applications into small, independent services
- [[CNCF]] - The foundation governing Cloud Native standards and projects
- [[12-Factor App]] - Methodology for building Cloud Native-ready applications
- [[DevOps]] - Cultural and operational practices enabling continuous delivery
- [[Service Mesh]] - Infrastructure layer for managing service-to-service communication
- [[Serverless Functions]] - Event-driven compute model abstracting server management
