---
title: "Kano Model"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [product-management, customer-satisfaction, usability-engineering, quality]
---

## Overview

The Kano Model is a theory of product development and customer satisfaction developed by Dr. Noriaki Kano in the 1980s. It provides a framework for categorizing product features or service attributes based on how they impact customer satisfaction. The model's insight is that not all features contribute equally to satisfaction—some must be present to avoid dissatisfaction, while others delight customers when present but don't cause dissatisfaction when absent.

The model emerged from Dr. Kano's work studying consumer behavior in Japan, particularly in the food and product industry. He observed that the relationship between feature implementation and customer satisfaction is often non-linear, leading to the development of a two-dimensional model that categorizes attributes based on their emotional impact.

Understanding which category a feature falls into helps product teams prioritize development efforts, allocate resources effectively, and create roadmaps that maximize customer satisfaction gains. The Kano Model is particularly valuable in agile environments where continuous prioritization decisions must be made.

## Key Concepts

The Kano model identifies five categories of product attributes:

**Must-Be (Basic) Attributes** are requirements that customers expect as baseline. When present, they don't increase satisfaction, but when absent, they cause significant dissatisfaction. Examples include a phone's ability to make calls or a car's brakes working properly. These are table-stakes features that must be implemented before any other work begins.

**One-Dimensional (Performance) Attributes** show a linear relationship with satisfaction—the more implemented, the more satisfied customers become. These are typically the metrics that competitors highlight, such as battery life, camera resolution, or processing speed. Product teams should invest in these to gain competitive advantage.

**Attractive (Excitement) Attributes** are unexpected features that delight customers when present but don't cause dissatisfaction when absent. These create differentiation and positive word-of-mouth. Examples include a smartphone's face unlock feature when it first launched, or a software app's intuitive gesture navigation. The challenge is that today's excitement features become tomorrow's must-haves.

**Indifferent Attributes** have no measurable impact on satisfaction regardless of their presence or absence. These might be features that customers never use or don't notice. Resources spent on indifferent attributes are often wasted.

**Reverse Attributes** demonstrate the opposite effect—when present, they cause dissatisfaction; when absent, they can increase satisfaction. These are features that some customers actively dislike, such as mandatory advertising or complex user interfaces.

## How It Works

The Kano model is typically implemented through a survey methodology. Customers are presented with pairs of questions for each feature—one asking about their reaction when the feature is present, and one asking about their reaction when the feature is absent.

The possible responses for each question are typically:
- I like it
- It must be that way
- I am neutral
- I can live with it
- I dislike it

The combination of answers places each feature into one of the five categories. A feature that customers "like" when present but "dislike" when absent is an Attractive attribute. A feature that customers expect ("must be that way") when present but "dislike" when absent is a Must-Be attribute, and so forth.

```
                    Satisfaction
                        ^
                        |
                        |     One-Dimensional
                        |    /         \ Attractive
                        |   /           \
                        |  /             \
                        | /               \
                        |/                 \
    --------------------*-------------------*-----> Implementation
                       /|                 /|
                      / |                / |
                     /  |               /  |
                    /   | Must-Be      /   |
                   /    |            /    |
                  /     |          /     |
                 /      |        /      |
                /       |       |       |
               /        |      |        |
              v         v      v        v
         Dissatisfaction
```

## Practical Applications

The Kano Model is primarily used for:

**Feature Prioritization** - When building products with limited resources, teams must decide what to build first. The model helps identify which features are table-stakes (build immediately), which drive satisfaction (invest heavily), and which can be deprioritized or removed.

**Customer Segmentation** - Different customer segments may categorize the same feature differently. Technical early adopters might find a feature exciting while mainstream users consider it must-have. This insight enables targeted product positioning.

**Competitive Analysis** - Understanding where competitors invest helps identify which attributes are becoming expected (shifting from exciting to must-be) versus which remain differentiation opportunities.

**Roadmap Planning** - The model helps create development roadmaps that progressively add value. Teams might focus first on must-haves, then invest in performance attributes for competitive advantage, while setting aside resources for exploring new attractive attributes.

## Examples

Consider a project management software product:

| Feature | Kano Category | Rationale |
|---------|---------------|-----------|
| Create and edit tasks | Must-Be | Users expect this functionality as baseline |
| Task due date reminders | One-Dimensional | More reminder options = more satisfaction |
| AI-generated task summaries | Attractive | Exciting when present, no impact if absent |
| Color theme selection | Indifferent | Most users don't care about this |
| Forced weekly reporting | Reverse | Causes dissatisfaction despite being potentially useful |

A practical survey question might be:
> "How do you feel if the software automatically sends reminder notifications before task deadlines?"
> - I like it
> - It must be that way
> - I am neutral
> - I can live with it
> - I dislike it

## Related Concepts

- [[Product Management]] - The discipline of guiding product development
- [[Customer Experience]] - The overall customer journey and satisfaction
- [[Design Thinking]] - Human-centered approach to product development
- [[User Research]] - Methods for understanding customer needs
- [[Quality Function Deployment]] - Related methodology for translating customer needs into design
- [[Minimum Viable Product]] - Building with only essential features

## Further Reading

- ["Kano Model" article on MeasuringU](https://measuringu.com/kano-model/)
- ["Understanding Customer Requirements" by Noriaki Kano](https://www.researchgate.net/publication/248406115)
- [Kano Model Templates and Resources](https://kano模型.com/)

## Personal Notes

The biggest mistake teams make with the Kano Model is treating categories as permanent. Attributes naturally migrate over time—yesterday's exciting feature becomes tomorrow's expected requirement. iPhones were once exciting; now their basic functionality is expected. Plan for this migration in your roadmap. Additionally, Kano surveys should be refreshed periodically as customer expectations evolve and competitive landscapes shift. The model works best when combined with quantitative usage data and qualitative customer interviews.
