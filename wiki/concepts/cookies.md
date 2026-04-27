---
title: "Cookies"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [http, web, http-headers, state-management, browser]
---

# Cookies

## Overview

HTTP cookies are small pieces of data that servers send to a user's web browser for storage and subsequent retrieval. The browser stores these key-value pairs locally and automatically includes them in subsequent HTTP requests to the same server. Cookies were introduced by Netscape Navigator in 1994 as a mechanism to maintain state across stateless HTTP connections, enabling features like session management, user authentication, shopping carts, and personalized preferences that modern web applications rely on.

Cookies operate through HTTP headers: the server sends a `Set-Cookie` header in its response, and the browser responds with a `Cookie` header on subsequent requests to the same domain. This simple mechanism powers much of the interactive web we use today, from keeping you logged into websites to remembering your language preferences across sessions.

## Key Concepts

### Cookie Attributes

Every cookie has a name and value, but several optional attributes control its behavior:

- **Domain**: Specifies which hosts can receive the cookie (e.g., `.example.com` matches all subdomains)
- **Path**: Restricts cookie to specific URL paths within the domain
- **Expires/Max-Age**: Determines cookie lifetime (session cookies are deleted when browser closes)
- **HttpOnly**: Prevents JavaScript access via `document.cookie`, mitigating XSS attacks
- **Secure**: Only transmits cookie over HTTPS connections
- **SameSite**: Controls cross-site request behavior (Strict, Lax, or None)

### Cookie Types

**Session Cookies** exist only during a browser session—they're deleted when the browser or tab closes. They're ideal for temporary data like shopping cart contents during a browsing session.

**Persistent Cookies** have a defined expiration date and remain on the device until that date or until manually deleted. These are used for features like "Remember Me" login functionality or storing long-term preferences.

**Third-Party Cookies** originate from a domain other than the one displayed in the address bar, typically set by advertisers or analytics services embedded as resources (images, scripts, iframes) on a page. These are now being phased out by major browsers due to privacy concerns.

## How It Works

When a server wants to set a cookie, it includes a `Set-Cookie` header in its HTTP response:

```http
Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Lax
```

On subsequent requests to the same domain and path, the browser automatically includes matching cookies:

```http
GET /dashboard HTTP/1.1
Host: example.com
Cookie: session_id=abc123
```

Servers read the `Cookie` header, parse the name-value pairs, and use the data for session lookup, authentication verification, or preference retrieval. This exchange happens invisibly for users but enables the stateful experiences we expect from web applications.

Modern web frameworks handle cookie management programmatically:

```javascript
// Setting a cookie in Express.js
res.cookie('preferences', JSON.stringify({ theme: 'dark' }), {
  maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
  httpOnly: true,
  secure: true,
  sameSite: 'strict'
});

// Reading cookies
const prefs = JSON.parse(req.cookies.preferences);
```

## Practical Applications

**Authentication**: Web applications use cookies to maintain logged-in state. After successful login, the server issues a session cookie containing a session identifier. Subsequent requests send this cookie, allowing the server to identify the user without requiring repeated login.

**Session Management**: Shopping carts, form progress saving, and multi-step workflows rely on cookies to maintain state across page navigations and even across browser sessions for anonymous users.

**Personalization**: Language preferences, display settings, and contentcustomization are commonly stored in cookies to provide a tailored experience across visits.

**Tracking and Analytics**: Third-party cookies have historically enabled cross-site tracking for advertising and analytics. Privacy regulations like GDPR and browser changes (Safari's ITP, Firefox's ETP) are transforming this landscape.

## Examples

A common pattern is the "Remember Me" checkbox on login forms:

```javascript
// Login handler
app.post('/login', (req, res) => {
  const user = authenticate(req.body.username, req.body.password);
  if (user) {
    const options = {
      httpOnly: true,
      secure: true,
      sameSite: 'lax'
    };
    if (req.body.rememberMe) {
      options.maxAge = 30 * 24 * 60 * 60 * 1000; // 30 days
    }
    res.cookie('auth_token', generateSessionToken(user), options);
    res.redirect('/dashboard');
  }
});
```

## Related Concepts

- [[Session Management]] - Server-side session handling often used alongside cookies
- [[Cross-Site Scripting]] - XSS attacks that cookies help protect against via HttpOnly flag
- [[Same-Origin Policy]] - Browser security mechanism that restricts cookie access
- [[Local Storage]] - Browser storage alternative to cookies with different characteristics
- [[HTTP Headers]] - The protocol mechanism through which cookies are transmitted

## Further Reading

- [HTTP State Management Mechanism (RFC 6265)](https://tools.ietf.org/html/rfc6265) - The official specification for cookies
- [Same-Site Cookies Explained](https://web.dev/samesite-cookies-explained/) - Comprehensive guide to SameSite attribute
- [MDN: Using HTTP cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies)

## Personal Notes

Cookies remain fundamental to web architecture despite their age. The deprecation of third-party cookies marks a significant shift—developers should prepare for a world without them by exploring first-party data strategies and respecting user privacy as a design principle rather than an afterthought.
