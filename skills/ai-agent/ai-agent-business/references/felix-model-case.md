# Felix Model — Case Study Reference

## Verified Revenue Numbers

| Month | Revenue | Stripe | ETH | Notes |
|-------|---------|--------|-----|-------|
| Week 3 | $14,718 | — | — | First product live |
| March 2026 | ~$200K total | $100,570 | $94,973 | ~20% of $1M goal |
| April 2026 | $300K+/month | $100,570 | $94,973 | 200x ROI on $1,500/mo cost |

## 3 Business Streams

1. **Felix Craft PDF ($29)** — $41K lifetime revenue
2. **ClawMart Marketplace** — 10% fee + $20/mo subscription, ~$14K/mo
3. **Clawcommerce** — $2,000 setup + $500/mo per client

## Cost Structure

- Claude Max: $200/mo
- Codex Max: $200/mo
- Vercel hosting: $20/mo
- OpenRouter API: ~$130/mo
- **Total: ~$1,500/mo** (96%+ profit margin)

## Sub-Agents

- **Iris** — Customer support (refunds, inquiries)
- **Remy** — Sales leads
- Felix as CEO manages both, reviews their work nightly

## Key Technical Details

### Heartbeat
- Fires every 30 minutes during active hours
- Checks Stripe revenue, email inbox, X mentions
- Alerts go to Telegram

### Nightly Self-Improvement Loop
- 2AM: Read all session logs from day
- Extract key decisions, learnings
- Update knowledge graph
- Next morning: agent is smarter

### Security
- Separate Stripe account for agent (restricted API keys)
- Agent reads X as "information layer" not authenticated input
- Prompt injection attempts ignored

## Sources

- https://felixcraft.ai/ — Official site
- https://www.midastools.co/blog/felix-craft-story — Full breakdown
- https://www.youtube.com/watch?v=nSBKCZQkmYw — Nat Eliason 35-min tutorial
- https://openclaw.report/use-cases/felix-zero-human-company — Detailed analysis
