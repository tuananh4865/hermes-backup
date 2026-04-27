---
title: "Research: Hermes Agent Self-Correction + Context Budgeting"
created: 2026-04-15
updated: 2026-04-15
type: concept
tags: [auto-filled]
---

# Research: Hermes Agent Self-Correction + Context Budgeting

**Date:** 2026-04-14
**Topic:** Implement Claude Code patterns in Hermes Agent
**Status:** Complete

## Research Summary

### Key Patterns from Claude Code Leak

#### 1. Self-Correction Loop

**Pattern:** Plan → Execute → Verify → Fix → Done

**Best Practice (from Reflexion paper):**
- Agent critiques its own reasoning
- Identifies failures
- Iteratively improves without human help

**Implementation Options:**

| Pattern | Complexity | Effect |
|---------|------------|--------|
| Self-critique | Low | Agent reviews own output |
| Tool-level retry | Medium | Tool signals failure, agent retries |
| Tree-of-thought | High | Multiple paths, verify each |

#### 2. Context Budgeting

**Claude Code approach (from MindStudio article):**
- Hard token limits enforced
- Auto-compact before context fills
- Pre-execution budget checks
- Hierarchical summarization

**Token budget breakdown (Claude Code ~180K effective):**
```
Task context:     ~80K (45%)
Related code:     ~50K (28%)
Tool definitions:  ~20K (11%)
History/summaries:~20K (11%)
Buffer:           ~10K (5%)
```

**5 Patterns to constrain context (AugmentCode):**
1. Selective context inclusion
2. Hierarchical summarization
3. Pre-execution budget check
4. Tool schema optimization
5. Conversation pruning

#### 3. Verification Layer

**Key insight from TowardsAI:**
```
The defining failure mode in production agents: NO VERIFICATION
The fix: Verification layer - not better model
```

**Types of verification:**
- Output format verification
- Tool call verification
- State consistency verification
- End-to-end result verification

---

## Implementation Strategy

### For Hermes Agent

**Where to implement:**
1. SOUL.md → Add self-correction guidance
2. Skills → Create self-verify skill
3. Scripts → Create context budget tracker
4. run_agent.py → Already has compressor (check if enough)

### Priority

1. **Self-correction** — Most impactful, easiest to add
2. **Context budgeting** — Already exists in compressor
3. **Verification layer** — New skill needed

---

## Sources

- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- [AI Agent Self-Improvement: Reflection Loops](https://www.buildmvpfast.com/blog/ai-agent-self-improvement-recursive-accuracy-production-2026)
- [How Multi-Agent Self-Verification Actually Works](https://pub.towardsai.net/how-multi-agent-self-verification-actually-works-and-why-it-changes-everything-for-production-ai-71923df63d01)
- [AI Agent Token Budget Management: Claude Code](https://www.mindstudio.ai/blog/ai-agent-token-budget-management-claude-code/)
- [AI Agent Loop: Token Costs and Context Constraints](https://www.augmentcode.com/guides/ai-agent-loop-token-cost-context-constraints)
- [Effective Context Engineering for AI Agents - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
