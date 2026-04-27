---
title: Yup
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [validation, schema, javascript, typescript, form-validation]
---

# Yup

## Overview

Yup is a JavaScript schema builder for value parsing and validation that has become a de facto standard for form validation in the React and broader JavaScript ecosystems. Originally created by Jason Quense and maintained as an open-source project, Yup provides an expressive, chainable API for defining validation schemas that can parse, validate, and transform data against defined rules. Unlike simpler validation libraries that only check conditions, Yup schemas serve a dual purpose: they both validate the structure and content of data AND transform raw input into properly typed, normalized values.

The library excels in form validation scenarios where you need to validate user input before it reaches your backend, ensure API request payloads match expected formats, or validate configuration files. Its schema-as-code approach means validation rules are declarative and self-documenting, making it easy to understand what constraints data must satisfy just by reading the schema definition.

## Key Concepts

**Schema**: The core concept in Yup. A schema is an object that defines the shape, types, and validation rules for a piece of data. Schemas can be nested, arrays of schemas can validate lists, and special schema types handle objects with dynamic keys.

**Validation Types**: Yup supports all common JavaScript data types through specialized schema constructors:

- `string()` — Validates strings with options for length, regex patterns, and built-in validators like email, url, uuid
- `number()` — Validates numbers with options for min, max, integer, and floating point
- `boolean()` — Validates boolean values
- `date()` — Validates JavaScript Date objects with min/max range options
- `array()` — Validates arrays with options for element type (using `Schema.of()`) and length constraints
- `object()` — Validates plain objects with named shape properties
- `mixed()` — Validates any type, useful as a base for custom validation

**Chained Validators**: Each schema type exposes a chainable API where you append multiple validation rules. Each method in the chain adds a constraint or transformation. For example, `string().required().min(3).max(50).email()` creates a string that must be present, between 3 and 50 characters, and match email format.

**Transformation**: Yup can transform values during validation. Built-in transforms normalize inputs (trimming strings, converting numeric strings to numbers) and custom transforms can restructure data. Transforms run before validation by default, allowing you to normalize input before checking it.

**Error Messages**: Each validator accepts a custom error message as its final argument, enabling localization and more descriptive feedback. The default messages are human-readable but can be overridden for production applications.

**Async Validation**: Some validation scenarios require asynchronous operations — checking if a username is taken, verifying an API key, looking up a record in a database. Yup supports async validation by returning a Promise from the validation function or using the `.test()` method with async callbacks.

## How It Works

Schema validation with Yup follows a predictable lifecycle:

1. **Schema Definition**: You define the expected shape of your data by composing typed schemas. The schema object is reusable and immutable — once defined, a schema can validate any number of inputs without modification.

2. **Validation Call**: Invoke `.validate(value, options)` on a schema to validate an input. The options object controls behavior like whether to abort early on the first error or collect all errors.

3. **Transformation Phase**: Before validation rules are checked, transform functions run to normalize the input. For example, `string().transform((v) => v.trim())` removes leading/trailing whitespace from all string inputs.

4. **Validation Phase**: Each chained validator is executed in order. Validators can access the current value, the schema's parent object (for cross-field validation), and the validation context. If a validator fails, it returns an error.

5. **Error Collection**: By default, Yup stops at the first error. Setting `abortEarly: false` in options collects all validation failures, which is useful for displaying comprehensive form feedback.

6. **Result**: On success, `.validate()` returns the transformed value. On failure, it throws a `ValidationError` with a structured `.errors` array and `.inner` property containing detailed error information.

```javascript
// Yup validation lifecycle example
const schema = object({
  name: string()
    .required('Name is required')
    .min(2, 'Name must be at least 2 characters'),
  email: string()
    .required('Email is required')
    .email('Invalid email format'),
  age: number()
    .required('Age is required')
    .min(0, 'Age cannot be negative')
    .max(150, 'Age seems unrealistic'),
});

try {
  const validated = await schema.validate(rawFormData, { abortEarly: false });
  // validated is fully typed and transformed
  console.log('Valid data:', validated);
} catch (err) {
  if (err.name === 'ValidationError') {
    const errors = err.errors; // ['Name is required', 'Invalid email format']
    // Display errors to user
  }
}
```

## Practical Applications

**Form Validation**: Yup is most commonly used with form libraries like React Hook Form, Formik, or raw form implementations to validate user input before submission. Pairing Yup with a form library provides a clean separation between form state management and validation logic.

**API Request Validation**: Validate incoming API requests on the server side using Yup schemas. This ensures that your endpoints receive data in the expected shape, preventing type errors and injection attacks. Many Express and Fastify applications use Yup for request middleware.

**Configuration Validation**: Define schemas for application configuration objects loaded from environment variables, config files, or remote sources. Validation at load time catches misconfiguration early with clear error messages.

**Data Sanitization**: Use Yup's transformation capabilities to sanitize and normalize data from untrusted sources. Transformations can strip dangerous characters, convert formats, and enforce consistent data shapes.

**Testing Data Factories**: Some teams use Yup schemas to define the shape of test data factories, ensuring test fixtures match the same validation rules as production data.

## Examples

**Nested Object Validation**:
```javascript
const addressSchema = object({
  street: string().required(),
  city: string().required(),
  zipCode: string().matches(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code'),
  country: string().oneOf(['US', 'CA', 'MX']).default('US'),
});

const personSchema = object({
  firstName: string().required('First name is required'),
  lastName: string().required('Last name is required'),
  email: string().required().email(),
  address: addressSchema,
  hobbies: array().of(string().min(1)).min(1, 'At least one hobby required'),
});

const result = await personSchema.validate({
  firstName: 'Ada',
  lastName: 'Lovelace',
  email: 'ada@example.com',
  address: {
    street: '123 Computing Way',
    city: 'London',
    zipCode: 'SW1A 1AA',
    country: 'UK',
  },
  hobbies: ['mathematics', 'computing'],
});
```

**Conditional Validation**:
```javascript
const subscriptionSchema = object({
  plan: string().oneOf(['free', 'pro', 'enterprise']).required(),
  paymentMethod: string().when('plan', {
    is: 'free',
    then: (schema) => schema.strip(), // Remove from output
    otherwise: (schema) => schema.required('Payment method required for paid plans'),
  }),
  companyName: string().when(['plan', 'paymentMethod'], {
    is: (plan, payment) => plan === 'enterprise' && payment,
    then: (schema) => schema.required('Company name required for enterprise'),
  }),
});
```

**Custom Validation with .test()**:
```javascript
const userSchema = object({
  username: string()
    .required()
    .min(3)
    .max(20)
    .matches(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores')
    .test(
      'no-reserved-words',
      'This username is reserved',
      async (value) => !await isReservedWord(value)
    ),
  password: string()
    .required()
    .min(8)
    .test(
      'no-common-passwords',
      'This password is too common',
      (value) => !COMMON_PASSWORDS.includes(value)
    )
    .test(
      'no-username',
      'Password cannot contain username',
      function(value) {
        const { username } = this.parent;
        return !value.toLowerCase().includes(username.toLowerCase());
      }
    ),
});
```

## Related Concepts

- [[schema-validation]] — The broader practice of validating data against schemas
- [[form-validation]] — Validating form inputs, the most common use case for Yup
- [[types]] — TypeScript type inference from Yup schemas
- [[react-hook-form]] — A React form library commonly paired with Yup
- [[api-validation]] — Validating API request/response payloads

## Further Reading

- [Yup Official Documentation](https://github.com/jquense/yup) — API reference and usage examples
- [Yup with React Hook Form](https://react-hook-form.com/docs/useform/register) — Integration patterns
- [Zod](https://zod.dev) — A TypeScript-first alternative to Yup with type inference
- [Joi](https://joi.dev/) — The original Node.js validation library that inspired Yup's API design

## Personal Notes

Yup strikes a great balance between power and simplicity for client-side form validation. The chainable API makes schemas readable, and the ability to share schemas between client and server validation is valuable. One gotcha: by default, validation runs on the schema definition file, so if you're using lazy evaluation for conditional fields, make sure you're calling `.validate()` not just accessing the schema. Also, Yup's `.default()` only applies when the field is `undefined`, not when it's an empty string — remember to handle that distinction in your forms.
