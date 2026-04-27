#!/opt/homebrew/bin/python3.14
"""
Generate Q&A Training Data from Wiki Content

Uses LM Studio to generate question-answer pairs from wiki concept pages.
Output: JSONL file for fine-tuning.

Usage:
    python generate_training_data.py              # Generate all
    python generate_training_data.py --limit 5   # Test with 5 pages
"""

import argparse
import glob
import json
import os
import re
import sys
import requests
from datetime import datetime
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CONCEPTS_PATH = WIKI_PATH / "concepts"
OUTPUT_FILE = WIKI_PATH / "training_data" / "train.jsonl"

LM_STUDIO_URL = "http://192.168.0.187:1234/v1"
MODEL = "google/gemma-4-e2b"

MAX_CONTENT_CHARS = 4000  # Limit content sent to model
MAX_TOKENS = 1500         # Max tokens for Q&A generation

# ═══════════════════════════════════════════════════════════════

QA_PROMPT = """Based on the following wiki content, generate 3 question-answer pairs that test understanding of key concepts.

CONTENT TITLE: {title}
CONTENT:
{content}

Generate Q&A pairs in this exact format (no other text):
Q1: [Clear question about a key concept]
A1: [Accurate answer based on the content]

Q2: [Question about another important concept]
A2: [Clear, accurate answer]

Q3: [Question about a third concept]
A3: [Informative answer]
"""

def extract_content(filepath: Path) -> tuple[str, str]:
    """Extract title and main content from markdown file."""
    content = filepath.read_text()
    frontmatter = ""
    
    # Extract frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            content = parts[2]
    
    # Get title from frontmatter or first H1
    title_match = re.search(r'^title:\s*"(.+)"', frontmatter, re.MULTILINE)
    if title_match:
        title = title_match.group(1)
    else:
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = h1_match.group(1) if h1_match else filepath.stem
    
    # Clean markdown
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Links
    content = re.sub(r'#+ ', '', content)  # Headers
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*([^*]+)\*', r'\1', content)  # Italic
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Code blocks
    content = re.sub(r'[=-]{3,}', '', content)  # Separators
    content = re.sub(r'\n{3,}', '\n\n', content)  # Multiple newlines
    
    return title, content.strip()

def generate_qa_pairs(title: str, content: str) -> list[dict]:
    """Generate Q&A pairs using LM Studio API."""
    
    prompt = QA_PROMPT.format(title=title, content=content[:MAX_CONTENT_CHARS])
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer ***"
    }
    
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": 0.7,
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{LM_STUDIO_URL}/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code != 200:
            print(f"    API Error: {response.status_code}")
            return []
        
        result = response.json()
        output = result["choices"][0]["message"]["content"]
        
        # Parse Q&A pairs
        pairs = []
        q_pattern = r'Q(\d+):\s*(.+)'
        a_pattern = r'A(\d+):\s*(.+)'
        
        questions = dict(re.findall(q_pattern, output))
        answers = dict(re.findall(a_pattern, output))
        
        for q_num, question in questions.items():
            if q_num in answers:
                pairs.append({
                    "messages": [
                        {"role": "user", "content": question.strip()},
                        {"role": "assistant", "content": answers[q_num].strip()}
                    ]
                })
        
        return pairs
    
    except Exception as e:
        print(f"    Error: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Generate Q&A training data from wiki')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of files to process')
    parser.add_argument('--reset', action='store_true', help='Reset output file')
    args = parser.parse_args()
    
    print(f"Wiki Training Data Generator")
    print(f"={'='*50}")
    print(f"Wiki: {WIKI_PATH}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    
    # Get concept files
    concept_files = sorted(CONCEPTS_PATH.glob("*.md"))
    if args.limit:
        concept_files = concept_files[:args.limit]
    
    print(f"Found {len(concept_files)} concept files")
    print()
    
    # Reset output if requested
    if args.reset and OUTPUT_FILE.exists():
        OUTPUT_FILE.unlink()
    
    # Process each file
    total_pairs = 0
    for i, filepath in enumerate(concept_files, 1):
        title, content = extract_content(filepath)
        
        if len(content) < 100:
            print(f"[{i}/{len(concept_files)}] Skip (too short): {filepath.stem}")
            continue
        
        print(f"[{i}/{len(concept_files)}] Processing: {title}")
        
        pairs = generate_qa_pairs(title, content)
        
        if pairs:
            # Append to JSONL
            with open(OUTPUT_FILE, 'a') as f:
                for pair in pairs:
                    f.write(json.dumps(pair) + '\n')
            
            print(f"    + {len(pairs)} Q&A pairs")
            total_pairs += len(pairs)
        else:
            print(f"    No pairs generated")
    
    print()
    print(f"={'='*50}")
    print(f"Done! Generated {total_pairs} Q&A pairs")
    print(f"Output: {OUTPUT_FILE}")
    
    if OUTPUT_FILE.exists():
        size_kb = OUTPUT_FILE.stat().st_size / 1024
        print(f"File size: {size_kb:.1f} KB")

if __name__ == "__main__":
    main()
