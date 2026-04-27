---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 automation (extracted)
  - 🔗 multi-agent-orchestration (extracted)
relationship_count: 2
---

# Autonomous Research Suite

Integration of 3 research frameworks:
- **last30days-skill**: Multi-source social search (Reddit, X, HN, YouTube, Polymarket)
- **Agent-Reach**: Internet access for AI agents (Twitter, Reddit, GitHub, Web)
- **AutoResearchClaw**: Full autonomous research pipeline (23 stages)

## Quick Install

```bash
# 1. Clone repos
git clone https://github.com/mvanhorn/last30days-skill.git /tmp/last30days-skill
git clone https://github.com/Panniantong/Agent-Reach.git /tmp/agent-reach
git clone https://github.com/aiming-lab/AutoResearchClaw.git /tmp/auto-research-claw

# 2. Install dependencies
pip3 install -e /tmp/agent-reach
pip3 install -e /tmp/auto-research-claw

# 3. Setup last30days
mkdir -p ~/.config/last30days
echo "SETUP_COMPLETE=true" > ~/.config/last30days/.env
```

## Architecture

```
autonomous_deep_research.py (main orchestrator)
├── web_search tool (MCP) — primary search
├── last30days concepts — social search patterns
├── Agent-Reach patterns — platform access
└── AutoResearchClaw phases — research pipeline
```

## Usage

```bash
# Run autonomous deep research
python3 ~/wiki/scripts/autonomous_deep_research.py

# Run with specific topic
python3 ~/wiki/scripts/autonomous_deep_research.py --topic "AI agents 2025"
```

## Research Workflow

1. Generate 20+ queries across categories
2. Execute web_search (limit=15 per query)
3. Score sources by credibility
4. Extract content from top 10 URLs
5. Compile structured report
6. Save to wiki with frontmatter

## Source Credibility Scoring

| Source | Score |
|--------|-------|
| arXiv | 95 |
| GitHub | 85 |
| Microsoft/Google/OpenAI | 90 |
| MIT/Stanford/Berkeley | 90 |
| Tech News | 70 |
| Reddit | 55 |
| X/Twitter | 45 |

## Quality Standards

- 15+ sources per search query
- 3 research rounds
- 20+ total queries
- Extract full content from top 10
- Proper citations and attributions

## Related Concepts

- [[automation]] — Automation patterns
- [[multi-agent-orchestration]] — Multi-agent coordination
