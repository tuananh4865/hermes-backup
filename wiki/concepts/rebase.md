---
title: Rebase
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [rebase, git, version-control, branching, commit-history]
---

# Rebase

## Overview

Rebase is one of the two primary methods for integrating changes from one [[git]] branch into another (the other being [[merge]]). Where merge combines entire commit histories as-is, rebasing rewrites the commit sequence by replaying commits from one branch onto a new base. This creates a cleaner, more linear commit history that is easier to read and understand. However, because rebase rewrites commit history (changing commit hashes), it must be used with caution on shared branches.

The fundamental principle of rebase is: take the commits from your feature branch and replay them, one by one, on top of the target branch's latest commit. The result looks as if your feature was developed against the current state of the target branch all along. This is why rebase is often described as "rebasing your branch onto the updated main."

Rebase is most commonly used in [[branching strategy]] workflows where developers want to maintain a clean, linear project history—popularized by workflows like [[GitHub Flow]] and the "squash and merge" approach.

## Key Concepts

### The Golden Rule of Rebase

**Never rebase commits that have been pushed to a shared repository.** Once other developers have based work on your commits, rewriting those commits (which rebase does) will create divergent histories that are painful to reconcile. If you've pushed a branch and are collaborating on it, use merge instead of rebase.

Private, local branches that haven't been shared can be rebased freely.

### Fast-Forward vs. Non-Fast-Forward Rebase

When the branch you're rebasing onto has not diverged (i.e., your branch is simply ahead of the target), rebase performs a **fast-forward**—it simply moves the branch pointer to the new base. No new commits are created; the existing commits are reused as-is.

When branches have diverged (both have new commits since the split), rebase performs a **three-way merge** for each commit being replayed, creating new commit objects with new hashes.

### Interactive Rebase

Interactive rebase (`git rebase -i`) provides fine-grained control over the commit sequence:

```
git rebase -i HEAD~5  # Edit the last 5 commits
```

This opens an editor with a list of commits and available commands:
- **pick** — Keep the commit as-is
- **reword** — Change the commit message
- **edit** — Pause to amend the commit
- **squash** — Combine with the previous commit
- **fixup** — Like squash but discard this commit's message
- **drop** — Remove the commit entirely

This is the primary tool for cleaning up commit history before submitting a [[pull request]].

### Auto-squashing

Git supports automatic squashing of fixup commits using the `--autosquash` flag:

```bash
git commit --fixup <original-commit-hash>
git rebase -i --autosquash HEAD~10
```

This automatically marks fixup commits for squashing against their target commits, eliminating manual sorting.

## How It Works

The mechanical process of `git rebase target-branch`:

1. Identify the common ancestor of the current branch and `target-branch`
2. Save aside all commits unique to the current branch
3. Reset the current branch to `target-branch`'s HEAD
4. Replay each saved commit, one at a time, onto the new base
5. For each replay, Git performs a three-way merge (or fast-forward if possible)
6. Conflicts, if any, are flagged per-commit and must be resolved before continuing

If conflicts occur during replay, Git pauses on the problematic commit. You resolve the conflict, `git add` the resolved files, then `git rebase --continue`. You can also `git rebase --abort` to cancel the entire operation.

```
Before rebase:
    A---B---C  (feature)
   /
D---E---F---G  (main)

After rebase:
           A'--B'--C'  (feature)
          /
D---E---F---G  (main)
```

## Practical Applications

### Keeping a Feature Branch Updated

When developing a long-running feature branch, periodically rebasing onto the updated main branch prevents the eventual integration from being a massive, conflict-laden merge:

```bash
git checkout feature/my-work
git fetch origin
git rebase origin/main
# Resolve any conflicts, then continue
git rebase --continue
```

### Cleaning Up Before a Pull Request

Before opening a PR, squash related micro-commits into logical units:

```bash
git rebase -i HEAD~8
# Mark commits as 'squash' or 'fixup' to combine them
```

This gives reviewers a coherent set of changes rather than a stream of "WIP," "fix typo," "actually fix it" commits.

### Linear History Enforcement

Many teams enforce linear history in their main branch by configuring their Git host to reject non-fast-forward merges:

```bash
# In .git/config or via CLI
git config branch.main.rebase true
```

This causes `git pull` to use rebase instead of merge, keeping history linear.

## Examples

### Basic rebase onto main:

```bash
# Starting on a feature branch that diverged from main
git status
# On branch feature/my-feature

# Fetch latest remote
git fetch origin

# Rebase onto updated main
git rebase origin/main

# If there are conflicts:
# Fix the files, then:
git add .
git rebase --continue

# Push (force since history changed)
git push --force-with-lease
```

### Interactive rebase to clean up commits:

```bash
git rebase -i HEAD~5
# Opens editor:
# pick a1b2c3d Add user authentication
# pick e5f6g7h Fix typo in auth
# pick i9j0k1l WIP
# pick m2n3o4p Add password reset
# pick q5r6s7t Fix another typo

# Change to:
# pick a1b2c3d Add user authentication
# fixup e5f6g7h Fix typo in auth
# squash i9j0k1l WIP
# pick m2n3o4p Add password reset
# fixup q5r6s7t Fix another typo
```

Result: 3 commits instead of 5.

### Rebase onto an upstream branch for a pull request:

```bash
# Sync your fork's main with upstream
git fetch upstream
git checkout feature/my-pr
git rebase upstream/main

# Resolve conflicts if any, then push
git push --force-with-lease origin feature/my-pr
```

## Related Concepts

- [[git]] — The version control system
- [[merge]] — The alternative integration method
- [[branch]] — Git branches and branch management
- [[branching-strategy]] — Branching models and workflows
- [[pull-request]] — Code review and integration via PRs
- [[commit]] — Git commit objects and history
- [[conflict-resolution]] — Resolving merge/rebase conflicts

## Further Reading

- [Git Rebase Documentation](https://git-scm.com/docs/git-rebase)
- [Atlassian Git Rebase Tutorial](https://www.atlassian.com/git/tutorials/rewriting-history/git-rebase)
- [Pro Git: Rebasing](https://git-scm.com/book/en/v2/Git-Branching-Rebasing)
- [When to Merge vs. Rebase](https://www.gitkraken.com/learn/git/best-practices/git-branch-strategy)

## Personal Notes

I used to fear rebase due to the "never rebase pushed commits" rule. Once I internalized that, rebase became my most-used integration tool. The `--force-with-lease` flag is essential when pushing after rebase—it refuses to overwrite if someone else has pushed to the branch in the meantime, which protects against accidental overwrites. For pull requests, I always do an interactive rebase to squash WIP commits before review. Reviewers get a cleaner diff, and the main branch history remains readable.
