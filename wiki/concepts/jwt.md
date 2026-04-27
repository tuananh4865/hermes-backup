---
title: "Jwt"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [jwt, authentication, security, tokens]
---

# Jwt

## Overview

JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact, self-contained method for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed using a secret key (HMAC) or a public/private key pair (RSA or ECDSA).

JWT is the foundation of modern token-based authentication systems. Unlike traditional session-based authentication where the server stores user state in memory or a database, JWTs allow servers to authenticate requests without storing any session data. The token itself contains all the necessary information about the user, making horizontal scaling significantly easier since any server in a cluster can validate a token independently.

The authentication flow typically works as follows: when a user logs in with credentials, the server verifies them and generates a JWT containing claims about that user (such as user ID, roles, and expiration time). This token is returned to the client, which stores it (commonly in localStorage or an HTTP-only cookie). On subsequent requests, the client sends the JWT in the Authorization header, and the server validates the signature and claims before processing the request.

## Structure

A JWT consists of three parts separated by dots: `xxxxx.yyyyy.zzzzz`

**Header**: The header typically contains two parts: the type of token (JWT) and the signing algorithm being used (such as HS256 or RS256). This JSON is then Base64URL encoded.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload**: The second part is the payload, which contains the claims. Claims are statements about the user and additional metadata. There are three types of claims: registered claims (predefined like iss, exp, sub, aud), public claims (user-defined but registered to avoid collisions), and private claims (custom claims agreed upon between parties). The payload is also Base64URL encoded.

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "role": "admin",
  "exp": 1516239022
}
```

**Signature**: To create the signature, the encoded header, encoded payload, a secret or private key, and the algorithm specified in the header are taken and signed. The signature verifies message integrity and, when using asymmetric keys, can also verify the identity of the token issuer.

## Use Cases

JWTs are widely used in several scenarios:

- **User Authentication**: Single Sign-On (SSO) implementations commonly use JWTs as they can be passed between multiple domains or services securely.
- **API Authorization**: RESTful APIs use JWTs to authorize requests, with the token containing permissions and scopes that the server validates.
- **Stateless Sessions**: High-traffic applications benefit from JWTs because validation requires no database lookup, reducing latency and infrastructure cost.
- **Information Exchange**: JWTs can securely transmit information between trusted parties since the signature guarantees authenticity.

## Related

- [[OAuth2]] - A complementary authorization framework that often uses JWTs as access tokens
- [[ApiSecurity]] - General API security concepts including token-based authentication
- [[Authentication]] - Overview of authentication methods and mechanisms
- [[SessionManagement]] - Comparison of session-based vs token-based session handling
