---
title: "Scrum"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agile, project-management, software-development, framework]
---

# Scrum

## Overview

Scrum is an agile framework for developing, delivering, and sustaining complex products, particularly in software development. It emphasizes iterative progress, team collaboration, and continuous improvement through defined roles, ceremonies, and artifacts. Unlike traditional waterfall approaches where work flows sequentially through phases, Scrum embraces uncertainty and allows teams to adapt by working in short, time-boxed iterations called sprints.

Scrum was formalized in the early 1990s by Ken Schwaber and Jeff Sutherland, and it has since become one of the most widely adopted agile frameworks globally. Its core philosophy centers on delivering the highest business value in the shortest time, maintaining transparency, and continuously reflecting on team performance to improve processes.

## Key Concepts

### The Three Pillars

Scrum rests on three foundational pillars that guide all activities:

**Transparency** ensures that all aspects of the process are visible to those responsible for the outcome. This requires common standards and a shared understanding across the team.

**Inspection** involves regularly examining Scrum artifacts and progress toward goals. Teams look for inconsistencies between what was expected and what actually occurred.

**Adaptation** occurs when inspection reveals that processes or products are deviating outside acceptable limits. The team must adjust immediately to minimize further deviation.

### The Five Values

Scrum teams commit to five core values: courage, focus, commitment, respect, and openness. These values drive behaviors and decisions throughout the sprint cycle.

## How It Works

### Sprint Cycle

A sprint is the heart of Scrum, typically lasting 1-4 weeks with 2 weeks being most common. Each sprint begins with Sprint Planning, where the team selects items from the backlog and creates a plan for completing them. Daily standups keep everyone aligned on progress and blockers. The sprint concludes with Sprint Review (demonstrating completed work to stakeholders) and Sprint Retrospective (team reflection on how to improve).

### Scrum Roles

**Product Owner** owns the product backlog and prioritizes work based on business value. This role ensures the team is always working on the most important items.

**Scrum Master** facilitates ceremonies, removes impediments, and ensures the Scrum framework is understood and followed. They serve the team, not control it.

**Development Team** is self-organizing and cross-functional. No titles exist within the team—all members are called developers regardless of specialty.

## Practical Applications

Scrum is used across industries beyond software, including marketing, HR, finance, and manufacturing. It excels when requirements are uncertain, technology is novel, or business conditions change rapidly.

Example organizations using Scrum at scale include Spotify, Amazon, and Salesforce. At Spotify, the "Squad" model is a direct adaptation of Scrum teams working autonomously on features.

## Examples

```python
# Simplified Scrum board representation
class ScrumBoard:
    def __init__(self):
        self.backlog = []
        self.sprint_goal = ""
    
    def add_story(self, title, points, priority):
        story = {
            "title": title,
            "points": points,
            "priority": priority,
            "status": "backlog"
        }
        self.backlog.append(story)
    
    def start_sprint(self, stories, duration_weeks=2):
        self.sprint_goal = f"Sprint: {len(stories)} stories in {duration_weeks} weeks"
        for story in stories:
            story["status"] = "in_progress"
        return self.sprint_goal
```

## Related Concepts

- [[Agile Methodology]] - The broader movement Scrum is part of
- [[Kanban]] - Another agile framework with different emphasis
- [[Product Backlog]] - The prioritized list of work items
- [[Sprint Planning]] - The ceremony starting each sprint

## Further Reading

- "Scrum Guide" by Ken Schwaber and Jeff Sutherland (scrumguides.org)
- "Scrum: The Art of Doing Twice the Work in Half the Time" by Jeff Sutherland

## Personal Notes

Scrum works best when the entire organization supports it, not just the development teams. Common pitfalls include treating sprints as deadlines, ignoring retrospectives, and allowing scope creep mid-sprint. The framework is simple to understand but difficult to master—it requires genuine commitment to transparency and continuous improvement.
