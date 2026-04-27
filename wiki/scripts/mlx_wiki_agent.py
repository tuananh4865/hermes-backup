#!/opt/homebrew/bin/python3.14
"""
MLX Wiki Agent — Autonomous concept page generator

Uses local LLM (MLX) to read raw content and generate wiki concept pages.

Usage:
    python mlx_wiki_agent.py              # Process all unprocessed files
    python mlx_wiki_agent.py --dry-run    # Show what would be processed
    python mlx_wiki_agent.py --model MODEL # Specify model
"""

import argparse
import glob
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# Try to import MLX
try:
    from mlx_lm import generate, load
    MLX_AVAILABLE = True
except ImportError:
    MLX_AVAILABLE = False
    print("Warning: MLX not installed. Run: pip install mlx mlx-lm")

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_PATH = WIKI_PATH / "raw" / "transcripts"
CONCEPTS_PATH = WIKI_PATH / "concepts"
PROCESSED_PATH = WIKI_PATH / ".processed"

DEFAULT_MODEL = "mlx-community/SmolLM2-360M-Instruct"
# Alternative models:
#   "mlx-community/Qwen2.5-0.5B-Instruct"  - Better quality, more memory
#   "mlx-community/Qwen2.5-1.5B-Instruct"  - Best quality, slower

# Prompt template
CONCEPT_PROMPT = """You are a wiki knowledge synthesizer. Read the raw content below and create a comprehensive wiki concept page.

## Raw Content
{content}

## Your Task
Create a markdown file with this exact structure:

```markdown
---
title: "[Concept Title]"
created: {date}
updated: {date}
type: concept
tags: [relevant, tags, from, content]
---

# [Concept Title]

## Summary
2-3 sentences summarizing what this concept is about.

## Key Insights
- First key insight
- Second key insight
- Third key insight

## Analysis
Detailed analysis of the concept, including:
- Background and context
- How it works / what it means
- Why it matters
- Connections to related concepts

## Related
- [[Related Concept 1]]
- [[Related Concept 2]]
- [[Related Concept 3]]
```

Important:
- Use actual wikilinks [[like this]] to related concepts in the wiki
- Add 2-4 relevant tags
- Make analysis thoughtful and substantive (3-5 paragraphs)
- Return ONLY the markdown content, no explanations
"""

# ═══════════════════════════════════════════════════════════════

def ensure_dirs():
    """Ensure required directories exist"""
    PROCESSED_PATH.mkdir(exist_ok=True)
    CONCEPTS_PATH.mkdir(exist_ok=True)

def get_raw_files() -> List[Path]:
    """Get all raw files that haven't been processed"""
    if not RAW_PATH.exists():
        return []
    
    # Get all markdown files in raw/
    raw_files = list(RAW_PATH.rglob("*.md"))
    
    # Filter out already processed
    processed_files = set()
    if PROCESSED_PATH.exists():
        for f in PROCESSED_PATH.glob("*.json"):
            processed_files.add(f.stem)
    
    unprocessed = []
    for f in raw_files:
        # Use relative path as key
        key = str(f.relative_to(RAW_PATH)).replace('/', '_').replace('\\', '_')
        if key not in processed_files:
            unprocessed.append(f)
    
    return unprocessed

def load_model(model_name: str):
    """Load MLX model (cached after first load)"""
    if not MLX_AVAILABLE:
        raise RuntimeError("MLX not available. Install with: pip install mlx mlx-lm")
    
    print(f"Loading model: {model_name}")
    model, tokenizer = load(model_name)
    print("Model loaded ✓")
    return model, tokenizer

def generate_concept(model, tokenizer, raw_content: str, source_name: str) -> str:
    """Generate concept page from raw content"""
    
    # Prepare prompt
    date = datetime.now().strftime('%Y-%m-%d')
    prompt = CONCEPT_PROMPT.format(content=raw_content[:8000], date=date)  # Limit content length
    
    # Generate
    print(f"  Generating concept page...")
    result = generate(
        model, 
        tokenizer,
        prompt=prompt,
        max_tokens=2048,
        temp=0.7
    )
    
    return result

def save_concept(concept_content: str, source_path: Path):
    """Save generated concept to file"""
    
    # Extract title from content
    title_match = re.search(r'^#\s+(.+)$', concept_content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
    else:
        title = source_path.stem
    
    # Sanitize filename
    safe_title = re.sub(r'[<>:"/\\|?*]', '-', title)
    concept_file = CONCEPTS_PATH / f"{safe_title}.md"
    
    # Handle duplicate filenames
    counter = 1
    while concept_file.exists():
        concept_file = CONCEPTS_PATH / f"{safe_title}_{counter}.md"
        counter += 1
    
    # Write file
    concept_file.write_text(concept_content)
    print(f"  Saved: {concept_file.name}")
    
    return concept_file

def mark_processed(source_path: Path):
    """Mark source file as processed"""
    key = str(source_path.relative_to(RAW_PATH)).replace('/', '_').replace('\\', '_')
    processed_file = PROCESSED_PATH / f"{key}.json"
    
    processed_file.write_text(json.dumps({
        'source': str(source_path),
        'processed': datetime.now().isoformat(),
        'concept': key
    }))

def process_files(model_name: str, dry_run: bool = False):
    """Process all unprocessed raw files"""
    ensure_dirs()
    
    raw_files = get_raw_files()
    
    if not raw_files:
        print("No new files to process.")
        return
    
    print(f"Found {len(raw_files)} files to process")
    print()
    
    if dry_run:
        print("DRY RUN — Files that would be processed:")
        for f in raw_files:
            print(f"  • {f}")
        return
    
    # Load model once
    model, tokenizer = load_model(model_name)
    
    # Process each file
    for i, raw_file in enumerate(raw_files, 1):
        print(f"\n[{i}/{len(raw_files)}] Processing: {raw_file.name}")
        
        try:
            # Read raw content
            content = raw_file.read_text()
            
            # Generate concept
            concept = generate_concept(model, tokenizer, content, raw_file.name)
            
            # Save concept
            save_concept(concept, raw_file)
            
            # Mark as processed
            mark_processed(raw_file)
            
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

def main():
    parser = argparse.ArgumentParser(description='MLX Wiki Agent')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='MLX model to use')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of files to process')
    args = parser.parse_args()
    
    print("=" * 70)
    print("MLX WIKI AGENT")
    print("=" * 70)
    print(f"Model: {args.model}")
    print(f"Wiki: {WIKI_PATH}")
    print()
    
    if not MLX_AVAILABLE:
        print("ERROR: MLX not installed")
        print("Run: pip install mlx mlx-lm")
        sys.exit(1)
    
    process_files(args.model, args.dry_run)

if __name__ == "__main__":
    main()
