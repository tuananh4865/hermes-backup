---
title: "Configuration Management"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [devops, infrastructure, automation, iac, configuration]
---

# Configuration Management

Configuration management is the practice of systematically managing, tracking, and controlling changes to software and infrastructure configurations throughout the software development lifecycle. It ensures consistency, traceability, and reproducibility across environments by treating configuration as code that can be versioned, reviewed, and automated.

## Overview

In modern software development, applications run across multiple environments—development, testing, staging, production—with each environment requiring specific configurations for databases, APIs, services, and infrastructure. Configuration management provides a systematic approach to handle these settings, preventing "works on my machine" problems and enabling reliable deployments.

Configuration management encompasses both application configuration (environment variables, feature flags, feature toggles) and infrastructure configuration (server settings, network configuration, installed packages). When done well, it provides a single source of truth for how systems should be configured, with audit trails showing exactly what changed, when, and why.

The shift from manual configuration to automated configuration management represents a fundamental improvement in operational reliability. When every configuration change is codified and tracked in version control, teams can reproduce any environment state, roll back problematic changes, and ensure new environments are identical to existing ones.

## Key Concepts

**Idempotency**: The property that applying a configuration multiple times produces the same result as applying it once. Good configuration management tools are idempotent—you can run them repeatedly without side effects.

**Drift Detection**: The ability to detect when the actual state of a system differs from its desired configuration state. Configuration management tools continuously check for drift and can optionally remediate it automatically.

**Secrets Management**: Separating sensitive data (passwords, API keys, certificates) from general configuration. Secrets should be encrypted, access-controlled, and injected at runtime rather than stored in plain text configuration files.

**Environment Parity**: Keeping development, staging, and production environments as similar as possible. Configuration management helps achieve this by applying the same configurations across all environments.

**Immutable Infrastructure**: Rather than modifying running servers, configuration management can provision new servers with the correct configuration and replace existing ones. This reduces drift and improves reliability.

## How It Works

Configuration management tools operate through a declarative model:

1. **Define Desired State**: Configuration is written as code (manifests, playbooks, charts) that describes the intended state of the system rather than step-by-step instructions.

2. **Store in Version Control**: Configuration files are committed to Git repositories, providing history, code review, and rollback capabilities.

3. **Execution/Agent**: A configuration management agent runs on target systems, reading the configuration definitions and applying necessary changes.

4. **Convergence**: The agent continuously ensures the system matches the desired state. If drift occurs (manual changes, external factors), the agent remediates it.

5. **Reporting**: The tool reports on compliance status, highlighting any differences between desired and actual state.

```yaml
# Example: Kubernetes ConfigMap (application configuration)
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "db.example.com"
  DATABASE_PORT: "5432"
  LOG_LEVEL: "info"
  FEATURE_FLAGS: |
    {
      "newCheckoutFlow": true,
      "betaFeatures": false
    }
---
# Example: Kubernetes Secret (sensitive data)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  DATABASE_PASSWORD: "s3cr3tP@ssw0rd"
  API_KEY: "sk-live-xxxxxxxxxxxx"
```

## Practical Applications

- **Database Configuration**: Managing database schemas, indexes, and initial data across environments. Migration scripts are a form of configuration management for database state.

- **Feature Flags**: Using configuration to enable/disable features without deploying code, enabling canary releases and A/B testing.

- **Environment-Specific Settings**: Different API endpoints, logging levels, or feature toggles per environment, all managed through the same codebase.

- **Compliance as Code**: Enforcing security policies (password policies, encryption settings, firewall rules) automatically rather than through manual audits.

- **Disaster Recovery**: Rebuilding infrastructure from scratch by applying configuration to new servers, ensuring recovery procedures work before they're needed.

## Examples

**Using Environment Variables with Container Applications**:
```dockerfile
# Dockerfile with environment-based configuration
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --production
COPY . .
EXPOSE 3000
ENV NODE_ENV=production
CMD ["node", "server.js"]
```

**Terraform for Infrastructure Configuration**:
```hcl
# Terraform configuration management example
resource "aws_instance" "app_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = var.instance_type
  
  tags = {
    Name        = "app-${var.environment}"
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}
```

## Related Concepts

- [[Infrastructure as Code]] — Treating infrastructure configuration as code
- [[DevOps]] — The cultural/engineering practice configuration management enables
- [[GitOps]] — Git-based workflow for configuration management
- [[Environment Variables]] — Common mechanism for application configuration
- [[Secrets Management]] — Secure handling of sensitive configuration
- [[Continuous Integration]] — How configuration changes are tested and validated

## Further Reading

- [Infrastructure as Code: What Is It? Why Is It Important?](https://www.hashicorp.com/resources/what-is-infrastructure-as-code) — HashiCorp overview
- [Ansible Documentation](https://docs.ansible.com/) — Popular configuration management tool
- [Terraform by HashiCorp](https://www.terraform.io/) — Infrastructure as code tool
- [12 Factor App](https://12factor.net/config) — Best practices for application configuration

## Personal Notes

Configuration management is often treated as an infrastructure concern, but application developers benefit just as much from treating configuration with the same care as code. Storing secrets in environment variables and using configuration files for non-sensitive settings has served me well. The key insight is to fail fast when required configuration is missing—many bugs in production are simply missing or incorrect configuration values that should have been caught during startup.
