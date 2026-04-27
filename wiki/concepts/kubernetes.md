---
title: Kubernetes
description: Open-source container orchestration platform for automating deployment, scaling, and management of containerized applications. Kubernetes v1.35 (2026) with Cilium eBPF networking.
tags:
  - infrastructure
  - devops
  - containers
  - orchestration
  - cloud-native
created: 2026-04-20
---

# Kubernetes

Kubernetes (K8s) is an open-source container orchestration platform that automates deployment, scaling, and management of containerized applications. Originally developed by Google, it is now maintained by the Cloud Native Computing Foundation (CNCF).

## Kubernetes v1.35 (2026)

The latest stable release as of 2026 is **Kubernetes v1.35** (patch 1.35.2 released February 2026). Key features:

### Breaking Changes

- **Automated cgroup driver detection** — No longer requires manual specification of container runtime cgroup driver
- **exec plugin versioned z-pages** — Enhanced debugging capabilities for exec plugins
- **containerd 1.7+ required** — Older containerd versions deprecated

### New Features

| Feature | Description |
|---------|-------------|
| **Device Manager GA** | General availability of device plugin framework for hardware acceleration |
| **exec plugin security** | Restricting executables invoked by kubeconfigs via exec plugin authentication |
| **Enhanced eBPF support** | Improved observability and security with versioned z-pages APIs |

## Kubernetes Networking in 2026

### Cilium eBPF — The New Standard

Cilium has emerged as the leading Kubernetes networking layer in 2026, replacing kube-proxy with eBPF-based packet processing:

**Performance gains:**
- **10x increase** in network throughput vs kube-proxy
- **40% reduction** in network latency
- Direct packet processing in Linux kernel via eBPF
- Built-in mTLS (mutual TLS) via eBPF and ztunnel sidecar

### Why Teams Are Switching to Cilium

```yaml
# CiliumClusterwideEnvoyConfig - enable eBPF kube-proxy replacement
apiVersion: cilium.io/v2
kind: CiliumClusterwideEnvoyConfig
metadata:
  name: enable-kube-proxy-replacement
spec:
  # Replaces kube-proxy with eBPF
  # Enables native routing
```

Benefits:
1. **Simpler architecture** — No iptables rules, direct eBPF maps
2. **Better scalability** — O(1) lookup vs O(n) iptables for large clusters
3. **Encryption built-in** — WireGuard or IPSec for pod-to-pod encryption
4. **Observability** — Hubble for per-flow visibility

### KubeCon EU 2026 Highlights

At KubeCon EU 2026, key themes included:
- **BSD integration** via Lima and urunc for running Linux containers on BSD hosts
- **Cilium maturity** — production-hardened at massive scale
- **AI/ML workloads** — Kubernetes as the backbone for distributed training
- **GitOps everywhere** — Flux and ArgoCD as standard deployment patterns

## Core Concepts

### Pods

The smallest deployable unit in Kubernetes:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ai-inference-pod
spec:
  containers:
  - name: llama-serve
    image: ollama/ollama:latest
    resources:
      limits:
        nvidia.com/gpu: 1
        memory: "16Gi"
    ports:
    - containerPort: 11434
```

### Deployments

Manage replica sets of pods with rolling updates:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-backend
  template:
    spec:
      containers:
      - name: backend
        image: my-registry/agent-backend:v2
        env:
        - name: OLLAMA_HOST
          value: "http://ollama-service:11434"
```

### Services

Stable network endpoints for pods:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
spec:
  selector:
    app: ollama
  ports:
  - port: 80
    targetPort: 11434
  type: ClusterIP
```

### Ingress

HTTP/HTTPS routing for external access:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: agent-ingress
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  rules:
  - host: api.agent.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: agent-backend
            port:
              number: 80
```

## AI/ML Workloads on Kubernetes

### Running Ollama at Scale

```yaml
# Ollama as a Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
spec:
  replicas: 2
  template:
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        env:
        - name: OLLAMA_HOST
          value: "0.0.0.0"
        resources:
          requests:
            memory: "32Gi"
            cpu: "4"
          limits:
            memory: "64Gi"
            cpu: "8"
        volumeMounts:
        - name: models
          mountPath: /root/.ollama/models
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models
```

### GPU Scheduling

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: llm-inference
spec:
  containers:
  - name: inference
    image: nvcr.io/nvidia/pytorch:latest
    resources:
      limits:
        nvidia.com/gpu: "2"  # Request 2 GPUs
```

### Serving Multiple Models

For running multiple LLM models simultaneously:

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: model-config
data:
  MODELS: "llama3.2:3b,mistral:7b,phi:latest"
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: multi-model-server
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        env:
        - name: OLLAMA_MODELS
          valueFrom:
            configMapKeyRef:
              name: model-config
              key: MODELS
```

## GitOps with ArgoCD

### Application Definition

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: agent-production
  namespace: argocd
spec:
  project: default
  source:
    repoURL: git@github.com:org/agent-k8s.git
    targetRevision: HEAD
    path: production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

## YAML Hell — The 2026 Solution

The notorious "YAML hell" of Kubernetes has improved with:

1. **Helm 4** — Improved templating with JSON Schema validation
2. **CDK8s** — Define Kubernetes configs in TypeScript/Python
3. **Kustomize** — Overlay-based configuration without templating
4. **Crossplane** — Kubernetes-native infrastructure provisioning
5. **GitOps automation** — ArgoCD/Flux reduce manual apply

```yaml
# Kustomize overlay example
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- deployment.yaml
- service.yaml
patches:
- path: production-patch.yaml
  target:
    kind: Deployment
```

## See Also

- [[cilium]] — eBPF-based Kubernetes networking
- [[devops]] — Development operations practices
- [[containerization]] — Container fundamentals
- [[gitops]] — Git-based deployment automation
- [[ai-agent]] — AI agents that run on Kubernetes infrastructure
