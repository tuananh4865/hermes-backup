---
title: "003-persist-database"
created: 2026-04-10
updated: 2026-04-10
type: decision
status: decided
phase: phase-3-launch
tags: [decision, database, vercel, turso, prisma]
---

# Decision: Database Persistence Strategy

## Context

Vercel uses ephemeral filesystem — SQLite database in `prisma/dev.db` is NOT persisted between deploys. Every push to GitHub wipes the database. This is a **critical blocker** for Phase 3 launch.

The app uses Prisma ORM with SQLite. NextAuth.js has been implemented with JWT sessions (no DB adapter needed).

## Options Considered

### Option 1: Turso/libSQL + Prisma Adapter
**Pros:**
- SQLite-compatible — minimal schema changes
- Zero-config Vercel integration via `@tursodatabase/vercel-experimental`
- libSQL replication to local serverless function
- Works with existing Prisma schema

**Cons:**
- BETA software (as of April 2026)
- Requires Turso API token + organization setup
- New preview feature in Prisma (driverAdapters)

### Option 2: Supabase (PostgreSQL)
**Pros:**
- Mature, production-ready
- Generous free tier
- Prisma native support

**Cons:**
- Requires schema migration (SQLite → PostgreSQL)
- PostgreSQL vs SQLite differences (TEXT vs VARCHAR limits, etc.)
- Auth setup more complex

### Option 3: Vercel Postgres (Neon)
**Pros:**
- First-party Vercel integration
- Serverless SQL database
- Native Next.js support

**Cons:**
- Requires schema migration
- Separate billing (not free tier)

## Decision

**Chosen: Option 1 — Turso/libSQL + Prisma Adapter**

### Rationale
1. Minimal code change — same SQLite schema, just change connection adapter
2. `@tursodatabase/vercel-experimental` provides zero-config integration
3. Local development still uses SQLite, production uses Turso
4. Prisma supports libSQL via `@prisma/adapter-libsql` preview feature

### Implementation Steps

1. Install dependencies:
   - `npm install @prisma/adapter-libsql @libsql/client`
   - `npm install @tursodatabase/vercel-experimental`

2. Update `prisma/schema.prisma` — add `previewFeatures = ["driverAdapters"]`

3. Update `src/lib/prisma.ts` — create adapter-based Prisma client for Turso

4. Add environment variables to Vercel:
   - `TURSO_DATABASE_URL` — Turso database URL
   - `TURSO_AUTH_TOKEN` — Turso auth token

5. Push local SQLite schema to Turso:
   - `npx prisma db push` with DATABASE_URL pointing to Turso

### Tradeoffs Accepted
- Using BETA software for production DB — accepted given the minimal migration path
- Preview feature in Prisma — acceptable for personal project

## Status
✅ Decided: 2026-04-10