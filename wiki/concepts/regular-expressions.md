---
title: "Regular Expressions"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [text-processing, string-matching, pattern-matching, programming-fundamentals]
---

# Regular Expressions

## Overview

Regular expressions (regex) are sequences of characters that define search patterns for matching, locating, and manipulating text. They are a powerful and compact notation for describing text patterns that would be cumbersome or impossible to express with simple string functions. Originally formalized in theoretical computer science through automata theory, regex has become an indispensable tool in software development, data validation, text mining, and system administration. Every major programming language, text editor, and command-line tool provides some form of regex support.

At their core, regular expressions allow you to describe patterns in text—such as "an email address," "a phone number," or "a line that starts with a timestamp"—in a concise, composable notation. This makes them ideal for tasks ranging from validating user input forms to parsing log files to transforming data in ETL pipelines.

## Key Concepts

Regex syntax is built from a small set of primitive elements that combine to form complex patterns.

**Literals and Metacharacters** — Most characters match themselves literally. However, a set of characters called metacharacters have special meaning: `. ^ $ * + ? { } [ ] \ | ( )`. To match a literal metacharacter, you escape it with a backslash.

**Character Classes** — Square brackets define a set of characters to match. `[aeiou]` matches any vowel. Ranges work too: `[0-9]` matches any digit, `[a-zA-Z]` matches any letter. Negation uses `^` inside the class: `[^0-9]` matches any non-digit.

**Predefined Character Classes** — `\d` matches a digit (equivalent to `[0-9]`), `\w` matches a word character (`[a-zA-Z0-9_]`), `\s` matches whitespace. Their capitals are negated: `\D`, `\W`, `\S`.

**Quantifiers** — Determine how many times the preceding element may match: `*` (zero or more), `+` (one or more), `?` (zero or one), `{n}` (exactly n), `{n,m}` (between n and m).

**Anchors** — Don't match characters but assert positions: `^` start of string/line, `$` end of string/line, `\b` word boundary.

**Groups and Alternation** — Parentheses create capture groups for extraction or backreferences. The pipe `|` creates alternation: `cat|dog` matches "cat" or "dog".

## How It Works

Under the hood, a regex engine compiles the pattern into a finite automaton—either a Deterministic Finite Automaton (DFA) or a Non-deterministic Finite Automaton (NFA). NFAs are more expressive and allow features like backreferences and lazy quantifiers, but can suffer from catastrophic backtracking on certain inputs. Most modern regex engines (PCRE, Python's `re`, JavaScript's RegExp) are NFA-based, which means poorly designed patterns can exhibit exponential worst-case matching time.

When a regex is applied to an input string, the engine scans through the string attempting to match the pattern at each position until a match is found or the string is exhausted. Greedy quantifiers (`.*`, `.+`) match as much as possible before backtracking, while lazy quantifiers (`.*?`, `.+?`) match as little as possible.

## Practical Applications

Regular expressions are used extensively for input validation (email addresses, phone numbers, credit card formats), data extraction from unstructured text (pulling dates, URLs, or prices from logs), search-and-replace operations in text editors and IDEs, log parsing and analysis, web scraping, and syntax highlighting. In data pipelines, regex is often the first step in transforming messy text fields into structured data.

## Examples

Validating an email address (simplified):

```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

Extracting dates from a log file:

```python
import re

log_line = "2026-04-13 09:15:32 ERROR connection timeout"
date_pattern = r'\d{4}-\d{2}-\d{2}'
match = re.search(date_pattern, log_line)
print(match.group())  # "2026-04-13"

# Extract all numbers from text
numbers = re.findall(r'\d+', "Order 12345 shipped on 2026-04-13")
print(numbers)  # ['12345', '2026', '04', '13']
```

Matching HTML tags:

```regex
<([a-z]+)[^>]*>(.*?)</\1>
```

## Related Concepts

- [[json-schema]] — Schema validation that often uses regex for string format validation
- [[documentation-quality]] — Clean documentation often involves consistent text patterns
- [[technical-writing]] — Regex used in maintaining consistent documentation formatting

## Further Reading

- Jeffrey Friedl, *Mastering Regular Expressions* (3rd Edition, O'Reilly)
- Python `re` module documentation: https://docs.python.org/3/library/re.html
- Regex101.com — Interactive regex testing and debugging tool
- "Regular Expression Matching Can Be Simple And Fast" — Russ Cox (2007)

## Personal Notes

Regex is one of those tools where knowing the basics unlocks a lot of power, but it's also easy to overconfidently write a complex pattern that passes all your tests and then fails mysteriously on real-world input. I try to keep patterns as simple and readable as possible, and I use regex101 extensively to debug them. For anything beyond simple validation, I often reach for proper parsers, but regex remains my go-to for quick text extraction tasks.
