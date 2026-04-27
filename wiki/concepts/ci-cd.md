---
title: CI/CD
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [ci-cd, devops, automation, pipeline]
---

## Overview

**CI/CD** stands for Continuous Integration and Continuous Delivery (or Continuous Deployment). It is a set of automated practices that allow developers to integrate code changes frequently, validate them through automated testing, and deploy those changes to production environments with minimal manual intervention. The goal is to reduce the risk of bugs reaching production, shorten feedback cycles, and deliver software more rapidly and reliably.

**Continuous Integration (CI)** is the practice of merging all developer working copies into a shared mainline several times per day. Every merge triggers an automated build and test sequence, ensuring that new code integrates cleanly with the existing codebase. This catches integration issues early, before they compound across multiple commits. CI relies heavily on version control systems and automated build tools to maintain a consistently buildable codebase.

**Continuous Delivery (CD)** extends CI by automatically deploying every validated change to a staging or production-like environment. The deployment itself remains a manual step in traditional Continuous Delivery, giving human reviewers a gate before final release. **Continuous Deployment** goes a step further by automatically promoting every change that passes the pipeline directly to end users without human approval, assuming the pipeline has sufficiently validated the change.

Together, CI and CD form the backbone of modern [[DevOps]] practices. They enable teams to ship smaller increments more frequently, detect regressions immediately, and maintain high confidence in the health of the codebase at all times.

## Pipeline Stages

A typical CI/CD pipeline consists of several sequential stages, each designed to validate a specific aspect of the software before proceeding to the next.

**Source Stage** is the entry point where code changes are triggered. This typically occurs when a developer pushes commits to a version control system like [[Git]]. Many pipelines also support triggers based on pull requests, schedule timing, or external webhooks.

**Build Stage** compiles the source code and resolves dependencies to produce an executable artifact. If the build fails, the pipeline halts immediately, preventing broken code from advancing further. This stage ensures that the code not only parses correctly but also that all external libraries and configurations are compatible.

**Test Stage** runs automated tests against the built artifact. This typically includes unit tests that verify individual functions, integration tests that confirm components work together, and possibly end-to-end tests that simulate user workflows. A well-designed test stage provides confidence that the changes do not break existing functionality.

**Deploy Stage** promotes the validated artifact to target environments. For Continuous Delivery, this means deploying to a staging environment for final review. For Continuous Deployment, the artifact is promoted directly to production. Deployment strategies may include rolling deployments, blue-green deployments, or canary releases depending on risk tolerance and infrastructure maturity.

**Post-Deploy Stage** validates that the deployment succeeded and that the application is healthy in its new environment. This often involves smoke tests, health checks, and monitoring queries. If issues are detected, automated rollback procedures can revert the environment to the previous stable version.

## Tools

The CI/CD ecosystem offers a wide range of tools spanning self-hosted and cloud-based solutions.

**Jenkins** is one of the oldest and most widely adopted open-source automation servers. It runs in a Java-based environment and offers thousands of plugins that extend its functionality to virtually any platform and technology stack. Jenkins pipelines are defined using a domain-specific language (DSL) that can be written as code, making them version-controllable and repeatable. Because Jenkins is self-hosted, teams have full control over their infrastructure, which is important for organizations with strict security or compliance requirements.

**GitHub Actions** is a native CI/CD solution integrated directly into the GitHub platform. Workflows are defined in YAML files stored within the repository, allowing pipeline configuration to travel alongside the code. GitHub Actions supports matrix builds, reusable workflows, and a marketplace of community-contributed actions. It provides free compute minutes for public repositories and offers flexible pricing for private repos, making it accessible for both open-source projects and enterprise teams.

**GitLab CI** is part of the GitLab platform and provides a unified experience for version control, issue tracking, and continuous integration. The pipeline configuration is defined in a file called `.gitlab-ci.yml` at the repository root. GitLab CI includes Auto DevOps, which can automatically detect, build, test, and deploy applications with minimal configuration. It supports containerized executors and Kubernetes integration, enabling scalable and isolated pipeline execution.

Other notable tools include **CircleCI**, which emphasizes speed and simplicity; **Travis CI**, a long-standing hosted solution popular among open-source projects; **Bitbucket Pipelines**, which integrates with Atlassian's Bitbucket repository hosting; and **Azure DevOps Pipelines**, Microsoft's offering for enterprise teams using Azure cloud services.

## Related

- [[DevOps]] — The broader cultural and technical movement that CI/CD practices support
- [[Automation]] — The principle of automating repetitive tasks that underpins CI/CD
- [[Git]] — The version control system that typically serves as the trigger source for pipelines
- [[Docker]] — Containerization technology often used to create consistent build and deployment environments
- [[Infrastructure as Code]] — Practice of managing infrastructure through code, often integrated into CI/CD workflows
