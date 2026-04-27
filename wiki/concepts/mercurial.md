---
title: "Mercurial"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [version-control, dvcs, programming, git-alternative]
---

# Mercurial

## Overview

Mercurial (also called "hg", after its chemical symbol for mercury) is a distributed version control system for tracking changes in files during software development. Like Git, it enables developers to maintain complete repositories locally, create branches for parallel development, merge changes from different lines of work, and efficiently synchronize repositories across teams.

Mercurial was created by Matt Mackall in 2005 as an alternative to BitKeeper, which had been used for Linux kernel development but became proprietary. Mercurial was designed with performance and scalability as primary goals, capable of handling large codebases efficiently. While Git has become the dominant VCS in most of the industry, Mercurial remains in use at several large organizations and offers a different philosophical approach to version control.

## Key Concepts

**Distributed Architecture**: Every checkout is a complete repository with full history, enabling full-featured version control operations without network connectivity. Developers can work independently, commit frequently, and reorganize commits before sharing.

**Revisions and Changesets**: Changes are organized into revisions identified by a 40-character hexadecimal hash. Each revision captures a complete snapshot of the repository at that point, not just deltas.

**Branches**: Mercurial supports named branches within repositories and bookmarks (lightweight pointers) for branch-like development. Branches can be closed when work is complete.

**Extensions**: Mercurial's functionality can be extended through extensions. Some are bundled (like mq for patch management, progress for progress bars), while others are third-party.

**Phases**: Revisions can be marked as draft (local, mutable), secret (hidden from peers), or public (shared, immutable). This prevents accidentally pushing work that isn't ready.

## How It Works

Mercurial stores repository data in a `.hg` directory at the repository root:

```
.hg/
  ├── store/          # The actual revision history (under .hg/store/)
  ├── cache/         # Cached data for performance
  ├── hgrc           # Repository configuration
  ├── requires       # Repository format requirements
  ├──phasestate     # Phase information for each revision
  └── bookmarks/     # Bookmarks (similar to Git branches)
```

```bash
# Common Mercurial commands
hg init                 # Create new repository
hg clone URL           # Clone existing repository
hg add FILE            # Track new files
hg commit -m "message" # Commit changes locally
hg push                # Push changes to remote
hg pull                # Pull changes from remote
hg log                 # View commit history
hg branch NAME         # Create named branch
hg merge               # Merge another branch
hg update REVISION     # Update working directory to revision
hg status              # Show modified, added, removed files
hg diff                # Show changes
hg annotate FILE       # Show revision info for each line
```

## Practical Applications

Mercurial is used for version control across diverse development scenarios:

- **Source Code Management**: Tracking code changes for individual developers and teams
- **Distributed Development**: Enabling offline work with later synchronization
- **Branch-Based Workflows**: Isolating features, releases, and hotfixes
- **Code Review Integration**: Extensions like hg-review for Gerrit integration
- **Large Codebase Handling**: Mercurial's performance on large repositories is excellent

## Examples

**Typical Mercurial Workflow**:

```bash
# Clone a repository to start working
hg clone https://example.com/myproject
cd myproject

# Create a feature branch
hg branch feature/user-authentication
hg commit -m "Add authentication framework"

# Work and commit incrementally
hg add newfile.py
hg commit -m "Add user login form"
hg commit -m "Implement session management"

# Share changes (after testing)
hg push --new-branch

# Merge when ready
hg update default
hg merge feature/user-authentication
hg commit -m "Merge authentication feature"
```

**Configuration (.hgrc)**:

```ini
# ~/.hgrc or repo/.hg/hgrc

[ui]
username = Your Name <your.email@example.com>
editor = vim

[paths]
default = https://example.com/myproject
backup = ssh://user@backupserver//path/to/backup

[extensions]
# Enable useful bundled extensions
progress = 
purge = 
rebase = 
mq = 

[web]
description = My Project
contact = Your Name <your.email@example.com>
```

## Related Concepts

- [[Git]] - The most popular DVCS, with similar concepts but different command syntax
- [[Version Control]] - The broader discipline Mercurial implements
- [[Distributed Version Control]] - The category of VCS Mercurial belongs to
- [[Software Development]] - The domain where Mercurial is applied
- [[Branching Strategy]] - Workflow patterns for using branches in version control

## Further Reading

- [Mercurial Official Website](https://www.mercurial-scm.org/)
- [Mercurial Wiki](https://www.mercurial-scm.org/wiki/)
- ["Mercurial: The Definitive Guide" by Bryan O'Sullivan](https://book.mercurial-scm.org/)

## Personal Notes

Mercurial's design philosophy emphasizes simplicity and performance. Where Git sometimes feels like a toolbox you're expected to assemble yourself, Mercurial provides a more complete "batteries included" experience. The commands are often more intuitive than Git's. That said, Git's dominance means more community resources, more integrations, and more tutorials available. If you're choosing a VCS for a new project, Git's network effects make it the default, but Mercurial is a solid choice with a gentler learning curve.
