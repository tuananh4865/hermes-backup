---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 phase-1-init (extracted)
  - 🔗 phase-2-build (extracted)
relationship_count: 2
---

# 001 — Tech Stack

## Context
Need to choose web framework + ORM + database for the finance tracker. Was debating between Django (Python) vs Next.js (JS/TS).

## Options Considered
1. **Django + PostgreSQL** — Full-featured, great ORM, but verbose setup
2. **Next.js + Prisma + SQLite** — Modern, fast prototyping, easy AI integration
3. **Vue + Supabase** — Good alternative, but less familiar to Anh

## Decision Made
**Chosen**: Option 2 — Next.js + Prisma + SQLite

## Rationale
- Next.js + TypeScript quen thuộc hơn sau nhiều project
- Prisma ORM giúp schema management dễ dàng, migrate đơn giản
- SQLite đủ cho personal use, không cần setup database server
- Có thể deploy lên Vercel miễn phí

## Consequences
- Phải handle SQLite concurrency issues nếu cần
- Migration từ SQLite → PostgreSQL khi scale sẽ cần effort
- Prisma client phải compatible với Next.js version

## Related
- [[phase-1-init]]
- [[phase-2-build]]
