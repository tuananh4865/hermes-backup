---
title: Chakra UI
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [chakra-ui, ui, components, react, accessible, design-system, frontend]
---

# Chakra UI

## Overview

Chakra UI is a popular, open-source React component library designed for building accessible, themeable, and composable user interfaces. Created by Segun Adebayo and first released in 2019, Chakra UI has become a go-to choice for React developers who want to rapidly build modern web applications without sacrificing accessibility or design flexibility. The library emphasizes simplicity, offering a clean API that abstracts away the complexity of styling while remaining fully customizable through a powerful theming system.

The library's core philosophy centers on style props—using React props directly for styling rather than separate CSS files or complex className systems. This approach dramatically accelerates development velocity while maintaining CSS-level power through a built-in style props API and support for CSS-in-JS features like responsive styles, pseudo-selectors, and dark mode.

## Key Concepts

### Style Props

Chakra UI allows you to style components directly through props:

```tsx
// Traditional CSS approach
<div className="flex items-center justify-between p-4 bg-blue-500">
  <h1 className="text-white text-2xl font-bold">Hello</h1>
</div>

// Chakra UI style props approach
<Box display="flex" alignItems="center" justifyContent="space-between" p={4} bg="blue.500">
  <Heading color="white" fontSize="2xl" fontWeight="bold">Hello</Heading>
</Box>
```

### Component Composition

Chakra UI emphasizes composability through polymorphic components:

```tsx
// Composing components for reusable UI patterns
const Card = ({ title, children }) => (
  <Box borderWidth="1px" borderRadius="lg" overflow="hidden">
    <Box bg="gray.100" p={4} fontWeight="bold">{title}</Box>
    <Box p={4}>{children}</Box>
  </Box>
);

const Button = ({ children, colorScheme = "blue", ...props }) => (
  <ChakraButton colorScheme={colorScheme} {...props}>
    {children}
  </ChakraButton>
);
```

### Theming

Chakra UI includes a powerful, extensible theme system:

```tsx
import { extendTheme } from '@chakra-ui/react';

const theme = extendTheme({
  colors: {
    brand: {
      50: '#e3f2fd',
      500: '#2196f3',
      900: '#1565c0',
    },
  },
  fonts: {
    heading: 'Inter, sans-serif',
    body: 'Inter, sans-serif',
  },
  components: {
    Button: {
      baseStyle: { fontWeight: '600' },
      variants: {
        solid: { bg: 'brand.500', color: 'white' },
      },
    },
  },
});
```

### Accessibility

Chakra UI ships with accessibility built-in:

- All interactive components have proper ARIA attributes
- Focus management works out of the box
- Keyboard navigation is fully supported
- Color contrast meets WCAG guidelines

## How It Works

Chakra UI is built on several foundational technologies:

1. **@emotion/react**: CSS-in-JS library for styling
2. **@emotion/styled**: Component creation with styled API
3. **React Context**: Theme and component state management
4. **React ARIA**: Accessible primitives

When you use a component like `<Button>`, Chakra UI:
- Wraps a base component with emotion styling
- Injects accessible attributes automatically
- Resolves styles from the theme
- Handles responsive styles and pseudo-selectors

## Practical Applications

Chakra UI excels in several scenarios:

- **Rapid Prototyping**: Quickly build UI mockups with minimal styling code
- **Dashboard Applications**: Data-heavy apps benefit from consistent component styling
- **Design Systems**: Build custom component libraries on top of Chakra's primitives
- **Internal Tools**: Fast development for admin panels and B2B tools
- **Startup MVPs**: Speed to market without design compromise

## Examples

Building a complete form with validation:

```tsx
import {
  Box,
  FormControl,
  FormLabel,
  Input,
  Button,
  FormErrorMessage,
  useToast,
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const toast = useToast();

  const onSubmit = (data) => {
    toast({
      title: 'Login successful',
      status: 'success',
      duration: 3000,
    });
    console.log(data);
  };

  return (
    <Box maxW="md" mx="auto" mt={8} p={6} borderWidth="1px" borderRadius="lg">
      <form onSubmit={handleSubmit(onSubmit)}>
        <FormControl isInvalid={!!errors.email}>
          <FormLabel>Email</FormLabel>
          <Input type="email" {...register('email', { required: true })} />
          <FormErrorMessage>Email is required</FormErrorMessage>
        </FormControl>

        <FormControl isInvalid={!!errors.password} mt={4}>
          <FormLabel>Password</FormLabel>
          <Input type="password" {...register('password', { required: true })} />
          <FormErrorMessage>Password is required</FormErrorMessage>
        </FormControl>

        <Button type="submit" colorScheme="blue" width="full" mt={6}>
          Sign In
        </Button>
      </form>
    </Box>
  );
}
```

## Related Concepts

- [[design-systems]] — Systematic approaches to UI design and component libraries
- [[ui-components]] — Reusable UI building blocks
- [[react]] — The JavaScript library Chakra UI is built for
- [[accessibility]] — Making interfaces usable by everyone
- [[css-in-js]] — Styling approach used by Chakra UI

## Further Reading

- [Chakra UI Official Documentation](https://chakra-ui.com/)
- [Chakra UI GitHub Repository](https://github.com/chakra-ui/chakra-ui)
- [Zero to Production with Chakra UI](https://egghead.io/courses/build-a-modern-user-interface-with-chakra-ui-f253)

## Personal Notes

Chakra UI was my gateway to component libraries in React. The style props API felt strange at first coming from CSS files, but the productivity gains were immediately apparent. I've used it for several side projects and internal tools. The dark mode support is excellent and the theming system is powerful enough for most use cases. One caveat: for very large applications, the CSS-in-JS runtime can impact performance—consider alternatives like Panda CSS or vanilla Extract for such cases.
