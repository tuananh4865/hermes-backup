---
title: Web Security
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [security, web, cybersecurity, https, authentication, vulnerabilities]
---

# Web Security

## Overview

Web security encompasses the practices, technologies, and policies designed to protect web applications, APIs, and services from unauthorized access, data breaches, and malicious attacks. As organizations increasingly move critical functionality to web-based systems, the attack surface available to malicious actors has expanded dramatically. Web security addresses the unique challenges of securing systems that are, by design, accessible from anywhere in the world via the public internet—requiring defenses that function correctly even when operating under active attack by sophisticated adversaries.

The field spans multiple layers—network infrastructure, server configuration, application logic, client-side code, and user behavior—and involves understanding both defensive measures and the offensive techniques attackers use to identify and exploit vulnerabilities. Web security is not a product that can be purchased and installed but rather an ongoing discipline requiring continuous vigilance, regular assessment, and rapid response to newly discovered threats.

## Key Concepts

**The OWASP Top 10** is a standardized awareness document representing the ten most critical security risks to web applications, developed by the Open Web Application Security Project. The list—currently featuring injection flaws, broken authentication, sensitive data exposure, XML external entities (XXE), broken access control, security misconfigurations, cross-site scripting (XSS), insecure deserialization, using components with known vulnerabilities, and insufficient logging—represents the most common vulnerabilities found in web applications. Security teams use the OWASP Top 10 as a starting point for security education, code review checklists, and penetration testing scopes.

**Authentication and Authorization** form the cornerstone of access control in web applications. Authentication verifies user identity (typically through passwords, biometrics, or token-based systems), while authorization determines what authenticated users are permitted to do. The distinction matters: a user may be properly authenticated but lack authorization for a particular action. Vulnerabilities arise when applications confuse these concepts or fail to enforce authorization checks consistently across all code paths.

**Transport Layer Security (TLS)** encrypts data in transit between clients and servers, preventing eavesdropping and man-in-the-middle attacks. HTTPS (HTTP over TLS) should be used for all web traffic, not just login pages. Modern web browsers now actively warn users when they visit sites without HTTPS, and features like HTTP Strict Transport Security (HSTS) enforce secure connections even for users who attempt HTTP access.

**Input Validation and Output Encoding** are fundamental defenses against injection attacks. Validating that user input conforms to expected formats, lengths, and character sets prevents malformed data from causing unexpected behavior. Output encoding—converting special characters to safe equivalents—prevents injected content from being interpreted as code when displayed, defending against cross-site scripting.

## How It Works

Web application security relies on defense in depth—layering multiple independent security controls so that no single failure results in compromise. A typical security architecture includes network-level protections (firewalls, intrusion detection), server hardening (minimal installations, rapid patching), application-level defenses (authentication, access controls, input validation), and monitoring (logging, alerting, incident response).

```
Secure Development Lifecycle Integration:

1. Design Phase
   └── Threat modeling identifies attack surfaces and required controls
   
2. Development Phase
   └── Secure coding guidelines, static analysis tools, peer review
   
3. Testing Phase
   └── Dynamic analysis, penetration testing, vulnerability scanning
   
4. Deployment Phase
   └── Configuration hardening, security scanning, baseline validation
   
5. Operations Phase
   └── Continuous monitoring, incident response, regular patching
```

Security headers (Content-Security-Policy, X-Frame-Options, X-Content-Type-Options) instruct browsers to enforce additional protections. Content Security Policy can significantly reduce XSS risk by specifying which sources of content are legitimate. Web Application Firewalls (WAFs) provide an additional layer of protection by filtering malicious traffic before it reaches application code.

## Practical Applications

**E-commerce platforms** must protect customer payment information, requiring compliance with PCI DSS standards, encryption of cardholder data, and strict access controls around payment processing systems. A single breach can result in thousands of compromised payment cards and significant reputational damage.

**SaaS applications** face unique security challenges around multi-tenancy—ensuring that one customer's data cannot be accessed by another, that workloads are properly isolated, and that shared infrastructure does not create cross-tenant vulnerabilities.

**APIs** have emerged as critical attack vectors as mobile applications and microservices architectures increasingly rely on programmatic interfaces. API security requires attention to authentication (API keys, OAuth tokens), rate limiting, input validation, and proper error handling that does not expose internal implementation details.

## Examples

```http
# Example security headers in HTTP response

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-random123'
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
```

```python
# Example: Secure password hashing in Python
import hashlib
import secrets

def hash_password(password: str) -> tuple[str, str]:
    """Hash password using PBKDF2 with salt."""
    salt = secrets.token_hex(32)  # 256-bit random salt
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # iterations - higher = slower but more secure
    )
    return salt, hash_obj.hex()

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return secrets.compare_digest(hash_obj.hex(), stored_hash)
```

## Related Concepts

- [[authentication]] — Verifying user identity
- [[authorization]] — Controlling access to resources
- [[xss]] — Cross-site scripting vulnerabilities
- [[sql-injection]] — Database attack technique
- [[https]] — Secure HTTP transport
- [[owasp]] — Security community and standards

## Further Reading

- OWASP Top 10 (current edition) | owasp.org
- "The Web Application Hacker's Handbook" by Dafydd Stuttard and Marcus Pinto
- NIST Special Publication 800-63 Digital Identity Guidelines

## Personal Notes

Web security is a field where staying current truly matters. New vulnerabilities are discovered regularly; attack techniques evolve; defensive tools and frameworks change. What was considered secure five years ago may have fundamental flaws by today's standards. The most effective security practitioners combine deep technical knowledge with an attacker's mindset—understanding not just how systems are supposed to work, but how they can be made to misbehave. Security is also everyone's responsibility; even the most carefully designed application can be compromised through social engineering, supply chain vulnerabilities, or misconfiguration in deployment.
