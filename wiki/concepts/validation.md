---
title: "Validation"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [validation, security, data-quality]
---

# Validation

## Overview

Validation is the process of checking whether data meets specified criteria before it is processed, stored, or used by an application. It ensures that input data is correct, complete, and safe to use. Validation is a critical component of [[data-quality]] and [[web-security]], preventing malformed data from causing crashes, corruption, or security vulnerabilities.

Validation occurs at multiple layers: client-side validation provides immediate user feedback, while server-side validation serves as the authoritative check since client-side checks can be bypassed. The principle of "never trust client input" drives the common practice of validating all data server-side, even when client-side validation exists for usability.

Effective validation reduces bugs, protects against [[injection-attacks]], ensures [[data-integrity]], and improves application reliability. It is foundational to [[form-validation]], [[api-design]], and secure [[input-sanitization]].

## Types

**Schema Validation** enforces the structure and format of data. It checks that required fields exist, data types are correct, string patterns match expected formats (such as email addresses or phone numbers), and numeric values fall within acceptable ranges. JSON Schema and XML Schema are common standards for defining structural rules.

**Type Validation** ensures data conforms to expected programming data types. This includes checking whether a value is an integer versus a float, whether a string represents a valid date, or whether a collection contains the expected element types. Type validation catches mismatches early in the execution pipeline.

**Business Logic Validation** applies domain-specific rules that go beyond format and type. Examples include checking that a withdrawal amount does not exceed an account balance, that a booking date is in the future, or that a username is not already taken. These rules encode the policies and constraints of the specific application domain.

**Range and Constraint Validation** verifies that values fall within acceptable boundaries. Minimum and maximum lengths for strings, lower and upper bounds for numbers, and enumerated lists of permitted values all fall into this category.

**Cross-Field Validation** validates relationships between different fields. For instance, a form with "start date" and "end date" fields must have the end date after the start date. This type of validation often requires custom logic beyond declarative schema rules.

## Libraries

**JavaScript/TypeScript**: Joi provides powerful schema-based validation. Zod offers type-safe validation with TypeScript integration. Yup focuses on parse-and-test validation with a readable API. Express-validator middleware integrates validation into Express routes.

**Python**: Pydantic leverages type hints for validation in data models. Cerberus provides lightweight rule-based validation. Marshmallow serializes and validates complex data structures.

**Java**: Hibernate Validator implements Bean Validation (JSR-380). Jakarta Validation is the standard specification for Java EE/Jakarta EE applications.

**Go**: go-playground/validator uses struct tags for validation rules. GOVAL offers declarative validation. Vali provides comprehensive rule sets with customizable error messages.

**Ruby**: ActiveModel::Validations is built into Rails. Dry-schema defines validation schemas. Reform separates validation from model logic.

**PHP**: Laravel's Validator provides expressive validation rules. Symfony Validator follows JSR-303/JSR-380 bean validation standards. Respect\Validation offers a fluent, chainable API.

## Related

- [[input-sanitization]]
- [[form-validation]]
- [[data-quality]]
- [[data-integrity]]
- [[web-security]]
- [[api-design]]
- [[schema]]
- [[error-handling]]
- [[type-safety]]
- [[injection-attacks]]
