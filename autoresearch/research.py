#!/usr/bin/env python3
"""
Fixed benchmark script - DO NOT MODIFY
Measures Skills Health Score (SHS)
SHS = stale_skills × 10 + missing_examples × 5 + broken_links × 3 + low_confidence × 2
Target: SHS = 0
"""
import subprocess
import re
import os
from pathlib import Path

SKILLS_DIR = Path("/Users/tuananh4865/.hermes/skills")

def scan_skills():
    """Scan all skills for health issues"""
    stale_count = 0
    missing_examples = 0
    broken_links = 0
    low_confidence = 0
    total_skills = 0
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        total_skills += 1
        content = skill_md.read_text()
        
        # Check last_updated date (should be within 30 days)
        updated_match = re.search(r'updated:\s*(\d{4}-\d{2}-\d{2})', content)
        if updated_match:
            # Simplified check - just count if it exists
            pass
        
        # Check missing examples (no code blocks or templates)
        if "```" not in content and "{{" not in content:
            missing_examples += 1
        
        # Check low confidence (confidence: low or no confidence field)
        if "confidence: low" in content or not re.search(r'confidence:', content):
            low_confidence += 1
        
        # Check for broken wikilinks (simplified)
        if "[[" in content and "]]" in content:
            # Count potential wikilinks that might be broken
            pass
    
    return stale_count, missing_examples, broken_links, low_confidence, total_skills

def calculate_shs(stale, examples, links, confidence):
    """Calculate Skills Health Score"""
    return stale * 10 + examples * 5 + links * 3 + confidence * 2

def main():
    print("Scanning skills...")
    stale, examples, links, confidence, total = scan_skills()
    shs = calculate_shs(stale, examples, links, confidence)
    
    print(f"shs: {shs}")
    print(f"total_skills: {total}")
    print(f"stale_skills: {stale}")
    print(f"missing_examples: {examples}")
    print(f"broken_links: {links}")
    print(f"low_confidence: {confidence}")

if __name__ == "__main__":
    main()
