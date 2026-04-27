---
title: "Authentication"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [authentication, security, identity, access-control]
---

# Authentication

## Overview

Authentication is the process of verifying the identity of a user, device, or system before granting access to protected resources. It answers the fundamental security question: "Who are you?" This differs from [[authorization]], which determines what an authenticated entity is permitted to do. Together, authentication and authorization form the foundation of [[access-control]] in computer systems.

In modern computing, authentication serves as the primary gatekeeper for systems ranging from simple web login forms to complex enterprise infrastructure. Effective authentication protects sensitive data, prevents unauthorized access, and maintains the integrity of digital interactions across [[web-security]] applications, APIs, mobile apps, and physical access systems. Without robust authentication mechanisms, attackers can impersonate legitimate users and exploit system vulnerabilities.

The authentication process typically involves three steps: identification (presenting an identity claim), credential presentation (providing proof of that identity), and verification (validating the credential against stored data). Strong authentication schemes separate these steps and make credential forgery computationally impractical.

## Methods

Authentication methods can be categorized by what they rely on: something you know, something you have, or something you are.

**Passwords** remain the most ubiquitous authentication method. Users provide a secret string known only to them and the system. Password strength depends on length, complexity, and uniqueness. Despite well-documented vulnerabilities like phishing and credential stuffing, passwords persist due to their simplicity and low implementation cost. Proper [[password-security]] practices include using unique passwords per service and employing password managers to handle multiple credentials.

**Biometrics** authenticate users based on unique physiological or behavioral characteristics: fingerprints, facial recognition, iris scans, voice patterns, or typing rhythm. [[Biometrics]] offer convenience without memorization but raise privacy concerns since biometric data cannot be revoked if compromised. Many systems use biometrics as a secondary factor rather than a standalone authentication method.

**Security Tokens** encompass hardware devices and software-based credentials. Hardware tokens (YubiKeys, smart cards) store cryptographic keys and perform authentication without revealing the secret. Software tokens generate time-based one-time passwords (TOTP) via authenticator apps. [[Multi-factor-authentication]] combines two or more factors—knowledge, possession, and inherence—to strengthen security beyond single-factor methods.

**Cryptographic Keys** use asymmetric or symmetric key algorithms for authentication. Public key infrastructure (PKI) enables passwordless authentication where the server verifies possession of a corresponding private key. This approach underlies modern [[web-security]] standards like WebAuthn.

## Protocols

Authentication protocols define the rules and data formats systems use to verify identity across networks.

**OAuth 2.0** is an authorization framework that enables applications to obtain limited access to user accounts on third-party services. Rather than sharing passwords, OAuth uses scoped [[JWT|access tokens]] to delegate permissions securely. It powers social login flows where users authenticate with providers like Google or Facebook. OAuth 2.0 itself does not define an authentication mechanism; it focuses on authorization delegation.

**SAML (Security Assertion Markup Language)** is an XML-based standard for exchanging authentication and authorization data between identity providers and service providers. SAML enables single sign-on (SSO) across enterprise applications, allowing users to authenticate once and access multiple services. SAML assertions contain claims about the user and are signed cryptographically to prevent tampering.

**OpenID Connect (OIDC)** builds on OAuth 2.0 to provide an authentication layer. OIDC adds an ID token that carries user identity information, along with standard OAuth access tokens. OIDC is widely used in modern web and mobile applications for federated identity management. It provides better developer experience than SAML due to its JSON-based tokens and simpler implementation.

[[JWT|JSON Web Tokens]] serve as a common token format across these protocols. JWTs are compact, URL-safe tokens that encode claims about a user and can be cryptographically signed or encrypted. They enable stateless authentication in distributed systems but require proper signature verification and expiration handling to prevent attacks.

## Related

- [[authorization]]
- [[access-control]]
- [[password-security]]
- [[biometrics]]
- [[multi-factor-authentication]]
- [[session-management]]
- [[web-security]]
- [[OAuth]]
- [[JWT]]
- [[SAML]]
- [[OpenID Connect]]
