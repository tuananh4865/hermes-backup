---
title: "Continuous Delivery"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [devops, software-engineering, deployment, automation, ci-cd, release-management]
---

# Continuous Delivery

## Overview

Continuous Delivery (CD) is a software engineering approach in which code changes are automatically prepared, tested, and packaged for release to production — not deployed immediately, but kept perpetually in a deployable state. The defining characteristic is that the path from a developer committing code to a user accessing it is fully automated and每天都可重复的. The decision to deploy is a business or operational choice made by a human; the engineering pipeline ensures that deployment is safe, fast, and low-risk whenever that decision is made.

CD extends Continuous Integration (CI), which automates the build and test process on every commit. While CI focuses on verifying that new code integrates correctly with the existing codebase, CD focuses on everything that happens after: staging environments, load testing, security scanning, database migrations, configuration management, and the final promotion to production. The goal is a software supply chain that is as automated, reliable, and boring as a manufacturing assembly line.

The concept was popularized by Jez Humble and David Farley's book *Continuous Delivery* (2010) and is now a foundational practice of modern [[DevOps]] engineering.

## Key Concepts

**Pipeline as Code**: The deployment pipeline itself is version-controlled alongside application code. Tools like [[Jenkins]], GitHub Actions, GitLab CI, and ArgoCD define pipelines in YAML or domain-specific languages. This means pipeline changes go through the same review process as application changes and can be rolled back if they cause problems.

**Immutable Artifacts**: Once a build passes all stages, the resulting artifact (a Docker image, a JAR file, a compiled binary) is never modified. It is tagged with a unique identifier (commit SHA, build number) and promoted through environments unchanged. This immutability ensures that what runs in production is exactly what was tested in staging.

**Feature Toggles (Feature Flags)**: CD enables a practice where new code is deployed but disabled via a flag. The feature is "shipping" the code to production continuously, but its activation is controlled independently of deployment. This decouples release from deployment, allowing dark launches, A/B testing, and instant rollbacks without redeployment.

**Database Migrations**: CD pipelines must handle schema changes carefully. Practices like forward-only migrations, expand-contract patterns for backwards-compatible database changes, and blue-green database migrations ensure that database changes don't break running applications or require coordinated downtime.

**The DORA Metrics**: DevOps Research and Assessment (DORA) program identifies four key metrics for measuring CD success: deployment frequency, lead time for changes, change failure rate, and mean time to recovery (MTTR). High-performing organizations deploy multiple times per day with low failure rates and fast recovery.

## How It Works

A typical CD pipeline proceeds through stages:

1. **Commit**: Developer pushes code to a version control branch.
2. **Build & Unit Test**: CI system compiles the code and runs unit tests.
3. **Integration Test**: Code is deployed to an integration environment for broader testing.
4. **Performance Test**: Load or stress testing against production-like infrastructure.
5. **Security Scan**: SAST, DAST, dependency scanning, container scanning.
6. **Staging / UAT**: Manual testing or automated acceptance tests in a production-equivalent environment.
7. **Artifact Promotion**: The immutable artifact is promoted to the production registry.
8. **Production Deployment**: A human or automated process triggers the actual deployment.

```yaml
# Example: GitHub Actions CD pipeline
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci
      - run: npm test
      - run: npm run build

  deploy-staging:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/deploy.sh staging
      - run: ./scripts/smoke-test.sh staging

  deploy-production:
    needs: deploy-staging
    environment: production
    runs-on: ubuntu-latest
    steps:
      - run: ./scripts/deploy.sh production
      - run: ./scripts/smoke-test.sh production
```

## Practical Applications

Web applications and SaaS platforms are the canonical CD use case. Teams at companies like Amazon, Netflix, and Etsy deploy dozens or hundreds of times per day, treating each deployment as a low-risk, routine event rather than a major production change. [[Netflix]] pioneered this with their CI/CD culture and tooling (including Spinnaker for multi-region deployments and chaos engineering to build confidence in resilience).

Mobile applications face the additional constraint of app store review cycles, which create a partial exception to pure CD. However, the server-side components of mobile apps — APIs, backend services — are fully CD-eligible and typically deploy continuously.

Infrastructure as Code (IaC) with [[Terraform]] or Pulumi extends CD to infrastructure: pipeline changes provision, update, or destroy cloud resources with the same automation and safety checks as application code.

## Examples

**Netflix's deployment philosophy**: Every code change is a candidate for production. The pipeline automatically deploys to a small percentage of production traffic (canary deployment), monitors error rates and latency, and either auto-promotes or auto-rolls back based on metrics. Engineers have deployment authority 24/7 and can ship at any time without manual approval gates.

**GitOps workflow**: A specific CD pattern where the Git repository is the single source of truth for desired infrastructure and application state. Tools like ArgoCD or FluxCD watch the repository and automatically sync the cluster to match it. A production deployment is simply a merge to the `main` branch.

**Blue-Green Deployment**: Two identical production environments (blue and green) run in parallel. Traffic routes to one (say, blue). The new version is deployed to green, validated, and then traffic is atomically switched to green. If problems emerge, traffic switches back to blue instantly — providing an instant rollback mechanism with zero downtime.

## Related Concepts

- [[DevOps]] — The cultural and organizational framework CD operates within
- [[Continuous Integration]] — CI, the prerequisite practice that feeds into CD
- [[GitHub Actions]] — Popular CI/CD tool for automating pipelines
- [[Docker]] — Container technology that enables consistent artifact promotion across environments
- [[Kubernetes]] — Container orchestration platform commonly paired with CD tools like ArgoCD
- [[Jenkins]] — Widely used open-source CI/CD automation server

## Further Reading

- *Continuous Delivery* by Jez Humble and David Farley — The definitive book on the subject
- [DORA State of DevOps Report](https://dora.dev/research/2023/dora-report/) — Annual data on CD performance and practices
- [ArgoCD Documentation](https://argo-cd.readthedocs.io/) — GitOps CD for Kubernetes
- [Spinnaker](https://spinnaker.io/) — Multi-cloud CD platform used at Netflix and others

## Personal Notes

The biggest mindset shift CD requires is treating deployment as a non-event. In organizations without CD, deployments are scary — they require freeze periods, change advisory boards, and careful scheduling because the process is manual and error-prone. CD makes deployment cheap and reversible, which paradoxically makes it safer: you deploy small changes frequently, find problems immediately, and roll back in minutes. The pipeline does the tedious work of consistency that humans are bad at. The metric I watch most is lead time for changes — if it is measured in days or weeks, the team is not getting the full benefit of CD, regardless of how many tests run in the pipeline.
