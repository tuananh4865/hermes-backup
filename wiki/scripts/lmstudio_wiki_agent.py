#!/opt/homebrew/bin/python3.14
"""
LM Studio Wiki Agent — Autonomous concept page generator

Uses LM Studio's local OpenAI-compatible API to generate wiki concept pages.
No MLX needed — uses whatever models Anh has loaded in LM Studio.

Usage:
    python lmstudio_wiki_agent.py              # Process all unprocessed files
    python lmstudio_wiki_agent.py --dry-run    # Show what would be processed
    python lmstudio_wiki_agent.py --list        # List available models
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
from typing import Optional, List, Dict

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_PATH = WIKI_PATH / "raw" / "transcripts"
CONCEPTS_PATH = WIKI_PATH / "concepts"
PROCESSED_PATH = WIKI_PATH / ".processed"

# LM Studio API settings
LM_STUDIO_URL = "http://192.168.0.187:1234/v1"
API_KEY = "lm-studio"  # Dummy key for LM Studio

# Default model - MUST match exactly what's shown in LM Studio
# Run: python lmstudio_setup.py to see available models
DEFAULT_MODEL = "google/gemma-4-e2b"

# Prompt template
CONCEPT_PROMPT = """Create a wiki concept page from the raw content below. Follow the structure exactly.

## Raw Content
{content}

## Required Output Structure
```
---
title: "[Exact Concept Title]"
created: {date}
updated: {date}
type: concept
tags: [tag1, tag2, tag3, tag4]
---

# [Concept Title]

## Summary
2-3 sentences.

## Key Insights
- Insight 1
- Insight 2
- Insight 3

## Analysis
Detailed paragraphs.

## Related
- [[existing-wiki-page]]
- [[another-wiki-page]]
```

## Rules
- Output ONLY the markdown. No intro text, no explanation, no "here's the page"
- Use wikilinks [[like-this]] only for pages that exist in the wiki
- Tags: 3-5 relevant tags from content
- Analysis: 2-4 substantive paragraphs
"""

# ═══════════════════════════════════════════════════════════════
# FRONTMATTER VALIDATION
# ═══════════════════════════════════════════════════════════════

REQUIRED_FRONTMATTER = ['title', 'created', 'updated', 'type', 'tags']
VALID_TYPES = ['concept', 'reference', 'personal', 'project']

def validate_frontmatter(content: str) -> tuple[bool, str]:
    """Validate frontmatter has required fields. Returns (is_valid, error_msg)."""
    if not content.strip().startswith('---'):
        return False, "Missing frontmatter opening '---'"
    
    end = content.find('---', 3)
    if end == -1:
        return False, "Missing frontmatter closing '---'"
    
    fm_text = content[3:end]
    
    # Check each required field
    for field in REQUIRED_FRONTMATTER:
        if not re.search(rf'^{field}:', fm_text, re.MULTILINE):
            return False, f"Missing required field: {field}"
    
    # Check type is valid
    type_match = re.search(r'^type:\s*(.+)$', fm_text, re.MULTILINE)
    if type_match:
        type_val = type_match.group(1).strip().strip('"\'')
        if type_val not in VALID_TYPES:
            return False, f"Invalid type '{type_val}'. Must be one of: {VALID_TYPES}"
    
    # Check tags format
    tags_match = re.search(r'^tags:\s*(.+)$', fm_text, re.MULTILINE)
    if tags_match:
        tags_str = tags_match.group(1).strip()
        if not (tags_str.startswith('[') and tags_str.endswith(']')):
            return False, "Tags must be in [tag1, tag2] format"
    
    return True, ""

def extract_frontmatter(content: str) -> dict:
    """Extract frontmatter as dict."""
    if not content.strip().startswith('---'):
        return {}
    end = content.find('---', 3)
    if end == -1:
        return {}
    fm_text = content[3:end]
    fm = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            fm[key.strip()] = value.strip().strip('"\'')
    return fm

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

def list_models() -> List[Dict]:
    """List available models in LM Studio"""
    try:
        response = requests.get(f"{LM_STUDIO_URL}/models", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", [])
        else:
            print(f"Error: {response.status_code}")
            return []
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to LM Studio")
        print("Make sure LM Studio is running with Server enabled")
        print("Go to: LM Studio → Local Server → Start Server")
        return []

def generate_concept(content: str, model: str, max_retries: int = 3) -> str:
    """Generate concept page from raw content using LM Studio with retry logic."""
    
    # Prepare prompt
    date = datetime.now().strftime('%Y-%m-%d')
    prompt = CONCEPT_PROMPT.format(content=content[:8000], date=date)
    
    # Call LM Studio API
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 4096,
        "temperature": 0.7,
        "stream": False
    }
    
    last_error = None
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{LM_STUDIO_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=120  # 2 minute timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            elif response.status_code == 400 and attempt < max_retries - 1:
                # Bad request, retry with lower temperature
                payload["temperature"] = 0.3
                last_error = f"API Error: {response.status_code}, retrying with lower temperature..."
                continue
            else:
                raise Exception(f"API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            last_error = "Cannot connect to LM Studio. Is the server running?"
        except requests.exceptions.Timeout:
            last_error = "Request timed out. Try a smaller model or increase timeout."
        except Exception as e:
            last_error = str(e)
        
        if attempt < max_retries - 1:
            import time
            time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception(f"Failed after {max_retries} attempts. Last error: {last_error}")

def save_concept(concept_content: str, source_path: Path):
    """Save generated concept to file after validating frontmatter."""
    
    # Validate frontmatter first
    is_valid, error_msg = validate_frontmatter(concept_content)
    if not is_valid:
        raise Exception(f"Generated content has invalid frontmatter: {error_msg}")
    
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

def process_files(model: str, dry_run: bool = False):
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
    
    # Process each file
    for i, raw_file in enumerate(raw_files, 1):
        print(f"\n[{i}/{len(raw_files)}] Processing: {raw_file.name}")
        
        try:
            # Read raw content
            content = raw_file.read_text()
            
            # Generate concept
            print(f"  Calling LM Studio ({model})...")
            concept = generate_concept(content, model)
            
            # Save concept
            save_concept(concept, raw_file)
            
            # Mark as processed
            mark_processed(raw_file)
            
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

def main():
    parser = argparse.ArgumentParser(description='LM Studio Wiki Agent')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be processed')
    parser.add_argument('--list', action='store_true', help='List available models in LM Studio')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Model to use (from LM Studio)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of files to process')
    args = parser.parse_args()
    
    print("=" * 70)
    print("LM STUDIO WIKI AGENT")
    print("=" * 70)
    print(f"LM Studio: {LM_STUDIO_URL}")
    print(f"Wiki: {WIKI_PATH}")
    print()
    
    if args.list:
        print("Available models in LM Studio:")
        models = list_models()
        if models:
            for m in models:
                print(f"  • {m.get('id', 'unknown')}")
        else:
            print("  No models found. Make sure LM Studio is running.")
        return
    
    # Check connection
    print("Checking LM Studio connection...")
    models = list_models()
    if not models:
        print("\nERROR: Cannot connect to LM Studio")
        print("\nTo fix:")
        print("1. Open LM Studio")
        print("2. Load a model")
        print("3. Go to 'Local Server' tab (or press Cmd+Shift+L)")
        print("4. Click 'Start Server'")
        print("5. Run this script again")
        sys.exit(1)
    
    print(f"Connected! Found {len(models)} model(s)")
    print()
    
    process_files(args.model, args.dry_run)

if __name__ == "__main__":
    main()
