---
title: CSRF
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [csrf, security, web, vulnerability]
---

# CSRF (Cross-Site Request Forgery)

## Overview

Cross-Site Request Forgery (CSRF) is a web-based security vulnerability that allows an attacker to induce users into performing actions they did not intentionally authorize. In a CSRF attack, the victim's browser is tricked into sending an HTTP request to a target site (such as a bank, social media platform, or web application), and the browser automatically includes the user's cookies, session tokens, or other credentials. Because the server cannot distinguish between a legitimate request initiated by the user and a forged request injected by an attacker, the action is executed as if it were the user's own request.

CSRF attacks are particularly insidious because they exploit the trust a web application has in a user's browser. Unlike vulnerabilities that target the server directly, CSRF leverages the browser's automatic credential inclusion to impersonate the user. This makes CSRF relevant to any web application that relies solely on session cookies or HTTP Basic authentication without additional verification mechanisms.

## How It Works

A typical CSRF attack unfolds in several stages. First, the attacker identifies a vulnerable endpoint within a web application that performs some state-changing action—such as transferring funds, changing account settings, or deleting data. The attacker then crafts a malicious HTML page or injects hostile code into a page the victim is likely to visit. This malicious resource contains an auto-submitting form or a script that triggers a request to the target endpoint.

When the victim visits the attacker's page while logged into the vulnerable site, the browser automatically includes the victim's session cookies with the request. The server receives what appears to be a legitimate request from the authenticated user and executes the action. Because the request originates from the victim's browser, the attacker never sees the response—but the damage is done.

```
<!-- Example of a CSRF attack vector -->
<html>
  <body>
    <form action="https://bank.example.com/transfer" method="POST" id="csrf">
      <input type="hidden" name="to" value="attacker" />
      <input type="hidden" name="amount" value="10000" />
    </form>
    <script>document.getElementById('csrf').submit();</script>
  </body>
</html>
```

## Key Concepts

**SameSite Cookies** — Modern browsers support the `SameSite` attribute on cookies, which controls whether cookies are sent with cross-site requests. Setting `SameSite=Strict` prevents cookies from being sent on any cross-site request, effectively blocking CSRF attacks. `SameSite=Lax` allows cookies to be sent only for top-level navigations but not for subrequests like form POSTs.

**Anti-CSRF Tokens** — The most common defense against CSRF is the use of synchronizer tokens. When a user loads a form, the server generates a unique, unpredictable token and embeds it as a hidden field. When the form is submitted, the server verifies that the token matches the one stored in the user's session. Since the attacker's page cannot read or retrieve this token due to the Same-Origin Policy, forged requests will lack the correct token and be rejected.

**Origin and Referer Headers** — Servers can inspect the `Origin` or `Referer` HTTP headers to verify that a request originated from the expected site. While these headers can be spoofed in some scenarios, they provide an additional layer of defense when combined with other measures.

## Practical Applications

CSRF protection is a standard requirement for any web application handling sensitive operations. Banking and financial applications absolutely require CSRF defenses to prevent unauthorized fund transfers. E-commerce platforms need protection for order placement, address changes, and payment processing. Administrative panels and content management systems must guard against configuration changes and user management actions.

## Related Concepts

- [[xss]] — Cross-site scripting, another prevalent web vulnerability often used in combination with CSRF
- [[web-security]] — The broader discipline of securing web applications
- [[same-site-cookies]] — Cookie attribute that helps mitigate CSRF
- [[session-management]] — How sessions are handled and protected

## Further Reading

- OWASP CSRF Prevention Cheat Sheet
- PortSwigger Web Security Academy: CSRF
- SameSite Cookies Explained (Mozilla Developer Network)

## Personal Notes

When auditing a new codebase, CSRF checks should be one of the first things to verify on any state-changing endpoint. The absence of anti-CSRF tokens on sensitive operations is a high-severity finding. It's also worth noting that modern frameworks like Ruby on Rails, Django, and Spring Security include CSRF protection by default—but developers sometimes disable it for APIs under the assumption that API clients will handle security differently, which can reintroduce the vulnerability.
