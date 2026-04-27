---
title: Version Control
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [version-control, git, code-management]
---

## Overview

Version control is a system that tracks changes to files over time, enabling developers to record modifications, review history, revert to previous states, and collaborate on shared codebases. It is foundational to modern software development, providing a systematic way to manage source code evolution and coordinate work among multiple contributors.

Without version control, developers risk losing work, introducing conflicting changes, or struggling to diagnose when bugs were introduced. Version control systems (VCS) solve these problems by maintaining a complete history of every change, along with metadata about who made each change and why.

## Git Fundamentals

Git is the most widely used distributed version control system, originally created by Linus Torvalds in 2005 to support Linux kernel development. Git organizes changes around three main concepts:

**Commits** are the core unit of work in Git. A commit captures a snapshot of files at a specific point, including a message describing the change, the author's identity, and a unique hash identifier. Commits form a directed acyclic graph (DAG), where each commit points to its parent(s), building a complete history tree.

**Branches** represent independent lines of development. A branch is a lightweight movable pointer to a specific commit. Creating a branch allows developers to work on features or bug fixes in isolation without affecting the main codebase. The default branch is typically called `main` or `master`.

**Merging** combines changes from one branch into another. When two branches have diverged, Git attempts to automatically reconcile differences through a merge commit, which has two parent commits. If conflicting changes exist, developers must resolve conflicts manually before completing the merge.

## Models

Version control systems operate under two primary architectural models:

**Centralized Version Control** (CVC) uses a single server to store the complete version history. Clients check out files from this central repository. Examples include Subversion (SVN) and CVS. CVC provides simple administration and visibility into all changes, but creates a single point of failure—if the central server goes down, no one can commit or access history.

**Distributed Version Control** (DVC) gives every client a full copy of the entire repository, including its complete history. Git is the dominant DVC system. This architecture eliminates single points of failure, enables powerful local operations like commits and diffs without network access, and supports diverse workflows such as pull requests and patch-based development.

## Related

- [[Git]] — Distributed version control system
- [[SVN]] — Centralized version control system
- [[Code Review]] — Process of evaluating code changes
- [[Branching Strategy]] — Approaches to organizing branches
