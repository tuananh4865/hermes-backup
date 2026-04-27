---
title: Blue-Green Deployment
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [deployment, devops, release, infrastructure, high-availability]
---

# Blue-Green Deployment

Blue-green deployment is a release strategy that maintains two identical production environments and switches traffic between them to achieve zero-downtime deployments. This approach provides instant rollback capability and minimizes risk during releases.

## Overview

The strategy involves keeping two parallel production environments—conventionally called "blue" and "green." At any given time, one environment serves all production traffic while the other sits idle, ready to receive the next release. When deploying a new version, operators first deploy to the inactive environment, thoroughly test it, then switch the load balancer to direct traffic to the newly updated environment. If anything goes wrong, the switch can be reversed immediately, restoring the previous state.

This pattern was popularized by Netflix and other tech companies that require high availability. It transforms deployment from a risky operation into a reversible, low-stress event.

## Key Concepts

### Environment Parity

Both environments must be identical in configuration:
- Same operating system and runtime versions
- Same middleware and service dependencies
- Same network configuration and security rules
- Same data stores and connection strings

Infrastructure-as-code tools like Terraform or Pulumi help maintain this parity programmatically.

### Traffic Switching

The router or load balancer controls which environment receives traffic:
```yaml
# Example: Nginx upstream switching
upstream backend {
    server blue-env:8080;  # Currently active
    # server green-env:8080;  # Standby
}

# On deployment, swap which server is commented:
upstream backend {
    # server blue-env:8080;  # Previous version
    server green-env:8080;  # New version now active
}
```

### Database Considerations

Database migrations require special care in blue-green deployments:
- **Expand-Contract Pattern**: Add new columns/tables in one release, remove in a later one
- **Backward-Compatible Schemas**: Always ensure old code can read new schema
- **Blue-Green with Read Replicas**: Use a read replica of the primary database

## How It Works

1. **Initial State**: Blue environment runs version N, green is identical but idle
2. **Deploy**: Version N+1 is deployed to the green environment
3. **Test**: Operators verify green environment health using pre-production checks
4. **Cutover**: Load balancer switches traffic from blue to green (often < 1 second)
5. **Monitor**: Observe error rates and metrics on the newly active environment
6. **Rollback** (if needed): Reverse the load balancer to point back to blue

## Practical Applications

- **E-commerce Platforms**: Deploy new features before holiday shopping seasons without risk
- **Financial Services**: Meet uptime SLAs while continuously improving compliance features
- **SaaS Applications**: Ship updates frequently without user-facing downtime
- **Microservices**: Coordinate deployments across multiple interdependent services

## Examples

A complete blue-green deployment with Docker Compose:

```yaml
# docker-compose.blue.yml (current production)
services:
  app:
    image: myapp:v1.0.0
    environment:
      - ENVIRONMENT=production
    networks:
      - frontend
      - backend

# docker-compose.green.yml (new version to deploy)
services:
  app:
    image: myapp:v1.1.0
    environment:
      - ENVIRONMENT=production
    networks:
      - frontend
      - backend
```

Deployment script:

```bash
#!/bin/bash
# deploy.sh - Blue-green deployment script

CURRENT_ENV="blue"
NEW_ENV="green"
HEALTH_URL="https://api.example.com/health"

# Deploy new version to standby environment
docker-compose -f docker-compose.${NEW_ENV}.yml up -d

# Wait for health check
for i in {1..30}; do
    if curl -sf "${HEALTH_URL}" > /dev/null; then
        echo "Health check passed"
        break
    fi
    echo "Waiting for health check... attempt $i"
    sleep 2
done

# Switch traffic (Nginx reload)
nginx -s reload

# Keep old environment running for quick rollback
echo "Deployment complete. Old environment preserved for 30 minutes."
```

## Related Concepts

- [[canary-deployments]] — Gradual rollout strategy releasing to a subset of users first
- [[infrastructure-as-code]] — Managing infrastructure through code definitions
- [[load-balancing]] — Distributing traffic across multiple servers
- [[continuous-deployment]] — Automated deployment pipeline practices
- [[database-migration]] — Schema migration strategies for production systems

## Further Reading

- Infrastructure patterns from Netflix: "From Netflix to Now"
- AWS Blue-Green Deployment documentation
- The Book of Kubernetes: Deployment Strategies

## Personal Notes

Blue-green deployments shine when combined with comprehensive automated testing. The ability to rollback instantly only matters if you detect problems quickly. Investing in good observability (metrics, logs, traces) is essential. Also consider the cost of running two full environments—this pattern is more expensive than canary but provides cleaner rollback semantics.
