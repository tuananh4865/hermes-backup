---
title: "Atlassian"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [atlassian, jira, confluence, bitbucket, software, collaboration, devops]
---

# Atlassian

## Overview

Atlassian is an Australian enterprise software company best known for developing a suite of collaboration and development tools widely used by software teams worldwide. Founded in 2002 by Mike Cannon-Brookes and Scott Farquhar in Sydney, Atlassian grew from a small startup into a publicly traded company (NASDAQ: TEAM) and eventually was acquired by IBM in 2024 for approximately $4.8 billion. Atlassian's flagship products include Jira (issue tracking and project management), Confluence (team knowledge wiki), Bitbucket (Git code hosting and CI/CD), and Trello (kanban-style task management). The company's product philosophy — often called the "Atlassian way" — emphasizes developer-friendly tools, cloud-native architecture, and aggressive pricing (including a very popular free tier for small teams). Atlassian's products are foundational in modern software development workflows, particularly in Agile and DevOps environments.

## Key Concepts

**Jira** is Atlassian's most well-known product. Originally designed as an issue tracker for software teams, Jira has evolved into a full-featured project management platform supporting Scrum, Kanban, and mixed methodologies. Jira offers highly customizable workflows, issue types, fields, and screens. The Jira Software product targets development teams, while Jira Service Management (formerly Jira Service Desk) targets IT and operations teams.

**Confluence** is a team wiki and collaboration platform where teams create, share, and manage knowledge. Confluence pages are organized into spaces, each with its own hierarchy. It supports rich formatting, embedded Jira issues, diagrams, and templates. Confluence is often used for meeting notes, product requirements documents (PRDs), runbooks, and team handbooks.

**Bitbucket** is Atlassian's Git code hosting platform, competing with GitHub and GitLab. Bitbucket provides Git repositories, pull request workflows, code review, and built-in CI/CD through Bitbucket Pipelines. A key differentiator is Bitbucket's support for Mercurial (though Git is now the dominant VCS), and its tight integration with Jira for linking commits and branches to issues.

**Trello** is a lightweight kanban and task management tool based on boards, lists, and cards. Acquired by Atlassian in 2017, Trello uses a visual drag-and-drop interface that appeals to non-technical teams, making Atlassian's offerings accessible beyond software developers.

**Atlassian Design System (ADS)** is Atlassian's unified design system used across their cloud products, providing consistent components, patterns, and guidelines for building Atlassian-style interfaces.

## How It Works

Atlassian's products are available in both cloud (hosted by Atlassian) and self-hosted (Data Center) deployment options. The cloud platform operates on a multi-tenant SaaS model, while Data Center allows large enterprises to run Atlassian products on their own infrastructure with high availability and performance tuning.

Integration between Atlassian products is a core part of their value proposition. Jira issues can be linked to Bitbucket commits, branches, and pull requests. Confluence pages can embed live Jira issue trackers. The Atlassian Marketplace offers over 3,000 apps that extend the base functionality with custom fields, reporting, automation, and integrations with third-party tools.

Automation is built into Atlassian products via Atlassian Automation (for cloud) and legacy automation rules in Jira. Teams can automate repetitive tasks like transitioning issues, sending notifications, or auto-assigning work based on triggers.

## Practical Applications

- **Agile project management** — Teams use Jira with Scrum or Kanban to plan sprints, track velocity, and manage backlogs
- **Knowledge management** — Confluence serves as a single source of truth for team documentation, processes, and decisions
- **Source code management** — Bitbucket hosts Git repositories with built-in CI/CD pipelines
- **IT service management** — Jira Service Management provides help desk functionality for IT teams
- **Product management** — Product teams use Jira to track feature requests, roadmap items, and customer feedback
- **Team communication** — While not a chat tool, Atlassian's products integrate with Slack and Teams for notifications

## Examples

A typical Jira issue transition workflow using Jira expressions:

```javascript
// In a Jira automation rule, using Jira expressions
{{#equals issue.status.name "To Do"}}
  {{issue.assignee.displayName}} please pick up {{issue.key}}
{{/equals}}

// Bitbucket Pipelines CI/CD configuration
// bitbucket-pipelines.yml
image: node:18

pipelines:
  default:
    - step:
        name: Build and Test
        script:
          - npm install
          - npm test
        caches:
          - npm
    - step:
        name: Deploy to Staging
        deployment: staging
        script:
          - npm run deploy:staging
        condition:
          branches:
            master: false
            main: true
```

## Related Concepts

- [[Jira]] — Atlassian's flagship issue tracking and project management tool
- [[Confluence]] — Team wiki and knowledge base platform
- [[Bitbucket]] — Git code hosting and CI/CD platform
- [[DevOps]] — The practice Atlassian tools support through integration and automation
- [[Agile]] — The software development methodology Jira was designed to support

## Further Reading

- [Atlassian Products](https://www.atlassian.com/software) — Product overview
- [Atlassian Marketplace](https://marketplace.atlassian.com/) — Apps and integrations
- [Atlassian Design System](https://atlassian.design/) — Design guidelines and components

## Personal Notes

Atlassian's free tier for small teams is one of the best deals in the software industry — you get Jira and Confluence for up to 10 users with no cost. I've used Jira extensively and found it incredibly powerful but sometimes overwhelming due to its flexibility. The key is to resist over-customizing workflows — simple is often better. Bitbucket Pipelines took me some time to appreciate but it's quite convenient for small teams that don't want to set up a separate CI/CD system. The IBM acquisition in 2024 is something to watch — it remains to be seen how IBM will integrate Atlassian's tools into its enterprise portfolio.
