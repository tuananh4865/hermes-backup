#!/opt/homebrew/bin/python3.14
"""
topic_workflow.py — Raw Source to Concept Pipeline

Takes a URL or file path, extracts content, and creates/updates wiki pages.
Follows the llm-wiki skill's 6-step ingestion workflow.

Usage:
    python3 topic_workflow.py <url_or_file> [--title "Title"] [--type article|paper|transcript]
    python3 topic_workflow.py --url "https://..." [--title "..."]
    python3 topic_workflow.py --file /path/to/file.md [--title "..."]
    python3 topic_workflow.py --check                          # Verify script dependencies
    python3 topic_workflow.py --help

Examples:
    python3 topic_workflow.py "https://blog.langchain.dev/your-harness-your-memory/"
    python3 topic_workflow.py --url "https://arxiv.org/abs/1234.5678" --title "Attention Is All You Need"
    python3 topic_workflow.py --file ~/Downloads/paper.pdf
"""

import argparse
import json
import os
import re
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# ─── Configuration ────────────────────────────────────────────────────────────

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_DIR = WIKI_ROOT / "raw"
ENTITIES_DIR = WIKI_ROOT / "entities"
CONCEPTS_DIR = WIKI_ROOT / "concepts"
INDEX_FILE = WIKI_ROOT / "index.md"
LOG_FILE = WIKI_ROOT / "log.md"
SCHEMA_FILE = WIKI_ROOT / "SCHEMA.md"

FRONTMATTER_TEMPLATE = """---
title: {title}
created: {created}
updated: {updated}
type: {type}
tags: [{tags}]
sources: [{sources}]
---
"""

# ─── Helpers ─────────────────────────────────────────────────────────────────

def run_tool(cmd: list[str], timeout: int = 30) -> str:
    """Run a command and return stdout."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=str(WIKI_ROOT)
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after {timeout}s"
    except Exception as e:
        return f"ERROR: {e}"


def extract_content(url: str) -> tuple[str, str]:
    """Extract content from URL using web_extract tool."""
    import urllib.request
    import urllib.error
    
    # Try vxtwitter for tweets first
    if "twitter.com" in url or "x.com" in url:
        match = re.search(r'status/(\d+)', url)
        if match:
            tweet_id = match.group(1)
            try:
                with urllib.request.urlopen(f"https://api.vxtwitter.com/twitter/status/{tweet_id}", timeout=15) as resp:
                    data = json.loads(resp.read())
                    return data.get("text", ""), data.get("user_name", "Unknown")
            except Exception:
                pass
    
    # Try direct web extract via curl
    try:
        cmd = ["curl", "-sL", "--max-time", "30", "-A", 
               "Mozilla/5.0 (compatible; WikiBot/1.0)", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=35)
        html = result.stdout
        
        # Simple title extraction
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else urlparse(url).netloc
        
        # Simple text extraction (strip scripts, styles, tags)
        # Remove script and style elements
        html_clean = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.DOTALL|re.IGNORECASE)
        # Extract text from remaining HTML
        text = re.sub(r'<[^>]+>', ' ', html_clean)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text[:10000], title  # Limit to 10k chars
    except Exception as e:
        return f"ERROR fetching URL: {e}", ""


def slugify(text: str) -> str:
    """Convert text to lowercase hyphenated slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def extract_wikilinks(content: str) -> list[str]:
    """Extract [[wikilinks]] from content."""
    return re.findall(r'\[\[([^\]]+)\]\]', content)


def extract_entities(content: str) -> list[tuple[str, str]]:
    """Extract potential entity mentions (people, organizations, products).
    
    Returns list of (name, type) tuples.
    Simple heuristic extraction — refine as needed.
    """
    entities = []
    
    # Capitalized phrases that might be entities
    # This is a simplified version — a real implementation would use NER
    STOP_WORDS = {'the', 'and', 'for', 'that', 'this', 'with', 'from', 'your', 'our', 'their',
                  'has', 'have', 'been', 'being', 'will', 'would', 'could', 'should', 'may', 'might', 'can'}
    words = re.findall(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b', content)
    for word in set(words):
        if len(word) > 2 and word.lower() not in STOP_WORDS:
            entities.append((word, "unknown"))
    
    return entities[:20]  # Limit to 20 candidates


def check_entity_exists(name: str) -> Optional[Path]:
    """Check if entity page already exists."""
    slug = slugify(name)
    patterns = [
        ENTITIES_DIR / f"{slug}.md",
        CONCEPTS_DIR / f"{slug}.md",
    ]
    for p in patterns:
        if p.exists():
            return p
    return None


def read_frontmatter(path: Path) -> dict:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = path.read_text()
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                fm_text = content[3:end].strip()
                # Simple YAML parsing
                fm = {}
                for line in fm_text.split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        val = val.strip().strip('"').strip("'")
                        if val.startswith('['):
                            # List value
                            items = [x.strip().strip('"').strip("'") for x in val[1:-1].split(',')]
                            fm[key.strip()] = items
                        else:
                            fm[key.strip()] = val
                return fm
    except Exception:
        pass
    return {}


def write_frontmatter(path: Path, title: str, type_: str, tags: list[str], sources: list[str]) -> None:
    """Add or update frontmatter on a wiki page."""
    existing = read_frontmatter(path)
    
    created = existing.get('created', datetime.now().strftime('%Y-%m-%d'))
    updated = datetime.now().strftime('%Y-%m-%d')
    
    fm = FRONTMATTER_TEMPLATE.format(
        title=title,
        created=created,
        updated=updated,
        type=type_,
        tags=', '.join(tags),
        sources=', '.join(sources)
    )
    
    # Read existing content (without frontmatter)
    try:
        content = path.read_text()
        if content.startswith('---'):
            end = content.find('---', 3)
            if end > 0:
                content = content[end+3:].strip()
    except FileNotFoundError:
        content = ""
    
    path.write_text(fm + '\n' + content)


def add_to_index(page_path: Path, section: str, summary: str = "") -> None:
    """Add or update entry in index.md."""
    if not INDEX_FILE.exists():
        return
    
    content = INDEX_FILE.read_text()
    slug = page_path.stem
    
    # Find section
    section_header = f"## {section}"
    if section_header not in content:
        # Add new section
        content += f"\n\n{section_header}\n\n"
    
    # Check if entry already exists
    existing_pattern = re.compile(rf'^.*{re.escape(slug)}.*$', re.MULTILINE)
    if existing_pattern.search(content):
        # Update existing entry
        content = existing_pattern.sub(f"- [[{slug}]] — {summary}", content)
    else:
        # Add new entry
        # Find section end (next ## or end of file)
        section_pos = content.find(section_header)
        next_section = content.find('\n## ', section_pos + 1)
        if next_section == -1:
            insert_pos = len(content)
        else:
            insert_pos = next_section
        
        new_entry = f"- [[{slug}]] — {summary}\n"
        content = content[:insert_pos] + new_entry + content[insert_pos:]
    
    INDEX_FILE.write_text(content)


def append_log(action: str, subject: str, details: str = "") -> None:
    """Append entry to log.md."""
    if not LOG_FILE.exists():
        LOG_FILE.write_text("# Wiki Log\n\n> Chronological record.\n\n")
    
    date = datetime.now().strftime('%Y-%m-%d')
    entry = f"\n## [{date}] {action} | {subject}"
    if details:
        entry += f"\n{details}"
    
    LOG_FILE.write_text(entry + '\n', mode='a')


# ─── Main Workflow ────────────────────────────────────────────────────────────

def process_url(url: str, title: str = "") -> dict:
    """Process a URL: extract content and create wiki pages."""
    print(f"Fetching: {url}")
    
    content, page_title = extract_content(url)
    if not content or content.startswith("ERROR"):
        return {"success": False, "error": content}
    
    if title:
        page_title = title
    
    # Determine content type
    if "arxiv.org" in url:
        raw_type = "paper"
        raw_subdir = RAW_DIR / "papers"
    elif "twitter.com" in url or "x.com" in url:
        raw_type = "transcript"
        raw_subdir = RAW_DIR / "transcripts"
    else:
        raw_type = "article"
        raw_subdir = RAW_DIR / "articles"
    
    raw_subdir.mkdir(parents=True, exist_ok=True)
    
    # Save raw content
    slug = slugify(page_title)[:50]
    raw_file = raw_subdir / f"{slug}.md"
    
    # Avoid overwriting existing raw files — append timestamp if collision
    if raw_file.exists():
        timestamp = datetime.now().strftime('%H%M%S')
        raw_file = raw_subdir / f"{slug}-{timestamp}.md"
    
    raw_file.write_text(f"# Source: {url}\n\n# {page_title}\n\n{content}")
    print(f"Saved raw: {raw_file}")
    
    # Extract and check entities
    entities = extract_entities(content)
    entity_pages_created = []
    
    for name, _ in entities:
        existing = check_entity_exists(name)
        if not existing:
            # Create entity stub
            entity_file = ENTITIES_DIR / f"{slugify(name)}.md"
            entity_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write entity page
            entity_content = f"""---
title: {name}
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: entity
tags: [person]
sources: [{raw_file.relative_to(WIKI_ROOT)}]
---

# {name}

*Entity page — needs manual expansion*

## Overview
[Add description]

## Key Facts
- 

## Related Entities
- [[]]

## Sources
- {url}
"""
            entity_file.write_text(entity_content)
            entity_pages_created.append(entity_file.name)
            print(f"Created entity: {entity_file.name}")
    
    # Create or update concept page
    concept_slug = slugify(page_title)
    concept_file = CONCEPTS_DIR / f"{concept_slug}.md"
    
    if concept_file.exists():
        # Update existing — append new content
        existing = concept_file.read_text()
        new_content = f"\n\n## Latest ({datetime.now().strftime('%Y-%m-%d')})\n\n{content[:2000]}"
        concept_file.write_text(existing + new_content)
        print(f"Updated concept: {concept_file.name}")
    else:
        # Create new concept page
        concept_tags = [raw_type]
        concept_content = f"""---
title: {page_title}
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: concept
tags: [{', '.join(concept_tags)}]
sources: [{raw_file.relative_to(WIKI_ROOT)}]
---

# {page_title}

## Summary
[Extract key takeaways from source]

## Key Concepts
- 

## Related
- [[]]

## Sources
- [{page_title}]({url})
"""
        concept_file.write_text(concept_content)
        print(f"Created concept: {concept_file.name}")
    
    # Update index and log
    add_to_index(concept_file, "Concepts", f"Summary of {page_title}")
    
    for ep in entity_pages_created:
        ep_path = ENTITIES_DIR / ep
        add_to_index(ep_path, "Entities", f"Entity page for {ep.stem}")
    
    files_touched = [str(raw_file.relative_to(WIKI_ROOT)), str(concept_file.relative_to(WIKI_ROOT))]
    if entity_pages_created:
        files_touched.extend([f"entities/{ep}" for ep in entity_pages_created])
    
    append_log(
        "ingest",
        page_title,
        "\n".join([f"- {f}" for f in files_touched])
    )
    
    return {
        "success": True,
        "raw_file": str(raw_file.relative_to(WIKI_ROOT)),
        "concept_file": str(concept_file.relative_to(WIKI_ROOT)),
        "entities_created": entity_pages_created,
    }


def process_file(file_path: str, title: str = "", type_: str = "article") -> dict:
    """Process a local file and add to wiki."""
    path = Path(file_path)
    if not path.exists():
        return {"success": False, "error": f"File not found: {file_path}"}
    
    content = path.read_text()
    
    if not title:
        title = path.stem.replace('-', ' ').replace('_', ' ').title()
    
    # Determine raw subdir
    if type_ == "paper":
        raw_subdir = RAW_DIR / "papers"
    elif type_ == "transcript":
        raw_subdir = RAW_DIR / "transcripts"
    else:
        raw_subdir = RAW_DIR / "articles"
    
    raw_subdir.mkdir(parents=True, exist_ok=True)
    
    # Copy to raw/
    slug = slugify(title)[:50]
    raw_file = raw_subdir / f"{slug}.md"
    
    if raw_file.exists():
        timestamp = datetime.now().strftime('%H%M%S')
        raw_file = raw_subdir / f"{slug}-{timestamp}.md"
    
    raw_file.write_text(f"# Source: {file_path}\n\n# {title}\n\n{content}")
    
    # Create concept page
    concept_file = CONCEPTS_DIR / f"{slugify(title)}.md"
    concept_tags = [type_]
    concept_content = f"""---
title: {title}
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: concept
tags: [{', '.join(concept_tags)}]
sources: [{raw_file.relative_to(WIKI_ROOT)}]
---

# {title}

## Summary
[Content from {path.name}]

## Key Points
- 

## Related
- [[]]

"""
    concept_file.write_text(concept_content)
    
    add_to_index(concept_file, "Concepts", f"Imported from {path.name}")
    append_log("ingest", title, f"- {raw_file.relative_to(WIKI_ROOT)}\n- {concept_file.relative_to(WIKI_ROOT)}")
    
    return {
        "success": True,
        "raw_file": str(raw_file.relative_to(WIKI_ROOT)),
        "concept_file": str(concept_file.relative_to(WIKI_ROOT)),
    }


def check_dependencies() -> bool:
    """Verify script can run (Python version, paths, etc.)."""
    print("Checking dependencies...")
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("ERROR: Python 3.9+ required")
        return False
    
    # Check wiki directory
    if not WIKI_ROOT.exists():
        print(f"ERROR: Wiki directory not found: {WIKI_ROOT}")
        return False
    
    # Check required directories
    for d in [RAW_DIR, ENTITIES_DIR, CONCEPTS_DIR]:
        if not d.exists():
            print(f"WARNING: {d} does not exist — will create on first use")
    
    print("✓ All checks passed")
    return True


# ─── CLI Interface ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Topic Workflow: Raw Source → Wiki Concept Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('url_or_file', nargs='?', help='URL or file path to process')
    parser.add_argument('--url', help='URL to process')
    parser.add_argument('--file', help='Local file to process')
    parser.add_argument('--title', help='Override title for the content')
    parser.add_argument('--type', choices=['article', 'paper', 'transcript'], 
                       default='article', help='Content type (default: article)')
    parser.add_argument('--check', action='store_true', help='Verify dependencies and exit')
    
    args = parser.parse_args()
    
    if args.check:
        sys.exit(0 if check_dependencies() else 1)
    
    if not args.url_or_file and not args.url and not args.file:
        parser.print_help()
        sys.exit(1)
    
    # Verify dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    # Process input
    if args.url:
        result = process_url(args.url, args.title)
    elif args.file:
        result = process_file(args.file, args.title, args.type)
    else:
        input_text = args.url_or_file
        if input_text.startswith(('http://', 'https://')):
            result = process_url(input_text, args.title)
        else:
            result = process_file(input_text, args.title, args.type)
    
    # Report result
    if result.get('success'):
        print("\n✓ Processing complete:")
        print(f"  Raw: {result.get('raw_file', 'N/A')}")
        print(f"  Concept: {result.get('concept_file', 'N/A')}")
        if result.get('entities_created'):
            print(f"  Entities: {', '.join(result['entities_created'])}")
    else:
        print(f"\n✗ Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == '__main__':
    main()
