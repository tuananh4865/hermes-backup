---
title: OAuth2
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [oauth2, authentication, authorization, security]
---

# OAuth2

## Overview

OAuth 2.0, defined in RFC 6749, is an authorization framework that enables third-party applications to obtain limited access to user resources on another service. Rather than sharing a user's credentials directly with a client application, OAuth 2.0 allows a resource owner to delegate specific permissions to a client through a trusted authorization server. This delegation model forms the foundation of modern API security and is the mechanism behind "Login with Google," "Connect with Facebook," and similar identity federation patterns.

The framework operates through a set of defined roles: the **resource owner** (the user), **client** (the third-party application requesting access), **authorization server** (the server that authenticates the user and issues tokens), and **resource server** (the API or service holding the protected resources). The client never handles user passwords after the initial authorization handshake. Instead, it receives an **access token** — a scoped credential that grants specific, time-limited permissions defined by the resource owner.

OAuth 2.0 focuses exclusively on authorization — determining what a client is allowed to do — and intentionally does not address authentication (verifying who a user is). This separation is deliberate and led to the development of [[OpenID Connect]] as a thin identity layer built on top of OAuth 2.0.

## Flows

OAuth 2.0 defines several authorization flows, each suited to different client types and security environments.

**Authorization Code Flow** is the most secure and widely recommended flow for server-side applications. The process begins when the client redirects the user to the authorization server with a request that includes its client ID, requested scope, and a redirect URI. After the user authenticates and grants permission, the authorization server redirects back with a short-lived **authorization code**. The client then exchanges this code with the authorization server (using its client secret) to receive an access token and optionally a refresh token. This flow keeps tokens away from the browser, reducing exposure to interception.

**Client Credentials Flow** is used for machine-to-machine communication where the client itself is the resource owner. There is no user involvement. The client authenticates directly with the authorization server using its client ID and secret, and receives an access token representing the client's own permissions rather than delegated user access. This flow is appropriate for background services, daemons, or microservices that need to access APIs on behalf of themselves.

**PKCE (Proof Key for Code Exchange)** is an extension to the Authorization Code Flow designed for public clients — notably mobile apps and single-page applications — that cannot securely store a client secret. PKCE adds a dynamically generated cryptographically random string called a **code verifier**, which is hashed into a **code challenge** and sent with the initial authorization request. When the client later exchanges the authorization code for tokens, it must present the original code verifier, which the authorization server validates against the stored challenge. This prevents authorization code interception attacks that are especially dangerous in environments where client secrets cannot be protected.

## OpenID Connect

[[OpenID Connect]] (OIDC) is an identity layer built on top of OAuth 2.0, adding standardized authentication. While OAuth 2.0 tells a client what resources a user has authorized access to, OIDC tells the client **who the user is**. OIDC introduces the **ID token**, a JSON Web Token (JWT) containing claims about the authenticated user such as their subject identifier, email, name, and authentication timestamp.

In technical terms, OIDC reuses the OAuth 2.0 Authorization Code and PKCE flows but adds an `openid` scope to the authorization request. The response includes both an access token (for API authorization) and an ID token (for identity verification). OIDC also standardizes the **UserInfo endpoint**, an API that returns additional user profile information when called with the access token.

The key distinction is that OAuth 2.0 answers "what can this application access on behalf of this user?" while OIDC answers "who is this user and was they authenticated?" Many applications use both: OIDC for user authentication (login) and OAuth 2.0 for API authorization (what data the logged-in user can access).

## Related

- [[OpenID Connect]] - Identity layer built on OAuth 2.0 for user authentication
- [[SAML]] - Older XML-based authentication and authorization protocol
- [[JWT]] - JSON Web Token format used for OAuth 2.0 access tokens and OIDC ID tokens
- [[API Security]] - Broader discipline of protecting application programming interfaces
- [[Token-based Authentication]] - Authentication pattern where credentials are exchanged for tokens
- [[SSO]] - Single Sign-On, often implemented using OAuth 2.0 or OIDC
