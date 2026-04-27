---
title: Researcher
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [agent, roles, multi-agent, research, autonomous-ai, information-gathering]
---

# Researcher

In multi-agent systems, a Researcher agent is responsible for gathering, analyzing, and synthesizing information to support task completion. The researcher acts as an intelligent information retrieval and analysis system, capable of exploring topics, evaluating sources, and producing structured findings. This role is essential in agentic workflows where autonomous systems need to make informed decisions based on comprehensive research.

## Key Concepts

**Information Gathering** — Systematically collecting data from multiple sources including web search, document analysis, database queries, and API calls. The researcher must know when to dig deeper and when to synthesize what's been found.

**Source Evaluation** — Assessing information quality, credibility, and relevance. Researchers distinguish primary from secondary sources, identify bias, and verify facts across multiple sources.

**Analysis and Synthesis** — Transforming raw information into actionable insights. This includes identifying patterns, comparing perspectives, and drawing conclusions from incomplete data.

**Structured Output** — Presenting findings in formats useful for downstream agents—whether concise summaries, detailed reports, or structured data for further processing.

## How It Works

A researcher agent typically operates within a larger workflow:

```markdown
Researcher Agent Workflow:
1. Receive research query or topic from orchestrator
2. Break down into search queries and sub-topics
3. Execute parallel searches across multiple sources
4. Filter and prioritize results by relevance
5. Extract key information from sources
6. Synthesize findings into coherent response
7. Identify gaps requiring additional research
8. Present structured findings with citations
9. Await follow-up queries or next task
```

### Example Implementation

```python
class ResearcherAgent:
    def __init__(self, search_tool, llm):
        self.search = search_tool
        self.llm = llm
    
    def research(self, query, depth="standard"):
        sub_queries = self.decompose_query(query)
        
        # Parallel search execution
        results = self.search.bulk(sub_queries)
        
        # Extract and rank by relevance
        findings = self.extract_findings(results)
        
        # Synthesize into coherent response
        synthesis = self.synthesize(findings, query)
        
        return synthesis
    
    def decompose_query(self, query):
        # Use LLM to break complex query into sub-queries
        return self.llm.generate_search_queries(query)
    
    def synthesize(self, findings, original_query):
        prompt = f"""
        Based on these findings about '{original_query}':
        {findings}
        
        Provide a structured synthesis with:
        - Key facts
        - Different perspectives
        - Knowledge gaps
        - Confidence level
        """
        return self.llm.complete(prompt)
```

## Practical Applications

**Deep Research Tasks** — Comprehensive reports on technical topics, market analysis, competitive research. Researchers can explore topics far faster than manual searching.

**Fact-Checking** — Verify claims against authoritative sources. Critical for AI systems where hallucinations are a concern.

**Technical Investigation** — Debugging complex issues by gathering logs, documentation, and similar issues from across the internet.

**Knowledge Expansion** — Proactively researching topics to fill gaps in an agent's knowledge base.

## Related Concepts

- [[multi-agent-systems]] — How multiple agents collaborate
- [[planner]] — Agent that coordinates task breakdown and delegation
- [[agent-architecture]] — Overall system design for AI agents
- [[autonomous-ai]] — Self-directed AI systems
- [[tool-use]] — How agents interact with external systems

## Further Reading

- AI Agent Architectures (various blog posts)
- Multi-Agent Systems literature
- Retrieval-Augmented Generation (RAG) for agentic systems

## Personal Notes

In practice, researcher agents are only as good as their tools. A researcher with web search, code execution, and document access is far more capable than one limited to a single source. The quality of synthesis also heavily depends on the underlying LLM's reasoning abilities.
