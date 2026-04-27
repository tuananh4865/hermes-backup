---
title: OAuth 2.0
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [oauth, security, authentication, authorization, protocol]
---

# OAuth 2.0

## Overview

OAuth 2.0 is an open standard authorization framework that enables applications to obtain limited access to user accounts on third-party services without exposing passwords. First published as RFC 6749 in 2012, OAuth 2.0 has become the foundational protocol for modern internet authorization, enabling the "Sign in with Google," "Connect with Facebook," and countless other social login experiences. It allows users to grant specific permissions to third-party applications while keeping their credentials secure—a critical capability in an ecosystem of interconnected services.

The key insight OAuth 2.0 provides is the concept of delegated authorization: instead of giving your password to an application (which would grant it full account access forever), you authorize a limited "access token" that the application can use to access specific resources for a limited time. This is authorization, not [[authentication]]—OAuth answers "what can this application do on your behalf?" rather than "who are you?"

Understanding OAuth 2.0 is essential for building secure applications that integrate with other services, implementing proper access control, and designing APIs that others can safely consume. The framework is widely used across web, mobile, and desktop applications, and its concepts underpin modern identity solutions like [[openid-connect]].

## Key Concepts

**Resource Owner**: The user who owns the data or service being accessed. When you authorize a third-party app to access your Google Drive, you are the resource owner.

**Client**: The application requesting access. It must be registered with the authorization server (e.g., Google) and receive a client ID and client secret.

**Authorization Server**: The service that authenticates the resource owner and issues access tokens. Google's authorization server, for example, handles the login flow and permission prompts.

**Resource Server**: The API that hosts the protected resources. Often the same as or closely related to the authorization server.

**Access Token**: A credential that grants specific access rights for a limited duration. The format varies (JWT, opaque) and is used to make API requests on behalf of the user.

**Refresh Token**: A credential that can be exchanged for a new access token when the current one expires, without requiring the user to re-authenticate. Not all flows include refresh tokens.

**Scope**: A parameter defining the specific permissions being requested (e.g., `read:email`, `profile`). Users approve specific scopes, and access is limited to those granted.

**Grant Types**: OAuth 2.0 defines several authorization flows, each suited to different client types and security requirements:
- **Authorization Code**: For server-side applications (most secure)
- **PKCE** (Proof Key for Code Exchange): Enhanced version for public clients
- **Client Credentials**: For machine-to-machine communication
- **Device Code**: For devices with limited input capabilities
- **Implicit**: Deprecated (was for browser-based apps)

## How It Works

The Authorization Code flow—the most commonly used and recommended approach—works as follows:

**Step 1: Authorization Request**
The client redirects the user to the authorization server with parameters including:
- `client_id`: Identifies the application
- `redirect_uri`: Where to return after authorization
- `scope`: Permissions being requested
- `state`: Random value to prevent CSRF attacks
- `response_type=code`: Indicates authorization code flow

**Step 2: User Authentication and Consent**
The user logs in (if not already) and sees a consent screen listing requested permissions. They approve or deny.

**Step 3: Authorization Code Grant**
If approved, the authorization server redirects back to the `redirect_uri` with a short-lived authorization code (e.g., `?code=abc123`).

**Step 4: Token Exchange**
The client server-side exchanges the code for tokens by making a direct back-channel request to the token endpoint with:
- `code`: The authorization code
- `client_id` and `client_secret`: To authenticate the client
- `redirect_uri`: Must match original request

**Step 5: Access Token Response**
The authorization server validates everything and returns:
- `access_token`: The credential for API requests
- `refresh_token`: For obtaining new access tokens later
- `expires_in`: Token lifetime in seconds

**Step 6: API Requests**
The client uses the access token in API requests, typically in an `Authorization: Bearer` header.

**PKCE (RFC 7636)** adds cryptographic proof that the same client that initiated the flow is completing it, preventing authorization code interception attacks on public clients (mobile apps, SPAs).

## Practical Applications

**Social Login**: Allowing users to sign in with existing accounts (Google, GitHub, Facebook) rather than creating new passwords. This improves user experience and reduces password-related security risks.

**API Access**: Granting third-party applications access to user data (like accessing your Twitter followers or Google Calendar) without sharing credentials.

**Microservices Authorization**: Using OAuth 2.0 tokens to authorize requests between services within a system, enabling stateless authorization checks.

**Single Sign-On (SSO)**: Enterprise environments use OAuth 2.0 (often with [[openid-connect]]) to enable employees to authenticate once and access multiple applications.

**Mobile App Integration**: Native apps use OAuth with PKCE to securely authenticate and access services without embedding credentials.

## Examples

```python
# Example: Implementing OAuth 2.0 Authorization Code flow with Flask
from flask import Flask, request, redirect, session
import requests
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# OAuth configuration
GOOGLE_CLIENT_ID = "your-client-id.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-client-secret"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_API_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
REDIRECT_URI = "http://localhost:5000/callback"

@app.route('/login')
def login():
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    
    auth_params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'offline',  # Gets refresh token
        'prompt': 'consent'
    }
    
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join(f'{k}={v}' for k,v in auth_params.items())}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Verify state to prevent CSRF
    if request.args.get('state') != session.get('oauth_state'):
        return "Invalid state parameter", 400
    
    code = request.args.get('code')
    
    # Exchange code for tokens
    token_data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    tokens = token_response.json()
    
    # Use access token to get user info
    headers = {'Authorization': f"Bearer {tokens['access_token']}"}
    user_info = requests.get(GOOGLE_API_URL, headers=headers).json()
    
    session['user'] = user_info
    return f"Hello, {user_info.get('name')}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
```

**Example token response structure**:
```json
{
  "access_token": "ya29.a0AfH6...",
  "expires_in": 3599,
  "refresh_token": "1//0g...",
  "token_type": "Bearer",
  "scope": "openid email profile"
}
```

**API request with Bearer token**:
```http
GET /v2/userinfo HTTP/1.1
Host: www.googleapis.com
Authorization: Bearer ya29.a0AfH6...
```

## Related Concepts

- [[authentication]] — Identity verification (different from OAuth's authorization focus)
- [[openid-connect]] — Identity layer built on top of OAuth 2.0
- [[jwt]] — JSON Web Token, commonly used as OAuth access token format
- [[saml]] — Older XML-based SSO protocol
- [[api-gateway]] — Often handles token validation in production systems
- [[zero-trust]] — Security philosophy that OAuth embodies

## Further Reading

- [RFC 6749: OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749)
- [OAuth 2.0 Security Best Current Practice](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [RFC 7636: PKCE](https://datatracker.ietf.org/doc/html/rfc7636)
- [OAuth.com](https://www.oauth.com/) — Practical guide
- [Auth0: OAuth](https://auth0.com/intro-to-auth/what-is-oauth-2/) — Accessible explanation

## Personal Notes

I first implemented OAuth 2.0 when building a third-party integration that needed access to users' Google Drive files. The complexity of the flow was initially intimidating, but PKCE's availability now makes it much more accessible for public clients too. Security considerations are important—I once saw a demo where an improperly implemented flow leaked tokens. Key lessons: always verify state parameters for CSRF, never expose client secrets in client-side code, use HTTPS always, and prefer the authorization code + PKCE flow even for server apps. The refresh token mechanism enables long-lived sessions without repeated logins but must be stored securely. OAuth 2.0 with OpenID Connect has essentially won the identity federation space—understanding it is non-negotiable for modern web developers.
