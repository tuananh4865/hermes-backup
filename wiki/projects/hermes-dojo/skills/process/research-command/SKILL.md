---
name: research-command
description: Understand the problem space before acting - creates research artifact with dependency map and analysis
version: 1.0.0
category: process
platforms: [macos, linux]
created: 2026-04-14
tags: [research, understanding, analysis, dependency-map, artifacts]
requires_toolsets: [terminal]
---

# Research Command

**Never code before understanding. Never fix before diagnosing.**

This skill creates a research artifact that documents your understanding before you start acting.

---

## When to Use

Use `/research` or this skill when:

1. **Bug fix** — Root cause unclear
2. **Feature addition** — Impact area unknown
3. **Refactor** — Dependencies not mapped
4. **Any non-trivial task** — When in doubt, research first

**Rule:** If you can't explain the problem space in one page, you need more research.

---

## The Research Workflow

### Step 1: Understand the Request

```
What is the user asking for?
What do they expect to happen?
What does "done" look like to them?
```

### Step 2: Read Relevant Code

```
Find files related to the task
Read the relevant sections
Understand the current implementation
```

### Step 3: Map Dependencies

```bash
# Find function callers
grep -r "function_name" --include="*.py" .

# Find imports
grep -r "from module import" --include="*.py" .

# Find related files
find . -name "*.py" -exec grep -l "keyword" {} \;
```

### Step 4: Identify Root Cause (for bugs)

```
What is the observed behavior?
What should happen?
What is the gap?
Why does the gap exist?
```

### Step 5: Document Findings

Create a research artifact (see template below).

---

## Research Artifact Template

```markdown
# Research: {Topic}

**Date:** {YYYY-MM-DD}
**Task:** {Original request from user}
**Status:** In Progress / Complete

## Understanding

### What the user wants
{Description}

### What "done" looks like
- [ ] {Criterion 1}
- [ ] {Criterion 2}

## Codebase Understanding

### Relevant files
| File | Purpose | Last Modified |
|------|---------|--------------|
| | | |

### Current implementation
{How does it currently work?}

### Information flow
{How data moves through the system}

## Dependency Map

### Functions/Classes involved
| Name | Location | Called By | Calls |
|------|----------|-----------|-------|
| | | | |

### Files that need changes
| File | Change Needed |
|------|--------------|
| | |

## Analysis

### For bugs: Root Cause
**Observed:** {What happens}
**Expected:** {What should happen}
**Root Cause:** {Why}
**Evidence:** {How we know}

### For features: Approach Options
**Option A:** {Description}
- Pros: {Pros}
- Cons: {Cons}

**Option B:** {Description}
- Pros: {Pros}
- Cons: {Cons}

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| | | | |

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| | |

## Next Steps
1. {Next action}
2. {Next action}

## Related
- {Links to related pages}
```

---

## Example Research Session

```
User: "Fix the bug where users can't upload files larger than 10MB"

Research:

1. UNDERSTANDING
   - User expects files up to 50MB to upload
   - Currently fails silently at 10MB
   - "Done" = files 1-50MB all upload successfully

2. RELEVANT FILES
   - src/api/upload.py (API endpoint)
   - src/services/storage.py (storage service)
   - src/config/upload.py (config)

3. DEPENDENCY MAP
   upload.py → storage.py → config.upload_max_size
   All 3 would need changes

4. ROOT CAUSE
   - config.upload_max_size = 10 * 1024 * 1024 (10MB hardcoded)
   - No validation feedback to user
   - Storage service throws exception silently

5. DECISIONS
   - Change config to 50MB
   - Add proper error handling
   - Show user-friendly message

6. NEXT STEPS
   1. Update plan.md with exact steps
   2. Change config value
   3. Update error handling
   4. Test with 50MB file
```

---

## Key Principles

### Research Before Action

```
BAD: User says "fix bug" → immediately start editing
GOOD: User says "fix bug" → research → understand → plan → implement
```

### Document Your Understanding

```
BAD: "I think I know what's happening"
GOOD: "The bug happens because [evidence-based explanation]"
```

### Map Dependencies First

```
BAD: "I'll just edit this one file"
GOOD: "This file is called by 12 others. Need to check each."
```

---

## Integration

- Use [[karpathy-principles]] — Think before coding
- Output feeds into [[plan-command]] — Research → Plan
- Use [[surgical-change-protocol]] — For cascade awareness
- Use [[dependency_tracker.py]] — For automated dependency mapping

---

## Related

- [[plan-command]] — Next step after research
- [[implement-command]] — Execute the plan
- [[karpathy-principles]] — Think before coding
