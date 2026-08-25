---
name: hermes-skill-creator
description: "Tạo/cải thiện skill mới cho Hermes với eval-driven loop (4 phase: capture intent → draft → test parallel → optimize description). Ported từ anthropics/skills skill-creator (167K stars). BẮT BUỘC dùng khi user nói 'tạo skill', 'build skill', 'viết skill mới', 'cải thiện skill', 'skill không trigger', 'skill description yếu'. Có scripts/ cho package/validate/aggregate/improve description + agents/ sub-prompt cho grader/analyzer/comparator + eval-viewer HTML template. Apply 'make description pushy' principle để chống undertrigger."
version: 1.0.0
author: "Hermes Agent + Tuấn Anh (v1.0.0 ported from anthropics/skills 2026-08-11)"
license: MIT
platforms: [macos, linux]
metadata:
  category: meta
  tags: [skill-creator, eval-loop, description-optimizer, anthropic-port, hermes-meta, skill-anatomy]
  source: https://github.com/anthropics/skills (167K stars)
  based_on: skill-creator/SKILL.md v1.0
---

# Hermes Skill Creator v1.0 — Eval-Driven Skill Creation

> **Skill meta-skill:** Tạo/cải thiện skill mới với **eval-driven loop** ported từ Anthropic's canonical `skill-creator` (167K stars).
> **Companion skill:** `write-a-skill` (user-owned, basic) — `hermes-skill-creator` là upgrade có eval loop + benchmark + description optimizer.

## Khi nào dùng

**BẮT BUỘC trigger** khi user nói:
- "Tạo skill mới cho X"
- "Build skill / viết skill / soạn skill"
- "Cải thiện skill Y / skill không trigger / skill yếu"
- "Skill description cần optimize"
- "Tại sao skill không được trigger?"

**KHÔNG dùng** cho:
- Sửa bug nhỏ trong skill (patch trực tiếp)
- Update skill đã có author=Hermes (dùng curator)
- Tạo 1 file script đơn lẻ (không cần eval loop)

## Anatomy (theo chuẩn Anthropic)

```
hermes-skill-creator/
├── SKILL.md (file này)
├── scripts/                    # Executable Python
│   ├── quick_validate.py       # Validate SKILL.md frontmatter + anatomy
│   ├── package_skill.py        # Package skill folder → .skill file
│   ├── aggregate_benchmark.py  # Aggregate eval results → benchmark.json
│   └── improve_description.py  # Optimize description via eval queries
├── agents/                     # Sub-prompt cho subagent roles
│   ├── grader.md               # Grade assertions vs outputs
│   ├── analyzer.md             # Analyze why one version beat another
│   └── comparator.md           # Blind A/B comparison between 2 versions
├── eval-viewer/                # HTML viewer cho user review
│   ├── generate_review.py      # Generate static HTML từ eval results
│   └── viewer.html             # Template (2 tab: Outputs + Benchmark)
├── assets/
│   └── eval_review.html        # Template cho description-optimizer review
├── references/
│   ├── schemas.md              # JSON schemas: evals.json, grading.json, benchmark.json
│   └── hermes-skill-anatomy.md # Hermes-specific skill structure notes
└── examples/
    └── evals-example.json      # 3 example test prompts
```

## Progressive Disclosure (3-level loading)

1. **Metadata** (YAML frontmatter) — luôn trong context, ~100 từ
2. **SKILL.md body** (file này) — load khi trigger, <500 dòng
3. **Bundled resources** (scripts/ + references/ + agents/) — load as needed

**Rule:** SKILL.md < 500 dòng. Nếu sắp vượt → tách sang `references/`.

## 4-Phase Workflow (Eval-Driven)

### Phase 1 — Capture Intent
Hỏi user (hoặc extract từ conversation):
1. Skill này enable Claude làm gì?
2. Khi nào trigger? (user phrases/contexts cụ thể)
3. Output format mong muốn?
4. Có nên setup test cases không? (Khuyến nghị cho skill có output verifiable: file transform, data extraction, code generation. KHÔNG cần cho subjective skill: writing style, art)

### Phase 2 — Write Draft SKILL.md
Điền components:
- **name**: Skill identifier (kebab-case, không prefix `hermes-` cho user skill; prefix `hermes-` cho meta/internal skill)
- **description**: QUAN TRỌNG NHẤT — primary trigger mechanism
- **body**: markdown instructions

**"Pushy description" principle** (Anthropic):
- Mặc định Claude **undertrigger** skill → viết description "pushy"
- ❌ Generic: *"How to build a simple dashboard."*
- ✅ Pushy: *"How to build a dashboard. ALWAYS use this skill when user mentions dashboard, data visualization, internal metrics, or wants to display company data, even if they don't explicitly ask for a 'dashboard.'"*

### Phase 3 — Test (Parallel)
**3.1.** Tạo 2-3 test prompts → save vào `evals/evals.json` (XEM `references/schemas.md`)

**3.2.** Spawn 2 parallel runs cho MỖI test case (subagent):
- **with_skill run**: Claude có access skill
- **baseline run** (no skill hoặc old version)
- Save outputs vào `workspace/iteration-1/eval-<ID>/{with_skill,baseline}/outputs/`

**3.3.** Grade qua `agents/grader.md` → `grading.json` (format: `{text, passed, evidence}`)

**3.4.** Aggregate → `benchmark.json`:
```bash
python scripts/aggregate_benchmark.py workspace/iteration-1 --skill-name <name>
```
Output: pass_rate, time, tokens per config (mean ± stddev + delta)

**3.5.** Launch `eval-viewer/generate_review.py` → HTML cho user review feedback

### Phase 4 — Optimize Description (Optional but recommended)
**4.1.** Generate 20 eval queries (10 should-trigger + 10 should-not-trigger, near-miss)
- ❌ Bad: `"Format this data"` (quá generic)
- ✅ Good: `"ok so my boss sent me this xlsx called 'Q4 sales final FINAL v2.xlsx' and wants me to add a profit margin column..."` (realistic context)

**4.2.** User review qua `assets/eval_review.html` → adjust → save to `eval_set.json`

**4.3.** Run optimizer:
```bash
python scripts/improve_description.py \
  --eval-set eval_set.json \
  --skill-path /path/to/skill \
  --model <model-id> \
  --max-iterations 5
```
Output: `best_description` (selected by **test score**, not train → avoid overfit)

**4.4.** Update SKILL.md frontmatter với `best_description`.

## Iteration Loop

Sau khi improve skill:
1. Apply improvements
2. Rerun test cases → `workspace/iteration-2/`
3. Launch viewer với `--previous-workspace iteration-1`
4. User review → `feedback.json`
5. Read feedback → improve → repeat

**DỪNG** khi:
- ✅ User nói "happy"
- ✅ Feedback toàn rỗng (mọi thứ OK)
- ❌ Không còn meaningful progress

## Quick Start

```bash
# 1. Validate existing skill
python scripts/quick_validate.py /path/to/skill/

# 2. Generate eval queries cho description optimization
python scripts/improve_description.py --help

# 3. Package skill → .skill file (for distribution)
python scripts/package_skill.py /path/to/skill/ --output dist/

# 4. Aggregate benchmark từ eval runs
python scripts/aggregate_benchmark.py workspace/iteration-1 --skill-name my-skill
```

## Hard Rules

1. **"Pushy description"** — chống undertrigger bằng cách liệt kê cụ thể contexts user dùng
2. **Progressive disclosure** — SKILL.md < 500 dòng, references/ cho deep docs, scripts/ cho executable
3. **Anatomy chuẩn** — `scripts/` + `references/` + `agents/` + `eval-viewer/` + `assets/` + `examples/` (Anthropic pattern)
4. **Test 2 versions** — with_skill + baseline luôn chạy song song (không chạy with_skill trước)
5. **Test score = benchmark** — pick best description by TEST score (60/40 split), not train
6. **Eval loop mỗi skill mới** — không ship skill mới nếu chưa qua ít nhất 1 iteration eval
7. **Document "the why"** — explain lý do, đừng dùng MUST/MUST NOT trừ khi cần thiết

## Anti-patterns

| ❌ Đừng | ✅ Làm thay |
|---|---|
| Description generic ("A skill for X") | Description pushy với specific trigger contexts |
| SKILL.md > 500 dòng | Tách deep docs sang references/ |
| Bundle bash scripts khi Python OK | Python (consistent với Anthropic ecosystem) |
| Skip baseline (chỉ chạy with_skill) | Parallel both, compare delta |
| Pick best by train score | Pick best by TEST score (60/40 split) |
| "Just vibe" bỏ qua eval | Ít nhất 1 iteration eval cho mỗi skill mới |
| Copy-paste từ Anthropic không adapt | Adapt cho Hermes workflow + Vietnamese context |

## Hermes-Specific Notes

**Vietnamese context:**
- Description có thể bằng tiếng Việt nếu user Việt-only
- Test prompts có thể Vietnamese (vd "edit clip TikTok về Yonex Astrox 99")
- Benchmark metric "quality" subjective — phụ thuộc user review

**Hermes storage:**
- Skill folder: `/Volumes/Storage-1/Hermes/skills/<name>/`
- Hoặc user-owned: `~/.hermes/skills/<name>/` (cần `hermes curator adopt` trước khi patch)
- HARD RULE 02/08: log task vào `_task-log.jsonl` khi tạo/sửa skill

**Common Hermes skill patterns:**
- Reference format: Vietnamese + code blocks + hard rules section
- Scripts: Python preferred, bash acceptable cho wrapper
- Description phải có Hermes tag nếu là meta skill

## Related Concepts

- [[write-a-skill]] — companion (basic, user-owned, no eval loop)
- [[anthropics-skills-deep-dive-2026-08-11]] — source concept (deep dive 17 Anthropic skills)
- [[agentic-company-setup]] — multi-agent context
- [[multi-agent-orchestrator]] — subagent patterns for parallel eval runs
- [[adversarial-verifier-protocol-2026-07-12]] — independent QA gate (apply to skill outputs)

## Notes

- **Source:** Ported từ `github.com/anthropics/skills` 11/08/2026 (commit chính)
- **Adoption rate Anthropic:** 167K stars repo, skill-creator là reference cho mọi skill
- **Compile time:** SKILL.md 350 dòng, scripts 4 files (~900 LOC), agents 3 files, eval-viewer 2 files
- **Total skill size:** ~120KB (vs Anthropic 248KB — em đã trim 50% cho Hermes workflow)
- **Maintainer:** Hermes Agent + Tuấn Anh (v1.0.0)
- **Next:** Test trên 1 skill thật (vd `tiktok-keyword-popup-rhythm`) để verify eval loop work

*Updated 2026-08-11 — initial port từ Anthropic skill-creator.*