---
title: Authorization
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [authorization, security, access-control, permissions]
---

# Authorization

## Overview

Authorization is the process of determining what actions a user or system is permitted to perform after their identity has been established through authentication. While authentication answers "who are you?", authorization determines "what can you do?" This fundamental separation of concerns is critical for building secure systems—authentication can verify identity rigorously, but without proper authorization controls, that identity grants access to everything.

Modern authorization systems implement fine-grained permissions that specify exactly which resources can be accessed and what operations are permitted. These systems must balance security with usability, providing enough flexibility to support complex organizational structures while remaining simple enough to audit and administer without error.

## Key Concepts

**Access Control Models**

Several canonical models structure authorization decisions. Role-Based Access Control (RBAC) assigns permissions to roles, which are then assigned to users. This simplifies administration by grouping permissions logically. Attribute-Based Access Control (ABAC) makes decisions based on attributes of the subject, resource, and environment, providing finer granularity. The principle of least privilege dictates that users should receive only the minimum permissions necessary to perform their tasks.

**Permission Hierarchy**

Permissions often form hierarchies reflecting organizational structure. A "team lead" role might include all permissions of "developer" plus additional management capabilities. Permission inheritance reduces administration burden but requires careful design to avoid unintended access grants.

**Deny-First Design**

Modern authorization systems typically evaluate deny rules before permit rules. This "deny-first" approach ensures that explicit restrictions are never overridden by broad permissive rules, improving security posture.

**Separation of Duties**

Critical operations may require multiple authorized users to approve. This prevents single points of compromise and creates accountability through shared responsibility.

## How It Works

Authorization typically operates as middleware or a service that intercepts requests and evaluates them against policy. The evaluation considers the authenticated identity, requested resource, intended action, and contextual factors like time or location.

Policy engines store authorization rules and evaluate incoming access requests. Some use formal policy languages like XACML or Rego (for Open Policy Agent), while others use simpler rule sets or attribute comparisons.

When access is denied, the system returns a structured error indicating the denial without revealing why whenever possible—information disclosure about why authorization failed could aid attackers in privilege escalation.

## Practical Applications

**API Gateways**

API gateways enforce authorization for all API traffic. They validate that the presented credentials (API keys, JWTs, OAuth tokens) authorize the requested operation before forwarding requests to backend services.

**Microservices Security**

In microservices architectures, each service typically handles its own authorization using shared policy definitions. Service mesh implementations like Istio can centralize authorization enforcement, applying consistent policies across all service-to-service communication.

**Data Platform Access**

Data warehouses and data lakes use authorization to control which users can query which datasets. Column-level and row-level security extends this to finer granularity, ensuring users only see data relevant to their role.

**Cloud Resource Management**

Cloud platforms (AWS IAM, Azure RBAC, GCP IAM) implement authorization for all cloud resources. Proper IAM configuration is critical for cloud security, preventing both external attacks and internal privilege abuse.

## Examples

```json
// Example RBAC policy structure
{
  "roles": {
    "editor": {
      "permissions": ["document:read", "document:write", "document:publish"],
      "members": ["user-123", "user-456"]
    },
    "admin": {
      "permissions": ["document:*", "user:manage"],
      "inherits": ["editor"]
    }
  }
}
```

```rego
# Open Policy Agent Rego example
package authz

default allow = false

allow {
    input.user.role == "admin"
}

allow {
    input.user.role == "editor"
    input.resource.owner == input.user.id
}

allow {
    input.method == "GET"
    input.resource.type == "public"
}
```

```python
# Simple authorization check
def authorize(user, resource, action):
    if user.role == "admin":
        return True  # Admins can do anything
    
    if user.role == "editor" and action in ["read", "write"]:
        return resource.project in user.assigned_projects
    
    if action == "read" and resource.visibility == "public":
        return True
    
    return False
```

## Related Concepts

- [[authentication]] — Identity verification (precedes authorization)
- [[access-control]] — Broader access control mechanisms
- [[RBAC]] — Role-based access control
- [[ABAC]] — Attribute-based access control
- [[OAuth-2.0]] — Delegation protocol that includes authorization
- [[web-security]] — Security context for web applications

## Further Reading

- [NIST RBAC](https://csrc.nist.gov/projects/role-based-access-control) — RBAC standards
- [Open Policy Agent](https://www.openpolicyagent.org/) — Policy engine for cloud-native authorization
- [OWASP Authorization](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authorization_Testing/) — Authorization testing guide

## Personal Notes

Authorization is where most security breaches happen—not from weak authentication, but from poorly designed authorization. I always recommend implementing authorization at multiple layers (gateway, service, data) with deny-first evaluation. The blast radius of a single misconfiguration is much smaller.
