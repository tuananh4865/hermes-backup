---
title: Command-Line Interface (CLI)
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [cli, terminal, bash, shell]
---

## Overview

A Command-Line Interface (CLI) is a text-based interface used to interact with computer programs by typing commands into a terminal. Unlike graphical user interfaces (GUIs) that rely on windows, icons, and mouse interactions, CLIs accept text commands from users and return text output. This interaction pattern makes CLIs particularly powerful for automation, scripting, and performing tasks that require precise control over system operations.

The CLI serves as a direct communication channel between the user and the operating system's kernel. When a user types a command, the shell interprets it, executes the corresponding program, and displays the results. This workflow enables rapid execution of complex operations through simple commands or sophisticated multi-step workflows through scripting. CLIs have been fundamental to computing since the earliest operating systems and remain essential tools for developers, system administrators, and power users across all major platforms.

The efficiency of CLIs stems from their ability to chain commands together, redirect input and output between programs, and automate repetitive tasks through scripts. A single command can accomplish what would require multiple clicks in a GUI, and command sequences can be saved as scripts to reproduce complex workflows reliably. This makes CLIs especially valuable for server management, software development, data processing, and any scenario where reproducibility and efficiency matter.

## Shells

A shell is the program that provides the CLI interface to the user. It interprets commands typed at the prompt, executes them, and returns results. Shells also provide their own scripting languages, allowing users to write programs that automate system tasks.

**Bash (Bourne Again Shell)** is the most widely used shell on Linux and macOS. It is a direct descendant of the original Bourne shell (sh) and incorporates features from other shells like csh and ksh. Bash supports command history, tab completion, aliases, and a comprehensive scripting language with support for variables, control structures, and functions. Most Linux distributions include Bash as their default login shell, and it is the standard shell for shell scripts due to its compatibility and widespread availability.

**Zsh (Z Shell)** is a modern shell that builds upon Bash while adding many advanced features. It offers improved tab completion with context-aware suggestions, powerful globbing patterns for file matching, spell correction, and the Oh-My-Zsh framework that provides thousands of plugins and themes. Zsh is popular among power users and developers who spend significant time in the terminal. Its configuration is more complex than Bash, but its productivity enhancements make it worth the setup effort for many users.

Other notable shells include **Fish** (Friendly Interactive Shell), which prioritizes simplicity and out-of-the-box usability with intuitive autosuggestions and syntax highlighting, and **PowerShell**, which is designed for system administration on Windows and cross-platform environments, using a verb-noun command structure and object-based output.

## Common Commands

Every CLI user should be familiar with a core set of commands that form the foundation of working in the terminal.

**File Operations:** `ls` lists directory contents with various formatting options, `cd` changes the current directory, `cp` copies files and directories, `mv` moves or renames files, and `rm` removes files. `mkdir` creates new directories while `rmdir` removes empty ones. These commands are the basic building blocks for file management in any shell environment.

**File Viewing and Editing:** `cat` displays entire file contents, `head` and `tail` show the beginning and end of files respectively, `less` allows paginated viewing of large files, and `grep` searches for patterns within files.

**System Information:** `ps` reports running processes, `top` or `htop` display system resource usage and active processes, `df` shows disk space usage, and `uname` provides system information. `whoami` displays the current username and `pwd` prints the working directory.

**Networking:** `ping` tests network connectivity to a host, `curl` transfers data from or to URLs, `ssh` provides secure remote connections, `scp` securely copies files between hosts, and `netstat` or `ss` display network connection information.

**Permissions and Users:** `chmod` changes file permissions, `chown` changes file ownership, `sudo` executes commands with elevated privileges, and `su` switches user accounts.

## Related

- [[Shell Scripting]] - Automating tasks by writing shell scripts
- [[Bash]] - The Bourne Again Shell and its capabilities
- [[Terminal Emulators]] - Applications that provide terminal access
- [[Environment Variables]] - System variables that configure the CLI environment
- [[SSH]] - Secure remote access via the command line
- [[Regular Expressions]] - Pattern matching used extensively in CLI tools like grep
