# GitHub Code Review Reference

Formerly a standalone skill. Content absorbed into `github-operations`.

## Review PRs

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

## Search and Filter

```bash
# Search PRs
gh search prs --repo owner/repo --state open --reviewer owner

# List PRs by author
gh pr list --author owner --state open

# View PR status
gh pr status
```
