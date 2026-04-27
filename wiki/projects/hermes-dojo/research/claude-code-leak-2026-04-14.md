---
title: "Research: Claude Code Leak"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Research: Claude Code Leak

**Date:** 2026-04-14
**Topic:** Anthropic Claude Code source code leak incident
**Status:** Complete

## What Happened

**Date:** March 31, 2026
**Event:** Anthropic accidentally leaked 500,000 lines of Claude Code source code
**Cause:** Human error - misconfigured build pipeline (.npmignore or package.json files field)
**Confirmation:** Anthropic confirmed the leak

This was the SECOND incident - an early version leaked in February 2025 showing the same pattern.

## Key Facts

| Fact | Detail |
|------|--------|
| Lines leaked | ~500,000 |
| What was exposed | Core agent orchestration, memory management, prompt injection defenses |
| Vulnerability found | Days after leak (by Adversa AI) |
| Malware attack | Hackers used leak as bait to spread malware |
| Root cause | Build pipeline misconfiguration |

## What Was Exposed

The leaked code revealed:
- **Agent orchestration** - How Claude Code coordinates tasks
- **Memory management** - How it tracks context and state
- **Prompt injection defenses** - Security measures
- **Tool-use patterns** - How it interacts with the filesystem, terminal, browser

## Attackers' Response

1. **Malware distribution** - Created fake GitHub pages claiming to host the leak, bundled with malware
2. **Phishing** - Sponsored Google ads leading to fake Claude Code installation guides
3. **Exploit development** - Used the source to find vulnerabilities

## Key Takeaways

1. **Build pipeline is the biggest risk** - Not external hackers, but internal misconfiguration
2. **Single misconfigured file** - .npmignore or files field in package.json can expose everything
3. **Repeat incident** - Same type of leak happened 13 months apart
4. **Speed of exploitation** - Vulnerability found within days, malware within hours

## Related

- Fortune article: fortune.com/2026/03/31/anthropic-source-code-claude-code-data-leak
- Forbes: forbes.com/sites/the-prompt/2026/04/01/what-anthropics-leak-means-for-the-coming-wave-of-dark-code
- SecurityWeek: Critical vulnerability found after source leak
- Reddit discussion: r/ClaudeCode/comments/1s9gk7s

## Tags
#claude-code #security #leak #anthropic #ai-security #build-pipeline
