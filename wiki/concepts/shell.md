---
title: Shell
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [shell, terminal, bash, command-line]
---

## Overview

A shell is a command-line interface (CLI) that provides an environment for interacting with an operating system by accepting text-based commands from users and executing them. Shells act as an intermediary between the user and the kernel, translating human-readable commands into instructions the operating system can process. They are fundamental tools in Unix-like systems including Linux and macOS, and have been central to software development, system administration, and automation since the early days of computing.

Shells offer features such as command history, tab completion, job control, and scripting capabilities. Users type commands either interactively at a prompt or execute sequences of commands stored in script files. The shell interprets the syntax, handles variable expansion, and manages the execution environment including input/output streams and processes.

## Common Shells

Several shells have become widely adopted across different operating systems:

**Bash (Bourne Again Shell)** is the default shell on most Linux distributions and macOS (until recent versions transitioned to Zsh). It is an enhanced version of the original Bourne Shell (sh) and offers comprehensive features including command history, aliases, and extensive scripting support.

**Zsh (Z Shell)** is a powerful shell that combines features from Bash, ksh, and tcsh. It is known for its advanced tab completion, spelling correction, plugin frameworks like Oh My Zsh, and highly customizable prompt. Zsh has become the default shell on macOS since Catalina.

**Fish (Friendly Interactive Shell)** emphasizes user-friendliness with syntax highlighting, autosuggestions, and out-of-the-box configuration. Fish is designed for interactive use rather than scripting compatibility, though it can still execute scripts.

Other notable shells include **sh** (the original Bourne Shell), **tcsh** (TENEX C Shell), and **PowerShell** (available cross-platform, originally from Windows).

## Key Concepts

Understanding shells requires familiarity with several foundational concepts:

**Pipes** allow the output of one command to become the input of another, enabling the chaining of commands. For example, `ls -la | grep ".md"` lists files and filters for those containing ".md".

**Redirections** control where input comes from and where output goes. The `>` operator redirects standard output to a file, `>>` appends to a file, and `<` redirects input from a file. The `2>` operator redirects stderr.

**Shell Scripts** are text files containing sequences of commands that the shell executes sequentially. Scripts support variables, conditionals, loops, and functions, enabling automation of repetitive tasks. A script typically begins with a shebang line such as `#!/bin/bash`.

**Environment Variables** store configuration values that affect shell behavior and program execution. Common variables include `PATH` (directories searched for commands), `HOME` (user's home directory), and `USER` (username).

**Job Control** allows users to manage running processes, including suspending, resuming, and running tasks in the background using keystrokes like Ctrl+Z and the `bg`/`fg` commands.

## Related

- [[Bash]]
- [[Zsh]]
- [[Fish]]
- [[Terminal]]
- [[Command Line]]
- [[Scripting]]
