---
title: "Deployment"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [devops, deployment, cicd]
---

# Deployment

## Overview

Deployment in software development refers to the process of making a software application or update available for use in a production environment. It encompasses all activities that move software from a development or staging environment to a live system where end users can access it. This process includes preparing the application, configuring servers, databases, and networking, and ensuring that the deployed version functions correctly without disrupting existing services.

Effective deployment practices are critical for maintaining system reliability, minimizing downtime, and delivering new features to users quickly. Modern deployment approaches emphasize automation, traceability, and risk reduction. The goal is to make releases routine, low-risk events that can be performed frequently without impacting user experience.

## Strategies

Several deployment strategies help organizations manage the risks associated with releasing new software versions.

**Blue-Green Deployment** maintains two identical production environments, called blue and green. At any time, one environment serves live traffic while the other remains idle. When deploying a new version, it is released to the idle environment, tested thoroughly, and then the router is switched to direct all traffic to the updated environment. If issues arise, rolling back is instantaneous—just switch traffic back to the original environment.

**Canary Deployment** releases a new version to a small subset of users or servers before rolling it out to the entire infrastructure. This strategy allows teams to monitor real-world performance and catch issues that might not appear in testing. Traffic is gradually shifted to the new version, with most requests still handled by the stable release. If the canary version performs well, it progressively receives more traffic until it completely replaces the old version.

**Rolling Deployment** incrementally replaces instances of the old version with the new one. Instead of taking the entire system down, pods or servers are updated in batches. The old and new versions coexist temporarily, ensuring continuous availability. This approach is common in Kubernetes environments where services are deployed as sets of replicas.

**Infrastructure as Code (IaC)** treats infrastructure configuration as software code that can be versioned, reviewed, and automated. Tools like Terraform, Ansible, and Pulumi allow teams to define servers, networks, and cloud resources in declarative configuration files. IaC ensures consistent, repeatable deployments and reduces human error in environment setup.

## CI/CD

Deployment is tightly integrated with Continuous Integration and Continuous Deployment (CI/CD) pipelines. CI/CD automates the build, test, and release process, enabling frequent and reliable deployments. A typical pipeline includes stages for compiling code, running unit and integration tests, building container images, and deploying to target environments.

Integration with deployment strategies often occurs in the final stages of a CI/CD pipeline. After successful testing, the pipeline may trigger a blue-green switch, orchestrate a canary rollout, or execute rolling updates. Pipeline tools like Jenkins, GitLab CI, CircleCI, and Argo CD support these strategies natively or through plugins.

Infrastructure provisioning can also be incorporated into CI/CD workflows, especially when using IaC tools. Changes to infrastructure code go through code review and automated testing before being applied to production environments. This creates a unified process for deploying both application code and underlying infrastructure.

## Related

- [[CI-CD]] — Continuous Integration and Continuous Deployment pipelines
- [[Infrastructure-as-Code]] — Managing infrastructure through code
- [[Kubernetes]] — Container orchestration platform commonly used for rolling deployments
- [[Blue-Green-Deployment]] — Dual-environment deployment strategy
- [[Canary-Deployment]] — Gradual rollout strategy for new versions
