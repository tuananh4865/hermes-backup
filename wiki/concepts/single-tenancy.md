---
title: "Single-Tenancy"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, single-tenancy, dedicated-infrastructure, isolation, enterprise]
---

# Single-Tenancy

## Overview

Single-tenancy is a software deployment model where each customer (tenant) receives dedicated infrastructure resources exclusively allocated to their organization. Unlike [[multi-tenancy]] where multiple customers share the same physical resources, single-tenancy provides complete isolation—one tenant's data, workloads, and system state are entirely separate from all others. This model is the traditional approach to enterprise software deployment and remains preferred in scenarios requiring maximum control, security, and compliance assurance.

The fundamental characteristic of single-tenancy is the one-to-one mapping between customer and infrastructure. When an organization subscribes to a single-tenant application, they receive their own dedicated database instance, application servers, storage volumes, and often network segments. This dedicated allocation eliminates noisy neighbor problems entirely—another tenant's workload cannot impact performance, and security boundaries are enforced at the hardware level rather than through logical controls.

Single-tenancy has historical precedence, emerging from the era of on-premises software where each enterprise installed applications on dedicated servers. The model persists in cloud computing through dedicated instance offerings, private cloud deployments, and specialized SaaS products serving regulated industries. While often contrasted with multi-tenancy, the two models exist on a spectrum—single-tenancy can incorporate shared components at the network or storage layer while maintaining strict isolation at critical layers.

## Key Concepts

Single-tenancy involves several architectural decisions that distinguish it from shared deployment models.

**Dedicated Resource Allocation** ensures each tenant receives guaranteed capacity. CPU, memory, storage, and network bandwidth are provisioned specifically for one customer and are not subject to contention from other workloads. This guarantee is particularly valuable for production systems with strict latency or throughput requirements. Predictable performance simplifies capacity planning and enables reliable SLAs.

**Deployment Isolation Models** vary in how they achieve separation. The strongest form runs entirely separate infrastructure—dedicated servers in dedicated data centers, network segments, and backup systems. More commonly, single-tenancy is implemented within a shared cloud environment using dedicated hosts (AWS Dedicated Hosts, Azure Dedicated Hosts, Google Cloud Sole Tenancy), which provide physical isolation at the host level while sharing underlying facility infrastructure.

**Data Sovereignty** is often cited as a driver for single-tenancy. Organizations in regulated industries may be required to store data within specific geographic boundaries, under specific organizational controls, or with specific audit capabilities. Single-tenancy enables explicit demonstration that data remains isolated—critical for compliance with GDPR, HIPAA, PCI-DSS, and sector-specific regulations.

**Customization Flexibility** distinguishes single-tenancy from multi-tenant alternatives. Since the infrastructure belongs to one organization, they can modify operating systems, install custom agents, tune database parameters, and implement specialized security controls without affecting other tenants. This flexibility supports legacy integration and unusual requirements that wouldn't be feasible in shared environments.

## How It Works

Single-tenant deployments can be implemented through various architectural approaches depending on the deployment environment and isolation requirements.

**Bare Metal Dedicated Servers** represent the strongest isolation model. The tenant receives physical servers located in colocation facilities or dedicated cloud instances. No hypervisor shares resources between tenants; the organization has direct hardware access. This approach suits workloads with extreme security requirements, regulatory mandates for hardware-level isolation, or performance-critical applications requiring predictable access to physical resources.

```hcl
# Terraform configuration for dedicated host allocation
resource "aws_dedicated_host" "company_host" {
  instance_type     = "r5.4xlarge"
  availability_zone = "us-east-1a"
  host_recovery     = "on"
  tags = {
    Name        = "company-dedicated-host"
    Environment = "production"
    Tenant      = "company-corp"
  }
}

resource "aws_instance" "app_server" {
  instance_type      = "r5.4xlarge"
  dedicated_host     = aws_dedicated_host.company_host.id
  availability_zone  = "us-east-1a"
  
  root_block_device {
    volume_size = 500
    volume_type = "gp3"
    encrypted   = true
  }
  
  tags = {
    Name        = "company-app-server"
    Environment = "production"
    ManagedBy   = "terraform"
  }
}
```

**Virtual Private Cloud (VPC)** isolation creates a logically isolated network segment for each tenant within shared cloud infrastructure. While compute resources may be virtualized, network traffic remains completely separated through VPC routing tables, security groups, and network ACLs. VPC peering or VPN connections connect the isolated tenant network to the organization's existing infrastructure.

**Database Instance Isolation** dedicates one database server per tenant. Whether using PostgreSQL, MySQL, Oracle, or SQL Server, each tenant receives their own database instance with dedicated CPU, memory, and storage. This approach eliminates the risk of query-level interference between tenants but increases operational complexity and cost at scale.

**Application Container Isolation** uses container technology (Docker, Kubernetes) to deploy tenant applications in isolated runtime environments. While containers on the same host may share the OS kernel, resource constraints, security contexts, and network policies enforce separation. Kubernetes namespaces provide additional isolation primitives including resource quotas, network policies, and access controls scoped to each tenant.

## Practical Applications

Single-tenancy serves diverse use cases where isolation, compliance, or customization requirements outweigh cost considerations.

**Financial Trading Platforms** require single-tenancy for regulatory compliance and competitive secrecy. Trading firms cannot risk information leakage to competitors, and regulators may require explicit isolation of customer funds and positions. Sub-millisecond latency requirements also favor dedicated resources where shared hypervisor overhead is unacceptable.

**Healthcare Systems** handling protected health information (PHI) often mandate single-tenancy to simplify HIPAA compliance. While HIPAA doesn't explicitly require dedicated infrastructure, demonstrating compliance is simpler when data isolation is enforced at the hardware level. Audit trails are cleaner, and breach notification obligations are clearer when data boundaries are well-defined.

**Government and Defense Systems** frequently require air-gapped or highly isolated environments that preclude shared infrastructure. Security classifications, chain of custody requirements, and national security considerations drive single-tenancy adoption. Government clouds like AWS GovCloud and Azure Government implement single-tenancy at the infrastructure level to meet these requirements.

**Enterprise Software with Complex Customization** scenarios benefit from single-tenancy when organizations require deep modifications to application behavior. ERPs, CRMs, and industry-specific software that require custom extensions, integrations, or configurations often deploy as single-tenant to avoid modification conflicts and simplify upgrade paths. The dedicated environment accommodates customization without impacting other users.

## Examples

A Kubernetes deployment configuration for a single-tenant application with enhanced isolation:

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tenant-finance-org
  labels:
    tenant: finance-org
    isolation: dedicated
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: finance-quota
  namespace: tenant-finance-org
spec:
  hard:
    requests.cpu: "16"
    requests.memory: 64Gi
    limits.cpu: "32"
    limits.memory: 128Gi
    persistentvolumeclaims: "10"
    pods: "50"
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: tenant-isolation
  namespace: tenant-finance-org
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
  # Allow only specified ingress sources
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
  # Deny all other traffic by default
---
apiVersion: v1
kind: Secret
metadata:
  name: tenant-secrets
  namespace: tenant-finance-org
type: Opaque
stringData:
  db-connection: "postgresql://finance专用连接"
  api-key: "sk-live-dedicated-tenant-key"
```

## Related Concepts

- [[multi-tenancy]] — Shared infrastructure serving multiple tenants
- [[private-cloud]] — Single-organization cloud infrastructure
- [[dedicated-host]] — Physical servers dedicated to one customer
- [[virtual-private-cloud]] — Isolated logical network in public cloud
- [[infrastructure-as-code]] — Managing infrastructure through code
- [[container-orchestration]] — Managing containers at scale
- [[compliance]] — Regulatory and standards compliance

## Further Reading

- AWS Dedicated Hosts Documentation
- Azure Dedicated Hosts Overview
- NIST SP 800-53 — Security and Privacy Controls for Information Systems
- "HIPAA Compliant Cloud Architecture" — ISACA Journal
- Google Cloud Sole Tenant Nodes Documentation

## Personal Notes

Single-tenancy has fallen out of fashion in the era of cloud-native SaaS, but it remains the right choice for specific scenarios. The decision framework I use: if you have regulatory requirements for hardware isolation, if your tenants are competitors who would be harmed by any data proximity, or if your customization requirements are so deep that multi-tenancy introduces unacceptable complexity—single-tenancy is worth the premium.

The cost differential is real but often overstated. Yes, you lose statistical multiplexing, but you also gain simpler operations (no tenant-scoped queries, no noisy neighbor debugging), clearer billing attribution, and stronger compliance posture. For large enterprises, the operational simplicity often justifies the infrastructure cost.

Watch for "single-tenancy theater"—vendors who claim single-tenancy but actually implement shared infrastructure with logical isolation. True single-tenancy requires dedicated hardware, dedicated network segments, and independent failure domains. Ask specifically: if another tenant's application is compromised, can they access my data? If the answer involves any logical control (access policies, query filtering, encryption key management), you're in multi-tenancy territory with extra steps.
