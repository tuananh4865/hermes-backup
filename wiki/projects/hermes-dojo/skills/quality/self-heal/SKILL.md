---
name: self-heal
description: Auto-fix wiki quality issues - broken links, formatting, missing frontmatter, stub content
version: 1.0.0
category: quality
platforms: [macos, linux]
created: 2026-04-14
tags: [self-healing, auto-fix, wiki-maintenance, broken-links, formatting]
requires_toolsets: [terminal]
---

# Self-Heal

**The wiki tends toward health on its own.**

This skill auto-fixes common wiki quality issues without human intervention.

---

## Auto-Fixable Issues

| Issue | Can Auto-Fix? | Method |
|-------|---------------|--------|
| Broken wikilinks | ✅ Yes | Repair or flag alternatives |
| Formatting errors | ✅ Yes | Apply standard format |
| Missing frontmatter | ✅ Yes | Add template |
| Broken external links | ⚠️ Sometimes | Update if URL changed |
| Stub content | ❌ No | Flag for expansion |
| Outdated info | ❌ No | Flag for review |
| Contradictions | ❌ No | Flag for resolution |

---

## The Self-Heal Workflow

### Step 1: Detect Issues

```
Run wiki lint:
- Check for broken links
- Check formatting
- Check frontmatter
- Check for orphans
```

### Step 2: Categorize Issues

```
For each issue found:
- Auto-fixable? → Fix immediately
- Needs review? → Flag and report
- User decision? → Ask user
```

### Step 3: Auto-Fix

```
For auto-fixable:
1. Apply fix
2. Verify fix worked
3. Log fix applied
4. Report to user
```

### Step 4: Report

```
Summary of:
- Issues found
- Issues fixed
- Issues needing review
```

---

## Auto-Fix Rules

### Rule 1: Broken Wikilinks

```
Detection:
grep -r "\[\[nonexistent\]\]" wiki/

Fix attempt:
1. Find likely target page
2. If confidence high → repair
3. If confidence low → flag

Report:
- "Fixed: [[OldPage]] → [[NewPage]]"
- "Flagged: [[AmbiguousPage]] (could be X or Y)"
```

### Rule 2: Formatting

```
Detection:
- Inconsistent headers
- Missing list bullets
- Code blocks not fenced

Fix:
- Apply standard formatting
- Match existing style in file
```

### Rule 3: Missing Frontmatter

```
Detection:
head -1 wiki/page.md | grep "^---"

Fix:
if no frontmatter:
  add template:
  ---
  title: {derived from filename}
  created: {today}
  updated: {today}
  type: concept
  tags: []
  ---
```

### Rule 4: Orphan Pages

```
Detection:
Pages with no incoming links

Fix attempt:
1. Find related pages
2. If related found → add wikilinks
3. If no relation → flag as orphan
```

---

## Self-Heal Template

```markdown
# Self-Heal Report: {YYYY-MM-DD}

## Summary
- Issues found: {N}
- Issues fixed: {N}
- Issues flagged: {N}

## Fixed Issues

| Issue | Fix Applied | Status |
|-------|-------------|--------|
| | | |

## Flagged Issues

| Issue | Severity | Action Needed |
|-------|----------|---------------|
| | | |

## Changes Made
```bash
{list of commands run}
```
```

---

## Example Session

```
1. Self-heal triggers

2. Run detection:
   - 3 broken wikilinks
   - 2 missing frontmatter
   - 1 orphan page

3. Auto-fix:
   - Fixed: [[Autonomous-App]] → [[autonomous-app-builder]]
   - Fixed: Added frontmatter to page1.md
   - Fixed: Added frontmatter to page2.md

4. Flagged:
   - Orphan: old-feature.md (no links, needs review)

5. Report:
   "Self-heal complete.
   Fixed: 4 issues
   Flagged: 1 orphan page"
```

---

## Integration

- Use [[wiki-quality-score]] — Detect issues
- Use with [[on-schedule]] — Daily/weekly self-heal
- Use with [[wiki_hooks.py]] — Hook integration

---

## Related

- [[wiki-quality-score]] — Issue detection
- [[contradiction-resolution]] — Non-auto-fixable
- [[wiki_hooks.py]] — Hook integration
