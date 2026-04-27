---
title: "Smoke Testing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [smoke-testing, testing, quality-assurance, sanity-testing, regression-testing, continuous-integration, rapid-testing]
---

# Smoke Testing

## Overview

Smoke testing is a type of software testing that evaluates whether the most critical and fundamental functions of an application work correctly after a build or code change. The term originated from hardware testing — if you plug in a new piece of hardware and it starts smoking, you know something is fundamentally wrong. Similarly, in software, smoke tests verify that the basic "vital signs" of the application are present before proceeding with more thorough testing. If the smoke tests fail, the build is rejected without further investigation.

Smoke tests are designed to be fast — typically completing in minutes rather than hours — so they can be run on every build without creating bottlenecks in the development process. They provide immediate feedback about whether a build is stable enough for more detailed testing. If the application cannot even start, or if critical paths like login and core workflows are broken, there is no point in running comprehensive test suites that would take hours to complete.

The practice of smoke testing is essential in modern CI/CD pipelines where builds may be produced multiple times per day. Rather than waiting for a full regression suite to complete before discovering that a build is fundamentally broken, smoke tests catch critical issues within minutes of a build being produced. This allows developers to receive immediate feedback and fix issues while the context of their changes is still fresh.

## Key Concepts

### Critical Path Testing

Smoke tests focus on critical path functionality — the essential features that users must be able to access for the application to be considered usable. What constitutes the critical path varies by application, but it typically includes:

- **Application startup**: The application launches without crashes or fatal errors
- **Authentication**: Users can log in successfully (and log out)
- **Core workflow**: The primary user task can be completed
- **Navigation**: Key sections of the application are accessible
- **API connectivity**: The application can communicate with required backend services

If any of these critical path elements fail, the application is not fit for further testing, regardless of how well other features work.

### Build Verification

Smoke testing is closely associated with build verification — the process of confirming that a new build is fit for testing. Before a build is promoted to a testing environment or before a deployment proceeds to the next stage, smoke tests are run to confirm basic functionality. If smoke tests pass, the build proceeds. If they fail, the build is rejected and returned to the development team.

In continuous integration environments, smoke tests are often the first tests to run after a build artifact is produced. Only after smoke tests pass does the build proceed to more comprehensive testing stages like integration testing, system testing, and full regression suites.

### Difference from Sanity Testing

Smoke testing and sanity testing are sometimes confused but serve different purposes:

**Smoke tests** are broad and shallow — they cover many areas of the application but only verify basic functionality in each area. They answer the question: "Does the build have any fundamental problems?"

**Sanity tests** are narrow and deep — they focus on specific areas of the application and verify that particular functionality works correctly after a change in that area. They answer the question: "Does this specific thing work correctly?"

A useful analogy: smoke testing is like checking that a car's engine turns on, the wheels turn, the brakes work, and the lights illuminate. Sanity testing is like taking the car for a drive and verifying that the steering is precise and the brakes stop the car within expected distances.

### Regression Detection

Smoke tests serve as an early warning system for regressions. When a new build introduces a regression in a critical path function, smoke tests catch it immediately rather than allowing the regression to persist through longer-running test suites. This is especially valuable in large codebases where a change in one module could have unexpected effects on other modules.

Smoke tests are typically kept small and fast intentionally — adding too many tests to the smoke test suite defeats the purpose. If smoke tests take an hour to run, developers will bypass them or ignore failures. The discipline is to keep smoke tests focused only on the truly critical path.

## How It Works

### Automated Smoke Test Suites

Smoke tests are almost always automated because their value depends on being fast and repeatable. Manual smoke testing is too slow and inconsistent for any but the most trivial applications. Automated smoke test suites can be run within minutes of a build being produced, providing rapid feedback.

Smoke test automation frameworks vary by technology stack. Common choices include Selenium for browser-based applications, REST Assured or Postman for API testing, and language-specific testing frameworks for unit and integration testing layers.

```python
# Example: Python smoke test suite using pytest and requests
import pytest
import requests

BASE_URL = "https://api.example.com"

class TestSmokeTestSuite:
    """Critical path smoke tests that must pass before further testing."""

    def test_health_endpoint_returns_200(self):
        """Verify the API server is running and responding."""
        response = requests.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_user_can_login(self):
        """Verify authentication flow works."""
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": "test@example.com", "password": "TestPassword123!"}
        )
        assert response.status_code == 200
        assert "token" in response.json()
        assert len(response.json()["token"]) > 0

    def test_core_api_endpoint_accessible(self):
        """Verify the main API resource is accessible."""
        response = requests.get(f"{BASE_URL}/api/v1/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_api_handles_invalid_requests_gracefully(self):
        """Verify the API returns proper error responses for bad input."""
        response = requests.get(f"{BASE_URL}/api/v1/products/invalid-id")
        assert response.status_code == 404
        assert "error" in response.json()

    def test_database_connection_from_api(self):
        """Verify the API can communicate with the database."""
        response = requests.get(f"{BASE_URL}/api/v1/users/1")
        # Should return 200 if user exists, 404 if not
        # Either way, we got a response, not a 500 (database error)
        assert response.status_code in [200, 404]
```

### Integration with CI/CD Pipelines

Smoke tests are typically configured as the first test stage in a CI/CD pipeline. The pipeline flow is: Build → Smoke Tests → Integration Tests → System Tests → Deployment. If smoke tests fail at any stage, the pipeline stops and subsequent stages are not executed.

```yaml
# Example: GitHub Actions pipeline with smoke test gate
name: Build and Test Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build application
        run: npm ci && npm run build
      - name: Run unit tests
        run: npm test -- --coverage

  smoke-tests:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to test environment
        run: |
          kubectl apply -f k8s/test/
          kubectl rollout status deployment/app --timeout=3m

      - name: Run smoke tests
        run: |
          npm run test:smoke -- --reporter=json
        env:
          API_BASE_URL: https://test.example.com

      - name: Publish smoke test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: smoke-test-results
          path: test-results/smoke-tests.json

  integration-tests:
    needs: smoke-tests
    runs-on: ubuntu-latest
    steps:
      - name: Run integration tests
        run: npm run test:integration
```

### Manual Smoke Testing

For some applications, particularly those with significant user interface complexity or domain-specific business logic, manual smoke testing can supplement automated checks. A manual smoke test involves a tester spending 10-15 minutes executing critical path scenarios by hand, observing the application for unexpected behavior, crashes, or errors.

Manual smoke testing is typically documented using a checklist:

- [ ] Application starts without errors
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials shows appropriate error
- [ ] Main dashboard or landing page loads correctly
- [ ] Core feature (add/edit/delete) works
- [ ] Logout clears session
- [ ] Application handles network disconnection gracefully

## Practical Applications

### Web Application Smoke Testing

For a typical web application, smoke tests verify:
- Homepage loads without errors
- User registration and login flow works
- Logged-in user can access their dashboard
- Core feature (e-commerce purchase, social post, data entry form) works end-to-end
- Logout terminates the session

### API Smoke Testing

For an API service, smoke tests verify:
- Health endpoint responds with healthy status
- API responds to requests with valid authentication
- API rejects requests without authentication (or with invalid credentials)
- Core endpoints return expected data structures
- API handles error cases with appropriate status codes and error messages

### Microservices Smoke Testing

In a microservice architecture, smoke tests verify:
- All services start successfully
- Service-to-service communication works
- API gateway routes requests correctly
- Database connections are established
- Message queue consumers process messages

## Examples

A practical smoke test for an e-commerce application might include:

```gherkin
Feature: E-commerce smoke tests
  Critical path tests for build verification

  Scenario: User can browse products
    Given the user is on the homepage
    When they navigate to the products page
    Then they should see a list of products

  Scenario: User can add product to cart
    Given the user is on the products page
    When they click "Add to Cart" on the first product
    Then the cart count should increase by 1

  Scenario: User can complete checkout flow
    Given the user has items in the cart
    When they proceed to checkout
    And they complete the payment form with test card details
    Then they should see an order confirmation

  Scenario: User login persists across pages
    Given the user is logged in
    When they navigate to the account page
    Then they should still be logged in
```

## Related Concepts

- [[regression-testing]] — Full test suites run to catch regressions; smoke tests are a subset
- [[sanity-testing]] — Narrow testing of specific functionality; complementary to smoke tests
- [[continuous-integration]] — CI pipelines often gate on smoke test results
- [[continuous-deployment]] — CD pipelines use smoke tests as quality gates before deployment
- [[automated-testing]] — Smoke tests are a form of automated testing
- [[unit-testing]] — Unit tests may feed into smoke test suites
- [[integration-testing]] — Integration tests run after smoke tests pass
- [[CI-pipeline]] — The pipeline structure that incorporates smoke test gates

## Further Reading

- \"Agile Testing\" by Lisa Crispin and Janet Gregory — Testing quadrants and where smoke tests fit
- Sauce Labs Smoke Testing Best Practices — Industry guidance on smoke test design
- Google Testing Blog: Just Say No to More End-to-End Tests — Argument for smoke tests over exhaustive end-to-end suites
- Cypress End-to-End Testing — Modern tooling for browser smoke test automation

## Personal Notes

The discipline in smoke testing is knowing what NOT to test. It is tempting to add "just one more" critical check to the smoke suite, but every test added to smoke tests is a test that must run on every single build. If your smoke suite takes 30 minutes to run, developers will stop trusting it. I prefer a strict 5-10 minute maximum for smoke test execution — if it cannot be validated in that window, it belongs in a higher test stage. The goal is to catch fundamental "is this build worth testing further?" questions, not to validate every feature. Save comprehensive validation for the regression suite that runs less frequently but covers more ground.
