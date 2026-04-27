---
title: "Behavior Driven Development"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [bdd, testing, agile, specification, gherkin, acceptance-testing, communication]
---

# Behavior Driven Development

## Overview

Behavior Driven Development (BDD) is an agile software development methodology that extends Test Driven Development by emphasizing collaboration between technical and non-technical stakeholders. While TDD focuses on writing tests for code behavior, BDD focuses on writing examples of system behavior in a language that everyone can understand — business users, product managers, developers, and QA engineers. The examples are written in a structured format called Gherkin, which uses keywords like Given, When, Then to describe scenarios in plain English.

BDD emerged from the recognition that a major failure mode of traditional TDD was communication breakdown between domain experts and development teams. Tests written by developers for developers often didn't capture the actual business behavior that mattered. BDD addresses this by making the examples — not just the tests — a first-class artifact of the development process. The examples become executable specifications, living documentation, and automated tests simultaneously.

The process was pioneered by Dan North in the early 2000s as a response to challenges he observed when introducing TDD to teams. He noticed that teams struggled with knowing where to start, what to test, and what to call tests. BDD introduced the concept of user stories with clear acceptance criteria written in a shared vocabulary. This vocabulary, or "ubiquitous language," reduces misunderstandings and ensures that the entire team agrees on what the software should do before implementation begins.

## Key Concepts

### The Ubiquitous Language

BDD establishes a shared vocabulary that spans the boundary between business language and technical language. Domain terms are defined consistently and used by everyone — product managers, developers, testers, and business stakeholders. This shared language reduces translation losses when communicating requirements and ensures that the resulting software accurately reflects business intent.

The ubiquitous language is captured in the glossary of the domain — terms like "Order," "Customer," "Inventory Level," or "Eligibility Criteria" are defined precisely so that when a product manager says "eligible," developers know exactly what conditions must be met. This precision flows directly into the Gherkin scenarios, where the same terms appear consistently.

### User Stories with Acceptance Criteria

BDD is structured around user stories that follow a specific template:

**As a** [role], **I want** [feature], **so that** [benefit].

Each user story includes acceptance criteria written as scenarios in Gherkin format. The acceptance criteria are concrete examples that illustrate what "done" means for that story. A story is not complete when the code is written — it is complete when all its acceptance criteria scenarios pass.

For example:

```
As a customer,
I want to apply a coupon code to my order,
so that I can receive a discount on qualifying purchases.
```

Acceptance criteria scenarios for this story might include:
- A valid coupon code reduces the order total by the correct percentage
- An expired coupon code displays an appropriate error message
- A coupon code with a minimum purchase requirement is rejected when the threshold is not met

### The Three Amigos Meeting

BDD emphasizes collaboration through the "Three Amigos" meeting — a regular sync between a developer, a tester, and a business analyst or product manager. The purpose is to discuss user stories and define acceptance criteria collaboratively before implementation begins. Each "amigo" brings a different perspective: the business analyst ensures the story delivers real value, the developer identifies technical constraints and edge cases, and the tester identifies failure scenarios and quality concerns.

This meeting produces concrete Gherkin scenarios that become the acceptance tests. The conversation is as valuable as the output — misunderstandings are caught early, assumptions are challenged, and the team builds shared ownership of quality.

## How It Works

### Gherkin Syntax

Gherkin is the language used to write BDD scenarios. It uses a small set of keywords to structure scenarios:

**Feature** — A high-level description of a software feature, grouping related scenarios.

**Scenario** — A concrete example of expected behavior.

**Given** — The preconditions and context before an action occurs.

**When** — The action or event being performed.

**Then** — The expected outcome.

**And / But** — Used to extend Given, When, Then steps for readability.

**Background** — Shared steps that run before each scenario in a feature file.

```gherkin
Feature: Online checkout
  As a customer
  I want to apply coupon codes to my order
  So that I can receive discounts on qualifying purchases

  Background:
    Given the following products exist:
      | name       | price |
      | Widget     | 29.99 |
      | Gadget     | 49.99 |
    And a customer "alice@example.com" is logged in

  Scenario: Valid coupon applies percentage discount
    Given the customer's cart contains:
      | product | quantity |
      | Widget  | 2        |
    When she applies coupon code "SAVE20"
    Then the order total should be $47.98
    And she should see "Coupon applied: 20% off"

  Scenario: Expired coupon is rejected
    Given coupon code "EXPIRED10" expired on "2024-01-01"
    When she applies coupon code "EXPIRED10"
    Then she should see error "This coupon has expired"
    And the order total should remain $59.98

  Scenario: Coupon with minimum purchase threshold is rejected
    Given coupon code "MIN50" requires minimum purchase of $50.00
    When she applies coupon code "MIN50" to a $29.99 order
    Then she should see error "Minimum purchase of $50.00 required"
```

### Step Definitions

Gherkin scenarios are not executable by themselves — they must be connected to code through step definitions. Step definitions are code snippets that map each Gherkin step to actual automation. In JavaScript, a step definition might look like:

```javascript
const { Given, When, Then } = require('@cucumber/cucumber');

Given('the customer {string} is logged in', async function (email) {
  await this.api.auth.login(email);
});

When('she applies coupon code {string}', async function (code) {
  const response = await this.api.cart.applyCoupon(code);
  this.lastResponse = response;
});

Then('she should see error {string}', async function (expectedError) {
  const actualError = this.lastResponse.error;
  if (!actualError.includes(expectedError)) {
    throw new Error(`Expected error "${expectedError}", got "${actualError}"`);
  }
});
```

The step definitions interact with the actual application through APIs, browser automation, or other testing interfaces. This allows the same Gherkin scenarios to drive different levels of testing — from unit tests to full end-to-end tests.

### The BDD Lifecycle

BDD follows a discover, formulate, automate, verify cycle:

1. **Discover**: The team (especially product manager and developer) discuss a user story and identify the key behaviors and acceptance criteria. What should the system do? What are the edge cases? What does "done" look like?

2. **Formulate**: The acceptance criteria are written as Gherkin scenarios in a shared document. These scenarios are reviewed by the Three Amigos to ensure they capture the expected behavior correctly.

3. **Automate**: Developers or QA engineers write step definitions that connect the Gherkin steps to automation code. The scenarios can now be run against the application.

4. **Verify**: The scenarios are executed. When they all pass, the story is considered complete. When a scenario fails, it indicates a gap between the implementation and the agreed behavior.

This cycle repeats for every user story, producing a growing suite of executable specifications that document the system's behavior.

## Practical Applications

BDD is most valuable in domains where business logic is complex and communication between technical and non-technical team members is critical. Financial applications, e-commerce platforms, healthcare systems, and regulatory compliance software benefit significantly from BDD because the scenarios capture not just what the code does but why it does it — the business rules and constraints that must be enforced.

BDD scenarios also serve as regression tests. When a new feature is added or an existing feature is modified, the scenarios ensure that existing behavior continues to work as specified. This is particularly valuable in large codebases where a change in one area could unintentionally break behavior in another.

## Examples

Consider a ride-sharing application implementing surge pricing. A BDD scenario would capture the business rule precisely:

```gherkin
Feature: Surge pricing
  In order to balance driver supply with rider demand
  As the platform
  I want to apply surge multipliers during high-demand periods

  Scenario: Surge pricing activates when driver availability is low
    Given 10 riders are waiting for rides in downtown
    And only 3 drivers are available
    When a rider requests a ride
    Then the fare should include a 1.5x surge multiplier
    And the rider should see "Surge pricing is active in your area"

  Scenario: Surge pricing does not activate during normal demand
    Given 5 riders are waiting for rides in downtown
    And 20 drivers are available
    When a rider requests a ride
    Then the fare should be at base rate with no surge
```

This scenario captures not just the happy path but the business logic that drives pricing decisions. A developer implementing this feature can reference the scenarios to understand exactly what behavior is expected, and the scenarios serve as automated tests that verify the implementation is correct.

## Related Concepts

- [[test-driven-development]] — BDD extends TDD practices with a focus on shared language
- [[acceptance-testing]] — BDD scenarios are a form of acceptance testing
- [[gherkin]] — The specification language used to write BDD scenarios
- [[agile-development]] — BDD is an agile methodology emphasizing collaboration
- [[domain-driven-design]] — Shares the concept of a ubiquitous language with BDD
- [[automated-testing]] — BDD scenarios are automated through step definitions
- [[cucumber]] — A popular BDD tool for writing and running Gherkin scenarios

## Further Reading

- \"Behavior-Driven Development\" by Addison Wesley — Comprehensive BDD methodology guide
- Cucumber Documentation — Practical guide to Gherkin and BDD tooling
- \"Specification by Example\" by Gojko Adzic — How teams use BDD-style examples
- The Cucumber Book — Hands-on guide to behavior-driven development

## Personal Notes

The greatest value of BDD is not the automated tests — it's the conversations that happen when writing the scenarios. I've seen teams discover gaps in requirements, contradictory assumptions, and missing edge cases during the Three Amigos meeting, before a single line of code is written. The Gherkin scenarios are a byproduct of those conversations. That said, BDD adds overhead that is not always justified — for simple CRUD applications with minimal business logic, the overhead of maintaining Gherkin feature files may not be worth the benefit. BDD shines brightest on complex domain logic where the business rules are nuanced and the cost of misunderstanding is high.
