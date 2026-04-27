---
title: "Heroku"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [paas, cloud, devops, deployment, ruby, nodejs]
---

# Heroku

## Overview

Heroku is a cloud platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud. Founded in 2007 and later acquired by Salesforce in 2010, Heroku pioneered the concept of letting developers deploy code to the cloud with minimal infrastructure configuration. It supports multiple programming languages including Ruby, Node.js, Python, Java, PHP, Go, and Scala. Heroku's flagship feature is its elegant deployment mechanism — developers push code via Git, and Heroku automatically detects the language, provisions the appropriate runtime, and spins up dynos (lightweight Linux containers) to run the application. This abstraction of infrastructure allows teams to focus entirely on writing application code rather than managing servers.

## Key Concepts

**Dynos** are the core building blocks of Heroku's architecture. Each dyno is an isolated, virtualized container running a single user-specified command, such as a web server for a web application. Dynos can be scaled horizontally by adding more dynos to handle increased load, or vertically by choosing larger dyno sizes with more memory and CPU. Heroku's routing layer automatically distributes incoming HTTP requests across all web dynos using a random distribution algorithm.

**Buildpacks** are the scripts that Heroku uses to compile your application. When you push code, Heroku detects the language and applies the appropriate buildpack, which installs dependencies, configures the runtime environment, and prepares the application to run. You can also use custom buildpacks for unsupported languages or specialized setups.

**Add-ons** extend Heroku's functionality through a rich marketplace of pre-integrated services. These include databases (PostgreSQL, MySQL, Redis), monitoring tools, email services, and much more. Add-ons are provisioned with a single command and tightly integrated with the Heroku platform.

**Config Vars** store environment-specific configuration as key-value pairs, keeping sensitive credentials and deployment-specific settings separate from application code.

## How It Works

When you deploy to Heroku, the following flow occurs:

1. You push code from your local Git repository to Heroku's Git remote
2. Heroku triggers a build process using the detected or specified buildpack
3. The buildpack fetches dependencies, compiles assets, and creates a slug — a compressed bundle of your application code and dependencies
4. The slug is distributed across Heroku's runtime infrastructure
5. The routing mesh receives incoming requests and forwards them to available dynos
6. Dynos run your application process (e.g., `web: node index.js`)
7. Logs from all dynos are aggregated into a unified log stream accessible via `heroku logs`

## Practical Applications

Heroku is widely used for:

- **Rapid prototyping and startups** — teams can deploy working software in minutes without DevOps expertise
- **Web applications** — hosting full-stack apps with managed databases and automatic SSL
- **API backends** — serving mobile and frontend applications with scalable dyno-based compute
- **Background workers** — running asynchronous tasks via worker dynos
- **Continuous deployment pipelines** — integrating with GitHub for automatic deployments on code push

## Examples

Deploying a Node.js app to Heroku:

```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create a new Heroku app
heroku create my-app

# Set a start script in package.json
# "scripts": { "start": "node index.js" }

# Deploy via Git
git push heroku main

# Scale web dynos
heroku ps:scale web=2

# Open in browser
heroku open
```

A basic `Procfile` for a web server and background worker:

```procfile
web: node web.js
worker: node worker.js
```

## Related Concepts

- [[PaaS]] — Platform as a Service, the category Heroku belongs to
- [[Dynos]] — Heroku's container-based compute model
- [[Buildpacks]] — Build automation scripts for Heroku deployments
- [[12-Factor App]] — Methodology Heroku pioneered for building SaaS applications
- [[Docker]] — Container technology related to Heroku's dyno isolation

## Further Reading

- [Heroku Dev Center](https://devcenter.heroku.com/) — Official documentation and guides
- [The Heroku Platform](https://www.heroku.com/platform) — Product overview and pricing

## Personal Notes

Heroku was my first real cloud deployment platform. The magic of `git push heroku main` still impresses me — it takes infrastructure complexity and hides it behind simplicity. Though competitors like Vercel and Railway have emerged with more modern DX, Heroku remains a solid choice, especially for teams already invested in the Salesforce ecosystem. One gotcha: the free tier dynos sleep after 30 minutes of inactivity, which can be surprising for web apps expecting traffic.
