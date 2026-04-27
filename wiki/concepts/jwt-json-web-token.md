---
title: "Jwt Json Web Token"
created: 2026-04-20
updated: 2026-04-20
type: concept
tags: [authentication, security, web, oauth2, oidc]
sources: [RFC 7519, RFC 7515, RFC 7517]
---

# JWT (JSON Web Token)

> A JWT is a compact, URL-safe means of representing claims to be transferred between two parties. It is widely used for stateless authentication and authorization in modern web applications and APIs.

## Overview

JSON Web Token (JWT, pronounced "jot") is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

The primary purpose of JWTs is to enable stateless authentication and authorization. Instead of storing user session data on the server, the token itself contains all the necessary information. This makes JWTs particularly well-suited for distributed systems, microservices architectures, and single-page applications where requests may be handled by different servers.

JWTs are embedded in HTTP headers (typically the `Authorization` header with the `Bearer` scheme) and are used extensively in OAuth 2.0 and OpenID Connect flows. They provide a standardized format that can be parsed and validated by any party that has access to the signing key.

## JWT Structure

A JWT consists of three parts separated by dots (`.`): `header.payload.signature`. The overall format looks like this:

```
xxxxx.yyyyy.zzzzz
```

### Header

The header is a JSON object that typically contains two fields: `alg` (the algorithm used to sign the token) and `typ` (the type of token, usually "JWT"). For example:

```json
{
  "alg": "RS256",
  "typ": "JWT"
}
```

This header JSON is then Base64URL-encoded to produce the first part of the JWT.

### Payload

The payload is a JSON object that contains the claims. Claims are statements about an entity (typically the user) and additional metadata. There are three types of claims:

- **Registered claims**: Predefined claims that are recommended but not mandatory. These include `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, and `jti`.
- **Public claims**: Claims defined in the IANA JSON Web Token Registry that can be used freely with interoperability in mind.
- **Private claims**: Custom claims created to share information between parties that agree on using them.

The payload is Base64URL-encoded to produce the second part of the JWT.

### Signature

The signature is computed by taking the encoded header, the encoded payload, the secret (or private key), and applying the algorithm specified in the header. For example, when using HMAC SHA256:

```
HMACSHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  secret
)
```

This produces the third and final part of the JWT.

### Example Decoded JWT

A decoded JWT (before Base64URL encoding) looks like:

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622,
  "iss": "https://example.com",
  "aud": "my-application"
}
```

## Registered Claims

The JWT specification defines several registered claims that provide standardized metadata:

- **`iss` (Issuer)**: Identifies the principal that issued the JWT. The issuer is typically a URI or a string that uniquely identifies the issuing authority.
- **`sub` (Subject)**: Identifies the principal that is the subject of the JWT. In authentication contexts, this is typically the user identifier.
- **`aud` (Audience)**: Identifies the recipients that the JWT is intended for. When present, the audience claim helps prevent tokens issued for one application from being used in another.
- **`exp` (Expiration Time)**: A timestamp that identifies when the token expires. After this time, the token should no longer be accepted for processing.
- **`nbf` (Not Before)**: A timestamp that identifies the time before which the token should not be accepted.
- **`iat` (Issued At)**: A timestamp that indicates when the token was issued. This can be used to determine the age of the token.
- **`jti` (JWT ID)**: A unique identifier for the token. This claim provides a unique identifier for individual tokens, useful for token revocation and replay prevention.

## JWS vs JWE

It is important to distinguish between two related standards: JSON Web Signature (JWS, RFC 7515) and JSON Web Encryption (JWE, RFC 7516).

**JWS** is what most people mean when they talk about JWTs. A JWS represents content that has been signed, ensuring integrity. The signature allows the recipient to verify that the payload has not been tampered with. However, the payload is encoded in plain text (Base64URL), meaning anyone can read it.

**JWE** adds encryption to the standard. With JWE, the content is encrypted using symmetric or asymmetric encryption algorithms, ensuring confidentiality. The payload (called the "ciphertext" in JWE terminology) is not readable without the decryption key.

For most authentication use cases, JWS is sufficient because sensitive information is not stored in the token itself—the token merely proves authentication. For cases where the token must carry sensitive data that should not be exposed to third parties, JWE provides the necessary encryption.

## Signing Algorithms

JWTs support multiple signing algorithms, which can be categorized into symmetric and asymmetric groups.

### Symmetric Algorithms (HS256, HS384, HS512)

HMAC-based algorithms use a single secret key that is shared between the issuer and the verifier. **HS256** (HMAC with SHA-256) is the most commonly used symmetric algorithm. It is fast and suitable for single-server deployments or scenarios where the secret can be securely distributed.

The main drawback is key distribution: the same secret must be available to all parties that need to validate tokens.

### Asymmetric Algorithms (RS256, RS384, RS512, ES256, ES384, ES512)

RSA-based and ECDSA-based algorithms use a key pair: a private key for signing and a public key for verification. **RS256** (RSA Signature with SHA-256) is widely adopted, particularly in enterprise applications.

The advantage of asymmetric algorithms is that the private key only needs to be kept secure by the issuer, while the public key can be freely distributed. This makes them ideal for distributed systems and scenarios where multiple services need to validate tokens without each having access to the signing key.

**ES256** (ECDSA with SHA-256) is an increasingly popular choice for new applications due to its shorter key lengths and computational efficiency compared to RSA.

## Use Cases

### API Authentication

JWTs are most commonly used to authenticate requests to APIs. After a user logs in, the server issues a JWT that the client includes in subsequent requests:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

The API server validates the signature and checks expiration before processing the request. This approach is stateless—the server does not need to query a database or session store to validate each token.

### OpenID Connect (OIDC)

JWTs are fundamental to OpenID Connect, an identity layer built on top of OAuth 2.0. In OIDC flows, the ID Token is a JWT that contains claims about the authenticated user, including their identifier (`sub`), the issuer (`iss`), and the audience (`aud`). OIDC ID tokens are always signed (typically with RS256 or ES256) and may optionally be encrypted.

The OIDC protocol uses JWTs for:

- **ID Tokens**: Proving user authentication
- **Access Tokens**: In some OIDC implementations, access tokens are JWTs rather than opaque tokens
- **UserInfo Endpoint Responses**: The UserInfo endpoint returns claims as a JSON object that may be serialized as a JWT

### Token Refresh Flows

JWTs typically have short expiration times (often 15 minutes to 1 hour) for security reasons. To maintain sessions beyond this period, applications implement token refresh flows. The server issues two tokens: an access token with a short lifetime and a refresh token with a longer lifetime.

When the access token expires, the client presents the refresh token to obtain a new access token. Refresh tokens can be single-use (rotation) or long-lived, depending on the security requirements. This pattern allows users to stay authenticated while limiting the damage from compromised tokens.

## Security Considerations

### Algorithm Confusion Attacks

One of the most serious security vulnerabilities involving JWTs is the algorithm confusion attack (also known as the `alg` header injection attack). If an application does not properly validate the algorithm specified in the token header, an attacker can change the `alg` field from an asymmetric algorithm like `RS256` to a symmetric algorithm like `HS256`.

The attack works because the server may use a configurable secret derived from the public key when it expects to use asymmetric verification. With the `alg` changed to `HS256`, the attacker can forge tokens by signing the header and payload with the public key (which is publicly known). To prevent this, always validate the expected algorithm explicitly and never trust the `alg` header from untrusted input without validation.

### Token Expiration and Revocation

JWTs are stateless and self-contained, which creates challenges for revocation. Because the server validates tokens based on signature and expiration rather than querying a database, revoking a token before its natural expiration is not straightforward.

Common approaches to handle revocation include:

- **Short token lifetimes**: Using short expiration times so that compromised tokens are automatically invalidated quickly
- **Token blacklists**: Maintaining a small database or cache of revoked token IDs (using the `jti` claim), though this reintroduces state
- **Refresh token rotation**: Issuing new refresh tokens on each use, making stolen refresh tokens useless after rotation
- **Token families**: Assigning each token a family identifier and invalidating entire families when compromise is detected

### Secret Key Management

For symmetric algorithms, the secret key must be carefully managed. It should be long enough to prevent brute-force attacks (at least 256 bits for HS256), stored securely (never in source code or version control), and rotated periodically.

With asymmetric algorithms, private keys require even more protection since compromise allows unlimited token forgery. Consider using hardware security modules (HSMs) or key management services (KMS) for production environments.

### Sensitive Data in Payloads

Because JWT payloads are Base64-encoded rather than encrypted, never include sensitive information such as passwords, credit card numbers, or personal data beyond what is necessary for the application's needs. If sensitive data must be transmitted, use JWE instead of JWS.

## Related Concepts

Understanding JWTs connects to several important related topics:

- [[OAuth 2.0]] — the authorization framework that often issues JWTs as access tokens
- [[OpenID Connect]] — an identity layer built on OAuth 2.0 that uses JWTs for ID tokens
- [[API Authentication]] — the general topic of authenticating API requests
- [[HMAC]] — the symmetric signing algorithm family used by HS256 and similar algorithms
- [[RSA]] — the asymmetric algorithm used by RS256 and related algorithms

## Further Reading

- [RFC 7519: JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519) — The primary specification for JWTs
- [RFC 7515: JSON Web Signature (JWS)](https://tools.ietf.org/html/rfc7515) — The specification for signed tokens
- [RFC 7517: JSON Web Key (JWK)](https://tools.ietf.org/html/rfc7517) — The specification for representing cryptographic keys
- [RFC 7518: JSON Web Algorithms (JWA)](https://tools.ietf.org/html/rfc7518) — Cryptographic algorithms used with JWTs
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html) — Security guidance for JWT implementation

## Personal Notes

> JWTs are a powerful tool for stateless authentication, but they require careful implementation. The simplicity of JWT validation can be deceptive—what seems like a straightforward signature check can harbor subtle vulnerabilities. Always stay updated on the latest security guidance and prefer well-tested libraries over custom implementations.
