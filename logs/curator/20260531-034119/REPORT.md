# Curator run — 2026-05-31T03:41:19.310235+00:00

Model: `MiniMax-M2.7` via `minimax`  ·  Duration: 3m 6s  ·  Agent-created skills: 10 → 8 (-2)

## Auto-transitions (pure, no LLM)

- checked: 10
- marked stale: 0
- archived (no LLM, pure time-based staleness): 0
- reactivated: 0

## LLM consolidation pass

- tool calls: **32** (by name: patch=3, read_file=1, skill_manage=2, skill_view=12, skills_list=1, terminal=11, write_file=2)
- consolidated into umbrellas: **2**
- pruned (archived for staleness): **0**
- new skills this run: **0**
- state transitions (active ↔ stale ↔ archived): **0**

### Consolidated into umbrella skills (2)

_These skills were **absorbed into another skill** during this run — their content still lives, just under a different name. The original directory was moved to `~/.hermes/skills/.archive/` for safety and can be restored via `hermes curator restore <name>` if the consolidation was wrong._

- `hermes-maintenance` → merged into `hermes-memory` — Narrow single-session artifact (disk cleanup workflow) — absorbed as `references/hermes-cluster/hermes-maintenance.md` under existing Hermes infra umbrella. SKILL.md deleted, content preserved in umbrella.
- `hermes-upgrade-verify` → merged into `hermes-memory` — Narrow single-session artifact (post-upgrade QA checklist) — absorbed as `references/hermes-cluster/hermes-upgrade-verify.md` under existing Hermes infra umbrella. SKILL.md deleted, content preserved in umbrella.

## LLM final summary

## Curator Pass Summary — 2026-05-31

### Clusters Processed

**HERMES cluster (hermes-maintenance + hermes-upgrade-verify) → absorbed into `hermes-memory`**

These two narrow skills were full-session artifacts with specific bug fixes and no subdirectories:
- `hermes-maintenance` — disk cleanup workflow, discovered and fixed during a single maintenance session
- `hermes-upgrade-verify` — post-upgrade QA checklist, discovered during a single upgrade verification session

Both are narrow class-of-one skills that a maintainer would consolidate under an umbrella. `hermes-memory` was the natural host — it already covers Hermes infra operation (gateway, upgrades, maintenance, ByteRover, wiki). Absorbed as `references/hermes-cluster/hermes-maintenance.md` and `references/hermes-cluster/hermes-upgrade-verify.md`; `hermes-memory` SKILL.md patched to reference them.

### Other Skills Reviewed — No Action Needed

The remaining 8 skills are class-level umbrellas or properly narrow with no sibling overlap:

| Skill | Status | Reason |
|-------|--------|--------|
| `business-opportunity-research` | Keep | Already a broad class-level skill — income stream research framework |
| `hermes-memory` | Keep (expanded) | Class-level umbrella for Hermes knowledge/persistence |
| `hyperframes` | Keep | Class-level — motion graphics creation, well-scoped |
| `openclaw-deep-research` | Keep | Class-level — OpenClaw Telegram bot setup |
| `qa-gate` | Keep | Class-level — QA gate protocol, already consolidated |
| `tiktok-viral-script` | Keep | Class-level — TikTok content creation framework, already massive |
| `voice-setup` | Keep | Class-level — voice STT/TTS configuration |
| `wiki-maintenance` | Keep | Class-level — wiki maintenance workflows |

### Decisions Made

- **Consolidated** `hermes-maintenance` → `hermes-memory` (absorbed as `references/hermes-cluster/hermes-maintenance.md`)
- **Consolidated** `hermes-upgrade-verify` → `hermes-memory` (absorbed as `references/hermes-cluster/hermes-upgrade-verify.md`)
- **No pruning** — no truly stale skills found among the 10 candidates

### Archive State
`~/.hermes/skills/.archive/` holds 42 previously archived skills (pre-existing, not from this pass). The 2 consolidated skills were absorbed directly without going through `.archive/`.

---

## Structured summary (required)

```yaml
consolidations:
  - from: hermes-maintenance
    into: hermes-memory
    reason: Narrow single-session artifact (disk cleanup workflow) — absorbed as `references/hermes-cluster/hermes-maintenance.md` under existing Hermes infra umbrella. SKILL.md deleted, content preserved in umbrella.
  - from: hermes-upgrade-verify
    into: hermes-memory
    reason: Narrow single-session artifact (post-upgrade QA checklist) — absorbed as `references/hermes-cluster/hermes-upgrade-verify.md` under existing Hermes infra umbrella. SKILL.md deleted, content preserved in umbrella.
prunings: []
```

## Recovery

- Restore an archived skill: `hermes curator restore <name>`
- All archives live under `~/.hermes/skills/.archive/` and are recoverable by `mv`
- See `run.json` in this directory for the full machine-readable record.
