#!/opt/homebrew/bin/python3.14
"""
Paper Ingest — Parse research papers (arXiv, PDF) into wiki format

Usage:
    python ingest_paper.py --arxiv 2504.12345
    python ingest_paper.py --url "https://arxiv.org/abs/2504.12345"
    python ingest_paper.py --file paper.pdf
    python ingest_paper.py --batch papers/*.pdf
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict
import urllib.request
import urllib.error
import json

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_PAPERS = WIKI_PATH / "raw" / "papers"

# arXiv API
ARXIV_API = "http://export.arxiv.org/api/query"

# ═══════════════════════════════════════════════════════════════

def extract_arxiv_id(url_or_id: str) -> Optional[str]:
    """Extract arXiv ID from URL or string"""
    # Direct ID
    if re.match(r'^\d{4}\.\d{4,5}$', url_or_id):
        return url_or_id
    
    # URL patterns
    patterns = [
        r'arxiv\.org/abs/([\d.]+)',
        r'arxiv\.org/pdf/([\d.]+)',
        r'arxiv\.org/abs/[a-z-]+/([\d.]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None

def fetch_arxiv_metadata(arxiv_id: str) -> Optional[Dict]:
    """Fetch paper metadata from arXiv API"""
    url = f"{ARXIV_API}?id_list={arxiv_id}&max_results=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            xml = response.read().decode('utf-8', errors='ignore')
        
        return parse_arxiv_xml(xml)
    except Exception as e:
        print(f"Error fetching arXiv {arxiv_id}: {e}", file=sys.stderr)
        return None

def parse_arxiv_xml(xml: str) -> Optional[Dict]:
    """Parse arXiv API XML response"""
    try:
        # Extract entry
        entry_match = re.search(r'<entry>([\s\S]*?)</entry>', xml)
        if not entry_match:
            return None
        entry = entry_match.group(1)
        
        # Parse fields
        def extract(tag):
            match = re.search(f'<{tag}[^>]*>([\s\S]*?)</{tag}>', entry)
            return match.group(1).strip() if match else None
        
        title = extract('title')
        summary = extract('summary')
        author_match = re.findall(r'<name>([^<]+)</name>', entry)
        authors = ', '.join(author_match) if author_match else None
        published = extract('published')
        updated = extract('updated')
        primary_category = re.search(r'<arxiv:primary_category[^>]*term="([^"]+)"', entry)
        primary_cat = primary_category.group(1) if primary_category else None
        
        # Get PDF link
        pdf_link = re.search(r'<link[^>]*title="pdf"[^>]*href="([^"]+)"', entry)
        if not pdf_link:
            pdf_link = re.search(r'<link[^>]*href="([^"]*arxiv\.org/pdf[^"]*)"', entry)
        pdf_url = pdf_link.group(1) if pdf_link else None
        
        return {
            'title': title.replace('\n', ' ').strip() if title else None,
            'summary': summary.replace('\n', ' ').strip() if summary else None,
            'authors': authors,
            'published': published[:10] if published else None,
            'updated': updated[:10] if updated else None,
            'category': primary_cat,
            'pdf_url': pdf_url,
            'arxiv_id': re.search(r'<id>([^<]+)</id>', entry).group(1) if re.search(r'<id>([^<]+)</id>', entry) else None,
        }
    except Exception as e:
        print(f"Error parsing arXiv XML: {e}", file=sys.stderr)
        return None

def fetch_pdf_text(pdf_url: str) -> Optional[str]:
    """Fetch PDF and extract text (basic extraction)"""
    try:
        # For arXiv PDFs, try to get abstract from HTML page first
        if 'arxiv.org' in pdf_url:
            abs_url = pdf_url.replace('/pdf/', '/abs/')
            return fetch_arxiv_abstract(abs_url)
        
        # For other PDFs, would need pdfminer or similar
        # For now, return None and rely on metadata
        return None
    except Exception as e:
        print(f"Error fetching PDF: {e}", file=sys.stderr)
        return None

def fetch_arxiv_abstract(abs_url: str) -> Optional[str]:
    """Fetch abstract from arXiv abstract page"""
    try:
        req = urllib.request.Request(abs_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        # Extract abstract
        match = re.search(r'<blockquote class="abstract[^"]*">[^<]*<span[^>]*>([\s\S]*?)</span>', html)
        if match:
            abstract = match.group(1)
            abstract = re.sub(r'<[^>]+>', '', abstract)
            return abstract.strip()
        
        return None
    except Exception:
        return None

def slugify(text: str) -> str:
    """Create URL-safe slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:50]

def save_paper(paper: Dict) -> Path:
    """Save paper to raw/papers/"""
    title = paper.get('title', 'Untitled')
    date = paper.get('published', datetime.now().strftime('%Y-%m-%d'))
    arxiv_id = paper.get('arxiv_id', '').split('/')[-1]
    
    slug = slugify(title)
    filename = f"{date}-{slug}.md"
    
    # Build content
    content_lines = [f"# {title}\n"]
    
    if paper.get('authors'):
        content_lines.append(f"**Authors:** {paper['authors']}\n")
    
    if paper.get('arxiv_id'):
        content_lines.append(f"**arXiv:** [{paper['arxiv_id']}]({paper['arxiv_id']})\n")
    
    if paper.get('category'):
        content_lines.append(f"**Category:** `{paper['category']}`\n")
    
    content_lines.append(f"\n## Abstract\n\n{paper.get('summary', 'No abstract available.')}\n")
    
    if paper.get('pdf_url'):
        content_lines.append(f"\n---\n*PDF: [{paper['pdf_url']}]*\n")
    
    content = ''.join(content_lines)
    
    # Build frontmatter
    tags = [paper.get('category', 'research')] if paper.get('category') else ['research']
    
    frontmatter = f"""---
title: "{title}"
date: {date}
type: paper
tags: [{', '.join(tags)}]
sources: [{paper.get('arxiv_id', '')}]
---

"""
    
    full_content = frontmatter + content
    
    # Ensure directory exists
    RAW_PAPERS.mkdir(parents=True, exist_ok=True)
    
    filepath = RAW_PAPERS / filename
    filepath.write_text(full_content, encoding='utf-8')
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Ingest research papers into wiki')
    parser.add_argument('--arxiv', help='arXiv ID (e.g., 2504.12345)')
    parser.add_argument('--url', help='arXiv URL to ingest')
    parser.add_argument('--file', help='PDF file to parse')
    parser.add_argument('--batch', nargs='+', help='Batch ingest multiple papers')
    parser.add_argument('--list', action='store_true', help='List ingested papers')
    args = parser.parse_args()
    
    if args.list:
        if not RAW_PAPERS.exists():
            print("No papers ingested yet.")
            return
        
        papers = list(RAW_PAPERS.glob("*.md"))
        if not papers:
            print("No papers ingested yet.")
            return
        
        print(f"Ingested papers ({len(papers)}):")
        for paper in sorted(papers, reverse=True):
            print(f"  - {paper.name}")
        return
    
    arxiv_id = None
    
    if args.arxiv:
        arxiv_id = extract_arxiv_id(args.arxiv)
        if not arxiv_id:
            print(f"Invalid arXiv ID: {args.arxiv}")
            sys.exit(1)
    
    elif args.url:
        arxiv_id = extract_arxiv_id(args.url)
        if not arxiv_id:
            print(f"Invalid arXiv URL: {args.url}")
            sys.exit(1)
    
    if arxiv_id:
        print(f"Fetching arXiv paper {arxiv_id}...")
        paper = fetch_arxiv_metadata(arxiv_id)
        if paper:
            filepath = save_paper(paper)
            print(f"Saved to {filepath}")
            if paper.get('title'):
                print(f"Title: {paper['title']}")
            if paper.get('authors'):
                print(f"Authors: {paper['authors']}")
        else:
            print("Failed to fetch paper metadata")
            sys.exit(1)
        return
    
    if args.file:
        print(f"PDF parsing not fully implemented. Use --arxiv or --url for arXiv papers.")
        print(f"File: {args.file}")
        # Would need pdfminer or similar for PDF extraction
        return
    
    if args.batch:
        for item in args.batch:
            if item.endswith('.pdf'):
                print(f"PDF not supported yet: {item}")
            else:
                arxiv_id = extract_arxiv_id(item)
                if arxiv_id:
                    print(f"Fetching {arxiv_id}...")
                    paper = fetch_arxiv_metadata(arxiv_id)
                    if paper:
                        saved = save_paper(paper)
                        print(f"  → {saved.name}")
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
