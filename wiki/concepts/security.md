---
title: "Security"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [security, vulnerabilities, owasp, web]
---

# Security

## Overview

Security in software development refers to the practice of protecting applications, systems, and data from unauthorized access, damage, or exploitation. Application security encompasses the measures taken to identify, mitigate, and prevent vulnerabilities throughout the software development lifecycle. Effective security requires a defense-in-depth approach, layering multiple protective mechanisms so that the failure of any single control does not compromise the entire system.

Security is not an afterthought but a fundamental quality attribute that must be considered from the design phase through deployment and maintenance. It involves understanding potential threats, attack vectors, and the potential impact of security breaches on users, organizations, and stakeholders.

## Common Threats

### OWASP Top 10

The Open Web Application Security Project (OWASP) maintains a widely recognized list of the most critical web application security risks. The current OWASP Top 10 includes: Broken Access Control, Cryptographic Failures, Injection, Insecure Design, Security Misconfiguration, Vulnerable and Outdated Components, Identification and Authentication Failures, Software and Data Integrity Failures, Security Logging and Monitoring Failures, and Server-Side Request Forgery. These categories represent the most prevalent and impactful vulnerabilities found in modern web applications.

### Injection

Injection attacks occur when untrusted data is sent to an interpreter as part of a command or query. SQL injection exploits vulnerabilities in database queries by inserting malicious SQL code through user input. Cross-Site Scripting (XSS) injects malicious scripts into web pages viewed by other users. Cross-Site Request Forgery (CSRF) tricks authenticated users into submitting unwanted requests to a web application.

### Authentication vs Authorization

Authentication and authorization are distinct but complementary security concepts. Authentication verifies the identity of a user or system, confirming that they are who they claim to be through credentials like passwords, biometrics, or tokens. Authorization determines what actions an authenticated user is permitted to perform, governing access to specific resources based on policies and permissions. Both must be properly implemented to maintain secure access control.

## Best Practices

Secure software development follows established practices to minimize vulnerabilities. Input validation ensures that all user-supplied data is checked for format, length, and content before processing. Output encoding prevents injection attacks by properly escaping special characters in generated content. Parameterized queries and prepared statements protect against SQL injection by separating code from data.

Security testing should be integrated into the development workflow through static analysis, dynamic testing, and penetration testing. Dependencies should be regularly audited and kept up to date to address known vulnerabilities. Principle of least privilege limits access rights to the minimum necessary for each user or component to function.

Logging and monitoring enable detection of security incidents and provide forensic information for incident response. Cryptography should be applied correctly using well-vetted algorithms and proper key management. Security awareness training helps developers recognize and avoid common pitfalls.

## Related

- [[web]] — Web security operates within broader web technology considerations
- [[authentication]] — Authentication mechanisms for verifying user identity
- [[authorization]] — Authorization models for access control decisions
- [[sql-injection]] — Detailed discussion of SQL injection attacks
- [[xss]] — Cross-site scripting prevention techniques
- [[csrf]] — Cross-site request forgery protection
- [[owasp]] — The OWASP Foundation and its security resources
