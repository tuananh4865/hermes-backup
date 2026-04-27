#!/opt/homebrew/bin/python3.14
"""
Add confidence tags to wiki pages

Usage:
    python3 scripts/add_confidence_tags.py --page wiki/concepts/agentic-ai.md
    python3 scripts/add_confidence_tags.py --all  # Add to all wiki pages
    python3 scripts/add_confidence_tags.py --check  # Check current status
"""

import argparse
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def extract_relationships(content: str) -> List[Dict[str, str]]:
    """Extract wiki links and infer relationship type"""
    relationships = []
    
    # Match [[wikilinks]]
    wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
    
    for link in wikilinks:
        link_lower = link.lower()
        
        # Determine confidence based on context
        confidence = "extracted"  # Default
        
        # Check if it's a direct mention vs contextual reference
        if re.search(rf'\[\[[^\]]*{re.escape(link)}[^\]]*\]\]', content):
            # Direct link, likely extracted
            confidence = "extracted"
        
        # Check for inference indicators
        inference_keywords = ["might be", "possibly", "related to", "similar to", "like"]
        for keyword in inference_keywords:
            if keyword in content.lower():
                confidence = "inferred"
                break
        
        # Check for ambiguity indicators
        if any(word in content.lower() for word in ["unclear", "uncertain", "ambiguous", "might", "could be"]):
            confidence = "ambiguous"
        
        relationships.append({
            "to": link.strip(),
            "type": "related",
            "confidence": confidence
        })
    
    return relationships


def get_current_frontmatter(content: str) -> tuple[Optional[Dict], str]:
    """Extract existing frontmatter"""
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    
    if frontmatter_match:
        fm_text = frontmatter_match.group(1)
        fm = {}
        for line in fm_text.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                fm[key.strip()] = value.strip()
        return fm, content[frontmatter_match.end():]
    
    return None, content


def add_confidence_frontmatter(content: str, page_path: str) -> str:
    """Add or update confidence frontmatter"""
    
    relationships = extract_relationships(content)
    
    if not relationships:
        return content
    
    # Parse existing frontmatter
    fm_match = re.match(r'^(---\n.*?\n---\n)', content, re.DOTALL)
    
    new_fm = {
        'confidence': 'medium',
        'last_verified': datetime.now().strftime('%Y-%m-%d'),
        'relationships': relationships,
        'relationship_count': len(relationships)
    }
    
    # Calculate overall confidence
    conf_scores = {'extracted': 1.0, 'inferred': 0.6, 'ambiguous': 0.3}
    avg_conf = sum(conf_scores.get(r['confidence'], 0.5) for r in relationships) / len(relationships)
    
    if avg_conf >= 0.8:
        new_fm['confidence'] = 'high'
    elif avg_conf >= 0.5:
        new_fm['confidence'] = 'medium'
    else:
        new_fm['confidence'] = 'low'
    
    # Build frontmatter string
    fm_lines = ['---']
    for key, value in new_fm.items():
        if key == 'relationships':
            fm_lines.append(f'{key}:')
            for rel in value:
                conf_emoji = '🔗' if rel['confidence'] == 'extracted' else '🔍' if rel['confidence'] == 'inferred' else '❓'
                fm_lines.append(f"  - {conf_emoji} {rel['to']} ({rel['confidence']})")
        else:
            fm_lines.append(f'{key}: {value}')
    fm_lines.append('---')
    fm_string = '\n'.join(fm_lines) + '\n'
    
    if fm_match:
        # Replace existing frontmatter
        return content.replace(fm_match.group(1), fm_string)
    else:
        # Add new frontmatter at top
        return fm_string + content


def process_page(page_path: Path) -> Dict:
    """Process a single wiki page"""
    if not page_path.exists():
        return {"status": "error", "message": "File not found"}
    
    content = page_path.read_text()
    original = content
    
    # Skip if already has confidence frontmatter
    if re.search(r'^---\n.*confidence:', content, re.MULTILINE | re.DOTALL):
        return {"status": "skipped", "message": "Already has confidence"}
    
    # Check for wiki links
    wikilinks = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
    
    if not wikilinks:
        return {"status": "skipped", "message": "No wiki links found"}
    
    # Add confidence tags
    content = add_confidence_frontmatter(content, str(page_path))
    
    if content != original:
        page_path.write_text(content)
        return {
            "status": "updated",
            "message": f"Added confidence to {len(wikilinks)} links",
            "links": wikilinks
        }
    
    return {"status": "no_change"}


def main():
    parser = argparse.ArgumentParser(description="Add confidence tags to wiki pages")
    parser.add_argument("--page", help="Process single page")
    parser.add_argument("--all", action="store_true", help="Process all wiki pages")
    parser.add_argument("--check", action="store_true", help="Check current status")
    parser.add_argument("--dir", default="wiki", help="Wiki directory")
    args = parser.parse_args()
    
    wiki_dir = Path(args.dir)
    
    if args.check:
        # Check status of all pages
        pages = list(wiki_dir.rglob("*.md"))
        has_confidence = 0
        has_wikilinks = 0
        total_links = 0
        
        for page in pages:
            content = page.read_text()
            if re.search(r'^---\n.*confidence:', content, re.MULTILINE | re.DOTALL):
                has_confidence += 1
                continue
            
            links = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)
            if links:
                has_wikilinks += 1
                total_links += len(links)
        
        print(f"""Wiki Confidence Status:
- Total pages: {len(pages)}
- With confidence tags: {has_confidence}
- With wiki links (no confidence): {has_wikilinks}
- Total wiki links: {total_links}
""")
        return
    
    if args.page:
        result = process_page(Path(args.page))
        print(f"{result['status']}: {result['message']}")
        if 'links' in result:
            print(f"  Links: {', '.join(result['links'])}")
    
    elif args.all:
        pages = list(wiki_dir.rglob("*.md"))
        updated = 0
        skipped = 0
        errors = 0
        
        for page in pages:
            result = process_page(page)
            if result['status'] == 'updated':
                print(f"✓ {page}: {result['message']}")
                updated += 1
            elif result['status'] == 'skipped':
                skipped += 1
            else:
                print(f"✗ {page}: {result.get('message')}")
                errors += 1
        
        print(f"\nSummary: {updated} updated, {skipped} skipped, {errors} errors")


if __name__ == "__main__":
    main()
