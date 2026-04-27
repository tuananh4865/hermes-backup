---
title: "Helm"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [helm, kubernetes, packaging, deployment, devops]
---

# Helm

## Overview

Helm is the package manager for Kubernetes, enabling developers to define, install, and upgrade complex Kubernetes applications. As Kubernetes has become the standard for container orchestration, Helm has become essential for managing the complexity of deploying and maintaining applications on Kubernetes clusters. It addresses the problem of "How do I share my Kubernetes application?" by providing a standardized packaging format called Charts.

A Helm Chart is a collection of YAML templates and configuration files that describe a Kubernetes application. Charts can be versioned, distributed through repositories (similar to apt or yum repositories), and parameterized at installation time using values files. This makes it possible to use the same Chart across multiple environments—development, staging, production—by simply changing configuration values.

## Key Concepts

**Charts** are the fundamental packaging unit in Helm. A Chart is a directory containing a `Chart.yaml` file (with metadata like name and version), templates directory (Kubernetes manifests), values file (`values.yaml`), and optionally dependencies on other Charts. Charts are versioned following Semantic Versioning, allowing precise control over which version of an application is deployed.

**Releases** are instances of a Chart deployed to a Kubernetes cluster. When you run `helm install`, Helm creates a release with a unique name. You can have multiple releases of the same Chart in the same cluster, each with different configuration values. Releases are tracked by Helm and can be upgraded, rolled back, or uninstalled.

**Values Files** provide configuration that is merged into the templates at installation or upgrade time. The default `values.yaml` in a Chart provides default values, while custom values files or inline `--set` flags override defaults. Values can reference environment variables, allowing dynamic configuration based on the deployment context.

**Template Engine** uses Go's `text/template` package to generate Kubernetes manifests. Templates can include conditionals, loops, named templates (helpers), and functions for common operations. This allows a single Chart to generate different manifests based on configuration, such as creating additional resources only when certain features are enabled.

## How It Works

Helm interacts directly with the Kubernetes API server to manage resources. When you install a Chart, Helm renders the templates with the provided values and sends the resulting Kubernetes manifests to the API server for creation. Helm also tracks releases by storing release metadata in Kubernetes Secrets (in the old v2 implementation) or ConfigMaps (in v2's release storage model) within the same cluster.

```yaml
# Chart.yaml example
apiVersion: v2
name: my-application
description: A Helm chart for my web application
version: 1.2.0
appVersion: "2.0.0"
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com"
```

```bash
# Common Helm commands
helm install my-release ./my-chart           # Install a chart
helm upgrade my-release ./my-chart           # Upgrade a release
helm rollback my-release 1                   # Rollback to revision 1
helm list                                    # List all releases
helm template my-release ./my-chart          # Render templates locally
helm show values ./my-chart                  # Show default values
```

The `helm template` command is particularly useful for CI/CD pipelines, as it allows rendering templates and validating the output without actually deploying to a cluster. Tools like `helm unittest` can run tests against rendered templates.

## Practical Applications

Helm is used across industries to manage everything from simple web applications to entire platforms. Organizations maintain internal Helm repositories with Charts for their standard infrastructure components—databases, message queues, monitoring stack—which enables developers to self-service deployment without deep Kubernetes expertise.

The Helm Hub andArtifact Hub provide centralized directories for finding Charts published by the community. Popular Charts include those for Prometheus, Grafana, nginx ingress controllers, and databases like MySQL and PostgreSQL. These off-the-shelf Charts allow teams to deploy production-grade infrastructure with minimal effort.

## Examples

A team deploying a microservices application might have a parent Chart that defines common resources like ServiceAccounts and NetworkPolicies, with subcharts for each microservice. Environment-specific values files (`values-dev.yaml`, `values-prod.yaml`) configure resource limits, replica counts, and feature flags appropriately for each environment.

An SRE team maintaining a Platform-as-a-Service offering might create a private Helm repository containing Charts for each service the platform supports. End users install services by adding the repository and running `helm install` with minimal configuration, while the platform team maintains and upgrades the underlying Charts.

## Related Concepts

- [[Kubernetes]] - Container orchestration platform Helm manages
- [[Docker]] - Containerization technology often used with Helm
- [[DevOps]] - Practice that Helm enables through consistent deployments
- [[ci-cd-pipelines]] - Continuous deployment workflows using Helm
- [[Kubernetes Operators]] - Pattern for managing complex stateful applications

## Further Reading

- [Helm Documentation](https://helm.sh/docs/)
- [Artifact Hub](https://artifacthub.io/) - Repository for finding Helm Charts
- [Helm Best Practices](https://helm.sh/docs/chart_best_practices/)

## Personal Notes

Helm's templating model can be confusing at first, especially when Charts become complex with many conditionals and helpers. Starting with a working Chart and making incremental modifications is much easier than building from scratch. I recommend using `helm template` heavily during development to understand what's being generated. The transition from Helm 2 to Helm 3 (removing Tiller and improving security) was significant, so ensure your environment is using Helm 3 for new projects. Consider using Helmfile or Argo CD for managing multiple releases across environments.
