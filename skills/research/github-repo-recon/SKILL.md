---
name: github-repo-recon
description: Reverse-engineer a GitHub repo's architecture, file structure, naming conventions, and workflow. Use when anh says "research repo X", "phân tích cấu trúc repo", "file nào được tạo khi chạy tool Y", "workflow của repo Z", "cách project tổ chức code", "đọc hiểu project open source", or wants a file-mapping report / architecture diagram for ANY GitHub project.
---

# GitHub Repo Reconnaissance

Class-level skill for **reverse-engineering any GitHub repo** (architecture, file generation per workflow, naming conventions, hard rules). Distinct from `ml-model-comparison-report` (research a pretrained MODEL for use), `youtube-channel-audit` (research a YOUTUBE CHANNEL), and `third-party-tool-install` (install a CLI). This skill maps the CODEBASE itself, not a domain artifact.

## When to use this skill

- User asks "file nào được tạo ra cho mỗi video edit" (or any workflow action) in a specific repo
- User wants to understand how an open-source project is organized before cloning/adapting it
- User asks "quy trình X của repo Y" — need to produce a workflow + file-map report
- User wants to extract design patterns (12 hard rules, EDL schema, render pipeline) from a third-party project
- User points at a GitHub URL and asks "cái này hoạt động thế nào"

**Distinct from:**
- `ml-model-comparison-report` — research a model (HuggingFace weights, benchmarks) for deployment
- `youtube-channel-audit` — research a YouTube channel (content/visual/thumbnail patterns) for replication
- `third-party-tool-install` — install a CLI on anh's Mac, not analyze someone else's code
- `source-driven-development` — use official docs while CODING, not analyze someone else's repo

## Quick Reference

| Step | Tool | What you get |
|---|---|---|
| 1. Recon tree | `curl /repos/{o}/{r}/git/trees/main?recursive=1` | Full file/folder map in 1 call |
| 2. Fetch manifest | parallel `mcp__exa__web_fetch_exa` (max 5-8 URLs/call) | README + SKILL.md + helpers/*.py in 1 round-trip |
| 3. Cross-check names | grep `.gitignore` + `f"seg_..."` in helpers + directory tree in SKILL.md | Naming conventions with 3-way verification |
| 4. Map workflow | read code top-down: main() → helpers → 3rd-party calls (ffmpeg, Scribe, ...) | Phase-by-phase file generation table |
| 5. Extract patterns | grep "HARD RULE", "NEVER", "MUST" | 5-10 reusable design lessons |
| 6. Clone + install skills into Hermes | `git clone --depth 1` + `cp -a` + `ln -s` | Upstream skill pack wired into `~/.hermes/skills` without overwriting user-owned cookbooks |

## Procedure (5 phases, follow in order)

### Phase 1 — Tree map (1 curl call, ~5s)

```bash
curl -s "https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); [print(t['path']) for t in d.get('tree',[])]"
```

**Output:** complete file/folder list. **Always do this FIRST** — it answers "what files exist" before you waste tokens fetching the wrong ones.

**Pitfall:** If repo has no `main` branch, try `master` or probe via `/repos/{o}/{r}` to get `default_branch` first. If response is 403, use the web UI path: `https://github.com/{o}/{r}/tree/main` (no auth needed for public repos).

### Phase 2 — Parallel manifest fetch (1 round-trip, ~15s)

**Critical rule: batch ALL high-signal files into ONE `mcp__exa__web_fetch_exa` call.**

Signal priority for ANY repo (skip what doesn't exist):
1. `README.md` — always
2. `SKILL.md` / `AGENTS.md` / `CLAUDE.md` / `ARCHITECTURE.md` — if exists
3. `install.md` / `SETUP.md` / `CONTRIBUTING.md` — if exists
4. `pyproject.toml` / `package.json` / `Cargo.toml` / `go.mod` — dependencies + version
5. ALL helper scripts under `helpers/`, `scripts/`, `tools/`, `bin/` — fetch in batches of 5-8 per call
6. `.gitignore` — REVEALS NAMING CONVENTIONS (everything gitignored is a session artifact)

```python
# Call 1: high-signal docs + entry points
mcp__exa__web_fetch_exa(urls=[
    "https://raw.githubusercontent.com/{o}/{r}/main/README.md",
    "https://raw.githubusercontent.com/{o}/{r}/main/SKILL.md",
    "https://raw.githubusercontent.com/{o}/{r}/main/install.md",
    "https://raw.githubusercontent.com/{o}/{r}/main/pyproject.toml",
    "https://raw.githubusercontent.com/{o}/{r}/main/.gitignore",
])

# Call 2: helper scripts (if any)
mcp__exa__web_fetch_exa(urls=[
    "https://raw.githubusercontent.com/{o}/{r}/main/helpers/transcribe.py",
    "https://raw.githubusercontent.com/{o}/{r}/main/helpers/render.py",
    # ...up to 8 per call
])
```

**Pitfall:** `web_extract` may fail with DuckDuckGo backend — use `mcp__exa__web_fetch_exa` instead. GitHub's HTML pages get truncated; raw URLs are clean.

### Phase 3 — Cross-check naming conventions from 3 sources

The directory tree from SKILL.md LIES about exact filenames. Cross-check with 2 other sources:

1. **Helper code f-strings** — grep for `f"seg_{`, `f"base_{`, `Path(...) / f"..."` patterns. These reveal EXACT filename patterns with zero-padding, separators, etc.
2. **`.gitignore` entries** — every line is a real output file. e.g. `preview.mp4`, `final.mp4`, `clips_graded/`, `edl.json`, `project.md` → all real artifacts.
3. **SKILL.md directory tree** — the IDEAL layout, may be aspirational.

**Rule: trust the helper code + .gitignore over SKILL.md text.** If they conflict, the code wins.

### Phase 4 — Map workflow → files (build the master table)

For each phase in the user-facing workflow (Setup / Inventory / Plan / Render / Verify), produce a row:

| Phase | Helper / Action | Files created | Persist? | Cache? |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

Column sources:
- **Helper/Action**: from helper script docstrings + main() argparse
- **Files created**: from helper script's `Path(...) / f"..."` and `mkdir()` calls
- **Persist?**: yes if writes to disk, no if temp file unlinked at end
- **Cache?**: yes if helper checks `if path.exists(): skip`

### Phase 5 — Extract design patterns (5-10 lessons)

Grep for: `HARD RULE`, `NEVER`, `MUST`, `Rule N`, `Pitfall`, `# Rule`, `## Rules`, `# ⚠️`.

For each pattern found:
- Quote the EXACT rule (don't paraphrase)
- Note WHY it exists (the silent failure mode it prevents)
- Translate to "how to apply this in MY project"

**Goal:** the final report is a "design patterns cheat sheet" anh can apply to his OWN projects, not just a description of someone else's repo.

## Output Format

Save to `/tmp/{repo-slug}-workflow.md` (temp, ephemeral) OR to wiki if user says "save to wiki".

Structure (5 sections, ~3000 words):
1. **Overview** — what the repo IS, language breakdown, license, stars (1 paragraph)
2. **File structure per [workflow action]** — comprehensive table with all files generated
3. **Naming conventions** — patterns extracted from code + .gitignore, with code citations
4. **Workflow steps** — phase-by-phase breakdown with input → output
5. **Key insights for [user's project]** — 5-10 reusable patterns, ranked by applicability

Bilingual: write in Vietnamese if user's query was Vietnamese (most likely).

## Pitfalls (GitHub Repo Recon)

- **❌ Skip Phase 1 (tree map)** — you'll fetch random files instead of the structural ones. ALWAYS start with tree map.
- **❌ Fetch files serially** — 5 separate `web_extract` calls = 5 round-trips. Batch into one `web_fetch_exa` with multiple URLs.
- **❌ Trust SKILL.md directory tree over code** — SKILL.md is documentation; code is truth. Always grep helper scripts for actual `f"..."` filename patterns.
- **❌ Skip the skill for "đọc skill này" requests** — when user shares a GitHub URL + asks "đọc skill này" / "cái này là gì" / "cách nó hoạt động", the deliverable is a Vietnamese digest of the SKILL.md (what it does, key design patterns, comparison to existing workflow), NOT a full file-map recon report. BUT still run Phase 1 (tree) + Phase 2 (fetch SKILL.md + AGENTS.md) — just skip Phase 3-4 (filename cross-check + full workflow table) unless user wants depth. Real case 27/07 23:30: user asked "đọc skill này" pointing at bradautomates/claude-video → em cloned full repo + read SKILL.md + summarized Vietnamese with 4-tier detail mode + comparison table. Output ~1500 chars, 3-5 min end-to-end, anh satisfied. Avoid wasting time on 6-page recon report when user just wants the digest.
- **❌ Skip .gitignore** — it's a FREE list of every output file the project considers "session artifact". Best naming convention source.
- **❌ Fabricate filename patterns** — if you didn't see it in code, don't put it in the table. Use "unclear" or "see code line N" instead.
- **❌ Read only README** — README is marketing. SKILL.md + helper scripts are substance. README gets you ~20% of the truth.
- **❌ Use `web_extract` with DuckDuckGo backend** — it returns `success: false` for GitHub. Use `mcp__exa__web_fetch_exa` exclusively for raw.githubusercontent.com URLs.
- **❌ Skip the workflow phase table** — "files per workflow action" is the most valuable output. If you only list all files in one table, you miss the SEQUENCE.
- **❌ Hallucinate helper scripts** — if tree map shows 6 helpers, don't claim 10. If a file path is in README but not in tree, it's aspirational/old.
- **❌ Report "no examples/"** — some repos have no examples dir. Don't invent one to fill the table. State "no examples directory" and move on.

### Phase 6 pitfalls — Clone + install upstream skills

- **❌ `cp -rf` trực tiếp đè lên `~/.hermes/skills/`** — khi repo upstream đặt tên trùng với skill user-owned (ví dụ `heygen-com/hyperframes` có 19 skill đặt tên ngắn: `hyperframes`, `hyperframes-cli`, `media-use`, `motion-graphics`, ...), overwrite sẽ xóa Tuấn-specific cookbook (case `creative/hyperframes` 83.8KB). ALWAYS clone vào path đặt tên phiên bản (`/Volumes/Storage-1/Hermes/skills/<repo>-<version>/`) rồi symlink từng entry lên `~/.claude/skills/` (nơi `~/.hermes/skills/` chốt). User-owned cookbook sống ở `creative/<name>/` (category-prefixed) không bị symlink đè.
- **❌ Quên backup bản local trước sync** — symlink lần đầu là dễ, rollback thì không. Trước khi symlink, `mv` entry cũ trong `~/.claude/skills/` sang `/Volumes/Storage-1/Hermes/archive/<repo>-pre-<version>-<STAMP>/`. Backup timestamp + diff hint giúp trace nếu upstream update gây regression.
- **❌ `git pull --ff-only` lên `~/.hermes/skills/` working tree** — repo upstream không có git remote gắn vào `~/.hermes/skills`. Clone nằm ở `/Volumes/Storage-1/Hermes/research/<repo>` (read-only reference), Hermes nhận snapshot immutable ở `/Volumes/Storage-1/Hermes/skills/<repo>-<version>/`. Update = clone lại + replace folder + backup cũ.
- **❌ Không verify hash sau install** — symlink tới snapshot sai → agent load skill sai mà không biết. Sau install, bắt buộc chạy SHA-256 diff source vs snapshot (expect `0 mismatch`), `find … -name SKILL.md | wc -l == 19` (hoặc count upstream manifest trong `skills-manifest.json`), `python3 -c "import yaml; yaml.safe_load(open(...))"` cho mỗi `SKILL.md` để confirm YAML frontmatter valid.
- **❌ Skip `npx <cli> --version` smoke test** — package upstream có thể cần Node ≥22, FFmpeg, system Chrome. Sau install, run `npx <cli>@<version> --version` (hoặc `npx --yes hyperframes@0.7.83 init smoke --non-interactive --example blank --resolution portrait` rồi `lint` + `check --json --no-contrast`). Nếu exit ≠0 trên máy anh, log evidence rồi flag, không pretend pass.
- **❌ Không log install** — anh cần audit trail. Mỗi file trong snapshot + mỗi entry trong backup phải được `python3 /Volumes/Storage-1/Hermes/scripts/log_helper.py append <path> --reason "..." --action create`. Đối chiếu `~/.hermes/memories/hermes-file-edit-logging` skill.
- **❌ Tự ý merge nội dung upstream + user cookbook** — recipe "merge cả 2" trong skill collision workaround (`tiktok-pipeline-studio/references/hyperframes-skill-collision-workaround-2026-07-18.md`) là LOW priority. Mỗi lần upstream bump → merge conflict thủ công → tốn hơn giữ tách. Default = tách layer, user cookbook giữ nguyên, dùng full path khi cần (`skill_view(name='creative/hyperframes')`).

## Verification (run before reporting done)

```bash
# Did you fetch the real tree?
test -s /tmp/repo-tree.txt && echo "tree OK"

# Did you fetch the real code?
grep -c "f\"seg_" /tmp/helpers-render.py  # should be > 0 if render.py was fetched

# Did you cite .gitignore for naming?
grep -c "^preview.mp4$\|^final.mp4$" /tmp/gitignore.txt  # should be > 0

# Cross-check: every file mentioned in table should appear in tree map
python3 -c "
import json
tree = json.load(open('/tmp/repo-tree.json'))
mentioned = ['preview.mp4', 'final.mp4', 'edl.json', 'project.md', 'master.srt']
real = [p['path'] for p in tree['tree']]
for m in mentioned:
    print(f'{m}: {\"FOUND\" if any(m in r for r in real) else \"MISSING in tree\"}')
"

# Phase 6: SHA-256 diff source vs snapshot (expect 0 mismatch)
python3 -c "
import hashlib
from pathlib import Path
src=Path('/Volumes/Storage-1/Hermes/research/<repo>/<skill-dir>')
dst=Path('/Volumes/Storage-1/Hermes/skills/<repo>-<version>/<skill-dir>')
mism=[(r.name) for r in src.rglob('*') if r.is_file() and not (dst/r.relative_to(src)).exists() or hashlib.sha256(r.read_bytes()).digest()!=hashlib.sha256((dst/r.relative_to(src)).read_bytes()).digest()]
print('MISMATCH',len(mism))
"

# Phase 6: every SKILL.md has valid YAML + unique name
python3 -c "
import yaml,re
from pathlib import Path
names=[]
for p in Path('/Volumes/Storage-1/Hermes/skills/<repo>-<version>').glob('*/SKILL.md'):
    t=p.read_text(); assert t.startswith('---')
    fm=yaml.safe_load(t[3:t.find('\n---',3)])
    names.append(fm['name'])
assert len(names)==len(set(names))
"

# Phase 6: symlink chain resolves
for n in <upstream-skill-names>:
    p=Path('/Users/tuananh4865/.hermes/skills')/n
    assert p.is_symlink() and p.resolve().is_dir(), n
"
```

If any "MISSING" → either the file is created by runtime code (not in tree as a committed file) OR you fabricated it. Re-check Phase 1.

## Real Case Implementation (2026-07-18)

**Trigger:** User asked "Research chi tiết quy trình edit video của repo browser-use/video-use - file nào được tạo ra cho mỗi video edit".

**Workflow executed:**
1. Phase 1: `curl /git/trees/main?recursive=1` → 31 paths (helpers/, skills/, root files)
2. Phase 2 batch 1: README + SKILL.md + install.md + pyproject.toml → 1 round-trip
3. Phase 2 batch 2: helpers/render.py + transcribe.py + pack_transcripts.py + pyproject.toml → 1 round-trip
4. Phase 2 batch 3: helpers/transcribe_batch.py + timeline_view.py + grade.py → 1 round-trip
5. Phase 3: extracted `seg_NN_<src>.mp4`, `<stem>_<start>.<end>.png`, `slot_<id>/` from code; cross-checked with .gitignore entries
6. Phase 4: built 16-row file map across 6 workflow phases
7. Phase 5: extracted 10 design patterns (text-first transcript, EDL as schema, per-segment extract, subtitles LAST, 30ms fades, cache transcripts, self-eval before present, 12 hard rules vs artistic freedom, parallel sub-agents)

**Output:** `/tmp/video_use_workflow.md` (150 lines, 13KB) — table of 16 files, naming convention table, 6-phase workflow, 10 key insights for Hermes-Edit.

**Time:** ~6 minutes end-to-end. 3 parallel fetch calls (vs 8+ if serialized). 100% accuracy vs code (no fabrication).

## Real Case Implementation (2026-07-30)

**Trigger:** User asked "Phân tích, học repo và clone skill trong repo này về" pointing at `https://github.com/heygen-com/hyperframes`. Deliverable = Vietnamese analysis + clone skill pack into Hermes.

**Workflow executed:**
1. Phase 1: `git ls-remote --heads` + `git ls-tree -r --name-only` → 4,839 paths, 19 skill directories, 889 skill files
2. Phase 2 batch: fetched `README.md`, `AGENTS.md`, `CLAUDE.md`, `skills-manifest.json` + `skills/hyperframes/SKILL.md`, `skills/hyperframes-core/SKILL.md`, `skills/hyperframes-cli/SKILL.md`, `skills/hyperframes-animation/SKILL.md` trong 1 round-trip → confirmed `5244dde5...` / `v0.7.83`
3. Phase 5 patterns: router → core contract → animation runtime adapters → CLI loop → creative direction → registry blocks
4. Phase 6 install: `git clone --depth 1` vào `/Volumes/Storage-1/Hermes/research/heygen-hyperframes/`, `cp -a` sang `/Volumes/Storage-1/Hermes/skills/heygen-hyperframes-v0.7.83/`, backup bản cũ vào `/Volumes/Storage-1/Hermes/archive/hyperframes-pre-v0.7.83-20260730-092938/`, symlink 19 entry lên `~/.claude/skills/` (nơi `~/.hermes/skills/` chốt qua chain symlink). User-owned cookbook `~/.hermes/skills/creative/hyperframes/SKILL.md` (83858 bytes) giữ nguyên vì nằm category-prefixed.
5. Verify: SHA-256 diff source vs snapshot = `0 mismatch` (889 files); `hermes skills list` thấy đủ 19 upstream skill với `state: enabled`; custom cookbook SHA256 đối chiến `0a39157fc374…` không đổi; `npx --yes hyperframes@0.7.83 init --non-interactive --example blank --resolution portrait` exit 0, lint exit 0, check exit 0.
6. Wiki: `/Volumes/Storage-1/Hermes/wiki/raw/articles/heygen-hyperframes-v0.7.83-source-2026-07-30.md` (raw source pointer) + `/Volumes/Storage-1/Hermes/wiki/concepts/heygen-hyperframes-v0.7.83-skill-clone-2026-07-30.md` (8.7KB Vietnamese analysis với routing table cho workflow của anh).
7. Adversarial verifier (subagent isolated context): PASS 3-layer với 19 SKILL.md hash-perfect match, custom cookbook preserved, mtime chứng minh pre-clone.

**Output:** snapshot `heygen-hyperframes-v0.7.83` (889 files), backup archive, 5 file log entries, 2 wiki pages.

**Lesson encoded (PITFALL appended to this skill):** upstream skill đặt tên ngắn (`hyperframes`, `media-use`, ...) đụng user cookbook; clone vào path `<repo>-<version>/` rồi symlink entry lên `~/.claude/skills/` để không xóa Tuấn-specific cookbook. Backup + SHA-256 + symlink chain verification là gate bắt buộc.

**Reference:** `references/clone-upstream-skills-into-hermes.md` — Phase 6 condensed runbook (commands cookbook + failure modes + handoff checklist).

## Related Skills

- `ml-model-comparison-report` — research a MODEL (weights/benchmarks), not a repo
- `youtube-channel-audit` — research a YOUTUBE CHANNEL, not a code repo
- `third-party-tool-install` — INSTALL a CLI on local Mac
- `source-driven-development` — use official docs WHILE CODING your own project
- `clone-and-adapt-competitor` — adapt a competitor's strategy (business-level), reverse-engineer after this skill
- `wiki-product-ground-truth` — every claim cần citation [N]; anh mandate 18/07
- `hermes-file-edit-logging` — NDJSON audit log cho mỗi file edit; bắt buộc khi install skill mới