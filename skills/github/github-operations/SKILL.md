---
name: github-operations
description: Complete GitHub workflow — auth, repo management, PR workflow, and code review. Covers HTTPS token setup, SSH keys, gh CLI, PR creation, review, merge, and repo operations.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, git, PR, code-review, repo-management, gh-cli]
    related_skills: [git-workflow-and-versioning, github-auth, github-pr-workflow, github-code-review, github-repo-management]
---

# GitHub Operations

Comprehensive GitHub workflow covering authentication, repository management, PR lifecycle, and code review. Uses the `gh` CLI and native git.

## Umbrella Note

This skill absorbs four formerly separate skills:
- `github-auth` — HTTPS token setup, SSH key configuration
- `github-pr-workflow` — branch, commit, PR creation, CI, merge
- `github-code-review` — PR diffs, inline comments, review workflow
- `github-repo-management` — clone, fork, release, nested repo backup

Below are labeled subsections for each domain. Each was formerly a standalone skill.

---

## Section: Authentication (`github-auth`)

### HTTPS Token Setup

```bash
# Configure gh to use HTTPS instead of SSH
gh auth setup-git
gh auth status
```

### SSH Key Configuration

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Add to GitHub
gh ssh-key add ~/.ssh/id_ed25519.pub --title "Hermes Agent"

# Verify
ssh -T git@github.com
```

### Token Management

```bash
# Store token
gh auth token | pbcopy

# Check auth status
gh auth status
```

---

## Section: Repository Management (`github-repo-management`)

### Clone / Create / Fork

```bash
# Clone
gh repo clone owner/repo

# Create new repo
gh repo create my-repo --public --clone

# Fork
gh repo fork owner/repo
```

### Nested Repo Backup

For backing up large directories (wikis, knowledge bases) into GitHub with proper .gitignore:

```bash
# In the large directory
cd /path/to/large-wiki

# Initialize with .gitignore for nested .git dirs
git init
echo "*/.git" >> .gitignore
git add .
git commit -m "Initial commit"

# Add remote and push
git remote add origin https://github.com/user/repo.git
git push -u origin main
```

**CRITICAL for nested repos:** Before committing, ensure `*/.git` is in .gitignore to avoid embedding nested .git directories. Failure to do this makes the backup repo enormous.

### Releases

```bash
# Create release
gh release create v1.0.0 --title "Release v1.0.0" --notes "Release notes"

# Upload assets
gh release upload v1.0.0 ./dist/bin --clobber
```

---

## Section: PR Workflow (`github-pr-workflow`)

### Standard PR Lifecycle

```bash
# 1. Create branch
git checkout -b feature/my-feature

# 2. Make changes and commit
git add .
git commit -m "feat: add new feature"

# 3. Push and create PR
git push -u origin feature/my-feature
gh pr create --title "feat: add new feature" --body "Description" --reviewer owner

# 4. Check CI status
gh pr checks

# 5. Merge (squash merge)
gh pr merge --squash

# 6. Delete branch
git branch -d feature/my-feature
git push origin --delete feature/my-feature
```

### PR from Fork

```bash
# Clone fork
gh repo clone your-username/repo
cd repo

# Add upstream
git remote add upstream https://github.com/original-owner/repo.git

# Create PR
git checkout -b feature
# make changes
git push your-username feature
gh pr create --repo original-owner/repo
```

### Sync Fork with Upstream

```bash
git fetch upstream
git checkout main
git merge upstream/main
git push
```

---

## Section: Code Review (`github-code-review`)

### Review PRs

```bash
# View PR diff
gh pr diff owner/repo --repo owner/repo

# Checkout PR locally
gh pr checkout 123

# Review with inline comments
gh pr review 123 --body "LGTM with suggestions"

# Request changes
gh pr review 123 --request-changes --body "Needs fix before merge"
```

### Search and Filter

```bash
# Search PRs
gh search prs --repo owner/repo --state open --reviewer owner

# List PRs by author
gh pr list --author owner --state open

# View PR status
gh pr status
```

---

## References

Former standalone skill content absorbed here:
- `references/github-auth.md` — full auth setup guide
- `references/github-pr-workflow.md` — complete PR lifecycle reference
- `references/github-code-review.md` — detailed review workflow
- `references/github-repo-management.md` — repo operations guide
