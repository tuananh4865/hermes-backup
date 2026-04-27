---
title: "Agile Methodology"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-development, project-management, methodology, iterative-development]
---

# Agile Methodology

## Overview

Agile is a family of iterative software development methodologies that prioritize adaptive planning, continuous delivery, collaborative decision-making, and rapid response to change. The [[agile-manifesto]] (formally the Manifesto for Agile Software Development) was created in 2001 when seventeen software developers gathered at a ski resort in Utah to discuss lightweight development approaches that could counterbalance what they saw as overly bureaucratic and rigid traditional methods.

Rather than committing to extensive upfront requirements and design, agile methodologies embrace short, time-boxed iterations called "sprints" or "iterations" typically lasting one to four weeks. Each iteration produces a potentially shippable product increment with functional software. Teams continuously reassess priorities based on stakeholder feedback and changing market conditions, allowing course corrections throughout the development lifecycle rather than discovering major problems at the end.

The four core values of the Agile Manifesto prioritize individuals and interactions over processes and tools, working software over comprehensive documentation, customer collaboration over contract negotiation, and responding to change over following a rigid plan. These values are not absolute—processes, documentation, contracts, and plans all have their place—but they should not supersede human collaboration and adaptive delivery of value.

## Key Concepts

**Scrum** is the most widely adopted agile framework, defining specific roles (Product Owner, Scrum Master, Development Team), ceremonies (Sprint Planning, Daily Standup, Sprint Review, Sprint Retrospective), and artifacts (Product Backlog, Sprint Backlog, Increment). Scrum uses fixed-length sprints with defined outputs and roles responsible for process enforcement.

**Kanban** (originally developed at Toyota for manufacturing) applies lean thinking to knowledge work through visual boards showing work items in columns (To Do, In Progress, Done), limiting work-in-progress at each stage, and measuring lead/cycle times. Unlike Scrum's time-boxed sprints, Kanban flows work continuously and can accommodate changing priorities without sprint boundaries.

**Extreme Programming (XP)** emphasizes technical excellence through practices like pair programming, test-driven development (TDD), continuous integration, refactoring, and short release cycles. XP places heavy emphasis on customer satisfaction through continuous delivery of high-quality software.

**Sprint** is a time-boxed iteration (typically 2 weeks) during which a cross-functional team works to complete a set of items from the product backlog. At the sprint's end, the team demonstrates working software in a Sprint Review and reflects on improvements in a Retrospective.

**Product Backlog** is an ordered list of everything known to be needed in the product: features, bug fixes, technical debt, and non-functional requirements. The Product Owner continuously refines and re-prioritizes the backlog based on stakeholder input, business value, and dependencies.

## How It Works

The agile lifecycle begins with a Product Owner creating and maintaining a prioritized backlog of user stories and requirements. Before each sprint, the team selects items they believe they can complete during the iteration based on their measured velocity. Sprint planning establishes a shared understanding of what "done" means for each item.

During the sprint, daily standup meetings keep everyone synchronized. Team members share what they accomplished yesterday, what they plan to do today, and any blockers requiring assistance. The Scrum Master facilitates these meetings and works to remove obstacles that impede the team's progress.

The Sprint Review demonstrates completed work to stakeholders, gathering feedback that informs backlog refinement. The Sprint Retrospective creates a safe space for the team to discuss what went well, what could improve, and what actions they will take in the next sprint. These feedback loops enable continuous process improvement.

Scrum defines clear requirements for "done"—an increment must be in a usable state meeting the team's quality bar, typically meaning code is written, tested, integrated, and documented. This definition ensures each sprint produces genuinely useful value rather than partial work that accumulates technical debt.

## Practical Applications

1. **Software Product Development**: Agile excels when requirements are uncertain or evolving, allowing teams to deliver value incrementally while learning from real users.

2. **Startup Environments**: Limited runway and need for market validation make agile's fast feedback cycles valuable for pivoting based on customer reactions.

3. **Large-Scale IT Operations**: Applying agile to IT service management through frameworks like ITIL's agile integration enables faster response to business demands.

4. **Research and Development**: Projects with high uncertainty benefit from agile's iterative hypothesis-testing approach rather than big upfront planning.

```bash
# Example: Simple Kanban board tracking with CLI tools
# Create a kanban board file: kanban.md
# To Do: [User Authentication] [Payment Integration]
# In Progress: [API Design]
# Done: [Database Schema] [Project Setup]
```

## Examples

**Spotify's Squad Model**: Spotify organized engineering around autonomous "squads" (small cross-functional teams), each owning a specific service or feature area. Squads group into "tribes" (chapters) for career development and "guilds" (communities of interest) for knowledge sharing. This scaling pattern adapts agile principles to larger organizations while maintaining team autonomy.

**SAFe (Scaled Agile Framework)**: Large enterprises use SAFe to coordinate multiple agile teams working on interdependent deliverables. SAFe defines layers (Team, Program, Large Solution, Portfolio) with corresponding planning and synchronization ceremonies.

## Related Concepts

- [[Scrum]] - Popular agile framework with defined roles and ceremonies
- [[Kanban]] - Flow-based agile method with visual work management
- [[Sprint Planning]] - Iteration planning ceremony
- [[Product Backlog]] - Prioritized requirements repository
- [[Standup Meeting]] - Daily synchronization practice
- [[Retrospective]] - Team improvement ceremony
- [[User Stories]] - Agile requirements format
- [[Velocity Tracking]] - Measuring team throughput

## Further Reading

- Agile Manifesto (2001) - original manifesto and principles
- "Scrum Guide" by Schwaber & Sutherland - definitive Scrum specification
- "Agile Estimating and Planning" by Mike Cohn
- "Accelerate" by Nicole Forsgren - research on high-performing agile organizations

## Personal Notes

Agile's popularity sometimes leads to cargo cult adoption where teams follow ceremonies mechanically without understanding underlying principles. True agility requires psychological safety, trust, and willingness to experiment with processes. The biggest agile failures I've witnessed came from organizations that adopted sprint ceremonies but resisted the mindset shift toward customer collaboration and embracing change.
