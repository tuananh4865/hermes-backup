---
title: "Access Control"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [security, authorization, access-control, identity, permissions]
---

# Access Control

## Overview

Access control is the discipline of regulating who can access what resources in a computing environment and what actions they can perform once access is granted. It is a fundamental pillar of information security, encompassing the policies, procedures, and technical mechanisms that govern authentication (proving identity) and authorization (granting permissions). Effective access control ensures that only legitimate users, processes, and systems can interact with protected assets—be they files, databases, APIs, physical spaces, or computational resources.

The field of access control addresses several fundamental questions: How do we identify entities? How do we verify their identity? What permissions should we grant? How do we enforce those permissions consistently? How do we audit access for compliance and incident response? The answers to these questions have evolved significantly over decades, from simple password systems to sophisticated zero-trust architectures that continuously verify trust at every interaction.

Access control is often conflated with [[authorization]], but they are distinct concepts. Authentication establishes identity ("who are you?"), while authorization determines permissions ("what can you do?"). Both are essential components of a complete access control system, and weakness in either compromises the entire framework.

## Key Concepts

Several foundational models and principles underpin modern access control systems. Understanding these models is essential for designing secure and maintainable access control architectures.

**Authentication Factors** classify evidence of identity into three categories: something you know (passwords, PINs), something you have (smart cards, hardware tokens), and something you are (biometrics). Multi-factor authentication (MFA) combines factors from different categories, dramatically increasing security. The strength of authentication depends not just on the factors used but also on how securely they are implemented and verified.

**Access Control Models** define the formal rules governing access decisions. The most common models include:

- **Discretionary Access Control (DAC)**: Resource owners determine who can access their resources. Common in personal operating systems, DAC offers flexibility but can lead to inconsistent policy enforcement.

- **Mandatory Access Control (MAC)**: System-wide policies enforced by a central authority. Used in government and military contexts, MAC provides strong guarantees but lacks flexibility for general enterprise use.

- **Role-Based Access Control (RBAC)**: Permissions are assigned to roles, and roles are assigned to users. This approach simplifies administration by grouping permissions logically and managing access through role membership rather than individual user accounts.

- **Attribute-Based Access Control (ABAC)**: Access decisions based on attributes of the subject (user), resource, environment, and action. ABAC provides fine-grained, policy-driven access control that can express complex rules.

## How It Works

A complete access control system involves several interacting components that work together to enforce security policies from authentication through authorization to audit.

**Identity Management** forms the foundation. User accounts are created, maintained, and eventually deprovisioned as part of the identity lifecycle. Modern identity systems often use directories (LDAP, Active Directory) or cloud identity providers (Okta, Azure AD) as centralized repositories for identity information.

**Authentication Services** verify credentials presented during login. Password-based authentication checks submitted passwords against stored hashes. Multi-factor authentication adds additional verification steps—time-based one-time passwords (TOTP), push notifications to registered devices, or biometric verification. Modern authentication supports federation protocols like SAML 2.0 and OpenID Connect that enable single sign-on across organizational boundaries.

**Policy Enforcement Points (PEPs)** intercept access requests and apply access control policies. In web applications, an authorization middleware component checks permissions before allowing access to protected routes or resources. In operating systems, the kernel enforces file permissions. In databases, row-level security and column-level security enforce access at the data layer.

**Policy Decision Points (PDPs)** evaluate access requests against defined policies and return permit or deny decisions. PDPs may consult attribute stores, role memberships, or external policy services to make decisions. The separation of PDP and PEP enables centralized policy management while distributing enforcement throughout the system.

**Audit Logging** records access decisions and attempts for security monitoring, compliance reporting, and incident investigation. Effective audit logs capture who attempted what action, on what resource, when, and the outcome (permit/deny).

## Practical Applications

Access control permeates every aspect of modern computing infrastructure, from mobile apps to cloud deployments to physical security systems.

**Cloud Resource Management** relies heavily on access control to govern access to services, APIs, and data across multi-tenant environments. Cloud providers offer identity and access management (IAM) services with fine-grained permission models. Resource-based policies, trust policies, and service control policies enable sophisticated access patterns like cross-account access and federated permissions.

**API Security** requires access control to protect backend services from unauthorized access. OAuth 2.0 with Scopes provides a standardized framework for delegating access to APIs. API keys identify calling applications, while JWT (JSON Web Tokens) carry authorization claims. Rate limiting complements authorization by preventing abuse even from legitimately authenticated clients.

**Database Access Control** enforces security at the data layer. Beyond traditional user permissions, modern databases support row-level security (RLS) that filters query results based on the caller's attributes, column-level security that restricts access to specific fields, and dynamic data masking that conceals sensitive information from unauthorized users.

**Physical Access Control** protects buildings, rooms, and equipment. Card readers, biometric scanners, and mantraps enforce physical security policies. Integration between physical and logical access control enables scenarios like badge-based computer login and automatic session termination when employees leave building areas.

## Examples

A typical RBAC implementation might define roles and permissions as follows:

```json
{
  "roles": {
    "viewer": {
      "permissions": ["read:dashboard", "read:reports"]
    },
    "analyst": {
      "permissions": ["read:dashboard", "read:reports", "export:reports"]
    },
    "admin": {
      "permissions": ["read:*", "write:*", "delete:*", "manage:users"]
    }
  },
  "userRoleMappings": {
    "alice@example.com": "analyst",
    "bob@example.com": "viewer",
    "carol@example.com": "admin"
  }
}
```

Checking authorization in application code might look like this:

```python
def check_permission(user, required_permission):
    user_role = get_user_role(user)
    role_permissions = roles[user_role]["permissions"]
    
    for perm in role_permissions:
        if perm == required_permission or perm == "*":
            return True
        # Check wildcard patterns like "read:*"
        if ":" in perm:
            action, resource = perm.split(":")
            req_action, req_resource = required_permission.split(":")
            if action == "*" and resource == req_resource:
                return True
    
    return False
```

## Related Concepts

- [[authorization]] — Permission granting and enforcement
- [[authentication]] — Identity verification
- [[rbac]] — Role-Based Access Control model
- [[abac]] — Attribute-Based Access Control model
- [[zero-trust]] — Security architecture assuming breach
- [[oauth]] — Delegated authorization framework
- [[identity-management]] — Lifecycle of digital identities

## Further Reading

- NIST SP 800-53 — Access Control frameworks and controls
- NIST SP 800-63 — Digital identity guidelines
- ISO/IEC 27001 — Information security management
- "Access Control: A Practical Implementation" by David F. Ferraiolo
- OWASP Access Control cheat sheet

## Personal Notes

Access control is one of those areas where getting the fundamentals right prevents countless security headaches. I've seen too many systems where access control was bolted on afterthought, leading to privilege escalation vulnerabilities and data breaches. My key takeaway: adopt deny-by-default permissions, implement proper separation between authentication and authorization, and always validate permissions server-side even when you've validated them client-side. Defense in depth matters.
