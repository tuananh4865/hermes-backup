---
title: "PaaS"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cloud-computing, platform, deployment, heroku, cloud-foundry]
---

# PaaS (Platform as a Service)

## Overview

Platform as a Service (PaaS) is a cloud computing service model that provides a managed platform for developing, running, and maintaining applications. In the PaaS model, the cloud provider handles the underlying infrastructure—servers, storage, networking, operating systems, and runtime environments—while the customer focuses on writing application code and configuring deployment settings. This frees developers from the operational overhead of managing servers while still offering more control than fully abstracted [[Serverless]] models.

PaaS sits between [[Infrastructure as a Service]] (IaaS), where you manage virtual machines and networking, and [[Software as a Service]] (SaaS), where you consume a complete application. It is sometimes described as "serverless containers" because the platform manages container scheduling, scaling, and health monitoring on behalf of the developer.

## Key Concepts

**The Buildpack Model** is central to classic PaaS offerings like Heroku and Cloud Foundry. A buildpack is a script or set of scripts that detects the language/framework of an application, downloads dependencies (e.g., `npm install`, `pip install`), compiles assets if needed, and configures the runtime. Popular buildpacks exist for Node.js, Ruby, Python, Java, Go, PHP, and .NET. If no custom buildpack is specified, the platform auto-detects the appropriate one.

**Dynos** (Heroku's term) or **Diego Cells** (Cloud Foundry) are the runtime containers where application code executes. Each dyno is an isolated, virtualized container with its own filesystem, memory, and process space. The platform manages scheduling these dynos across physical hosts, handling failover and load distribution automatically.

**Routing Mesh** distributes incoming HTTP traffic across running dynos. The router is aware of the health of each dyno via heartbeats and only forwards requests to healthy instances. This enables zero-downtime deployments and automatic re-routing around failed instances.

**Add-ons** are third-party managed services (databases, caching, logging, monitoring) that extend the platform. The platform provides a marketplace and one-click provisioning with environment variables injected into the application, simplifying the integration of external services.

**Environment Variables** are the primary mechanism for configuring applications in PaaS. Secrets, connection strings, feature flags, and environment-specific settings are all passed via environment variables, keeping configuration separate from code.

## How It Works

When a developer pushes code (via `git push` in Heroku's case), the platform triggers a build pipeline: the buildpack runs, dependencies are resolved, a slug is produced (a compressed tarball of the application and its dependencies), and the slug is distributed to dynos. The router begins routing traffic to the new dynos alongside the old ones, and after a health check period, traffic shifts to the new version and old dynos are terminated. This is a form of blue-green deployment.

Scaling in PaaS is typically horizontal (adding more dynos) rather than vertical (adding more resources to existing dynos). The developer specifies the number of dynos per process type (e.g., 2 web dynos, 4 worker dynos), and the platform ensures that count is maintained. If a dyno crashes, the platform automatically replaces it.

PaaS pricing is usually based on dyno-hours (compute time consumed). Free tiers typically offer a single small dyno that sleeps after inactivity, while production workloads scale across multiple dynos with optional auto-scaling based on metrics like request latency or queue depth.

## Practical Applications

- **Web Application Hosting**: Deploy and scale web apps without managing servers. Node.js, Django, Rails, and Spring Boot applications are common targets.
- **API Backends**: Host RESTful or GraphQL APIs with automatic scaling and health monitoring.
- **CI/CD Targets**: Use PaaS as a deployment target from CI pipelines, enabling rapid iteration.
- **Proof of Concept / MVP**: Get an application live quickly without infrastructure setup, making PaaS ideal for validating ideas before committing to infrastructure investment.
- **Microservices**: Deploy individual services as separate PaaS apps, each independently scalable and maintainable.

## Examples

A minimal `Procfile` for a Node.js app on Heroku:

```
web: node server.js
worker: node worker.js
```

A `runtime.txt` specifying the Python version:

```
python-3.12.3
```

Deploying with git:

```bash
heroku create my-app-name
git push heroku main
heroku ps:scale web=2 worker=1
heroku open
```

Setting environment variables:

```bash
heroku config:set NODE_ENV=production DATABASE_URL=postgres://...
heroku config:get NODE_ENV  # Verify
```

## Related Concepts

- [[Heroku]] - The most well-known PaaS provider
- [[Cloud Foundry]] - Open-source PaaS and enterprise PaaS option
- [[Containerization]] - The technology underlying PaaS dynos
- [[12-Factor App]] - Methodology for building SaaS apps that aligns with PaaS principles
- [[Kubernetes]] - More powerful but more complex container orchestration, often compared to PaaS
- [[Self-Healing Wiki]] - The system that auto-created this page

## Further Reading

- [Heroku Dev Center](https://devcenter.heroku.com/) - Comprehensive documentation
- [Cloud Foundry Documentation](https://docs.cloudfoundry.org/) - Open-source PaaS reference
- [12-Factor App](https://12factor.net/) - Best practices for cloud-native applications

## Personal Notes

PaaS is the right choice when you want developer velocity without infrastructure complexity. Heroku's DX (developer experience) is excellent—`git push` deployment with automatic slug compilation and routing is hard to beat for simplicity. The main trade-off is cost at scale: a PaaS dyno is more expensive than an equivalent raw virtual machine, and when you need fine-grained control over the runtime environment, containers or VM-based deployment become more cost-effective.
