---
name: skill-self-improve
description: Improve skills through patch-only updates - never rewrite full skills, only patch changed portions
version: 1.0.0
category: lifecycle
platforms: [macos, linux]
created: 2026-04-14
tags: [skill-maintenance, self-improvement, patch-only, skills]
requires_toolsets: [terminal]
---

# Skill Self-Improve

**Skills evolve. But never rewrite. Always patch.**

This skill ensures skills improve through targeted patches, not full rewrites.

---

## The Rule

```
NEVER rewrite a full skill.
ALWAYS patch only what changed.

Reason: Full rewrites risk breaking working parts.
        Patches preserve working code while fixing issues.
```

---

## When to Improve a Skill

1. **Better approach discovered** — Found a more efficient way
2. **Incomplete** — Skill missing important details
3. **Incorrect** — Skill contains wrong information
4. **Outdated** — Skill no longer reflects current reality
5. **Obsolete** — Part of the skill is no longer relevant

---

## The Patch Workflow

### Step 1: Identify the Issue

```
Questions:
- What specifically is wrong?
- What specifically should change?
- Is this isolated or widespread?

If isolated → Patch
If widespread → Consider rewriting (rare)
```

### Step 2: Locate the Exact Text

```
Find the OLD text you want to replace.
Must be:
- Unique in the file
- Exact (copy-paste)
- Includes enough context for uniqueness
```

### Step 3: Create the Patch

```bash
skill_manage(
  action='patch',
  name='{skill-name}',
  old_string='{exact old text to find}',
  new_string='{exact new text to replace}',
  replace_all=false  # or true if intentional
)
```

### Step 4: Verify

```
After patch:
1. Read the updated skill
2. Confirm change looks correct
3. Confirm no unintended changes
4. Confirm other parts still intact
```

---

## Patch Examples

### Example 1: Improving a Step

```
SKILL: setup-python-project

OLD:
2. python3 -m venv venv

NEW:
2. python3 -m venv venv --system-site-packages
```

Patch command:
```bash
skill_manage(
  action='patch',
  name='setup-python-project',
  old_string='2. python3 -m venv venv',
  new_string='2. python3 -m venv venv --system-site-packages'
)
```

### Example 2: Adding a Trigger Condition

```
OLD:
## When to Use
Starting a new Python project.

NEW:
## When to Use
- Starting a new Python project
- Resetting a corrupted venv
- Setting up CI/CD environment

NEW:
## When to Use
Starting a new Python project from scratch.
Setting up CI/CD environments.
```

### Example 3: Fixing Incorrect Info

```
OLD:
pip install requirements.txt

NEW:
pip install -r requirements.txt
```

---

## When Full Rewrite is OK

**Only in these cases:**

1. **Complete redesign** — The entire skill concept is wrong
2. **Major version** — Skill is now fundamentally different
3. **Format change** — Template structure changed

**Even then, consider:**
- Can the old skill be archived instead?
- Can you create a new skill instead?

---

## Archive vs. Delete vs. Patch

### Archive (Preferred)
```
If skill is obsolete but historically interesting:
1. Rename: skill-name → skill-name.archived
2. Add note: "# Archived: {date}\n# Reason: {reason}"
3. Keep for reference
```

### Delete (Rare)
```
Only if:
- Skill is actively harmful
- Completely duplicates another skill
- User requests deletion
```

### Patch (Always)
```
Default action for improvements.
Preserves history.
Minimizes risk.
```

---

## Quality Checklist

- [ ] Change is isolated (not rewriting entire skill)
- [ ] Old text is exact (copy-pasted)
- [ ] New text is correct
- [ ] No unintended changes
- [ ] Other parts still intact
- [ ] Verified after patch

---

## Integration

- Use [[skill-from-experience]] — Creates new skills
- Use [[memory-manage]] — Updates memory index
- Use with [[periodic-nudge]] — Triggered by self-reflection

---

## Related

- [[skill-from-experience]] — Create new skills
- [[periodic-nudge]] — Trigger improvement
- [[memory-manage]] — Update memory
