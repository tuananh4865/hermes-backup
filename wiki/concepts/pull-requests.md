---
title: "Pull Requests"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [pull-requests, version-control, git, code-review, collaborative-development, GitHub]
---

# Pull Requests

## Overview

A Pull Request (PR) is a workflow mechanism in distributed version control systems, most notably Git, that enables developers to notify team members about changes they have made to a repository branch. When a developer wants to merge their changes into another branch (typically the main branch), they open a pull request, which creates an interface for code review, discussion, automated checks, and eventual integration of the changes.

Pull requests are central to the **forking workflow** and **branching workflow** models of collaborative software development. They serve as the focal point for quality assurance in modern software teams: no code enters the main codebase without passing through a pull request, where it can be reviewed, tested, and discussed before integration.

The name "pull request" comes from the operation of "pulling" changes from one branch into another. Rather than pushing changes directly to a shared branch (which could introduce unvetted code), a developer requests that the maintainers "pull" their changes, giving them an opportunity to review first. This seemingly simple mechanism has become the backbone of distributed software collaboration, used by millions of developers on platforms like GitHub, GitLab, Bitbucket, and Azure DevOps.

## Key Concepts

**Source branch** is the branch containing the changes being proposed. The developer creates a feature branch from the target branch, commits their changes, and then opens a PR to merge that feature branch back into the target.

**Target branch** (or base branch) is the branch into which the changes will be merged, typically `main`, `master`, or a release branch. PRs allow explicit control over where code lands.

**Diff** is the comparison between the source and target branches, showing exactly what lines were added, modified, or removed. Reviewers examine the diff to understand the changes and identify issues.

**Reviews** are the formal assessment of a pull request by one or more team members. Reviewers can leave comments on specific lines, approve the PR, request changes, or simply acknowledge the review without blocking merge.

**Merge strategies** determine how the history of the source branch is integrated into the target. Common strategies include:
- **Merge commit**: Creates a new commit that combines histories of both branches
- **Squash and merge**: Combines all commits into a single commit on the target branch
- **Rebase and merge**: Replays the source branch's commits onto the target

**Status checks** (or CI checks) are automated tests and validations that run against the PR code. PRs can be configured to block merging until all required checks pass, ensuring code quality gates.

**CODEOWNERS** files define which teams or individuals are automatically requested to review certain code paths, ensuring domain experts are always in the loop.

## How It Works

The pull request lifecycle typically follows these stages:

1. **Creation**: A developer pushes a branch and opens a PR via the hosting platform's UI or CLI. They provide a title, description, and optionally reference linked issues.

2. **Review**: Team members are notified and examine the code. They may:
   - Comment with questions or suggestions
   - Approve (optional or required based on branch protection rules)
   - Request changes (blocking merge until addressed)
   - Approve with comments (non-blocking)

3. **CI/CD Pipeline**: Automated tests run against the PR. These may include unit tests, integration tests, linting, security scans, and build verification.

4. **Discussion**: The team discusses the changes in the PR's comment thread. The author may push additional commits in response to feedback.

5. **Merge**: Once all requirements are met (approvals, passing checks), the PR is merged. The feature branch can be deleted automatically or manually.

6. **Closure**: The PR is closed, and linked issues may be automatically transitioned (e.g., closing an issue when its fix is merged).

```bash
# Typical PR workflow using GitHub CLI
gh repo clone owner/project
git checkout -b feature/add-login-oauth
# ... make commits ...
git push -u origin feature/add-login-oauth
gh pr create --title "Add OAuth login support" --body "Fixes #123"
# ... await reviews, push fixes ...
gh pr merge --squash
```

**Branch protection rules** control what is required before a PR can merge. Settings include requiring a minimum number of approvals, requiring passing CI checks, disallowing force pushes, and requiring linear history.

## Practical Applications

Pull requests serve multiple purposes in modern development teams:

- **Code quality gate**: Every change gets at least one other pair of eyes before entering the main codebase
- **Knowledge sharing**: Team members learn about changes across the codebase through review
- **Audit trail**: PR descriptions and comments provide context for why changes were made
- **CI/CD trigger**: PRs can automatically trigger build and test pipelines
- **Documentation**: The PR itself becomes part of the project record

Large organizations often have strict PR requirements: minimum reviewer counts, required CODEOWNERS sign-offs for certain directories, mandatory security reviews for sensitive changes, and linear history requirements to keep git blame useful.

## Examples

A typical PR for a bug fix might look like this:

**Title**: Fix null pointer exception in user profile loader

**Description**:
```
## Problem
When the user profile service is unavailable, the loader throws an NPE
instead of displaying a graceful error state.

## Solution
Added null check before accessing the profile object. Returns
UserProfileError with RECOVERY_HINT instead of crashing.

## Testing
- [x] Unit test covering unavailable service scenario
- [x] Manual test in dev environment
- [x] Verified error message displays correctly

Closes #456
```

## Related Concepts

- [[Git]] — The version control system underlying pull request workflows
- [[Code Review]] — The practice of systematically examining code changes
- [[Branching Strategy]] — Models for organizing branches and PRs (GitFlow, trunk-based development)
- [[Continuous Integration]] — Automated testing triggered by PRs
- [[GitHub]] and [[GitLab]] — Platforms that host pull request functionality
- [[Forking Workflow]] — Collaboration model where PRs come from forked repositories

## Further Reading

- GitHub's "About pull requests" documentation
- "How to Write a Good Pull Request Description" — Several engineering blog posts on PR hygiene
- "The Code Review Checklist" — Standard items to verify in any PR review

## Personal Notes

Pull requests have become so ubiquitous that it's strange to think there was a time when developers pushed directly to shared branches. The discipline of "PR first, then merge" enforces documentation (you're forced to describe your change), review (someone else sees it before it ships), and traceability (PRs and commits are linkable to issues and tickets). My personal practice: keep PRs small and focused. A 200-line PR gets reviewed carefully; a 2000-line PR gets a cursory glance and a rubber stamp.
