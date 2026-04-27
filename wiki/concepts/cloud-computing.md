---
title: Cloud Computing
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [cloud-computing, iaas, paas, saas, aws]
---

# Cloud Computing

## Overview

Cloud computing is the delivery of on-demand computing resources over the internet, including servers, storage, databases, networking, software, and analytics. Instead of purchasing and maintaining physical hardware and data centers, organizations can access these resources from cloud service providers on a pay-as-you-go basis. This model eliminates the need for upfront capital expenditure and allows businesses to scale their infrastructure elastically based on demand.

The cloud computing paradigm represents a fundamental shift in how computing resources are provisioned and consumed. Users can access servers, storage, and applications from anywhere with an internet connection, rather than being tied to a specific physical location. Cloud providers maintain massive data centers distributed across multiple geographic regions, offering high availability, redundancy, and global reach. The on-demand nature of cloud services means that organizations can provision resources within seconds rather than waiting weeks or months for physical hardware to be delivered and installed.

Cloud computing underpins a vast ecosystem of modern digital services, from web applications and mobile backends to machine learning pipelines and big data analytics. Major cloud providers such as [[AWS]], [[Microsoft Azure]], and [[Google Cloud Platform]] offer hundreds of services covering compute, storage, database, networking, security, and specialized domains like artificial intelligence and Internet of Things. The flexibility and agility of cloud computing has made it the default choice for startups and enterprises alike, enabling rapid innovation and reducing time-to-market for new products and services.

## Service Models

Cloud computing offers three primary service models, each providing a different level of abstraction and control over the underlying infrastructure.

**Infrastructure as a Service (IaaS)** provides the most fundamental building blocks of computing. With IaaS, users rent virtual machines, storage, and networking resources from a cloud provider. The customer has control over the operating system, applications, and runtime environment, while the cloud provider manages the physical hardware, virtualization layer, and data center operations. [[IaaS]] offers maximum flexibility and control, making it suitable for organizations with specific infrastructure requirements or legacy applications to migrate. Popular IaaS offerings include [[Amazon EC2]], [[Azure Virtual Machines]], and [[Google Compute Engine]].

**Platform as a Service (PaaS)** abstracts away infrastructure management entirely, providing a complete development and deployment environment in the cloud. Developers can focus on writing application code without worrying about provisioning servers, configuring storage, or managing databases. [[PaaS]] offerings typically include runtime environments, middleware, development tools, and database services integrated into a cohesive platform. Examples include [[Heroku]], [[Google App Engine]], and [[Azure App Service]]. This model accelerates development cycles and is particularly attractive to software teams prioritizing productivity over infrastructure control.

**Software as a Service (SaaS)** delivers complete applications over the internet on a subscription basis. Users access software through a web browser or thin client without installing or maintaining anything locally. [[SaaS]] applications are fully managed by the provider, including updates, security patches, and infrastructure scaling. Familiar examples include [[Salesforce]], [[Microsoft 365]], [[Google Workspace]], and countless business applications. SaaS is the most user-friendly model, requiring minimal technical knowledge to adopt, but offers the least customization compared to IaaS and PaaS.

## Deployment Models

Cloud computing resources can be deployed through several different models, each with distinct characteristics regarding ownership, access, and management.

**Public Cloud** resources are owned and operated by third-party cloud providers and shared across multiple organizations. The provider manages all underlying infrastructure, and customers access resources over the internet on a self-service basis. [[Public Cloud]] deployment offers the lowest cost of entry and greatest scalability, as organizations only pay for what they consume. This model is ideal for workloads with variable demand, new projects requiring rapid provisioning, and organizations seeking to avoid capital expenditure on hardware.

**Private Cloud** refers to cloud computing resources used exclusively by a single organization. The infrastructure may be located in the organization's own data center or hosted by a third party, but it is dedicated solely to that customer. [[Private Cloud]] provides greater control over security, compliance, and data residency, making it suitable for industries with strict regulatory requirements such as healthcare, finance, and government. However, private cloud requires significant capital investment and ongoing operational overhead.

**Hybrid Cloud** combines public and private cloud resources, allowing data and applications to move between them. Organizations might run sensitive workloads on a private cloud while leveraging public cloud resources for burst capacity or disaster recovery purposes. [[Hybrid Cloud]] strategies provide flexibility to optimize costs while maintaining compliance and control where required. Many enterprises adopt hybrid approaches to gradually migrate to the cloud while keeping critical systems on-premises.

**Multi-Cloud** extends this concept further by using services from multiple public cloud providers simultaneously. This approach avoids vendor lock-in, improves resilience, and allows organizations to use best-of-breed services from different providers. However, managing complexity across multiple cloud platforms increases operational overhead and requires sophisticated orchestration and governance.

## Related

- [[Cloud Storage]] — Distributed data storage services in the cloud
- [[Virtualization]] — Foundation technology enabling cloud resource isolation
- [[Containerization]] — Lightweight application packaging technology
- [[Microservices]] — Architectural pattern commonly deployed in cloud environments
- [[Serverless]] — Cloud execution model where the provider manages infrastructure automatically
- [[Edge Computing]] — Distributed computing model that extends cloud capabilities to the network edge
- [[DevOps]] — Development practices that align with cloud-native workflows
