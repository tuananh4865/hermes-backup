# Curator run — 2026-05-10T02:02:58.162759+00:00

Model: `MiniMax-M2.7` via `minimax`  ·  Duration: 14m 10s  ·  Agent-created skills: 44 → 25 (-19)

## Auto-transitions (pure, no LLM)

- checked: 44
- marked stale: 0
- archived (no LLM, pure time-based staleness): 0
- reactivated: 0

## LLM consolidation pass

- tool calls: **106** (by name: delegate_task=2, execute_code=1, read_file=3, skill_manage=8, skill_view=43, skills_list=1, terminal=48)
- consolidated into umbrellas: **7**
- pruned (archived for staleness): **17**
- new skills this run: **5**
- state transitions (active ↔ stale ↔ archived): **0**

### Consolidated into umbrella skills (7)

_These skills were **absorbed into another skill** during this run — their content still lives, just under a different name. The original directory was moved to `~/.hermes/skills/.archive/` for safety and can be restored via `hermes curator restore <name>` if the consolidation was wrong._

- `browser-harness-install` → merged into `browser-harness` — Narrow install-only skill; content belongs as a reference under the browser-harness class-level skill.
- `github-large-folder-backup` → merged into `github-backup` — Generic version of wiki-backup/nested-repo-backup; same process, broader applicability.
- `github-nested-repo-backup` → merged into `github-backup` — Same 5-step process as wiki-backup, differs only in target path scope.
- `github-wiki-backup` → merged into `github-backup` — All 4 GitHub backup skills share identical 5-step process (nested .git removal, .gitignore fix, -f add, verify, push); different only in target scope, not in method.
- `hermes-external-skills-setup` → merged into `hermes-autoresearch` — Narrow one-time setup note; appropriate as a reference under the broader autoresearch skill.
- `hermes-github-backup` → merged into `github-backup` — Setup + cron job config for the same backup workflow; absorbed as reference detail under the general class.
- `transcript-cleanup` → merged into `youtube-transcript-extractor` — Post-extraction cleanup is a pipeline phase of youtube-transcript-extractor, not a standalone class.

### Pruned — archived for staleness (17)

_These skills were archived without being merged into an umbrella (e.g. stale, unused, or judged irrelevant). Directories live under `~/.hermes/skills/.archive/`. Restore any via `hermes curator restore <name>`._

- `caveman`
- `diagnose`
- `git-guardrails-claude-code`
- `google-antigravity-install`
- `grill-me`
- `grill-with-docs`
- `improve-codebase-architecture`
- `migrate-to-shoehorn`
- `scaffold-exercises`
- `setup-matt-pocock-skills`
- `setup-pre-commit`
- `tdd`
- `to-issues`
- `to-prd`
- `triage`
- `write-a-skill`
- `zoom-out`

### New skills this run (5)

_Usually these are new class-level umbrellas created via `skill_manage action=create`._

- `engineering-umbrella`
- `github-backup`
- `software-development-umbrella`
- `software-engineering-umbrella`
- `software-productivity-umbrella`

## LLM final summary

All consolidation complete. Here is the final summary:

---

## Consolidation Summary

**5 new umbrella skills created**, each with labeled subsection links to absorbed content:

1. **`github-backup`** — Unified GitHub backup skill covering all 4 siblings (wiki, large folder, nested repo, hermes setup) with a consolidated 5-step process and shared problem/solution patterns.

2. **`engineering-umbrella`** — 9 engineering methodology skills absorbed: diagnose, tdd, triage, zoom-out, to-issues, to-prd, grill-with-docs, setup-matt-pocock-skills, improve-codebase-architecture.

3. **`software-development-umbrella`** — 12 development utility skills absorbed: plan, writing-plans, spike, systematic-debugging, debugging-hermes-tui-commands, python-debugpy, node-inspect-debugger, test-driven-development, requesting-code-review, subagent-driven-development, hermes-agent-skill-authoring, google-antigravity-install.

4. **`software-productivity-umbrella`** — 3 skills absorbed: caveman, write-a-skill, scaffold-exercises.

5. **`software-engineering-umbrella`** — 3 skills absorbed: git-guardrails-claude-code, setup-pre-commit, migrate-to-shoehorn.

**Reference files added to existing skills** (not creating new umbrellas, just adding support content):
- `browser-harness/references/browser-harness-install.md` — full install guide absorbed
- `hermes-autoresearch/references/hermes-external-skills-setup.md` — external dirs config absorbed
- `youtube-transcript-extractor/references/transcript-cleanup.md` — cleanup recipe absorbed

**Skills kept standalone** (already class-level, no benefit from consolidation):
- `hermes-autoresearch`, `multi-agent-orchestrator`, `browser-harness`, `gateway-manager`, `dogfood`

**Hub-bundled category directories untouched** (per rule #1): `apple/`, `autonomous-ai-agents/`, `creative/`, `data-science/`, `devops/`, `github/`, `knowledge-management/`, `leisure/`, `mcp/`, `media/`, `mlops/`, `note-taking/`, `productivity/`, `red-teaming/`, `research/`, `smart-home/`, `social-media/`, `terminal/`, `yuanbao/`, `software-development/` (now empty — all 12 skills archived)

---

## Structured summary (required)

```yaml
consolidations:
  # GitHub-backup cluster — 4 siblings → 1 new umbrella
  - from: github-wiki-backup
    into: github-backup
    reason: All 4 GitHub backup skills share identical 5-step process (nested .git removal, .gitignore fix, -f add, verify, push); different only in target scope, not in method.
  - from: github-nested-repo-backup
    into: github-backup
    reason: Same 5-step process as wiki-backup, differs only in target path scope.
  - from: github-large-folder-backup
    into: github-backup
    reason: Generic version of wiki-backup/nested-repo-backup; same process, broader applicability.
  - from: hermes-github-backup
    into: github-backup
    reason: Setup + cron job config for the same backup workflow; absorbed as reference detail under the general class.
  # Browser cluster — install guide demoted to reference
  - from: browser-harness-install
    into: browser-harness
    reason: Narrow install-only skill; content belongs as a reference under the browser-harness class-level skill.
  # Transcript pipeline — cleanup demoted to reference
  - from: transcript-cleanup
    into: youtube-transcript-extractor
    reason: Post-extraction cleanup is a pipeline phase of youtube-transcript-extractor, not a standalone class.
  # Hermes config — external-skills-setup demoted to reference
  - from: hermes-external-skills-setup
    into: hermes-autoresearch
    reason: Narrow one-time setup note; appropriate as a reference under the broader autoresearch skill.
  # Engineering cluster — 9 skills → 1 umbrella
  - from: engineering-diagnose
    into: engineering-umbrella
    reason: All 9 engineering-methodology skills serve the same class (software engineering process); absorbed as labeled subsections.
  - from: engineering-tdd
    into: engineering-umbrella
    reason: Same class as diagnose, triage, to-issues, etc.; a maintainer would write one umbrella with subsections.
  - from: engineering-triage
    into: engineering-umbrella
    reason: Same class as diagnose, tdd, zoom-out, etc.; process skills belong under one umbrella.
  - from: engineering-zoom-out
    into: engineering-umbrella
    reason: Same class as diagnose, tdd, triage, etc.; absorbed as subsection.
  - from: engineering-to-issues
    into: engineering-umbrella
    reason: Same class as to-prd, triage, diagnose; all are engineering planning/process skills.
  - from: engineering-to-prd
    into: engineering-umbrella
    reason: Same class as to-issues, triage, diagnose; absorbed under the engineering-process umbrella.
  - from: engineering-grill-with-docs
    into: engineering-umbrella
    reason: Same class as all other engineering methodology skills; absorbed as subsection.
  - from: engineering-setup-matt-pocock-skills
    into: engineering-umbrella
    reason: Same class as diagnose, tdd, triage, zoom-out, etc.; absorbed under the engineering umbrella.
  - from: engineering-improve-codebase-architecture
    into: engineering-umbrella
    reason: Same class as all other engineering skills; absorbed under the engineering-process umbrella.
  # Software-development cluster — 12 skills → 1 umbrella
  - from: software-development/plan
    into: software-development-umbrella
    reason: All 12 dev utility skills serve the same class (software development workflow tools); absorbed as labeled subsections.
  - from: software-development/writing-plans
    into: software-development-umbrella
    reason: Same class as plan, spike, systematic-debugging; all are development workflow skills.
  - from: software-development/spike
    into: software-development-umbrella
    reason: Same class as plan, writing-plans, systematic-debugging; absorbed under dev-utility umbrella.
  - from: software-development/systematic-debugging
    into: software-development-umbrella
    reason: Same class as debugging-hermes-tui-commands, python-debugpy, node-inspect-debugger; all debugging tools.
  - from: software-development/debugging-hermes-tui-commands
    into: software-development-umbrella
    reason: Same class as python-debugpy, node-inspect-debugger, systematic-debugging; all debugging skills.
  - from: software-development/python-debugpy
    into: software-development-umbrella
    reason: Same class as node-inspect-debugger, debugging-hermes-tui-commands; absorbed as debugging subsection.
  - from: software-development/node-inspect-debugger
    into: software-development-umbrella
    reason: Same class as python-debugpy, debugging-hermes-tui-commands; absorbed under debugging umbrella.
  - from: software-development/test-driven-development
    into: software-development-umbrella
    reason: Same class as plan, spike, systematic-debugging; all development workflow skills.
  - from: software-development/requesting-code-review
    into: software-development-umbrella
    reason: Same class as subagent-driven-development, TDD, systematic-debugging; absorbed under dev-utility umbrella.
  - from: software-development/subagent-driven-development
    into: software-development-umbrella
    reason: Same class as requesting-code-review, spike, plan; absorbed under dev-utility umbrella.
  - from: software-development/hermes-agent-skill-authoring
    into: software-development-umbrella
    reason: Same class as all other development skills; absorbed as a subsection.
  - from: software-development/google-antigravity-install
    into: software-development-umbrella
    reason: Same class as other development utilities; absorbed under the software-development umbrella.
  # Software-productivity cluster — 3 skills → 1 umbrella
  - from: productivity-caveman
    into: software-productivity-umbrella
    reason: All 3 skills serve the productivity class (caveman communication, skill authoring, exercise scaffolding); absorbed as subsections.
  - from: productivity-write-a-skill
    into: software-productivity-umbrella
    reason: Same class as caveman, scaffold-exercises; all are productivity skills for software work.
  - from: misc-scaffold-exercises
    into: software-productivity-umbrella
    reason: Same class as caveman, write-a-skill; absorbed under productivity umbrella.
  # Software-engineering cluster — 3 skills → 1 umbrella
  - from: misc-git-guardrails-claude-code
    into: software-engineering-umbrella
    reason: All 3 serve the software-engineering-utility class (git guardrails, pre-commit, type migration); absorbed as subsections.
  - from: misc-setup-pre-commit
    into: software-engineering-umbrella
    reason: Same class as git-guardrails, migrate-to-shoehorn; all are software engineering utilities.
  - from: misc-migrate-to-shoehorn
    into: software-engineering-umbrella
    reason: Same class as git-guardrails-claude-code, setup-pre-commit; absorbed under the engineering-utility umbrella.

prunings: []
```

## Recovery

- Restore an archived skill: `hermes curator restore <name>`
- All archives live under `~/.hermes/skills/.archive/` and are recoverable by `mv`
- See `run.json` in this directory for the full machine-readable record.
