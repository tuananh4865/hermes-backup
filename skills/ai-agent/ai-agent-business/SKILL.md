---
title: AI Agent Business — Felix Model Monetization
name: ai-agent-business
created: 2026-05-05
updated: 2026-05-07
type: skill
tags: [ai-agent, monetization, felix-model, openclaw, hermes, revenue]
description: Build autonomous AI agent businesses using the Felix Model — SOUL.md, 3-layer memory, heartbeat, revenue stack. Turn AI agents into income-generating digital employees.
trigger: User wants to monetize AI agents, build agent businesses, or replicate the Felix/OpenClaw model
---

# AI Agent Business — Felix Model

> Build autonomous businesses with AI agents. Source: Felix Craft — $300K/month verified, Nat Eliason.

## The Core Model

```
Setup Agent → Create Digital Product → Sell → Scale → Automate Further
```

**Felix Craft Stats:**
- Revenue: $300K+/month ($100K Stripe + $94K ETH verified)
- Cost: ~$1,500/month (2x Claude Max)
- ROI: 200x
- Time to first sale: <24 hours
- Starting capital: $1,000 (optional)

## Step-by-Step Implementation

### Step 1: Setup Hermes Agent (Recommended over OpenClaw)

Hermes is easier to set up and has self-improving loop. OpenClaw has larger skill ecosystem.

```bash
# Hermes install
curl -sL https:// herbs | bash

# Model choice:
# - Free: Qwen 3.5 on OpenRouter (routine tasks)
# - Paid: Claude Sonnet 4.6 or GPT-4o (complex reasoning)
```

### Step 2: Create SOUL.md (Most Critical File)

SOUL.md defines if agent is focused on revenue OR just "helpful."

```markdown
# SOUL.md Template

## Core Mission
You are an AI entrepreneur. Your ONE goal: grow revenue.
Every action measured against: "Does this make money?"

## Revenue Focus
- Primary: Monthly recurring revenue (MRR)
- Secondary: Customer acquisition cost, lifetime value
- Everything else is noise.

## Decision Framework
1. Will this increase revenue? Do it.
2. Will this reduce costs? Do it.
3. Will this save time? Automate it.
4. If uncertain: "Does this make money?"

## Anti-Patterns (Never Do)
- Don't research indefinitely — ship and iterate
- Don't over-engineer — MVP first
- Don't ask permission for obvious wins
- Don't spend >$50 without human approval
```

### Step 3: Setup 3-Layer Memory Architecture

Memory is what makes agents "smart" vs. generic chatbots.

| Layer | Purpose | Implementation |
|-------|---------|----------------|
| Knowledge Graph | Long-term facts | PARA system in ~/life/ |
| Daily Notes | Session context | memory/YYYY-MM-DD.md |
| Tacit Knowledge | User preferences | USER.md, MEMORY.md |

**Nightly Consolidation (Cron at 2AM):**
```markdown
1. Read all session logs from today
2. Extract key decisions, revenue, learnings
3. Update knowledge graph
4. Index everything
5. Report to human
```

### Step 4: Setup Heartbeat (Proactive Checks)

Heartbeat = agent works while you sleep.

```markdown
## HEARTBEAT.md

### Every 30 min (8AM-10PM)
- Check revenue (Stripe dashboard)
- Check for urgent emails
- Check support issues

### Every 2 hours
- Post to X/Twitter
- Check competitor activity

### Every 6 hours
- Strategic review: what's working?
- Update todo with next 5 priorities

### Morning (8AM)
- Daily briefing to Telegram:
  * Yesterday's revenue
  * Today's priorities
  * Any blockers

### Night (11PM)
- Self-improvement review
- What failed today?
- What to automate next time?
```

### Step 5: Connect Revenue Stack

| Tool | Purpose | Cost |
|------|---------|------|
| Stripe | Payments | 2.9% + 30¢ |
| Vercel | Deploy sites | Free/$20/mo |
| GitHub | Code | Free |
| X/Twitter | Marketing | Free |
| Gmail | Support | Free |
| OpenRouter | AI models | $0-200/mo |
| Telegram | Commands | Free |

**SECURITY RULE:** Create SEPARATE accounts for agent. Never use personal accounts.

### Step 6: Create First Product (Must Be <24 Hours)

**Options:**
1. **PDF Guide ($29-49):** "How to Setup [AI Tool] for [Use Case]"
2. **Template Bundle ($19-99):** Notion template, workflow, prompts
3. **Skill Package ($5-20):** Markdown files others can install

**Product Creation Prompt:**
```
Task: Create a digital product by tomorrow morning.

Requirements:
- Format: PDF or digital download
- Price: $29-49
- Topic: Something you've learned doing [X]
- Solve ONE specific problem
- Include step-by-step instructions

Steps:
1. Research what problems people face in [niche]
2. Outline solution (5-10 steps)
3. Write content — specific, not generic
4. Create Stripe/Gumroad checkout
5. Deploy landing page to Vercel
6. Write launch post for X
7. Monitor sales and iterate

Deadline: Live by 9AM tomorrow.
```

## Revenue Timeline

| Week | Revenue | Milestone |
|------|---------|-----------|
| 1 | $500-3,500 | First product live |
| 2 | $1,000-5,000 | First customers |
| 3 | $2,000-8,000 | Feedback → iterate |
| 4 | $3,000-10,000 | Scale what's working |
| 8 | $10,000-30,000 | Multiple products |
| 12 | $30,000-100,000 | Business system |

## Cost Breakdown

| Component | Monthly |
|-----------|---------|
| VPS (DigitalOcean) | $5-20 |
| AI Model (OpenRouter) | $10-100 |
| Stripe fees | Variable |
| Vercel | $0-20 |
| **TOTAL** | **$15-140/mo** |

## Success Factors

**✅ DO:**
- SOUL.md with revenue focus
- 3-layer memory system
- Heartbeat for 24/7 operation
- Tool access (Stripe, X, email)
- Daily review → improve 1% per day

**❌ DON'T:**
- Let agent decide without checkpoints
- Give too many permissions at once
- Skip memory setup
- Skip heartbeat → agent forgets tasks

## The Overnight Challenge

To start, give agent one task before bed:

```
"Tomorrow morning I want to wake up with a product live.
You can build it entirely on your own.
Leave blockers in a note. Go."
```

Agent will: research → write product → build landing page → setup Stripe → deploy → write launch post

Next morning: review → approve → launch!

## Key Resources

- Felix Craft: https://felixcraft.ai/
- Nat Eliason walkthrough: https://www.youtube.com/watch?v=nSBKCZQkmYw
- Midas Tools breakdown: https://www.midastools.co/blog/felix-craft-story

## Related Skills

- `hermes-autoresearch` — nightly self-improvement
- `multi-agent-orchestrator` — running multiple agents
- `openclaw` — alternative agent framework

## Support Files

| File | Purpose |
|------|---------|
| `references/felix-model-case.md` | Verified revenue numbers, cost structure, sub-agent architecture |
| `references/worker-cron-2026-05-07.md` | Worker cron status log — tracks which worker crons verified working |
| `references/worker-cron-2026-05-08.md` | **CRITICAL**: Worker output gap — workers not writing to shared outputs/ |
| `templates/soul-template.md` | Copy-paste SOUL.md for revenue-focused agent |
| `templates/heartbeat-template.md` | Copy-paste heartbeat schedule for 24/7 operation |

## Pitfalls

1. **Vague SOUL.md** — "be helpful" = generic agent = no revenue. Must say "make money"

2. **"Workers configured" ≠ "Workers running"** — Tạo SOUL.md + HEARTBEAT.md ≠ autonomous agents đang chạy. tmux pipeline đang chạy demo project (pi-coding-agent build smartapp UI) KHÔNG PHẢI business workflow tự động. Workers cần scheduled triggers (cron jobs) gọi worker tasks, không chỉ config files.

3. **"Cron job fires" ≠ "Worker wrote to shared outputs/"** — Worker cron jobs có thể chạy và produce output, nhưng output đi vào `~/.hermes/cron/output/{job_id}/` KHÔNG PHẢI `~/hermes/workers/{worker}/outputs/`. Orchestrator đọc shared outputs/ để aggregate — nếu trống thì pipeline bị broken. Workers phải write output file vào shared directory AND respond normally. See `references/worker-cron-2026-05-08.md`.

4. **No memory setup** — agent starts fresh every session, can't compound learning

4. **No heartbeat** — agent only works when you talk to it, not while sleeping

5. **Too many tools at once** — start with 2-3, add after basics work

6. **Agent full financial access** — always use restricted API keys

7. **No checkpoints** — agent can make expensive mistakes without approval gates

8. **Confusing "setup complete" with "business running"** — Phase 1: config files created. Phase 2: workers executing tasks. Phase 3: revenue generated. Most stop at Phase 1 and wonder why no money comes in.

9. **"Cron job list shows job" ≠ "Job is running"** — Job exists in cronjob list with `last_run_at: null` means it NEVER fired. Must check BOTH: (a) job exists in `cronjob list`, AND (b) `~/.hermes/cron/output/{job_id}/` has recent output files. If job_id dir is missing or empty = job never triggered. System cron daemon must be running (`ps aux | grep cron` shows `/usr/sbin/cron`).

10. **Orchestrator 2AM ≠ orchestrator daily cycle** — The 2AM cron runs `hermes-autoresearch` (self-improvement), NOT the orchestrator role. Orchestrator duties (monitor workers, morning briefing, nightly consolidation) run on their own crons (9AM, every 2h, 9PM). Workers fire at 8AM/8:30AM BEFORE orchestrator morning briefing — correct timing for fresh content.
