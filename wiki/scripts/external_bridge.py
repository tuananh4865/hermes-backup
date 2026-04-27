#!/opt/homebrew/bin/python3.14
"""
External Knowledge Bridge — Search web when wiki doesn't have answer

Usage:
    python3 external_bridge.py --query "What is attention?"
    python3 external_bridge.py --query "latest AI news"
"""

import argparse
import json
import subprocess
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
WIKI_SEARCH = WIKI_PATH / "scripts" / "semantic_search.py"

# ═══════════════════════════════════════════════════════════════

def search_wiki(query: str) -> List[Dict]:
    """Search wiki using semantic search"""
    try:
        from scripts.semantic_search import load_index, search
        index = load_index()
        if index:
            results = search(query, top_k=3, index=index)
            return results
    except Exception as e:
        print(f"Wiki search error: {e}")
    return []

def search_web_ddg(query: str) -> List[Dict]:
    """Search using DuckDuckGo HTML (free, no API key)"""
    try:
        url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
        
        results = []
        # Simple HTML parsing for DuckDuckGo results
        import re
        # Find result snippets
        pattern = r'<a class="result__snippet"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        for i, match in enumerate(matches[:5]):
            # Clean HTML
            text = re.sub(r'<[^>]+>', '', match)
            results.append({
                'title': f'Web Result {i+1}',
                'snippet': text.strip()[:200],
                'source': 'duckduckgo'
            })
        
        return results
    except Exception as e:
        print(f"Web search error: {e}")
        return []

def search_web_google(query: str) -> List[Dict]:
    """Search using Google (requires custom search API or scrape)"""
    # Fallback to DuckDuckGo
    return search_web_ddg(query)

def query(question: str, prefer_wiki: bool = True) -> Dict:
    """Query with wiki-first, web fallback"""
    result = {
        'question': question,
        'wiki_results': [],
        'web_results': [],
        'source': 'none',
        'answer': None
    }
    
    # Try wiki first
    if prefer_wiki:
        wiki_results = search_wiki(question)
        if wiki_results:
            result['wiki_results'] = wiki_results
            result['source'] = 'wiki'
            
            # Build answer from wiki
            if wiki_results[0]['score'] > 0.5:
                result['answer'] = f"Found in wiki: {wiki_results[0]['title']}\n\n{wiki_results[0]['chunk'][:300]}..."
                return result
    
    # Fallback to web
    web_results = search_web_ddg(question)
    if web_results:
        result['web_results'] = web_results
        if result['source'] == 'none':
            result['source'] = 'web'
            result['answer'] = f"From web:\n\n{web_results[0]['snippet']}"
    
    return result

def print_result(result: Dict):
    """Print query result"""
    print("=" * 70)
    print(f"QUESTION: {result['question']}")
    print(f"SOURCE: {result['source'].upper()}")
    print("=" * 70)
    
    if result['answer']:
        print(f"\n{result['answer']}")
    
    if result['wiki_results']:
        print(f"\nWiki Results:")
        for r in result['wiki_results'][:3]:
            print(f"  - [{r['score']:.2f}] {r['title']}")
    
    if result['web_results']:
        print(f"\nWeb Results:")
        for r in result['web_results'][:3]:
            print(f"  - {r['snippet'][:100]}...")

def main():
    parser = argparse.ArgumentParser(description='External knowledge bridge')
    parser.add_argument('--query', '-q', help='Question to answer')
    parser.add_argument('--web-only', action='store_true', help='Skip wiki search')
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        return
    
    prefer_wiki = not args.web_only
    result = query(args.query, prefer_wiki=prefer_wiki)
    print_result(result)

if __name__ == '__main__':
    main()
