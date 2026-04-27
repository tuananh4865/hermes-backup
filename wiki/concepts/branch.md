---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 git (extracted)
  - 🔗 merge (extracted)
  - 🔗 workflow (inferred)
last_updated: 2026-04-11
tags:
  - git
  - branching
  - version-control
  - workflow
---

# Branch

> Git branches enable parallel development by creating independent lines of work.

## Overview

A branch in Git is a lightweight pointer to a commit. Creating a branch lets you:
- Work on features without affecting main code
- Experiment freely without risk
- Collaborate on multiple features simultaneously
- Isolate production hotfixes from development

## Key Concepts

### HEAD
HEAD is a pointer to your current location:
```
HEAD → main → abc123
```

Switching branches moves HEAD:
```
git checkout feature → HEAD → feature → def456
```

### Branch Types

| Type | Purpose | Lifespan |
|------|---------|----------|
| **main/master** | Production code | Permanent |
| **develop** | Integration branch | Long-lived |
| **feature/** | New features | Short-lived |
| **bugfix/** | Bug fixes | Short-lived |
| **hotfix/** | Production fixes | Short-lived |
| **release/** | Release preparation | Short-lived |

## Common Commands

### Viewing Branches
```bash
# List local branches
git branch

# List all branches (local + remote)
git branch -a

# List branches with last commit
git branch -v

# Show current branch
git branch --show-current
```

### Creating Branches
```bash
# Create from current position
git branch feature/login

# Create and switch
git checkout -b feature/login

# Create from specific commit
git branch feature/login abc123

# Create from another branch
git branch feature/login main
```

### Switching Branches
```bash
# Switch (old way)
git checkout feature/login

# Switch (new way)
git switch feature/login

# Switch to previous branch
git switch -
```

### Deleting Branches
```bash
# Delete merged branch
git branch -d feature/login

# Force delete unmerged
git branch -D feature/login

# Delete remote branch
git push origin --delete feature/login
```

## Branching Strategies

### 1. Git Flow
```
main ────────────────────────────────
          ↑                ↑
          │ hotfix/1.0.1   │ merge
          └───────┬────────┘
                  │
develop ────────────────────────────
    ↑                    ↑
    │ feature/login       │ release/1.0
    └─────────┬───────────┘
              │
    feature/login ──────────
```

**Branches:**
- `main`: Production releases
- `develop`: Integration, pre-release
- `feature/*`: New features
- `release/*`: Release preparation
- `hotfix/*`: Production fixes

### 2. GitHub Flow
Simpler, continuous deployment:
```
main ────────────────────────────────
          ↑           ↑
          │ feature/   │ merge + deploy
          │ login      │
          └─────┬──────┘
                │
    feature/login ──────────
```

**Rules:**
- `main` is always deployable
- Feature branches from `main`
- PR for code review
- Squash and merge to `main`

### 3. Trunk-Based Development
Developers commit directly to main (or very short-lived branches):
```
main ────────────────────────────────
    ↑       ↑       ↑
    │       │       │ commit
    └───────┴───────┘
```

**For:**
- Small teams
- Continuous deployment
- Fast iteration

## Working with Branches

### Stashing Changes
```bash
# Save current changes
git stash save "WIP: login feature"

# List stashes
git stash list

# Apply latest stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop stash
git stash drop
```

### Rebasing
```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase (squash, edit, reorder)
git rebase -i HEAD~5

# Continue after resolving conflicts
git rebase --continue

# Abort rebase
git rebase --abort
```

### Cherry-picking
```bash
# Pick a commit from another branch
git cherry-pick abc123

# Pick without committing
git cherry-pick -n abc123
```

## Branch Naming

### Conventions
```bash
# Features
feature/login-page
feature/user-authentication
feature/955-add-dark-mode

# Bug fixes
bugfix/login-crash
bugfix/1234-fix-memory-leak

# Hotfixes
hotfix/security-patch
hotfix/critical-login-bug

# Releases
release/v1.0.0
release/v2.1.0-beta
```

### Good Practices
- Use prefixes: `feature/`, `bugfix/`, `hotfix/`
- Include issue number if using issue trackers
- Keep names short but descriptive
- Use kebab-case: `feature/login-page` not `feature/loginPage`

## Remote Branches

### Tracking
```bash
# Set upstream tracking
git branch -u origin/feature/login

# Or when pushing
git push -u origin feature/login

# See tracking info
git branch -vv
```

### Fetching
```bash
# Fetch all remotes
git fetch --all

# Fetch specific branch
git fetch origin feature/login

# Prune deleted remote branches
git fetch --prune
```

## Branch Protection

### GitHub Settings
```bash
# Via GitHub UI:
# Settings → Branches → Add rule

# Or via CLI (GitHub CLI)
gh api repos/:owner/:repo/branches/main/protection -X PUT \
  -f required_status_checks=null \
  -f enforce_admins=true \
  -f required_pull_request_reviews=true
```

### Protection Rules
- Require PR reviews
- Require status checks to pass
- Require branches to be up to date
- Restrict who can push
- Allow force pushes (or not)

## Branch Workflow for Wiki

```bash
# Start new task
git checkout -b expand/batch-3-stubs

# Work on expansion
# ... make changes ...

# Commit
git add concepts/*.md
git commit -m "feat: expand batch 3 stubs"

# Push
git push -u origin expand/batch-3-stubs

# When done, merge via PR
gh pr create --base main --head expand/batch-3-stubs
```

## Related Concepts

- [[git]] — Git basics
- [[commit]] — Commits (branch commits)
- [[merge]] — Merging branches
- [[workflow]] — Git workflow strategies

## External Resources

- [Git Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials/using-branches)