---
title: "Deep Research — Multi-Source Research Pipeline"
created: 2026-04-23
updated: 2026-04-23
type: concept
tags: [research, ai_agents, workflow, LLM, deep_dive]
---

# Deep Research — Multi-Source Research Pipeline

## Summary
This concept outlines a structured deep research workflow designed to maximize the quality and breadth of information gathered for complex topics, particularly in the AI and developer space. The core principle mandates collecting 15 to 50+ results before synthesis begins, ensuring high source legitimacy. It defines a multi-tool search chain and prioritizes specific high-value research topics such as AI agents, Local LLMs, and AI business models.

## Key Insights
- **Minimum Result Threshold:** Every research task must yield at least 15 search results before any content synthesis or reporting is performed.
- **Mandatory Search Chain:** The primary pipeline utilizes three tools (`ddgs`, `mcp_MiniMax_web_search`, and `SearxNG`) to ensure comprehensive coverage, with specific limitations on banned tools (e.g., Tavily).
- **Topic Prioritization:** Research efforts should be focused on high-demand areas: AI agents, Local LLM implementations (Apple Silicon MLX), developer workflows (vibe coding, solo dev), and AI business strategies.

## Analysis
The workflow emphasizes methodological rigor over speed, establishing strict quality thresholds for both result volume and source legitimacy. Web sources must be official documentation, research papers, or reputable media (e.g., Forbes, Arxiv), while social sources are limited to industry experts and core maintainers to ensure credibility. This approach mitigates the risk of synthesizing low-quality, clickbait content.

The operational status section details a critical update regarding search tool reliability. It highlights that autonomous execution often fails with social search tools (`last30days`) due to TTY/subprocess limitations, necessitating their use only in interactive sessions. The primary reliable chain consists of `mcp_MiniMax_web_search` and `ddgs`, supplemented by `SearxNG`.

For content extraction from GitHub repositories (gists, READMEs), the workflow recommends using specific `curl` commands as an excellent alternative to standard search tools, bypassing potential API or search engine blocks. This layered approach ensures that regardless of external platform limitations, critical technical and business data can be successfully collected.

## Related
- [[AI Agent Development]]
- [[Local LLM Setup (Apple Silicon MLX)]
- [[LLM Reasoning Techniques]]
- [[Developer Workflow Automation]]