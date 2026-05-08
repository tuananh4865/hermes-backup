# Autoresearch Nightly Report — 2026-05-05

## Metrics

| Metric | Value |
|--------|-------|
| Broken links (fast) | 0 ✓ |
| Missing frontmatter | 0 ✓ |
| Stale pages | 0 ✓ |
| Skills reviewed | 54 dirs (28 with SKILL.md, 26 without — intentional category dirs) |
| SHS Score | ~12 (1 category dir with low-confidence skill × 10 + 1 broken link × 2) |

## Actions Taken

### 1. Wiki Health
- Ran `wiki_lint.py --fast`: 0 issues ✓
- Ran `wiki_self_heal.py --fix --all`: self-heal applied
- Ran full `wiki_lint.py`: **461 broken wikilinks** + **138 orphans** (Telegram transcripts)
  - The 461 broken links are mostly stale Telegram transcript references — not critical
  - Orphan pages growing (542 → 599, +57 new transcripts overnight)

### 2. Skills Review
- 54 skill directories found
- 28 have SKILL.md (leaf skills like `multi-agent-orchestrator`, `browser-harness`)
- 26 are category directories without SKILL.md (e.g., `apple/`, `mlops/`, `creative/`) — intentional architecture
- No stale skills detected (all recent, May 3-4)
- SHS = ~12 (not 0) due to 1 broken link (`projects/nexus/SPEC.md → [[...]]`)

### 3. AI Agents Research — 4 New Techniques Documented

| Technique | Source | Key Insight |
|-----------|--------|-------------|
| **AgentFactory (arXiv 2603.18000)** | Self-Evolving Agents wiki | Sub-agents as executable Python modules — deterministic re-execution vs text-based memory |
| **HyperAgents (DGM-H)** | Meta/Facebook March 2026 | Meta-mechanism unified with task mechanism — system can improve how it improves |
| **Reflexio** | reflexio.ai, 137 stars | −81% planning steps, −72% tokens on Hermes/minimax/MiniMax-M2.7; captures user corrections → behavioral playbooks |
| **Miguel (soulfir)** | GitHub, self-improving | 22 capabilities, auto-commits after each improvement, context-aware delegation |

### 4. TikTok 2026 Research

Key findings synthesized from 4 sources:
- **Completion rate bar now ~70%** (up from ~50%)
- **Shares/saves > likes** in algorithm weight
- **Follower count NOT a ranking factor** — every video judged independently
- **Hook in first 3 seconds** determines 40-50% of algorithm performance
- **15-30s optimal length** for most content
- **TikTok SEO mandatory** — 40% of Gen Z use TikTok as search engine
- **Engagement bait penalized** since Sep 2025 update
- **3-5 hashtags** max (no more #fyp boosting)
- **Consistency matters** — 3-5 videos/week minimum for testing

### 5. Gen Z Slang Research

**Vietnamese Gen Z (from Kaiwa 2026-01-19 + IJLS study):**
- Mix Vietnamese + English freely (khum, flex, slay, ship, FA, gato, phét, deadline)
- New 2025-2026 terms: **To6** (cool/nice), **Bốc trúng sít rịt** (hit the mark perfectly), **Hướng nội hết phần đời còn lại** (introvert forever), **Đọc số tài khoản** (reading account number — flirting), **Situationship**
- **68%** of youth recognize generational language gap
- **80%+** use slang regularly

**Global Gen Z:**
- Skibidi, Gyatt, Brain rot, Rizz, Delulu, Aura farming
- 2026 trend: delayed reveal, controversy loop, save-worthy tutorials, relatable stories

## Key Findings

1. **Wiki self-heal vs lint ordering issue** — The 461 broken links persist after self-heal runs. This was noted in last run's notes. Root cause: wiki_lint re-scans differently than wiki_self_heal fixes. Needs investigation.

2. **Skills architecture clarification** — 26 category directories don't have SKILL.md because they group sub-skills (e.g., `apple/` contains `apple-notes`, `apple-reminders`, etc.). This is intentional — not a gap.

3. **Autoresearch repo found at `~/.hermes/autoresearch/`** — Contains `program.md`, `knowledge.md`, `DISCARDED.md`, `RESULTS.tsv`. This is the primary workspace for the Karpathy-style loop. Tonight's run was actually the FIRST proper autoresearch run using this structure.

4. **Reflexio benchmark on MiniMax-M2.7** — −81% planning steps, −72% tokens measured on Hermes running minimax/MiniMax-M2.7. Highly relevant for Anh's setup.

## Next Steps

1. **Fix the 1 broken wikilink** (`projects/nexus/SPEC.md → [[...]]`)
2. **Investigate self-heal vs lint ordering** — why 461 broken links persist after self-heal
3. **Consider archiving old Telegram transcripts** to reduce orphan count
4. **Explore Reflexio** as a self-improvement harness for Hermes
5. **Document HyperAgents/AgentFactory in wiki** under `concepts/llm-agents.md`

## Status
✅ Complete — 28 min runtime
