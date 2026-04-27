---
title: Hosting
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [hosting, deployment, infrastructure, web-hosting, serverless]
---

# Hosting

## Overview

Hosting refers to the provision of computing infrastructure and services that make a website, web application, or API accessible on the internet. This encompasses everything from a single virtual machine running a web server to globally distributed, auto-scaling serverless functions at the edge of the network. Hosting is the foundational layer of any web presence—without it, code exists only on a developer's machine with no way for the public to access it.

Modern hosting has evolved far beyond the shared web hosting of the early 2000s. Today's landscape includes managed [[platform-as-a-service]] (PaaS) offerings, container-based platforms like [[Kubernetes]], [[serverless computing]], [[edge computing]] solutions, and traditional virtual private servers (VPS). Choosing the right hosting model depends on factors like traffic scale, operational complexity tolerance, cost structure, and performance requirements.

## Key Concepts

### Types of Hosting

**Shared Hosting**: Multiple websites share a single physical server. Cheapest option but lowest performance and no root access. Providers like GoDaddy, HostGator. Suitable for low-traffic personal sites.

**Virtual Private Server (VPS)**: A slice of a physical server with guaranteed resources and root access. [[Virtual machine]] technology (KVM, Xen, VMware) provides isolation. Providers: [[DigitalOcean]], Linode, Vultr. Balances cost and control.

**Dedicated Server**: An entire physical machine dedicated to one customer. Maximum performance, control, and cost. Used for high-traffic sites needing consistent resources.

**Cloud Hosting**: [[AWS]], [[Google Cloud]], [[Microsoft Azure]] provide on-demand, scalable compute instances. "Cloud hosting" typically means cloud VMs (EC2, Compute Engine), but the term also encompasses managed services.

**[[Platform as a Service]] (PaaS)**: Heroku, Railway, Render, [[Vercel]], [[Netlify]]. The platform manages infrastructure, OS, runtime—developers push code. Great for developer experience and rapid deployment.

**[[Serverless Computing]]**: [[AWS Lambda]], Google Cloud Functions, Azure Functions. No servers to manage; code runs in response to events. Scales to zero automatically, bills per invocation. Ideal for event-driven workloads and APIs with variable traffic.

**[[Edge Computing]] / [[CDN]]-based**: [[Cloudflare Workers]], [[Vercel]] Edge Functions. Code runs in data centers close to users worldwide, with ultra-low latency. Good for request transformation, authentication, A/B testing.

### Managed vs. Unmanaged

**Managed hosting** means the provider handles server maintenance, security patches, updates, and often backups. This frees the developer from ops work but offers less control. [[Heroku]], [[Vercel]], [[Railway]], managed [[Kubernetes]] (EKS, GKE, AKS) are managed.

**Unmanaged** means you're responsible for everything. [[DigitalOcean]] Droplets, raw AWS EC2, self-hosted [[Kubernetes]]. More work, more control, potentially lower cost.

### Domain and DNS

Hosting requires a domain name registered through a registrar (GoDaddy, Namecheap, Cloudflare Registrar) and DNS configuration pointing the domain to the hosting provider's servers. [[DNS]] A records map domains to IP addresses; CNAME records map subdomains to other domains. [[Cloudflare]] provides both DNS and [[CDN]]/proxy services that sit in front of most hosting setups.

### SSL/TLS

All modern hosting should provide HTTPS. This is typically handled by:
- **Provider-managed certificates**: [[Vercel]], [[Netlify]], [[Cloudflare Workers]] provide certificates automatically via Let's Encrypt
- **Manual certificate management**: [[certbot]]/Let's Encrypt on your own servers
- **Load balancer termination**: TLS decrypted at the load balancer, traffic to servers is HTTP

## How It Works

A typical request flow for a hosted web application:

```
User types example.com
    ↓
DNS resolution (Cloudflare)
    ↓
Request hits CDN/Edge (if configured)
    ↓
Load Balancer routes to appropriate server(s)
    ↓
Application server processes request
    ↓
Response returned through CDN (static assets cached)
    ↓
User sees the website
```

For [[serverless]] functions:
```
User makes API request
    ↓
API Gateway receives request
    ↓
Lambda/Cloudflare Worker cold-starts (if needed)
    ↓
Function executes with request data
    ↓
Response returned, instance scales down (or stays warm)
```

## Practical Applications

Hosting decisions affect every stage of an application's lifecycle:

- **Static Sites**: [[Vercel]], [[Netlify]], [[Cloudflare Pages]]—push to deploy, global CDN, free tier
- **Dynamic Web Apps**: [[Heroku]], [[Railway]], [[Render]] for managed Node/Python/Ruby backends
- **High-Traffic APIs**: AWS EC2/ECS, [[Google Cloud]] Run, or managed Kubernetes for auto-scaling
- **Event-Driven Workloads**: [[AWS Lambda]], Google Cloud Functions for infrequent, bursty workloads
- **Global, Low-Latency APIs**: [[Cloudflare Workers]], [[Vercel]] Edge Functions
- **Enterprise Applications**: Dedicated servers or private cloud for compliance and control

## Examples

Deploying a Node.js app to Railway (one of the simplest PaaS options):

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and initialize
railway login
railway init

# Add a database
railway add

# Deploy (Railway auto-detects Node.js)
railway up

# Get the public URL
railway status
```

Deploying a Docker container to a VPS:

```bash
# SSH into your VPS
ssh root@your-server-ip

# Install Docker
curl -fsSL get.docker.com | sh

# Pull your image
docker pull yourregistry/your-app:latest

# Run with environment variables and restart policy
docker run -d \
  --name your-app \
  --restart unless-stopped \
  -p 80:3000 \
  -e NODE_ENV=production \
  -e DATABASE_URL=postgres://user:pass@host:5432/db \
  yourregistry/your-app:latest

# Set up nginx as a reverse proxy (optional)
# Set up Let's Encrypt for TLS (certbot --nginx)
```

Configuring a [[Cloudflare Workers]] edge function:

```javascript
// worker.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    // Rewrite requests to API
    if (url.pathname.startsWith('/api/')) {
      url.hostname = 'api.your-app.com'
      return fetch(url, {
        headers: request.headers,
        cf: { cacheTtl: 60 }, // Cache for 60 seconds at edge
      })
    }

    // Return static response
    return new Response('Hello from the edge!', {
      headers: { 'Content-Type': 'text/plain' },
    })
  },
}
```

## Related Concepts

- [[cloud-computing]] — Broader cloud infrastructure
- [[edge-computing]] — Edge-hosted code
- [[serverless]] — Serverless computing model
- [[deployment]] — Deploying applications to hosts
- [[CDN]] — Content delivery networks often paired with hosting
- [[DNS]] — Domain name system for routing
- [[Vercel]] — Popular frontend hosting platform
- [[Netlify]] — Static site and Jamstack hosting
- [[Heroku]] — Classic PaaS hosting
- [[Kubernetes]] — Container orchestration platform
- [[Virtual Machine]] — Traditional virtualization

## Further Reading

- [MDN: How to host a website](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/How_do_you_host_your_website)
- [DigitalOcean: VPS hosting tutorial](https://www.digitalocean.com/community/tutorials)
- [Serverless comparison: Lambda vs Cloudflare Workers](https://www.serverless.com/workers)
- [Cloudflare Workers documentation](https://developers.cloudflare.com/workers/)

## Personal Notes

For side projects and MVPs, I almost always start with [[Vercel]] or [[Netlify]]. The DX is unbeatable—git push to deploy, automatic HTTPS, and generous free tiers. When I need a database or background worker, I add Railway or Supabase. The moment I need more control (custom nginx config, specific database version, GPU instances), I reach for a VPS on [[DigitalOcean]]. The biggest mistake I see is teams choosing enterprise-grade infrastructure for small projects due to FOMO. Start simple, scale when you hit real limits.
