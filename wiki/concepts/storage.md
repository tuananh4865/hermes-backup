---
title: Storage
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [storage, cloud, data, persistence]
---

## Overview

Storage refers to the mechanisms and technologies used to retain digital data persistently. In modern computing, storage is a fundamental component that enables data to persist beyond the lifetime of a single process or session. Storage systems can be broadly categorized into [[local storage]] and [[cloud storage]], each offering distinct trade-offs in capacity, durability, accessibility, and cost.

Data persistence is critical for virtually every application, from operating systems that store files to databases that maintain structured records. The choice of storage architecture affects performance characteristics, scalability, and operational complexity.

## Types

### Block Storage

Block storage divides data into fixed-size blocks, each with a unique address. This approach provides fine-grained control over data placement and is optimized for high-throughput, low-latency operations. Block storage is commonly used for database workloads, virtual machine disks, and applications requiring consistent performance. Examples include Amazon Elastic Block Store (EBS) and Azure Disk Storage.

### File Storage

File storage organizes data in a hierarchical structure of directories and files. It abstracts data as files with paths, making it intuitive for human users and compatible with standard operating system interfaces. Network File System (NFS) and Server Message Block (SMB) are common file storage protocols. File storage suits shared file systems, content repositories, and legacy applications.

### Object Storage

Object storage treats data as discrete units called objects, each containing data, metadata, and a unique identifier. Objects are accessed via HTTP-based APIs, enabling broad compatibility and easy distribution. Object storage excels at scale, durability, and cost efficiency for unstructured data such as media files, backups, and data lakes. It is the foundation of most [[cloud storage]] services.

## Cloud Providers

### Amazon S3

Amazon Simple Storage Service (S3) is a widely adopted object storage service offering 11 nines of durability. S3 provides multiple storage classes optimized for different access patterns, including S3 Standard, S3 Infrequent Access, and S3 Glacier for archival. Its event-driven architecture integrates tightly with other AWS compute and analytics services.

### Google Cloud Storage (GCS)

Google Cloud Storage provides object storage with global availability and strong consistency. GCS offers similar storage classes to S3, including Standard, Nearline, Coldline, and Archive. It benefits from Google's global network infrastructure, delivering high performance for data-intensive workloads.

### Azure Blob Storage

Azure Blob Storage is Microsoft's object storage solution, optimized for massive-scale data workloads. Blob storage integrates with Azure's broader ecosystem, including Azure Files (file storage), Azure Disk Storage (block storage), and Azure Data Lake for analytics. It supports both hot and cool tiers to optimize costs.

## Related

- [[Local Storage]] — On-premises storage infrastructure
- [[Cloud Computing]] — Delivery of computing resources over networks
- [[Data Persistence]] — Techniques for maintaining data over time
- [[Database]] — Structured data storage and retrieval systems
- [[Backup and Recovery]] — Data protection and restoration strategies
