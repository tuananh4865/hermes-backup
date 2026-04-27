---
title: "Npx"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [nodejs, npm, package-manager, cli, execution]
---

# Npx

## Overview

npx is a package runner included with npm (Node Package Manager) starting at version 5.2.0. It allows developers to execute Node.js packages directly from the npm registry without globally installing them or adding them as project dependencies. This is particularly useful for one-off CLI tools, scaffolding commands, or running specific versions of packages where global installation would create version conflicts. npx searches for the requested package in the local `node_modules/.bin` directory first, then falls back to downloading and caching the latest version (or a specified version) from the npm registry. The cached packages are stored in `~/.npm/_npx`, and subsequent executions reuse the cache unless the `--cache` flag is refreshed.

## Key Concepts

**Local Execution Priority**: npx first checks if the package exists in the project's `node_modules/.bin` directory, ensuring it uses the version specified in `package.json` if present. This prevents unexpected behavior from globally installed versions.

**On-Demand Package Download**: When a package is not found locally, npx automatically downloads and executes it. This eliminates the need to globally install CLI tools that are rarely used, keeping the global environment clean.

**Version Specification**: npx supports semver ranges and specific tags, allowing execution of exact versions: `npx cowsay@1.2.3 "hello"` or `npx create-react-app@latest my-app`.

**Interactive Mode**: npx can run packages in interactive mode, prompting for input when needed. This is useful for scaffolding tools that ask questions during setup.

**Offline Execution**: Once a package is cached, npx can execute it without network access using the `--offline` flag.

## How It Works

When you invoke `npx <package-name>`, npx performs the following steps:

1. Check if `<package-name>` exists in `node_modules/.bin`
2. If not found, check if it's a scoped package or contains a slash (e.g., `@babel/core` or `webpack/cli`)
3. Resolve the version from `package.json` or use the latest version from the registry
4. Download the package tarball to the npx cache (`~/.npm/_npx`)
5. Extract to a temp directory and execute the binary

```bash
# Execute the latest version of cowsay
npx cowsay "Hello from npx"

# Execute a specific version
npx ts-node@10.4.0 script.ts

# Use a package not installed as a dependency
npx eslint@latest ./src

# Create a new React app without global install
npx create-react-app my-app
```

## Practical Applications

**Scaffolding Projects**: npx is the recommended way to run project scaffolding tools like `create-react-app`, `vite`, `ng new`, or `yeoman`. Users don't need to globally install these tools, which often have specific version requirements or are used infrequently.

**Running One-Off Scripts**: Developers can execute utility scripts published on npm without polluting the global namespace. For example, `npx spotify-docker-compose` or `npx http-server` can be run without prior installation.

**Testing Different Versions**: When debugging version-specific behavior, npx allows running a package at an exact version to verify compatibility, something that would be cumbersome with global installs.

**CI/CD Pipelines**: In continuous integration, npx ensures the exact same tool version runs across environments without relying on pre-installed globals.

## Examples

Running a local build script defined in package.json:

```bash
# If "build:prod" is defined in package.json scripts
npx -p node.js npm run build:prod
```

Executing a TypeScript compiler directly:

```bash
# Run TypeScript compiler without installing globally
npx typescript --version
npx tsc --outDir dist src/**/*.ts
```

Using npx in a CI script to ensure consistent tooling:

```bash
#!/bin/bash
set -e
cd project-directory
npx playwright install --with-deps chromium
npx playwright test
```

## Related Concepts

- [[npm]] - The package manager that bundles npx
- [[Node.js]] - The JavaScript runtime environment
- [[Yarn]] - Alternative package manager with similar exec capabilities
- [[pnpm]] - Performant npm alternative with strict dependency management
- [[package.json]] - The file defining project dependencies and scripts
