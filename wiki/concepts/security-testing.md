---
title: "Security Testing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [security, testing, quality-assurance, penetration-testing, vulnerability-assessment, appsec]
---

# Security Testing

## Overview

Security testing is the process of evaluating a system, application, or infrastructure to identify vulnerabilities, weaknesses, and potential entry points that could be exploited by malicious actors. Unlike functional testing, which verifies that software behaves correctly according to specifications, security testing proactively searches for ways to make the system behave incorrectly in ways that compromise confidentiality, integrity, availability, or authentication. The goal is to find weaknesses before attackers do and provide actionable remediation guidance.

Security testing is not a single technique but a discipline encompassing multiple testing methodologies, each targeting different attack surfaces and threat vectors. Effective security testing combines automated scanning with manual penetration testing, static code analysis with dynamic runtime evaluation, and infrastructure testing with application-layer assessment. No single tool or approach provides complete coverage — a defense-in-depth strategy for testing is as important as a defense-in-depth strategy for security controls.

## Key Concepts

### The CIA Triad

Every security test evaluates controls against the three pillars of information security:

**Confidentiality** ensures that sensitive information is accessible only to authorized parties. Tests verify that data at rest and in transit is properly protected through encryption, access controls, and proper data classification. A confidentiality breach might involve an authorization flaw that allows User A to access User B's data, or a database misconfiguration that exposes sensitive records to the public internet.

**Integrity** ensures that data remains unaltered and trustworthy. Tests verify that systems prevent unauthorized modification of data, that audit trails capture changes, and that cryptographic mechanisms detect tampering. Integrity failures can result from missing input validation (allowing SQL injection or command injection), broken authentication (allowing impersonation), or missing integrity checks on data in transit.

**Availability** ensures that systems and data are accessible when needed. Tests look for denial-of-service vulnerabilities, resource exhaustion patterns, and architectural weaknesses that could cause outages. High-availability systems require testing not just for immediate availability impact but for gradual degradation under sustained attack.

### Vulnerability vs. Exploit

A **vulnerability** is a weakness in a system that could be exploited — a missing patch, a misconfiguration, a code defect. A vulnerability becomes a security incident only when it is **exploited**, meaning an attacker actually leverages the vulnerability to achieve unauthorized access or impact. Security testing prioritizes finding exploitable vulnerabilities, not just theoretical weaknesses. A system with thousands of theoretical vulnerabilities but zero exploitable weaknesses is more secure than a system with one critical remote code execution flaw.

**Risk assessment** combines the severity of a vulnerability (how much damage could an exploit cause), the likelihood of exploitation (is the attack surface exposed, is the exploit practical), and the business context (what data or systems are at risk). Security testing produces findings that engineering teams use to prioritize remediation based on actual risk, not just severity scores.

### Authentication and Authorization Testing

Authentication mechanisms verify user identity; authorization mechanisms verify what an authenticated user is permitted to do. Both are frequent sources of security flaws:

**Authentication testing** examines password policies, credential storage (are passwords hashed, not stored in plaintext?), session management (are session tokens properly generated, transmitted, and invalidated?), multi-factor authentication implementation, and account recovery mechanisms. Common findings include predictable session tokens, missing rate limiting on login endpoints, and credential exposure in logs or error messages.

**Authorization testing** verifies that access controls are correctly enforced at every layer — not just at the API layer but also at the database layer, file system layer, and within application logic. Horizontal privilege escalation (accessing other users' resources of the same type) and vertical privilege escalation (gaining admin access from a user account) are the two most common authorization failure patterns.

### Input Validation and Injection Attacks

All external input is a potential attack vector. Security testing evaluates how the system processes and validates input at every entry point:

**SQL Injection** occurs when user input is incorporated into database queries without proper sanitization, allowing attackers to modify query logic or extract data. Testing involves providing malicious input (e.g., `' OR '1'='1` in a login field) and observing whether it is executed as code rather than treated as data.

**Cross-Site Scripting (XSS)** occurs when user input is reflected in web pages without proper encoding, allowing attackers to execute JavaScript in victims' browsers. Testing involves injecting script tags or JavaScript event handlers in input fields and verifying whether the output is properly escaped.

**Command Injection** occurs when user input flows into operating system commands without sanitization. This is particularly dangerous in applications that execute shell commands based on user input — a successful exploit can give attackers full control of the server.

**Path Traversal** occurs when file paths constructed from user input are not validated, allowing attackers to access files outside the intended directory. Testing involves providing paths like `../../etc/passwd` and verifying whether the server returns unauthorized file contents.

## How It Works

### Static Application Security Testing (SAST)

SAST tools analyze source code without executing it, scanning for patterns known to be associated with vulnerabilities. Tools like SonarQube, Checkmarx, and Semgrep can identify potential SQL injection, XSS, hardcoded credentials, weak cryptography, and many other vulnerability classes during development. SAST integrates into IDEs for real-time feedback and into CI/CD pipelines for automated scanning on every commit.

SAST has limitations: it produces false positives (flagging code that looks suspicious but is actually safe) and cannot detect runtime vulnerabilities, configuration issues, or vulnerabilities that only manifest in deployed environments. It is most effective when tuned to the specific codebase to reduce noise and when developers are trained to investigate findings rather than dismiss them.

### Dynamic Application Security Testing (DAST)

DAST tools probe running applications, sending malformed and unexpected inputs and observing how the application responds. Tools like OWASP ZAP, Burp Suite, and Acunetix can identify reflected XSS, CSRF, information disclosure, and many other vulnerabilities without access to source code. DAST is particularly valuable because it tests the application as an attacker would see it — from the outside in.

DAST limitations include incomplete coverage (only links and forms that the crawler can discover), difficulty with authenticated testing (requires managing sessions and state), and inability to pinpoint the exact code location of vulnerabilities. Modern DAST tools include authenticated scanning modes and API scanning capabilities to address these gaps.

### Penetration Testing

Penetration testing (pen testing) involves skilled security professionals attempting to actively exploit vulnerabilities to demonstrate real-world attack impact. Unlike automated scanning, penetration testers use creativity, reasoning, and specialized tools to chain multiple vulnerabilities together into attack scenarios. A penetration test might demonstrate not just that an XSS vulnerability exists, but how it could be combined with a CSRF vulnerability to hijack administrator sessions and gain backend access.

Penetration tests are typically scoped by agreement — defining which systems, which attack vectors, and which types of attacks are in scope. Tests may be black-box (no knowledge of the system), gray-box (some knowledge, such as credentials), or white-box (full source code access). The output is a detailed report with proof-of-concept exploit code and specific remediation guidance.

```python
# Example: Python script demonstrating basic CSRF vulnerability check
import requests

# Check if CSRF tokens are present in forms
response = requests.get('https://example.com/form')
if 'csrf_token' in response.text or 'csrfToken' in response.text:
    print("CSRF protection detected")
else:
    print("WARNING: No CSRF token found in form")

# Test state-changing operation without token
session = requests.Session()
form_response = session.get('https://example.com/settings')
# Attempt to change email without CSRF token
exploit_response = session.post(
    'https://example.com/settings',
    data={'email': 'attacker@evil.com'}
)
if exploit_response.status_code == 200:
    print("WARNING: State change succeeded without CSRF token!")
```

### Runtime Protection and RASP

Runtime Application Self-Protection (RASP) instruments applications at runtime to detect and block attacks as they execute. Unlike WAFs that sit in front of applications, RASP instruments the application itself, giving it full context about what the application is doing and enabling more accurate detection with fewer false positives. RASP can detect and prevent SQL injection, command injection, and other attacks in real time, even against previously unknown attack patterns.

## Practical Applications

### CI/CD Pipeline Integration

Security testing should be integrated into CI/CD pipelines to catch vulnerabilities early and prevent them from reaching production. SAST scans code on every commit, DAST scans deployed applications in staging environments, and dependency scanners check for known vulnerabilities in third-party libraries. Pipeline gates can be configured to block deployments when critical vulnerabilities are found, though teams must manage false positives carefully to avoid "alert fatigue" that leads to ignoring security findings entirely.

```yaml
# Example: GitHub Actions security scanning workflow
name: Security Scans
on: [push, pull_request]

jobs:
  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Semgrep SAST
        run: |
          pip install semgrep
          semgrep --config=auto scan/

  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check dependencies
        run: |
          pip install safety
          safety check

  dast:
    runs-on: ubuntu-latest
    steps:
      - name: Run OWASP ZAP Scan
        run: |
          docker run -v $(pwd):/zap/wrk:rw \
            owasp/zap2docker-stable zap-baseline.py \
            -t https://staging.example.com \
            -r report.html
```

### Threat Modeling

Threat modeling is a structured approach to identifying, quantifying, and addressing security risks before testing begins. By diagramming data flows, identifying trust boundaries, and enumerating potential threats, teams can focus security testing effort on the highest-risk areas. STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) is a common threat modeling framework that maps potential attacks to specific security controls that must be tested.

## Examples

A real-world security testing engagement might proceed as follows:

1. **Reconnaissance**: The tester enumerates the application's attack surface — URLs, API endpoints, subdomains, third-party integrations — using automated tools and manual investigation.

2. **Authentication Testing**: The tester identifies all authentication mechanisms (OAuth, SAML, username/password, API keys) and tests for credential stuffing vulnerabilities, weak password policies, missing rate limiting, and session fixation issues.

3. **Authorization Testing**: Using multiple accounts with different privilege levels, the tester attempts horizontal privilege escalation (accessing another user's resources) and vertical privilege escalation (accessing admin functions from a user account).

4. **Input Validation Testing**: Every user-facing input is tested with payloads designed to trigger injection vulnerabilities — SQL injection in search fields and IDs, XSS in comment fields and URLs, command injection in file upload fields.

5. **Dependency Scanning**: The application's third-party libraries and dependencies are checked against vulnerability databases (CVE, OSINT) for known vulnerabilities.

6. **Reporting**: Findings are documented with severity ratings (Critical, High, Medium, Low), proof-of-concept descriptions, and specific remediation guidance prioritized by risk.

## Related Concepts

- [[penetration-testing]] — Manual exploitation-focused security assessment
- [[vulnerability-assessment]] — Systematic identification and evaluation of vulnerabilities
- [[OWASP]] — Open Web Application Security Project, a foundational resource for application security
- [[SQL-injection]] — Specific vulnerability class testing
- [[XSS]] — Cross-site scripting vulnerability class
- [[authentication]] — Identity verification mechanisms
- [[authorization]] — Access control mechanisms
- [[secure-coding]] — Development practices that prevent vulnerabilities

## Further Reading

- OWASP Top 10 — The ten most critical web application security risks
- \"The Web Application Hacker's Handbook\" by Dafydd Stuttard and Marcus Pinto
- NIST SP 800-53 — Security and Privacy Controls for Information Systems
- OWASP Testing Guide — Comprehensive web application security testing methodology

## Personal Notes

The most effective security testing programs combine automated tools with manual penetration testing. Automated scanners find known vulnerability patterns efficiently but miss business logic flaws, authentication bypasses, and novel attack chains. Manual testing catches what scanners miss but doesn't scale to cover every code path in every release. The sweet spot is automated scanning for every commit plus periodic manual penetration testing focused on critical functionality and high-risk areas. Security testing is never \"done\" — it must evolve as the application evolves and as new attack techniques emerge.
