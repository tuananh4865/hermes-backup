---
title: "Sso"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [authentication, security, identity-management, enterprise]
---

# SSO (Single Sign-On)

## Overview

Single Sign-On (SSO) is an authentication method that allows users to log in once and gain access to multiple related but independent software systems or resources without being prompted to sign in again for each application. This user experience improvement reduces password fatigue—the temptation to reuse passwords or use simple ones—and decreases time spent on repeated login processes. For organizations, SSO provides centralized user management, improved security visibility, and reduced IT support overhead related to password-related issues.

SSO operates on the principle of federated identity, where authentication state is shared between systems through a trusted relationship. When a user authenticates to one application (the identity provider), that authentication can be leveraged to access other participating applications (service providers). This trust relationship is established through standardized protocols and cryptographic verification, ensuring that service providers can reliably verify authentication decisions made by the identity provider.

## Key Concepts

**Identity Provider (IdP)** is the system that performs user authentication and maintains user identity information. Popular IdPs include Okta, Azure Active Directory (now Entra ID), Auth0, Ping Identity, and Google Workspace. The IdP is the single source of truth for user credentials and authentication status.

**Service Provider (SP)** is any application or system that relies on an external IdP for authentication. Instead of storing passwords, service providers redirect users to the IdP for login and receive cryptographic assertions confirming successful authentication.

**SAML (Security Assertion Markup Language)** is an XML-based protocol for exchanging authentication data between an IdP and SP. SAML 2.0, the current standard, enables cross-domain SSO and is common in enterprise environments. SAML assertions contain user attributes and are digitally signed for verification.

**OAuth 2.0** is an authorization framework (not an authentication protocol per se) that enables applications to obtain limited access to user accounts on third-party services. While not designed explicitly for SSO, OAuth 2.0 combined with OpenID Connect provides modern SSO functionality.

**OpenID Connect (OIDC)** is an identity layer built on top of OAuth 2.0. It adds ID tokens and a UserInfo endpoint, making it suitable for authentication. OIDC is the preferred choice for new applications due to its JSON-based format (easier than XML) and simpler implementation.

**SAML vs OIDC**: SAML is mature and widely supported in enterprise legacy systems. OIDC is more modern, mobile-friendly, and increasingly the default for new implementations.

## How It Works

A typical SSO flow works as follows:

1. User attempts to access a service provider application
2. SP detects user is not authenticated and redirects to the identity provider
3. User enters credentials at IdP and authenticates successfully
4. IdP generates a signed assertion (SAML token or OIDC ID token) containing user information
5. User is redirected back to SP with this assertion
6. SP validates the assertion's signature and extracts user identity
7. User is granted access to SP without needing to re-enter credentials

```javascript
// Example: Simple OIDC callback handling (pseudo-code)
async function handleAuthCallback() {
  const params = new URLSearchParams(window.location.search);
  const code = params.get('code');
  
  if (code) {
    // Exchange authorization code for tokens
    const tokenResponse = await fetch('/api/token', {
      method: 'POST',
      body: JSON.stringify({ code }),
      headers: { 'Content-Type': 'application/json' }
    });
    
    const { id_token, access_token } = await tokenResponse.json();
    
    // Store tokens
    sessionStorage.setItem('id_token', id_token);
    sessionStorage.setItem('access_token', access_token);
    
    // Decode ID token to get user info
    const user = parseJwt(id_token);
    console.log('User:', user.name, user.email);
  }
}
```

## Practical Applications

SSO is essential in:

- **Enterprise environments** where employees access dozens of internal applications daily
- **SaaS ecosystems** where organizations use multiple cloud services
- **Developer platforms** needing secure access across tools, documentation, and services
- **E-commerce platforms** where merchants access multiple dashboards and tools

## Related Concepts

- [[oauth]] - Authorization framework often paired with SSO
- [[openid-connect]] - Identity layer built on OAuth 2.0
- [[authentication]] - The general concept of verifying user identity
- [[identity-provider]] - System performing authentication
- [[saml]] - XML-based SSO protocol

## Further Reading

- NIST Digital Identity Guidelines (SP 800-63)
- Okta's "The Fundamentals of IAM"
- "Identity: The Right Way" by Okta

## Personal Notes

SSO significantly improves user experience but introduces a single point of failure—if the IdP is down, users cannot authenticate to ANY protected resource. Also, when an employee leaves, access revocation must happen at the IdP, not individual systems. For smaller projects, implementing full SSO might be overkill; consider starting with simple token-based auth and adding SSO later if needed.
