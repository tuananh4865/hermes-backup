---
title: "Amazon EC2"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, aws, infrastructure, virtualization]
---

# Amazon EC2

## Overview

Amazon Elastic Compute Cloud (EC2) is a foundational web service within Amazon Web Services (AWS) that provides resizable compute capacity in the cloud. It allows users to launch virtual servers—called instances—on demand, paying only for the capacity they actually use. EC2 eliminates the need for upfront capital expenditure on hardware and gives developers and enterprises the ability to scale computing resources up or down in response to workload demands, a property often described as elasticity.

EC2 forms the backbone of most AWS architectures. Whether running a simple web server, hosting a high-performance computing cluster, or deploying a distributed data processing pipeline, EC2 provides the underlying compute infrastructure. The service offers a wide variety of instance types optimized for different use cases: general-purpose instances balance compute, memory, and networking; compute-optimized instances prioritize raw CPU power; memory-optimized instances serve applications that require large RAM footprints; and GPU instances accelerate machine learning training and graphics rendering workloads.

The service abstracts away the physical hardware layer entirely. Users select an Amazon Machine Image (AMI) containing the operating system and software stack, choose an instance type and size, configure networking and security settings, and launch. The underlying physical servers, storage, and networking are all managed by AWS, allowing users to focus purely on the software running on their instances.

## Key Concepts

**Instance Types** define the hardware characteristics of a virtual machine. AWS offers over 750 instance types across families including:

- **General Purpose (T, M)** — balanced resources for everyday workloads, web servers, small databases
- **Compute Optimized (C)** — high-performance processors for batch processing, scientific modeling, gaming servers
- **Memory Optimized (R, X)** — large RAM for in-memory databases, real-time analytics, SAP HANA
- **Storage Optimized (D, I, H)** — high-speed local storage for data warehousing, log processing, distributed file systems
- **GPU Instances (P, G, Inf)** — NVIDIA GPUs for machine learning inference/training, video transcoding, scientific computing
- **High Memory (U)** — massive RAM for in-memory databases and SAP deployments

**Amazon Machine Images (AMIs)** are pre-configured templates that contain the operating system, application server, and applications. AWS provides managed AMIs, the community shares others, and users can create custom AMIs from running instances to capture their own configurations.

**Instance Lifecycle** — An EC2 instance moves through states: `pending` (launching), `running` (active and billable), `stopping`, `stopped`, `shutting-down`, and `terminated`. Stopped instances retain their EBS volumes but do not incur compute charges, only storage charges.

**Placement Groups** control how instances are distributed across underlying hardware. Cluster placement packs instances close together on the same rack for low-latency communication; Spread placement places instances on distinct hardware for high availability; Partition placement distributes instances across logical partitions (different racks, power circuits) for large distributed workloads like Hadoop.

## How It Works

When you launch an EC2 instance, AWS allocates a virtual machine running on a hypervisor (Nitro, a custom AWS hypervisor) on a physical host in one of its Availability Zones. The Nitro hypervisor provides near-native performance with hardware virtualization, ENI (Elastic Network Interface) attachments for networking, and local NVMe storage for instance store volumes.

Networking is handled through the Virtual Private Cloud (VPC) framework. Each instance receives one or more elastic network interfaces (ENIs), each with a primary private IPv4 address, optional secondary addresses, and optionally one or more Elastic IPs (public IPv4 addresses). Security Groups act as virtual stateful firewalls at the instance level, controlling inbound and outbound traffic based on protocol, port, and source/destination.

```bash
# Launch an EC2 instance using AWS CLI
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --instance-type t3.medium \
  --key-name my-key-pair \
  --security-group-ids sg-0123456789abcdef0 \
  --subnet-id subnet-0123456789abcdef0 \
  --count 1

# Check instance status
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query "Reservations[*].Instances[*].{ID:InstanceId,Type:InstanceType,State:State.Name}" \
  --output table

# Stop an instance (preserves data on EBS volumes)
aws ec2 stop-instances --instance-ids i-0123456789abcdef0

# Terminate an instance (deletes attached instance-store volumes; EBS volumes depend on delete-on-terminate flag)
aws ec2 terminate-instances --instance-ids i-0123456789abcdef0
```

EC2 integrates with services like Elastic Load Balancing (ELB) for distributing traffic across instances, Auto Scaling Groups (ASG) for automating capacity management, and CloudWatch for monitoring metrics like CPU utilization, network traffic, and disk I/O.

## Practical Applications

**Web Hosting** — EC2 powers millions of websites and web applications. Combined with Elastic Load Balancing and Auto Scaling, instances can automatically scale horizontally to handle traffic spikes without manual intervention. An ASG can be configured to add instances when CPU average exceeds 70% and terminate instances when it drops below 30%.

**Big Data Processing** — Frameworks like Apache Spark, Hadoop, and Kafka run on EC2 clusters to process massive datasets. Spot Instances (which offer up to 90% discount in exchange for interruptibility) are particularly popular for batch processing jobs that can tolerate interruption.

**Machine Learning** — ML practitioners use GPU instances (P4d, P5) for training large models, and CPU instances for inference serving. SageMaker, AWS's managed ML service, itself runs on EC2 infrastructure under the hood.

**High-Performance Computing (HPC)** — EC2's HPC instances (Hpc6a, Hpc7g) provide high-performance networking (EFA — Elastic Fabric Adapter) for tightly coupled workloads like computational fluid dynamics, drug discovery, and financial simulations.

**Desktop Virtualization** — Amazon WorkSpaces and Amazon AppStream run on EC2, providing cloud desktops to end users without managing physical hardware.

## Examples

A typical three-tier web application on EC2 might look like this: a fleet of web servers (Application Load Balancer + Auto Scaling Group of T3 medium instances in a public subnet) sitting behind a load balancer, which forwards requests to a pool of application servers in a private subnet (ASG of C6i instances), which in turn connect to an RDS Aurora database in an isolated database subnet group. A CloudWatch alarm triggers scale-out when CPU exceeds 75% for 3 consecutive minutes, and CloudFront CDN caches static assets at the edge.

A data engineering team might use a batch-processing pipeline: Spot Instances in a cluster placement group for a 100-node Spark cluster processing 10TB of daily log data. Because the job is fault-tolerant (Spark retries failed tasks), interrupted Spot instances are replaced automatically, and the entire job costs a fraction of what On-Demand pricing would charge.

## Related Concepts

- [[Amazon Web Services]] - The broader cloud platform of which EC2 is a part
- [[Virtualization]] - The underlying technology that makes EC2 possible
- [[Auto Scaling]] - Automatically adjusting EC2 capacity based on demand
- [[Elastic Load Balancing]] - Distributing traffic across EC2 instances
- [[Amazon EBS]] - Elastic Block Store, persistent block storage for EC2 instances
- [[Amazon VPC]] - Virtual Private Cloud, the networking framework for EC2
- [[Cloud Computing]] - The delivery model that EC2 exemplifies
- [[Spot Instances]] - Cost-optimization feature using spare EC2 capacity

## Further Reading

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/) — Official documentation with tutorials and best practices
- [EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/) — Complete listing of all instance families and their specifications
- [Amazon EC2 On-Demand Pricing](https://aws.amazon.com/ec2/pricing/on-demand/) — Current pricing for all instance types and regions

## Personal Notes

EC2 is the Swiss Army knife of cloud computing—versatile enough to power anything from a personal blog to the world's largest websites. The key to using it effectively is choosing the right instance type for your workload and using Auto Scaling to match capacity to demand. Don't forget to implement proper cost controls: set billing alarms, use Spot Instances for fault-tolerant workloads, and regularly clean up unused resources. Security Groups should follow the principle of least privilege—open only the ports and protocols you actually need.
