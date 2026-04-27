---
title: "Iaas"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, iaas, infrastructure, aws, virtualization]
---

# IaaS

## Overview

Infrastructure as a Service (IaaS) is a cloud computing service model that provides virtualized computing resources over the internet. IaaS offers fundamental compute, storage, and networking infrastructure on a pay-per-use basis, replacing traditional on-premises data centers. Users can provision virtual machines, storage volumes, and networks on demand without investing in physical hardware.

IaaS is the foundation layer of cloud computing services, sitting below Platform as a Service (PaaS) and Software as a Service (SaaS). It gives users the most control over infrastructure while abstracting away the physical hardware management.

## Key Concepts

**Virtual Machines (VMs)**: The core IaaS offering. Users can create, configure, and manage virtual server instances with specified vCPUs, memory, storage, and operating systems. Major providers offer various instance types optimized for compute, memory, storage, or GPU workloads.

**Elastic Compute Cloud (EC2)**: AWS's IaaS offering, along with similar services from other providers: Azure Virtual Machines, Google Compute Engine, and Oracle Cloud Infrastructure.

**Virtual Private Cloud (VPC)**: An isolated virtual network within a cloud provider's infrastructure. VPCs allow users to define IP address ranges, create subnets, configure route tables, and set up network gateways for secure connectivity.

**Block Storage**: Persistent storage volumes that can be attached to VMs. Examples include AWS EBS, Azure Disk Storage, and Google Persistent Disk. Block storage provides high-performance, durable storage for databases and applications.

**Object Storage**: Highly scalable, durable storage for unstructured data. AWS S3, Azure Blob Storage, and Google Cloud Storage offer RESTful APIs for storing and retrieving any amount of data.

**Load Balancing**: Distributing network traffic across multiple instances for high availability and performance. Cloud providers offer managed load balancers like AWS ELB, Azure Load Balancer, and Google Cloud Load Balancing.

## How It Works

IaaS architecture builds on virtualization technology:

1. **Physical Infrastructure**: Cloud providers maintain massive data centers with physical servers, networking equipment, and power systems.
2. **Virtualization Layer**: Hypervisors (Xen, KVM, VMware ESXi) create virtual machines by partitioning physical resources.
3. **Resource Pooling**: Multiple tenants share the underlying physical infrastructure while maintaining logical isolation.
4. **Orchestration**: Cloud providers use automated systems to provision, manage, and scale virtual resources based on user requests via API or web console.

```bash
# Example: AWS EC2 CLI commands to launch and manage instances
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --count 1 \
    --instance-type t3.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0

# SSH into the instance
ssh -i my-key-pair.pem ec2-user@<public-ip>

# Create and attach a volume
aws ec2 create-volume --size 100 --availability-zone us-east-1a
aws ec2 attach-volume --volume-id vol-0123456789abcdef0 --instance-id i-0123456789abcdef0 --device /dev/sdf
```

## Practical Applications

**Web Hosting**: Deploy web applications on scalable VM infrastructure without managing physical servers.

**Development and Testing**: Quickly provision and tear down development environments, reducing setup time from days to minutes.

**Disaster Recovery**: Replicate infrastructure to cloud environments for business continuity without maintaining a secondary data center.

**High-Performance Computing**: Run computational workloads on GPU-optimized instances for machine learning training, rendering, or simulations.

**Lift-and-Shift Migration**: Move existing applications to the cloud with minimal modifications to leverage cloud scalability.

## Examples

```yaml
# Terraform configuration for IaaS infrastructure
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web_server" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"
  
  tags = {
    Name        = "web-server"
    Environment = "production"
  }
}

resource "aws_security_group" "web_sg" {
  name        = "web-security-group"
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_ebs_volume" "data" {
  availability_zone = "us-east-1a"
  size              = 100
  
  tags = {
    Name = "data-volume"
  }
}
```

## Related Concepts

- [[Cloud Computing]] - The broader paradigm that includes IaaS
- [[PaaS]] - Platform as a Service, sits above IaaS in the stack
- [[SaaS]] - Software as a Service, the topmost cloud service model
- [[Virtualization]] - The technology enabling IaaS
- [[DevOps]] - Practices that often leverage IaaS for infrastructure automation
- [[Kubernetes]] - Container orchestration that often runs on IaaS infrastructure

## Further Reading

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/)
- [Microsoft Azure Architecture Center](https://learn.microsoft.com/azure/architecture/)
- [Google Cloud Architecture Framework](https://cloud.google.com/architecture/framework)

## Personal Notes

IaaS gives teams flexibility and speed compared to traditional infrastructure, but it also introduces complexity in security, cost management, and operations. Using infrastructure-as-code tools like Terraform helps manage this complexity systematically. Always consider the shared responsibility model—cloud providers secure the infrastructure, but you're responsible for everything running on it.
