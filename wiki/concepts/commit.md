---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 git (extracted)
  - 🔗 branch (extracted)
  - 🔗 diff (inferred)
last_updated: 2026-04-11
tags:
  - git
  - commits
  - version-control
  - history
---

# Commit

> Commits are snapshots of your repository at a point in time — the atomic unit of Git history.

## Overview

A commit in Git records changes to files:
- **Snapshot**: All files at that point
- **Parent**: Previous commit (creates chain)
- **Message**: Description of what changed
- **Metadata**: Author, timestamp, SHA

Commits are immutable — changing them creates new commits.

## Anatomy of a Commit

```
commit abc123 (SHA-1 hash)
Author: Tuấn Anh <tuananh@example.com>
Date:   Sat Apr 11 12:00:00 2026 +0700

    feat: add RAG implementation guide

    - Add architecture diagram
    - Include code examples
    - Add comparison table

 | 2 files changed, 150 insertions(+), 3 deletions(-)
```

### SHA Hash
- 40-character hexadecimal string
- Uniquely identifies commit
- Can use short form (7 chars): `abc1234`

## Creating Commits

### Basic Flow
```bash
# Stage changes
git add file1.md file2.md

# Or stage all changes
git add .

# Commit with message
git commit -m "feat: add new concept page"
```

### Commit Message Format
```
<type>: <short description>

<longer description if needed>

- bullet points
- more details

Refs: #123
```

### Types
| Type | Use For |
|------|---------|
| **feat** | New feature |
| **fix** | Bug fix |
| **docs** | Documentation |
| **style** | Formatting, no code change |
| **refactor** | Code restructuring |
| **test** | Adding tests |
| **chore** | Maintenance tasks |

## Amending Commits

### Fix last commit message
```bash
git commit --amend -m "new message"
```

### Add changes to last commit
```bash
# Stage new changes
git add forgotten-file.md

# Amend (without changing message)
git commit --amend --no-edit

# Amend (with new message)
git commit --amend -m "updated message"
```

**Warning:** Only amend commits not pushed to shared branch.

## Viewing History

### Log
```bash
# Show commits (basic)
git log

# Show commits in one line
git log --oneline

# Show last N commits
git log -5

# Show commits with graph
git log --graph --oneline --all

# Show commits affecting file
git log -- path/to/file.md

# Show commits by author
git log --author="Tuấn"
```

### Show Commit
```bash
# Show commit details
git show abc123

# Show commit stats
git show abc123 --stat

# Show commit with diff
git show abc123 -p
```

## Undoing Commits

### Revert (Safe)
Creates new commit that undoes previous:
```bash
git revert abc123
```

### Reset (Destructive)
Remove commits, change history:
```bash
# Soft (keep changes staged)
git reset --soft abc123

# Mixed (keep changes unstaged)
git reset --mixed abc123

# Hard (lose all changes)
git reset --hard abc123
```

### When to Use What
| Situation | Command |
|-----------|---------|
| **Undo published commit** | `git revert` |
| **Undo unpublished commits** | `git reset` |
| **Keep changes** | `--soft` or `--mixed` |
| **Lose changes** | `--hard` |

## Finding Commits

### By Message
```bash
git log --grep="RAG"
git log --grep="fix" --grep="login" --all-match
```

### By Content
```bash
# Find commits that added/removed string
git log -S "function_name"
git log -S "TODO" -p
```

### By Date
```bash
git log --after="2026-04-01"
git log --before="2026-04-11"
git log --after="2026-04-01" --before="2026-04-11"
```

### By Author
```bash
git log --author="Tuấn"
git log --author-email="tuananh@example.com"
```

## Interactive Staging

### git add -p (Patch Mode)
```bash
git add -p

# Options for each hunk:
# y - stage this hunk
# n - skip this hunk
# s - split into smaller hunks
# e - edit hunk manually
```

### git add -i (Interactive)
```bash
git add -i

# Opens interactive menu:
# 1. Status
# 2. Update
# 3. Revert
# 4. Add untracked
# 5. ...
```

## Best Practices

1. **Atomic commits**: One logical change per commit
2. **Clear messages**: Explain "why", not just "what"
3. **Test before commit**: Don't break builds
4. **Don't commit secrets**: Use .gitignore
5. **Sign-off**: Use `git commit -s` for DCO

### Commit Message Example
```markdown
feat: add RAG implementation guide

This page explains how to implement RAG systems including:
- Architecture diagrams
- Code examples with LangChain
- Comparison with fine-tuning
- Production deployment tips

Closes #45
Reviewed-by: @reviewer
```

## Commit in Wiki Workflow

```bash
# Expand a page
vim concepts/rag.md

# Stage changes
git add concepts/rag.md

# Commit with descriptive message
git commit -m "feat: expand RAG page with implementation details

- Add LangChain code examples
- Add architecture diagram
- Add comparison table with fine-tuning
- Fix broken wikilinks"

# Push
git push
```

## Related Concepts

- [[git]] — Git basics
- [[branch]] — Branches (where commits live)
- [[merge]] — Merging commits
- [[diff]] — Comparing commits

## External Resources

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Commit Messages](https://chris.beams.io/posts/git-commit/)
- [Pro Git: Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)