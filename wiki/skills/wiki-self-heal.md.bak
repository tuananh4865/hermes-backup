---
confidence: medium
last_verified: 2026-04-21
relationships:
  - 🔍 phase-2-name (inferred)
  - 🔍 target (inferred)
  - 🔍 skills/wiki-watchdog (inferred)
  - 🔍 wiki-watchdog (inferred)
  - 🔍 link (inferred)
  - 🔍 target (inferred)
  - 🔍 target (inferred)
  - 🔍 target (inferred)
  - 🔍 self-healing-wiki (inferred)
  - 🔍 wiki-self-evolution (inferred)
  - 🔍 skills/wiki-watchdog (inferred)
relationship_count: 11
---

# Wiki Self-Heal Skill

> Agent behavior for auto-fixing wiki issues: broken links, missing frontmatter, orphans.

## Trigger Conditions

- User asks to "heal", "fix", "check wiki health"
- Wiki lint finds issues
- Watchdog detects file changes that may cause issues
- Post-commit hook triggers

## Behavior

### Step 1: Diagnose
```
python3 scripts/wiki_self_heal.py --all
```

Issues to find:
- Broken wikilinks (target doesn't exist)
- Missing frontmatter
- Orphan pages (no incoming links)
- Stale pages (>30 days old)

### Step 2: Analyze Results
**IMPORTANT: Not all "broken links" are real issues.**

False positives to ignore:
- `projects/_templates/` — placeholder links like `[[phase-2-name]]` are EXPECTED (design by design)
- Wikilinks inside code blocks or inline backticks
- Path-based wikilinks from non-existent project directories
- **Aliased wikilinks `[[target|display]]` where target EXISTS** — these are false positives IF the target page exists. But if the target does NOT exist, it's a REAL broken link.

**ONLY fix real broken links** — links to pages that genuinely don't exist.
**But also** — aliased wikilinks where the target doesn't exist are real broken links. Fix by: (a) creating the target page, OR (b) changing the alias to point to an existing page.

### Step 3: Auto-Fix (Manual Approval Required)
```
python3 scripts/wiki_self_heal.py --all --fix  # NEVER auto-create stubs!
```

**NEVER run `--fix` on wikis with `_templates/` directories** — it creates garbage files like `{project-name}.md`, `mistakes/001-xxx|mistake-1.md`.

Safe auto-fix only for:
- Missing frontmatter (add default frontmatter)
- Broken wikilinks (remove the dead link, don't create stub)

### Step 4: Manual Review
For orphans and complex issues:
- Orphan pages often have incoming links via path-based wikilinks — check with `grep`
- Don't auto-create stubs for complex topics — create proper content manually

### Step 5: Verify
```
python3 scripts/wiki_self_heal.py --all
```
Confirm 0 broken links, 0 missing frontmatter.

## Key Implementation Details

### Path-Based Wikilinks

Wikilinks can use full paths: `[[wiki-watchdog]]` instead of just `[[wiki-watchdog]]`.

**Fix in `get_existing_pages()`**: Add BOTH full path AND stem name:
```python
def get_existing_pages(files: List[Path]) -> set:
    pages = set()
    for f in files:
        rel = f.relative_to(WIKI_PATH)
        
        # Add full relative path stem (e.g. 'skills/wiki-watchdog')
        full_stem = str(rel).replace(".md", "").lower()
        pages.add(full_stem)
        
        # Also add just the filename stem (e.g. 'wiki-watchdog')
        page_name = rel.stem
        pages.add(page_name.lower())
        
        pages.add(page_name.lower().replace(" ", "-"))
    return pages
```

### Code Block Stripping

Wikilinks inside code blocks (` ``` ` ` or single backticks) must be excluded.

**Fix in `extract_wikilinks()`**:
```python
def extract_wikilinks(content: str) -> List[str]:
    # Strip code blocks (triple backticks)
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    
    # Strip inline code (single backticks) - removes `[[link]]`
    content_no_inline = re.sub(r'`[^`]*`', '', content_no_code)
    
    links = re.findall(r'\[\[([^\]]+)\]\]', content_no_inline)
    
    # Normalize aliased links [[target|display]] -> [[target]]
    normalized = []
    for link in links:
        if '|' in link:
            link = link.split('|')[0]
        normalized.append(link)
    
    return normalized
```

### Skip _templates/

`_templates/` contains placeholder links — skip during broken link scanning.

```python
skip_dirs = {'_templates', '.obsidian', '__pycache__', 'raw', 'transcripts'}
```

### Aliased Wikilinks

`[[target|display]]` — extract only `target`:
```python
if '|' in link:
    link = link.split('|')[0]
```

**Fix strategy for aliased broken links:**
- If `target` page exists → alias is a false positive (the target exists)
- If `target` page does NOT exist → two options:
  - (a) Create the `target` page as a redirect/content page
  - (b) Change alias to point to an EXISTING related page

Example: `[[TLS/SSL|HTTPS]]` where `tls-ssl.md` doesn't exist but `tls.md` does → fix to `[[tls|HTTPS]]`
Example: `[[Async/Await]]` where `async-await.md` doesn't exist → create it OR change to existing `async-await` page

## Cascade Effect (Critical)

**When fixing broken links, expect MORE broken links to appear after each fix.**

Pattern: 42 → 28 → 6. Each fix batch reveals more issues as the lint resolves aliases in cascade.

**Always re-run lint after each batch fix**, never assume a single pass is complete.
Run lint multiple times until count stabilizes.

## Bug Patterns Discovered

| Date | Bug | Fix |
|------|-----|-----|
| 2026-04-09 | `Path.with_suffix("")` returns string not Path | Use `.stem` directly |
| 2026-04-10 | Path-based wikilinks not recognized | Add full stem to pages set |
| 2026-04-10 | Code blocks not stripped | Regex strip before matching |
| 2026-04-10 | Inline backticks not stripped | Add single backtick pattern |
| 2026-04-10 | Aliased links not normalized | Split on `\|` keep target |
| 2026-04-10 | _templates/ scanned | Add to skip_dirs |
| 2026-04-21 | Aliased wikilinks cascade | Fix aliases pointing to non-existent pages — each fix reveals more. Re-run lint after each batch. |
| 2026-04-21 | External URLs in `[[...]]` | Strip `[[` wrapper from external URLs (`[[https://...]]` → `https://...`) |

## Output Format

```
## Self-Heal Report

### Fixed
- [page]: [issue] → [fix]

### Needs Review  
- [page]: [issue] (manual fix required)

### Wiki Health
- Broken links: X → Y
- Missing frontmatter: X → Y
- Orphans: X → Y (verify before fixing — orphan detector may be wrong)
```

## Related

- [[self-healing-wiki]] — Concept page for background
- [[wiki-self-evolution]] — For content gaps
- [[wiki-watchdog]] — For event-driven triggers

> **Auto-improvement:** healing for fixing broken links, missing frontmatter, and orphan pages.

> **Auto-improvement:** *Incomplete thought at the end**: The last bullet point under "Aliased Wikilinks" says "two op" - this is clearly truncated/incomplete. It should explain the two options for fixing aliased broken links.

> **Auto-improvement:** fixing wiki issues (broken links, missing frontmatter, orphans).

> **Auto-improvement:** *Current Content Analysis:**

> **Auto-improvement:** fixing wiki issues (broken links, missing frontmatter, orphans). Let me identify areas for improvement:

> **Auto-improvement:** 2 concrete improvements.

> **Auto-improvement:** 2 concrete improvements. Let me analyze the document for clarity, completeness, and potential pitfalls.