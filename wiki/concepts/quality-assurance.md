---
title: "Quality Assurance (QA)"
description: "The systematic process of ensuring software meets specified requirements and is free of defects, encompassing testing, validation, and verification activities across the development lifecycle."
tags: [testing, software-engineering, quality, QA, automated-testing, CI/CD]
created: 2026-04-12
updated: 2026-04-20
type: concept
sources:
  - https://testing.googleblog.com/2021/06/code-quality-quality-assurance.html
  - https://www.oreilly.com/library/view/test-driven-development/0321146530/
related:
  - [[automated-testing]]
  - [[code-review]]
  - [[static-analysis]]
  - [[continuous-integration]]
  - [[software-testing]]
---

# Quality Assurance (QA)

Quality Assurance in software is the discipline of ensuring that code does what it's supposed to do and doesn't do what it shouldn't. It's not just "testing" — it's a systematic approach to building confidence in the correctness, reliability, and security of software across its entire lifecycle.

## QA in the AI Coding Era (2026)

The rise of AI coding assistants has fundamentally changed QA:

- **AI writes code fast** — human review can't keep up with AI's speed of code generation
- **Tests can be AI-generated** too — automated testing with AI-generated test cases
- **The bottleneck shifted** — from writing code to verifying code is correct
- **New failure modes** — AI-generated code can be confidently wrong, requiring stronger verification

The pattern that works in 2026: use AI to generate tests, use AI to generate code, but use humans + AI together to verify correctness.

## The Testing Pyramid

The foundational framework for QA:

```
        /\
       /  \       E2E Tests (few, slow, expensive)
      /----\      — User flows, critical paths
     /      \     
    /--------\    Integration Tests (some, medium)
   /          \   — API contracts, service interactions
  /------------\  
 /              \ Unit Tests (many, fast, cheap)
/----------------\ — Individual functions, classes
```

The key principle: **more tests at lower levels** because they're faster, cheaper, and more specific. E2E tests are necessary but should be reserved for truly critical paths.

## Types of Testing

### Unit Tests
- Test individual functions/methods in isolation
- Mock all dependencies
- Run in milliseconds
- Should constitute 70%+ of your test suite

### Integration Tests
- Test how components interact (e.g., database queries, API calls)
- Use real dependencies where feasible
- Critical for catching contract mismatches

### End-to-End (E2E) Tests
- Test complete user flows (click button → see result)
- Slowest, most expensive, most brittle
- Use tools like Playwright, Cypress, Puppeteer

### Property-Based Testing
- Generate random inputs to verify properties hold (e.g., "for all lists, sort(list) returns a sorted list")
- Excellent for finding edge cases humans miss
- Tools: Hypothesis (Python), fast-check (JS)

## Shift-Left: Moving QA Earlier

Traditional QA: write code → send to QA team → find bugs → fix
Shift-left: write tests alongside code → catch bugs immediately

AI coding assistants enable shift-left at scale:
1. Write the function signature and docstring
2. Ask AI to generate the implementation + test cases simultaneously
3. Run tests immediately
4. If tests fail, iterate with AI

## Test-Driven Development (TDD)

The discipline of writing tests *before* code:

```
Red → Green → Refactor
1. Write a failing test
2. Write minimum code to pass it
3. Refactor for clarity
Repeat
```

TDD creates:
- Tests that actually test what you need (not what the code does)
- Living documentation of intended behavior
- Confidence to refactor

## CI/CD + QA

In modern development, QA is automated into the pipeline:

```yaml
# GitHub Actions example
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run unit tests
      run: pytest tests/unit --cov=src
    - name: Run integration tests
      run: pytest tests/integration
    - name: E2E tests
      run: playwright test
```

Every PR must pass all tiers before merge.

## AI-Assisted QA in 2026

New tooling has emerged:

- **AI-generated test cases**: Given a function, AI suggests edge cases and generates test inputs
- **Automated bug reproduction**: Paste an error message → AI generates a minimal repro case
- **Regression detection**: AI identifies which existing tests are likely to break given a code change

## Related Concepts

- [[automated-testing]] — writing tests that run automatically
- [[code-review]] — human QA gate in the code review process
- [[static-analysis]] — automated code quality checks without execution
- [[continuous-integration]] — automated testing on every commit
- [[software-testing]] — broader category of testing techniques
