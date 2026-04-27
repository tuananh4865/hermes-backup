---
title: "Unit Testing"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [testing, software-engineering, quality, tdd, test-pyramid]
---

# Unit Testing

## Overview

Unit testing is a software testing methodology where individual components are tested in isolation from the rest of the system. A unit is the smallest testable piece of code—typically a function, method, or class. Unit tests verify that each unit produces the expected output given specific inputs, catching bugs early in development before they compound into larger issues.

The defining characteristic of a unit test is isolation: the unit under test should not depend on real databases, file systems, network services, or other modules. These dependencies are replaced with test doubles (mocks, stubs, fakes) that simulate the behavior of real components without side effects or external calls.

## Key Concepts

**Test Doubles** replace real dependencies with controlled substitutes:
- **Mock**: Asserts that specific methods were called with specific arguments
- **Stub**: Provides predetermined responses to calls
- **Fake**: Has working implementation but simplified for testing (e.g., in-memory database)
- **Spy**: Records information about calls for later verification

```python
from unittest.mock import Mock, MagicMock

# Mock: verifies interaction occurred
def test_user_notifier_sends_email():
    mock_email_service = Mock()
    notifier = UserNotifier(mock_email_service)
    
    notifier.notify_user("user@example.com", "Hello!")
    
    mock_email_service.send.assert_called_once_with(
        to="user@example.com",
        subject="Hello!",
        body="Hello!"
    )

# Stub: provides canned responses
def test_order_processor_with_insufficient_inventory():
    mock_inventory = Mock()
    mock_inventory.check_stock.return_value = 0  # Stub response
    
    processor = OrderProcessor(inventory=mock_inventory)
    result = processor.process(Order(product_id="SKU123", quantity=10))
    
    assert result.success is False
    assert result.error == "Insufficient inventory"
```

**Arrange-Act-Assert (AAA)** is the standard pattern for structuring tests:

```python
def test_calculate_discount():
    # Arrange: set up test data and dependencies
    order = Order(subtotal=100.00, customer_tier="gold")
    pricing_service = PricingService()
    
    # Act: execute the behavior being tested
    discount = pricing_service.calculate_discount(order)
    
    # Assert: verify the expected outcome
    assert discount == 0.15  # Gold tier gets 15% off
```

**Given-When-Then** is an equivalent BDD-style notation:

```python
def test_calculator_divides_two_numbers():
    # Given
    calc = Calculator()
    
    # When
    result = calc.divide(10, 2)
    
    # Then
    assert result == 5
```

## How It Works

Unit tests run against code modules without external dependencies:

1. **Setup**: Create test fixtures, instantiate the unit under test with mocked dependencies
2. **Execute**: Call the method or function being tested
3. **Assert**: Verify the return value, state changes, or interactions
4. **Teardown**: Clean up any resources (though with mocks, this is usually minimal)

```python
# Complete example demonstrating isolation principle
class TestOrderValidator:
    """Unit tests for OrderValidator - no real database calls."""
    
    def test_validates_email_format(self):
        # Arrange
        validator = OrderValidator()  # No external dependencies
        
        # Act & Assert
        assert validator.is_valid_email("user@example.com") is True
        assert validator.is_valid_email("invalid-email") is False
    
    def test_validates_phone_number(self):
        validator = OrderValidator()
        
        assert validator.is_valid_phone("+1-555-123-4567") is True
        assert validator.is_valid_phone("123") is False
    
    def test_order_total_exceeds_minimum(self):
        validator = OrderValidator()
        
        assert validator.is_valid_total(50.00, minimum=10.00) is True
        assert validator.is_valid_total(5.00, minimum=10.00) is False
```

## Practical Applications

**Test-Driven Development (TDD)**: Write tests before implementation:

```python
# Red: Write failing test first
def test_adds_two_numbers():
    assert add(2, 3) == 5  # Fails: add() doesn't exist yet

# Green: Write minimal implementation
def add(a, b):
    return a + b

# Refactor: Clean up code while keeping tests passing
```

**Testing Edge Cases**: Unit tests excel at verifying boundary conditions:

```python
def test_array_slice_returns_correct_subarray():
    arr = [1, 2, 3, 4, 5]
    
    assert arr[1:3] == [2, 3]
    assert arr[0:1] == [1]  # Edge: single element
    assert arr[4:5] == [5]  # Edge: last element
    assert arr[0:0] == []   # Edge: empty slice
    assert arr[5:10] == []  # Edge: out of bounds returns empty
```

**Testing Error Handling**:

```python
def test_raises_exception_for_invalid_input():
    validator = OrderValidator()
    
    with pytest.raises(ValidationError) as exc_info:
        validator.validate(None)
    
    assert "Order cannot be None" in str(exc_info.value)
```

## Related Concepts

- [[Integration Testing]] - Testing component interactions
- [[End-to-End Testing]] - Testing complete user flows
- [[Test-Driven Development]] - Writing tests before code
- [[Test Pyramid]] - Balancing test types by scope and speed
- [[Mocking]] - Creating test doubles for dependencies
- [[Assertion]] - Verifying expected behavior

## Further Reading

- [xUnit Test Patterns](https://books.google.com/books/about/xUnit_Test_Patterns.html) - Comprehensive guide to test patterns
- [Clean Code: Functions](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882) - Writing testable code
- [pytest Documentation](https://docs.pytest.org/) - Python testing framework

## Personal Notes

Unit tests give you the fastest feedback loop. When I'm fixing a bug, I first write a unit test that reproduces it, then fix the code. This ensures the bug doesn't regress and documents the expected behavior.

The key insight is that tests should be first-class citizens, not an afterthought. If a function is hard to unit test, it's often a sign of poor design—too many dependencies, too much state, or doing too many things. Making code testable often makes it better designed overall.

I aim for tests that are:
- **Fast**: Thousands of tests run in seconds
- **Independent**: No test depends on another completing first
- **Repeatable**: Same result every time, no flaky behavior
- **Self-verifying**: Clear pass/fail, no manual inspection needed
- **Timely**: Written before or alongside the code they test
