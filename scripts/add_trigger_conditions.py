#!/usr/bin/env python3
"""
Add trigger_conditions to skill frontmatter.

Usage:
    python3 add_trigger_conditions.py              # dry run (show suggestions)
    python3 add_trigger_conditions.py --apply      # actually modify SKILL.md files
    python3 add_trigger_conditions.py --apply --force  # overwrite existing trigger_conditions
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Any, Optional

HERMES_HOME = Path.home() / ".hermes"
SKILLS_DIR = HERMES_HOME / "skills"

STOPWORDS = frozenset([
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "as", "is", "was", "are", "were", "be", "have", "has", "had",
    "use", "using", "used", "use when", "use for", "use this", "useful for",
    "when you need", "when the user", "if you need", "invoked when",
    "skill", "description", "this", "that", "it", "its", "not", "are",
])


def extract_use_case_phrases(description: str, body: str, max_phrases: int = 3) -> list[str]:
    """Extract natural language phrases that describe when to use this skill."""
    combined = f"{description} {body[:3000]}"
    phrases = []

    # Pattern 1: "Use when...", "Use for...", "Use this when..."
    use_patterns = [
        r"use\s+(?:this\s+)?(?:skill\s+)?(?:when|when you need|for)\s+([^.,]+)",
        r"useful\s+for\s+([^.,]+)",
        r"apply\s+(?:this\s+)?(?:skill\s+)?(?:when|for)\s+([^.,]+)",
        r"invoked\s+(?:when|when you need)\s+([^.,]+)",
        r"triggered?\s+(?:when|by|for)\s+([^.,]+)",
        r"when\s+(?:the\s+)?(?:user|you)\s+(?:want|need|ask|want\s+to)\s+([^.,]+)",
    ]

    for pattern in use_patterns:
        for m in re.finditer(pattern, combined, re.IGNORECASE):
            phrase = m.group(1).strip()
            # Clean up: remove trailing stuff, limit length
            phrase = re.sub(r"\s+", " ", phrase).strip()
            phrase = phrase[:100]
            if len(phrase) > 10 and phrase.lower() not in STOPWORDS:
                phrases.append(f"when {phrase}" if not phrase.startswith("when ") else phrase)

    # Dedupe while preserving order
    seen = set()
    unique = []
    for p in phrases:
        key = p.lower()[:50]
        if key not in seen:
            seen.add(key)
            unique.append(p)
        if len(unique) >= max_phrases:
            break

    return unique


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown."""
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 4)
    if end == -1:
        return {}, content
    try:
        fm = yaml.safe_load(content[4:end])
        body = content[end + 4:]
        return (fm or {}), body
    except Exception:
        return {}, content[end + 4:]


def build_frontmatter(fm: dict) -> str:
    """Build YAML frontmatter string from dict."""
    # Use block style for trigger_conditions if present
    fm_copy = dict(fm)
    if "trigger_conditions" in fm_copy:
        tc = fm_copy["trigger_conditions"]
        if isinstance(tc, list) and tc:
            fm_copy["trigger_conditions"] = tc

    lines = yaml.dump(fm_copy, default_flow_style=False, sort_keys=False, allow_unicode=True)
    return f"---\n{lines}---\n"


def process_skill(skill_md: Path, dry_run: bool = True, force: bool = False) -> Optional[str]:
    """Process a single SKILL.md file. Returns suggestion or None."""
    try:
        raw = skill_md.read_text(encoding="utf-8")
    except Exception:
        return None

    frontmatter, body = parse_frontmatter(raw)
    name = frontmatter.get("name", skill_md.parent.name)
    description = frontmatter.get("description", "")

    # Check if already has trigger_conditions
    existing_tc = frontmatter.get("trigger_conditions", [])
    if existing_tc and not force:
        return None  # Already has trigger_conditions

    # Extract phrases
    phrases = extract_use_case_phrases(description, body)

    if not phrases:
        return None

    if dry_run:
        return f"  {name}: {phrases}"

    # Add trigger_conditions to frontmatter
    frontmatter["trigger_conditions"] = phrases
    new_frontmatter = build_frontmatter(frontmatter)
    new_content = new_frontmatter + body

    skill_md.write_text(new_content, encoding="utf-8")
    return f"  {name}: added {len(phrases)} triggers"


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Add trigger_conditions to skills")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing trigger_conditions")
    parser.add_argument("--skill", type=str, help="Process only this skill name")
    args = parser.parse_args()

    dry_run = not args.apply

    if dry_run:
        print("DRY RUN — no files will be modified (use --apply to apply)")
        print()

    count = 0
    modified = 0

    for skill_md in SKILLS_DIR.rglob("SKILL.md"):
        if any(part in (".git", ".github", ".hub") for part in skill_md.parts):
            continue

        if args.skill:
            if skill_md.parent.name != args.skill:
                continue

        result = process_skill(skill_md, dry_run=dry_run, force=args.force)
        if result:
            print(result)
            modified += 1
        count += 1

    print()
    if dry_run:
        print(f"Dry run: {modified} skills would get trigger_conditions, {count} total scanned")
    else:
        print(f"Applied: {modified} skills modified out of {count} total")


if __name__ == "__main__":
    main()
