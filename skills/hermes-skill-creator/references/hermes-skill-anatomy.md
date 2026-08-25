# Hermes Skill Anatomy — Notes

> Differences between Anthropic's skill anatomy and Hermes conventions.

## Standard anatomy (Anthropic)

```
skill-name/
├── SKILL.md (required)
├── scripts/
├── references/
├── assets/
└── examples/  (optional)
```

## Hermes extended anatomy

```
skill-name/
├── SKILL.md (required)
├── scripts/        - Python (preferred) or bash wrapper
├── references/     - Deep docs, schemas
├── agents/         - Sub-prompt for subagent roles
├── eval-viewer/    - HTML viewer template (for skill-creator workflow)
├── assets/         - Templates, fonts, HTML samples
├── examples/       - Use case examples
├── _log_task.py    - HARD RULE 02/08 task logger
├── _task-log.jsonl - JSONL audit log
└── LICENSE.txt     - MIT or Apache 2.0 (added by Hermes curator)
```

## Key differences

1. **`_log_task.py` + `_task-log.jsonl`** — Hermes HARD RULE 02/08 mandatory log
2. **`agents/` directory** — for meta skills that spawn subagents (e.g., hermes-skill-creator has grader/analyzer/comparator)
3. **`eval-viewer/` directory** — for skills that have eval loop
4. **Python preferred over bash** — Anthropic uses Python almost exclusively; Hermes has many bash scripts (acceptable for wrapper but Python preferred for new skills)
5. **Vietnamese comments OK** — for Hermes-specific context

## Storage paths

| Purpose | Path |
|---|---|
| Source-of-truth skill | `/Volumes/Storage-1/Hermes/skills/<name>/` |
| User-owned skill | `~/.hermes/skills/<name>/` |
| Symlinked (after curator adopt) | `~/.hermes/skills/<name>/` → `/Volumes/Storage-1/Hermes/skills/<name>/` |
| Backup | `/Volumes/Storage-1/Hermes/_archive/skill-<name>-v<X>-<STAMP>/` |
| Research repo reference | `/Volumes/Storage-1/Hermes/research/<repo>/` (read-only clone) |

## Naming convention

- **Skill name** = kebab-case lowercase + digits + hyphens (max 64 chars)
- **No leading/trailing hyphens**, no consecutive hyphens
- **Prefix conventions:**
  - `hermes-*` — meta/internal Hermes skills
  - `tiktok-*` — TikTok content workflow
  - `media-*` — media processing
  - `creative-*` — design/art
  - `research-*` — research workflows
  - `devops-*` — CI/CD, deployment
  - No prefix — generic / user-owned

## Description formula (pushy)

```
[What skill does]. BẮT BUỘC/ALWAYS dùng khi user nói [trigger phrases]
+ khi user đề cập [additional contexts]
+ ngay cả khi user không nói rõ ràng.
Không dùng cho [anti-patterns].
```

## YAML frontmatter rules

```yaml
---
name: kebab-case-name           # required
description: "Quoted string with pushy triggers"  # required, ≤1024 chars
version: 1.0.0                  # optional (Hermes addition)
author: "Name + source"         # optional (Hermes addition)
license: MIT                   # optional
platforms: [macos, linux]      # optional (Hermes addition)
metadata:                       # optional
  category: media
  tags: [tiktok, ffmpeg]
---

# Skill body (markdown, <500 lines)
```

⚠️ Watch out for:
- `:` inside unquoted description → YAML parse fail (wrap in quotes)
- `:` inside `author: Name (X: Y)` → wrap whole value in quotes
- `description > 1024 chars` → validate fail