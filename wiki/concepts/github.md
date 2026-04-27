---
title: GitHub
created: 2026-04-12
updated: 2026-04-12
type: concept
tags: [github, git, collaboration, platform]
---

# GitHub

## Overview

GitHub is a web-based hosting platform for version control and collaborative software development, built on top of [[Git]], the distributed version control system. Founded in 2008 and acquired by Microsoft in 2018, GitHub has grown into the largest code hosting platform in the world, serving millions of developers and organizations. It provides a graphical interface for managing Git repositories, facilitating source code management, bug tracking, feature requests, task management, and continuous integration. GitHub operates on a freemium model, offering free public repository hosting and paid plans for private repositories with advanced features.

At its core, GitHub enables developers to store their code remotely, track changes over time, and collaborate with others through branching strategies and merge workflows. The platform hosts over 420 million repositories as of 2025, making it a central hub for open-source software development and enterprise code management alike. Beyond simple code storage, GitHub provides a comprehensive ecosystem of tools designed to support the entire software development lifecycle, from ideation to deployment.

## Features

GitHub offers a rich set of features that extend far beyond basic Git hosting.

**Pull Requests (PRs)** are one of GitHub's most defining features. They provide a structured way for developers to propose changes to a codebase, request reviews from team members, and discuss modifications before merging. Pull requests serve as a focal point for code review conversations, allowing line-by-line comments, approval workflows, and automated status checks. This process ensures code quality and facilitates knowledge sharing within teams.

**GitHub Issues** is a lightweight tracking system for bug reports, feature requests, and project tasks. Issues can be assigned to team members, labeled for categorization, linked to pull requests, and organized into milestones. The tight integration between Issues and other GitHub features creates a seamless workflow for managing project priorities and tracking progress over time.

**GitHub Actions** is a powerful continuous integration and continuous deployment (CI/CD) platform built directly into GitHub. It allows developers to automate workflows triggered by repository events such as pushes, pull requests, or scheduled times. Actions can run tests, build containers, deploy applications, and perform virtually any automated task using a marketplace of pre-built actions or custom workflows defined in YAML files.

Additional notable features include **GitHub Pages** for hosting static websites directly from repositories, **GitHub Copilot** for AI-assisted code completion, **Projects** for kanban-style project management, **Wikis** for documentation, and **Security** features including dependency scanning and secret detection.

## Comparison

GitHub competes with other Git hosting platforms, most notably [[GitLab]] and [[Bitbucket]]. Each platform has distinct strengths and target audiences.

GitHub is generally considered the industry standard for open-source projects, boasting the largest community and most extensive marketplace of integrations. Its pull request workflow is widely regarded as best-in-class, and the platform's network effects make it the default choice for many developers. However, GitHub's free tier historically offered fewer private repository features compared to competitors, though this has improved significantly in recent years.

GitLab positions itself as an all-in-one DevOps platform, offering a more comprehensive suite of tools out-of-the-box including integrated CI/CD, container registry, and project management features. GitLab's free tier includes more advanced features, and its open-source nature appeals to organizations seeking transparency or self-hosting options. Many enterprises prefer GitLab for its built-in compliance and security features.

Bitbucket, owned by Atlassian, integrates deeply with other Atlassian products like Jira and Confluence. It offers free unlimited private repositories for small teams and provides strong support for Mercurial in addition to Git. Bitbucket is often chosen by organizations already invested in the Atlassian ecosystem for seamless toolchain integration.

The choice between these platforms typically depends on team size, budget, existing toolchain, and specific feature requirements. All three platforms offer similar core Git functionality, with differentiation coming from ecosystem, integrations, and additional features beyond basic version control.

## Related

- [[Git]] - The underlying distributed version control system
- [[GitLab]] - Competing Git hosting and DevOps platform
- [[Bitbucket]] - Atlassian-owned Git hosting service
- [[Pull Requests]] - GitHub's code review and merge workflow feature
- [[Continuous Integration]] - Practice of automating builds and tests
- [[GitHub Actions]] - GitHub's built-in CI/CD and automation platform
