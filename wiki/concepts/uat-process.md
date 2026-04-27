---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 testing (extracted)
  - 🔗 quality (extracted)
  - 🔗 deployment (inferred)
last_updated: 2026-04-11
tags:
  - testing
  - UAT
  - QA
  - process
---

# UAT Process

> User Acceptance Testing — the final testing phase before production release.

## Overview

UAT (User Acceptance Testing) is when end users validate that software meets their business needs before going live. It's the last gate before production deployment.

**Key Principle:** If it passes UAT but users hate it, it failed UAT.

## UAT vs Other Testing

| Testing Type | Who | What | When |
|-------------|-----|------|------|
| Unit | Developers | Individual functions | During development |
| Integration | Developers | Module interactions | After features |
| System | QA | Complete system | Pre-UAT |
| **UAT** | **End users** | **Business requirements** | **Pre-production** |
| Performance | QA/DevOps | Load, stress | Before launch |

## UAT Process Flow

```
┌─────────────────────────────────────────────────────────────┐
│  1. PLAN UAT                                               │
│  - Define scope                                             │
│  - Identify users                                           │
│  - Create test cases                                        │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  2. PREPARE TESTING                                        │
│  - Set up environment                                       │
│  - Train users                                              │
│  - Distribute test cases                                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  3. EXECUTE TESTING                                        │
│  - Users test scenarios                                     │
│  - Document results                                         │
│  - Report bugs                                              │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  4. RESOLVE ISSUES                                         │
│  - Triage bugs by priority                                 │
│  - Fix critical issues                                     │
│  - Re-test fixes                                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  5. SIGN-OFF                                               │
│  - Review test results                                     │
│  - Get stakeholder approval                                 │
│  - Authorize deployment                                     │
└─────────────────────────────────────────────────────────────┘
```

## Creating Test Cases

### Test Case Template
```
Test Case ID: TC-001
Title: User can log in with email/password
Priority: P0 (Critical)
Prerequisites: User has registered account

Steps:
1. Navigate to /login
2. Enter email: user@example.com
3. Enter password: correctpassword
4. Click "Sign In" button

Expected Result:
- User is redirected to dashboard
- Welcome message appears
- Session persists on page refresh

Test Data:
- Email: user@example.com
- Password: correctpassword
```

### Test Case Examples

#### Login Flow
```
TC-001: Successful login
TC-002: Invalid email format
TC-003: Wrong password
TC-004: Account locked after 5 failed attempts
TC-005: Password reset flow
```

#### E-commerce
```
TC-101: Add item to cart
TC-102: Remove item from cart
TC-103: Update item quantity
TC-104: Apply discount code
TC-105: Checkout with valid card
TC-106: Checkout with expired card
```

## Identifying Testers

### Who Should Test
- **Power users**: Know the system well, find edge cases
- **End users**: Representative of target audience
- **Stakeholders**: Product owner, business analysts

### Tester Selection Criteria
1. Representative of actual users
2. Available during UAT window
3. Trained on the system
4. Empowered to approve/reject

## Bug Reporting

### Bug Report Template
```
Bug ID: BUG-001
Title: Cart total doesn't update when quantity changed
Severity: High
Priority: P1
Environment: Chrome 123, macOS 14
Steps to Reproduce:
1. Add item to cart (price: $10)
2. Click quantity dropdown
3. Change quantity to 3
4. Observe cart total

Expected: Cart total shows $30
Actual: Cart total shows $10
Frequency: 100%

Attachments:
- Screenshot
- Screen recording
```

### Severity vs Priority

| Severity | Description | Example | Priority |
|----------|-------------|---------|----------|
| Critical | System unusable | Login broken | P0 |
| High | Major feature broken | Checkout fails | P1 |
| Medium | Feature degraded | Slow search | P2 |
| Low | Minor issue | Typo in label | P3 |

## UAT Sign-Off

### Sign-Off Checklist
```
□ All P0 bugs fixed
□ All P1 bugs fixed or accepted
□ Test coverage complete
□ Test results documented
□ User feedback incorporated
□ Stakeholders briefed
□ Rollback plan confirmed
□ Deployment window communicated
```

### Sign-Off Document
```markdown
# UAT Sign-Off

Project: [Project Name]
UAT Period: 2026-04-01 to 2026-04-05
Environments: staging.acme.com

## Test Summary
| Category | Total | Passed | Failed |
|----------|-------|--------|--------|
| Login | 15 | 14 | 1 |
| Checkout | 20 | 19 | 1 |
| Profile | 10 | 10 | 0 |

## Critical Bugs (P0)
- [x] BUG-001: Cart total issue — FIXED

## Open Issues (P1)
- [ ] BUG-010: Slow search on large catalogs — ACCEPTED (fix in v1.1)

## Decision
[ ] APPROVED for production deployment
[ ] NOT APPROVED — requires fixes

Approvers:
- Product Owner: _______________
- QA Lead: _______________
- Tech Lead: _______________

Date: 2026-04-05
```

## Common UAT Mistakes

### 1. Starting UAT Too Late
UAT should begin when system testing is complete, not when you run out of time.

### 2. Unclear Requirements
If requirements aren't clear, test cases can't be definitive.

### 3. Insufficient Training
Users can't test what they don't understand.

### 4. Ignoring Low-Priority Bugs
Low-priority bugs often mask deeper issues.

### 5. Skipping Sign-Off
Production deployment without sign-off is risky.

## Automation in UAT

### What Can Be Automated
- Smoke tests (critical paths)
- Regression tests
- Performance benchmarks

### What Must Stay Manual
- Exploratory testing
- UX/UI validation
- Business workflow approval

## Related Concepts

- [[testing]] — Testing fundamentals
- [[quality]] — Quality assurance
- [[deployment]] — Deployment processes
- [[ci-cd]] — CI/CD pipelines
- [[automation]] — Test automation

## External Resources

- [ISTQB Glossary](https://www.istqb.org/)
- [UAT Best Practices](https://www.guru99.com/user-acceptance-testing.html)
