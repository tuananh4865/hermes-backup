---
title: "Argo CD"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [gitops, kubernetes, continuous-delivery, declarative-deployments]
---

# Argo CD

Argo CD is a declarative, GitOps-based continuous delivery tool for Kubernetes that continuously monitors Git repositories and automatically synchronizes application state to cluster state. It follows the GitOps principle where the desired state of applications is stored in Git, and Argo CD ensures the actual cluster state matches the desired state defined in the repository.

## Overview

Argo CD is a Kubernetes-native continuous deployment tool that implements GitOps methodology using a pull-based deployment pattern. Unlike traditional push-based CI/CD pipelines that directly deploy code to clusters, Argo CD monitors Git repositories and pulls changes when detected, comparing the desired state in Git against the live state running in Kubernetes. This approach provides a single source of truth for infrastructure and application configuration, enabling audit trails, rollback capabilities, and reduced blast radius for deployments.

As a core component of the Argo ecosystem (which includes Argo Workflows, Argo Rollouts, and Argo Events), Argo CD has become a foundational tool for organizations adopting cloud-native practices and Kubernetes at scale.

## Key Concepts

**Application**: The core resource in Argo CD, an Application represents a deployed instance of a microservice or application. It defines the source (Git repo + path), destination (target cluster), and sync policy.

**Application Controller**: The Kubernetes controller that continuously reconciles the desired state (from Git) with the actual state (running in cluster), detecting and reporting drift.

**Sync Policy**: Determines how Argo CD responds when drift is detected. Options include automated sync (auto-deploy) or manual sync (requires approval via UI or CLI).

**Rollback**: Argo CD maintains a history of deployed revisions, allowing instant rollback to any previous known-good state by re-syncing an older Git commit.

**Health Assessment**: Argo CD can perform custom health checks for Kubernetes resources, ensuring applications are truly healthy after deployment, not just present.

## How It Works

Argo CD operates through a control loop that continuously monitors and reconciles state:

1. **Repository Registration**: Users register a Git repository containing application manifests (YAML, Helm, Kustomize, etc.) with Argo CD.

2. **Application Creation**: An Application resource is created, specifying the repo URL, revision, path to manifests, and target cluster/namespace.

3. **Controller Reconciliation**: The Application Controller watches all Application resources. Every 3 minutes (configurable), it compares the desired state from Git against the live state in the target cluster.

4. **Drift Detection**: If differences are found, Argo CD marks the application as "OutOfSync" and can optionally trigger automated synchronization.

5. **Sync Execution**: During sync, Argo CD applies, creates, or updates Kubernetes resources as needed to match Git state. It respects resource dependencies and ordering.

6. **Status Reporting**: All application states are visible in the Argo CD UI, CLI, and Kubernetes custom resources, providing real-time visibility into deployment status.

```yaml
# Example Argo CD Application resource
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example/app.git
    targetRevision: main
    path: manifests/
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## Practical Applications

- **Microservices Deployment**: Manage dozens to hundreds of microservices across multiple environments with consistent deployment patterns and standardized workflows.

- **Multi-Environment Promotion**: Promote applications through dev → staging → production environments with Git-based audit trails and controlled rollouts.

- **Infrastructure Synchronization**: Keep infrastructure-as-code manifests synchronized with running cluster state, ensuring compliance and consistency.

- **Disaster Recovery**: Use Git as the source of truth for instant recovery—re-sync to any previous known-good state in minutes.

- **Multi-Tenant Platforms**: Build internal developer platforms where teams manage their own applications while platform teams maintain standards.

## Examples

**Creating an Application via CLI**:
```bash
argocd app create my-app \
  --repo https://github.com/example/app.git \
  --path manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace production \
  --sync-policy automated
```

**Syncing and Rolling Back**:
```bash
# Manual sync
argocd app sync my-app

# View deployment history
argocd app history my-app

# Rollback to previous revision
argocd app rollback my-app
```

## Related Concepts

- [[GitOps]] — The underlying methodology that Argo CD implements
- [[Kubernetes]] — The container orchestration platform Argo CD targets
- [[Continuous Delivery]] — The practice Argo CD enables for Kubernetes
- [[Helm]] — A package manager often used with Argo CD for templating manifests
- [[Argo Workflows]] — Workflow engine for CI/CD pipelines in the Argo ecosystem
- [[Infrastructure as Code]] — The practice of managing infrastructure through version-controlled files

## Further Reading

- [Argo CD Official Documentation](https://argo-cd.readthedocs.io/)
- [Argo Project Website](https://argoproj.github.io/)
- [GitOps Engine Deep Dive](https://github.com/argoproj/gitops-engine)

## Personal Notes

Argo CD has transformed how teams approach Kubernetes deployments. The shift from imperative scripts to declarative application definitions stored in Git provides incredible benefits for auditability and reproducibility. When starting with Argo CD, begin with manual sync policies to understand the flow before enabling automation. The health assessment feature is particularly valuable for stateful applications where simply having pods running doesn't mean the application is truly operational.
