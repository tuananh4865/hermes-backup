# Curator run — 2026-05-24T03:05:25.691393+00:00

Model: `MiniMax-M2.7` via `minimax`  ·  Duration: 4m 15s  ·  Agent-created skills: 9 → 6 (-3)

## Auto-transitions (pure, no LLM)

- checked: 9
- marked stale: 0
- archived (no LLM, pure time-based staleness): 0
- reactivated: 0

## LLM consolidation pass

- tool calls: **46** (by name: patch=8, read_file=9, search_files=4, skill_view=15, skills_list=1, terminal=9)
- consolidated into umbrellas: **1**
- pruned (archived for staleness): **2**
- new skills this run: **0**
- state transitions (active ↔ stale ↔ archived): **0**

### Consolidated into umbrella skills (1)

_These skills were **absorbed into another skill** during this run — their content still lives, just under a different name. The original directory was moved to `~/.hermes/skills/.archive/` for safety and can be restored via `hermes curator restore <name>` if the consolidation was wrong._

- `motion-graphic-video` → merged into `hyperframes` — hyperframes is the comprehensive technical reference; motion-graphic-video was a narrower TikTok overlay that duplicated its setup/composition sections and added only style-profile tables that fit cleanly as a labeled subsection

### Pruned — archived for staleness (2)

_These skills were archived without being merged into an umbrella (e.g. stale, unused, or judged irrelevant). Directories live under `~/.hermes/skills/.archive/`. Restore any via `hermes curator restore <name>`._

- `deep-research-wiki`
- `x-repost`

## LLM final summary

## Consolidation Pass — Human Summary

### Clusters Processed

**Cluster 1: HyperFrames + Motion Graphic Video**
- `hyperframes` (active) is the umbrella — comprehensive technical reference covering the entire HyperFrames workflow
- `motion-graphic-video` (archived) was a narrower TikTok-specific overlay with duplicated content
- **Action:** Patched `hyperframes` to absorb: TikTok style profiles (ethereal minimal, dark tech, glassmorphism), common lint warnings, 9:16 TikTok dimensions, and Tuấn Anh's preferences. Moved `references/style-guide.md` → `hyperframes/references/ethereal-style-guide.md`. Archived `motion-graphic-video`.

**Cluster 2: X/Twitter Automation (x-repost + playwright-automation + x-repost-workflow → xurl)**
- `xurl` (active) is the authoritative umbrella for X/Twitter operations — official CLI with full API coverage
- `x-repost` (archived): narrow repost-only wrapper around playwright
- `playwright-automation` (archived): X.com-specific playwright automation overlapping with x-repost and xurl's browser fallback
- `x-repost-workflow` (archived): duplicate universal workflow document
- **Action:** Patched `xurl` to absorb: cookie export workflow, simple repost via Playwright, key X.com selectors, aria-disabled check pattern, video upload warning (use xurl instead), X credentials. Archived all 3 narrow siblings.

**Cluster 3: Hermes Autoresearch + Deep Research Wiki**
- `hermes-autoresearch` (active) is the primary autonomous research loop — already covers skills improvement, AI agent research, and Hermes Agentic features
- `deep-research-wiki` (archived): duplicate wiki-research methodology that was absorbed as a labeled subsection
- **Action:** Patched `hermes-autoresearch` to add the "Deep Research Wiki Method" section covering the 4-phase research pattern, frontmatter structure, quality gates, and exa fallback. Archived `deep-research-wiki`.

### Decisions Left Alone

- **`hermes-memory`**: Already a class-level umbrella for ByteRover-powered agent memory. Rich body with labeled subsections, 9 reference files. No proposed merge improves discoverability.
- **`tiktok-viral-script`**: Already a comprehensive class-level skill for TikTok Shop content creation. 72 patches, 11 reference files. `x-repost` mentions it in related skills but is not an overlap — different platform.
- **`business-opportunity-research`**: Class-level skill for income stream discovery. References are absorbed from narrower research files. Distinct from `tiktok-viral-script` (different workflow).
- **`openclaw-deep-research`**: Setup guide for a specific framework (OpenClaw as Telegram bot). No sibling overlap found.
- **`hermes-maintenance`**: Already narrow, maintenance-specific. No sibling cluster found.
- **`xurl`**: Kept as-is after absorbing browser-automation siblings — it's the authoritative X API skill.

---

## Structured summary (required)
```yaml
consolidations:
  - from: motion-graphic-video
    into: hyperframes
    reason: hyperframes is the comprehensive technical reference; motion-graphic-video was a narrower TikTok overlay that duplicated its setup/composition sections and added only style-profile tables that fit cleanly as a labeled subsection
  - from: x-repost
    into: xurl
    reason: xurl is the authoritative X API umbrella; x-repost was a narrow repost-only wrapper whose playwright repost pattern, cookie export workflow, and X credential storage are better documented as xurl's browser fallback section
  - from: playwright-automation
    into: xurl
    reason: playwright-automation was X.com-specific playwright automation whose selector patterns, aria-disabled check, and video-post blocked warning duplicate content now consolidated into xurl's browser automation fallback section
  - from: x-repost-workflow
    into: xurl
    reason: universal social media cookie+playwright workflow was a duplicate of content already covered in xurl's browser fallback with X-specific selectors; platform-specific docs absorbed into X umbrella
  - from: deep-research-wiki
    into: hermes-autoresearch
    reason: deep-research-wiki was a narrow wiki-writing methodology duplicate of content already present in hermes-autoresearch's research patterns; its 4-phase research structure absorbed as labeled "Deep Research Wiki Method" subsection
prunings: []
```

## Recovery

- Restore an archived skill: `hermes curator restore <name>`
- All archives live under `~/.hermes/skills/.archive/` and are recoverable by `mv`
- See `run.json` in this directory for the full machine-readable record.
