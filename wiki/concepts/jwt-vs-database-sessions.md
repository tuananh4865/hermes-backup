---
confidence: high
last_verified: 2026-04-11
relationships:
  - [[authentication]]
  - [[vercel-database-persistence]]
  - [[api-design-patterns]]
relationship_count: 3
---

# JWT vs Database Sessions

> Two fundamentally different approaches to managing user authentication state in web applications.

## Overview

When building web applications, you need to track whether a user is logged in. Two main patterns exist:

- **JWT (JSON Web Tokens)**: Stateless tokens stored client-side that contain encoded user data
- **Database Sessions**: Stateful session records stored server-side, identified by a session ID cookie

Both solve the same problem — maintaining user identity across HTTP requests — but with very different trade-offs.

## JWT (JSON Web Tokens)

### How JWT Works

A JWT is a self-contained token that encodes three parts:

1. **Header**: Algorithm and token type
2. **Payload**: User data (claims), expiration
3. **Signature**: Verified with a secret key

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNCIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTcxMjM0NTY3OH0K8pW3x7TpW3x7TpW3x7TpW3x7TpW3x7Q
```

### Implementation

**Creating a JWT:**

```python
import jwt
from datetime import datetime, timedelta

def create_token(user_id: str, role: str) -> str:
    payload = {
        "user_id": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Verifying a JWT:**

```python
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"success": True, "payload": payload}
    except jwt.ExpiredSignatureError:
        return {"success": False, "error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"success": False, "error": "Invalid token"}
```

### Where JWTs Are Stored

| Storage | Pros | Cons |
|---------|------|------|
| **localStorage** | Easy to implement | Vulnerable to XSS |
| **HttpOnly Cookie** | Protected from XSS | CSRF risk, harder to read client-side |
| **Memory (variable)** | Most secure | Lost on page refresh |

## Database Sessions

### How Database Sessions Work

1. User logs in → server creates session record in database
2. Server returns session ID (random string) in a cookie
3. Subsequent requests include the cookie
4. Server looks up session ID, retrieves user data

### Implementation

**Session table schema:**

```sql
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    data JSONB DEFAULT '{}',
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_sessions_expires ON sessions(expires_at);
```

**Creating a session:**

```python
import secrets
from datetime import datetime, timedelta

def create_session(user_id: str) -> str:
    session_id = secrets.token_urlsafe(32)
    db.execute(
        """
        INSERT INTO sessions (id, user_id, expires_at)
        VALUES (%s, %s, %s)
        """,
        session_id, user_id, datetime.utcnow() + timedelta(days=7)
    )
    return session_id
```

**Session middleware:**

```python
async def session_middleware(request, next):
    session_id = request.cookies.get("session_id")
    
    if not session_id:
        return Response(status=401, body="Not authenticated")
    
    session = db.query_one(
        "SELECT * FROM sessions WHERE id = %s AND expires_at > NOW()",
        session_id
    )
    
    if not session:
        return Response(status=401, body="Session expired")
    
    request.user_id = session["user_id"]
    return await next(request)
```

## Comparison

| Aspect | JWT | Database Sessions |
|--------|-----|-------------------|
| **State** | Stateless (self-contained) | Stateful (server-side) |
| **Storage** | Client-side | Server-side database |
| **Revocation** | Difficult (until expiry) | Instant |
| **Scalability** | Easier (no DB lookups) | Harder (DB required) |
| **Payload size** | Larger (contains all data) | Small (just session ID) |
| **Cookie size** | Large | Small |
| **Security** | Depends on storage | HttpOnly cookie is safer |

## When to Use Which

### Use JWT When:

- You need stateless authentication across services
- You're building microservices or distributed systems
- You don't need instant revocation
- Cross-origin authentication is required (mobile app + web)

### Use Database Sessions When:

- You need instant session revocation
- You want to store sensitive data in sessions
- GDPR compliance requires "right to be forgotten" revocation
- You need server-side session data (IP, device info)
- You want centralized session management

## Security Considerations

### JWT Security

- **Never store sensitive data in JWT payload** (easily decoded)
- **Always verify signature** — never trust tampered tokens
- **Set short expiration times** for access tokens
- **Use refresh tokens** for long-lived sessions

### Session Security

- **Use secure, random session IDs** (secrets.token_urlsafe)
- **Set HttpOnly cookies** to prevent XSS access
- **Implement CSRF protection** (SameSite cookie attribute)
- **Clean up expired sessions** regularly (cron job)

## Related Concepts

- [[authentication]] — Authentication fundamentals
- [[vercel-database-persistence]] — Database patterns on serverless platforms
- [[authentication]] — Authentication patterns

## References

- [JWT.io](https://jwt.io/) — JWT debugger
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/)
