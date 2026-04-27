---
title: "DEP/NX"
created: 2026-04-21
updated: 2026-04-21
type: concept
tags: [security, exploit-mitigation]
confidence: medium
sources: []
---

# DEP/NX

## Overview

DEP (Data Execution Prevention) and NX (No-eXecute) are operating system security features that mark certain memory regions as non-executable. This prevents code from running in memory regions that should only contain data (like the stack or heap), blocking a common exploitation technique.

## How It Works

When a program attempts to execute code from a memory page marked as non-executable, the CPU raises an exception. This stops buffer overflow exploits that inject and run malicious code on the stack or heap.

## Related Concepts

- [[buffer-overflow]] — Exploit technique DEP prevents
- [[aslr]] — Address Space Layout Randomization, often paired with DEP
- [[secure-coding]] — Writing code resistant to memory exploits
- [[exploit-development]] — Understanding attacker techniques
