#!/opt/homebrew/bin/python3.14
"""
Wiki Auto-Improve Script

Autonomous content generation for wiki:
1. Run gap analysis to find missing topics
2. Generate content using LM Studio
3. Auto-create pages for high-priority gaps

Usage:
    python3 scripts/wiki_auto_improve.py [--dry-run] [--min-score N]
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
LM_STUDIO_URL = "http://192.168.0.187:1234/v1/chat/completions"
MODEL = "qwen3.5-2b"
MIN_GAP_SCORE = 8.0  # Only auto-generate for high-priority gaps

# ═══════════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════════

def get_all_wiki_pages(path: Path) -> set:
    """Get existing page names"""
    pages = set()
    for f in path.rglob("*.md"):
        if any(x in f.parts for x in ["raw", "_archive", ".obsidian", "__pycache__"]):
            continue
        pages.add(f.stem.lower())
    return pages


def call_lm_studio(prompt: str, max_tokens: int = 500) -> str:
    """Call LM Studio API for content generation"""
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.7,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        LM_STUDIO_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.URLError as e:
        print(f"LM Studio error: {e}")
        return None


def generate_topic_content(topic: str, related_topics: list) -> str:
    """Generate wiki page content for a topic using LM Studio"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    related_str = ", ".join([f"[[{t}]]" for t in related_topics[:5]])
    topic_title = topic.replace("-", " ").replace("_", " ").title()
    
    system_prompt = f"""You are a wiki writer. Generate ONLY frontmatter + brief content for topic: {topic_title}

Use this EXACT format (no explanations, just output the page):

---
title: "{topic_title}"
created: {today}
updated: {today}
type: concept
tags: [{topic}, auto-generated]
---

# {topic_title}

{{1-2 sentence overview}}

## Key Points

{{2-3 bullet points}}

## Related

{related_str}"""

    content = call_lm_studio(system_prompt, max_tokens=400)
    return content


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki Auto-Improve")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without creating pages")
    parser.add_argument("--min-score", type=float, default=MIN_GAP_SCORE, help=f"Minimum gap score (default {MIN_GAP_SCORE})")
    parser.add_argument("--topic", type=str, help="Generate specific topic only")
    args = parser.parse_args()
    
    # Run gap analysis
    gap_script = WIKI_PATH / "scripts" / "wiki_gap_analyzer.py"
    if not gap_script.exists():
        print("Error: wiki_gap_analyzer.py not found")
        sys.exit(1)
    
    # Import gap analyzer functions
    sys.path.insert(0, str(WIKI_PATH / "scripts"))
    try:
        from wiki_gap_analyzer import (
            find_suggested_but_missing, 
            find_cluster_gaps, 
            get_all_wiki_pages as ga_get_pages, 
            get_content_for_analysis, 
            find_topic_mentions,
            get_existing_topics
        )
    except ImportError as e:
        print(f"Import error: {e}")
        sys.exit(1)
    
    files = ga_get_pages(WIKI_PATH)
    existing = get_existing_topics(files)
    content_map = get_content_for_analysis(files)
    mentions = find_topic_mentions(content_map)
    
    suggested_gaps = find_suggested_but_missing(mentions, existing)
    suggested_gaps = [g for g in suggested_gaps if g["suggested_score"] >= args.min_score]
    
    print("=" * 80)
    print("WIKI AUTO-IMPROVE")
    print("=" * 80)
    print()
    print(f"Wiki path: {WIKI_PATH}")
    print(f"Min gap score: {args.min_score}")
    print(f"High-priority gaps found: {len(suggested_gaps)}")
    print()
    
    if not suggested_gaps:
        print("No high-priority gaps found. Wiki is well-covered! ✅")
        return
    
    print("Gaps to potentially fill:")
    for gap in suggested_gaps[:5]:
        print(f"  [[{gap['topic']}]] (score: {gap['suggested_score']})")
        print(f"    Mentioned in: {', '.join(gap['mentioned_in'][:3])}")
    print()
    
    if args.dry_run:
        print("DRY RUN - No pages created. Use without --dry-run to generate.")
        return
    
    # Generate content for top gaps
    print("-" * 80)
    print("GENERATING CONTENT")
    print("-" * 80)
    
    created_count = 0
    for gap in suggested_gaps[:3]:  # Limit to top 3 per run
        topic = gap["topic"]
        related = gap.get("related", [])
        
        print(f"\nGenerating [[{topic}]]...")
        content = generate_topic_content(topic, related)
        
        if not content:
            print(f"  Failed to generate content for {topic}")
            continue
        
        # Save page
        page_path = WIKI_PATH / "concepts" / f"{topic}.md"
        if page_path.exists():
            print(f"  Page already exists, skipping")
            continue
        
        try:
            page_path.write_text(content, encoding="utf-8")
            print(f"  Created: {page_path.relative_to(WIKI_PATH)}")
            created_count += 1
        except Exception as e:
            print(f"  Error saving: {e}")
    
    print()
    print(f"Done! Created {created_count} new pages.")
    print(f"Run: cd ~/wiki && git add -A && git commit -m 'feat: auto-generated pages' && git push")


if __name__ == "__main__":
    main()
