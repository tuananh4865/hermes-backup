---
title: "Public Cloud"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, infrastructure, aws, azure, gcp]
---

## Overview

Public cloud refers to [[cloud-computing]] infrastructure that is owned and operated by third-party providers and delivered over the internet. In a public cloud model, computing resources like servers, storage, networking, and applications are hosted in the provider's data centers and shared across multiple organizations (tenants). Users access these resources on a pay-per-use basis, scaling consumption up or down as needed without investing in physical hardware.

The three major public cloud providers are Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP), though others like Oracle Cloud, IBM Cloud, and Alibaba Cloud serve specific market segments. Public cloud has become the dominant deployment model for enterprise computing, with market research indicating that over 60% of enterprise workloads now run in public cloud environments.

## Key Concepts

**Multi-Tenancy** is the foundational principle enabling public cloud economics. Multiple customers share the same physical infrastructure, with strong isolation between tenants through hardware virtualization and software-defined networking. This shared model allows providers to achieve economies of scale that individual organizations could not match.

**Service Models** define what responsibilities the provider handles. [[infrastructure-as-a-service|IaaS]] offers raw compute, storage, and networking (virtual machines, block storage, VPCs). Platform as a Service (PaaS) provides managed platforms for application development (databases, Kubernetes, function runtimes). [[saas|Software as a Service (SaaS)]] delivers complete applications (email, CRM, collaboration tools).

**Resource Pooling** means providers aggregate physical and virtual resources into elastic pools that can be dynamically assigned to customers. A customer needing 100 servers sees them as available instantly, even though physical hardware is shared across thousands of concurrent users.

**Elasticity and Scalability** are core advantages of public cloud. Resources can scale horizontally (adding more instances) or vertically (adding more power to existing instances) automatically based on demand. This eliminates the need to provision for peak capacity.

## How It Works

Public cloud providers operate massive, globally distributed data centers. When you create a virtual machine in AWS, it runs on one of millions of physical servers in data centers spread across regions and availability zones. The provider handles power, cooling, hardware maintenance, and physical security.

Access is provided through web consoles, command-line interfaces, and APIs. All major providers offer infrastructure-as-code capabilities:

```yaml
# Example: Cloud-agnostic infrastructure definition (Terraform)
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.medium"

  tags = {
    Name        = "WebServer"
    Environment = "production"
  }
}
```

The same conceptual code can provision infrastructure in Azure or GCP with provider changes, enabling multi-cloud architectures.

## Practical Applications

Public cloud serves virtually every computing need. Startups use it for rapid infrastructure deployment without capital expenditure. Enterprises migrate applications for elasticity during peak usage. Research institutions spin up massive compute clusters for simulations, then scale to zero when complete.

Common patterns include:
- **Web applications** with auto-scaling to handle variable traffic
- **Data lakes and analytics** using managed big data services
- **Machine learning** with GPU-enabled instances and managed ML platforms
- **Disaster recovery** replicating to multiple regions for resilience
- **Software development** with ephemeral environments for testing

## Examples

A typical three-tier web application architecture in public cloud:

```
┌─────────────────────────────────────────────────────────┐
│                     Route 53 / Cloud DNS                 │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Load Balancer (ALB / Azure LB)              │
└─────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌───────────┐     ┌───────────┐     ┌───────────┐
    │ Web Tier  │     │ Web Tier  │     │ Web Tier  │
    │ (EC2/VM)  │     │ (EC2/VM)  │     │ (EC2/VM)  │
    └───────────┘     └───────────┘     └───────────┘
            │               │               │
            └───────────────┼───────────────┘
                            ▼
    ┌─────────────────────────────────────────────────┐
    │              Managed Database (RDS/Cloud SQL)   │
    └─────────────────────────────────────────────────┘
                            │
                            ▼
    ┌─────────────────────────────────────────────────┐
    │              Object Storage (S3/Blob/GCS)        │
    └─────────────────────────────────────────────────┘
```

## Related Concepts

- [[private-cloud]] - On-premises cloud infrastructure for sensitive workloads
- [[hybrid-cloud]] - Combining public and private for specific requirements
- [[infrastructure-as-a-service]] - Core IaaS offerings
- [[cloud-computing]] - The broader computing paradigm
- [[edge-computing]] - Distributed computing near data sources

## Further Reading

- AWS Well-Architected Framework (free PDF from Amazon)
- Microsoft Azure Architecture Center
- Google Cloud Architecture Framework
- "Cloud Architecture Patterns" by Bill Wilder

## Personal Notes

Public cloud is not always cheaper than on-premises for steady-state workloads. The economics shine for variable workloads and new projects, but organizations should analyze total cost of ownership including data egress charges and vendor lock-in risks. Multi-cloud strategies can reduce dependency but increase operational complexity.
