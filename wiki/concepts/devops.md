---
title: "Devops"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [devops, software-development, operations, automation]
---

# Devops

DevOps is a cultural and technical movement that bridges the traditionally separated domains of software development and IT operations. The term combines "development" and "operations," reflecting its core mission: to eliminate the silos between teams that build software and those that deploy and maintain it. DevOps promotes collaborative practices, automation, and continuous feedback loops to deliver software faster, more reliably, and with higher quality.

The DevOps mindset emerged from recognizing that handoffs between development and operations teams often create bottlenecks, miscommunication, and deployment failures. Rather than treating these as separate concerns, DevOps embeds operations thinking into the development process and encourages developers to understand the runtime environment of their applications. This shared responsibility leads to more robust systems and faster iteration cycles.

## Overview

At its heart, DevOps is about flow and feedback. It seeks to maximize the flow of work from development through operations to the end user, while gathering feedback at every stage to improve continuously. The approach draws heavily from [[Agile]] methodologies and the [[Lean]] manufacturing principle of eliminating waste. Organizations adopt DevOps to reduce the lead time from code commit to running production software, decrease deployment failure rates, and shorten recovery times when failures occur.

DevOps transformation typically involves changes across people, process, and technology dimensions. Culturally, it encourages breaking down team boundaries, fostering a sense of shared ownership, and promoting a culture of experimentation and learning from failure. Technically, it relies heavily on automation across the entire software delivery lifecycle, from code integration and testing to deployment and infrastructure management.

The movement has also given rise to new roles such as [[Site Reliability Engineering]] (SRE), which applies software engineering practices to IT operations, and [[Platform Engineering]], which focuses on building internal developer platforms that streamline the path from code to production.

## Core Practices

**Continuous Integration and Continuous Delivery (CI/CD)** form the backbone of DevOps technical practices. [[Continuous Integration]] is the discipline of merging all developer code changes into a shared repository multiple times per day, with each integration triggering automated builds and tests to detect integration issues early. [[Continuous Delivery]] extends this by ensuring that code changes are automatically prepared for release to production after passing tests, allowing teams to deploy at any time with confidence. [[Continuous Deployment]] goes further by automatically releasing every change that passes the pipeline to production.

**Infrastructure as Code (IaC)** is another foundational DevOps practice. Rather than manually provisioning and configuring servers and infrastructure, teams define their infrastructure in code files that can be versioned, reviewed, and tested like application code. Tools like Terraform, Ansible, and Pulumi enable reproducible infrastructure deployments that reduce configuration drift and enable disaster recovery.

**Monitoring and Observability** are critical for understanding system behavior in production. [[Monitoring]] involves collecting metrics, logs, and traces to track system health and performance. Modern DevOps emphasizes [[Observability]]—the ability to understand internal system states from external outputs—which enables teams to diagnose issues quickly and make data-driven decisions about improvements.

**Configuration Management** ensures consistent system state across environments, while [[Containerization]] technologies like Docker and [[Container Orchestration]] platforms like Kubernetes enable consistent application packaging and deployment across development, testing, and production environments.

## Related

- [[ci-cd]] - The combined practice of continuous integration, delivery, and deployment
- [[Agile]] - Methodological foundation that shares values with DevOps
- [[Site Reliability Engineering]] - Role applying software engineering to operations
- [[Platform Engineering]] - Building internal tools and platforms for developers
- [[Infrastructure as Code]] - Managing infrastructure through code definitions
- [[Containerization]] - Packaging applications in isolated containers
- [[Container Orchestration]] - Managing containerized applications at scale
- [[Monitoring]] - Tracking system health and performance
- [[Observability]] - Understanding system behavior from outputs
- [[Configuration Management]] - Maintaining consistent system configurations
