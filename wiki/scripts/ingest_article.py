#!/opt/homebrew/bin/python3.14
"""
Article Ingest — Parse web articles into wiki format

Usage:
    python ingest_article.py --url "https://example.com/article"
    python ingest_article.py --file article.html
    python ingest_article.py --batch articles/*.html
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import urllib.request
import urllib.error

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_ARTICLES = WIKI_PATH / "raw" / "articles"

# Fields to extract
EXTRACT_FIELDS = ['title', 'author', 'date', 'content', 'url']

# ═══════════════════════════════════════════════════════════════

def extract_title(html: str) -> Optional[str]:
    """Extract article title"""
    # Try og:title first
    match = re.search(r'<meta property="og:title" content="([^"]+)"', html)
    if match:
        return match.group(1)
    
    # Try <title>
    match = re.search(r'<title>([^<]+)</title>', html)
    if match:
        return match.group(1).strip()
    
    return None

def extract_author(html: str) -> Optional[str]:
    """Extract author"""
    patterns = [
        r'<meta name="author" content="([^"]+)"',
        r'<span class="author">([^<]+)</span>',
        r'By ([A-Z][a-z]+ [A-Z][a-z]+)',
        r'author:\s*([^<\n]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1).strip()
    return None

def extract_date(html: str) -> Optional[str]:
    """Extract publication date"""
    patterns = [
        r'<meta property="article:published_time" content="([^"]+)"',
        r'<time[^>]*datetime="([^"]+)"',
        r'(\d{4}-\d{2}-\d{2})',
    ]
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            return match.group(1)[:10]  # YYYY-MM-DD
    return None

def extract_content(html: str) -> str:
    """Extract main content, removing ads/nav/comments"""
    # Remove script/style tags
    html = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', html)
    html = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', html)
    
    # Remove nav/header/footer
    html = re.sub(r'<nav[^>]*>[\s\S]*?</nav>', '', html)
    html = re.sub(r'<header[^>]*>[\s\S]*?</header>', '', html)
    html = re.sub(r'<footer[^>]*>[\s\S]*?</footer>', '', html)
    
    # Remove comments
    html = re.sub(r'<!--[\s\S]*?-->', '', html)
    
    # Try to find main content area
    main_patterns = [
        r'<article[^>]*>([\s\S]*?)</article>',
        r'<main[^>]*>([\s\S]*?)</main>',
        r'<div class="content">([\s\S]*?)</div>',
        r'<div class="post">([\s\S]*?)</div>',
    ]
    for pattern in main_patterns:
        match = re.search(pattern, html)
        if match:
            html = match.group(1)
            break
    
    # Convert to markdown
    content = html_to_markdown(html)
    
    # Clean up
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    return content

def html_to_markdown(html: str) -> str:
    """Simple HTML to markdown conversion"""
    # Headings
    html = re.sub(r'<h1[^>]*>([^<]+)</h1>', r'# \1\n', html)
    html = re.sub(r'<h2[^>]*>([^<]+)</h2>', r'## \1\n', html)
    html = re.sub(r'<h3[^>]*>([^<]+)</h3>', r'### \1\n', html)
    html = re.sub(r'<h4[^>]*>([^<]+)</h4>', r'#### \1\n', html)
    
    # Bold/italic
    html = re.sub(r'<strong[^>]*>([^<]+)</strong>', r'**\1**', html)
    html = re.sub(r'<b[^>]*>([^<]+)</b>', r'**\1**', html)
    html = re.sub(r'<em[^>]*>([^<]+)</em>', r'*\1*', html)
    html = re.sub(r'<i[^>]*>([^<]+)</i>', r'*\1*', html)
    
    # Links
    html = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', r'[\2](\1)', html)
    
    # Lists
    html = re.sub(r'<li[^>]*>([^<]+)</li>', r'- \1\n', html)
    html = re.sub(r'<ul[^>]*>', '\n', html)
    html = re.sub(r'</ul>', '\n', html)
    html = re.sub(r'<ol[^>]*>', '\n', html)
    html = re.sub(r'</ol>', '\n', html)
    
    # Paragraphs
    html = re.sub(r'<p[^>]*>', '\n\n', html)
    html = re.sub(r'</p>', '', html)
    
    # Line breaks
    html = re.sub(r'<br[^>]*>', '\n', html)
    
    # Remove remaining tags
    html = re.sub(r'<[^>]+>', '', html)
    
    # Decode HTML entities
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&quot;', '"')
    html = html.replace('&#39;', "'")
    
    return html

def slugify(text: str) -> str:
    """Create URL-safe slug"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:50]

def fetch_url(url: str) -> Optional[str]:
    """Fetch HTML from URL"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except urllib.error.URLError as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None

def parse_article(url: str, html: str = None) -> Dict:
    """Parse article from URL or HTML"""
    if html is None:
        html = fetch_url(url)
        if html is None:
            return None
    
    return {
        'title': extract_title(html),
        'author': extract_author(html),
        'date': extract_date(html) or datetime.now().strftime('%Y-%m-%d'),
        'content': extract_content(html),
        'url': url,
    }

def save_article(article: Dict) -> Path:
    """Save article to raw/articles/"""
    title = article.get('title', 'Untitled')
    date = article.get('date', datetime.now().strftime('%Y-%m-%d'))
    slug = slugify(title)
    
    filename = f"{date}-{slug}.md"
    
    # Build frontmatter
    frontmatter = f"""---
title: "{title}"
date: {date}
type: article
tags: []
sources: [{article['url']}]
---

"""
    
    content = f"# {title}\n\n"
    if article.get('author'):
        content += f"*By {article['author']}*\n\n"
    content += article.get('content', '')
    
    # Add source link at bottom
    content += f"\n\n---\n*Source: [{article['url']}]*"
    
    full_content = frontmatter + content
    
    # Ensure directory exists
    RAW_ARTICLES.mkdir(parents=True, exist_ok=True)
    
    filepath = RAW_ARTICLES / filename
    filepath.write_text(full_content, encoding='utf-8')
    
    return filepath

def main():
    parser = argparse.ArgumentParser(description='Ingest web articles into wiki')
    parser.add_argument('--url', help='Article URL to ingest')
    parser.add_argument('--file', help='HTML file to parse')
    parser.add_argument('--batch', nargs='+', help='Batch ingest multiple HTML files')
    parser.add_argument('--list', action='store_true', help='List ingested articles')
    args = parser.parse_args()
    
    if args.list:
        # List existing articles
        if not RAW_ARTICLES.exists():
            print("No articles ingested yet.")
            return
        
        articles = list(RAW_ARTICLES.glob("*.md"))
        if not articles:
            print("No articles ingested yet.")
            return
        
        print(f"Ingested articles ({len(articles)}):")
        for article in sorted(articles, reverse=True):
            print(f"  - {article.name}")
        return
    
    if args.url:
        print(f"Ingesting {args.url}...")
        article = parse_article(args.url)
        if article:
            filepath = save_article(article)
            print(f"Saved to {filepath}")
        else:
            print("Failed to parse article")
            sys.exit(1)
        return
    
    if args.file:
        print(f"Ingesting {args.file}...")
        html = Path(args.file).read_text(encoding='utf-8', errors='ignore')
        article = parse_article(args.file, html)
        if article:
            filepath = save_article(article)
            print(f"Saved to {filepath}")
        return
    
    if args.batch:
        for filepath in args.batch:
            print(f"Ingesting {filepath}...")
            try:
                html = Path(filepath).read_text(encoding='utf-8', errors='ignore')
                article = parse_article(filepath, html)
                if article:
                    saved = save_article(article)
                    print(f"  → {saved.name}")
            except Exception as e:
                print(f"  → Error: {e}")
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
