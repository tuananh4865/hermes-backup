---
title: Hermes v0.15 Velocity Release Research
created: 2026-05-31
updated: 2026-05-31
type: reference
tags: [hermes, release, v0.15, velocity-release, security]
confidence: high
relationships: [hermes-agent]
---

# Hermes v0.15.0 / v0.15.2 "Velocity Release" (May 28-29, 2026)

## Version History
| Version | Date | Key Change |
|---------|------|------------|
| v0.15.2 (v2026.5.29.2) | May 29, 2026 | Packaging fix for plugin.yaml manifests |
| v0.15.0 "Velocity Release" | May 28, 2026 | 16,083-line PR, dramatically faster, Brainworm defense |

**Stars:** 158K+ GitHub stars (May 30, 2026)

## What's New in v0.15.0

1. **Promptware Defense (Brainworm)** — Blocks prompt-injection attacks at 3 chokepoints, defends context window. Direct response to arXiv:2605.17634 (May 17, 2026) "AI Agents May Always Fall for Prompt Injections"
2. **Bitwarden Secrets Manager** — One bootstrap token replaces N per-provider API keys
3. **Skill Bundles** — Package related skills together
4. **TUI Session Orchestrator** — Terminal UI for managing sessions
5. **Auto Supply-Chain Defense** — Automatic security patching
6. **NFTY Platform** — Multi-agent coordination platform
7. **Kanban Multi-Agent v2** — Real production workflow tool
8. **Sessions 4,500x faster** (Reddit benchmark)
9. **747 PRs by 321 contributors** — largest release cycle

## Security: Brainworm Prompt-Injection Defense

arXiv:2605.17634 (May 17, 2026): "AI Agents May Always Fall for Prompt Injections" showed prevailing defenses still fail.

**Hermes v0.15 response:** Promptware defense at 3 chokepoints — traffic filtering, context window defense, prompt sanitization.

## Upgrade Command
```bash
pip3 install 'hermes-agent>=0.15' -q
pip3 show hermes-agent | grep Version
```

## Sources
- https://github.com/NousResearch/hermes-agent/releases
- https://www.reddit.com/r/hermesagent/comments/1tqfrgq/hermes_agent_v0150_the_velocity_release/
- https://techsy.io/en/blog/hermes-agent-v0-15
- https://arxiv.org/abs/2605.17634 (prompt injection paper)
