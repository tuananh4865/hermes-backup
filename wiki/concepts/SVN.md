---
title: SVN
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [svn, version-control, subversion]
---

# SVN

## Overview

Apache Subversion (SVN) is a centralized version control system that tracks changes to files and directories over time. Originally developed by CollabNet in 2000 as an open-source alternative to CVS (Concurrent Versions System), SVN was designed to address limitations in CVS while maintaining a similar operational model. The Apache Software Foundation adopted SVN in 2010, and it has since been maintained as a top-level project.

Unlike distributed version control systems where each user has a complete local copy of the repository, SVN operates on a client-server model. A single central repository stores the full history of all changes, and developers check out working copies rather than full repositories. This centralized approach provides administrators with clear oversight of all project activity and simplifies access control management. SVN working copies contain the current state of files along with metadata that tracks which repository revision each file reflects, allowing users to see what changes have been made since last synchronization.

SVN excels in scenarios where linear history and strict access controls are priorities. It handles large binary files more efficiently than some older distributed systems, and its atomic commits ensure that either all changes in a commit are applied or none are, preventing repository corruption from failed operations. Many organizations, particularly in enterprise environments, continue to use SVN for projects that benefit from its straightforward branching model and centralized governance structure.

## Core Concepts

SVN organizes version control through a hierarchical directory structure with three fundamental components: trunk, branches, and tags.

**Trunk** represents the main line of development where active work occurs. Developers continuously commit changes to trunk, which should always contain the latest stable code ready for integration. Trunk serves as the authoritative source of truth for the current project state and the basis for creating feature branches or release branches.

**Branches** are parallel development lines that diverge from trunk or from other branches. Feature branches isolate new development work from the main codebase, allowing developers to work without disrupting stable code. Once work is complete and reviewed, branches are typically merged back into trunk. SVN uses a lightweight copy model for branching, where a branch is implemented as an efficient directory copy rather than a full duplication of files. This makes branching and merging operations relatively fast even for large projects.

**Tags** are static snapshots of the repository at a specific point in time. Unlike branches, tags are not intended for ongoing development and should not be modified after creation. Common uses include marking release versions (e.g., v1.0.0, v2.1.3), creating build baselines, or preserving significant milestones. In SVN convention, tags reside in a dedicated `/tags/` directory alongside `/trunk/` and `/branches/` at the repository root.

Additional important concepts include **revisions**, which are immutable snapshots of the entire repository at a given point, identified by sequential numbers starting from zero, and **properties**, which are metadata attached to files and directories including version information, merge tracking data, and custom user-defined attributes.

## SVN vs Git

Git and SVN both serve the fundamental purpose of version control but differ substantially in architecture, performance characteristics, and workflow implications.

The most fundamental difference is their architecture. Git is distributed, meaning every developer has a complete local repository including full history. SVN is centralized with a single server repository and client working copies. This distinction affects everything from network dependency to collaboration patterns.

Performance characteristics vary notably between the systems. Git operations like commits, branches, and history queries typically execute instantly on local data. SVN commits directly to the central repository, which requires network access but provides immediate server-side backup and verification. For operations that require comparing versions or viewing logs, Git can do this entirely offline while SVN needs server connectivity.

Branching and merging reveal significant differences in design philosophy. Git branches are extremely lightweight pointers to commits, designed for frequent creation and rapid switching. SVN branches are directory copies, which can consume more storage but provide intuitive visual organization. Modern Git excels at complex merge scenarios with sophisticated conflict resolution, while SVN's merge tracking has historically required more manual attention.

Collaboration models differ accordingly. Git enables fully distributed workflows where developers share changes peer-to-peer through remotes, patches, or forks. SVN typically uses a hub-and-spoke model where all contributors push to a central repository.

Offline capability represents a practical advantage of Git, allowing full development operations during travel or connectivity issues. SVN requires server access for commits and certain operations, though checkout and basic edits work offline.

For projects prioritizing linear history, fine-grained access controls, or intuitive folder-based organization, SVN remains a viable choice. For projects needing maximum flexibility, offline work, or complex collaborative branching, Git typically offers advantages.

## Related

- [[Version Control]] - The broader discipline of tracking changes to files
- [[Git]] - The leading distributed version control system
- [[CVS]] - The predecessor system SVN was designed to replace
- [[Branching Strategy]] - Approaches to organizing parallel development lines
- [[Merge]] - The process of combining changes from different branches
- [[Repository]] - The storage location for versioned files and their history
