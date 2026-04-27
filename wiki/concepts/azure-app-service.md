---
title: Azure App Service
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [azure, web-hosting, paas, cloud-computing, devops]
---

## Overview

Azure App Service is a fully managed Platform-as-a-Service (PaaS) offering from Microsoft Azure that enables developers to build, deploy, and scale web applications, REST APIs, and mobile backends. It supports multiple programming languages including .NET, .NET Core, Java, Node.js, Python, and PHP, providing a frictionless path from code to cloud. App Service handles infrastructure provisioning, load balancing, auto-scaling, and security patches automatically, allowing developers to focus purely on application code.

## Key Concepts

**App Service Plans**: The underlying compute resources that determine capacity, features, and cost. Plans range from free/shared tiers for development to premium tiers with dedicated VMs, custom domain support, and TLS certificates. Sizing directly impacts performance, scale-out behavior, and available features like backup slots.

**Deployment Slots**: App Service allows creating multiple deployment slots (e.g., staging, production) that swap in seconds. This enables zero-downtime deployments, testing in production-like environments, and instant rollbacks. Traffic can be gradually shifted between slots using the traffic routing feature.

**Authentication and Authorization**: Built-in authentication middleware supports Microsoft Entra ID, Google, Facebook, Twitter, and custom identity providers. This eliminates boilerplate auth code while providing OAuth 2.0/OIDC integration, token storage, and session management.

**Continuous Deployment**: App Service integrates with Azure DevOps, GitHub Actions, Bitbucket, and external Git repositories for automated build and deployment pipelines. Deployment center streamlines configuration with preset workflows for common frameworks.

## How It Works

Azure App Service runs web workloads in managed Azure VMs running IIS (Windows) or Apache/Nginx (Linux). The service abstracts away VM management through a PaaS model. When you deploy an app, App Service handles:

1. **Environment provisioning** - Allocates compute based on your plan tier
2. **Runtime installation** - Sets up the appropriate language runtime
3. **Load balancer configuration** - Routes traffic with health probes
4. **Auto-scaling rules** - Adjusts capacity based on metrics
5. **SSL/TLS termination** - Handles certificates for HTTPS
6. **Logging and monitoring** - Integrates with Azure Monitor and App Insights

```bash
# Deploy via Azure CLI
az webapp up --name myapp --runtime PYTHON:3.11 --plan myAppServicePlan --resource-group myRG

# Configure auto-scaling
az monitor app-insights autoscale create \
  --resource-group myRG \
  --resource myAppServicePlan \
  --name scale-rule
```

## Practical Applications

Azure App Service excels for enterprise web applications requiring AD integration, government compliance (FedRAMP, DoD IL4/IL5), and seamless Azure service integration. Line-of-business applications, customer portals, and e-commerce sites benefit from the managed infrastructure and built-in disaster recovery. API backends for mobile and single-page applications can leverage App Service's easy scaling and authentication features.

## Examples

- **ASP.NET Core Web API**: Deploy a REST API with Entity Framework and SQL Database
- **Node.js Express App**: Host a server-side rendered app with PM2 process management
- **Python Flask**: Run a machine learning model's prediction API with Docker deployment
- **Static Frontend + Functions**: SPA served by App Service with Azure Functions backend

## Related Concepts

- [[Platform as a Service]] - The cloud service model App Service represents
- [[Web Hosting]] - Traditional hosting concepts App Service automates
- [[Cloud Computing]] - Broader context of managed infrastructure
- [[DevOps]] - CI/CD integration and deployment best practices
- [[Azure Functions]] - Serverless complement to App Service's IaaS-lite model

## Further Reading

- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [App Service Environment](https://docs.microsoft.com/en-us/azure/app-service/environment/overview) - Isolated deployment for enterprise
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/) - Best practices and reference architectures

## Personal Notes

App Service is my go-to for .NET projects—it handles deployment slots beautifully for staging->production promotion. The authentication middleware saves days of boilerplate. One gotcha: always set WEBSITE_TIME_ZONE if your app has time-based logic, as VMs may not be in your expected timezone.
