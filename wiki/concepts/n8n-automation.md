---
title: "N8N Automation"
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [automation, n8n, workflow, ai-agents, no-code]
related:
  - [[workflow-automation]]
  - [[ai-agents]]
  - [[local-llm-agents]]
---

# N8N Automation

## Overview

[N8N](https://n8n.io) is an open-source workflow automation platform ("fair-code" model) combining AI capabilities with business process automation. 400+ integrations, self-hostable, with native AI agent nodes.

**Why n8n matters:** Unlike Zapier/Make, n8n can self-host and gives you full control over your data. The AI agent nodes make it a powerful platform for building autonomous agents without writing code.

## Key Features

### AI Agent Nodes

N8N has dedicated AI agent nodes that enable:
- **Router agents** — Route requests to appropriate handlers
- **Query agents** — Answer questions from your data
- **Task agents** — Execute multi-step tasks autonomously
- **Feedback agents** — Learn from user feedback

### Workflow Examples

**AI Customer Support Agent:**
```
Webhook → AI Agent → Lookup CRM → Generate Response → Send Email
```

**Research Pipeline:**
```
RSS Feed → AI Agent (extract insights) → Save to Notion → Notify Slack
```

**Lead Qualification:**
```
Form Submit → AI Agent (score lead) → Update CRM → Route to sales
```

## Self-Hosting with Cloudflare Tunnel

For privacy-sensitive AI workflows:

```bash
# Run n8n with Cloudflare Tunnel
docker run -d --name n8n \
  -p 5678:5678 \
  n8nio/n8n

# Create Cloudflare Tunnel for remote access
cloudflared tunnel --url http://localhost:5678
```

Benefits:
- Full data control
- No usage limits (unlike cloud)
- Custom AI model integration

## Comparison with Alternatives

| Feature | N8N | Zapier | Make |
|---------|-----|--------|------|
| Self-host | ✅ | ❌ | ❌ |
| AI Agents | ✅ | Limited | Limited |
| Open source | ✅ | ❌ | ❌ |
| Free tier | Unlimited (self-host) | 100 runs/mo | 1K ops/mo |
| Custom code | ✅ | ❌ | ✅ |

## Resources

- [N8N Official](https://n8n.io)
- [Udemy: n8n Agentic AI](https://www.udemy.com/course/n8n-agentic-ai-and-automation/)
- [Fynch Blog: How to Build AI Agents with n8n](https://blog.fyn.ch/how-to-build-ai-agents-n8n/)
- [Awesome Agents n8n Review](https://awesomeagents.ai/reviews/review-n8n/)

## Related Concepts

- [[workflow-automation]] — General automation patterns
- [[ai-agents]] — Autonomous AI agent concepts
- [[local-llm-agents]] — Running AI agents on local models
