---
title: "Token Based Authentication"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [authentication, security, jwt, oauth, api, web-security]
---

# Token Based Authentication

## Overview

Token-based authentication is a stateless authentication pattern where the server issues a signed token to the client after validating credentials, and the client subsequently presents this token with each request to prove identity and authorize access. Unlike session-based authentication, which stores user state on the server, token-based auth embeds all necessary information in the token itself—enabling horizontal scaling, cross-domain architectures, and stateless API designs.

The dominant form of token-based authentication today is JWT (JSON Web Tokens), an open standard (RFC 7519) that encodes claims as JSON, base64-encodes them, and signs the result cryptographically. JWTs have become the foundation of modern API security, powering OAuth 2.0 flows, SPAs, mobile apps, and microservices architectures. The key advantage: any server with the signing key can validate the token—no session store required.

## Key Concepts

### JWT Structure

A JWT consists of three base64-encoded parts separated by dots:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

- **Header**: Algorithm and token type (e.g., `{"alg": "HS256", "typ": "JWT"}`)
- **Payload**: Claims (e.g., `{"sub": "123", "name": "John", "exp": 1516239022}`)
- **Signature**: HMAC or RSA signature of `header.payload`

### Access and Refresh Tokens

Modern applications separate tokens into:
- **Access Token**: Short-lived token (minutes to hours) used for API authorization
- **Refresh Token**: Long-lived token (days to weeks) used to obtain new access tokens

This separation limits exposure if an access token is leaked while enabling legitimate sessions to persist without repeated logins.

### Token Storage

Where tokens are stored on the client matters for security:
- **HttpOnly Cookies**: Most secure against XSS, but limited to browser cookie storage
- **LocalStorage**: Accessible to JavaScript, vulnerable to XSS but convenient
- **Memory (variable)**: Most secure against XSS but lost on page reload
- **SessionStorage**: Cleared on tab close, better than localStorage for sensitive apps

## How It Works

```
User Login Flow:
┌────────┐                    ┌──────────┐                 ┌────────┐
│ Client │                    │ Auth Server │             │ User DB │
└───┬────┘                    └─────┬─────┘              └───┬────┘
    │ POST /login {user,pass}      │                         │
    │─────────────────────────────►│ validate credentials     │
    │                              │─────────────────────────►│
    │                              │◄─────────────────────────┤
    │   { access_token,            │                         │
    │     refresh_token }          │                         │
    │◄─────────────────────────────│                         │
    │                              │                         │
    │ API Request with Bearer      │                         │
    │ Authorization header         │                         │
    │─────────────────────────────►│ validate JWT signature   │
    │   { requested_resource }     │                         │
    │◄─────────────────────────────│                         │
```

```javascript
// Express.js JWT middleware example
const jwt = require('jsonwebtoken');

app.get('/api/protected', authenticateToken, (req, res) => {
  // req.user populated by middleware
  res.json({ 
    message: 'Protected data', 
    user: req.user.sub 
  });
});

function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1]; // Bearer TOKEN
  
  if (!token) return res.sendStatus(401);
  
  jwt.verify(token, process.env.ACCESS_TOKEN_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}
```

## Practical Applications

- **REST API Authorization**: Stateless API calls where each request carries credentials
- **Single Page Applications (SPAs)**: Maintaining session without server-side session storage
- **Mobile Applications**: Secure token storage on devices with refresh token rotation
- **Microservices**: Shared secret or public key validation across service boundaries
- **Federated Identity**: OAuth 2.0 and OIDC rely on JWTs for identity and access tokens

## Examples

**Login and API Access Example**:
```javascript
// Client-side login
const response = await fetch('/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username, password })
});
const { access_token, refresh_token } = await response.json();

// Store tokens securely
sessionStorage.setItem('access_token', access_token);
httpOnlyCookie('refresh_token', refresh_token);

// Use token for API calls
const data = await fetch('/api/data', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
```

**Refresh Token Rotation Example**:
```javascript
// Refresh endpoint - issues new access token and rotates refresh token
app.post('/refresh', (req, res) => {
  const refreshToken = req.cookies.refresh_token;
  if (!refreshToken) return res.sendStatus(401);
  
  jwt.verify(refreshToken, REFRESH_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    
    // Rotate refresh token (invalidate old one)
    const newAccessToken = jwt.sign(
      { sub: user.sub }, 
      ACCESS_SECRET, 
      { expiresIn: '15m' }
    );
    const newRefreshToken = jwt.sign(
      { sub: user.sub }, 
      REFRESH_SECRET, 
      { expiresIn: '7d' }
    );
    
    res.cookie('refresh_token', newRefreshToken, { httpOnly: true });
    res.json({ access_token: newAccessToken });
  });
});
```

## Related Concepts

- [[oauth-2]] — Authorization framework that uses tokens
- [[jwt]] — JSON Web Token standard
- [[authentication]] — Broader authentication concepts
- [[api-security]] — Securing API endpoints
- [[session-management]] — Comparison with session-based auth

## Further Reading

- [RFC 7519: JSON Web Token (JWT)](https://tools.ietf.org/html/rfc7519)
- [RFC 6749: OAuth 2.0 Authorization Framework](https://tools.ietf.org/html/rfc6749)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

## Personal Notes

Token-based auth is excellent for scalability but introduces complexity that sessions avoid. The biggest mistake I see: storing tokens in localStorage for convenience, then being surprised when XSS vulnerabilities expose them. HttpOnly cookies are safer for browser apps. Also: always implement refresh token rotation—it's the best defense against token theft replay attacks. For microservices, prefer asymmetric keys (RS256) so each service only needs the public key to validate tokens, not the signing key. And remember: JWT payload is encoded, not encrypted—don't put sensitive data like passwords in it.
