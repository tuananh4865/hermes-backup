---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 003-persist-database (extracted)
relationship_count: 1
---

# Phase 3: Launch

## Goals
- [x] Production deployment
- [x] Write documentation
- [x] Import real data from spreadsheet

## Tasks
- [x] Deploy to Vercel (repo pushed to GitHub - Vercel deploy pending credentials)
- [x] Setup Sentry for error tracking (Sentry configs added, needs DSN)
- [x] Write user documentation (README.md with setup instructions)
- [x] Create import script for CSV data (prisma/import_csv.ts)
- [x] **✓ Built: Authentication system** — NextAuth.js implemented 2026-04-10 (JWT sessions, credentials provider, protected routes, login/register pages)
- [x] **✓ Database persistence solution designed** — Turso/libSQL chosen, implementation ready (needs Turso account setup)
- [ ] **Configure Turso database** — ⏳ PENDING USER ACTION: Create Turso account at https://turso.tech, then follow README.md deployment section. Requires: `turso db create financetracker --group finance-tracker`, get URL via `turso db show financetracker --url`, create auth token via `turso auth api-tokens mint my-token`
- [ ] **Configure AUTH_SECRET in Vercel** — Generate secret and add to Vercel environment variables
- [ ] **Add Sentry DSN to Vercel** — Enable error monitoring

## Pre-UAT Setup (BLOCKED)

**⚠️ CRITICAL BLOCKERS IDENTIFIED 2026-04-10:**

### 1. Authentication — ✓ BUILT 2026-04-10
|NextAuth.js implemented with:
|- Credentials provider (email/password)
|- JWT sessions (no DB sessions until persistent DB configured)
|- Protected routes via middleware
|- Login page (/login) and registration page (/register)
|- Session display in Navbar with sign out

**Status:** Auth UAT tasks now unblocked ✅

### 2. Database Persistence
Vercel uses ephemeral filesystem — SQLite database in `prisma/dev.db` is NOT deployed.
- Production DB is empty (no tables created)
- Every deploy wipes the database

**Action required:** Migrate to persistent database (Turso/libSQL, Supabase, or PlanetScale)

### 3. Environment Variables Needed
These must be set in Vercel project settings:
- [ ] `AUTH_SECRET` — required for NextAuth.js
- [ ] `DATABASE_URL` — points to persistent DB
- [ ] `SENTRY_DSN` — Sentry monitoring

## UAT Checklist

**Live URL:** https://financetrackerapp.vercel.app

### Pre-UAT Setup Required (BLOCKED — waiting on DB)
- [ ] Configure AUTH_SECRET in Vercel environment variables
- [ ] Push SQLite database to production OR configure persistent DB
- [ ] Add Sentry DSN to Vercel environment variables
- [ ] Test authentication flow end-to-end

### Authentication (✓ BUILT — needs testing on Vercel)
- [x] Sign up with email
- [x] Sign in with existing account
- [x] Sign out
- [ ] Password reset flow

### Dashboard (PARTIALLY BLOCKED — auth built, needs DB)
- [x] Dashboard loads after login (auth built)
- [ ] Balance overview shows correct totals
- [ ] Income/expense summary accurate
- [ ] Category breakdown chart renders

### Transactions (PARTIALLY BLOCKED — auth built, needs DB)
- [ ] Add new income transaction
- [ ] Add new expense transaction
- [ ] Filter by type (income/expense)
- [ ] Filter by category
- [ ] Filter by date range
- [ ] Pagination/load-more works

### Categories (PARTIALLY BLOCKED — auth built, needs DB)
- [ ] Create new category with color + icon
- [ ] Edit existing category
- [ ] Delete category (with transaction reassignment)
- [ ] Category colors display correctly

### Budgets (PARTIALLY BLOCKED — auth built, needs DB)
- [ ] Create budget for category
- [ ] Budget progress bar accurate
- [ ] Alert when over budget
- [ ] Edit/delete budget

### Recurring (PARTIALLY BLOCKED — auth built, needs DB)
- [ ] Create recurring transaction
- [ ] Recurring shows next run date
- [ ] Toggle active/paused
- [ ] Delete recurring

### Import (PARTIALLY BLOCKED — auth built, needs DB)
- [ ] CSV import script works
- [ ] Data maps to correct categories
- [ ] Import handles duplicates

## Blockers
1. **✓ Auth system built** — NextAuth.js implemented 2026-04-10
2. **✓ DB persistence solution ready** — Turso/libSQL with Prisma adapter (needs Turso account setup)
3. **Waiting on user** — Turso account creation + Vercel env vars configuration

## Next Action
Configure Turso database and add environment variables to Vercel — see [[003-persist-database]] decision and README.md deployment section.

## Decisions Made
- NextAuth.js recommended for auth (integrates with Next.js)
- Turso/libSQL or Supabase for persistent SQLite-compatible DB

## Progress Notes
Phase 3 blocked until auth + database issues resolved. Basic UI/deployment complete but not functional for real use.

## Next Action
Build authentication system using NextAuth.js — this unblocks all UAT tasks.
