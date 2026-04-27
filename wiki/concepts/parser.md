---
title: "Parser"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [compilers, parsing, languages, text-processing, AST]
---

# Parser

## Overview

A parser is a program or component that analyzes text according to a formal grammar, constructing a structured representation from raw character sequences. Parsers are the bridge between textual input and semantic meaning—taking source code, configuration files, query strings, or any structured text and producing data structures that downstream systems can process programmatically. The output is typically an [[Abstract Syntax Tree]] (AST) that captures hierarchical relationships while discarding superficial syntax like whitespace and comments.

Parsers are fundamental to every programming language implementation—[[Compiler|compilers]] and [[Interpreter|interpreters]] both begin with parsing. But parsers also appear in web servers (parsing HTTP headers), APIs (parsing JSON or XML), and databases (parsing SQL queries). The [[Parser Generator|parser generator]] tools like ANTLR, Yacc, and Lark automate parser construction from grammar specifications.

The theory of parsing divides into two broad categories: top-down parsing (starting from the root grammar symbol and recursively expanding) and bottom-up parsing (starting from tokens and reducing toward grammar symbols). Each has different error handling characteristics and performance trade-offs.

## Key Concepts

### Lexical Analysis (Tokenization)

Before parsing, a **lexer** (also called scanner or tokenizer) divides the input into tokens—meaningful sequences of characters. The lexer applies regular expression rules to classify tokens: identifiers, keywords, operators, literals. This separation of concerns keeps the grammar simple and enables lexer reuse across multiple grammars.

```
Input: "result = x + 42 * y"
Tokens: IDENTIFIER("result"), EQUALS, IDENTIFIER("x"), PLUS, NUMBER(42), STAR, IDENTIFIER("y")
```

### Context-Free Grammars (CFG)

Parsers are defined by [[Context-Free Grammar|context-free grammars]]—formal specifications of syntax. A grammar consists of terminal symbols (tokens), non-terminal symbols (patterns), and production rules that expand non-terminals into sequences of terminals and non-terminals.

```peg
expression = term (("+" / "-") term)*
term = factor (("*" / "/") factor)*
factor = NUMBER / "(" expression ")"
```

### Abstract Syntax Trees (AST)

The parser produces an AST—a tree representation where nodes are grammar constructs and edges represent containment. Unlike a parse tree (which includes every grammar production), an AST captures semantic structure, omitting syntactic sugar. The AST is the interface between parsing and semantic analysis or interpretation.

### Error Recovery

Real parsers must handle syntax errors gracefully. Common strategies include:
- **Panic mode**: Skip tokens until a synchronization point (like a semicolon or closing brace)
- **Phrase-level recovery**: Attempt local corrections (inserting a missing token)
- **Error productions**: Include common mistakes in the grammar

## How It Works

Parser implementation approaches vary in complexity and flexibility:

**1. Recursive Descent** — Write a function for each grammar rule that directly implements the expansion. Simple for small grammars, readable, but can become unwieldy for complex languages. Many hand-written parsers use this approach.

**2. Table-Driven LR Parsing** — Use a parser generator that produces state tables. Handles more grammars efficiently, but the tables are opaque. [[ANTLR]] produces tree parsers that can handle any grammar.

**3. Parsing Expression Grammars (PEG)** — Deterministic choice-based grammars where alternatives are tried in order. No ambiguity by construction—useful when language design is under your control.

**4. Pratt Parsing** — Combines top-down parsing with operator precedence for expressions. Elegant for languages where expressions need different handling than statements. Used in TypeScript's parser.

## Practical Applications

### Configuration Files

Applications parse TOML, YAML, or JSON configuration files. A [[Schema Validation|schema validator]] may run after parsing to enforce configuration structure.

### Query Languages

[[SQL]] engines parse queries before optimization and execution. NoSQL databases parse query predicates. [[GraphQL]] has its own query language parsed by servers.

### Build Systems

[[Build Tool|Build tools]] parse dependency specifications, Makefiles, or package manifests (like `package.json`).

## Examples

A simple recursive descent parser for arithmetic expressions:

```python
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self):
        return self.expression()
    
    def expression(self):
        left = self.term()
        while self.current().type in ('PLUS', 'MINUS'):
            op = self.current()
            self.advance()
            right = self.term()
            left = ('binop', op, left, right)
        return left
    
    def term(self):
        left = self.factor()
        while self.current().type in ('STAR', 'SLASH'):
            op = self.current()
            self.advance()
            right = self.factor()
            left = ('binop', op, left, right)
        return left
    
    def factor(self):
        token = self.current()
        if token.type == 'NUMBER':
            self.advance()
            return ('literal', token.value)
        elif token.type == 'LPAREN':
            self.advance()
            expr = self.expression()
            self.expect('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected {token}")
    
    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    
    def advance(self):
        self.pos += 1
    
    def expect(self, token_type):
        if self.current().type != token_type:
            raise SyntaxError(f"Expected {token_type}")
        self.advance()
```

## Related Concepts

- [[Abstract Syntax Tree]] - The tree structure produced by parsing
- [[Compiler]] - Complete language implementation pipeline starting with parser
- [[Interpreter]] - Executes parsed code directly
- [[Lexer]] - Tokenizer that precedes parsing
- [[Regular Expressions]] - Pattern matching used in lexing

## Further Reading

- *Compilers: Principles, Techniques, and Tools* (The Dragon Book) — Definitive text on parsing theory
- *Crafting Interpreters* by Bob Nystrom — Practical guide to building parsers and interpreters

## Personal Notes

I've built parsers both by hand and using generator tools. For one-off needs like config files, a hand-written recursive descent parser is often faster to implement correctly than wrestling with a generator. But for production languages, parser generators provide guarantees about coverage and reduce maintenance burden. The key insight: parsing is solved technology. Don't reinvent the wheel—use established tools unless you have a compelling reason.
