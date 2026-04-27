---
title: "OPA"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [policy, authorization, cncf, security, kubernetes]
---

# OPA (Open Policy Agent)

## Overview

Open Policy Agent (OPA) is an open-source, general-purpose policy engine that provides unified, declarative policy-as-code across the cloud-native stack. Originally developed by Styra and now a graduated Cloud Native Computing Foundation (CNCF) project, OPA enables organizations to enforce granular, context-aware policies on API requests, microservices, Kubernetes resources, and CI/CD pipelines. Instead of embedding policy logic directly into applications, developers externalize policy decisions to OPA, which evaluates incoming data against customizable rules written in Rego, OPA's purpose-built policy language. This separation of policy from application code simplifies auditing, reduces inconsistencies, and allows policy updates without recompiling or redeploying services.

## Key Concepts

**Policy-as-Code** is the foundational principle behind OPA. Policies are expressed as code in Rego, version-controlled alongside application code, and reviewed through standard development workflows. This approach replaces traditional hardcoded if-then rules or external configuration files with maintainable, testable policy definitions.

**Decentralized Policy Enforcement** means OPA can be deployed sidecar, standalone, or as a library within Go applications. This flexibility allows teams to enforce policies close to their target systems without a single point of failure or network bottleneck.

**Rego** is OPA's expressive query language designed for hierarchical document structures. Rego supports complex logic including negation, unification, and comprehension expressions, making it capable of modeling sophisticated policy scenarios.

**Sidecar Pattern** involves running OPA as a separate container alongside your main application. The application sends authorization decisions to OPA via HTTP, and OPA returns permit or deny responses based on loaded policies.

## How It Works

OPA operates on an input-document model. When an authorization request arrives—typically containing the subject (who), action (what), and resource (which)—OPA evaluates the input against loaded policy modules. The evaluation produces a boolean result or a structured object containing multiple decision outputs.

```rego
package play.http.authorization

default allow := false

allow {
    input.user.role == "admin"
}

allow {
    input.user.role == "member"
    input.method == "GET"
}
```

Policies are compiled into a bundle and pushed to OPA instances via HTTP or loaded from local files. OPA watches for policy changes and hot-reloads without restart, enabling dynamic policy updates in production environments.

## Practical Applications

OPA is widely used for Kubernetes admission control through the OPA Gatekeeper project, which integrates OPA as a ValidatingWebhookConfiguration. Teams define constraints such as "all containers must have resource limits" or "images must come from approved registries," and Gatekeeper enforces them at admission time.

In API gateways like Envoy, OPA can authorize HTTP requests based on JWT claims, query parameters, and upstream service metadata. This enables fine-grained access control without modifying application code.

For microservices, OPA centralizes authorization logic that would otherwise be scattered across dozens of services, ensuring consistent policy enforcement and simplifying compliance audits.

## Examples

A practical example: securing a REST API where only users with `viewer` role can read resources, while `editor` role is required for mutations.

```rego
package api.authz

import future.keywords.if"

default allow := false

allow if {
    input.method == "GET"
    role := input.user.roles[_]
    role in {"viewer", "editor"}
}

allow if {
    input.method in {"POST", "PUT", "DELETE"}
    role := input.user.roles[_]
    role == "editor"
}
```

## Related Concepts

- [[Kubernetes]] - Frequently used with OPA for admission control
- [[Envoy]] - Proxy that integrates with OPA for authorization
- [[Policy-as-Code]] - The broader practice OPA embodies
- [[Zero Trust Security]] - OPA supports zero trust architectures through fine-grained policy evaluation
- [[Rego]] - OPA's policy query language
