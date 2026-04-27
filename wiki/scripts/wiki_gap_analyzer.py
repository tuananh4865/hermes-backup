#!/opt/homebrew/bin/python3.14
"""
Wiki Gap Analyzer

Finds missing topics that should exist based on:
1. Related concepts that are mentioned but don't have pages
2. Topics suggested by existing page clusters
3. Common patterns in user's interests (from transcripts)

Usage:
    python3 scripts/wiki_gap_analyzer.py [--all] [--min-score N]
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

# Topics that should probably have pages (based on user's interests)
SUGGESTED_TOPICS = {
    "lm-studio": {"related": ["ollama", "local-llm", "mlx", "models"], "score": 10},
    "ollama": {"related": ["lm-studio", "local-llm", "models"], "score": 8},
    "local-llm": {"related": ["lm-studio", "ollama", "mlx", "huggingface"], "score": 9},
    "hermes": {"related": ["hermes-agent", "telegram", "mcp"], "score": 8},
    "hermes-agent": {"related": ["hermes", "gateway", "hooks"], "score": 9},
    "mcp": {"related": ["tools", "hermes-agent", "safari"], "score": 7},
    "telegram": {"related": ["messaging", "bots", "hermes-agent"], "score": 7},
    "wiki": {"related": ["obsidian", "knowledge-base", "wikilinks"], "score": 9},
    "obsidian": {"related": ["wikilinks", "vault", "plugins"], "score": 8},
    "github": {"related": ["git", "sync", "repo"], "score": 8},
    "git": {"related": ["github", "commit", "branch"], "score": 7},
    "browser": {"related": ["automation", "mcp", "scrape"], "score": 6},
    "automation": {"related": ["scripts", "workflow", "cron"], "score": 7},
    "scripts": {"related": ["automation", "python", "workflow"], "score": 6},
    "knowledge-base": {"related": ["wiki", "obsidian", "rag"], "score": 8},
    "rag": {"related": ["knowledge-base", "embedding", "search"], "score": 7},
    "embedding": {"related": ["rag", "vector", "search"], "score": 6},
    "models": {"related": ["lm-studio", "ollama", "huggingface", "local-llm"], "score": 9},
    "huggingface": {"related": ["models", "embedding", "fine-tuning"], "score": 8},
    "fine-tuning": {"related": ["models", "training", "lora"], "score": 8},
    "training": {"related": ["fine-tuning", "dataset", "models"], "score": 7},
    "lora": {"related": ["fine-tuning", "training", "models"], "score": 7},
}

# Topic keywords to detect from content
TOPIC_PATTERNS = {
    "lm-studio": [r"lm\s*studio", r"lm-studio"],
    "ollama": [r"ollama"],
    "local-llm": [r"local\s*llm", r"local-llm", r"local\s*model"],
    "hermes-agent": [r"hermes\s*agent"],
    "mcp": [r"\bmcp\b", r"model\s*context\s*protocol"],
    "telegram": [r"telegram"],
    "obsidian": [r"obsidian"],
    "github": [r"github"],
    "git": [r"\bgit\b"],
    "wiki": [r"\bwiki\b"],
    "browser": [r"browser", r"scrape", r"crawl"],
    "automation": [r"automation", r"auto(-|\s)ingest"],
    "knowledge-base": [r"knowledge\s*base", r"knowledge\s*management"],
    "rag": [r"\brag\b", r"retrieval\s*augmented"],
    "models": [r"\bmodel", r"llm"],
    "huggingface": [r"hugging\s*face", r"hf\s*hub"],
    "fine-tuning": [r"fine.?tun", r"finetun"],
    "training": [r"training", r"train\s*model"],
    "lora": [r"\blora\b"],
    "mlx": [r"\bmlx\b"],
    "python": [r"python"],
    "javascript": [r"javascript", r"js\b"],
    "typescript": [r"typescript", r"ts\b"],
}

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


def extract_wikilinks(content: str) -> List[str]:
    """Extract all [[wikilinks]] from content"""
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)


def get_existing_topics(files: List[Path]) -> Set[str]:
    """Get all existing topic/page names"""
    topics = set()
    for f in files:
        topics.add(f.stem.lower())
    return topics


def get_content_for_analysis(files: List[Path]) -> Dict[str, str]:
    """Get all content keyed by page name"""
    content_map = {}
    for f in files:
        content_map[f.stem.lower()] = f.read_text(encoding="utf-8")
    return content_map


# ═══════════════════════════════════════════════════════════════
# GAP DETECTION
# ═══════════════════════════════════════════════════════════════

def find_topic_mentions(content_map: Dict[str, str]) -> Dict[str, List[str]]:
    """
    Scan all content for mentions of topics.
    Returns: {topic: [pages_mentioning_topic]}
    """
    mentions = defaultdict(list)
    
    for page_name, content in content_map.items():
        content_lower = content.lower()
        
        for topic, patterns in TOPIC_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    mentions[topic].append(page_name)
                    break
    
    return mentions


def find_suggested_but_missing(mentions: Dict[str, List[str]], existing: Set[str]) -> List[Dict]:
    """
    Find topics that are mentioned but don't have pages.
    These are gaps that could be filled.
    """
    gaps = []
    
    for topic, data in SUGGESTED_TOPICS.items():
        if topic in existing:
            continue  # Already exists
        
        mention_count = len(mentions.get(topic, []))
        if mention_count > 0:
            base_score = data["score"]
            # Boost score if mentioned often but no page exists
            adjusted_score = base_score + (mention_count * 0.5)
            
            gaps.append({
                "topic": topic,
                "suggested_score": round(adjusted_score, 1),
                "mentioned_in": mentions.get(topic, []),
                "mention_count": mention_count,
                "related": data["related"],
            })
    
    # Sort by score
    gaps.sort(key=lambda x: x["suggested_score"], reverse=True)
    return gaps


def find_cluster_gaps(content_map: Dict[str, str], existing: Set[str]) -> List[Dict]:
    """
    Find topics that are related to existing clusters but missing.
    E.g., if user has "lm-studio" and "ollama" pages, maybe they need a "local-llm" overview.
    """
    gaps = []
    
    for f_stem, content in content_map.items():
        wikilinks = extract_wikilinks(content)
        
        for link in wikilinks:
            link_lower = link.lower()
            
            # If this link exists, check what related topics might also be needed
            if link_lower in SUGGESTED_TOPICS:
                related = SUGGESTED_TOPICS[link_lower]["related"]
                for rel_topic in related:
                    if rel_topic not in existing:
                        gaps.append({
                            "topic": rel_topic,
                            "suggested_score": 5.0,  # Medium priority
                            "suggested_by": f_stem,
                            "reason": f"Related to [[{link}]] but no page exists",
                            "related": [link],
                        })
    
    # Deduplicate by topic
    seen = set()
    unique_gaps = []
    for gap in gaps:
        if gap["topic"] not in seen:
            seen.add(gap["topic"])
            unique_gaps.append(gap)
    
    unique_gaps.sort(key=lambda x: x["suggested_score"], reverse=True)
    return unique_gaps


# ═══════════════════════════════════════════════════════════════
# REPORTING
# ═══════════════════════════════════════════════════════════════

def print_report(gaps: List[Dict], mentioned_gaps: List[Dict], cluster_gaps: List[Dict]):
    """Print gap analysis report"""
    print("=" * 80)
    print("WIKI GAP ANALYSIS REPORT")
    print("=" * 80)
    print()
    
    # Section 1: Suggested topics based on user interests
    print("-" * 80)
    print("HIGH-PRIORITY GAPS (Suggested Topics)")
    print("-" * 80)
    print("Topics that align with user's interests but don't exist yet:")
    print()
    
    for gap in gaps[:10]:
        print(f"  [[{gap['topic']}]] (score: {gap['suggested_score']})")
        if gap["mentioned_in"]:
            print(f"    Mentioned in: {', '.join(gap['mentioned_in'][:5])}")
        if gap["related"]:
            print(f"    Related to: {', '.join(['[[' + r + ']]' for r in gap['related'][:3]])}")
        print()
    
    # Section 2: Cluster-based gaps
    if cluster_gaps:
        print("-" * 80)
        print("CLUSTER GAPS (Related to Existing Pages)")
        print("-" * 80)
        print("Topics that complete existing topic clusters:")
        print()
        
        for gap in cluster_gaps[:10]:
            print(f"  [[{gap['topic']}]] (score: {gap['suggested_score']})")
            print(f"    Suggested by: {gap['suggested_by']}")
            print(f"    Reason: {gap['reason']}")
            print()
    
    # Summary
    print("-" * 80)
    print("SUMMARY")
    print("-" * 80)
    total_gaps = len(gaps) + len(cluster_gaps)
    print(f"Total gaps found: {total_gaps}")
    print(f"  - Suggested topics: {len(gaps)}")
    print(f"  - Cluster gaps: {len(cluster_gaps)}")
    print()
    print("Recommendation: Create pages for top 5 gaps first.")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Wiki Gap Analyzer")
    parser.add_argument("--all", action="store_true", help="Run full analysis")
    parser.add_argument("--min-score", type=float, default=5.0, help="Minimum score to report")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    
    files = get_all_wiki_pages(WIKI_PATH)
    existing = get_existing_topics(files)
    content_map = get_content_for_analysis(files)
    
    print(f"Wiki path: {WIKI_PATH}")
    print(f"Existing pages: {len(existing)}")
    print()
    
    # Find mentions
    mentions = find_topic_mentions(content_map)
    
    # Find gaps
    suggested_gaps = find_suggested_but_missing(mentions, existing)
    cluster_gaps = find_cluster_gaps(content_map, existing)
    
    # Filter by min score
    suggested_gaps = [g for g in suggested_gaps if g["suggested_score"] >= args.min_score]
    cluster_gaps = [g for g in cluster_gaps if g["suggested_score"] >= args.min_score]
    
    if args.json:
        print(json.dumps({
            "suggested_gaps": suggested_gaps,
            "cluster_gaps": cluster_gaps
        }, indent=2))
    else:
        print_report(suggested_gaps, [], cluster_gaps)


if __name__ == "__main__":
    main()
