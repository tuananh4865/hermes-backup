---
title: "Json Web Tokens"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [authentication, security, web, jwt, api, stateless-auth]
---

# Json Web Tokens

## Overview

JSON Web Tokens (JWT, pronounced "jot") are an open standard (RFC 7519) for transmitting compact, self-contained pieces of information between parties as a JSON object. A JWT is digitally signed, which allows the receiver to verify its authenticity, and can be signed using a secret (HMAC) or a public/private key pair (RSA or ECDSA). Because the token is self-contained — it carries its own payload — the receiver does not need to query a database to validate a user's identity on each request.

JWTs have become the de facto standard for stateless authentication in modern web applications, APIs, and microservices. They power the "Log in once, stay authenticated" experience across distributed systems where the frontend, backend, and third-party services may run on entirely separate domains or infrastructure.

## Key Concepts

**Three-Part Structure**: A JWT is a string formatted as `xxxxx.yyyyy.zzzzz`, consisting of three Base64URL-encoded components concatenated with dots:
- **Header**: Contains the algorithm (`HS256`, `RS256`, etc.) and token type (`JWT`)
- **Payload**: Contains the claims — registered claims like `iss`, `exp`, `sub`, and custom claims specific to the application
- **Signature**: The cryptographic seal that verifies the header and payload have not been tampered with

**Claims**: The payload is a JSON object of "claims." Registered claims include `exp` (expiration time), `nbf` (not before), `iat` (issued at), `sub` (subject, typically the user ID), and `aud` (audience). Custom claims like `role: "admin"` or `plan: "pro"` carry application-specific data.

**Signed vs. Encrypted**: A signed JWT (JWS) only guarantees integrity — it proves the payload hasn't been modified. An encrypted JWT (JWE) also guarantees confidentiality, as the payload is encrypted and cannot be read without the decryption key. Most authentication use cases use JWS only.

## How It Works

In a typical authentication flow, the user submits credentials to a `/login` endpoint. The server verifies them and generates a JWT containing the user's ID and any roles or permissions needed. The server signs this token with a secret or private key and returns it to the client.

On every subsequent request, the client sends the JWT in the `Authorization` header as `Bearer <token>`. The server validates the signature using its copy of the secret (or the user's public key), checks that the token hasn't expired, and if valid, trusts the claims inside — no database lookup required.

```javascript
// Creating a JWT (using the jsonwebtoken library)
const jwt = require('jsonwebtoken');
const token = jwt.sign(
  { userId: 42, role: 'editor' },
  process.env.JWT_SECRET,
  { expiresIn: '2h' }
);
// token is a string: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

// Verifying a JWT
try {
  const decoded = jwt.verify(token, process.env.JWT_SECRET);
  console.log(decoded.userId); // 42
} catch (err) {
  // Token invalid or expired
}
```

## Practical Applications

JWTs shine in microservices architectures where multiple services need to share authentication context without a central session store. Each service can independently verify a token using a shared secret or the issuing service's public key, eliminating the need for a shared database or session server.

In Single Sign-On (SSO) scenarios, an identity provider issues a JWT after login, and relying services accept it without requiring the user to re-authenticate. [[OAuth 2.0]] flows frequently use JWTs as the `access_token` format.

Mobile applications use JWTs for the same reason: no session cookies means no CSRF vulnerability, and token storage (with care) on the device is straightforward. The tradeoff is that revoking a JWT before it expires is difficult — solutions like token blacklists or short expiration windows mitigate this.

## Examples

A decoded JWT payload for a blog application might look like:

```json
{
  "sub": "user_123",
  "name": "Alice Nakamura",
  "role": "author",
  "iat": 1712000000,
  "exp": 1712003600
}
```

A frontend fetching a protected resource would send:

```
GET /api/posts HTTP/1.1
Host: example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

The server decodes and verifies the token, trusting `sub` and `role` to determine what data to return.

## Related Concepts

- [[OAuth 2.0]] — Authorization framework that often uses JWTs as tokens
- [[API Security]] — Broader practices for securing APIs, many of which center on JWTs
- [[JSON]] — The data format on which JWTs are built
- [[Public Key Cryptography]] — Used for RS256/ES256 signed JWTs
- [[Session Management]] — Contrast with server-side session-based authentication

## Further Reading

- [RFC 7519 — JSON Web Token (JWT)](https://datatracker.ietf.org/doc/html/rfc7519)
- [JWT.io](https://jwt.io/) — Debug and validate JWTs interactively
- *Identity and Access Management for the Rest of Us* — Practical JWT patterns

## Personal Notes

I initially treated JWTs as opaque strings, but understanding the three-part structure changed how I debug authentication issues. When a token fails verification, the error is almost always either a clock-skewed expiration, a mismatched algorithm (a classic security pitfall where an attacker specifies `none` or `HS256` when the server accepts `alg: none`), or a secret that was rotated without updating active tokens. I now always inspect the decoded payload during debugging with `atob()` rather than guessing from error messages.
