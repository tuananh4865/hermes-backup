---
title: "Aws"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, infrastructure, devops, amazon]
---

# Aws

## Overview

Amazon Web Services (AWS) is a comprehensive cloud computing platform offered by Amazon, providing over 200 services spanning compute, storage, networking, database, analytics, machine learning, and物联网. Launched in 2006 with S3 storage and EC2 compute, AWS pioneered the modern cloud computing industry and maintains the largest market share in the space.

AWS enables organizations to provision computing resources on-demand without investing in physical infrastructure. This on-demand model provides elasticity—scaling resources up during peak demand and down during low usage—while paying only for what is consumed. From startups building their first web applications to enterprises migrating critical systems, AWS provides the building blocks for virtually any computing workload.

## Key Concepts

**Regions and Availability Zones**: AWS infrastructure is distributed globally across geographic regions (e.g., us-east-1, eu-west-1), each containing multiple isolated Availability Zones. This design supports both low-latency access and high availability through geographic redundancy.

**IAM (Identity and Access Management)**: The service for managing permissions and authentication. IAM defines who can access what resources through policies attached to users, roles, and groups. Least-privilege access is a fundamental security principle in AWS.

**Virtual Private Cloud (VPC)**: A logically isolated network within AWS where you deploy resources. VPCs enable control over IP ranges, subnets, routing tables, and network gateways, essential for secure architectures.

**Serverless**: Services like Lambda, DynamoDB, and API Gateway that abstract server management entirely. You write functions, AWS handles provisioning, scaling, and high availability.

**Shared Responsibility Model**: AWS manages security "of" the cloud (infrastructure, hardware, virtualization), while customers manage security "in" the cloud (data, access, applications).

## How It Works

AWS operates through a combination of web consoles, command-line interfaces, and APIs:

1. **Account Creation**: Sign up at aws.amazon.com, provide payment method and identity verification
2. **Service Selection**: Choose services from the extensive catalog based on workload requirements
3. **Resource Provisioning**: Use Console, CLI, or SDKs to create and configure resources
4. **Network Configuration**: Define VPC, subnets, security groups, and routing
5. **Deployment**: Deploy applications using infrastructure-as-code (CloudFormation, Terraform) or manual provisioning
6. **Monitoring**: Use CloudWatch for metrics, logs, and alerting

```bash
# Example AWS CLI commands for common operations
# Configure AWS credentials
aws configure

# Launch an EC2 instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.micro \
    --key-name my-key-pair \
    --security-group-ids sg-0123456789abcdef0

# List S3 buckets
aws s3 ls

# Create DynamoDB table
aws dynamodb create-table \
    --table-name MyTable \
    --attribute-definitions AttributeName=ID,AttributeType=S \
    --key-schema AttributeName=ID,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST
```

## Practical Applications

AWS services power applications across every industry:

- **Web Applications**: EC2, Lambda, RDS, CloudFront, Route 53 for hosting scalable web apps
- **Data Analytics**: S3, Athena, Redshift, EMR for data warehousing and processing
- **Machine Learning**: SageMaker for building, training, and deploying ML models
- **Media Processing**: Elemental MediaConvert, S3, CloudFront for video transcoding and delivery
- **IoT**: IoT Core for connecting and managing billions of devices
- **Gaming**: GameLift for deploying and scaling game servers

## Examples

**Serverless Web Application Architecture**:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Users     │────▶│ CloudFront  │────▶│   S3        │
└─────────────┘     └──────┬──────┘     │ (Static)    │
                          │            └─────────────┘
                          ▼
                   ┌─────────────┐     ┌─────────────┐
                   │ API Gateway │────▶│   Lambda    │
                   └─────────────┘     └──────┬──────┘
                                               │
                          ┌────────────────────┼────────────────────┐
                          ▼                    ▼                    ▼
                   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                   │  DynamoDB   │     │     S3     │     │    SES      │
                   │ (Database)  │     │ (Storage)  │     │  (Email)    │
                   └─────────────┘     └─────────────┘     └─────────────┘
```

**Infrastructure as Code with AWS CloudFormation**:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Simple web server on EC2

Resources:
  MyInstance:
    Type: 'AWS::EC2::Instance'
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t3.micro
      KeyName: my-key-pair
      SecurityGroups:
        - !Ref MySecurityGroup
  
  MySecurityGroup:
    Type: 'AWS::EC2::SecurityGroup'
    Properties:
      GroupDescription: Allow HTTP traffic
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: 0.0.0.0/0
```

## Related Concepts

- [[Cloud Computing]] - The broader paradigm AWS implements
- [[Serverless]] - AWS Lambda and related serverless services
- [[DevOps]] - Practices AWS infrastructure enables
- [[Terraform]] - Infrastructure as code tool supporting AWS
- [[Kubernetes]] - Container orchestration AWS supports through EKS
- [[Microservices]] - Architecture pattern common in AWS deployments

## Further Reading

- [AWS Documentation](https://docs.aws.amazon.com/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/)
- [AWS Free Tier](https://aws.amazon.com/free/)

## Personal Notes

AWS's breadth is both its strength and complexity. With 200+ services, there's often multiple ways to accomplish the same goal—choosing between Lambda, ECS, EKS, or EC2 requires understanding trade-offs. The free tier is generous but billing can surprise newcomers. I recommend starting with the simplest service that meets your needs and scaling up only when necessary. AWS's maturity means excellent documentation and community support, but also significant architectural complexity for enterprise workloads.
