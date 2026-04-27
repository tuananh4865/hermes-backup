---
title: "OAuth 2.0"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [oauth, authorization, security, api]
---

# OAuth 2.0

## Overview

OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts on third-party services. Rather than sharing passwords, OAuth allows users to grant specific permissions to applications through an authorization server, which issues access tokens that can be used to access protected resources.

The framework separates the roles of client application, authorization server, resource server, and resource owner. This delegation model is fundamental to secure API access, allowing users to authorize third-party apps without exposing their credentials.

OAuth 2.0 is widely adopted across web and mobile applications, serving as the foundation for modern authentication patterns including [[SAML]] federation, [[OpenID Connect]], and countless API authorization scenarios.

## Flows

**Authorization Code Flow** is the most secure flow for server-side applications. The user authenticates with an authorization server and grants permission, which returns an authorization code to the application. The application exchanges this code for access and refresh tokens. This flow keeps tokens away from the user agent, reducing exposure to attacks.

**Client Credentials Flow** is designed for machine-to-machine communication where the application itself is the resource owner. Instead of representing a user, the client authenticates directly with the authorization server and receives an access token scoped to its own resources. This flow is commonly used for backend services accessing APIs.

**PKCE (Proof Key for Code Exchange)** extends the authorization code flow to protect against token interception attacks, particularly important for mobile and single-page applications. It adds cryptographic challenge and verification steps that prevent attackers from exchanging stolen authorization codes.

## Use Cases

OAuth 2.0 powers common scenarios including social login (signing into apps with Google or GitHub), API authorization (third-party apps accessing user data from platforms), and delegated access (giving apps permission to perform actions on behalf of users without sharing passwords).

Single Sign-On (SSO) implementations often build on OAuth 2.0, as do enterprise identity federation systems that integrate with [[SAML]] or [[OpenID Connect]].

## Security

Key security considerations include using short-lived access tokens and secure refresh token rotation, validating all redirect URIs precisely, implementing PKCE for public clients, and using state parameters to prevent CSRF attacks.

Token storage must be secure—access tokens should be kept in memory when possible, and refresh tokens should use platform secure storage. Authorization servers should support token revocation and monitor for suspicious usage patterns.

## Related

- [[OpenID Connect]] - Identity layer built on OAuth 2.0
- [[SAML]] - Alternative federation protocol
- [[API Gateway]] - Enforcement point for OAuth tokens
- [[JWT]] - Common token format in OAuth flows
- [[scopes]] - Permission mechanisms within OAuth
