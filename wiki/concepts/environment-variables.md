---
title: "Environment Variables"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [environment-variables, configuration, security, devops]
---

# Environment Variables

## Overview

Environment variables are named values that configure the behavior of processes and applications at the operating system level. They exist as key-value pairs that persist in a process's execution environment and can be queried by running programs to adjust their behavior without code changes. The concept originates from the Unix operating system philosophy of configuring software through the environment rather than hardcoded values, making systems more flexible and portable across different deployments.

When an operating system boots or a user logs in, the system initializes a set of environment variables that describe the runtime context. These include system-level variables like PATH (which directories contain executable programs), HOME (the current user's home directory), and SHELL (the default command interpreter). Applications can read these variables to locate resources, determine user preferences, or gate feature availability. The mechanism is language-agnostic: whether an application is written in Python, Java, Node.js, or compiled C, it can access environment variables through standard library functions or APIs provided by the runtime environment.

Environment variables differ from configuration files in several important ways. They are set at the process level and inherited by child processes, making them ideal for runtime configuration that needs to propagate through a process tree. They are also easier to manage in containerized and cloud-native deployments, where injecting environment variables is a standard mechanism for configuring applications at runtime. Because they are external to application code, they enable the same binary artifact to behave differently across environments such as development, staging, and production.

## Use Cases

The primary use case for environment variables is application configuration. Rather than embedding database connection strings, API endpoints, feature flags, or log levels directly in source code, applications read these values from the environment at startup or during execution. This separation allows the same application image to be deployed across multiple environments with different configurations, which is fundamental to modern deployment practices in [[DevOps]] pipelines.

Environment variables serve as a bridge between infrastructure and application code in [[containerization]] environments. In Docker, Kubernetes, and similar platforms, operators inject configuration through environment variables when creating containers or pods. This approach aligns with the twelve-factor app methodology, which prescribes storing configuration in the environment as one of its core principles for building robust cloud-native applications. Environment variables also integrate naturally with secret management systems, allowing sensitive values to be injected at runtime without being baked into container images.

Another common use case is controlling application behavior during development and testing. Developers can toggle debug modes, enable verbose logging, mock external services, or switch between test and production endpoints by modifying environment variables. This flexibility accelerates development workflows because engineers do not need to modify code or maintain multiple configuration files for different scenarios. In continuous integration and continuous deployment pipelines, environment variables carry deployment-specific information such as build numbers, git commit hashes, and deployment timestamps, which applications can record for auditing and traceability purposes.

## Security

Environment variables present significant security considerations that developers and operators must understand. The most critical concern is that environment variables are exposed to all child processes spawned by an application. If a parent process runs with elevated privileges, its environment variables including any secrets contained within them may be accessible to unprivileged child processes, creating a potential privilege escalation vector. Additionally, in many systems, environment variables of other users' processes can be inspected through the /proc filesystem, meaning sensitive values stored in environment variables on shared systems may not remain private.

Secrets stored in environment variables are vulnerable to accidental exposure through logging and monitoring systems. Application logs, container inspect commands, process status displays, and error reporting tools often include environment variable values, which can leak sensitive information if these logs are subsequently stored or transmitted without appropriate access controls. Some operating systems also write environment variables to core dumps and crash reports, further expanding the attack surface for sensitive data.

Best practices for handling sensitive environment variables include treating them as secrets by default and minimizing their use for highly sensitive data such as private keys or long-lived API credentials. For such values, dedicated secret management solutions like HashiCorp Vault, AWS Secrets Manager, or Kubernetes Secrets should be used instead, as these provide encryption at rest, access control, and audit logging. When environment variables must be used for secrets, applications should avoid printing them in logs, clear them before spawning child processes where unnecessary, and ensure proper file permissions prevent unauthorized access to shell history or process listings. Additionally, modern container runtimes and operating systems offer mechanisms to restrict environment variable inheritance and mark specific variables as protected, which should be leveraged in security-sensitive deployments.

## Related

- [[Configuration Management]] - The broader practice of managing application and system settings
- [[Secrets Management]] - Specialized tools and practices for handling sensitive credentials
- [[Containerization]] - Technology that relies heavily on environment variables for configuration
- [[DevOps]] - Development and operations practices where environment variables are fundamental
- [[Twelve-Factor App]] - Methodology that prescribes environment-based configuration
