---
title: "Himalaya"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [email, cli, terminal, himalaya]
---

# Himalaya

Himalaya is a command-line email client written in Rust, designed for Unix-like systems. It provides a fast, terminal-based interface for managing email accounts with support for multiple backends and providers.

## Overview

Himalaya aims to be a modern, extensible CLI email client that works exclusively through the terminal. Unlike traditional email clients with graphical interfaces, Himalaya embraces the Unix philosophy of composable, text-based tools. It supports reading, composing, and sending emails directly from the command line, making it ideal for developers and power users who spend most of their time in terminal environments.

The project was originally created by soywod and is now maintained under the pimalaya organization on GitHub. It leverages Rust's performance and safety guarantees to deliver a responsive experience even with large mailboxes.

## Features

Himalaya offers a comprehensive set of features for terminal-based email management:

**Multi-Account Support**: Configure multiple email accounts and switch between them seamlessly. Each account can have its own IMAP/SMTP settings, folder aliases, and authentication methods.

**Multiple Backend Support**: Himalaya supports various backends through cargo features:
- IMAP backend for standard email servers
- Maildir backend for local mail storage
- Notmuch backend for email indexing and searching
- SMTP and Sendmail backends for sending email

**Authentication Options**: Flexible authentication including password-based auth, OAuth 2.0 for Gmail and Outlook, and integration with system keyrings like GNOME Keyring or KDE Wallet.

**Message Composition**: Emails are composed using the user's preferred editor defined in `$EDITOR`, allowing full control over message content with familiar editing shortcuts.

**PGP Encryption**: Built-in support for PGP encryption via shell commands, GPG bindings, or a native implementation.

**JSON Output**: Machine-readable output via `--output json` flag enables integration with other tools and scripts.

**Vim-like Keybindings**: Navigation and management follow vim conventions for users familiar with the editor.

**Security**: Sensitive credentials can be stored in system keyrings rather than plain text configuration files.

## Configuration

Himalaya uses a TOML-based configuration file located at `~/.config/himalaya/config.toml`. The interactive wizard (`himalaya` or `himalaya account configure <name>`) guides users through initial setup.

Configuration supports numerous email providers including Gmail, Outlook, Proton Mail, and iCloud Mail. Each account section defines the backend type (IMAP/SMTP), host, port, encryption method, and authentication credentials.

For password management, users can either store raw passwords for testing, use external password managers via shell commands (e.g., `pass show account-name`), or leverage system keyring integration.

Installation is available through multiple channels: pre-built binaries via the install script, Cargo, Homebrew, Arch Linux packages, Fedora COPR, Nix, or building from source.

## Related

- [[email]] - General email concept
- [[terminal-build-startup]] - Terminal workflow concepts
- [[terminal-startup-flow]] - Terminal startup processes
- [[self-healing-wiki]] - Wiki system that created this stub
