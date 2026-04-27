---
title: "Cross Site Request Forgery"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags:
  - security
  - web-security
  - csrf
  - authentication
  - web-vulnerabilities
---

## Overview

Cross-Site Request Forgery (CSRF) is a web security vulnerability that allows an attacker to induce users into performing actions they did not intentionally authorize. The attack exploits the way browsers automatically include credentials like cookies with every request to a domain, regardless of the request's origin. If a user is logged into their bank and visits a malicious page, that page can silently trigger a transfer request to the bank—the browser obligingly includes the authentication cookie, making the request appear legitimate to the server. The user, seeing nothing suspicious, has no indication their action was triggered by an external site.

CSRF attacks succeed because web applications historically trusted all requests that included valid session credentials, without verifying that the request originated intentionally from the application's own UI. This trust model proved catastrophically flawed as web usage expanded and attack techniques grew more sophisticated. The vulnerability appears in many forms: state-changing GET requests that should be POSTs, form submissions, AJAX calls, and even image or script loads that trigger side effects. Any action a user can perform—changing passwords, making purchases, modifying settings—can potentially be forged from a cross-site origin.

## Key Concepts

**Automatic credential inclusion** is the root mechanism enabling CSRF. Browsers automatically attach cookies, client certificates, or HTTP authentication credentials to requests destined for a domain. This design, which makes sense for legitimate session continuity, becomes dangerous when combined with state-changing operations. The browser cannot distinguish between a user clicking "Transfer Funds" on their bank's website and the same request triggered by JavaScript on an attacker's page.

**SameSite cookies** represent the most effective browser-level defense. When a cookie includes the `SameSite=Strict` attribute, browsers refuse to include it in any cross-site request. `SameSite=Lax` allows the cookie in top-level navigations (the user clicking a link) but blocks it in subrequests (images, scripts, frames). The modern default, `SameSite=Lax`, provides substantial protection while preserving usability, though full `Strict` offers the strongest guarantee.

**CSRF tokens** provide application-level protection by requiring an additional secret token with each state-changing request. The server generates a unique token per session or per request, embedding it in forms or AJAX calls. When the request reaches the server, it validates the token's presence and correctness. An attacker cannot obtain this token because it is never transmitted to third-party sites—cross-site pages can trigger requests but cannot read the response or access the token value.

**Origin and Referer headers** provide additional context about request sources. Servers can verify that the `Origin` or `Referer` header matches an expected value, rejecting requests that appear to originate from untrusted domains. However, these headers can sometimes be spoofed or omitted due to privacy extensions, browser bugs, or special cases like `file://` URLs, making them unreliable as sole defenses.

## How It Works

A CSRF attack unfolds through a deceptively simple sequence. First, the attacker identifies a vulnerable endpoint—a URL that performs some state-changing action (password change, email update, purchase initiation) and trusts the request solely based on authentication credentials. Second, the attacker constructs a proof-of-concept exploit, typically an HTML page or script that will automatically trigger the malicious request when the victim visits. Third, the attacker lures the victim to visit this page—through phishing, social media, compromised ad networks, or embedded content in comments or forums.

```html
<!-- Simple CSRF attack example -->
<!-- Victim is logged into vulnerable-bank.com -->

<html>
<body>
  <!-- Image tag triggers GET request (less common but possible) -->
  <img src="https://vulnerable-bank.com/transfer?to=attacker&amount=10000" 
       width="0" height="0">
  
  <!-- More commonly, auto-submitting form for POST actions -->
  <form action="https://vulnerable-bank.com/transfer" method="POST" 
        id="csrf-form" style="display:none;">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="10000">
  </form>
  
  <script>
    // Auto-submit on page load
    document.getElementById('csrf-form').submit();
  </script>
</body>
</html>
```

When the victim loads the attacker's page, their browser executes the malicious request. The browser includes all cookies for `vulnerable-bank.com`, including the session cookie proving the user is authenticated. The bank's server receives what appears to be a legitimate request—the user is authenticated, the parameters are correctly formatted—and processes the action. The victim loses funds without any indication that the transaction was triggered externally.

Defenses must be implemented server-side because clients alone cannot distinguish legitimate requests from forgeries. The server must verify that the request's origin is trusted and that the action was intentionally initiated by the authenticated user.

## Practical Applications

CSRF remains relevant despite browser SameSite cookie defaults because not all applications have migrated to SameSite-aware configurations, and some use cases require cookies that work across origins. **Legacy web applications** that predate SameSite cookie support may remain vulnerable if SameSite defaults to `None` (which requires `Secure` attribute) or if developers explicitly set `SameSite=None`. **APIs consumed by mobile or desktop applications** often require cross-origin cookie authentication, creating attack surface when those same endpoints are accessible from browsers.

**Single Sign-On (SSO) systems** present interesting CSRF considerations. An SSO login typically establishes a session cookie at the identity provider, then redirects to the service provider. Without proper CSRF protection on the SP callback, an attacker could log the victim into the attacker's account at the SP while the victim believes they're logged into their own account—a "login CSRF" attack that enables account takeover through association.

**JSON APIs** are not immune. While `<form>` submissions can't target JSON endpoints without CORS complications, AJAX requests can. If the API uses cookie-based authentication and doesn't properly implement CORS restrictions or CSRF tokens, cross-site requests can still succeed. Many APIs inadvertently allow cross-origin requests by accepting `Authorization` headers or cookies without proper origin validation.

## Examples

A social media CSRF vulnerability allows an attacker to force victims to follow the attacker's account, share the attacker's content, or modify their profile. The victim clicks a link in what appears to be a harmless quiz site, and meanwhile their browser sends a POST to the social network changing their email to an attacker-controlled address. Once the email changes, the attacker initiates a password reset and takes over the account completely.

A forum or blog with a CSRF vulnerability allows an attacker to modify the victim's account settings, post content in their name, or even delete their account. Moderators visiting a malicious page might unknowingly elevate attacker's privileges or demote legitimate users, disrupting community management.

## Related Concepts

- [[Same-Site Cookies]] - Browser mechanism for limiting cookie scope
- [[CSRF Tokens]] - Cryptographic tokens preventing forged requests
- [[Cross-Origin Resource Sharing]] - CORS controls affecting cross-site requests
- [[Web Security]] - Broader web application security landscape
- [[Session Management]] - Authentication mechanisms CSRF exploits
- [[XSS]] - Cross-site scripting, often used in combination with CSRF

## Further Reading

- OWASP CSRF Prevention Cheat Sheet
- SameSite cookie specification (RFC 6265bis)
- SameSite=Lax Explained - Web.dev guide to SameSite cookie migration
- PortSwigger Web Security Academy CSRF materials

## Personal Notes

SameSite cookies have dramatically reduced CSRF in modern applications, but the vulnerability taught an important lesson: never trust that a request's origin can be inferred from credentials alone. Every state-changing endpoint needs explicit verification that the request was intentionally initiated—whether through CSRF tokens, SameSite cookies, or custom headers. I've found that many developers misunderstand SameSite=Lax as "mostly safe"—it still allows top-level navigations, which means a victim clicking a link can trigger the request. For high-value actions like password changes or payment initiation, Strict or explicit CSRF token verification is more appropriate.
