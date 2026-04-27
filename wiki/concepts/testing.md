---
title: "Testing (Software)"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-engineering, quality, automation, tdd, qa]
---

# Testing (Software)

## Overview

Software testing is the systematic process of evaluating a software application or system to identify defects, verify functional requirements, and provide assurance that the delivered product meets specified quality standards. Testing encompasses a wide range of activities from manual exploratory sessions to fully automated regression suites. The fundamental goal is to uncover failures before they reach production, reducing risk and improving user satisfaction. Software testing is not merely a gatekeeping activity but an integral part of the development lifecycle that informs design decisions, documents expected behavior, and enables confident refactoring. Effective testing strategies balance coverage, speed, and maintenance cost, adapting to project size, regulatory requirements, and team expertise. The field has evolved from purely manual inspection processes in the early computing era to a sophisticated discipline with specialized roles, frameworks, and automated tooling.

## Key Concepts

**Test Pyramid**: A foundational model advocating for a broad base of unit tests, a narrower layer of integration tests, and a small number of end-to-end tests. This distribution prioritizes fast, focused feedback while still validating system behavior at higher levels.

**Black Box vs. White Box Testing**: Black box testing examines functionality without knowledge of internal implementation—testers interact with interfaces and verify outputs. White box testing leverages knowledge of internal structure, code paths, and logic to design targeted tests.

**Test-Driven Development (TDD)**: A discipline where tests are written before the code they verify. The Red-Green-Refactor cycle (write failing test, write minimal code to pass, then refactor) drives design and ensures testability.

**Assertion**: A statement in a test that expresses expected behavior, such as `assert.equal(actual, expected)`. Tests fail when assertions do not hold, signaling a defect or changed requirement.

**Test Fixture**: The preconditions and environment setup required for a test to execute reproducibly. Fixtures may include mock objects, database state, configuration, or helper functions.

**Mock, Stub, Spy**: Test doubles that replace real dependencies. Mocks verify interactions occurred; stubs provide predetermined responses; spies record how a function was called.

## How It Works

A typical automated test follows the Arrange-Act-Assert pattern:

```javascript
// Arrange: Set up test dependencies and inputs
const calculator = new Calculator();
const operands = [2, 3, 5];

// Act: Execute the behavior being tested
const result = calculator.sum(operands);

// Assert: Verify the outcome matches expectations
assert.equal(result, 10);
```

Unit tests isolate individual functions or classes, running in milliseconds and providing precise failure locations. Integration tests verify that components work together correctly—connecting to databases, message queues, or external APIs.

End-to-end (E2E) tests simulate real user workflows through the full application stack, typically using browser automation tools like Playwright or Cypress.

Continuous Integration (CI) pipelines automatically run test suites on every code push, blocking merges when tests fail and providing rapid feedback to developers.

## Practical Applications

Testing applies across virtually all software domains:

**Web Applications**: Unit tests for business logic, integration tests for API endpoints and database queries, E2E tests for user flows like checkout or login. Frameworks like Jest, Mocha, pytest, and JUnit are standard tools.

**APIs**: REST and GraphQL APIs are tested by sending requests and validating responses against schemas and business rules. Tools like Postman, Insomnia, and automated HTTP clients verify status codes, payloads, and performance.

**Databases**: Tests verify migration scripts, query correctness, and ORM behavior. Test databases are often containerized to ensure reproducible state.

**Infrastructure as Code**: Terraform, Ansible, and CloudFormation configurations are tested using tools like Terratest, kitchen-terraform, or policy engines to prevent misconfigured deployments.

## Examples

A comprehensive test suite for a Node.js API endpoint using Jest:

```javascript
const request = require('supertest');
const app = require('../../src/app');
const { createTestUser, cleanDatabase } = require('../helpers');

describe('POST /api/users', () => {
    beforeEach(async () => {
        await cleanDatabase();
    });

    it('creates a new user with valid input', async () => {
        const response = await request(app)
            .post('/api/users')
            .send({ email: 'test@example.com', name: 'Test User' })
            .expect(201);

        expect(response.body).toMatchObject({
            email: 'test@example.com',
            name: 'Test User'
        });
        expect(response.body.id).toBeDefined();
    });

    it('returns 400 for duplicate email', async () => {
        await createTestUser({ email: 'existing@example.com' });

        await request(app)
            .post('/api/users')
            .send({ email: 'existing@example.com', name: 'Another' })
            .expect(400)
            .expect({ error: 'Email already exists' });
    });
});
```

## Related Concepts

- [[Test-Driven Development]] - The practice of writing tests first
- [[Unit Testing]] - Testing individual components in isolation
- [[Integration Testing]] - Testing component interactions
- [[Continuous Integration]] - Automated testing in the development pipeline
- [[Mock Objects]] - Test doubles for isolating units under test
- [[Quality Assurance]] - The broader discipline of maintaining software quality
