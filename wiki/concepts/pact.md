---
title: "Pact"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [contract-testing, microservices, testing, api]
---

# Pact

## Overview

Pact is a consumer-driven contract testing framework that enables teams to verify API compatibility between services without the need for integration environments or end-to-end tests. Originally developed at Sighten (later Uber), Pact has become a widely adopted standard for testing microservices integrations, particularly in environments where services evolve independently and need confidence that changes won't break their consumers.

Unlike traditional contract testing approaches where contracts are defined by the provider, Pact follows a consumer-driven contract pattern. The consumer of an API defines what it expects from the provider, and those expectations become the contract that the provider must satisfy. This shift in responsibility ensures that the API is designed from the consumer's perspective, leading to more usable and stable APIs.

## Key Concepts

**Consumer-Driven Contracts** is the foundational principle of Pact. Rather than having providers dictate their API structure, consumers specify exactly what data they need and what request formats they will send. This approach prevents provider APIs from including unnecessary fields that no consumer uses, reduces coupling, and gives consumer teams autonomy over their data requirements.

**Pact Files** are the artifacts generated when consumer tests run. These JSON files contain the expected interactions between a consumer and provider, including request method, path, headers, body patterns, and expected response structures. The Pact file serves as a portable contract that can be shared with providers for verification.

**Broker** is a central repository for Pact files that enables provider teams to automatically verify their implementations against all existing consumer contracts. The Pact Broker also tracks deployment history and can determine whether it's safe to deploy a service based on the contract verification status of all dependent services.

## How It Works

The Pact testing workflow follows a specific sequence designed to catch compatibility issues early. When a consumer team writes tests using the Pact framework, they define their expectations for API responses using matchers that describe patterns rather than exact values. This approach allows tests to remain stable even when unrelated fields change in the provider's response.

When consumer tests run, Pact records the interactions and generates a Pact file. This file is then published to a Pact Broker, where it becomes available to provider teams. When a provider wants to verify compatibility, they pull the relevant Pact files from the broker and run verification tests that check whether their actual implementation matches the consumer's expectations.

The verification process involves replaying each interaction from the consumer's perspective against the provider's actual implementation. If any interaction fails, the provider knows that their changes have broken a consumer's expectations, and they must either adapt their changes to maintain compatibility or coordinate with the consumer team to update their contract.

```ruby
# Example Pact consumer test (Ruby)
describe "GET /users/:id" do
  context "when the user exists" do
    it "returns the user with required fields" do
      provider_state "a user with id 123 exists"
      
      interaction {
        given "a user with id 123 exists"
        with_request {
          method :get
          path "/users/123"
          headers { Accept: "application/json" }
        }
        will_respond_with {
          status 200
          headers { Content-Type: "application/json" }
          body {
            id: 123,
            name: match(type: String),
            email: match(email_regex)
          }
        }
      }
    end
  end
end
```

## Practical Applications

Pact is particularly valuable in microservices architectures where teams deploy services independently. By using consumer-driven contracts, teams can achieve confidence that new service versions won't break existing consumers without requiring expensive integration environments or complex end-to-end test suites.

The framework excels in continuous integration pipelines where it can run quickly and provide fast feedback. Consumer tests run against mocked provider responses, making them fast and reliable. Provider verification can be triggered automatically when Pact files are updated, ensuring that any breaking change is caught before deployment.

## Examples

A typical Pact implementation might involve an e-commerce platform where the Order Service is a consumer of the User Service. The Order Service team writes Pact tests that define exactly what user data they need: user ID, name, and shipping address. When the User Service team makes changes to their API, they run verification against the Order Service's Pact file, ensuring they don't accidentally remove or restructure fields that the Order Service depends on.

Another common pattern is using Pact with CI/CD pipelines where provider verification runs automatically when new Pact files are published, and deployment is blocked if any verification fails.

## Related Concepts

- [[Contract Testing]] - General concept of testing API compatibility
- [[Microservices]] - Architecture pattern where Pact is commonly used
- [[API Gateway]] - Often sits between consumers and providers
- [[End-to-End Testing]] - Traditional approach contrasted with contract testing
- [[Service Level Agreements]] - Related to API reliability guarantees

## Further Reading

- [Pact Official Documentation](https://docs.pact.io/)
- [Pact Broker](https://docs.pact.io/pact_broker)
- [Consumer-Driven Contracts by Martin Fowler](https://martinfowler.com/articles/consumerDrivenContracts.html)

## Personal Notes

Pact represents an important shift in how teams think about API compatibility. Rather than relying on documentation or ad-hoc communication, it creates a machine-readable, version-controlled contract that both consumer and provider teams can work against. The initial setup requires some investment, but the long-term benefits of faster feedback and reduced integration issues are substantial. Consider starting with a single critical consumer-provider pair to validate the approach before rolling out organization-wide.
