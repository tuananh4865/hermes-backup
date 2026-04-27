---
title: "Integration Testing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [testing, software-engineering, quality, test-pyramid]
---

# Integration Testing

## Overview

Integration testing verifies that different modules or services of an application work correctly together. It sits between [[unit-testing]] (which tests individual components in isolation) and [[end-to-end-testing]] (which tests the complete application flow). Integration tests catch issues that unit tests miss—problems arising from component interactions, API contracts, database integration, message queue communication, and external service dependencies.

The key characteristic of integration testing is that components are combined and tested as a group, exercising the real interfaces between them rather than mocked substitutes. This provides higher confidence than unit tests that the system works as a whole, while remaining more manageable than full E2E tests.

## Key Concepts

**Test Scope**: Integration tests exercise multiple components but may use test doubles for truly external systems (other microservices, third-party APIs). The exact boundary depends on what you're trying to verify.

**Database Integration**: Testing with a real database (often an in-memory or containerized instance) rather than mocks. This catches issues like:
- Incorrect SQL queries that work with mocks but fail on real data
- Transaction handling and rollback behavior
- Constraint violations and data integrity
- Query performance issues

**API Contract Testing**: Verifying that service interfaces match expectations. Tools like Pact enable consumer-driven contract testing, where the client specifies what it expects from the server.

**Message Queue Integration**: Testing that producers and consumers work correctly together, messages are properly serialized/deserialized, and error handling for failed messages works as expected.

**Test Databases**: Common approaches:
- In-memory databases (SQLite, H2) for fast, isolated tests
- Docker containers spun up per test suite
- Shared test database reset between test runs
- Database per tenant/namespace for parallel execution

## How It Works

Integration tests typically follow a setup-execute-verify pattern:

```python
# Example: Testing repository integration with database
import pytest
from myapp.database import Session, UserRepository
from myapp.models import User

@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    session = Session()
    yield session
    session.rollback()  # Clean up: rollback, don't commit
    session.close()

@pytest.fixture
def user_repo(db_session):
    """Repository instance using test database."""
    return UserRepository(db_session)

def test_create_and_retrieve_user(db_session, user_repo):
    """Integration test: create user, verify it's persisted correctly."""
    # Setup
    new_user = User(name="Alice", email="alice@example.com")
    
    # Execute - repository calls real database
    created_user = user_repo.create(new_user)
    
    # Verify - query the actual database
    retrieved = user_repo.get_by_id(created_user.id)
    
    assert retrieved.name == "Alice"
    assert retrieved.email == "alice@example.com"
    assert retrieved.created_at is not None
```

## Practical Applications

**Service Layer Tests**: Test business logic that spans multiple repositories or external services without going through the HTTP layer:

```python
def test_transfer_funds_between_accounts(account_repo, transaction_repo):
    """Test that transfers correctly update both accounts atomically."""
    # Setup accounts with starting balances
    source = account_repo.create(Account(balance=1000))
    destination = account_repo.create(Account(balance=500))
    
    # Execute transfer (uses both repos internally)
    transfer_service.transfer(source.id, destination.id, amount=100)
    
    # Verify: real database state changed
    db_session.expire_all()  # Clear cached state
    assert account_repo.get_by_id(source.id).balance == 900
    assert account_repo.get_by_id(destination.id).balance == 600
    
    # Verify transaction was recorded
    transactions = transaction_repo.list_by_account(source.id)
    assert len(transactions) == 1
    assert transactions[0].amount == -100
```

**HTTP API Tests**: Using test clients to exercise complete request handling:

```python
from fastapi.testclient import TestClient

def test_create_product(api_client: TestClient):
    """Integration test: full HTTP request handling."""
    response = api_client.post("/products", json={
        "name": "Widget",
        "price": 19.99,
        "category_id": 1
    })
    
    assert response.status_code == 201
    product = response.json()
    assert product["name"] == "Widget"
    assert product["id"] is not None
    
    # Verify persisted: GET the same resource
    get_response = api_client.get(f"/products/{product['id']}")
    assert get_response.json() == product
```

## Related Concepts

- [[Unit Testing]] - Testing individual components in isolation
- [[End-to-End Testing]] - Testing complete user flows
- [[Test-Driven Development]] - Writing tests before implementation
- [[Mocking]] - Replacing dependencies with test doubles
- [[Test Pyramid]] - Strategy for balancing test types
- [[ci-cd-pipelines]] - Automating test execution

## Further Reading

- [Martin Fowler on Integration Testing](https://martinfowler.com/articles/microservices-testing/) - Comprehensive testing guide for distributed systems
- [Testing in the Test Pyramid](https://automationpanda.com/2017/03/15/the-testing-pyramid/) - Balancing different test types
- [Pytest Documentation](https://docs.pytest.org/) - Python testing framework

## Personal Notes

Integration tests catch bugs that unit tests simply cannot. I once spent days debugging an issue where our code worked with SQLite (used in unit tests) but failed with PostgreSQL due to datetime handling differences. The fix was simple, but we never would have caught it without integration tests against the real database.

The tradeoff is speed: integration tests are typically slower than unit tests because they involve real I/O. The test pyramid is the right model—many fast unit tests at the base, fewer slower integration tests in the middle, and very few slow E2E tests at the top.

I recommend separating integration tests from unit tests physically (different directories, different test configuration) so they can be run independently. CI pipelines should run unit tests on every commit, but integration tests might run less frequently or in parallel to keep feedback loops fast.
