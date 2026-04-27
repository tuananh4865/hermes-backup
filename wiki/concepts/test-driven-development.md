---
title: "Test Driven Development"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [tdd, testing, software-development, quality, refactoring, unit-testing]
---

# Test Driven Development

Test Driven Development (TDD) is a software development methodology where tests are written before the code they validate. The developer follows a short repetitive cycle: write a failing test (Red), write minimal code to pass the test (Green), then refactor the code while keeping tests passing (Refactor). This approach, popularized by Kent Beck and the Extreme Programming movement, produces well-tested, maintainable code with a bias toward simplicity.

## The TDD Cycle

### Red — Write a Failing Test

Before writing any implementation code, write a test that describes the desired behavior. The test must fail initially because the feature doesn't exist yet. This test serves as a specification for what the code should do.

```javascript
// Example in JavaScript (Jest)
describe('Calculator', () => {
  it('should add two positive numbers', () => {
    const calc = new Calculator();
    expect(calc.add(2, 3)).toBe(5); // This fails - Calculator doesn't exist
  });
});
```

### Green — Write Minimal Code to Pass

Write only enough code to make the failing test pass. Don't anticipate future requirements or add unnecessary functionality. The goal is to get to green as quickly as possible.

```javascript
class Calculator {
  add(a, b) {
    return a + b;
  }
}
```

### Refactor — Improve Code Structure

With tests passing, now improve the code's internal structure. Extract duplicated logic, rename variables for clarity, break complex functions into smaller pieces. Tests ensure refactoring doesn't break behavior.

```javascript
// Refactored with additional operations, still passing all tests
class Calculator {
  add(a, b) {
    return a + b;
  }
  
  subtract(a, b) {
    return a - b;
  }
  
  multiply(a, b) {
    return a * b;
  }
}
```

## Key Concepts

**Baby Steps** — Keep iterations small. Write one failing test, make it pass, repeat. Small steps prevent over-engineering and make debugging easier.

**Triangulation** — Add new test cases with different inputs to verify behavior, not to "prove" the implementation works. Write tests that fail edge cases specifically.

**Test Isolation** — Each test should be independent, able to run in any order. Shared state between tests causes flaky, unpredictable failures.

**Behavior over Implementation** — Test what the code does, not how it does it. Implementation details change; behavior should remain stable.

## Benefits of TDD

- **Regression Prevention** — Immediate feedback when changes break existing functionality
- **Design Clarity** — Writing tests first forces thinking about interfaces before implementation
- **Living Documentation** — Tests document expected behavior; passing tests prove code works
- **Reduced Debugging Time** — Bugs are caught immediately rather than discovered later
- **Confidence for Refactoring** — Strong test coverage enables aggressive optimization and restructuring

## Limitations and Criticisms

- **Productivity Perception** — Initial development appears slower; benefits accumulate over time
- **Test Maintenance Overhead** — Changing requirements means rewriting tests
- **Not Suited for All Domains** — Exploratory work and prototypes benefit less from TDD
- **Integration Testing Gap** — Unit tests alone don't verify system-level behavior

## Practical Applications

TDD works well with [[unit-testing]] frameworks (Jest, pytest, JUnit). Many teams practice "TDD-lite" — writing tests for core business logic while using manual testing for UI and exploratory work.

In [[CI-pipeline]] workflows, tests run automatically on every commit, preventing broken code from reaching production.

## Related Concepts

- [[unit-testing]] — Individual component testing
- [[test-coverage]] — Measuring how much code is tested
- [[regression-testing]] — Ensuring existing features still work
- [[automated-testing]] — General test automation
- [[software-testing]] — Testing methodology overview

## Further Reading

- Test Driven Development: By Example by Kent Beck
- Clean Code by Robert C. Martin (chapters on testing)
- xUnit Test Patterns by Gerard Meszaros

## Personal Notes

The hardest part of TDD is fighting the urge to "just write the feature first." When I actually follow the cycle—write a failing test, make it pass, refactor—the resulting code is almost always cleaner. The tests become invaluable when I return to code months later.
