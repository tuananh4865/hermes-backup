---
title: Permissions
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [permissions, security, access-control, authorization]
---

# Permissions

## Overview

Permissions define the specific actions that a user, process, or system is authorized to perform within a computing environment. They represent the granular rules that govern what resources can be accessed, what operations can be executed, and what data can be viewed or modified. Permissions operate at multiple levels of the system stack—from the operating system kernel to application-level features—and serve as the primary mechanism for enforcing the principle of least privilege.

In any system where multiple actors interact with shared resources, permissions prevent unauthorized actions while enabling legitimate work. Without permissions, any compromised account or malicious process would have full access to systems and data. Permissions transform a binary all-or-nothing model into a nuanced access model where different users can access different resources based on their roles, relationships, and responsibilities.

The concept of permissions extends beyond simple allow/deny decisions. Modern permission systems handle complex scenarios including time-based restrictions (access only during business hours), contextual constraints (access only from approved network locations), approval workflows (access granted after manager approval), and delegation (users can temporarily grant access to others). These capabilities enable organizations to implement sophisticated security policies that balance protection with usability.

## Key Concepts

Understanding permissions requires grasping several interrelated concepts that form the foundation of access control.

**Subjects** are the entities that request access—typically users, but also service accounts, processes, or systems acting on behalf of users. Each subject has an identity (who they are) and attributes (what roles they hold, what groups they belong to).

**Objects** are the resources being protected—files, databases, API endpoints, infrastructure components, or application features. Objects have their own attributes, including owner, sensitivity level, and classification.

**Actions** define what can be done with objects—read, write, execute, delete, admin, or custom actions specific to particular resource types. Permissions typically map specific actions to specific objects for specific subjects.

**Access Control Models** define the rules governing how permissions are evaluated. Common models include:

- **Discretionary Access Control (DAC)** — Object owners decide who can access their objects (e.g., Unix file permissions)
- **Mandatory Access Control (MAC)** — System-wide policies enforced by the OS, based on classification levels (e.g., military clearance systems)
- **Role-Based Access Control (RBAC)** — Permissions are assigned to roles, and users are assigned to roles (e.g., "admin," "editor," "viewer")
- **Attribute-Based Access Control (ABAC)** — Decisions based on attributes of subject, object, and environment

**Privilege Escalation** occurs when a subject obtains permissions beyond those granted to them, either legitimately (vertical escalation where a user temporarily gains elevated permissions) or maliciously (exploiting vulnerabilities to gain unauthorized access).

## How It Works

Permission systems generally follow an evaluation cycle: intercept the access request, retrieve the applicable policy, evaluate against the request context, and render an allow or deny decision.

In practice, this manifests differently depending on the system. Operating systems maintain access control lists (ACLs) or capabilities that enumerate permissions per subject or object. Linux uses a combination of owner/group/other permissions with special bits for read/write/execute. Windows uses ACLs with entries specifying principal and allowed/denied actions. Application-level permissions often build on these OS primitives or implement their own models on top.

Modern applications frequently delegate authentication and authorization to external identity providers using protocols like OAuth 2.0 and OpenID Connect. In these architectures, permissions are often encoded as JWT claims or retrieved from a centralized policy engine. Policy engines like Open Policy Agent (OPA) or AWS IAM evaluate complex policies written in purpose-built languages (Rego for OPA, IAM policies for AWS).

The enforcement point varies by architecture. Some systems evaluate permissions inline during request processing; others use a sidecar or proxy that intercepts requests and validates permissions before forwarding to the target service. This separation of concerns allows policy changes without modifying application code.

## Practical Applications

Permissions are ubiquitous in modern computing. Cloud infrastructure uses permissions extensively—AWS IAM policies define what actions an IAM role can perform on which resources. Misconfigured IAM policies are a leading cause of cloud security breaches, making proper permission management critical.

Enterprise applications use permissions to implement multi-tenant isolation, ensuring customers cannot access each other's data. API gateways enforce permissions to control which clients can invoke which endpoints. Database systems use permissions to limit what queries users can execute and what tables they can access.

Mobile applications request permissions to access device capabilities—camera, location, contacts. Users grant or deny these permissions, and operating systems enforce them to protect user privacy. This pattern demonstrates permissions as a user-facing control mechanism, not just an administrative tool.

## Examples

A practical example of permissions in a web application using role-based access:

```python
from functools import wraps
from flask import abort

# Permission definitions
PERMISSIONS = {
    "admin": ["users:read", "users:write", "users:delete", "reports:read"],
    "manager": ["users:read", "users:write", "reports:read"],
    "viewer": ["users:read", "reports:read"],
}

def require_permission(permission):
    """Decorator to enforce permission requirements."""
    def decorator(f):
        @wraps(f)
        def decorated_function(user, *args, **kwargs):
            user_role = user.get("role", "viewer")
            user_permissions = PERMISSIONS.get(user_role, [])
            
            if permission not in user_permissions:
                abort(403, description="Insufficient permissions")
            
            return f(user, *args, **kwargs)
        return decorated_function
    return decorator

# Usage
@app.route("/admin/users")
@require_permission("users:write")
def manage_users(user):
    return "User management panel"
```

Kubernetes RBAC configuration example:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: production
  name: pod-reader
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: production
subjects:
- kind: User
  name: alice@example.com
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

## Related Concepts

Permissions connect to broader security and access concepts:

- [[access-control]] — The overarching discipline of controlling who can access what
- [[authorization]] — The process of determining what permissions a subject has
- [[authentication]] — The process of verifying subject identity (permissions depend on auth)
- [[zero-trust]] — Security model that never trusts and always verifies, including permissions
- [[oauth]] — Protocol for delegated authorization
- [[rbac]] — Role-Based Access Control, a common permission model
- [[security]] — The broader field of protecting systems and data
- [[identity]] — Managing who subjects are across systems

## Further Reading

- NIST SP 800-53 Security and Privacy Controls — Comprehensive permission-related controls
- Kubernetes RBAC Documentation
- OAuth 2.0 Security Best Current Practice

## Personal Notes

I've seen countless security incidents caused by overly permissive access. Early in my career, I encountered a production database that developers could access directly because "it's just for debugging." When a developer's laptop was compromised, the attacker had read access to all customer data. Permissions should be treated as critical infrastructure—designed carefully, reviewed regularly, and changed cautiously.
