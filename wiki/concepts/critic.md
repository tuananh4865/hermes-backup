---
title: Critic
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent, roles, multi-agent, evaluation, llm-agents]
---

# Critic

## Overview

In multi-agent AI systems, the critic is a specialized agent role responsible for evaluating the outputs, decisions, or intermediate reasoning of other agents and providing structured feedback. The critic acts as a quality assurance mechanism within agentic systems, enabling iterative refinement and ensuring that agent outputs meet specified criteria, safety constraints, or performance standards.

The critic role emerges naturally from the observation that agents producing complex outputs—code, text, plans, or decisions—benefit from independent evaluation before those outputs are acted upon or finalized. Rather than relying on a single agent's self-assessment, introducing a separate critic agent creates a form of internal oversight that can catch errors, identify logical inconsistencies, and push back against flawed reasoning. This architectural pattern draws from human collaborative workflows where writers, engineers, and decision-makers benefit from peer review.

In practical terms, a critic agent receives information about a task, the agent's proposed solution or output, and evaluation criteria. It then produces structured feedback that may include identifying specific errors, suggesting improvements, rating quality along various dimensions, or recommending rejection and revision. This feedback can either be presented to a human supervisor for final decisions or fed back directly to the original agent for self-correction.

## Key Concepts

**Evaluation Criteria** are the specific dimensions along which the critic assesses output quality. These may include correctness (does the output achieve the stated goal?), safety (does the output introduce risks or violate constraints?), coherence (is the output internally consistent?), and efficiency (is the approach optimal?).

**Structured Feedback** refers to criticism formatted in a way that enables constructive action. Rather than vague assessments, structured feedback identifies specific issues, provides evidence or reasoning for the criticism, and often suggests concrete improvements.

**Iterative Refinement** is the process of cycles between agent output, critic evaluation, and agent revision. Each iteration should produce measurably improved output until quality thresholds are met.

**Calibration** in the critic context refers to ensuring that the critic's assessments accurately reflect ground truth or human judgment. A poorly calibrated critic may be too lenient, too harsh, or inconsistent in its evaluations.

**Critic-Agent Alignment** is the challenge of ensuring the critic's evaluation criteria align with the actual goals and values of the broader system. Misaligned critics may optimize for the wrong qualities or introduce subtle biases.

## How It Works

The typical workflow involving a critic agent follows a loop pattern. A primary agent—such as a [[planner]] or [[researcher]]—produces an initial output. This output, along with the original task specification and evaluation criteria, is passed to the critic agent. The critic analyzes the submission and returns structured feedback.

Critic implementations vary in sophistication. Simple critics may use [[large-language-models]] with specific prompting to evaluate against predefined criteria. More advanced critics may have access to tools for testing code, verifying factual claims, or running simulations. Some critics maintain state across multiple evaluation rounds to track improvement over iterations.

The effectiveness of a critic depends heavily on the quality of its instructions. Well-designed critics receive detailed rubrics specifying what constitutes acceptable output, examples of good and poor responses, and guidance on how to handle edge cases. Without clear evaluation criteria, critics tend to be inconsistent or overly subjective.

## Practical Applications

In code generation pipelines, a critic agent reviews generated code for correctness, security vulnerabilities, adherence to coding standards, and efficiency before the code is accepted. This catches bugs and security issues early in the development process.

In document drafting systems, critic agents evaluate generated text for clarity, factual accuracy, tone consistency, and alignment with brand guidelines. This enables automated quality control without human review for first-pass drafts.

For [[multi-agent-systems]] performing complex tasks, critics provide oversight at key decision points. A strategic planning system might use critics to evaluate whether proposed plans meet safety constraints before execution begins.

In safety-critical applications, critics serve as guardrails that can halt or reject agent actions that violate safety boundaries. A critic monitoring an autonomous system's decision pipeline can prevent dangerous actions even if other agents have proposed them.

## Examples

```python
class CriticAgent:
    """Simple critic agent for evaluating agent outputs."""
    
    def __init__(self, llm, evaluation_criteria):
        self.llm = llm
        self.criteria = evaluation_criteria
    
    def evaluate(self, task, agent_output):
        prompt = f"""Evaluate the following agent output against these criteria:
        
        Task: {task}
        
        Output: {agent_output}
        
        Evaluation Criteria:
        {self._format_criteria()}
        
        Provide your evaluation in this format:
        1. PASS/FAIL for each criterion
        2. Specific issues identified (if any)
        3. Suggested improvements
        4. Overall recommendation: ACCEPT / REVISE / REJECT
        """
        response = self.llm.generate(prompt)
        return self._parse_response(response)
    
    def _format_criteria(self):
        return "\n".join(
            f"- {c['name']}: {c['description']}" 
            for c in self.criteria
        )
```

## Related Concepts

- [[planner]] — Agent role for planning and task decomposition
- [[researcher]] — Agent role for information gathering and analysis
- [[multi-agent-systems]] — Systems composed of multiple specialized agents
- [[agent-roles]] — Overview of common agent roles and responsibilities
- [[prompt-engineering]] — Techniques for instructing critic agents effectively

## Further Reading

- Wu, J., et al. (2023). "CRITIC: Large Language Models Can Self-Correct with Web Search"
- Pan, L., et al. (2024). "The Critic Actor Framework for Multi-Agent Systems"
- OpenAI (2024). "Implementing Multi-Agent Critic Systems in Production"

## Personal Notes

The critic pattern is deceptively simple but requires careful design to avoid becoming a bottleneck. Critics that are too strict prevent legitimate agent creativity; those too lenient fail to catch genuine problems. Finding the right calibration often requires iterative refinement of the critic's instructions based on observed behavior. I've found that giving critics access to execution environments—allowing them to test code, verify links, or run queries—significantly improves evaluation quality.
