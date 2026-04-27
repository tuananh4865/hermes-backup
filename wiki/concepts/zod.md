---
title: Zod
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [zod, typescript, validation, schema]
---

# Zod

## Overview

Zod is a TypeScript-first schema declaration and validation library that enables developers to define schemas for data structures and automatically infer their TypeScript types. Created by Colin McDonnell and released in 2019, Zod has become a cornerstone of type-safe development in the TypeScript ecosystem. Unlike traditional validation libraries that require separate type definitions, Zod schemas serve dual purposes: they validate data at runtime and generate TypeScript types at compile time. This bidirectional coherence ensures that schema and type definitions never drift apart, eliminating runtime type errors.

Zod operates on a simple principle: define a schema once, and Zod handles validation, type inference, and transformation. The library runs in Node.js, Deno, Bun, and browsers, integrating seamlessly with React, Next.js, and tRPC.

## Key Features

### Schema Definition

Zod provides validators for all JavaScript primitive types and composite types. Basic schemas include `z.string()`, `z.number()`, `z.boolean()`, `z.date()`, and `z.null()`. Composite schemas compose complex structures: `z.object()` for objects, `z.array()` for arrays, `z.union()` for discriminated unions, `z.enum()` for enumerated values, and `z.record()` for key-value maps. Optional fields use `.optional()` and nullable fields use `.nullable()`.

### Type Inference

One of Zod's most valued features is type inference. Using `z.infer<typeof schema>`, you extract the TypeScript type directly from a Zod schema. Defining `z.object({ name: z.string(), email: z.string().email() })` gives you a `User` type without redundant annotations. The inferred type includes any refinements or transformations applied in the schema.

### Transforms and Refinements

Zod supports data transformation during parsing. The `.transform()` method modifies data during validation—useful for normalizing strings or converting dates. The `.refine()` method adds custom validation logic with error messages, while `.superRefine()` provides granular control over the validation context. Preprocessing via `.preprocess()` transforms input before standard validation, enabling JSON string parsing or automatic whitespace trimming.

### Custom Schemas

Developers create reusable custom schemas using `z.custom<T>()` for cases where built-in validators are insufficient. Default values use `.default(value)`, and lazy evaluation with `z.lazy()` enables recursive schemas for tree-like data structures.

## Comparison

| Aspect | Zod | Yup | Joi |
|--------|-----|-----|-----|
| TypeScript Support | Native type inference | Requires separate types | Requires separate types |
| Bundle Size | ~12KB | ~15KB | ~200KB |
| Performance | Fast | Fast | Slower |
| Transformations | Native | Limited | Native |

Zod distinguishes itself through TypeScript-first design. While [[Yup]] and [[Joi]] were originally designed for JavaScript and later gained TypeScript support, Zod was architected for TypeScript from the start. This yields superior type inference without maintaining separate type files. Zod's smaller bundle size makes it preferable for performance-sensitive applications. However, Joi offers more comprehensive built-in validators for complex enterprise scenarios, and Yup remains popular in React Hook Form integration.

## Related

- [[typescript]] — TypeScript language that Zod leverages
- [[schema-validation]] — General concept of data validation
- [[type-inference]] — Compile-time type extraction in TypeScript
- [[yup]] — Alternative validation library
- [[joi]] — Enterprise-grade validation library
