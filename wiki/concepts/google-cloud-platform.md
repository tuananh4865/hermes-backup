---
title: Google Cloud Platform
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [google-cloud-platform, GCP, cloud-computing, infrastructure, cloud]
---

# Google Cloud Platform

## Overview

Google Cloud Platform (GCP) is Google's suite of cloud computing services that provides infrastructure, platforms, and software for building, deploying, and operating applications and services. Launched in 2008 with Google App Engine, GCP has grown into a comprehensive platform competing with Amazon Web Services (AWS) and Microsoft Azure. It leverages Google's global infrastructure—the same physical infrastructure that powers Google Search, YouTube, Gmail, and other Google services.

GCP offers compute, storage, networking, data analytics, machine learning, and developer tools. Organizations use GCP for running web applications, analyzing big data, training machine learning models, and modernizing legacy systems. Key differentiators include Google's expertise in data processing (MapReduce, BigQuery), strong ML/AI tooling (TensorFlow, Vertex AI), and high-performance networking.

## Key Concepts

**Projects**: All GCP resources belong to a project. Projects are the organizing entity for billing, access control, and resource management. You can have multiple projects for different environments (dev, staging, prod) or different teams.

**Regions and Zones**: Resources are deployed in specific geographic regions (e.g., us-central1, europe-west1). Each region contains multiple zones (isolated data centers). Zonal resources are in one zone; regional resources span multiple zones for high availability.

**IAM (Identity and Access Management)**: GCP's unified access control system. Define who (principals) can do what (roles) on which resources. Roles are sets of permissions. Bindings associate principals with roles on resources.

```yaml
# Example IAM policy binding
bindings:
- members:
  - user: alice@example.com
  - serviceAccount: my-app@my-project.iam.gserviceaccount.com
  role: roles/storage.objectAdmin
```

**VPC (Virtual Private Cloud)**: Isolated network for your GCP resources. VPCs span regions and allow you to define IP ranges, subnets, routing, and firewall rules. VPCs can be shared across projects in an organization.

**APIs and Services**: GCP services are exposed via REST APIs. You enable APIs per project. Cloud Console, gcloud CLI, or client libraries interact with these APIs.

## Core Services

**Compute Engine**: Virtual machines (VMs) running in Google's data centers. Full control over OS and configuration. Useful for migrating existing applications or running custom workloads.

**Google Kubernetes Engine (GKE)**: Managed Kubernetes for containerized applications. Handles master node management, automatic upgrades, and scaling. Supports both workload Identity (for pod authentication) and Anthos for hybrid/multi-cloud.

**Cloud Run**: Fully managed container platform optimized for stateless HTTP services. Scales to zero and charges only for actual usage. Ideal for microservices and event-driven workloads.

**App Engine**: Platform-as-a-Service (PaaS) for web applications and APIs. Supports Python, Node.js, Go, Java, PHP, Ruby. App Engine handles scaling, load balancing, and infrastructure maintenance automatically.

**Cloud Functions**: Event-driven serverless functions. Triggers include HTTP requests, Cloud Storage changes, Pub/Sub messages. Pay only for execution time.

```bash
# Deploy a Cloud Run service
gcloud run deploy my-service \
  --image gcr.io/my-project/my-image:latest \
  --region us-central1 \
  --allow-unauthenticated

# Deploy a Cloud Function (2nd gen)
gcloud functions deploy my-function \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated
```

**Cloud Storage**: Object storage for files, backups, archives. Various storage classes (Standard, Nearline, Coldline, Archive) with different pricing for access frequency. Universally unique bucket names.

**BigQuery**: Serverless, highly scalable data warehouse. Uses SQL interface. Separate storage and compute pricing. Handles petabyte-scale analytics. Native support for ML with BigQuery ML.

**Pub/Sub**: Global messaging and ingestion for streaming analytics. Publishers send messages to topics; subscribers receive messages. At-least-once delivery with optional exactly-once delivery.

**Cloud SQL**: Managed relational databases (MySQL, PostgreSQL, SQL Server). Handles patching, backups, replication, and failover. Private IP connectivity within VPC.

**Spanner**: Globally distributed relational database with horizontal scaling. Strong consistency with external consistency guarantees. Supports SQL, automatic sharding, and multi-region deployment.

## Practical Applications

**Web Application Hosting**: Deploy containerized microservices on Cloud Run or GKE, use Cloud SQL for data, Cloud CDN for static assets, and load balancing for global traffic.

**Data Analytics Pipelines**: Ingest logs and events via Pub/Sub, process with Dataflow (Apache Beam), store in BigQuery, visualize in Looker or Looker Studio.

**ML/AI Workloads**: Train models on Vertex AI (managed training with auto-scaling), use pre-trained APIs for vision, language, speech. Deploy models for prediction on Vertex Endpoints.

**Migration of On-Premises Workloads**: Use Migrate for Compute Engine (formerly Velostrata) for lift-and-shift, or refactor to containers on GKE for cloud-native benefits.

## Examples

**Deploying a Web App on Cloud Run**:
```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", ":8080", "app:app"]
```

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/my-app
gcloud run deploy my-app --image gcr.io/$PROJECT_ID/my-app --platform managed
```

**Setting up a VPC with private Google Access**:
```bash
gcloud compute networks create my-vpc --subnet-mode=custom

gcloud compute subnets create my-subnet \
  --network my-vpc \
  --region us-central1 \
  --range 10.0.0.0/24 \
  --enable-private-ip-google-access
```

## Related Concepts

- [[Cloud Computing]] — General cloud infrastructure concepts
- [[AWS]] — Amazon Web Services, competing platform
- [[Kubernetes]] — Container orchestration, core of GKE
- [[Serverless]] — FaaS and PaaS models
- [[Microservices]] — Architecture style common in cloud deployments
- [[DevOps]] — Practices for cloud-native development

## Further Reading

- GCP Documentation: https://cloud.google.com/docs
- Google Cloud Skills Boost (formerly Qwiklabs) — Hands-on learning
- "Architecting with GCP" course series on Coursera

## Personal Notes

GCP's strength is its data and ML ecosystem. BigQuery's separation of storage and compute is genuinely game-changing for analytics—you can query petabytes without managing clusters. But I've found the console sometimes confusing due to constant UI changes. The gcloud CLI is more stable and I recommend mastering it. Also watch out for egress costs—they can surprise you when data leaves GCP.
