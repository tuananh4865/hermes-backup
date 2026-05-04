# Self-Improving AI Agent Frameworks (2026)

## Reflexio — reflexio.ai
- **What**: AI agent self-improvement harness that learns from real user interactions
- **Benchmark**: −81% planning steps, −72% tokens on Hermes running minimax/MiniMax-M2.7 (GDPVal benchmark)
- **Key insight**: Transforms user corrections into behavioral playbooks; captures successful execution paths for reuse
- **Transfer learning**: One user teaches → all users benefit
- **Integrations**: Claude Code, LangChain, OpenClaw
- **Status**: 137 stars, active development

## AgentFactory — arXiv 2603.18000
- **What**: Sub-agents stored as executable Python modules (not text summaries)
- **Key insight**: Code-based skill storage = deterministic re-execution in complex scenarios
- **Three-phase lifecycle**: Decompose → Generate sub-agents → Save to persistent skill library
- **Feedback loop**: Failed sub-agent → analyze → modify → validate → promote
- **Cross-system portability**: Mature sub-agents are standalone Python modules

## HyperAgents (DGM-H) — Meta, March 2026
- **What**: Meta-mechanism unified with task mechanism — system can improve how it improves
- **Key insight**: Solves infinite regress problem of layered meta-architectures
- **Archive-based exploration**: Preserves historically successful agent variants as "stepping stones"
- **Emergent capabilities**: Autonomously wrote memory, performance tracking, resource planning into own codebase
- **Cross-domain transfer**: Transferred HyperAgent scored 0.630 on IMO-GradingBench vs DGM baseline 0.0

## Miguel — github.com/soulfir/miguel
- **What**: Self-improving agent that reads/modifies/extends own source code in Docker
- **Started**: 10 seed capabilities → now 22 capabilities
- **Safety**: Validates (syntax, imports, schema) before writing; automatic rollback on failure
- **Architecture**: Agno Team with context-aware delegation to sub-agents (Coder, Researcher, Analyst)
- **Self-modification**: Rewrites own prompts, creates new tools, auto-registers them
- **Context awareness**: Monitors context usage, auto-compacts when running low

---

## Comparison Table

| Framework | Self-Modifies Code | Benchmark | Transfer | Status |
|-----------|-------------------|-----------|---------|--------|
| Reflexio | No (playbooks) | −81% steps | Yes | 137 stars |
| AgentFactory | Sub-agents only | N/A | Portable Python | arXiv |
| HyperAgents | Yes (meta too) | 0.630 IMO | Yes | Research |
| Miguel | Yes | N/A | Docker | 22 caps |

## Relevance to Hermes
- Reflexio directly benchmarks on MiniMax-M2.7 — most immediately applicable
- AgentFactory pattern (executable sub-agents) could improve skill system
- Miguel's Docker sandbox + validation = safe self-modification model
