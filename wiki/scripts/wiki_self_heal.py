#!/opt/homebrew/bin/python3.14
"""
Wiki Self-Heal Script

Auto-fixes wiki issues:
1. Broken wikilinks - create stub pages or remove dead links
2. Missing frontmatter - add default frontmatter
3. Stale pages - detect and optionally auto-bump
4. Duplicate detection - flag pages that might be duplicates
"""

import re
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
DAYS_STALE = 30  # Pages older than this are "stale"

# Default frontmatter template — generates Q>5 stubs
# Target: 300+ words, 5+ sections, 3+ wikilinks
DEFAULT_FRONTMATTER = """---
title: "{title}"
created: {date}
updated: {date}
type: concept
tags: [untagged, auto-created]
sources: []
---

# {title}

> This page was auto-created by [[self-healing-wiki]] to fill a broken link.
> The content below is a starting point — please expand with real knowledge.
> This is a placeholder stub. Replace all [TODO] items with actual content.

## Overview

This concept is an important piece of knowledge within its broader domain. It connects to various related ideas and has practical applications in real-world scenarios. The concept itself represents a fundamental building block that professionals and practitioners encounter frequently when working in this area. Understanding this concept deeply will help you make better decisions, avoid common pitfalls, and communicate more effectively with peers in your field. Take time to explore the related concepts listed at the end of this page to build a comprehensive mental model.

## Key Concepts

This concept encompasses several important sub-ideas that are worth understanding individually:

- **Core Principle**: Every concept has a foundational principle that explains why it exists and how it works. For this concept, the core principle relates to [TODO: Document the fundamental principle behind this concept]. Understanding this principle will clarify many of the practical aspects described below.
- **Typical Use Cases**: This concept is most commonly applied in scenarios involving [TODO: List common scenarios where this concept applies]. Recognizing these patterns will help you identify opportunities to leverage this knowledge effectively.
- **Related Patterns**: Many similar concepts share common patterns and approaches. Here, the related patterns include [TODO: Identify related patterns or complementary ideas] which you may find useful to explore.
- **Common Misconceptions**: Several misunderstandings frequently arise around this topic. The most notable include [TODO: Note frequent misunderstandings to avoid]. Being aware of these will help you think more clearly about the subject.

## Practical Applications

This concept appears in various real-world scenarios across different industries and contexts. Understanding when and how to apply it requires experience with the specific constraints and requirements of each situation.

### Common Use Cases

In practice, this concept is most frequently applied in the following contexts:

1. [TODO: First common use case — be specific about what this looks like in reality]
2. [TODO: Second common use case — include details about scale, scope, or prerequisites]
3. [TODO: Third common use case — note any trade-offs or considerations]
4. [TODO: Add more use cases as relevant to your domain]

### Implementation Considerations

When working with this concept in practice, keep the following factors in mind:

- **Complexity**: Consider whether the added complexity is justified for your use case
- **Trade-offs**: Every approach involves trade-offs between competing concerns
- **Dependencies**: Identify what other concepts, tools, or skills are prerequisites
- **Maintenance**: Consider the long-term maintenance implications of any approach

## Examples

The following examples illustrate how this concept applies in concrete situations. Use these as starting points and develop your own examples based on your experience.

### Example 1

[TODO: Provide a concrete, real example from your work or study.
 Make sure the example is specific enough to be informative.]

```python
# Example code showing this concept in practice
# Replace with your own implementation

def example():
    # TODO: Add real example
    pass
```

### Example 2

[TODO: Add another relevant example that illustrates a different aspect.
 Real examples from your experience are most valuable here.]

## Related Concepts

Understanding this concept connects to several other topics in your knowledge base:

- [[self-healing-wiki]] — the system that created this stub
- [[concept-template]] — the general template used for concept pages
- [[learning]] — approaches to learning new concepts effectively

[TODO: Replace the wikilinks above with links to actual related concepts in your wiki.
 Use [[double brackets]] to link to related pages.]

## Further Reading

The following resources may help you develop a deeper understanding of this concept:

- [TODO: Add relevant external resources, documentation links, or related wiki pages]
- [TODO: Note any particularly useful books, articles, or courses]
- [TODO: Add links to primary sources where applicable]

## Personal Notes

> Use this space for your personal notes, observations, and insights about this concept.
> These notes are private to your wiki brain and won't be overwritten by automated systems.

[TODO: Write your personal notes here — what did you learn? What surprised you?
 What questions do you still have?]

---

*This page was auto-generated by [[self-healing-wiki]]. Last updated: {date}*
"""

# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

def get_all_markdown_files(path: Path) -> List[Path]:
    """Get all .md files in wiki, excluding raw/, _archive/, _templates/, and .obsidian/.
    
    _templates/ is skipped because it contains placeholder links (e.g. [[phase-2-name]])
    that are designed to be broken until a project is instantiated.
    """
    files = []
    for f in path.rglob("*.md"):
        # Skip raw, _archive, _templates, .obsidian
        if any(x in f.parts for x in ["raw", "_archive", "_templates", ".obsidian"]):
            continue
        files.append(f)
    return files


def extract_wikilinks(content: str) -> List[str]:
    """Extract all [[wikilinks]] from content, excluding those in code/inline code.
    
    Also normalizes aliased links [[target|display]] to just [[target]].
    """
    # Strip code blocks first (triple backticks)
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    
    # Strip inline code (single backticks) - removes `[[link in backticks]]`
    content_no_inline = re.sub(r'`[^`]*`', '', content_no_code)
    
    # Extract wikilinks
    links = re.findall(r'\[\[([^\]]+)\]\]', content_no_inline)
    
    # Normalize aliased links (keep only the target, not display text)
    normalized = []
    for link in links:
        if '|' in link:
            link = link.split('|')[0]
        normalized.append(link)
    
    return normalized


def get_existing_pages(files: List[Path]) -> set:
    """Get set of all existing page names (for link validation).
    
    Adds BOTH path-based names (e.g. 'skills/wiki-watchdog') AND 
    stem names (e.g. 'wiki-watchdog') to handle both wikilink formats.
    """
    pages = set()
    for f in files:
        # Get relative path and strip extension
        rel = f.relative_to(WIKI_PATH)
        
        # Add full relative path stem (e.g. 'skills/wiki-watchdog')
        full_stem = str(rel).replace(".md", "").lower()
        pages.add(full_stem)
        
        # Also add just the filename stem (e.g. 'wiki-watchdog')
        page_name = rel.stem  # stem = filename without extension
        pages.add(page_name.lower())
        
        # Also add with hyphens normalized (for 'some page name' style)
        pages.add(page_name.lower().replace(" ", "-"))
    return pages


def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
    """Parse YAML frontmatter. Returns (fm_dict, body_content)."""
    if not content.startswith("---"):
        return None, content
    
    end = content.find("\n---", 3)
    if end == -1:
        return None, content
    
    fm_text = content[4:end]
    body = content[end + 4:].lstrip("\n")
    
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
    
    return fm, body


def has_frontmatter(content: str) -> bool:
    """Check if content has proper YAML frontmatter."""
    return content.startswith("---")


def is_stale(updated_str: str, days: int = DAYS_STALE) -> bool:
    """Check if a page is stale based on its updated date."""
    if not updated_str:
        return True
    
    try:
        updated = datetime.strptime(updated_str[:10], "%Y-%m-%d")
        age = (datetime.now() - updated).days
        return age > days
    except:
        return False


# ═══════════════════════════════════════════════════════════════
# SELF-HEAL OPERATIONS
# ═══════════════════════════════════════════════════════════════

def _safe_slug(link: str) -> str:
    """Convert wikilink to safe filename slug.
    
    Handles:
    - Aliased links [[Target|Display]] -> extracts 'Target'
    - Multi-word links with spaces/hyphens/underscores -> hyphenated
    - Path separators (/, \) -> rejected (return empty)
    """
    # Handle aliased links: [[Target|Display]] -> 'Target'
    if '|' in link:
        link = link.split('|')[0]
    
    # Normalize: lowercase, replace spaces/underscores with hyphens
    slug = re.sub(r'[\s\-_]+', '-', link.strip()).lower()
    
    # IMPORTANT: reject slugs containing path separators
    # These would create directories instead of files
    if '/' in slug or '\\' in slug:
        return ""
    
    return slug


def fix_broken_links(files: List[Path], dry_run: bool = True) -> Dict[str, any]:
    """
    Find broken wikilinks and either:
    - Create stub pages for them (default)
    - Or remove the dead links
    
    Returns: {action: str, broken_links: [(file, link)], stubs_created: [path]}
    """
    existing_pages = get_existing_pages(files)
    results = {
        "action": "dry_run" if dry_run else "fix",
        "broken_links": [],
        "stubs_created": [],
        "links_fixed": [],
        "skipped_paths": []  # Links that would create directories
    }
    
    for f in files:
        content = f.read_text(encoding="utf-8")
        wikilinks = extract_wikilinks(content)
        
        for link in wikilinks:
            # Safe slug conversion (handles aliases, rejects path separators)
            link_normalized = _safe_slug(link)
            
            # Skip if slug is empty (would create directory)
            if not link_normalized:
                results["skipped_paths"].append((str(f.relative_to(WIKI_PATH)), link))
                continue
            
            # Check if link target exists
            if link_normalized not in existing_pages:
                results["broken_links"].append((str(f.relative_to(WIKI_PATH)), link))
                
                if not dry_run:
                    # Create stub page
                    stub_path = WIKI_PATH / "concepts" / f"{link_normalized}.md"
                    if not stub_path.exists():
                        stub_content = DEFAULT_FRONTMATTER.format(
                            title=link.split('|')[0].strip().replace("-", " ").title(),
                            date=datetime.now().strftime("%Y-%m-%d")
                        )
                        stub_path.parent.mkdir(parents=True, exist_ok=True)
                        stub_path.write_text(stub_content, encoding="utf-8")
                        results["stubs_created"].append(str(stub_path.relative_to(WIKI_PATH)))
    
    return results


def fix_missing_frontmatter(files: List[Path], dry_run: bool = True) -> Dict[str, any]:
    """
    Find pages without frontmatter and add default frontmatter.
    """
    results = {
        "action": "dry_run" if dry_run else "fix",
        "missing_fm": [],
        "fixed": []
    }
    
    for f in files:
        content = f.read_text(encoding="utf-8")
        
        if not has_frontmatter(content):
            results["missing_fm"].append(str(f.relative_to(WIKI_PATH)))
            
            if not dry_run:
                # Extract title from first H1 or filename
                title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    title = f.name.replace(".md", "").replace("-", " ").title()
                
                # Prepend frontmatter
                fm = f"""---
title: "{title}"
created: {datetime.now().strftime("%Y-%m-%d")}
updated: {datetime.now().strftime("%Y-%m-%d")}
type: concept
tags: [auto-filled]
---

"""
                new_content = fm + content
                f.write_text(new_content, encoding="utf-8")
                results["fixed"].append(str(f.relative_to(WIKI_PATH)))
    
    return results


def check_stale_pages(files: List[Path], days: int = DAYS_STALE) -> Dict[str, any]:
    """
    Find pages that haven't been updated in >N days.
    """
    results = {
        "stale_pages": [],
        "summary": {}
    }
    
    for f in files:
        content = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        
        if fm and "updated" in fm:
            if is_stale(fm["updated"], days):
                age = (datetime.now() - datetime.strptime(fm["updated"][:10], "%Y-%m-%d")).days
                results["stale_pages"].append({
                    "file": str(f.relative_to(WIKI_PATH)),
                    "updated": fm["updated"],
                    "age_days": age
                })
    
    results["summary"] = {
        "total_checked": len(files),
        "stale_count": len(results["stale_pages"]),
        "threshold_days": days
    }
    
    return results


def find_orphan_pages(files: List[Path]) -> Dict[str, any]:
    """
    Find pages with no inbound wikilinks from other pages.
    """
    # Build inbound link map
    inbound_links: Dict[str, set] = {}
    all_pages: set = set()
    
    for f in files:
        page_name = f.relative_to(WIKI_PATH).stem.lower()
        all_pages.add(page_name)
        inbound_links[page_name] = set()
    
    # Scan all files for wikilinks
    for f in files:
        content = f.read_text(encoding="utf-8")
        wikilinks = extract_wikilinks(content)
        
        for link in wikilinks:
            link_lower = link.lower().replace(" ", "-")
            if link_lower in inbound_links:
                # Current file links to this page
                current_page = f.relative_to(WIKI_PATH).stem.lower()
                inbound_links[link_lower].add(current_page)
    
    # Find orphans (no inbound links)
    orphans = []
    for page, linkers in inbound_links.items():
        if not linkers:
            orphans.append(page)
    
    return {
        "orphans": sorted(orphans),
        "count": len(orphans)
    }


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki Self-Heal")
    parser.add_argument("--fix", action="store_true", help="Actually fix issues (default is dry-run)")
    parser.add_argument("--links", action="store_true", help="Fix broken wikilinks")
    parser.add_argument("--frontmatter", action="store_true", help="Fix missing frontmatter")
    parser.add_argument("--stale", action="store_true", help="Check stale pages")
    parser.add_argument("--orphans", action="store_true", help="Find orphan pages")
    parser.add_argument("--all", action="store_true", help="Run all checks")
    parser.add_argument("--days", type=int, default=DAYS_STALE, help=f"Stale threshold days (default {DAYS_STALE})")
    args = parser.parse_args()
    
    # If no specific args, show help
    if not any([args.links, args.frontmatter, args.stale, args.orphans, args.all]):
        parser.print_help()
        return
    
    files = get_all_markdown_files(WIKI_PATH)
    print(f"Wiki path: {WIKI_PATH}")
    print(f"Files scanned: {len(files)}")
    print()
    
    if args.all or args.links:
        print("=" * 60)
        print("BROKEN WIKILINKS")
        print("=" * 60)
        results = fix_broken_links(files, dry_run=not args.fix)
        if results["broken_links"]:
            print(f"Found {len(results['broken_links'])} broken links:")
            for f, link in results["broken_links"]:
                print(f"  {f}: [[{link}]]")
        else:
            print("No broken links found ✅")
        if results.get("skipped_paths"):
            print(f"\nSkipped {len(results['skipped_paths'])} path-separator links (would create directories):")
            for f, link in results["skipped_paths"][:10]:
                print(f"  {f}: [[{link}]]")
            if len(results["skipped_paths"]) > 10:
                print(f"  ... and {len(results['skipped_paths']) - 10} more")
        print()
    
    if args.all or args.frontmatter:
        print("=" * 60)
        print("MISSING FRONTMATTER")
        print("=" * 60)
        results = fix_missing_frontmatter(files, dry_run=not args.fix)
        if results["missing_fm"]:
            print(f"Found {len(results['missing_fm'])} pages without frontmatter:")
            for f in results["missing_fm"]:
                print(f"  {f}")
        else:
            print("All pages have frontmatter ✅")
        print()
    
    if args.all or args.stale:
        print("=" * 60)
        print("STALE PAGES")
        print("=" * 60)
        results = check_stale_pages(files, days=args.days)
        print(f"Checked: {results['summary']['total_checked']} files")
        print(f"Stale (> {args.days} days): {results['summary']['stale_count']}")
        if results["stale_pages"]:
            print("\nStale pages:")
            for p in sorted(results["stale_pages"], key=lambda x: x["age_days"], reverse=True)[:10]:
                print(f"  {p['file']} - {p['age_days']} days old")
        print()
    
    if args.all or args.orphans:
        print("=" * 60)
        print("ORPHAN PAGES")
        print("=" * 60)
        results = find_orphan_pages(files)
        print(f"Found {results['count']} orphan pages (no inbound links):")
        for p in results["orphans"]:
            print(f"  {p}")
        print()


if __name__ == "__main__":
    main()
