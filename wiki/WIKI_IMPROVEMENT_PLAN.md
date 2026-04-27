---
title: "WIKI IMPROVEMENT PLAN"
created: 2026-04-21
updated: 2026-04-21
type: page
tags: ['page']
---

# WIKI IMPROVEMENT PLAN

## Context (Phase 1 Findings)
- **Stub files**: 1 found at `projects/tiktok-content-strategy/hoc-tu-content-creator-noi-tieng.md`
- **Concepts bloat**: Top directory `concepts/` has 2863 `.md` files (86% of wiki)
- **Broken links**: 3+ identified — `../entities/user-profile.md`, `./reports/analysis-2024.md`, `./Page_Name.md`

---

## Priority 1 — Critical: Fix Broken Links & Stub Files

### Step 1.1: Resolve or remove stub file
- **File**: `projects/tiktok-content-strategy/hoc-tu-content-creator-noi-tieng.md` (0 bytes)
- **Action**: Either delete the file OR expand it with minimal content (title + brief description)
- **Owner**: Coder

### Step 1.2: Fix broken links
- **Link 1**: `../entities/user-profile.md` — target may have moved; search `entities/` for renamed analogue or recreate
- **Link 2**: `./reports/analysis-2024.md` — verify `reports/` directory exists; if file missing, either recreate or remove link
- **Link 3**: `./Page_Name.md` — likely a capitalization typo; search for `page_name.md` or `Page_name.md`
- **Action**: For each broken link, either (a) fix the target path, (b) recreate the missing file, or (c) remove the dangling link
- **Owner**: Coder

### Step 1.3: Audit all links in concepts/ directory
- **Action**: Run link-check across all 2863 files in `concepts/` to catch any additional broken references before they surface
- **Tool**: `grep -rn '\.\./' ~/wiki/concepts/*.md` or use `lychee` / `markdown-link-check`
- **Owner**: Analyst

---

## Priority 2 — High: Address Concepts Directory Bloat

### Step 2.1: Categorize existing concepts files
- **Action**: Analyze 2863 files in `concepts/` — group by naming pattern, topic, or content similarity
- **Deliverable**: CSV or markdown table listing file groups (e.g., `concepts/ai-*.md`, `concepts/swiftui-*.md`)
- **Owner**: Analyst

### Step 2.2: Create subdirectory structure
- **Action**: Replace flat `concepts/` with nested structure, e.g.:
  - `concepts/domains/ai/`, `concepts/domains/mobile/`, `concepts/domains/web/`
  - `concepts/topics/growth/`, `concepts/topics/content/`
  - OR by alphabetical: `concepts/a/`, `concepts/b/`, ... `concepts/z/`
- **Decision criteria**: Choose structure based on natural groupings found in Step 2.1
- **Owner**: Planner (makes recommendation), Coder (executes)

### Step 2.3: Migrate files and update all internal links
- **Action**: Move files to new subdirectories, then run a bulk link-rewrite script to update all `../` and `./` references
- **Script approach**: `grep -rl 'concepts/' --include="*.md" | xargs sed -i 's|concepts/|concepts/domains/|g'`
- **Validation**: Re-run link-check after migration
- **Owner**: Coder

---

## Priority 3 — Medium: Long-Term Organization Improvements

### Step 3.1: Enforce stub-file prevention
- **Action**: Add a pre-commit hook or CI check that fails on new 0-byte `.md` files
- **Implementation**: Add to `.git/hooks/pre-commit`: `find . -name '*.md' -size 0 -exec echo "STUB FILE: {}" \; && exit 1`

### Step 3.2: Implement link-checking CI
- **Action**: Integrate `lychee` or `markdown-link-check` into CI pipeline to catch broken links on every PR
- **Benefit**: Prevents link rot from being merged

### Step 3.3: Establish naming conventions
- **Action**: Document slug-style naming standard (e.g., `kebab-case.md`, no spaces, lowercase) and enforce via lint rule
- **Benefit**: Reduces typo-based broken links (e.g., `Page_Name.md` → `page-name.md`)

### Step 3.4: Create wiki home / index page
- **Action**: Author `wiki-index.md` at wiki root linking to major sections (`concepts/`, `projects/`, `entities/`, `reports/`)
- **Benefit**: Improves navigability and reduces orphaned content discovery

---

## Summary

| Priority | Focus | Key Actions |
|---|---|---|
| **P1 Critical** | Broken links & stubs | Delete/expand stub; fix 3 broken links; audit all concepts links |
| **P2 High** | Concepts bloat | Categorize 2863 files; create subdir structure; migrate + rewrite links |
| **P3 Medium** | Long-term health | Pre-commit stub check; CI link-check; naming conventions; wiki index |
