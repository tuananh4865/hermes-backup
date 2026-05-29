# Hermes X Research — 2026-05-29

**Stars:** 157.2K+ (up from 155K on May 20)
**v0.14 Foundation Release** — verified current as of May 29

## Key Findings

### CEO Pattern (Keith Rumjahn's Setup)
```
Hermes = CEO (memory, coordination, quick tasks, cron)
OpenClaw = Senior Engineer (deep research, complex workflows)
Both share same Obsidian vault = single knowledge base
```

- Hermes handles daily life, delegates hard stuff to OpenClaw
- Both read/write same markdown files
- Prompt to wire: "Use Hermes for simple reasoning, quick tasks, coordination. Use OpenClaw for multi-step workflows, deep research, long-running tasks."

### Real-World Cron Job Setups (from r/hermesagent)
- Morning briefing: calendar + email + health stats
- Weekly sales/report automation
- Hourly "surprise me" heartbeat checks
- Social media analytics tracking
- Research digest delivery

### Customization Files That Matter
- **Souls.md** — personality ("concise technical expert, no fluff")
- **Agents.md** — brain/rules (coding style, post formats, do's/don'ts)
- **User.md** — memory about you (name, job, preferences)

### v0.14 Features Validated
- 180x faster browser automation (CDP-based)
- Native Windows beta (no WSL2)
- OpenHands orchestration: `hermes skills install official/open-hands`
- Self-Evolution: DSPy + GEPA for automatic skill file evolution

### Community Frustrations (v2026.5.28 broke containers)
- Latest daily build broke Hermes Agent container
- Workaround: use `nousresearch/hermes-agent:v2026.5.16`
- Install path scary for non-devs (Python 3.11+)
- Memory opacity (can't export "what Hermes knows about me")
- Skills from complex tasks can over-generalize

## Sources
- https://rumjahn.substack.com/p/complete-guide-to-mastering-hermes (Keith Rumjahn, Apr 27)
- https://www.reddit.com/r/hermesagent/comments/1tpms69/ (cron job discussions)
- https://www.reddit.com/r/hermesagent/comments/1t5ifvg/ (Self-Evolution release)
- https://www.techtimes.com/articles/316694/20260515/ (OpenClaw comparison)
- https://tokenmix.ai/blog/hermes-agent-review-self-improving-open-source-2026
