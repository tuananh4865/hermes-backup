---
name: agent-skill-authoring
description: Author skills so lessons enforce, not sit in refs.
version: 0.1.0
author: Hermes
metadata:
  hermes:
    tags: [Meta-Skill, Authoring, Skill-Maintenance, Workflow-Rules]
---

# Agent Skill Authoring — workflow-rules enforce, references alone don't

Author or patch Hermes Agent skills so lessons actually take effect across sessions. Distilled from real failures (17/07: 32/33 TikTok clips missing speed 1.3x despite 14/07 references existing).

## When to Use

- Patching or creating a workflow skill (FFmpeg pipeline, content script, batch processor)
- Pitfall or lesson needs to land DURING the next session, not just sit in `references/`
- Something broke twice despite references documenting the fix
- User escalates with a question like "không có trong skill à?" — references-only lesson drifted

## Prerequisites

- Skill class covers multi-step workflow (not one-shot lookup)
- Real failure data exists showing lesson was learned but not enforced
- Hermes skill-authoring standards: 60-char description limit, version bump per major edit, hardline description rule

## How to Run

**Frame through Hermes tools.** Invoke `skill_view` to read existing skill before patching. Use `skill_manage(action='patch')` for surgical edits, `skill_manage(action='edit')` for full rewrites. Use `skill_manage(action='write_file')` for references/templates/scripts.

When **choosing action**: lightest intervention that catches the lesson.

## Quick Reference

| Path/Field | Rule |
|---|---|
| `description` | ONE sentence ≤60 chars (truncated at 60) |
| `version` | Bump 0.1→0.2 patch, 0.X.0 minor lesson |
| `author` | Literal `Hermes` — NEVER use OS user / git / probe |
| `frontmatter` | Yaml, name lowercase-hyphen ≤64 |
| HARD RULE block | Required for workflow-critical rules |
| `references/` | Session-specific detail, protocol docs |
| `templates/` | Starter files meant to copy + modify |
| `scripts/` | Statically re-runnable (verify, probes) |

## Procedure

### Step 1 — Identify the load-bearing rule

1. Re-read the lesson: is it **WORKFLOW-CRITICAL** (must execute every time) or **REFERENCE-ONLY** (lookup when stuck)?
2. Workflow-critical → MUST go in HARD RULE block at top of SKILL.md
3. Reference-only → `references/<topic>.md` is enough

**Decision tree:**
```
Lesson: ?
├── Will next session repeat the same mistake WITHOUT seeing this?
│   ├── YES → HARD RULE in SKILL.md intro
│   └── NO  → references/<topic>.md OK
├── Does it apply every time the skill loads?
│   ├── YES → HARD RULE + body section
│   └── NO  → references/<topic>.md
└── Is it workflow-step or domain knowledge?
    ├── STEP       → intro HARD RULE
    └── KNOWLEDGE  → references/
```

Real case 17/07: "Speed 1.3x mandatory" was in `references/lesson-speed-13x-mandatory-2026-07-14.md` (14/07), but skill workflow had no step enforcing it. Result: 32/33 clips shipped without speed. **Lesson: reference ≠ enforcement.**

### Step 2 — HARD RULE block format

In SKILL.md, place immediately after the intro description (before the first H1):

```markdown
> **🚨 [PITFALL #N] (NEW YYYY-MM-DD) — [short title]:** [one-line description with concrete trigger + consequence]. Workflow: see section below.
```

Three rules:
- Must say "workflow" or "step" to signal it's a procedure, not theory
- Must include the fix in one line (not just "see references")
- Must use 🚨 emoji so it catches eye in a scrolled skill list

### Step 3 — Body section format

For each HARD RULE, add body section following this template:

```markdown
## 🚨 Lesson #N FIRST-CLASS: [title — match HARD RULE]

**Context:** [real case with date + clip/script identifier]

**Quy tắc vĩnh viễn:**
1. [Concrete rule 1]
2. [Concrete rule 2 — must be EXECUTABLE, not vague]

**Quy trình N bước:**
[copy-paste-exact commands, env, file paths]

**Anti-pattern ❌:**
- [anti-pattern 1 — what NOT to do]
- [anti-pattern 2]

**Real case YYYY-MM (proves lesson):**
[concrete failure → concrete fix → result]
```

### Step 4 — Verify the patch stuck

After patching, grep skill to confirm keyword appears in intro:

```python
import subprocess
r = subprocess.run(["grep", "-c", "PITFALL #N", skill_path])
assert r.stdout.strip() >= 2, f"PITFALL #N missing from skill"
```

Then `skill_view(name)` and read the first 50 lines — HARD RULE block must be visible.

### Step 5 — Bump version + author

If rule is major (new HARD RULE added), bump version:

```yaml
version: X.Y.Z  # was X.Y.Z-1
```

Update `author` to record who added:

```yaml
author: 'Tuấn Anh + Hermes Agent (vX.Y.Z — YYYY-MM-DD add PITFALL #N [title])'
```

Then update description (≤60 chars) — must include the NEW rule prominently because that's all the skill index loads.

## Pitfalls (Skill Authoring)

- **❌ Reference-only lesson fails to land** — next session won't `cat references/`. Enforce via HARD RULE intro.
- **❌ Description > 60 chars** — system truncates silently after char 60. Anything important must be in chars 1-60.
- **❌ HARD RULE without body section** — agent sees the rule but doesn't know HOW to apply. Always pair with workflow.
- **❌ Patching outside the loaded skill** — agent will fix one bug but miss the connected lesson (e.g. fixing speed but not lint check, OR fixing lint check but not speed).
- **❌ \"Author: Hermes\" pattern leak** — NEVER pull author from OS user/git config. Skill gets shared; privacy leak.
- **❌ Combining update + new HARD RULE in one patch** — review PRs become impossible. One HARD RULE per version bump.
- **❌ Anti-pattern without concrete fix** — "don't do X" without "do Y instead" is useless.
- **❌ New skill for every new lesson** — drift to 100 narrow skills. PATCH umbrella class skill instead.

## Verification

```bash
# Run this after every skill patch:
grep -c "PITFALL #N" SKILL.md       # must be ≥ 2 (intro + body)
wc -l SKILL.md                       # note size growth
head -60 SKILL.md | grep "PITFALL"   # HARD RULE in first 50 lines? if not — wrong placement
```

If HARD RULE not visible in first 50 lines → intro placement is wrong → re-patch.

## Related

- [[tiktok-video-editor]] — concrete patched skill (v3.28.0) using this methodology
- `references/lesson-21-false-start-scan-protocol.md` etc. — examples of when references are correct
- Hermes SKILL.md authoring standards (loaded via `skill_view`)
