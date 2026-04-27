---
title: Single Sign-On
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [single-sign-on, authentication, identity, SSO, security]
---

# Single Sign-On

## Overview

Single Sign-On (SSO) is an authentication mechanism that allows users to authenticate once and gain access to multiple independent software systems or applications without needing to re-enter credentials for each one. Instead of maintaining separate username/password pairs for every application, users maintain a single identity with an identity provider (IdP), and that identity is trusted by all connected service providers (SPs).

SSO addresses a fundamental tension in digital identity: users need secure, unique credentials for each service, but managing dozens or hundreds of account passwords is impractical. The result is password reuse, weak passwords, or forgotten passwords—all security risks. SSO reduces password fatigue while improving security posture through centralized authentication enforcement.

Modern SSO is typically built on federated identity standards like SAML 2.0, OAuth 2.0 with OpenID Connect (OIDC), or proprietary protocols like Windows Integrated Authentication (Kerberos/SPNEGO) used in enterprise Active Directory environments.

## Key Concepts

**Identity Provider (IdP)**: The central authority that maintains user identities and handles authentication. Examples include Okta, Azure AD, Auth0, Google Workspace, and Keycloak. The IdP is responsible for verifying user credentials and issuing assertions/tokens.

**Service Provider (SP)**: An application or system that trusts the IdP for authentication. Instead of checking passwords itself, the SP accepts identity assertions from the IdP. Applications delegate authentication to the IdP.

**SAML 2.0 (Security Assertion Markup Language)**: An XML-based standard for exchanging authentication data between IdP and SP. Uses signed XML documents to assert user identity. Dominant in enterprise environments, especially older systems.

**OAuth 2.0 + OpenID Connect**: OAuth 2.0 is primarily an authorization framework (granting access to resources). OpenID Connect (OIDC) adds an identity layer on top, enabling authentication. Modern web and mobile apps predominantly use OIDC.

**Trust Relationships**: For SSO to work, SPs must be configured to trust specific IdPs. This involves exchanging metadata, certificates, and configuring allowed identifiers. Misconfigured trust is a common source of SSO failures.

**Session Management**: After the initial SSO authentication, the SP typically creates its own local session. The IdP may also maintain a session for single logout capability—terminating all active sessions across SPs when user logs out.

## How It Works

### SAML Flow

1. User attempts to access SP application
2. SP detects no local session, redirects to IdP with SAML AuthnRequest
3. IdP presents login page, user enters credentials
4. IdP generates SAML Response containing user attributes (email, name, roles), signs it with private key
5. User's browser posts SAML Response to SP
6. SP validates signature using IdP's public certificate, extracts user identity, creates local session

### OAuth/OIDC Flow

1. User clicks "Login with [Provider]" on SP
2. SP redirects to IdP's authorization endpoint with client_id, redirect_uri, scopes
3. User authenticates with IdP (may use existing session)
4. IdP redirects back to SP with authorization code
5. SP exchanges code for tokens (access_token, id_token) at token endpoint
6. SP validates id_token (signature, issuer, audience, expiry)
7. SP extracts user info from id_token or userinfo endpoint, creates local session

```javascript
// OIDC callback handler (simplified)
async function handleCallback(code) {
    // Exchange code for tokens
    const tokens = await fetch(tokenEndpoint, {
        method: 'POST',
        body: new URLSearchParams({
            grant_type: 'authorization_code',
            code: code,
            redirect_uri: redirectUri,
            client_id: clientId,
            client_secret: clientSecret
        })
    }).then(r => r.json());
    
    // Validate id_token (in production, verify signature with JWKS)
    const claims = JSON.parse(atob(tokens.id_token.split('.')[1]));
    
    // Check issuer, audience, expiry
    if (claims.iss !== expectedIssuer || 
        claims.aud !== clientId || 
        claims.exp > Date.now() / 1000) {
        throw new Error('Invalid token');
    }
    
    // Create session
    return createSession(claims.sub, claims.email, claims.name);
}
```

## Practical Applications

**Enterprise Identity**: Large organizations use SSO with Azure AD or Okta to provide employees one-click access to Office 365, Salesforce, Slack, and hundreds of internal applications. This is particularly valuable in environments with high employee turnover and frequent access changes.

**SaaS Consolidation**: Instead of managing accounts in each SaaS tool, IT departments configure SSO so the company's IdP controls access. When an employee leaves, disabling their IdP account immediately revokes access to all connected applications.

**Developer Authentication**: Developers implement SSO using Auth0, Okta, or AWS Cognito to handle user authentication in applications, avoiding the complexity and liability of storing passwords directly.

**Government and Education**: FedRAMP-compliant identity providers serve government agencies. Edugate/InCommon serves universities. These federations enable cross-institutional collaboration.

## Examples

**Google Workspace SSO**: Many organizations use Google as their IdP. After logging into Google (or having an existing Google session), users can access configured third-party apps without re-authenticating.

**Okta Integration**: Okta supports both SAML and OIDC. An administrator configures applications in Okta, obtains metadata, and configures the SP accordingly. Okta's Lifecycle Management automates provisioning/deprovisioning.

**Enterprise Active Directory + ADFS**: On-premises AD domains can federate with cloud services using ADFS (Active Directory Federation Services) or Azure AD Connect. Users log in with domain credentials; ADFS issues tokens for cloud apps.

## Related Concepts

- [[OAuth 2.0]] — Authorization framework often paired with OIDC for SSO
- [[OpenID Connect]] — Identity layer on top of OAuth 2.0
- [[SAML]] — XML-based federated identity standard
- [[Authentication]] — General authentication concepts
- [[RBAC]] — Role-based access control, often integrated with SSO
- [[MFA]] — Multi-factor authentication, frequently required alongside SSO

## Further Reading

- NIST SP 800-63C: Federation and Assertions — Government guidance on SSO
- Okta's "The Fundamentals of IAM" — Practical SSO guide
- OIDC Specification: https://openid.net/connect/

## Personal Notes

SSO is one of those technologies where the implementation details matter enormously for security. The SAML/OIDC flow looks straightforward, but certificate rotation, clock skew, and session lifetime management trip up many productions deployments. I've seen SSO break in subtle ways—token lifetime mismatches causing unexpected logouts, or attribute mapping mismatches silently denying access. The hardest part isn't getting SSO working; it's keeping it working under the pressure of real organizational change (employee departures, IdP migrations, certificate renewals).
