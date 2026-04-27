---
title: Git
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [git, version-control, dvcs, developer-tools]
---

## Overview

Git is a distributed version control system (DVCS) created by Linus Torvalds in 2005 for the development of the Linux kernel. Unlike centralized version control systems where users check out files from a single server, Git gives every developer a complete local copy of the entire repository, including its full history. This architecture enables developers to work offline, commit changes locally, and synchronize with remote repositories only when needed.

The distributed nature of Git provides significant advantages for collaborative software development. Each clone contains the complete dataset, so if any server dies or is corrupted, any client repository can be used to restore the server. Git has become the industry standard for version control, powering millions of projects from open-source initiatives to enterprise-scale software systems. Its speed, data integrity, and support for distributed workflows make it an essential tool in modern software development.

## Core Concepts

### Commits

A [[commit]] represents a snapshot of changes at a specific point in time. Each commit contains a unique SHA-1 hash identifier, the author's information, a commit message describing the changes, and pointers to its parent commits. Git commits form a directed acyclic graph (DAG), where each commit knows its predecessors, allowing complete traceability of code history. Commits are lightweight and inexpensive to create, encouraging developers to checkpoint their work frequently with meaningful messages.

### Branches

A [[branch]] is an independent line of development within a repository. Git's branching model is remarkably efficient—creating a new branch simply creates a new pointer to an existing commit, rather than copying entire files. The default branch is typically called "main" or "master." Developers create feature branches to work on specific changes in isolation, then merge those branches back into the mainline when ready. This isolation enables multiple parallel development streams without interfering with stable code.

### Merge vs Rebase

[[Merge]] and [[rebase]] are two strategies for combining changes from different branches. Merge integrates the entire history of one branch into another, creating a new "merge commit" that ties together the divergent histories. Merge preserves the original commit chronology and is safe for integrating published changes, but it can create a cluttered history with many merge commits.

Rebase rewrites commit history by replaying commits from one branch onto another, creating a linear history. It takes the changes introduced in each commit and reapplies them on top of the target branch. Rebase produces a clean, linear history that is easier to read and understand, but it should never be used on published commits that others have based their work on, as it rewrites commit SHAs. The choice between merge and rebase depends on the workflow and whether historical accuracy or cleanliness is prioritized.

## Related

- [[GitHub]] - A cloud-based hosting service for Git repositories
- [[GitLab]] - A web-based Git repository manager with CI/CD capabilities
- [[Bitbucket]] - A Git repository hosting service by Atlassian
- [[Commit]] - The fundamental unit of change in Git
- [[Branch]] - An independent line of development in Git
- [[Merge]] - Combining changes from different branches
- [[Rebase]] - Replaying commits on a different base
- [[Version Control]] - The broader category of systems for tracking file changes
- [[Distributed Systems]] - The architectural paradigm Git implements
