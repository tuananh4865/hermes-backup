---
title: SAML
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [saml, sso, authentication, security]
---

# SAML

## Overview

Security Assertion Markup Language (SAML) is an open standard for exchanging authentication and authorization data between parties, specifically between an Identity Provider (IdP) and a Service Provider (SP). SAML is an XML-based protocol that enables Single Sign-On (SSO) functionality, allowing users to authenticate once and gain access to multiple applications without needing to re-enter credentials for each service.

SAML was developed by the OASIS (Organization for the Advancement of Structured Information Standards) consortium and first published in 2002. The current widely deployed version is SAML 2.0, which superseded the earlier SAML 1.1 and SAML 1.0 specifications. The protocol is particularly prevalent in enterprise environments, government systems, and educational institutions where secure inter-domain authentication is required.

The core purpose of SAML is to solve the problem of identity federation across different organizations and domains. Rather than maintaining separate user accounts in each application, organizations can delegate authentication to a trusted IdP that vouches for user identity. This approach reduces password fatigue among users, simplifies identity management for administrators, and enhances security by limiting the number of places where credentials must be stored.

## How It Works

SAML authentication involves a browser-based flow with three primary actors: the user (via their browser), the Service Provider (the application the user wants to access), and the Identity Provider (the system that authenticates the user and issues assertions).

The typical SAML SSO flow proceeds as follows:

**1. User Initiates Access**: The user attempts to access a protected resource at the Service Provider. If the user is not already authenticated, the SP generates a SAML Authentication Request and redirects the user to the IdP.

**2. Authentication at IdP**: The user completes authentication with the Identity Provider. This may involve entering username and password, multi-factor authentication, or other credential mechanisms. The IdP validates credentials and prepares a SAML Response.

**3. Assertion Generation**: The IdP creates a SAML Response containing one or more SAML Assertions. These assertions are XML documents that contain statements about the user's identity, authentication event, and potentially attributes such as name, email, and group memberships. The IdP digitally signs the assertion using X.509 certificates to ensure integrity and authenticity.

**4. Response Delivery**: The IdP returns the SAML Response to the Service Provider. This can occur via HTTP POST binding (where the browser posts the response) or HTTP redirect binding (for smaller responses).

**5. Validation and Access Grant**: The Service Provider validates the SAML Response by checking the digital signature, verifying the certificate, confirming the audience restriction, and ensuring the response is not expired. Upon successful validation, the SP establishes a local session for the user and grants access to the requested resource.

Key SAML components include the Assertion (the XML document containing user identity information), the AuthnRequest (a request from SP to IdP), the Response (the IdP's reply containing assertions), and various protocol bindings that define how SAML messages are transmitted over HTTP.

## OAuth/OIDC Comparison

While SAML, OAuth, and OpenID Connect (OIDC) all address authentication and authorization, they differ significantly in their design, use cases, and technical approaches.

**Protocol Age and Format**: SAML 2.0 dates from 2005 and uses XML for all message formats. OAuth 2.0 was finalized in 2012 and relies on JSON data formats. OpenID Connect, built on top of OAuth 2.0 in 2014, also uses JSON but adds an identity layer with standardized claims.

**Primary Use Cases**: SAML excels in enterprise single sign-on scenarios where users need to access legacy applications and internal systems within or across organizational boundaries. OAuth 2.0 is designed for authorization, particularly for API access and third-party application permissions (such as "Sign in with Google" functionality). OIDC provides identity verification optimized for modern web and mobile applications, offering a lighter-weight alternative to SAML.

**Token Structure**: SAML assertions are XML-based and can be quite large, sometimes several kilobytes. OAuth access tokens are typically compact bearer tokens (often JWTs), and OIDC adds ID tokens that contain user identity information in a standardized JSON format. This makes OAuth/OIDC more suitable for mobile applications and bandwidth-constrained scenarios.

**Complexity and Implementation**: SAML's XML processing requirements and digital signature mechanisms make implementation more complex, requiring specialized XML security libraries. OAuth and OIDC benefit from simpler JSON-based processing and widespread support across modern development frameworks.

**Federation Standards**: SAML supports sophisticated federation scenarios with automated metadata exchange and entity categorization. OIDC has gained significant traction for consumer-facing identity due to its developer-friendly design, while SAML remains dominant in enterprise and government sectors with existing identity infrastructure.

## Related

- [[Single Sign-On]] - The authentication concept that SAML implements
- [[Identity Provider]] - The trusted authority that authenticates users in SAML flows
- [[OAuth 2.0]] - The authorization framework that OIDC extends
- [[OpenID Connect]] - An identity layer built on OAuth 2.0 often compared to SAML
- [[X.509 Certificates]] - Used for digital signatures in SAML assertions
- [[XML Digital Signature]] - The XML security standard for ensuring SAML message integrity
- [[Federated Identity]] - The broader concept of sharing identity across organizational boundaries
