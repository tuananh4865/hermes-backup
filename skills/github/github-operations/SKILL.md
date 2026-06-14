---
name: github-operations
description: Complete GitHub workflow — auth, repo management, PR workflow, code review, issue management, and codebase inspection. Covers HTTPS token setup, SSH keys, gh CLI, PR creation/review/merge, issue CRUD/triage, and repo metrics via pygount.
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [github, git, PR, code-review, repo-management, gh-cli, issues, triage, codebase, pygount, loc]
    related_skills: [git-workflow-and-versioning, github-auth, github-pr-workflow, github-code-review, github-repo-management, github-issues, codebase-inspection]
---

# GitHub Operations

Comprehensive GitHub workflow covering authentication, repository management, PR lifecycle, and code review. Uses the `gh` CLI and native git.

## Umbrella Note

This skill absorbs six formerly separate skills:
- `github-auth` — HTTPS token setup, SSH key configuration
- `github-pr-workflow` — branch, commit, PR creation, CI, merge
- `github-code-review` — PR diffs, inline comments, review workflow
- `github-repo-management` — clone, fork, release, nested repo backup
- `github-issues` — issue CRUD, labeling, assignment, triage, bulk ops
- `codebase-inspection` — LOC, language breakdown, code/comment ratios via pygount

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

## Section: Issues (`github-issues`)

Create, search, triage, and manage GitHub issues. Each subsection shows `gh` first, then the `curl` fallback.

### Setup (auth + repo detection)

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="***"
else
  AUTH="***"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

### Viewing Issues

```bash
# gh
gh issue list
gh issue list --state open --label "bug"
gh issue list --assignee @me
gh issue list --search "authentication error" --state all
gh issue view 42

# curl fallback
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" \
  | python3 -c "import sys,json
for i in json.load(sys.stdin):
  if 'pull_request' not in i:
    print(f\"#{i['number']:5}  {i['state']:6}  {i['title']}\")"
```

### Creating Issues

```bash
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body-file /tmp/body.md \
  --label "bug,backend" \
  --assignee "username"
```

**CRITICAL — body-file pitfall**: Always use `--body-file` for complex bodies. Inlining with `--body` breaks on backticks, multi-line code, and special chars. Write the body to `/tmp/issue_body.md` first, then `gh issue create ... --body-file /tmp/issue_body.md`.

Starter templates for body files:
- `templates/bug-report.md`
- `templates/feature-request.md`

For repos without a local git clone, use `--repo owner/repo`:
```bash
gh issue create --repo NousResearch/hermes-agent --title "Bug title" --body-file /tmp/body.md
```

### Managing Issues

```bash
# Add/remove labels
gh issue edit 42 --add-label "priority:high,bug"
gh issue edit 42 --remove-label "needs-triage"

# Assignment
gh issue edit 42 --add-assignee username
gh issue edit 42 --add-assignee @me

# Comment
gh issue comment 42 --body "Investigated — root cause is in auth middleware."

# Close / reopen
gh issue close 42
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### Linking Issues to PRs

Issues auto-close when a PR body contains one of:

```
Closes #42
Fixes #42
Resolves #42
```

To create a branch from an issue:
```bash
gh issue develop 42 --checkout
# or manually
git checkout main && git pull origin main
git checkout -b fix/issue-42-login-redirect
```

### Triage Workflow

1. List untriaged: `gh issue list --label "needs-triage" --state open`
2. Read each issue (`gh issue view N`), categorize (bug / feature / question)
3. Apply labels (`gh issue edit N --add-label "bug,priority:high"`)
4. Assign if owner is clear (`gh issue edit N --add-assignee @me`)
5. Comment with triage notes if needed

### Bulk Operations

```bash
# Close all issues with a specific label
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --reason "not planned"
```

### Quick Reference

| Action | gh | curl endpoint |
|--------|-----|--------------|
| List issues | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| View issue | `gh issue view N` | `GET /repos/{o}/{r}/issues/N` |
| Create issue | `gh issue create ...` | `POST /repos/{o}/{r}/issues` |
| Add labels | `gh issue edit N --add-label ...` | `POST /repos/{o}/{r}/issues/N/labels` |
| Assign | `gh issue edit N --add-assignee ...` | `POST /repos/{o}/{r}/issues/N/assignees` |
| Comment | `gh issue comment N --body ...` | `POST /repos/{o}/{r}/issues/N/comments` |
| Close | `gh issue close N` | `PATCH /repos/{o}/{r}/issues` |
| Search | `gh issue list --search "..."` | `GET /search/issues?q=...` |

---

## Section: Codebase Inspection (`codebase-inspection`)

Analyze repositories for lines of code, language breakdown, file counts, and code-vs-comment ratios using `pygount`.

### When to Use

- User asks for LOC (lines of code) count
- User wants a language breakdown of a repo
- User asks about codebase size or composition
- User wants code-vs-comment ratios
- General "how big is this repo" questions

### Prerequisites

```bash
pip install --break-system-packages pygount 2>/dev/null || pip install pygount
```

### Basic Summary (Most Common)

Get a full language breakdown with file counts, code lines, and comment lines:

```bash
cd /path/to/repo
pygount --format=summary \
  --folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,.eggs,*.egg-info" \
  .
```

**IMPORTANT:** Always use `--folders-to-skip` to exclude dependency/build directories, otherwise pygount will crawl them and take a very long time or hang.

### Folder Exclusions by Project Type

```bash
# Python projects
--folders-to-skip=".git,venv,.venv,__pycache__,.cache,dist,build,.tox,.eggs,.mypy_cache"

# JavaScript/TypeScript projects
--folders-to-skip=".git,node_modules,dist,build,.next,.cache,.turbo,coverage"

# General catch-all
--folders-to-skip=".git,node_modules,venv,.venv,__pycache__,.cache,dist,build,.next,.tox,vendor,third_party"
```

### Filter by Language

```bash
# Only count Python files
pygount --suffix=py --format=summary .

# Only count Python and YAML
pygount --suffix=py,yaml,yml --format=summary .
```

### Detailed File-by-File Output

```bash
# Default format shows per-file breakdown
pygount --folders-to-skip=".git,node_modules,venv" .

# Sort by code lines (pipe through sort)
pygount --folders-to-skip=".git,node_modules,venv" . | sort -t$'\t' -k1 -nr | head -20
```

### Output Formats

```bash
pygount --format=summary .   # Summary table (recommended default)
pygount --format=json .      # JSON output for programmatic use
```

### Interpreting Results

The summary table columns:
- **Language** — detected programming language
- **Files** — number of files of that language
- **Code** — lines of actual code (executable/declarative)
- **Comment** — lines that are comments or documentation
- **%** — percentage of total

Special pseudo-languages:
- `__empty__` — empty files
- `__binary__` — binary files (images, compiled, etc.)
- `__generated__` — auto-generated files (detected heuristically)
- `__duplicate__` — files with identical content
- `__unknown__` — unrecognized file types

### Pitfalls

1. **Always exclude .git, node_modules, venv** — without `--folders-to-skip`, pygount will crawl everything and may take minutes or hang on large dependency trees.
2. **Markdown shows 0 code lines** — pygount classifies all Markdown content as comments, not code. This is expected behavior.
3. **JSON files show low code counts** — pygount may count JSON lines conservatively. For accurate JSON line counts, use `wc -l` directly.
4. **Large monorepos** — for very large repos, consider using `--suffix` to target specific languages rather than scanning everything.

---

## References

Former standalone skill content absorbed here:
- `references/github-auth.md` — full auth setup guide
- `references/github-pr-workflow.md` — complete PR lifecycle reference
- `references/github-code-review.md` — detailed review workflow
- `references/github-repo-management.md` — repo operations guide
