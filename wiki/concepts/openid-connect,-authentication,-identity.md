---
title: "OpenID Connect, Authentication, Identity"
created: 2026-04-13
updated: 2026-04-20
type: concept
tags: [authentication, identity, oauth2, security, sso]
sources: [https://openid.net/connect/, https://datatracker.ietf.org/doc/html/rfc6749, https://datatracker.ietf.org/doc/html/rfc7519]
---

# OpenID Connect, Authentication, Identity

> This page was expanded from a stub with real content on OpenID Connect.

## Overview

OpenID Connect (OIDC) is an identity layer built on top of the OAuth 2.0 authorization protocol. It enables third-party authentication — allowing users to authenticate to one service using credentials they already have with another service (like Google or Microsoft) without sharing the actual password. OIDC provides a standardized way to verify user identity and obtain basic profile information, making it the dominant standard for modern web application authentication and single sign-on (SSO).

OIDC emerged from the OAuth 2.0 ecosystem to address a fundamental gap: OAuth 2.0 was designed for authorization (granting access to resources), not authentication (verifying who a user is). While OAuth 2.0 can be bent to handle login, it wasn't designed for it. OpenID Connect added the identity layer that makes OAuth 2.0 useful for authentication scenarios, producing a protocol that both confirms user identity and can grant access to user data.

## OAuth 2.0 Foundation

Understanding OIDC requires understanding OAuth 2.0, as OIDC is fundamentally an extension of OAuth 2.0 with additional identity-specific components.

OAuth 2.0 operates through a system of authorization grants (flow types) that allow users to grant applications access to their resources without sharing credentials. The core grant types include:

- **Authorization Code Grant**: A multi-step flow where the user authenticates with the authorization server, receives an authorization code (not an access token directly), and then exchanges that code for tokens. This is the most secure flow for server-side applications.
- **Client Credentials Grant**: Used for machine-to-machine communication where the client application is also the resource owner. No user involvement.
- **Refresh Token Grant**: Allows clients to obtain new access tokens without re-authenticating the user, using a previously issued refresh token.

OAuth 2.0 introduces four key roles:

1. **Resource Owner**: The user who owns the data or can grant access to it.
2. **Client**: The application requesting access to resources.
3. **Authorization Server**: The server that authenticates the resource owner and issues access tokens.
4. **Resource Server**: The server hosting the protected resources, validating access tokens.

In OAuth 2.0 alone, the authorization server returns an access token that grants access to resources. However, nothing in OAuth 2.0 itself tells the client who the user is — the access token is opaque to the client. OpenID Connect solves this by adding an identity layer on top of OAuth 2.0.

## OpenID Connect Flow Types

OIDC builds on OAuth 2.0 authorization code flow and introduces an ID token alongside access tokens. It supports two primary flows for user authentication:

### Authorization Code Flow

The recommended flow for most applications, providing the highest security:

1. The client redirects the user to the authorization server's login page
2. User authenticates (credentials verified by the authorization server)
3. User consents to the requested permissions (scopes)
4. Authorization server redirects back to the client with an authorization code
5. Client exchanges the code for tokens (access token + ID token + optionally refresh token)
6. Client validates the ID token and extracts user identity information

This flow keeps tokens away from the browser, making it suitable for server-side applications and modern SPAs using backend-for-frontend patterns.

### Implicit Flow

Historically used for client-side applications (JavaScript SPAs), implicit flow was designed for scenarios where keeping a client secret is not possible. However, implicit flow has been deprecated in OAuth 2.1 and should no longer be used. The authorization code flow with PKCE (Proof Key for Code Exchange) is now recommended for all public clients.

### Hybrid Flow

Combines aspects of authorization code and implicit flows, returning some tokens on the authorization endpoint and others on the token endpoint. Used in some scenarios with OIDC, though less common.

## ID Tokens vs Access Tokens

A critical distinction in OIDC is between ID tokens and access tokens:

**ID Token** is a JSON Web Token (JWT) that represents the authentication event. It contains claims about the authenticated user — who they are, when they authenticated, which audience it's intended for. The ID token is meant to be read by the application (the Relying Party) to establish the user's identity.

Key claims in an ID token include:
- `iss`: The issuer identifier (the authorization server)
- `sub`: The subject identifier (unique to that user at that issuer)
- `aud`: The audience (must include the client's `client_id`)
- `exp`: Expiration timestamp
- `iat`: Issued-at timestamp
- `nonce`: A random value to prevent replay attacks

**Access Token** is an OAuth 2.0 token that grants access to protected resources (APIs). In OIDC, access tokens are typically opaque to the client when calling userinfo endpoints, but may be JWTs when calling resource servers. The access token is not meant to convey identity — it's an authorization artifact.

**Refresh Token** allows obtaining new access tokens without re-authenticating the user, enabling long-lived sessions without requiring the user to log in repeatedly.

## Claims and Scopes

OIDC defines standardized scopes that map to specific sets of claims:

- `openid`: The minimal required scope for any OIDC authentication. Without this scope, the request is standard OAuth 2.0, not OIDC.
- `profile`: Grants access to basic user profile claims: `name`, `family_name`, `given_name`, `middle_name`, `nickname`, `preferred_username`, `profile`, `picture`, `website`, `gender`, `birthdate`, `zoneinfo`, `locale`, `updated_at`.
- `email`: Grants access to `email` and `email_verified` claims.
- `phone`: Grants access to `phone_number` and `phone_number_verified` claims.
- `address`: Grants access to `address` claim containing a structured address object.
- `offline_access`: Request a refresh token for long-lived sessions.

The `sub` (subject) claim is the only required claim in every ID token. It serves as the unique identifier for the user at that particular issuer. The same user at different OIDC providers will have different `sub` values.

Claims can be requested selectively — an application that only needs the user's email doesn't need to request the full `profile` scope. This follows the principle of minimum necessary data collection.

## Key OIDC Providers

Several major identity providers implement OIDC, making it easy to add authentication to applications:

### Google Identity Platform

Google's OIDC implementation at accounts.google.com is widely used. It supports standard OIDC flows and provides userinfo endpoints. Google is often used as the identity provider in consumer applications and increasingly in enterprise scenarios through Google Workspace.

### Microsoft Entra ID (Azure AD)

Microsoft's cloud identity platform supports OIDC for authentication to Microsoft 365, Azure resources, and custom applications. Microsoft's implementation includes support for work and school accounts, as well as Microsoft personal accounts. It integrates deeply with the Microsoft ecosystem and supports advanced enterprise features like conditional access policies.

### Auth0

Auth0 (now part of Okta) provides a flexible identity platform that supports OIDC for all types of applications. It offers extensive customization options, supports hundreds of social providers, and provides features like anomaly detection, attack protection, and universal login. Auth0 is popular for B2C, B2B, and SaaS applications.

### Okta

Okta's identity platform provides OIDC support as part of a comprehensive IAM (Identity and Access Management) solution. It offers both cloud and on-premises deployment options, making it suitable for regulated industries. Okta integrates with thousands of applications and supports advanced enterprise requirements.

### Other Notable Providers

- **Keycloak**: Open-source identity provider by Red Hat, suitable for self-hosted scenarios
- **IdentityServer**: .NET-based open-source OIDC provider
- **FusionAuth**: Open-source auth platform with OIDC support
- **AWS Cognito**: Amazon's identity service with OIDC support

## OIDC for AI Agent Authentication

As AI agents become more prevalent, authentication patterns for agents represent an emerging use case for OIDC. AI agents often need to authenticate to APIs and services on behalf of users, and OIDC provides a standardized foundation for this.

### Agent-to-Service Authentication

AI agents can use OIDC flows to authenticate to services. The agent acts as a client, obtaining tokens that authorize actions on behalf of the user. This enables:
- **Delegated user context**: Agents can operate within the authenticated user's security context
- **Audit trails**: Actions can be attributed to specific users through the token claims
- **Scoped permissions**: Agents receive only the permissions the user authorized

### Challenges for Agent Authentication

Agent authentication with OIDC presents unique challenges:

1. **Interactive flows**: Traditional OIDC flows assume an interactive human user at a browser. Agents may need to authenticate without user interaction.
2. **Token storage and rotation**: Agents must securely store tokens and handle refresh before expiration.
3. **Scope limitations**: Agents may need very specific, fine-grained permissions that don't map cleanly to OIDC scopes.
4. **Non-repudiation**: Determining whether an action was taken by a human or an agent acting on their behalf.

Some emerging patterns address these challenges:
- **Client credentials with OIDC**: Using client credentials flow where the agent itself is the resource owner
- **On-behalf-of flow**: User authenticates once, agent receives tokens to act on user's behalf
- **Delegation frameworks**: Extended OIDC implementations that explicitly model agent principals

## Zero-Trust Architecture and OIDC

Zero-trust security assumes no implicit trust based on network location or device. Every request must be authenticated and authorized. OIDC is a foundational technology for zero-trust architectures because it provides:

### Strong Authentication

Zero-trust requires verifying every identity, not just accepting credentials at the network perimeter. OIDC provides standardized, cryptographically verifiable authentication through ID tokens signed by trusted issuers.

### Stateless Authorization

Access tokens in OIDC (especially JWT-based access tokens) can carry authorization information directly, enabling stateless authorization decisions at API gateways and microservices. This scales better than centralized session checking.

### Fine-Grained Access Control

OIDC supports structured scopes and claims that can encode fine-grained permissions. Combined with external authorization systems (like Open Policy Agent), OIDC tokens can enable attribute-based access control (ABAC) within zero-trust architectures.

### Continuous Verification

While OIDC tokens have expiration times, zero-trust architectures often implement short-lived tokens and continuous verification patterns. The `offline_access` scope and refresh token mechanisms support this, though real-time validation against the authorization server may be required for high-security scenarios.

## OIDC vs SAML

Two dominant SSO protocols exist: OpenID Connect and Security Assertion Markup Language (SAML). Understanding when to use each matters for architecture decisions.

### Protocol Characteristics

**SAML 2.0** is an XML-based standard that predates OIDC. It was designed for enterprise SSO scenarios and is widely supported by enterprise identity providers (Okta, Azure AD, Ping Identity). SAML assertions are XML documents containing user identity information, signed with XML signatures.

**OIDC** is JSON-based and designed for modern web architectures. It works naturally with REST APIs and JavaScript applications. OIDC has become the default choice for new implementations, especially consumer and SaaS applications.

### Comparison Matrix

| Aspect | OIDC | SAML |
|--------|------|------|
| Protocol format | JSON/JWT | XML |
| REST API friendliness | Excellent | Poor |
| Browser SSO | Good (via redirect) | Good (via redirect) |
| Mobile app support | Excellent | Moderate |
| Ecosystem maturity | Growing rapidly | Very mature |
| Typical use case | Consumer apps, modern SaaS | Enterprise SSO |
| Token size | Smaller (JWT) | Larger (XML) |
| Mobile app complexity | Lower | Higher |

### When to Choose SAML

- Integrating with legacy enterprise identity providers that only support SAML
- Existing SAML investment that would be costly to migrate
- Strict enterprise environments where SAML's maturity and extensive security analysis provide comfort

### When to Choose OIDC

- New application development
- Mobile applications
- Microservices architectures
- REST API authentication
- Consumer-facing applications
- Integration with modern identity providers

## Practical Applications

### Common Use Cases

1. **Social Login**: Users authenticate to web applications using their Google, GitHub, or Microsoft accounts. The application receives an ID token confirming the user's identity without handling passwords.

2. **Single Sign-On Across Applications**: Enterprise users authenticate once with their corporate identity provider and access multiple SaaS applications without separate logins. OIDC enables this across applications from different vendors.

3. **API Authentication for Microservices**: Microservices validate JWT access tokens issued by the company's OIDC authorization server, enabling distributed authorization without a central session store.

4. **Zero-Trust Network Access**: Employees access internal applications from any location. OIDC tokens verify identity for every request, replacing VPN-based network perimeters.

5. **B2B Partner Authentication**: Organizations authenticate partner users through their own identity providers, enabling controlled cross-organizational access without separate credentials.

### Implementation Considerations

- **Token validation**: Always validate ID token signatures, issuer, audience, expiration, and nonce
- **HTTPS requirement**: All OIDC communication must occur over HTTPS
- **State parameter**: Use the `state` parameter to prevent CSRF attacks on redirect flows
- **PKCE for public clients**: Use Proof Key for Code Exchange when implementing authorization code flow in public clients (mobile apps, SPAs)
- **Token storage**: Never store tokens in localStorage for browser applications (XSS risk); prefer httpOnly cookies
- **Scope creep**: Request only necessary scopes; users may refuse excessive permission requests

## Examples

### Authorization Code Flow with Python

```python
import requests
from urllib.parse import urlencode

# Step 1: Redirect user to authorization endpoint
client_id = "your-client-id"
redirect_uri = "https://yourapp.com/callback"
authorization_endpoint = "https://auth.example.com/authorize"
state = "random-state-value"  # Generate cryptographically random
nonce = "random-nonce-value"
scope = "openid profile email"

auth_url = f"{authorization_endpoint}?{urlencode({
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': scope,
    'state': state,
    'nonce': nonce
})}"

# Step 2: Exchange authorization code for tokens
token_endpoint = "https://auth.example.com/token"
code = request.args.get('code')  # From callback

response = requests.post(token_endpoint, data={
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': 'your-client-secret'
})

tokens = response.json()
access_token = tokens['access_token']
id_token = tokens['id_token']
refresh_token = tokens.get('refresh_token')

# Step 3: Validate and decode ID token (use a proper JWT library in production)
# Step 4: Extract claims and establish user session
```

### Validating an ID Token

```python
import jwt
import requests

def validate_id_token(id_token, issuer, client_id):
    # Fetch OIDC discovery document
    jwks_uri = f"{issuer}/.well-known/openid-configuration"
    config = requests.get(jwks_uri).json()
    
    # Fetch signing keys
    jwks = requests.get(config['jwks_uri']).json()
    
    # Decode and validate token
    # In production, use a library like python-jose with proper validation
    claims = jwt.decode(
        id_token,
        jwt.get_unverified_header(id_token)['kid'],
        algorithms=['RS256'],
        audience=client_id,
        issuer=issuer
    )
    
    return claims
```

## Related Concepts

- [[OAuth-2.0]] — The authorization protocol foundation that OIDC builds upon
- [[JWT-JSON-Web-Token]] — The token format used for ID tokens in OIDC
- [[SAML]] — The XML-based SSO alternative to OIDC
- [[Zero-Trust]] — Security architecture where OIDC provides identity verification
- [[Identity-Provider]] — Systems like Auth0, Okta, and Keycloak that implement OIDC
- [[API-Security]] — How OIDC tokens secure API access
- [[Multi-Factor-Authentication]] — Authentication methods that complement OIDC

## Further Reading

- [OpenID Connect Official Specification](https://openid.net/connect/)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OIDC Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html)
- [JSON Web Token RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [RFC 8414 - OAuth 2.0 Authorization Server Metadata](https://datatracker.ietf.org/doc/html/rfc8414)
- [Okta OIDC Documentation](https://developer.okta.com/docs/reference/api/oidc/)
- [Auth0 OIDC Documentation](https://auth0.com/docs/authenticate/protocols/openid-connect-protocol)

## Personal Notes

> OpenID Connect replaced earlier identity protocols (OpenID 2.0, SAML 2.0 SSO) by being designed for modern web architectures. The shift from XML to JSON/JWT was pragmatic — REST APIs handle JSON natively, making OIDC a better fit for microservices and single-page applications. Enterprise environments still commonly use SAML for SSO, but OIDC has become the default for new cloud-native applications.
