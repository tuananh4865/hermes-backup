---
title: "Terraform"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [infrastructure-as-code, devops, cloud, provisioning, hashicorp]
---

# Terraform

## Overview

Terraform is an open-source Infrastructure as Code (IaC) tool developed by HashiCorp that enables developers and operations teams to define, provision, and manage cloud infrastructure declaratively. Rather than manually configuring servers through cloud consoles or SSH, Terraform allows you to describe your desired infrastructure in configuration files and then applies those configurations to create, modify, or destroy resources across multiple cloud providers.

The core philosophy behind Terraform is immutable infrastructure—where instead of modifying running servers (which leads to configuration drift), you define infrastructure as code, destroy the old resources, and recreate them from the new definitions. This approach ensures reproducibility, version control, and consistency across environments. Terraform supports all major cloud providers including AWS, Azure, Google Cloud, and dozens of others through its provider ecosystem.

## Key Concepts

**Declarative Configuration**: In Terraform, you declare what resources you want rather than how to create them step-by-step. The Terraform engine determines the optimal order of operations and handles dependency resolution automatically. Your configuration files describe the desired end state, and Terraform figures out how to achieve that state.

**State Management**: Terraform maintains a state file that tracks the mapping between your configuration and the real-world infrastructure. This state is critical—it tells Terraform what resources it manages, their current attributes, and what changes need to be applied. State can be stored locally or remotely (using backends like S3, Azure Blob Storage, or HashiCorp Cloud), with remote state enabling team collaboration and state locking.

**Providers**: Providers are plugins that interface with cloud APIs, SaaS providers, and other services. The Terraform Registry hosts thousands of providers. Each provider exposes resources that map to infrastructure components—AWS providers give you `aws_instance`, `aws_s3_bucket`, `aws_vpc`, etc. Providers handle authentication, API interactions, and resource lifecycle management.

**Modules**: Modules are reusable, parameterized Terraform configurations. Instead of copying and pasting configuration blocks, you can encapsulate a set of resources into a module with input variables and output values. The Terraform Registry contains many community modules for common infrastructure patterns.

## How It Works

The Terraform workflow consists of three main stages:

1. **Write**: Define your infrastructure in `.tf` files using HashiCorp Configuration Language (HCL). These files declare resources, data sources, variables, and outputs.

2. **Plan**: Run `terraform plan` to create an execution plan. Terraform compares your desired state against the current state and shows what actions it will take—creating, updating, or destroying resources. This step lets you review changes before applying them.

3. **Apply**: Run `terraform apply` to execute the plan. Terraform makes API calls to your cloud provider to provision or modify resources. After completion, it updates the state file to reflect the new reality.

```hcl
# Example: Create an AWS EC2 instance
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name        = "WebServer"
    Environment = "production"
  }
}

output "public_ip" {
  value = aws_instance.web_server.public_ip
}
```

## Practical Applications

Terraform excels in scenarios where infrastructure needs to be consistent, version-controlled, and reproducible across multiple environments or teams.

**Multi-Cloud Deployments**: Organizations using multiple cloud providers can manage all infrastructure through a single tool. Terraform's provider architecture means the same HCL syntax works across AWS, Azure, GCP, and specialty providers like Cloudflare or Datadog.

**Environment Parity**: Development, staging, and production environments can be generated from the same configuration, ensuring that what works in development will work in production. Variable files or workspace concepts allow for environment-specific overrides.

**Disposable Environments**: For testing, demos, or temporary infrastructure, Terraform can spin up environments on demand and destroy them when no longer needed. This approach reduces costs and avoids infrastructure clutter.

## Examples

A complete web application stack might include networking, compute, database, and DNS resources:

```hcl
# VPC and networking
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
}

# RDS database
resource "aws_db_instance" "postgres" {
  identifier           = "mydb"
  engine               = "postgres"
  instance_class       = "db.t3.micro"
  allocated_storage    = 20
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
}

# Route 53 DNS
resource "aws_route53_record" "www" {
  zone_id = var.hosted_zone_id
  name    = "www.example.com"
  type    = "A"
  ttl     = 300
  records = [aws_instance.web_server.public_ip]
}
```

## Related Concepts

- [[Infrastructure as Code]] - The broader discipline Terraform belongs to
- [[Ansible]] - A complementary configuration management tool
- [[Kubernetes]] - Container orchestration often provisioned with Terraform
- [[AWS]] - Major cloud provider with extensive Terraform support
- [[Immutable Infrastructure]] - The philosophy of replacing rather than modifying infrastructure
- [[Packer]] - HashiCorp tool for creating machine images, often used with Terraform

## Further Reading

- [Terraform Documentation](https://www.terraform.io/docs)
- [Terraform Registry](https://registry.terraform.io/) - Providers and modules
- [HashiCorp Learn](https://learn.hashicorp.com/terraform) - Interactive tutorials
- [Terraform: Up & Running](https://www.terraformupandrunning.com/) - Essential book by Yevgeniy Brikman

## Personal Notes

Terraform's state management is both its greatest strength and its most tricky aspect. Always use remote state with state locking in production to prevent concurrent modifications. Learn to use `terraform import` to bring existing infrastructure under Terraform management. The `terraform graph` command is underutilized—it visualizes resource dependencies which is invaluable for debugging complex configurations. For large organizations, consider Terraform Cloud or Terragrunt for workspace management and state file organization.
