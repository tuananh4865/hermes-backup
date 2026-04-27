---
title: Rowboat
created: 2026-04-18
updated: 2026-04-18
type: entity
entity_type: software_repository
tags: [electron, monorepo, desktop-app, rowboatlabs]
confidence: high
relationships: []
---

# Rowboat

## Overview

**Rowboat** là một Electron desktop application monorepo được phát triển bởi **rowboatlabs**. Repository chứa nhiều ứng dụng trong một codebase, bao gồm desktop app, web dashboard, CLI tools, và Python SDK.

## Repository Structure

```
rowboat/
├── apps/
│   ├── x/                 # Electron desktop app (MAIN FOCUS)
│   ├── rowboat/           # Next.js web dashboard
│   ├── rowboatx/          # Next.js frontend
│   ├── cli/               # CLI tool
│   ├── python-sdk/        # Python SDK
│   └── docs/              # Documentation site
├── CLAUDE.md              # AI coding agent context
└── README.md              # User-facing readme
```

## Electron App Architecture (apps/x)

Đây là core của Rowboat — một nested pnpm workspace:

```
apps/x/
├── apps/
│   ├── main/              # Electron main process
│   │   ├── src/           # Main process source
│   │   ├── forge.config.cjs   # Electron Forge config
│   │   └── bundle.mjs     # esbuild bundler
│   ├── renderer/          # React UI (Vite)
│   │   ├── src/           # React components
│   │   └── vite.config.ts
│   └── preload/           # Electron preload scripts
│       └── src/
└── packages/
    ├── shared/            # @x/shared - Types, utilities, validators
    └── core/              # @x/core - Business logic, AI, OAuth, MCP
```

### Build Order (Dependencies)

```
shared (no deps)
   ↓
core (depends on shared)
   ↓
preload (depends on shared)
   ↓
renderer (depends on shared)
   ↓
main (depends on shared, core)
```

## Key Commands

```bash
# Install dependencies
cd apps/x && pnpm install

# Build workspace packages (shared → core → preload)
cd apps/x && npm run deps

# Development mode (builds deps, runs app)
cd apps/x && npm run dev

# Production build (.app)
cd apps/x/apps/main && npm run package

# Create DMG distributable
cd apps/x/apps/main && npm run make
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Desktop Framework | Electron |
| UI | React + Vite |
| Package Manager | pnpm |
| Build System | Electron Forge |
| Bundler | esbuild |

## Clone Location

```
/Volumes/Storage-1/Hermes/rowboat
```

## Source

- GitHub: https://github.com/rowboatlabs/rowboat
