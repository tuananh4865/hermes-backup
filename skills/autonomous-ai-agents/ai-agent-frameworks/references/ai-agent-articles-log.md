# AI Agent Articles — Research Log (2026-06-01)

> Log of articles analyzed under the `ai-agent-frameworks` skill.
> Each entry: source URL + classification + key takeaways + Anh's action items.

---

## 2026-06-01: Addy Osmani — "Loop Engineering" (Substack, Jun 8, 2026)

- **URL:** https://addyo.substack.com/p/loop-engineering
- **Source tweet:** https://x.com/addyosmani/status/2064127981161959567
- **Type:** Original essay (intellectual framework)
- **Length:** ~5,000 words

### Core Thesis
Loop engineering = replacing yourself as the prompter with designing the system that prompts. Leverage point moved from "typing prompts" to "designing systems that prompt."

### Key Quotes
- Peter Steinberger: "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents."
- Boris Cherny: "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do."

### 5+1 Building Blocks
1. **Automations** (heartbeat) — Codex Automations tab / Claude Code `/loop`, `/goal`, hooks
2. **Worktrees** (isolation) — `git worktree` for parallel agents without collision
3. **Skills** (project knowledge) — `SKILL.md` files, capture intent once
4. **Plugins/Connectors** (MCP) — real tool integration
5. **Sub-agents** (maker vs checker) — split writer from verifier
+1. **Memory** (state file) — markdown or Linear, lives outside single conversation

### 3 Pitfalls (must remember)
1. **Verification is still on you** — loop mistakes are unattended mistakes
2. **Comprehension debt** — faster loop = bigger gap between what exists and what you understand
3. **Cognitive surrender** — easy to stop having an opinion

### Application to Anh's Systems
| Component | Hermes Equivalent | Match |
|-----------|-------------------|-------|
| Automations | Heartbeat + cron jobs | ✅ 80% |
| Worktrees | Sub-agents in different contexts | ⚠️ Need explicit isolation |
| Skills | Skills (gskill files) | ✅ 100% |
| Plugins/MCP | MCP servers (browser, exa) | ✅ 100% |
| Sub-agents | Single agent per task | ❌ **Missing maker/checker split** |
| Memory | Wiki + memory system | ✅ 100% |

### Top 3 Action Items for Anh
1. **Add "Checker" sub-agent pattern** (biggest gap) — Worker → Worker (verifier) → Hermes → Anh
2. **Implement `/goal` primitive** — Loop until verifiable condition holds
3. **State file for long workflows** — `state.md` per project tracks tried/passed/failed

### Session 2026-06-01 — Plan Presented, NOT Executed
Anh asked: "verify và lên plan đi" for the 3 actions above.

**Verification done** (read-only, no writes):
- `~/.hermes/workers/` — does NOT exist (no `content-creator/`, no `state.md`)
- `~/.hermes/cron/jobs.json` — `a4b8e528983f` (autoresearch nightly, 49 runs done), `7cba6ba5f52a` (backup, 49 runs done)
- `/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/hub.md` — full Content Creator project already set up
  - 3 trụ nội dung (SETUP/EDIT/GEAR REVIEW)
  - 7 quy tắc bắt buộc (Hiến pháp kênh)
  - 142 skills healthy
- `Operations/` folder has voice profile, SOP, progress notes
- Niche: phụ kiện quay dựng phim cho người mới bắt đầu
- Voice profile: "các bạn" (trung tính, đã update 13/06/2026, bỏ "mấy con vợ")

**Plan presented** (timeline ~2.5h total):
- Action 1: `~/.hermes/skills/quality-checker/SKILL.md` — 30 min
  - Verify 7 quy tắc Hiến pháp kênh, voice "các bạn", ≥5 nguồn, hook theo 17 công thức viral
  - Output: PASS/FAIL + danh sách lỗi + đề xuất fix
- Action 2: `/goal` primitive in `~/.hermes/skills/loop-goal/` — 1h
  - Loop chạy tới khi đạt verified condition
  - VD: "Mỗi script đạt ≥3/5 tiêu chí: hook <30 chars, body 60-90s, CTA rõ, voice OK, checker PASS"
- Action 3: `~/.hermes/workers/content-creator/state.md` — 20 min
  - Sections: Current Goal, Last 5 Runs, What Worked, What Failed, Open Items, Resources
- E2E test + report — 30 min

**Status: PLAN ACCEPTED BUT NOT EXECUTED.** Conversation ended at plan presentation. Next session should resume from here if Anh asks to implement.

---

## 2026-06-01: 0xCodez — "Loop Engineering 14-Step Roadmap" (X, status 2064374643729773029)

- **URL:** https://x.com/0xCodez/status/2064374643729773029
- **Author:** @0xCodez (AI researcher + builder, AI insights from 2030)
- **Type:** TL;DR / Roadmap (derivative of Addy Osmani's essay)
- **Content source:** Summarized via secondary aggregator (bittide.aicompass.dev)

### Assessment
- **NOT original** — directly summarizes Addy Osmani's framework
- Adds: "AI slop" warning, 3 Claude Code primitives specifics, 4-mode loop design
- Useful for: Quick reference when user doesn't want to read 5K words

### When to Use
- User wants quick checklist version of Loop Engineering
- Already discussed Addy Osmani's essay, user wants concrete steps

### When to Skip
- User has already understood the framework
- User wants original insight (none here)

---

## Quick Reference: AI Agent Frameworks Comparison

| Framework | Author | Core Idea | When to Apply |
|-----------|--------|-----------|---------------|
| Loop Engineering | Addy Osmani | Design system that prompts itself | Long-running workflows |
| Agent Harness Engineering | Addy Osmani | Environment for one agent | Building single agents |
| Multi-Agent Teams | Boris Cherny / 0xCodez | Up to 20 specialists + coordinator | Complex parallel tasks |
| Maker/Checker Split | Industry pattern | Sub-agent verifies work | Quality-critical tasks |
| Claude Managed Agents | Anthropic | Roster of up to 20 agents | Production multi-agent |

## Common Patterns Across All Frameworks

1. **Memory must be on disk, not in context** — agents forget between runs
2. **Sub-agents for verification** — same agent can't grade own work
3. **State file as spine** — what's tried, what passed, what's next
4. **Human review for high-stakes** — loop speeds up, doesn't replace judgment
