#!/opt/homebrew/bin/python3.14
"""
Wiki Cross-Reference Suggester

Analyzes pages and suggests cross-links that should exist but don't:
1. Pages with same tags but no link between them
2. Pages that mention topics but don't link to them
3. Bidirectional link checker (if A links to B, B should link to A)

Usage:
    python3 scripts/wiki_cross_ref.py [--all] [--file path] [--fix]
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import json

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")

# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

def get_all_wiki_pages(path: Path) -> List[Path]:
    """Get all .md files in wiki"""
    files = []
    for f in path.rglob("*.md"):
        if any(x in f.parts for x in ["raw", "_archive", ".obsidian", "__pycache__"]):
            continue
        files.append(f)
    return files


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """Parse YAML frontmatter"""
    if not content.startswith("---"):
        return {}, content
    
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    
    fm_text = content[4:end]
    body = content[end + 4:].lstrip("\n")
    
    fm = {}
    for line in fm_text.split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            fm[key.strip()] = val.strip().strip('"').strip("'")
    
    return fm, body


def extract_wikilinks(content: str) -> List[str]:
    """Extract all [[wikilinks]] from content"""
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)


def extract_tags(fm: Dict) -> List[str]:
    """Extract tags from frontmatter"""
    tags_str = fm.get("tags", "")
    if not tags_str:
        return []
    # Parse [tag1, tag2] format
    tags = re.findall(r'[\w-]+', tags_str)
    return [t.lower() for t in tags if t not in ["and", "or", "the"]]


def get_page_topics(f: Path) -> Set[str]:
    """Get topics/keywords mentioned in page content"""
    content = f.read_text(encoding="utf-8").lower()
    
    # Common topic patterns
    topics = set()
    topic_patterns = {
        "lm-studio": [r"lm\s*studio"],
        "ollama": [r"ollama"],
        "hermes": [r"hermes"],
        "mcp": [r"\bmcp\b"],
        "telegram": [r"telegram"],
        "obsidian": [r"obsidian"],
        "github": [r"github"],
        "git": [r"\bgit\b"],
        "wiki": [r"\bwiki\b"],
        "browser": [r"browser"],
        "automation": [r"automation"],
        "knowledge-base": [r"knowledge\s*base"],
        "rag": [r"\brag\b"],
        "models": [r"model"],
        "local-llm": [r"local\s*llm", r"local-llm"],
    }
    
    for topic, patterns in topic_patterns.items():
        for pattern in patterns:
            if re.search(pattern, content):
                topics.add(topic)
                break
    
    return topics


# ═══════════════════════════════════════════════════════════════
# CROSS-REFERENCE ANALYSIS
# ═══════════════════════════════════════════════════════════════

def build_link_graph(files: List[Path]) -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Build bidirectional link graph.
    Returns: (outbound_map, inbound_map)
    outbound_map[page] = {pages that page links to}
    inbound_map[page] = {pages that link to page}
    """
    outbound = defaultdict(set)
    inbound = defaultdict(set)
    
    for f in files:
        page_name = f.stem.lower()
        content = f.read_text(encoding="utf-8")
        links = extract_wikilinks(content)
        
        for link in links:
            link_lower = link.lower()
            outbound[page_name].add(link_lower)
            inbound[link_lower].add(page_name)
    
    return dict(outbound), dict(inbound)


def find_missing_bidirectional(outbound: Dict[str, Set[str]]) -> List[Dict]:
    """
    Find pages where A links to B but B doesn't link to A.
    These are "suggested links" - B should probably link back to A.
    """
    suggestions = []
    
    for page_a, links in outbound.items():
        for page_b in links:
            # Check if B links back to A
            if page_b not in outbound or page_a not in outbound[page_b]:
                suggestions.append({
                    "from": page_a,
                    "to": page_b,
                    "type": "bidirectional",
                    "suggestion": f"Add [[{page_b}]] → [[{page_a}]] (bidirectional link)",
                    "priority": 5,
                })
    
    return suggestions


def find_same_tag_no_link(files: List[Path], outbound: Dict[str, Set[str]]) -> List[Dict]:
    """
    Find pages with same tags but no link between them.
    """
    suggestions = []
    
    # Build tag map
    tag_map = defaultdict(list)
    for f in files:
        fm, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        tags = extract_tags(fm)
        for tag in tags:
            tag_map[tag].append(f.stem.lower())
    
    # For each tag, check if pages with same tag link to each other
    for tag, pages in tag_map.items():
        if len(pages) < 2:
            continue
        
        for i, page_a in enumerate(pages):
            for page_b in pages[i+1:]:
                # Check if they already link
                already_links = (
                    page_b in outbound.get(page_a, set()) or
                    page_a in outbound.get(page_b, set())
                )
                if not already_links:
                    suggestions.append({
                        "from": page_a,
                        "to": page_b,
                        "type": "same-tag",
                        "tag": tag,
                        "suggestion": f"Add [[{page_b}]] or [[{page_a}]] (both have tag #{tag})",
                        "priority": 3,
                    })
    
    return suggestions


def find_related_topic_no_link(files: List[Path], outbound: Dict[str, Set[str]]) -> List[Dict]:
    """
    Find pages that mention topics but don't link to them.
    """
    suggestions = []
    
    # Build topic mentions per page
    page_topics = {}
    for f in files:
        page_topics[f.stem.lower()] = get_page_topics(f)
    
    # Check each page
    for f in files:
        page_a = f.stem.lower()
        topics_mentioned = page_topics.get(page_a, set())
        links_a = outbound.get(page_a, set())
        
        for topic in topics_mentioned:
            if topic not in links_a and topic in page_topics:
                # Find pages that ARE about this topic
                for page_b, topics_b in page_topics.items():
                    if page_a != page_b and topic in topics_b and topic not in outbound.get(page_a, set()):
                        suggestions.append({
                            "from": page_a,
                            "to": topic,
                            "type": "topic-mention",
                            "suggestion": f"Add [[{topic}]] (page mentions {topic} but doesn't link)",
                            "priority": 4,
                        })
    
    return suggestions


def find_orphan_suggestions(inbound: Dict[str, Set[str]], files: List[Path]) -> List[Dict]:
    """
    Find pages with no inbound links that should probably be linked from related pages.
    """
    suggestions = []
    
    for f in files:
        page = f.stem.lower()
        if not inbound.get(page):
            # This page has no inbound links
            # Check if it should link TO others that might link back
            content = f.read_text(encoding="utf-8")
            links = extract_wikilinks(content)
            
            # If page has outbound links, suggest reciprocation
            for link in links:
                link_lower = link.lower()
                if link_lower in inbound and not inbound[link_lower]:
                    suggestions.append({
                        "from": page,
                        "to": link_lower,
                        "type": "orphan-reciprocate",
                        "suggestion": f"Consider asking [[{link_lower}]] to link to [[{page}]]",
                        "priority": 2,
                    })
    
    return suggestions


# ═══════════════════════════════════════════════════════════════
# REPORTING
# ═══════════════════════════════════════════════════════════════

def print_report(suggestions: List[Dict]):
    """Print cross-reference suggestions"""
    print("=" * 80)
    print("WIKI CROSS-REFERENCE SUGGESTIONS")
    print("=" * 80)
    print()
    
    if not suggestions:
        print("No cross-reference suggestions found. Wiki is well-connected! ✅")
        return
    
    # Group by priority
    high = [s for s in suggestions if s["priority"] >= 5]
    medium = [s for s in suggestions if 3 <= s["priority"] < 5]
    low = [s for s in suggestions if s["priority"] < 3]
    
    print(f"Total suggestions: {len(suggestions)}")
    print(f"  High priority: {len(high)}")
    print(f"  Medium priority: {len(medium)}")
    print(f"  Low priority: {len(low)}")
    print()
    
    if high:
        print("-" * 80)
        print("HIGH PRIORITY (Bidirectional links missing)")
        print("-" * 80)
        for s in high[:10]:
            print(f"  {s['suggestion']}")
        print()
    
    if medium:
        print("-" * 80)
        print("MEDIUM PRIORITY (Same tag or topic mention)")
        print("-" * 80)
        for s in medium[:10]:
            print(f"  {s['suggestion']}")
        print()
    
    if low:
        print("-" * 80)
        print("LOW PRIORITY (Nice to have)")
        print("-" * 80)
        for s in low[:5]:
            print(f"  {s['suggestion']}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki Cross-Reference Suggester")
    parser.add_argument("--all", action="store_true", help="Run full analysis")
    parser.add_argument("--file", type=str, help="Analyze specific file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--fix", action="store_true", help="Apply fixes (not implemented)")
    args = parser.parse_args()
    
    files = get_all_wiki_pages(WIKI_PATH)
    outbound, inbound = build_link_graph(files)
    
    print(f"Wiki path: {WIKI_PATH}")
    print(f"Pages analyzed: {len(files)}")
    print()
    
    suggestions = []
    suggestions.extend(find_missing_bidirectional(outbound))
    suggestions.extend(find_same_tag_no_link(files, outbound))
    suggestions.extend(find_related_topic_no_link(files, outbound))
    suggestions.extend(find_orphan_suggestions(inbound, files))
    
    # Deduplicate
    seen = set()
    unique = []
    for s in suggestions:
        key = f"{s['from']}->{s['to']}"
        if key not in seen:
            seen.add(key)
            unique.append(s)
    
    # Sort by priority
    unique.sort(key=lambda x: x["priority"], reverse=True)
    
    if args.json:
        print(json.dumps(unique, indent=2))
    else:
        print_report(unique)


if __name__ == "__main__":
    main()
