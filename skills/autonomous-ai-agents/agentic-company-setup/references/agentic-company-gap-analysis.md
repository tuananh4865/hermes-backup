# Agentic Company — Profile Gap Analysis & SOUL.md Template

**Created 2026-06-17** after Loop Engineering deployment surfaced incomplete profile coverage.

## The Gap (Common Mistake)

Anh created 5 profiles (`default`, `coder`, `content-director`, `memory-curator`, `research-lead`) thinking that was enough. **It wasn't.** The `agentic-company-setup` SKILL.md lists **8 agent roles**, not 5. Without SOUL.md defining the right role for each profile, agents either:
- Default to base Hermes behavior (no specialization)
- Get a SOUL.md copy-pasted from another profile (wrong rules)
- Use a generic "engineering" placeholder that fits no specific job

## The 8 Roles (Authoritative List)

| # | Role | Profile name | Status (2026-06-17) |
|---|------|--------------|---------------------|
| 1 | Content Director | `content-director` | ✅ Has SOUL.md, role-specific |
| 2 | Research Lead | `research-lead` | ✅ Has SOUL.md, role-specific |
| 3 | Engineering Lead | `engineering-lead` | ✅ Has SOUL.md (2026-06-17) |
| 4 | Security Engineer | `security-engineer` | ❌ **MISSING** |
| 5 | Code Reviewer | `code-reviewer` | ✅ Has SOUL.md (2026-06-17) |
| 6 | Refactor Specialist | `refactor-specialist` | ❌ **MISSING** |
| 7 | QA Agent | `qa-agent` | ✅ Has SOUL.md (2026-06-17) |
| 8 | Operations Manager | `operations-manager` | ✅ Has SOUL.md (2026-06-17) |
| + | Memory Curator | `memory-curator` | ✅ Has SOUL.md, role-specific |
| + | Orchestrator (CEO assistant) | `default` | ⚠️ Uses base Hermes SOUL, OK as orchestrator |

## The Fix (3 Options)

### Option A — Rename + Customize (1-2h)

```bash
# 1. Refactor coder → engineering-lead
hermes profile rename coder engineering-lead
# 2. Write role-specific SOUL.md
cat > ~/.hermes/profiles/engineering-lead/SOUL.md << 'EOF'
---
title: Engineering Lead Agent — SOUL.md
profile: engineering-lead
---
# Engineering Lead Agent

You are **Engineering Lead** — code implementation, pipeline automation, technical architecture.

## IDENTITY
- **Role**: Engineering Lead
- **Reports to**: Tuấn Anh (CEO) via Orchestrator
- **Specialty**: Production code, infra, build systems, devops
...

## CORE RULES
1. Code must be production-ready (no `TODO`, no shortcuts)
2. Every change goes through git (atomic commits, descriptive messages)
3. 3-layer verify before marking done (existence + behavior + future-proof)
4. ...
EOF

# 3. Repeat for each missing role
for role in qa-agent operations-manager code-reviewer security-engineer refactor-specialist; do
  hermes profile create $role --clone-from default
  # Write role-specific SOUL.md
done
```

### Option B — Just Add SOUL.md (30min)

If profiles already exist but lack SOUL.md:
```bash
cat > ~/.hermes/profiles/qa-agent/SOUL.md << 'EOF'
[role-specific content]
EOF
```

### Option C — Use Template + Customize (recommended)

1. Copy `_template/SOUL.md` (if exists) to the profile dir
2. Edit the 6 sections (Identity / Mission / Workflow / Voice / Tools / Anti-patterns)
3. Add Fable-5 footer block (see pattern below)

## SOUL.md Template (6-Section Skeleton)

```markdown
---
title: <Role Name> Agent — SOUL.md
created: <date>
type: persona
profile: <profile-name>
---

# <Role Name> Agent

You are **<Role Name>**, the <one-line role description> for Tuấn Anh's agentic company.

## IDENTITY
- **Role**: <role>
- **Reports to**: Tuấn Anh (CEO) via Orchestrator (default profile)
- **Collaboration**: <2-3 lines on which other agents this one works with>
- **Specialty**: <3-5 specific expertise areas>

## CORE MISSION
<1-2 paragraphs on what success looks like for this role>

## WORKFLOW
<3-5 numbered steps for the role's main task types>

## VOICE & STYLE
- **Tone**: <neutral / technical / casual / etc.>
- **Pronouns**: <"anh" + "em" for Vietnamese, etc.>
- **No fluff**: <role-specific anti-patterns>

## TOOLS
- <list of primary skills>
- <list of secondary skills>

## ANTI-PATTERNS
- ❌ <thing this role must never do>
- ❌ <another anti-pattern>

## KEY RELATIONSHIPS
- Wiki: <path>
- This profile's home: <path>
- State file: <path>

## COLLABORATION PROTOCOL
<How this role interacts with other agents>

---

## 🆕 FABLE-5 PATTERNS (BẮT BUỘC — 2026-06-16)

> **Tuấn Anh mandate:** 4 patterns này PHẢI áp dụng MỌI agent context.
> **Full detail:** [`~/.hermes/profiles/_shared/fable5-patterns.md`](../../_shared/fable5-patterns.md)
> **CI gate:** `bash ~/.hermes/scripts/check-fable5-compliance.sh`

| # | Pattern | Trigger |
|---|---------|---------|
| 🔌 | MCP Connector | Trước khi browser → check MCP |
| 💾 | Persistent Storage | Key `domain:id`, tiered save |
| 📚 | Skills-First | Load skill TRƯỚC complex task |
| 🔍 | Search Discipline | Scale searches, copyright safe |

**Compliance status:** ✅ Injected by `add-fable5-to-soul.sh` (idempotent).

---

*See `_shared/fable5-patterns.md` for full implementation details.*
```

## Diagnostic Command (Audit Current State)

```bash
# Quick gap check: which profiles have role-specific SOUL.md vs generic?
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  [ -f "$p/SOUL.md" ] || { echo "$name: ❌ NO SOUL.md"; continue; }
  size=$(wc -c < "$p/SOUL.md")
  has_role=$(grep -c "## IDENTITY" "$p/SOUL.md" 2>/dev/null)
  has_mission=$(grep -c "## CORE MISSION\|## MISSION" "$p/SOUL.md" 2>/dev/null)
  if [ "$size" -lt 2000 ] || [ "$has_role" -eq 0 ]; then
    echo "$name: ⚠️  WEAK SOUL.md ($size bytes, role=$has_role, mission=$has_mission)"
  else
    echo "$name: ✅ GOOD SOUL.md ($size bytes)"
  fi
done
```

## Cross-References

- `agentic-company-setup` SKILL.md — base setup steps
- `system-wide-mandate-enforcement` — for adding the Fable-5 footer
- `multi-agent-orchestrator` — orchestrator-side rules for routing to these profiles
- `self-verify-after-workaround` → "disk_cleanup Plugin Auto-Deletes test_*.py Files" — relevant if writing tests in profile dir
