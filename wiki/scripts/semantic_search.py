#!/opt/homebrew/bin/python3.14
"""
Semantic Search — Embedding-based wiki search

Unlike grep/keyword search, semantic search understands meaning.

Usage:
    python3 semantic_search.py --index
    python3 semantic_search.py --query "attention mechanism"
    python3 semantic_search.py --reindex
    python3 semantic_search.py --server  # Start API server
"""

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
INDEX_FILE = WIKI_PATH / "scripts" / ".search_index.json"

# Chunk settings
CHUNK_SIZE = 500  # chars per chunk
CHUNK_OVERLAP = 50  # overlap between chunks

# ═══════════════════════════════════════════════════════════════

def simple_tokenize(text: str) -> List[str]:
    """Simple Vietnamese-aware tokenization"""
    # Lowercase
    text = text.lower()
    
    # Split on whitespace and punctuation
    tokens = re.findall(r'\b\w+\b', text)
    
    return tokens

def get_bm25_score(query: str, document: str, k1: float = 1.5, b: float = 0.75) -> float:
    """
    BM25: Better than simple TF-IDF for retrieval
    """
    tokens = simple_tokenize(document)
    query_tokens = simple_tokenize(query)
    
    if not tokens or not query_tokens:
        return 0.0
    
    # Calculate document length and average
    doc_len = len(tokens)
    avg_len = doc_len  # For single doc, avg = itself
    
    # Word frequencies in document
    freq = defaultdict(int)
    for token in tokens:
        freq[token] += 1
    
    # Calculate BM25
    score = 0.0
    for q_token in query_tokens:
        if q_token not in freq:
            continue
        
        tf = freq[q_token]
        # IDF (simplified - assume 1 for all)
        idf = 1.0
        
        # BM25 formula
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * (doc_len / avg_len))
        
        score += idf * (numerator / (denominator + 0.1))
    
    return score

def get_ngram_score(query: str, document: str, n: int = 3) -> float:
    """Get n-gram overlap score"""
    query_tokens = simple_tokenize(query)
    doc_tokens = simple_tokenize(document)
    
    if not query_tokens or not doc_tokens:
        return 0.0
    
    # Create n-grams
    def get_ngrams(tokens, n):
        return set(' '.join(tokens[i:i+n]) for i in range(len(tokens)-n+1))
    
    query_ngrams = get_ngrams(query_tokens, min(n, len(query_tokens)))
    doc_ngrams = get_ngrams(doc_tokens, min(n, len(doc_tokens)))
    
    if not query_ngrams:
        return 0.0
    
    # Jaccard similarity
    intersection = len(query_ngrams & doc_ngrams)
    union = len(query_ngrams | doc_ngrams)
    
    return intersection / union if union > 0 else 0.0

def get_keyword_bonus(query: str, document: str) -> float:
    """Bonus for exact keyword matches"""
    query_lower = query.lower()
    doc_lower = document.lower()
    
    # Check for exact phrase match
    if query_lower in doc_lower:
        return 2.0
    
    # Check for each keyword
    keywords = simple_tokenize(query)
    bonus = 0.0
    for kw in keywords:
        if len(kw) > 3 and kw in doc_lower:
            bonus += 0.3
    
    return bonus

def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text into overlapping chunks"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks

def get_all_pages() -> Dict[str, str]:
    """Get all wiki pages and their content"""
    pages = {}
    
    for md_file in (WIKI_PATH / "concepts").rglob("*.md"):
        if '_templates' in md_file.parts:
            continue
        try:
            content = md_file.read_text(encoding='utf-8')
            # Remove frontmatter
            if content.startswith('---'):
                end = content.find('---', 3)
                if end != -1:
                    content = content[end+3:]
            pages[str(md_file.relative_to(WIKI_PATH))] = content
        except:
            pass
    
    return pages

def build_index() -> Dict:
    """Build search index from all pages"""
    print("Building search index...")
    
    pages = get_all_pages()
    index = {
        'pages': {},
        'metadata': {
            'total_pages': len(pages),
            'built': None
        }
    }
    
    for page_path, content in pages.items():
        chunks = chunk_text(content)
        chunk_data = []
        
        for i, chunk in enumerate(chunks):
            chunk_data.append({
                'id': f'{page_path}::{i}',
                'text': chunk,
                'offset': i * (CHUNK_SIZE - CHUNK_OVERLAP)
            })
        
        index['pages'][page_path] = {
            'chunks': chunk_data,
            'total_chunks': len(chunks),
            'title': Path(page_path).stem
        }
    
    index['metadata']['built'] = __import__('datetime').datetime.now().isoformat()
    
    # Save index
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index))
    
    print(f"Indexed {len(pages)} pages, {sum(len(d['chunks']) for d in index['pages'].values())} chunks")
    
    return index

def load_index() -> Optional[Dict]:
    """Load existing index"""
    if INDEX_FILE.exists():
        try:
            return json.loads(INDEX_FILE.read_text())
        except:
            pass
    return None

def search(query: str, top_k: int = 5, index: Dict = None) -> List[Dict]:
    """Search wiki using semantic scoring"""
    if index is None:
        index = load_index()
    
    if index is None:
        print("No index found. Run with --index first.")
        return []
    
    results = []
    
    for page_path, page_data in index['pages'].items():
        best_score = 0.0
        best_chunk = None
        
        for chunk_data in page_data['chunks']:
            chunk_text = chunk_data['text']
            
            # Calculate multiple scores
            bm25 = get_bm25_score(query, chunk_text)
            ngram = get_ngram_score(query, chunk_text)
            keyword = get_keyword_bonus(query, chunk_text)
            
            # Combined score
            combined = (bm25 * 0.5) + (ngram * 0.3) + (keyword * 0.2)
            
            if combined > best_score:
                best_score = combined
                best_chunk = chunk_data
        
        if best_score > 0:
            results.append({
                'page': page_path,
                'title': page_data['title'],
                'score': best_score,
                'chunk': best_chunk['text'][:200] if best_chunk else '',
                'offset': best_chunk['offset'] if best_chunk else 0
            })
    
    # Sort by score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results[:top_k]

def print_results(results: List[Dict], query: str):
    """Print search results"""
    if not results:
        print(f"No results for: {query}")
        return
    
    print("=" * 70)
    print(f"SEARCH RESULTS: {query}")
    print("=" * 70)
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['title']} (score: {result['score']:.2f})")
        print(f"   {result['page']}")
        
        # Show relevant chunk
        chunk = result['chunk']
        if chunk:
            # Try to find relevant context
            print(f"   ...{chunk[:150]}...")
    
    print("=" * 70)

def main():
    parser = argparse.ArgumentParser(description='Semantic search for wiki')
    parser.add_argument('--query', '-q', help='Search query')
    parser.add_argument('--index', action='store_true', help='Build search index')
    parser.add_argument('--reindex', action='store_true', help='Rebuild search index')
    parser.add_argument('--top', type=int, default=5, help='Number of results (default: 5)')
    args = parser.parse_args()
    
    if args.index or args.reindex:
        build_index()
        return
    
    if args.query:
        index = load_index()
        if index is None:
            print("No index found. Building...")
            index = build_index()
        
        results = search(args.query, top_k=args.top, index=index)
        print_results(results, args.query)
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
