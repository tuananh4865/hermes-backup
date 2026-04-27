---
title: "Merge"
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [git, merge, version-control, collaboration]
---

# Merge

## Overview

Merge is a fundamental operation in version control systems that combines changes from two or more distinct branches into a single unified branch. In Git, merging integrates the commit history of one branch into another, preserving the linear progression of work while incorporating collaborative contributions. When developers work on feature branches, bug fixes, or experiments, merge allows their changes to be safely incorporated into the main codebase without overwriting or discarding work done by others.

The merge process in Git is intelligent: it analyzes the divergent commit histories, identifies the common ancestor commit, and determines what changes need to be applied to bring the branches together. This collaborative workflow enables teams to work concurrently on different features while maintaining a coherent project history.

## Types

Git supports several merge strategies that determine how diverged histories are combined:

**Fast-Forward Merge** occurs when the branch receiving the merge has not diverged from the source branch. Since no conflicting commits exist on the target branch, Git simply moves the branch pointer forward to the latest commit of the source branch. This results in a linear history but discards the separate branch context. Fast-forward merges are common when integrating short-lived feature branches that had no concurrent modifications.

**Three-Way Merge** is used when both branches have progressed with independent commits. Git identifies the common base commit and compares it against the two branch tips, then creates a new merge commit that incorporates changes from both histories. This strategy handles divergent work gracefully and preserves the full branch structure, though it may require conflict resolution.

**Recursive Merge** is Git's default strategy for handling three-way merges, particularly effective when branches have diverged significantly. It recursively handles merge bases when dealing with complex histories involving multiple branching points, creating a single consolidated merge commit. This strategy excels at managing octopus-style merges of multiple branches simultaneously.

**Octopus Merge** allows merging more than two branches at once. Git combines multiple branch heads in a single merge commit, useful for integrating several feature branches concurrently.

## Conflicts

Merge conflicts arise when Git cannot automatically reconcile changes because the same lines or regions of a file were modified differently across branches. Conflicts typically occur when two developers modify the same function, when one branch deletes a file while another modifies it, or when structural changes to the codebase conflict.

When a conflict occurs, Git marks the affected files with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), separating the competing changes into distinct sections. Developers must manually edit these files to select or combine the appropriate changes, removing markers and ensuring the code is syntactically correct.

After resolving conflicts in working files, developers use `git add` to stage the resolved files and `git commit` to complete the merge. Some tools like `git mergetool` provide visual interfaces for conflict resolution, showing side-by-side comparisons of conflicting versions.

Preventing conflicts involves frequent rebasing onto main branches, maintaining small focused commits, and communicating with team members about file ownership. Experienced teams establish conventions around modifying shared code to minimize collision points.

## Related

- [[Git]] — the distributed version control system that implements merge operations
- [[Branch]] — parallel lines of development that are merged together
- [[Rebase]] — an alternative to merging that rewrites commit history
- [[Conflict Resolution]] — the process of manually reconciling competing changes
- [[Version Control]] — the broader discipline of tracking and managing file changes
- [[Pull Request]] — a collaboration mechanism that often triggers merge operations
- [[Commit]] — the atomic unit of change in a Git repository
