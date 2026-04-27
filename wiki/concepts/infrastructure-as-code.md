---
title: Infrastructure-as-Code
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [iac, devops, infrastructure, terraform, ansible, configuration-management]
---

# Infrastructure-as-Code

## Overview

Infrastructure-as-Code (IaC) is the practice of managing and provisioning computing infrastructure through machine-readable configuration files rather than manual processes or interactive configuration tools. Instead of physically racking servers, adjusting network settings through a web UI, or running setup scripts by hand, IaC allows teams to define their entire infrastructure in code — servers, networks, databases, load balancers, and more — that can be versioned, reviewed, tested, and deployed automatically.

IaC is a foundational practice in modern [[DevOps]] and [[ci-cd]] pipelines. It eliminates the "it works on my machine" class of problems for infrastructure, because the same codified configuration that passes testing gets deployed to production. This dramatically reduces configuration drift — where production servers slowly diverge from their intended state due to one-off manual changes.

## Key Concepts

**Declarative vs. Imperative:** Most IaC tools operate declaratively, meaning you specify the desired end state (e.g., "there should be 3 web servers with 2 CPU cores each") and the tool figures out how to achieve it. Imperative approaches explicitly list the steps to take. [[Terraform]] by HashiCorp is the canonical declarative IaC tool; [[Ansible]] supports both but is often used imperatively.

**Idempotency:** A core IaC principle. Running the same IaC script multiple times should always produce the same result — applying the configuration if the resource doesn't exist, or doing nothing if it already matches the desired state. This prevents accidental duplication or destruction.

**State Management:** Tools like Terraform maintain a state file that maps real-world resources to your configuration. State can be stored locally or remotely (e.g., in S3 with DynamoDB locking), and must be handled carefully in team environments to avoid conflicts.

**Drift Detection:** IaC can detect when actual infrastructure has drifted away from the coded desired state, often due to manual changes, and reconcile it.

## How It Works

A typical IaC workflow looks like this:

1. **Write:** Define infrastructure in a domain-specific language (HCL for Terraform, YAML for Ansible, etc.)
2. **Plan:** Run a dry-run to see what changes will be made
3. **Apply:** Execute the plan to create, update, or destroy resources
4. **Verify:** Use the same code in CI to validate environment consistency

```hcl
# Terraform example: define an AWS EC2 instance
resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"
  tags = {
    Name        = "WebServer"
    Environment = "production"
    ManagedBy   = "IaC"
  }
}
```

The code above declares a single EC2 instance. In practice, IaC configurations span entire environments — VPCs, subnets, security groups, databases, DNS records, and more — all parameterized and composable.

## Practical Applications

- **Cloud Provisioning:** Spinning up multi-region AWS/Azure/GCP environments with consistent security rules
- **Environment Parity:** Creating identical dev, staging, and prod environments quickly
- **Disaster Recovery:** Redeploying entire infrastructures from code in minutes
- **Compliance:** Enforcing security baselines (e.g., encryption at rest, mandatory tags) across all resources
- **Self-Healing Infrastructure:** Combining IaC with auto-scaling groups to replace failed instances automatically

## Examples

- **Terraform** (HashiCorp) — cloud-agnostic, declarative, stateful; the industry standard for multi-cloud IaC
- **Ansible** (Red Hat) — agentless, YAML-based, can do both configuration management and provisioning
- **AWS CloudFormation** — native AWS, JSON/YAML, no external state file needed
- **Pulumi** — uses general-purpose programming languages (Python, TypeScript) instead of HCL
- **Crossplane** — extends Kubernetes to manage cloud infrastructure via CRDs

## Related Concepts

- [[Terraform]] — Leading declarative IaC tool
- [[Ansible]] — Configuration management and IaC tool
- [[CI-pipeline]] — Where IaC is typically integrated for automated testing/deployment
- [[Cloud]] — The primary target environment for IaC
- [[DevOps]] — The methodology IaC is core to
- [[Version Control]] — How IaC configurations are managed and collaborated on
- [[Configuration Management]] — The broader discipline IaC falls within

## Further Reading

- Terraform Documentation: https://www.terraform.io/docs
- "Infrastructure as Code" by Kief Morris (O'Reilly)
- Ansible Documentation: https://docs.ansible.com/

## Personal Notes

IaC transformed how I think about infrastructure. Once you have your environment codified, you can destroy and recreate it at will — this alone is worth the investment. The biggest mistake teams make is treating IaC as a one-time setup rather than an ongoing practice. Keep your IaC configs in version control, review them in pull requests, and run them through CI just like application code.
