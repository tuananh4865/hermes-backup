---
title: "Dead Code Detection"
description: "The practice of identifying and removing code that is never executed or provides no functional contribution to a software system."
tags: [code-quality, static-analysis, refactoring, technical-debt, automated-testing]
created: 2026-04-12
updated: 2026-04-20
type: concept
sources:
  - https://en.wikipedia.org/wiki/Dead_code_elimination
  - https://github.com/analysis-tools-dev/static-analysis
  - https://www.sonarsource.com/products/codequality/security/
related:
  - [[code-quality]]
  - [[static-analysis]]
  - [[technical-debt]]
  - [[refactoring]]
  - [[automated-testing]]
---

# Dead Code Detection

Dead code is any code that can be executed but never contributes to the program's output or behavior. This includes:

- **Unreachable code** — protected by conditions that can never be true
- **Unused functions** — defined but never called from any code path
- **Obsolete features** — feature flags removed but associated code left behind
- **Commented-out code** — historical artifacts that serve no purpose
- **Duplicate implementations** — multiple ways to do the same thing, only one used

## Why Dead Code Matters

Dead code accumulates silently. Every software project over 2-3 years has it. The problems it causes:

- **Cognitive overhead** — developers waste time understanding code that does nothing
- **Maintenance burden** — changing an interface but missing dead code that still references it
- **Security risk** — dead code may contain vulnerabilities that are never patched because no one knows it exists
- **Performance traps** — in some languages, dead code still gets loaded into memory
- **Test pollution** — dead code can cause tests to pass when they shouldn't

## Detection Techniques

### Static Analysis (Primary Approach)

Modern static analysis tools detect dead code through control flow analysis:

| Tool | Strength | Language Support |
|------|----------|----------------|
| SonarQube | Deep integration, CI/CD pipelines | 20+ languages |
| Semgrep | Custom rules, fast | 15+ languages |
| Pyflakes | Simple, Python-native | Python only |
| ESLint (no-unused-vars) | JavaScript/TypeScript | JS/TS |
| Go's `go vet` | Built-in, zero config | Go |

### Coverage Analysis (Runtime)

Tools like Istanbul/NYC for JavaScript, Coverage.py for Python, and JaCoCo for Java measure which code paths are actually executed during tests. Code covered by tests is by definition live; code with zero coverage is a dead code candidate.

### Language-Specific Tools

- **Python**: `pyflakes`, `vulture` (finds dead code), `interrogate` (docstring coverage)
- **JavaScript/TypeScript**: `ts-prune`, `depcheck` (unused dependencies and code)
- **Go**: `staticcheck` includes `U1000` (unused variable/function/import)
- **Rust**: The compiler itself catches most unused code via `#[allow(dead_code)]` requirement

## The `git blame` Pattern

One of the most effective dead code detection techniques is temporal: find code that hasn't been modified in N months (configurable, often 6-12 months). If code hasn't been touched in over a year and has no tests covering it, it's a strong candidate for removal.

```bash
# Find files not modified in 12 months
git log --since="12 months ago" --name-only --pretty=format: | sort | uniq
```

## Automated Removal Workflow

The safest approach to removing dead code follows this sequence:

1. **Identify** — static analysis + coverage analysis
2. **Verify** — search entire codebase for any references (comments, strings, dynamic calls)
3. **Test** — ensure test suite passes before AND after removal
4. **Remove** — delete the code
5. **Commit separately** — dead code removal deserves its own commit with explanation

## Dead Code vs. Code Quality

Dead code is a subset of [[technical-debt]]. Like all technical debt, it accumulates gradually and requires intentional effort to address. The best teams have a "zero tolerance" policy: every PR that touches a file should also remove any dead code discovered in that file's scope.

## Related Concepts

- [[static-analysis]] — the category of tools that detect dead code
- [[code-quality]] — overall code health and maintainability
- [[technical-debt]] — dead code as a form of debt that slows development
- [[refactoring]] — the process of improving code structure, often including dead code removal
- [[automated-testing]] — tests that verify dead code removal doesn't break anything
