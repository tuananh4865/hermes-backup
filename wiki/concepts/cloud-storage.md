---
title: Cloud Storage
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-storage, storage, object-storage, s3, data-persistence]
---

# Cloud Storage

## Overview

Cloud storage is a model of computer data storage in which digital data is stored on remote servers accessed via the internet, managed by a third-party cloud provider. Rather than storing files on a local hard drive or on-premises server, organizations and individuals rent storage capacity from providers like [[AWS]], [[Google Cloud]], or [[Microsoft Azure]]. The provider maintains the physical infrastructure, handles replication across data centers, manages durability guarantees, and provides APIs for programmatic access.

Cloud storage has become the dominant paradigm for data persistence in modern applications, replacing traditional on-premises storage area networks (SANs) and network-attached storage (NAS) for most use cases. It underpins everything from static website hosting and [[CDN]] origin storage to big data analytics, [[machine learning]] training datasets, and [[backup-and-recovery]] systems.

## Key Concepts

### Object Storage

The dominant model for cloud storage is [[object storage]], where data is stored as objects within containers called "buckets" (in [[AWS S3]]) or equivalent namespaces. Each object consists of:
- **Data**: The raw file content
- **Metadata**: Descriptive information (content type, creation date, custom tags)
- **Identifier**: A unique key within the bucket

Object storage differs fundamentally from traditional [[file-system]] or block storage. There is no directory hierarchy at the storage layer (though logical "folders" can be simulated via key prefixes), and objects are immutable—modifying an object typically means replacing it entirely.

### Durability and Availability

Major cloud storage providers offer strong durability guarantees:
- [[AWS S3]] Standard: 99.999999999% (11 nines) durability per object per year
- [[Google Cloud Storage]]: 99.999999999% durability for Multi-Regional
- [[Azure Blob Storage]]: 99.999999999% durability for LRS

These guarantees are achieved through automatic replication across multiple physical facilities (availability zones or regions). "Durability" means the object will not be lost; "availability" (usually 99.9-99.99%) means the object will be accessible when you want it.

### Storage Tiers

Cloud providers offer multiple storage classes optimized for different access patterns:

| Tier | Use Case | Access Latency | Cost |
|------|----------|----------------|------|
| Hot/Standard | Frequent access | Milliseconds | Higher $/GB |
| Cool/Warm | Infrequent access | Seconds | Lower $/GB |
| Cold/Glacier | Archival, rare access | Minutes to hours | Lowest $/GB |
| Archive Deep | Long-term compliance | 12+ hours | Pennies per GB |

Transitioning between tiers can be automatic via lifecycle policies, which is critical for cost optimization.

### Access Control and Security

Cloud storage integrates with identity and access management ([[IAM]]):
- **Bucket policies**: JSON-based rules defining who can access what
- **Access Control Lists (ACLs)**: Legacy per-object permissions
- **Pre-signed URLs**: Time-limited access without IAM credentials
- **Server-side encryption (SSE)**: Data encrypted at rest using provider-managed, customer-managed, or customer-provided keys

## How It Works

When you upload a file to cloud storage:

1. **API Call**: Your application sends a `PUT` request to the storage API with the object data and metadata
2. **Authentication**: The provider verifies your credentials via [[IAM]]
3. **Receipt Confirmation**: The provider returns a unique object key/identifier
4. **Replication**: The provider asynchronously replicates data across multiple physical disks and facilities
5. **Retrieval**: Later, your application sends a `GET` request with the object key, and the provider streams the data back

The underlying storage system uses distributed databases and custom file systems designed for massive scale. [[AWS S3]] alone stores trillions of objects across multiple data centers globally.

For the application, cloud storage appears as an HTTP API. Libraries in every language (boto3 for Python, AWS SDK for Node.js, etc.) wrap these HTTP calls into idiomatic APIs.

## Practical Applications

Cloud storage is fundamental across virtually all software domains:

- **Static Website Hosting**: HTML, CSS, JS, and media files served via [[CDN]] (CloudFront, Cloudflare) with origin in S3/GCS
- **Data Lakes**: Massive unstructured and structured datasets for analytics, accessed by [[Apache Spark]], [[Athena]], [[BigQuery]]
- **Machine Learning**: Training data, model weights, and datasets stored and versioned (see [[MLflow]], [[DVC]])
- **Backup and Recovery**: Automated backup to cloud with lifecycle policies for compliance retention
- **Media Storage**: Video, image, and audio files for streaming platforms, often paired with [[transcoding]]
- **Database Storage**: Cloud databases (RDS, Cloud SQL, Cosmos DB) store data on cloud block storage underneath

## Examples

Uploading and downloading a file with boto3 (Python AWS SDK):

```python
import boto3

s3 = boto3.client('s3')

# Upload a file
s3.upload_file(
    'local_data.csv',
    'my-bucket-name',
    'uploads/2026/data.csv',
    ExtraArgs={'ContentType': 'text/csv', 'Metadata': {'source': 'etl-pipeline'}}
)

# Generate a pre-signed URL (valid for 1 hour)
url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'my-bucket-name', 'Key': 'uploads/2026/data.csv'},
    ExpiresIn=3600
)

# Download using the pre-signed URL
import urllib.request
response = urllib.request.urlopen(url)
print(response.read())
```

Setting up a lifecycle policy with Terraform (HCL):

```hcl
resource "aws_s3_bucket" "data_lake" {
  bucket = "my-data-lake"
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    filter {
      prefix = "logs/"
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    noncurrent_version_transition {
      noncurrent_days = 30
      storage_class  = "GLACIER"
    }
  }
}
```

## Related Concepts

- [[AWS]] — Major cloud provider with S3
- [[Google Cloud Platform]] — Provider with Google Cloud Storage
- [[Microsoft Azure]] — Provider with Blob Storage
- [[backup-and-recovery]] — Using cloud storage for backups
- [[CDN]] — Content delivery networks that pull from cloud storage origins
- [[local-storage]] — Contrast with on-device storage
- [[data-persistence]] — General concept of keeping data over time
- [[database]] — Often uses cloud block storage underneath
- [[storage]] — General storage concepts

## Further Reading

- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/) — The most widely used cloud storage service
- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Azure Blob Storage Documentation](https://learn.microsoft.com/en-us/azure/storage/blobs/)
- [Cloud Storage Comparison: S3 vs GCS vs Azure](https://provider comparison guides)

## Personal Notes

The biggest mistake I see with cloud storage is ignoring storage tiering. Teams store everything in "Standard" tier forever, racking up unnecessary costs. Setting up lifecycle policies that auto-transition to Glacier after 90 days has saved several clients 60-80% on storage costs with zero operational impact. Also, always enable versioning—it costs a bit more but saves you from accidental deletions. The pre-signed URL pattern is underutilized; it's a clean way to give time-limited access to private objects without exposing IAM credentials to clients.
