---
title: "Interpreter"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [design-patterns, software-architecture, design, patterns, oop]
---

# Interpreter

## Overview

The Interpreter pattern is a behavioral design pattern in object-oriented programming that defines a representation for a grammar of a language and provides a mechanism to interpret sentences in that language. It is one of the Gang of Four design patterns and is particularly useful when you need to process simple languages, configuration formats, or domain-specific query engines without building a full compiler. The pattern represents the grammar as a hierarchy of classes (one class per grammar rule) and uses recursion to interpret expressions.

While the Interpreter pattern is elegant for simple grammars, it is generally not recommended for complex languages because the maintenance burden grows significantly as the grammar expands. In practice, parser generators like ANTLR, Yacc, or Lark are preferred for serious language work. However, understanding Interpreter remains valuable for grasping how languages are processed and for implementing simple rule engines or expression evaluators.

## Key Concepts

**Abstract Expression**: An interface or abstract class defining the `interpret(context)` method that all concrete expressions implement.

**Terminal Expressions**: Leaf nodes in the grammar that represent actual values or constants. They implement the expression interface and don't contain sub-expressions.

**Non-terminal Expressions**: Composite expressions that contain and evaluate sub-expressions according to grammar rules. Examples include `AndExpression`, `OrExpression`, or `BinaryExpression`.

**Context**: Contains information that the interpreter needs—variable values, state, or shared data accessible during interpretation.

**Client**: Builds the abstract syntax tree (AST) from the grammar and invokes the interpret operation on the root expression.

## How It Works

1. **Grammar Definition**: Define the language grammar as a set of production rules. Each rule becomes a class in the hierarchy.

2. **AST Construction**: The client builds an abstract syntax tree representing valid sentences in the language by combining expression objects.

3. **Recursive Interpretation**: Each expression's `interpret()` method recursively evaluates its sub-expressions (for non-terminals) or returns its value (for terminals).

4. **Context Utilization**: During interpretation, expressions read from and write to the shared context to resolve variables and store results.

```text
Expression Interface
    │
    ├── TerminalExpression (NumberExpression)
    │       │
    │       └── interpret(context) → returns constant value
    │
    └── NonTerminalExpression (AddExpression)
            │
            ├── left: Expression
            ├── right: Expression
            │
            └── interpret(context)
                    │
                    ├── left.interpret(context) → 5
                    ├── right.interpret(context) → 3
                    │
                    └── returns 5 + 3 = 8
```

## Practical Applications

- **Mathematical Expression Evaluators**: Evaluating user-provided formulas like `(3 + 5) * 2`
- **Regular Expression Engines**: Interpreting regex patterns to match strings
- **Configuration File Parsers**: Interpreting INI, YAML, or JSON-like configurations
- **Rule Engines**: Processing business rules expressed in a simple DSL
- **SQL Subset Processors**: Handling simple SQL-like queries on in-memory data

## Examples

Simple arithmetic expression interpreter in Python:

```python
from abc import ABC, abstractmethod
from typing import Dict

# Abstract Expression
class Expression(ABC):
    @abstractmethod
    def interpret(self, context: Dict[str, int]) -> int:
        pass

# Terminal Expression - Number
class NumberExpression(Expression):
    def __init__(self, number: int):
        self.number = number
    
    def interpret(self, context: Dict[str, int]) -> int:
        return self.number

# Terminal Expression - Variable
class VariableExpression(Expression):
    def __init__(self, name: str):
        self.name = name
    
    def interpret(self, context: Dict[str, int]) -> int:
        return context.get(self.name, 0)

# Non-terminal Expression - Addition
class AddExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Dict[str, int]) -> int:
        return self.left.interpret(context) + self.right.interpret(context)

# Non-terminal Expression - Multiplication
class MultiplyExpression(Expression):
    def __init__(self, left: Expression, right: Expression):
        self.left = left
        self.right = right
    
    def interpret(self, context: Dict[str, int]) -> int:
        return self.left.interpret(context) * self.right.interpret(context)

# Usage
context = {"x": 10, "y": 5}

# Represents: (x + y) * 2
expression = MultiplyExpression(
    AddExpression(VariableExpression("x"), VariableExpression("y")),
    NumberExpression(2)
)

print(expression.interpret(context))  # Output: 30
```

## Related Concepts

- [[Design Patterns]] - The broader category of software design patterns
- [[Composite Pattern]] - Similar structure, Interpreter uses it for expression trees
- [[Visitor Pattern]] - Can be used with Interpreter to add new operations on expressions
- [[Compiler]] - Transforms source code to executable form (contrast with Interpreter)
- [[Abstract Syntax Tree]] - Tree representation of program structure used by Interpreter

## Further Reading

- [Interpreter Pattern - Source Making](https://sourcemaking.com/design_patterns/interpreter)
- [Design Patterns: Interpreter - Refactoring Guru](https://refactoring.guru/design-patterns/interpreter)
- [Programming Language Pragmatics - Michael Scott](https://www.elsevier.com/books/programming-language-pragmatics/scott/978-0-12-374514-9)

## Personal Notes

I've used the Interpreter pattern for a simple rules engine in a billing system and it worked well because the grammar was small and needed flexibility. The key lesson: if you anticipate the grammar growing, consider using a proper parser generator instead. I also found that combining Interpreter with the [[Visitor Pattern]] allows adding new operations (formatting, serialization, validation) without modifying expression classes—classic open/closed principle. For any language work beyond trivial DSLs, ANTLR is almost always the better choice.
