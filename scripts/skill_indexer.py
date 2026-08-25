#!/usr/bin/env python3
"""
Skill Indexer — builds a searchable index of all skills.

Scans ~/.hermes/skills/ for SKILL.md files, extracts:
- name, description, category, tags
- first 500 chars of content (for keyword matching)
- trigger_conditions (when to use this skill)
- use_case_keywords (extracted from description + content)

Output: ~/.hermes/skills/_index.json

Usage:
    python3 skill_indexer.py          # build index
    python3 skill_indexer.py --watch  # watch mode (requires watchdog)
"""

import json
import os
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Tuple, List, Dict, Set

# ─── Paths ────────────────────────────────────────────────────────────────────

HERMES_HOME = Path.home() / ".hermes"
SKILLS_DIR = HERMES_HOME / "skills"
INDEX_PATH = SKILLS_DIR / "_index.json"

# Skip these system directories when scanning (must match skill_commands.py)
_EXCLUDED_SKILL_DIRS = frozenset((".git", ".github", ".hub"))

# ─── YAML Frontmatter Parsing ─────────────────────────────────────────────────

def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 4)
    if end == -1:
        return {}, content
    try:
        import yaml
        frontmatter = yaml.safe_load(content[4:end])
        body = content[end + 4:].lstrip("\n")
        return (frontmatter or {}), body
    except Exception:
        return {}, content[end + 4:]


def parse_tags(tags_value) -> List[str]:
    """Parse tags from frontmatter value."""
    if not tags_value:
        return []
    if isinstance(tags_value, list):
        return [str(t).strip() for t in tags_value if t]
    tags_value = str(tags_value).strip()
    if tags_value.startswith("[") and tags_value.endswith("]"):
        tags_value = tags_value[1:-1]
    return [t.strip().strip("\"'") for t in tags_value.split(",") if t.strip()]


# ─── Keyword Extraction ────────────────────────────────────────────────────────

# Stopwords for Vietnamese + English (common in technical content)
STOPWORDS = frozenset([
    # English
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "is", "was", "are", "were", "been", "be", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might", "must",
    "shall", "can", "need", "dare", "ought", "used", "it", "its", "this", "that",
    "these", "those", "i", "you", "he", "she", "we", "they", "what", "which", "who",
    "when", "where", "why", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "just", "also", "now", "here", "there", "then",
    "once", "if", "because", "until", "while", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "up", "down",
    "out", "off", "over", "under", "again", "further", "any", "many", "much",
    "your", "their", "our", "my", "his", "her", "when", "where", "why", "how",
    "use", "using", "used", "uses", "optional", "required", "example", "see",
    "file", "files", "path", "default", "value", "values", "key", "name", "names",
    "type", "types", "string", "int", "integer", "list", "dict", "bool", "boolean",
    "null", "none", "true", "false", "return", "returns", "arg", "args", "argument",
    "arguments", "parameter", "parameters", "class", "function", "method", "data",
    "like", "not", "are", "was", "were", "is", "be", "has", "have", "had", "get",
    # Vietnamese common
    "và", "của", "là", "có", "được", "trong", "cho", "với", "này", "để", "từ",
    "khi", "như", "hoặc", "các", "một", "về", "ra", "vào", "lại", "nên", "phải",
    "không", "tại", "bởi", "cũng", "sau", "trước", "mà", "thì", "đã", "sẽ",
    "nếu", "vì", "nên", "hay", "nhưng", "do", "đó", "đây", "kia", "nọ",
])


def extract_keywords(text: str, max_keywords: int = 30) -> List[str]:
    """
    Extract meaningful keywords from text.
    Returns lowercase tokens (2+ chars, not stopwords, not pure numbers).
    """
    # Split on whitespace and punctuation, keep alphanumeric+
    tokens = re.findall(r"[a-zA-Z_À-ỹ][a-zA-Z0-9_À-ỹ]*", text.lower())
    keywords = []
    for token in tokens:
        if len(token) < 2:
            continue
        if token in STOPWORDS:
            continue
        # Skip pure numbers
        if token.isdigit():
            continue
        keywords.append(token)
        if len(keywords) >= max_keywords:
            break
    return keywords


def extract_trigger_keywords(description: str, body: str) -> List[str]:
    """
    Extract trigger-condition keywords — the use-case phrases that indicate
    when a skill should be loaded (Garry Tan's "fat skills" philosophy).
    """
    combined = f"{description} {body[:2000]}"
    keywords = extract_keywords(combined, max_keywords=40)

    # Boost phrases that look like use-case triggers
    trigger_indicators = [
        "use when", "use for", "use this", "apply when", "useful for",
        "invoked when", "trigger", "when the user", "when you need",
        "for building", "for creating", "for managing", "for automating",
        "for testing", "for debugging", "for deploying", "for running",
        "for generating", "for extracting", "for searching", "for querying",
    ]

    trigger_phrases = []
    for indicator in trigger_indicators:
        idx = combined.lower().find(indicator)
        if idx != -1:
            phrase = combined[max(0, idx-20):idx+60].strip()
            trigger_phrases.extend(extract_keywords(phrase, max_keywords=5))

    # Merge and dedupe
    all_keywords = list(dict.fromkeys(keywords + trigger_phrases))[:40]
    return all_keywords


# ─── Category Detection ────────────────────────────────────────────────────────

def get_category_from_path(skill_path: Path) -> Optional[str]:
    """Extract category from skill path like ~/.hermes/skills/mlops/axolotl/SKILL.md"""
    try:
        rel = skill_path.resolve().relative_to(SKILLS_DIR.resolve())
        parts = rel.parts
        if len(parts) >= 3:
            return parts[0]
        return None
    except ValueError:
        return None


# ─── Skill Scanning ───────────────────────────────────────────────────────────

def scan_skills() -> List[dict]:
    """Scan all SKILL.md files and build indexed records."""
    if not SKILLS_DIR.exists():
        SKILLS_DIR.mkdir(parents=True, exist_ok=True)
        return []

    skills: list[dict[str, Any]] = []

    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        # Skip hidden system dirs only (.git, .github, .hub)
        if any(part in _EXCLUDED_SKILL_DIRS for part in skill_md.parts):
            continue

        try:
            content = skill_md.read_text(encoding="utf-8")
        except Exception:
            continue

        frontmatter, body = parse_frontmatter(content)

        name = frontmatter.get("name") or skill_md.parent.name
        description = frontmatter.get("description", "")

        # Category
        category = frontmatter.get("category")
        if not category:
            category = get_category_from_path(skill_md)

        # Tags
        raw_tags = frontmatter.get("tags", [])
        tags = parse_tags(raw_tags)
        # Also check metadata.hermes.tags
        metadata = frontmatter.get("metadata", {}) or {}
        if isinstance(metadata, dict):
            hermes_meta = metadata.get("hermes", {}) or {}
            if isinstance(hermes_meta, dict):
                raw_tags = hermes_meta.get("tags", [])
                tags = tags + parse_tags(raw_tags)
        tags = list(dict.fromkeys(tags))  # dedupe

        # Trigger conditions (frontmatter field — Garry Tan's "when to use")
        raw_trigger = frontmatter.get("trigger_conditions", [])
        if isinstance(raw_trigger, str):
            raw_trigger = [raw_trigger]
        trigger_conditions: List[str] = []
        if isinstance(raw_trigger, list):
            for t in raw_trigger:
                if isinstance(t, str) and t.strip():
                    trigger_conditions.append(t.strip())
                elif isinstance(t, dict):
                    trigger_conditions.append(str(t).strip())

        # Content preview (first 500 chars of body, no frontmatter)
        content_preview = body.strip()[:500] if body else ""

        # Keyword extraction
        use_case_keywords = extract_trigger_keywords(description, body)

        # Skill path (relative to SKILLS_DIR)
        try:
            skill_rel = skill_md.resolve().relative_to(SKILLS_DIR.resolve())
            skill_dir = str(skill_rel.parent)
        except ValueError:
            skill_dir = skill_md.parent.name

        # File hash (for change detection)
        content_hash = hashlib.md5(content.encode()).hexdigest()[:12]

        skill_record = {
            "name": name,
            "description": description,
            "category": category,
            "tags": tags,
            "trigger_conditions": trigger_conditions,
            "content_preview": content_preview,
            "use_case_keywords": use_case_keywords,
            "skill_dir": skill_dir,
            "skill_md_path": str(skill_md.relative_to(SKILLS_DIR)),
            "content_hash": content_hash,
            "indexed_at": datetime.now().isoformat(),
        }

        skills.append(skill_record)

    return skills


# ─── Index Building ───────────────────────────────────────────────────────────

def build_index() -> dict[str, Any]:
    """Build the complete skill index."""
    skills = scan_skills()

    # Sort by category, then name
    skills.sort(key=lambda s: (s.get("category") or "", s["name"]))

    # Build category list
    categories = sorted(set(
        s.get("category") for s in skills if s.get("category")
    ))

    index = {
        "version": 1,
        "generated_at": datetime.now().isoformat(),
        "total_skills": len(skills),
        "categories": categories,
        "skills": skills,
    }

    return index


def save_index(index: dict[str, Any]) -> None:
    """Save index to _index.json."""
    INDEX_PATH.write_text(
        json.dumps(index, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"Index saved: {INDEX_PATH}")
    print(f"  Total skills: {index['total_skills']}")
    print(f"  Categories: {len(index['categories'])}")


# ─── Skill Recommendation Engine ──────────────────────────────────────────────

def recommend_skills(
    task_description: str,
    top_k: int = 5,
    category_filter: Optional[str] = None,
) -> List[Tuple[dict, float]]:
    """
    Find the best-matching skills for a task description.

    Uses a multi-signal scoring approach (no embeddings needed):
    1. Exact keyword overlap between task and skill's use_case_keywords
    2. Trigger-condition match (if skill has trigger_conditions, weight higher)
    3. Description keyword match (lower weight)
    4. Tag overlap

    Returns list of (skill_record, score) sorted by descending score.
    """
    # Load index
    if not INDEX_PATH.exists():
        print("Index not found, building...", file=sys.stderr)
        index = build_index()
        save_index(index)
    else:
        try:
            index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error loading index: {e}, rebuilding...", file=sys.stderr)
            index = build_index()
            save_index(index)

    skills = index.get("skills", [])
    if not skills:
        return []

    # Extract keywords from task description
    task_keywords = set(extract_keywords(task_description, max_keywords=50))

    scored: list[tuple[dict[str, Any], float]] = []

    for skill in skills:
        if category_filter and skill.get("category") != category_filter:
            continue

        score = 0.0

        # 1. use_case_keywords match (weight: 3.0) — highest signal
        skill_keywords = set(skill.get("use_case_keywords", []))
        kw_overlap = task_keywords & skill_keywords
        score += len(kw_overlap) * 3.0

        # 2. trigger_conditions match (weight: 5.0) — Garry Tan's "fat skills"
        trigger_conditions = skill.get("trigger_conditions", [])
        if trigger_conditions:
            for trigger in trigger_conditions:
                trigger_keywords = set(extract_keywords(trigger, max_keywords=20))
                trigger_overlap = task_keywords & trigger_keywords
                score += len(trigger_overlap) * 5.0

        # 3. description match (weight: 1.5)
        desc_keywords = set(extract_keywords(skill.get("description", ""), max_keywords=30))
        desc_overlap = task_keywords & desc_keywords
        score += len(desc_overlap) * 1.5

        # 4. tag overlap (weight: 2.0)
        skill_tags = set(skill.get("tags", []))
        # Tags often have hyphens, split them
        expanded_tags: set[str] = set()
        for tag in skill_tags:
            expanded_tags.add(tag.lower())
            if "-" in tag:
                expanded_tags.update(tag.lower().split("-"))
        tag_overlap = task_keywords & expanded_tags
        score += len(tag_overlap) * 2.0

        # 5. content_preview match (weight: 0.5) — lower priority
        preview_keywords = set(extract_keywords(
            skill.get("content_preview", ""), max_keywords=20
        ))
        preview_overlap = task_keywords & preview_keywords
        score += len(preview_overlap) * 0.5

        if score > 0:
            scored.append((skill, score))

    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)

    return scored[:top_k]


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Skill indexer and recommendation engine")
    parser.add_argument("--watch", action="store_true", help="Watch mode (requires watchdog)")
    parser.add_argument("--recommend", type=str, help="Task description to recommend skills for")
    parser.add_argument("--top-k", type=int, default=5, help="Number of recommendations (default: 5)")
    parser.add_argument("--category", type=str, help="Filter by category")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild index")
    args = parser.parse_args()

    # Rebuild if requested or if index doesn't exist
    if args.rebuild or not INDEX_PATH.exists():
        print("Building skill index...")
        index = build_index()
        save_index(index)
    else:
        index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
        print(f"Index loaded: {index['total_skills']} skills, {len(index['categories'])} categories")

    if args.watch:
        print("Watch mode not yet implemented — use --rebuild to update")
        return

    if args.recommend:
        recommendations = recommend_skills(
            args.recommend,
            top_k=args.top_k,
            category_filter=args.category,
        )
        print(f"\nTop {len(recommendations)} recommendations for: {args.recommend!r}")
        print("-" * 60)
        for i, (skill, score) in enumerate(recommendations, 1):
            print(f"\n{i}. {skill['name']} (score: {score:.1f})")
            print(f"   Category: {skill.get('category') or 'uncategorized'}")
            print(f"   Description: {skill.get('description', '')[:120]}")
            if skill.get('trigger_conditions'):
                print(f"   Trigger: {skill['trigger_conditions'][0][:80]}")
            print(f"   Keywords: {', '.join(skill.get('use_case_keywords', [])[:10])}")


if __name__ == "__main__":
    main()
