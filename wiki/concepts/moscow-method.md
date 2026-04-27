---
title: "Moscow Method"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [requirements, prioritization, project-management, agile]
---

# Moscow Method

The MoSCoW method is a prioritization technique used in project management, requirements engineering, and software development to categorize items by their importance. The acronym stands for Must have, Should have, Could have, and Won't have—each representing a different priority tier that helps teams focus on what matters most when resources are constrained.

## Overview

Every project faces the reality of limited time, budget, and people. When scope creeps or deadlines tighten, teams need a principled way to cut features without losing sight of what truly matters. MoSCoW provides this by forcing explicit categorization of requirements into four buckets.

The technique was popularized by Dai Clegg in the late 1990s during his work at Oracle, and gained wider adoption through the Dynamic Systems Development Method (DSDM), which emphasized timeboxing and iterative delivery. Today it appears in agile retrospectives, sprint planning, product roadmaps, and enterprise architecture reviews.

The "Won't have this time" category is often overlooked but critically important. Explicitly acknowledging that certain features are deliberately excluded prevents scope creep and focuses discussion on the prioritized items.

## The Four Categories

**Must Have (Critical)**

Must-have requirements are non-negotiable. Without them, the product cannot ship or the project is considered a failure. In an MVP (Minimum Viable Product), only must-haves are included. These items typically represent core functionality, regulatory requirements, or features that address safety concerns.

Examples: For an e-commerce checkout, "complete purchase" is a must-have. For a medical device, "prevent incorrect dosage" is a must-have. For a mobile app, "crash on launch" fixes are must-haves.

A common heuristic: if you removed this requirement, would the product be fundamentally broken or unusable? If yes, it's a must-have.

**Should Have (Important)**

Should-have requirements are significant and valuable, but the product could function without them. They represent important functionality that improves the user experience or addresses meaningful business needs, but workarounds exist or the impact is less severe than must-haves.

These are typically included if time permits after must-haves are complete. In a timebox, should-haves might be moved to a future iteration if they prove too complex.

Examples: Email receipts (SMS receipts are acceptable), Dark mode (light mode works fine), Social sharing (direct links work).

**Could Have (Desirable)**

Could-have requirements are nice-to-have features that enhance the product but aren't essential. They often improve user satisfaction or provide competitive differentiation, but users would still be satisfied without them.

These are the first candidates for deferral when scope needs trimming. They typically represent 20% of effort for 80% of perceived value—the remaining 20% of value comes from should and must haves.

Examples: Animated transitions, Export to PDF, Two-factor authentication (if passwords alone are acceptable).

**Won't Have (Out of Scope)**

The won't-have category explicitly documents features that the team has decided not to address in the current iteration or timeframe. This is not a negative classification—it represents deliberate choices made with stakeholder agreement.

Common reasons for Won't Have: Out of scope for this phase, Requires technology not yet available, Addressing would compromise other priorities, No stakeholder demand.

Documenting these prevents future debates about "why isn't X implemented?" and reinforces team focus.

## Application in Agile Development

In sprint planning, the MoSCoW technique helps the team and product owner agree on what's essential for the sprint versus what would be nice to include.

A typical sprint might target:
- 60% Must Have items
- 20% Should Have items
- 20% Could Have items
- Won't Have explicitly noted

The percentages aren't rigid rules but guidelines for realistic expectation-setting.

In user story mapping, MoSCoW helps prioritize the "walking skeleton" of the product—the minimal set of features that demonstrates the core value proposition.

## Limitations

MoSCoW can be misused when stakeholders mark everything as "Must Have," defeating the purpose of prioritization. Facilitators must push for honest categorization and guide difficult conversations about trade-offs.

The technique doesn't capture the relative importance within categories. Two must-haves might have very different business impact, but MoSCoW treats them equally. Teams sometimes combine it with weighted scoring ( Effort vs. Impact matrices) for finer granularity.

The method also lacks temporal dimension. A Should Have for Q1 might become a Must Have for Q2 if a competitor ships it first.

## Code Example: Python Implementation

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class Priority(Enum):
    MUST = "Must Have"
    SHOULD = "Should Have"
    COULD = "Could Have"
    WONT = "Won't Have"

@dataclass
class Requirement:
    id: str
    title: str
    description: str
    priority: Priority
    effort_hours: float

def prioritize_backlog(requirements: List[Requirement]) -> dict:
    """Group requirements by MoSCoW priority."""
    buckets = {
        Priority.MUST: [],
        Priority.SHOULD: [],
        Priority.COULD: [],
        Priority.WONT: []
    }
    for req in requirements:
        buckets[req.priority].append(req)
    return buckets

def estimate_velocity(buckets: dict, velocity: float) -> dict:
    """Estimate how much can be delivered in current sprint."""
    must_total = sum(r.effort_hours for r in buckets[Priority.MUST])
    should_total = sum(r.effort_hours for r in buckets[Priority.SHOULD])
    
    if must_total > velocity:
        return {"status": "OVERCAPACITY", "deficit": must_total - velocity}
    
    remaining = velocity - must_total
    can_include_should = min(should_total, remaining) / should_total if should_total else 0
    
    return {
        "status": "FEASIBLE",
        "must_hours": must_total,
        "should_coverage": f"{can_include_should:.0%}"
    }
```

## Related Concepts

- [[Requirements Engineering]] - The discipline of gathering and specifying requirements
- [[Prioritization]] - Broad category of techniques for ranking work
- [[Agile Methodology]] - Development approach where MoSCoW is commonly used
- [[MVP]] - Minimum Viable Product concept aligned with Must-Haves
- [[User Story Mapping]] - Technique often combined with MoSCoW

## Further Reading

- "Agile Estimating and Planning" by Mike Cohn
- "User Story Mapping" by Jeff Patton
- DSDM Consortium resources on MoSCoW prioritization

## Personal Notes

MoSCoW's simplicity is both its strength and weakness. Stakeholders grasp it instantly, which makes it useful for aligning expectations. However, I've seen it become meaningless when everything gets labeled "Must Have" to avoid difficult conversations. The facilitator's job is to push back—not everything is equally critical. The Won't Have bucket is particularly valuable because it forces explicit scope decisions that teams often avoid.
