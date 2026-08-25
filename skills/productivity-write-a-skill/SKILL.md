---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
---

# Writing Skills

## Process

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** - create:
   - SKILL.md with concise instructions
   - Additional reference files if content exceeds 500 lines
   - Utility scripts if deterministic operations needed

3. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
---

# Skill Name

## Quick start

[Minimal working example]

## Workflows

[Step-by-step processes with checklists for complex tasks]

## Advanced features

[Link to separate files: See [REFERENCE.md](REFERENCE.md)]
```

## Description Requirements

The description is **the only thing your agent sees** when deciding which skill to load. It's surfaced in the system prompt alongside all other installed skills. Your agent reads these descriptions and picks the relevant skill based on the user's request.

**Goal**: Give your agent just enough info to know:

1. What capability this skill provides
2. When/why to trigger it (specific keywords, contexts, file types)

**Format**:

- Max 1024 chars
- Write in third person
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"

**Good example**:

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Bad example**:

```
Helps with documents.
```

The bad example gives your agent no way to distinguish this from other document skills.

## When to Add Scripts

Add utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability vs generated code.

## When to Split Files

Split into separate files when:

- SKILL.md exceeds 100 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

**Hard limit on SKILL.md size (lesson 2026-06-27):** `skill_manage` rejects `patch`/`edit` operations when SKILL.md exceeds **100,000 characters**. Affected as of 2026-06-27: `multi-agent-heartbeat`, `hermes-agent`, `video-download-yt-dlp`, `quality-checker`, `operations-manager-routing-audit` — all became silently stale because nightly curators can't patch them.

**Rule of thumb:** If your SKILL.md is heading past **50K characters**, split NOW. Use:
- `SKILL.md` — core instructions + quick start (target: 20-30K)
- `references/<topic>.md` — detailed sweeps, evidence tables, examples
- `templates/<name>.<ext>` — copy-and-modify boilerplate
- `scripts/<name>.<ext>` — statically re-runnable verifications

For skills that accumulate data (sweep results, log entries, accumulated lessons), add a rotation policy: archive old data to `references/YYYY-MM/` so SKILL.md stays slim.

## Review Checklist

After drafting, verify:

- [ ] Description includes triggers ("Use when...")
- [ ] SKILL.md under 100 lines
- [ ] No time-sensitive info
- [ ] Consistent terminology
- [ ] Concrete examples included
- [ ] References one level deep

## Anti-Over-Engineering Pitfalls (lesson 2026-06-23)

When user asks to "save this lesson as a skill" or "apply X system-wide", DO NOT scaffold infrastructure that the platform already provides.

### Before creating ANY new file, ask:

| Question | If NO → STOP and reconsider |
|----------|------------------------------|
| Does the framework's official docs mention this file/concept? | Don't invent (e.g. "worker", "node", "agent pool") |
| Will the new file be auto-loaded by the framework? | If not, user has to manually load it → defeats purpose |
| Does Hermes already have a mechanism for this (SOUL.md Slot 1, skill auto-load via description, memory injection)? | Use existing mechanism — don't build parallel infra |
| Is the new file doing the same job as an existing one? | Extend the existing file instead |

### Concrete patterns from real failures (2026-06-23 TikTok transcript task):

| ❌ Don't create | ✅ Use instead |
|------------------|----------------|
| `add-X-to-soul.sh` injector scripts | Put the rule in `~/.hermes/SOUL.md` (Slot 1 Tier 1 STABLE — auto-loaded every session, survives compaction) |
| `check-X-compliance.sh` CI gate scripts | CI gate does not change behavior. SOUL.md injection is the canonical enforcement. |
| `active-checklist.md` shared reference | The skill itself IS the checklist. Put reminders in `SKILL.md` body. |
| Inject same rule into 10 sub-profile SOUL.md files | Default `~/.hermes/SOUL.md` is the only one auto-loaded. Hermes does NOT load profile SOULs. |
| `~/.hermes/profiles/_shared/X.md` (when X is already in default SOUL.md) | Reference doc is fine, but NEVER claim it's "loaded" — Hermes doesn't auto-load shared files. Add "REFERENCE ONLY — not auto-loaded" header. |

### "Inject ≠ Follow" root cause (lesson 2026-06-23)

User feedback: *"Tại sao không tuân thủ dù đã lưu system-wide?"*

**Root cause:** Mandate injection into SOUL.md is PASSIVE. Agent sees the rule in context but is not FORCED to apply it. Memory fact only triggers when agent actively searches for it.

**The fix:** When patching a skill for a "read-full-request" lesson, embed the rule IN THE SKILL BODY where the work happens, NOT in a separate shared file:

- ✅ In `SKILL.md` → always loaded with skill
- ✅ In `~/.hermes/SOUL.md` (Slot 1) → always in system prompt
- ✅ In user's wiki `learned-about-tuananh.md` → durable behavioral preference
- ❌ In `~/.hermes/profiles/_shared/X.md` (alone) → not auto-loaded
- ❌ In `~/.hermes/scripts/add-X-to-soul.sh` → file system scripts are not in agent's prompt path

### Self-audit before declaring "DONE":

```
For each file I just created:
1. Will Hermes auto-load this file in a fresh session? If NO → label it "reference only"
2. Does this file duplicate an existing one? If YES → delete or merge
3. Did I verify the upstream concept exists in hermes-agent.nousresearch.com/docs? If NO → research first
4. Did the user say "over-engineered" or "too many files"? → rollback the over-engineering immediately
```

### Lesson from a real cleanup (2026-06-23):

User said: *"Nghe có vẻ hơi over engineering quá!"* after agent created:
- `~/.hermes/profiles/_shared/read-full-request.md`
- `~/.hermes/profiles/_shared/active-checklist.md`
- `~/.hermes/scripts/add-readfullrequest-to-soul.sh`
- `~/.hermes/scripts/check-readfullrequest-compliance.sh`
- 9 sub-profile SOUL.md injections (all later rolled back)

Correct behavior would have been:
1. Single edit to `~/.hermes/SOUL.md` (default — auto-loaded Slot 1)
2. Put full rule in `tiktok-transcript-pipeline/SKILL.md` (where the work happens)
3. Done. No scripts, no CI gate, no shared file, no sub-profile injections.

**Rule of thumb:** If you're creating more than 2 files for a single rule/lesson, you're probably over-engineering. Stop and ask: "Does the user need this OR do I think they need this?"

## Verify Upstream Concept Exists (lesson 2026-06-23)

**Before scaffolding anything for a new term/concept, confirm it exists in canonical source.**

For Hermes:
- Official docs: `hermes-agent.nousresearch.com/docs/`
- Source code: `github.com/NousResearch/hermes-agent`
- Check the term exists in BOTH places — if only one, it's likely user-specific terminology

**Specific check pattern:** When user says "save this system-wide" or "apply to all profiles":

```bash
# 1. Check if the framework has a built-in mechanism
ls ~/.hermes/SOUL.md  # Default profile — auto-loaded
ls ~/.hermes/profiles/*/SOUL.md  # Sub-profiles — NOT auto-loaded by default
ls ~/.hermes/skills/  # Skills — auto-loaded when description matches keywords

# 2. Check official docs for the concept
# E.g. for "system-wide mandate": search docs for "SOUL.md" loading rules

# 3. Verify prompt assembly order
# Tier 1 STABLE: SOUL.md (auto-injected every session)
# Tier 2 CONTEXT: project files (.hermes.md, AGENTS.md)
# Tier 3 VOLATILE: MEMORY.md, USER.md (rebuilt on session start)
# → Only Tier 1 is "always there". Tier 3 is "in memory but might overflow".

# 4. If term/concept doesn't exist in official docs:
#    - Surface this BEFORE building 25 files of dead infrastructure
#    - Ask user to confirm OR use the closest official concept
```

**Hermes official paths (verified 2026-06-23):**
- `~/.hermes/SOUL.md` → Slot 1 Tier 1 STABLE — always loaded
- `~/.hermes/skills/<name>/SKILL.md` → loaded when description matches keywords
- `~/.hermes/profiles/<name>/SOUL.md` → only loaded if profile is active
- `~/.hermes/profiles/_shared/*.md` → NOT auto-loaded (reference docs only)
- `~/.hermes/scripts/*.sh` → file system only, not in agent context
- `~/.hermes/hooks/<name>/` → only fires on configured events (session:start, etc.)

**Anti-pattern:** Building a custom injector script + CI gate + shared checklist for a rule that fits in 5 lines of default SOUL.md.
