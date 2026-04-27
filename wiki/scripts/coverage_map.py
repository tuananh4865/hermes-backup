#!/opt/homebrew/bin/python3.14
"""
Knowledge Coverage Map — Visualize wiki topic distribution

Usage:
    python coverage_map.py
"""

import os
import re
from collections import Counter
from pathlib import Path
from typing import List, Dict

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CONCEPTS_PATH = WIKI_PATH / "concepts"
TOP_N = 30  # Show top N tags

# ═══════════════════════════════════════════════════════════════

def parse_frontmatter(content: str) -> Dict:
    """Parse YAML frontmatter from markdown content"""
    frontmatter = {}
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm_text = content[3:end]
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'')
    return frontmatter

def extract_tags(content: str) -> List[str]:
    """Extract tags from frontmatter"""
    fm = parse_frontmatter(content)
    tags_str = fm.get('tags', '')
    if not tags_str:
        return []
    # Parse tags like [ml, ai, paper]
    tags_str = tags_str.strip('[]')
    return [t.strip() for t in tags_str.split(',') if t.strip()]

def extract_type(content: str) -> str:
    """Extract type from frontmatter"""
    fm = parse_frontmatter(content)
    return fm.get('type', 'unknown')

def count_words(content: str) -> int:
    """Count words in content (excluding frontmatter)"""
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            content = content[end+3:]
    words = content.split()
    return len(words)

def get_all_pages() -> List[Dict]:
    """Get all concept pages with metadata"""
    pages = []
    if not CONCEPTS_PATH.exists():
        return pages
    
    for md_file in CONCEPTS_PATH.glob("*.md"):
        try:
            content = md_file.read_text()
            pages.append({
                'name': md_file.stem,
                'path': md_file,
                'content': content,
                'tags': extract_tags(content),
                'type': extract_type(content),
                'words': count_words(content)
            })
        except:
            pass
    
    return pages

def generate_tag_cloud():
    """Generate tag coverage visualization"""
    pages = get_all_pages()
    all_tags = []
    
    for page in pages:
        all_tags.extend(page['tags'])
    
    tag_counts = Counter(all_tags)
    
    print("=" * 70)
    print("KNOWLEDGE COVERAGE MAP")
    print("=" * 70)
    print(f"\nTotal concept pages: {len(pages)}")
    print(f"Total tags used: {len(tag_counts)}")
    print()
    
    # Tag distribution
    print("TAG DISTRIBUTION (by frequency)")
    print("-" * 70)
    
    max_count = max(tag_counts.values()) if tag_counts else 1
    bar_width = 40
    
    for tag, count in tag_counts.most_common(TOP_N):
        bar_len = int(count / max_count * bar_width)
        bar = "█" * bar_len
        pct = count / len(pages) * 100
        print(f"  {tag:<25} {bar:<40} {count:>3} ({pct:>5.1f}%)")
    
    # Type distribution
    print("\nTYPE DISTRIBUTION")
    print("-" * 70)
    type_counts = Counter(p['type'] for p in pages)
    for type_name, count in type_counts.most_common():
        pct = count / len(pages) * 100
        bar_len = int(pct / 100 * bar_width)
        bar = "█" * bar_len
        print(f"  {type_name:<25} {bar:<40} {count:>3} ({pct:>5.1f}%)")
    
    # Content length stats
    print("\nCONTENT LENGTH STATS")
    print("-" * 70)
    if pages:
        total_words = sum(p['words'] for p in pages)
        avg_words = total_words / len(pages)
        print(f"  Total words:        {total_words:,}")
        print(f"  Average per page:   {avg_words:,.0f}")
        print(f"  Min:                {min(p['words'] for p in pages):,}")
        print(f"  Max:                {max(p['words'] for p in pages):,}")
    
    # Pages without tags
    print("\nPAGES WITHOUT TAGS")
    print("-" * 70)
    no_tags = [p for p in pages if not p['tags']]
    if no_tags:
        for p in no_tags[:10]:
            print(f"  • {p['name']}")
        if len(no_tags) > 10:
            print(f"  ... and {len(no_tags) - 10} more")
    else:
        print("  None ✓")
    
    # Gap Analysis
    print("\n" + "=" * 70)
    print("GAP ANALYSIS")
    print("=" * 70)
    
    # Expected topics based on what we've discussed
    expected_topics = {
        'ml', 'ai', 'machine-learning', 'llm', 'transformers',
        'apple-silicon', 'optimization', 'local-ai', 'pruning',
        'fine-tuning', 'synthetic-data'
    }
    
    actual_topics = set(tag_counts.keys())
    gaps = expected_topics - actual_topics
    
    if gaps:
        print("  Topics from our discussions but not in wiki:")
        for gap in sorted(gaps):
            print(f"    • {gap}")
    else:
        print("  ✓ Wiki covers all major discussion topics")
    
    # Orphan tags (tags used only once)
    orphan_tags = [tag for tag, count in tag_counts.items() if count == 1]
    if orphan_tags:
        print(f"\n  Orphan tags (used only once): {len(orphan_tags)}")
        print("  Consider merging or expanding:")
        for tag in list(orphan_tags)[:5]:
            print(f"    • {tag}")
    
    print("=" * 70)

if __name__ == "__main__":
    generate_tag_cloud()
