---
title: SQL Injection
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [sql-injection, security, database, owasp, web-security]
---

# SQL Injection

## Overview

SQL injection is a code injection technique that exploits vulnerabilities in database query construction, allowing attackers to interfere with queries that applications make to their databases. By inserting malicious SQL code into input fields, query parameters, or other user-controllable data, attackers can read sensitive data (including credentials and personal information), modify database contents, execute administrative operations on the database, and in some cases, issue commands to the underlying operating system. SQL injection remains one of the most prevalent and dangerous web security vulnerabilities, consistently ranking in the OWASP Top 10 and responsible for numerous high-profile data breaches.

The vulnerability arises when applications incorporate user input into SQL queries without proper sanitization or parameterization. The root cause is mixing code (SQL statements) with data (user input) in the same string. When user input contains SQL metacharacters, the database engine may interpret them as SQL code rather than literal data, fundamentally changing the query's intended behavior.

Understanding SQL injection requires knowledge of both database systems and application security. Attackers exploit these vulnerabilities through systematic probing of application inputs, gradually refining their attacks based on observed behavior and error messages. Even when initial attempts fail, attackers gather information about database structure and application behavior that informs subsequent attempts.

## Key Concepts

Several concepts are essential for understanding and preventing SQL injection attacks.

**Query Construction** refers to how applications build SQL statements. Vulnerable approaches include string concatenation and string formatting that insert user input directly into SQL. Safe approaches use parameterized queries or prepared statements that separate SQL structure from data.

**SQL Metacharacters** are characters with special meaning in SQL syntax—quotes for strings, semicolons for statement termination, comments for truncating queries. User input containing these characters can break out of intended data contexts into SQL code contexts.

**Union-Based Attacks** leverage the SQL UNION operator to combine results from multiple tables. Attackers use this technique to extract data from tables unrelated to the application's original query by appending a UNION SELECT statement.

**Blind Injection** techniques apply when applications don't return database output but still behave differently based on query results. Attackers infer information by observing boolean conditions (true/false responses) or timing differences (time-based blind injection).

**Error-Based Injection** exploits detailed error messages returned by misconfigured databases. These errors reveal database structure, table names, and sometimes data values that inform further attacks.

## How It Works

SQL injection attacks exploit the trust relationship between applications and databases. When an application constructs queries dynamically, user input flows directly into the query string. If the database receives input that includes SQL code, it executes that code as part of the query.

A classic example involves login authentication. A vulnerable query might look like:

```sql
SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
```

If a user provides `admin' --` as the username, the query becomes:

```sql
SELECT * FROM users WHERE username = 'admin' --' AND password = ''
```

The `--` begins a SQL comment, causing the database to ignore the rest of the query, potentially authenticating the attacker as admin without knowing the password.

More sophisticated attacks extract data systematically. Attackers probe for vulnerability, identify the database type and version, enumerate tables and columns, and extract target data—all through carefully crafted inputs that return results through error messages, visible output, or behavioral differences.

```python
# Vulnerable Python code (DO NOT USE)
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

# Safe parameterized version
def get_user_safe(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    return cursor.fetchall()
```

## Practical Applications

SQL injection prevention requires defense in depth—multiple layers of controls that together reduce risk even if individual layers fail.

**Parameterized Queries** (prepared statements) are the most effective prevention, ensuring user input is always treated as data, never as SQL code. Every major database API supports parameterization, and this approach should be the default for all database queries.

**Input Validation** rejects obviously malicious input before it reaches the database query layer. Validation should be allowlist-based (accepting only known-good patterns) rather than blocklist-based (trying to block known-bad patterns), as attackers find ways around blocklists.

**Least Privilege Principle** limits what database accounts used by applications can do. If the application account only has SELECT permissions on needed tables, injection cannot modify data or drop tables.

**Web Application Firewalls** (WAFs) detect and block common injection patterns before they reach applications. WAFs provide defense-in-depth but should not replace secure coding practices.

## Examples

A real-world example: an e-commerce site's product search function used string concatenation to build queries. Attackers discovered that searching for `'; DROP TABLE products; --` would execute the attacker's SQL instead of searching. The vulnerability was fixed by rewriting the search to use parameterized queries, and an emergency patch prevented exploitation while the fix was deployed.

Another example: a healthcare application's patient lookup used user-controlled parameters in queries. Attackers exploited this to access patient records beyond their authorization by injecting `UNION SELECT` statements that extracted data from tables the application wasn't designed to expose. The breach affected millions of patient records and resulted in regulatory penalties.

## Related Concepts

- [[web-security]] — Web application security principles
- [[owasp]] — OWASP Top 10 and security guidelines
- [[database-security]] — Database security best practices
- [[parameterized-queries]] — Safe query construction
- [[input-validation]] — Input sanitization techniques
- [[data-breach]] — Breach prevention and response

## Further Reading

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection) — Comprehensive OWASP resource
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) — Prevention guidelines
- [PortSwigger SQL Injection](https://portswigger.net/web-security/sql-injection) — Interactive learning

## Personal Notes

SQL injection vulnerabilities often exist because developers don't understand how SQL interprets user input. Every database query should be written with the assumption that all user input is malicious until proven otherwise. I advocate for treating parameterized queries as the only acceptable approach—no exceptions for "internal" inputs or "trusted" sources. Static analysis tools can catch obvious cases during development, but security code review remains essential for identifying subtle vulnerabilities.
