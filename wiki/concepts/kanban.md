---
title: "Kanban"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [kanban, project-management, agile, workflow, continuous-delivery]
---

# Kanban

## Overview

Kanban is a visual workflow management method that originated at Toyota in the 1940s as a scheduling system for lean manufacturing. Originally called "just-in-time manufacturing" and "signaling systems," the approach uses visual cards and columns to represent work items and their progress through stages. The term "Kanban" itself comes from Japanese and translates to "signboard" or "billboard" — reflecting its visual nature.

In software development and project management, Kanban has become one of the most popular agile frameworks, distinguished by its emphasis on continuous flow, WIP (Work In Progress) limits, and evolutionary change rather than large-scale transformation. Unlike Scrum, which operates in fixed-length sprints with defined roles, Kanban is deliberately minimal in its prescriptions — teams can adopt it alongside existing processes without restructuring everything at once.

The Kanban method is codified by the Lean Kanban University and centers on four core principles: visualize the workflow, limit WIP, manage flow, and continuously improve. When implemented effectively, Kanban surfaces bottlenecks, reduces cycle time, and helps teams deliver value more consistently by creating transparency around how work actually moves through a system.

## Key Concepts

**Kanban Board**: The central artifact of any Kanban implementation, a board visualizes workflow stages as columns, with individual work items represented as cards. Teams design their board to reflect their actual process — a software team might have columns like "Backlog," "Ready," "In Progress," "In Review," "QA," and "Done," while a support team might use "New," "Triaged," "In Progress," and "Resolved."

**Work In Progress (WIP) Limits**: Perhaps the most powerful concept in Kanban — each column has a maximum number of cards it can hold at any time. WIP limits are set to match the team's capacity (typically one card per team member per column). When a column hits its WIP limit, team members must complete existing work before pulling new items. This prevents the "too many things in progress at once" problem that dilutes focus and extends cycle time.

**Work Items (Cards)**: Each card represents a unit of work — a user story, bug fix, task, or feature request. Cards carry key information: a clear title, the responsible team member, and often estimates, priority indicators, or links to external resources. The act of writing a card forces clarity about what "done" means for a given piece of work.

**Pull System**: In Kanban, work is pulled by team members when they have capacity, rather than being pushed into the system by a manager or schedule. This self-organizing approach naturally paces the flow of work to match the team's actual throughput. When a column is at its WIP limit, no new work enters until space opens up.

**Cycle Time and Lead Time**: Two critical metrics in Kanban. **Cycle time** measures how long it takes a card to move through the active work stages (from "In Progress" to "Done"). **Lead time** measures the total elapsed time from when a card enters the system to when it's completed. These metrics reveal process health, predict delivery capacity, and surface inefficiencies.

**Classes of Service**: Different types of work may have different handling requirements. A common pattern is to define classes such as "Standard" (regular work), "Expedite" (urgent items that bypass WIP limits), "Intangible" (low-priority background tasks), and "Fixed Date" (work with hard deadlines). Each class has its own policies for prioritization and handling.

## How It Works

A team starts by mapping their existing workflow onto a board — literally drawing or digitally creating columns that represent each stage work passes through. No process redesign is required at this stage; Kanban begins with what the team actually does, not what it should do.

Work items enter the leftmost column (typically "Backlog" or "To Do") and flow rightward as they progress. When a team member starts a task, they physically or digitally move the card to the "In Progress" column. When review or another handoff is needed, the card moves to the next column. The card remains in a column until the next person pulls it.

WIP limits prevent accumulation in any single stage. If the "In Review" column has a limit of three cards and currently holds three, no one can pull a new card into that column — regardless of how urgently new work is needed. This pressure to complete existing work before starting new work is the primary mechanism by which Kanban reduces bottlenecks and improves flow.

Teams conduct regularcadence meetings (often daily for standups and weekly or monthly for service delivery reviews) to examine the board, identify blockers, calculate metrics, and make incremental improvements to the process.

## Practical Applications

**Software Development Teams**: Kanban has become extremely popular among software teams, particularly those practicing continuous delivery. The visual board maps naturally to the software development lifecycle, and WIP limits help prevent the multitasking that degrades code quality and slows delivery.

**DevOps and SRE Teams**: Operations teams use Kanban to manage incident response, feature requests, and technical debt. Classes of service are particularly valuable here — "Expedite" cards for production incidents can bypass normal WIP limits to ensure critical issues get immediate attention.

**Personal Productivity**: The underlying principles of Kanban — visualizing tasks, limiting WIP, focusing on flow — apply at the personal level. Many individuals use simple Kanban-style boards (physical sticky notes or apps like Trello) to manage personal projects and daily work.

**Customer Support**: Support teams track incoming tickets through defined stages, using WIP limits to ensure each team member isn't overwhelmed and that tickets don't languish in any single stage. Lead time metrics help set customer expectations and identify systemic delays.

## Examples

A software team Kanban board configuration:

| Column | WIP Limit | Policy |
|--------|-----------|--------|
| Backlog | ∞ | Prioritized by product owner |
| Ready | 5 | Ready for sprint planning |
| In Progress | 3 | One per developer |
| In Review | 2 | Requires one approval |
| QA | 2 | One per QA engineer |
| Done | ∞ | Archived weekly |

An Expedite class of service policy:

```
Expedite:
- Reserved for production incidents causing customer-facing outages
- Always pulls to In Progress immediately, bypassing all WIP limits
- Maximum 1 active expedite at a time
- Requires immediate acknowledgment (< 15 minutes)
- Daily review of expedite frequency — spikes indicate underlying instability
```

Cycle time calculation and improvement:

```python
# Example: Calculate average cycle time from board history
import datetime

def calculate_cycle_time(done_cards):
    """Calculate average cycle time in days for completed cards."""
    cycle_times = []
    for card in done_cards:
        start = card['started_at']  # When moved to In Progress
        end = card['completed_at']  # When moved to Done
        cycle_times.append((end - start).days)
    
    return sum(cycle_times) / len(cycle_times) if cycle_times else 0

def identify_bottlenecks(board_state):
    """Identify columns where cards spend the most time."""
    bottlenecks = {}
    for col_name, cards in board_state.items():
        if not cards or col_name == 'Done':
            continue
        avg_time = sum(c['wait_time_hours'] for c in cards) / len(cards)
        bottlenecks[col_name] = avg_time
    return sorted(bottlenecks.items(), key=lambda x: x[1], reverse=True)
```

## Related Concepts

- [[Agile Methodology]] - The broader movement Kanban belongs to
- [[Scrum]] - Another popular agile framework with fixed-length sprints
- [[Project Management]] - The discipline of planning and executing work
- [[Continuous Delivery]] - Software delivery practice often paired with Kanban
- [[Workflow]] - The general concept of work progression systems
- [[Lean Manufacturing]] - The manufacturing origin of Kanban principles

## Further Reading

- [Lean Kanban University](https://leankanban.com/)
- *Kanban: Successful Evolutionary Change for Your Technology Business* — David J. Anderson
- [Kanban vs Scrum](https://www.atlassian.com/agile/kanban-vs-scrum)

## Personal Notes

Kanban's appeal is its adaptability — unlike [[Scrum]], which imposes a specific framework of sprints and ceremonies, Kanban lets teams work with their existing process and evolve it incrementally. The WIP limit is the concept I return to most often as a diagnostic tool: if a column keeps hitting its limit, that's a clear signal of a bottleneck that needs attention. I've also found that the visual board alone — even without metrics — dramatically improves team awareness of work in progress and reduces the "can you pick this up?" interruptions because the board makes capacity visible.
