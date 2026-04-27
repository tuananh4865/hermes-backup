---
name: stale-detection
description: Find content that needs updating - detect outdated info, stale claims, abandoned pages
version: 1.0.0
category: proactive
platforms: [macos, linux]
created: 2026-04-14
tags: [proactive, stale-detection, outdated, wiki-health, content-maintenance]
requires_toolsets: [terminal]
---

# Stale Detection

**Find content that's gone stale. Fix or flag it.**

This skill detects content that needs updating, ensuring the wiki stays current.

---

## What is Stale?

```
Stale content:
- Pages not updated in 30+ days (active topics)
- Pages not updated in 90+ days (stable topics)
- Claims that contradict newer information
- Pages with outdated examples
- Abandoned pages (incomplete, never finished)
```

---

## The Stale Detection Workflow

### Step 1: Scan for Old Pages

```bash
# Find pages not updated in N days
find wiki/ -name "*.md" -mtime +30

# Check frontmatter for last updated
grep -r "updated:" wiki/ | sort
```

### Step 2: Categorize Staleness

```
Categories:
1. Time-based: Too old based on topic velocity
2. Claim-based: Contradicts current knowledge
3. Structural: Orphan pages, missing pieces
4. Abandoned: Incomplete and forgotten
```

### Step 3: Assess Each Page

```
For each stale page:
1. Is it still relevant?
2. Is the outdated info dangerous?
3. Can it be updated or should it be archived?
4. What's the update effort?
```

### Step 4: Take Action

```
Actions:
1. Update: Still relevant, easy to fix
2. Archive: Still relevant, too much effort
3. Delete: No longer relevant
4. Flag: Keep but mark as potentially outdated
```

---

## Staleness Criteria

### Time-Based

| Topic Type | Warning | Critical |
|------------|---------|----------|
| Fast-moving (AI, web) | 14 days | 30 days |
| Medium (frameworks) | 30 days | 60 days |
| Slow (concepts, principles) | 90 days | 180 days |

### Claim-Based

```
Signs of stale claims:
- Uses deprecated tools/methods
- References outdated versions
- Contradicts newer wiki pages
- Contradicts known current facts
```

### Structural

```
Signs of structural staleness:
- Orphan pages (no links in or out)
- Stub pages (no content)
- Duplicate pages (same topic)
```

---

## Stale Detection Report Template

```markdown
# Stale Detection Report: {YYYY-MM-DD}

## Summary
- Pages scanned: {N}
- Stale pages found: {N}
- Critical: {N}
- Warning: {N}
- Info: {N}

## Critical (Needs Immediate Action)

| Page | Issue | Action Needed |
|------|-------|---------------|
| | | |

## Warning (Needs Update Soon)

| Page | Last Updated | Issue |
|------|--------------|-------|
| | | |

## Info (Monitor)

| Page | Last Updated | Notes |
|------|--------------|-------|
| | | |

## Actions Taken
- [ ] {Action 1}
- [ ] {Action 2}

## Recommendations
1. {Recommendation 1}
2. {Recommendation 2}
```

---

## Example Session

```
1. Stale detection triggers (weekly)

2. Scan:
   find wiki/ -name "*.md" -mtime +30
   Found: 12 pages older than 30 days

3. Categorize:
   Critical: 2 (outdated API docs)
   Warning: 5 (old project notes)
   Info: 5 (stable concepts)

4. Assess:
   - api-docs.md: Uses v1 API, v2 is out
   - project-notes.md: Project abandoned

5. Actions:
   - api-docs.md: Update to v2
   - project-notes.md: Archive

6. Report:
   "Found 12 stale pages.
   Critical: 2 (actioned)
   Warning: 5 (flagged)
   Info: 5 (monitoring)"
```

---

## Integration

- Use [[self-heal]] — Auto-fix some issues
- Use [[wiki-quality-score]] — Assess page quality
- Use with [[on-schedule]] — Weekly detection

---

## Related

- [[daily-review]] — Daily check
- [[weekly-review]] — Weekly deep dive
- [[self-heal]] — Auto-fix issues
- [[on-schedule]] — Scheduled detection
