---
title: "Agile"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [software-development, project-management, methodology, sprint, scrum]
---

# Agile

## Overview

Agile is an iterative approach to software development that emphasizes flexibility, collaboration, and rapid delivery of working software. Rather than planning everything upfront and executing a fixed plan, Agile teams work in short cycles called sprints (typically 1-4 weeks), continuously adapting their plans based on feedback and changing requirements. The philosophy was formalized in 2001 when seventeen software developers published the Agile Manifesto, which values individuals and interactions over processes and tools, working software over comprehensive documentation, customer collaboration over contract negotiation, and responding to change over following a plan.

Agile represents a fundamental shift from traditional "waterfall" development, where each phase (requirements, design, implementation, testing, deployment) must be completed before moving to the next. Waterfall's rigidity often caused projects to fail when requirements changed or unforeseen issues emerged. Agile embraces change as inevitable, building it into the process through regular feedback loops and adaptive planning.

## Key Concepts

### The Agile Manifesto Principles

The manifesto includes twelve principles that guide Agile implementation:

1. Satisfy the customer through early and continuous delivery of valuable software
2. Welcome changing requirements, even late in development
3. Deliver working software frequently (weeks rather than months)
4. Business people and developers must work together daily
5. Build projects around motivated individuals, give them environment and support
6. Face-to-face conversation is the most efficient communication method
7. Working software is the primary measure of progress
8. Maintain a sustainable pace indefinitely
9. Continuous attention to technical excellence and good design
10. Simplicity—maximizing work not done—is essential
11. Self-organizing teams produce the best designs and requirements
12. Regular reflection and adjustment to increase effectiveness

### Sprint Structure

A sprint is a time-boxed iteration (usually 2 weeks) with a consistent duration throughout development. Each sprint begins with planning (selecting and detailing work) and ends with review (demonstrating what was built) and retrospective (examining how the team worked). This cadence creates rhythm and forces incremental delivery rather than "big bang" releases.

## How It Works

Agile teams maintain a backlog of work items—user stories, bug fixes, technical improvements—prioritized by business value. During sprint planning, the team selects items they believe they can complete in the upcoming sprint based on their velocity (historical throughput). Daily standup meetings keep everyone aligned on progress and blockers.

At sprint end, teams deliver a potentially shippable product increment. This doesn't necessarily mean deploying to production—it means having code in a deployable state with appropriate tests. The increment is demonstrated to stakeholders, feedback is collected, and the product backlog is refined based on that feedback. Then the next sprint begins.

```python
# Example: Simple sprint velocity calculation
def calculate_velocity(sprint_history):
    """Calculate average velocity from completed sprints."""
    completed_points = [sprint.completed_story_points for sprint in sprint_history]
    return sum(completed_points) / len(completed_points) if completed_points else 0

# Forecasting next sprint capacity
def forecast_sprint(user_stories, velocity, sprint_capacity=None):
    capacity = sprint_capacity or velocity
    selected = []
    total_points = 0
    for story in sorted(user_stories, key=lambda s: s.priority):
        if total_points + story.points <= capacity:
            selected.append(story)
            total_points += story.points
    return selected, total_points
```

## Practical Applications

Agile shines in environments where requirements are unclear or likely to change—typical of startups, product companies, and innovation teams. It's less suited for projects with fixed requirements and regulatory constraints (infrastructure, compliance-driven software) where changing scope mid-stream is impractical.

**Software Product Development**: Agile is the dominant methodology for SaaS, mobile apps, and consumer software where market feedback drives feature prioritization.

**Innovation and R&D**: Teams exploring new domains use Agile's inspect-and-adapt cycles to validate assumptions quickly and pivot when needed.

**Consulting and Custom Development**: Agencies use Agile to collaborate closely with clients, reducing the risk of building the wrong thing.

## Examples

A practical Agile workflow for a web application feature:

1. **Sprint Planning**: "As a user, I want to reset my password via email" is selected (3 story points)
2. **Daily Standup**: Developer mentions she's working on email template, blocker: needs SMTP credentials
3. **Development**: Implement password reset endpoint, generate secure token, send email
4. **Code Review**: Teammate reviews PR, suggests adding rate limiting
5. **Sprint Review**: Product owner sees working feature, requests adding SMS option
6. **Retrospective**: Team notes email service integration took longer than expected, decides to create spike stories for unknowns

## Related Concepts

- [[Scrum]] - A specific Agile framework with defined roles and ceremonies
- [[Kanban]] - Another Agile method focusing on continuous flow and visual management
- [[User Stories]] - Brief requirements descriptions used in Agile planning
- [[Sprint]] - The time-boxed iteration in which Agile work occurs
- [[Continuous Integration]] - Practice of merging code frequently, complementary to Agile
- [[DevOps]] - Cultural movement bridging development and operations, often paired with Agile

## Further Reading

- [Agile Manifesto](https://agilemanifesto.org/) - Original manifesto and principles
- [Scrum Guide](https://www.scrumguides.org/) - Definitive guide to the Scrum framework
- [Agile Alliance](https://www.agilealliance.org/) - Resources and guidance for Agile practitioners

## Personal Notes

After working with multiple teams transitioning to Agile, the biggest failure mode I've seen is cargo-culting ceremonies without embracing the underlying mindset. Sprints don't create agility—genuine willingness to change based on feedback does. Also, story point estimation often becomes politicized; focusing on cycle time instead can be more honest and actionable.
