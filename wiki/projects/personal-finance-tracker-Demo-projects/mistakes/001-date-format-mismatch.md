---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 001-tech-stack (extracted)
  - 🔗 001-tech-stack (extracted)
  - 🔗 phase-2-build (extracted)
relationship_count: 3
---

# 2026-04-09 — Date format mismatch in transaction API

## What Happened

Transaction list component displayed dates incorrectly:
- Frontend expected: `2026-04-09` (ISO 8601)
- API returned: `09/04/2026` (DD/MM/YYYY)
- Result: Dates showed as December 2026 instead of April 2026

Error manifested as: transactions sorted incorrectly, date picker range wrong.

## Root Cause

**Assumption without validation**

Frontend component used `new Date(string)` which interprets `09/04/2026` as MM/DD/YYYY format. When parsing `09/04/2026`:
- JavaScript reads it as September 4th (month 9)
- Instead of intended April 9th

Backend Prisma was formatting dates with `format('dd/MM/yyyy')` from date-fns, but frontend expected ISO strings for JavaScript Date objects.

**Why it happened:**
1. No explicit schema contract between frontend and backend
2. Assumed "dates will work" without specifying format
3. No validation on frontend to check if date parsing was correct
4. No integration test to catch format mismatch

## Lesson Learned

**Always specify date format contract in API early**

Options:
1. **Best**: Use ISO 8601 (UTC) throughout — `2026-04-09T00:00:00Z`
2. Accept ISO strings on frontend, let API return UTC
3. If custom format needed, document explicitly and add validation

**Never rely on implicit assumptions about data format**

## Prevention Actions

- [ ] Add API response schema validation (Zod or similar)
- [ ] Add integration test: verify date parsing works both directions
- [ ] Document date format in [[001-tech-stack]] decision
- [ ] Add `date-fns` parseExact with explicit format string

## Context

**When discovered**: During phase-2-build testing
**Time spent debugging**: 2.5 hours
**Files involved**:
- `pages/api/transactions.ts` (API handler)
- `components/TransactionList.tsx` (frontend)
- `prisma/schema.prisma` (date fields)

## Related

- [[001-tech-stack]] — Tech stack had no explicit date contract
- [[phase-2-build]] — Current phase affected
