#!/usr/bin/env python3
"""
MLX Wiki Agent
Automatically generates wiki concept pages from raw content using local LLM.
"""

import os
import glob
import hashlib
import argparse
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple

# Configuration
WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_PATH = WIKI_PATH / "raw"
CONCEPTS_PATH = WIKI_PATH / "concepts"
LOGS_PATH = WIKI_PATH / "logs"
PROCESSED_PATH = WIKI_PATH / ".processed"

# Create directories
for path in [LOGS_PATH, PROCESSED_PATH]:
    path.mkdir(parents=True, exist_ok=True)

@dataclass
class ProcessedFile:
    """Track processed files"""
    path: str
    hash: str
    concept_path: Optional[str]
    timestamp: str

def get_file_hash(filepath: str) -> str:
    """Get MD5 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def is_processed(filepath: str) -> Tuple[bool, Optional[str]]:
    """Check if file was already processed"""
    hash_val = get_file_hash(filepath)
    marker_file = PROCESSED_PATH / f"{hash_val}.txt"
    
    if marker_file.exists():
        with open(marker_file) as f:
            return True, f.read().strip()
    return False, None

def mark_processed(filepath: str, concept_path: str):
    """Mark file as processed"""
    hash_val = get_file_hash(filepath)
    marker_file = PROCESSED_PATH / f"{hash_val}.txt"
    
    with open(marker_file, 'w') as f:
        f.write(concept_path)

def extract_frontmatter(content: str) -> Tuple[dict, str]:
    """Extract YAML frontmatter from markdown"""
    frontmatter = {}
    body = content
    
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2].strip()
            
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, val = line.split(':', 1)
                    frontmatter[key.strip()] = val.strip().strip('"\'')
    
    return frontmatter, body

def sanitize_filename(title: str) -> str:
    """Convert title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '-', safe)
    return safe[:80].lower()

def extract_title(content: str, filepath: str) -> str:
    """Extract title from content or filename"""
    frontmatter, body = extract_frontmatter(content)
    
    if 'title' in frontmatter:
        return frontmatter['title'].strip('"\'')
    
    if 'Title' in frontmatter:
        return frontmatter['Title'].strip('"\'')
    
    # Try to find first H1
    h1_match = re.search(r'^#\s+(.+)$', body, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    # Fall back to filename
    return Path(filepath).stem.replace('-', ' ').title()

def extract_tags(frontmatter: dict, content: str) -> List[str]:
    """Extract tags from frontmatter or content"""
    tags = []
    
    if 'tags' in frontmatter:
        tags_str = frontmatter['tags']
        # Parse [tag1, tag2] format
        tags = re.findall(r'[\w-]+', tags_str)
    
    if 'topics' in frontmatter:
        topics_str = frontmatter['topics']
        tags.extend(re.findall(r'[\w-]+', topics_str))
    
    return list(set(tags))[:10]  # Max 10 tags

def generate_concept_prompt(raw_content: str, title: str, tags: List[str]) -> str:
    """Generate the prompt for concept page creation"""
    
    prompt = f"""You are a knowledge management expert. Analyze the following content and create a comprehensive wiki concept page.

TITLE: {title}
TAGS: {', '.join(tags) if tags else 'General'}

CONTENT:
{raw_content[:8000]}

Create a markdown file with this EXACT structure:

---
title: "{title}"
created: {datetime.now().strftime("%Y-%m-%d")}
updated: {datetime.now().strftime("%Y-%m-%d")}
type: concept
tags: [{', '.join(tags[:5]) if tags else 'general'}]
---

# {title}

## Summary
[2-3 sentence summary of what this is about]

## Key Insights
[5-7 bullet points capturing the most important ideas. Be specific and concrete.]

## Analysis
[Detailed analysis paragraph explaining the significance, context, and implications. Write at least 3-4 sentences.]

## Technical Details
[Any specific technical information, formulas, or implementation details if applicable]

## Related Concepts
[List 3-5 related wiki concepts with [[wikilinks]]]
"""
    return prompt

def call_mlx_llm(model: str, prompt: str, max_tokens: int = 2048, temperature: float = 0.7) -> str:
    """Call MLX LLM for inference"""
    try:
        from mlx_lm import generate, load
        
        # Load model and tokenizer
        model_path, tokenizer = load(model)
        
        # Generate response
        response = generate(
            model_path,
            tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=temperature
        )
        
        return response
    except Exception as e:
        print(f"Error calling LLM: {e}")
        raise

def parse_generated_content(generated: str) -> str:
    """Clean and parse the generated content"""
    # Remove any thinking tags if present
    cleaned = re.sub(r'<think>.*?</think>', '', generated, flags=re.DOTALL)
    
    # Ensure it starts with frontmatter
    if not cleaned.startswith('---'):
        # Find the first --- 
        match = re.search(r'---', generated)
        if match:
            cleaned = generated[match.start():]
    
    return cleaned.strip()

def create_concept_page(title: str, tags: List[str], generated_content: str, source_file: str) -> Path:
    """Create and save the concept page"""
    concept_name = sanitize_filename(title)
    concept_path = CONCEPTS_PATH / f"{concept_name}.md"
    
    # Check if already exists
    if concept_path.exists():
        # Add suffix to avoid collision
        concept_path = CONCEPTS_PATH / f"{concept_name}-{datetime.now().strftime('%H%M%S')}.md"
    
    # Parse and clean content
    content = parse_generated_content(generated_content)
    
    # If parsing failed, create basic structure
    if not content.startswith('---'):
        content = f"""---
title: "{title}"
created: {datetime.now().strftime("%Y-%m-%d")}
updated: {datetime.now().strftime("%Y-%m-%d")}
type: concept
tags: [{', '.join(tags[:5]) if tags else 'general'}]
source: {source_file}
---

# {title}

{content}
"""
    
    # Write file
    with open(concept_path, 'w') as f:
        f.write(content)
    
    return concept_path

def process_file(filepath: str, model: str, max_tokens: int, temperature: float, dry_run: bool = False) -> Optional[Path]:
    """Process a single file"""
    print(f"\n{'='*60}")
    print(f"Processing: {filepath}")
    
    # Read file
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract metadata
    title = extract_title(content, filepath)
    frontmatter, body = extract_frontmatter(content)
    tags = extract_tags(frontmatter, content)
    
    print(f"Title: {title}")
    print(f"Tags: {tags}")
    print(f"Content length: {len(body)} chars")
    
    # Generate concept
    prompt = generate_concept_prompt(body, title, tags)
    
    if dry_run:
        print(f"\n[DRY RUN] Would generate concept for: {title}")
        print(f"Prompt preview: {prompt[:200]}...")
        return None
    
    try:
        generated = call_mlx_llm(model, prompt, max_tokens, temperature)
        
        # Create concept page
        concept_path = create_concept_page(title, tags, generated, filepath)
        
        print(f"\n✓ Created: {concept_path.name}")
        
        # Mark as processed
        mark_processed(filepath, str(concept_path))
        
        return concept_path
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None

def get_raw_files() -> List[str]:
    """Get all raw files that haven't been processed"""
    patterns = [
        RAW_PATH / "**" / "*.md",
        RAW_PATH / "**" / "*.txt",
    ]
    
    files = []
    for pattern in patterns:
        files.extend(glob.glob(str(pattern), recursive=True))
    
    # Filter out processed and concept files
    raw_files = []
    for f in files:
        # Skip if already processed
        processed, _ = is_processed(f)
        if processed:
            continue
        
        # Skip concept pages (they go in concepts/)
        if '/concepts/' in f or '/.processed/' in f:
            continue
        
        raw_files.append(f)
    
    return sorted(raw_files, key=lambda x: os.path.getmtime(x), reverse=True)

def watch_mode(model: str, max_tokens: int, temperature: float):
    """Watch for new files and process them"""
    import time
    
    print(f"Watching {RAW_PATH} for new files...")
    print("Press Ctrl+C to stop")
    
    processed_hashes = set()
    
    while True:
        files = get_raw_files()
        
        for filepath in files:
            hash_val = get_file_hash(filepath)
            
            if hash_val not in processed_hashes:
                result = process_file(filepath, model, max_tokens, temperature)
                if result:
                    processed_hashes.add(hash_val)
        
        time.sleep(60)  # Check every minute

def main():
    parser = argparse.ArgumentParser(description='MLX Wiki Agent')
    parser.add_argument('--model', default='mlx-community/SmolLM2-360M-Instruct',
                        help='Model to use (default: mlx-community/SmolLM2-360M-Instruct)')
    parser.add_argument('--max-tokens', type=int, default=2048,
                        help='Max tokens to generate (default: 2048)')
    parser.add_argument('--temperature', type=float, default=0.7,
                        help='Temperature for generation (default: 0.7)')
    parser.add_argument('--watch', action='store_true',
                        help='Watch for new files continuously')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be processed without processing')
    
    args = parser.parse_args()
    
    print("="*60)
    print("MLX Wiki Agent")
    print("="*60)
    print(f"Model: {args.model}")
    print(f"Raw path: {RAW_PATH}")
    print(f"Concepts path: {CONCEPTS_PATH}")
    print("="*60)
    
    if args.watch:
        watch_mode(args.model, args.max_tokens, args.temperature)
    else:
        # Process all unprocessed files once
        files = get_raw_files()
        
        if not files:
            print("\nNo new files to process")
            return
        
        print(f"\nFound {len(files)} files to process")
        
        results = []
        for filepath in files:
            result = process_file(filepath, args.model, args.max_tokens, args.temperature, args.dry_run)
            results.append((filepath, result))
        
        # Summary
        success = sum(1 for _, r in results if r is not None)
        print(f"\n{'='*60}")
        print(f"Done! Processed {success}/{len(files)} files")
        
        # Auto-commit if configured
        if success > 0 and not args.dry_run:
            print("\nCommitting to git...")
            os.system(f'cd {WIKI_PATH} && git add concepts/ raw/')
            os.system(f'cd {WIKI_PATH} && git commit -m "Wiki Agent: Auto-generated {success} concept pages"')
            os.system(f'cd {WIKI_PATH} && git push')
            print("Committed!")

if __name__ == "__main__":
    main()
