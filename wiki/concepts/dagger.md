---
title: "Dagger"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ci-cd, devops, containers, programming]
---

# Dagger

## Overview

Dagger is a modern CI/CD pipeline framework that allows developers to define continuous integration and deployment workflows as code, portable across different CI providers. Unlike traditional CI/CD systems that rely on provider-specific YAML configurations, Dagger uses general-purpose programming languages (primarily Go and CUE) to express pipelines, making them testable locally, reusable, and version-controlled like application code.

The core innovation behind Dagger is its use of containers as the execution environment for pipeline steps. Each step in a Dagger pipeline runs inside a container, ensuring consistency between local development and CI environments. This approach eliminates the classic "works on my machine" problem by guaranteeing that what runs locally will produce identical results in production CI systems.

## Key Concepts

**Pipelines as Code**: Dagger pipelines are defined in code rather than YAML, enabling developers to use familiar programming constructs like loops, functions, conditionals, and variables. This makes complex workflows easier to express and maintain.

**Container-Native Execution**: Every Dagger operation executes within a container, with automatic handling of volume mounts, environment variables, and networking. This provides strong isolation and reproducibility.

**Cross-Platform Compatibility**: Dagger pipelines work identically across different CI providers including GitHub Actions, GitLab CI, Jenkins, CircleCI, and local development machines.

**CUE Language**: Dagger uses CUE (CUE Unifying Environment) as its primary configuration language, which provides a terse, declarative syntax with powerful validation capabilities.

## How It Works

Dagger operates through a client-server architecture where the local Dagger CLI acts as a client that communicates with a Dagger engine running in containers. When you execute a Dagger pipeline:

1. The Dagger CLI reads your pipeline definition written in CUE or Go
2. It compiles this definition into a directed acyclic graph (DAG) of operations
3. The Dagger engine resolves dependencies between pipeline steps
4. Each step executes in an appropriate container with proper resource allocation
5. Results flow between steps as typed values, not just files

The engine handles caching intelligently, reusing container layers and computation results across pipeline runs when inputs haven't changed.

## Practical Applications

Dagger is particularly valuable for teams managing complex deployment workflows:

- **Microservices Deployment**: Orchestrating multi-service deployments with interdependent release sequences
- **Build Pipeline Standardization**: Creating reusable build templates across multiple projects
- **Cross-Platform Testing**: Running identical test suites across different CI providers
- **Local CI Development**: Developing and debugging CI pipelines locally before committing

## Examples

A simple Dagger pipeline in CUE that builds and tests a Node.js application:

```cue
package main

import (
	"dagger.io/dagger"
	"dagger.io/dagger/core"
)

dagger.#Plan & {
	actions: {
		build: core.#Image & {
			rootfs: dagger.#FS
		}
		readJson: core.#File & {
			path: "/app/package.json"
		}
		install: core.#Exec & {
			input:  build.output
			command: name: "npm"
			args:    ["install"]
			workdir: "/app"
		}
		test: core.#Exec & {
			input:  install.output
			command: name: "npm"
			args:    ["test"]
			workdir: "/app"
		}
	}
}
```

## Related Concepts

- [[ci-cd]] - Continuous Integration and Deployment practices
- [[Containers]] - Container technology that powers Dagger execution
- [[GitHub Actions]] - Popular CI platform that Dagger can run on
- [[GitLab CI]] - GitLab's CI/CD platform compatible with Dagger
- [[DevOps]] - The broader practice Dagger helps implement

## Further Reading

- [Dagger Official Documentation](https://docs.dagger.io/)
- [Dagger GitHub Repository](https://github.com/dagger/dagger)
- [CUE Language Documentation](https://cuelang.org/)

## Personal Notes

Dagger represents a significant shift in how teams think about CI/CD infrastructure. The ability to test pipelines locally before committing them has been a long-standing pain point in DevOps. The container-native approach also means less time spent debugging environment differences between local and CI. However, the CUE language has a learning curve, and teams already invested heavily in YAML-based CI systems may face adoption challenges.
