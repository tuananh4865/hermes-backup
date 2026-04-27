#!/usr/bin/env python3
"""
Test Infrastructure for Wiki Scripts

Run with: pytest tests/ -v
"""

import pytest
import sys
from pathlib import Path

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

WIKI_PATH = Path.home() / "wiki"


class TestWikiLint:
    """Tests for wiki_lint.py"""
    
    def test_extract_wikilinks(self):
        """Test wikilink extraction"""
        from wiki_lint import extract_wikilinks
        
        # Basic wikilinks
        assert extract_wikilinks("See [[wiki]] for details") == ["wiki"]
        assert extract_wikilinks("[[a]] and [[b]]") == ["a", "b"]
        
        # Wikilinks with aliases
        assert extract_wikilinks("[[page|alias]]") == ["page|alias"]
        
        # Skip code blocks
        assert extract_wikilinks("`[[skip]]`") == []
        assert extract_wikilinks("```\n[[skip]]\n```") == []
        
        # Skip raw directories
        from wiki_lint import get_all_md_files
        files = get_all_md_files(WIKI_PATH)
        raw_files = [f for f in files if 'raw' in f.parts]
        assert len(raw_files) == 0, "Should skip raw/ directory"
    
    def test_skip_dirs(self):
        """Test that skip directories are excluded"""
        from wiki_lint import get_all_md_files
        
        files = get_all_md_files(WIKI_PATH)
        
        for f in files:
            assert '_templates' not in f.parts, f"Should skip _templates: {f}"
            assert '.obsidian' not in f.parts, f"Should skip .obsidian: {f}"
            assert '__pycache__' not in f.parts, f"Should skip __pycache__: {f}"
            assert 'raw' not in f.parts, f"Should skip raw/: {f}"
            assert 'transcripts' not in f.parts, f"Should skip transcripts/: {f}"
    
    def test_parse_frontmatter(self):
        """Test frontmatter parsing"""
        from wiki_lint import parse_frontmatter
        
        fm = parse_frontmatter("""---
title: Test
tags: [a, b]
---""")
        assert fm.get('title') == 'Test'
        assert 'a' in fm.get('tags', '')
        
        # No frontmatter should return empty dict
        fm = parse_frontmatter("No frontmatter")
        assert fm.get('title') is None or fm.get('title') == ''
    
    def test_lint_runs(self):
        """Test that wiki_lint runs without error"""
        import subprocess
        
        result = subprocess.run(
            ["python3", str(WIKI_PATH / "scripts" / "wiki_lint.py")],
            capture_output=True,
            timeout=30,
            cwd=str(WIKI_PATH)
        )
        
        assert result.returncode == 0, f"wiki_lint.py failed: {result.stderr}"


class TestSemanticSearch:
    """Tests for semantic_search.py"""
    
    def test_tokenize(self):
        """Test tokenization"""
        from semantic_search import simple_tokenize
        
        tokens = simple_tokenize("Hello World")
        assert "hello" in tokens
        assert "world" in tokens
    
    def test_bm25_score(self):
        """Test BM25 scoring"""
        from semantic_search import get_bm25_score
        
        # Same doc should score higher
        doc = "machine learning is great"
        score1 = get_bm25_score("machine learning", doc)
        score2 = get_bm25_score("cooking recipes", doc)
        
        assert score1 > score2, "Relevant doc should score higher"
    
    def test_chunk_text(self):
        """Test text chunking"""
        from semantic_search import chunk_text
        
        short = "Short text"
        chunks = chunk_text(short)
        assert len(chunks) == 1
        
        long_text = "a" * 1000
        chunks = chunk_text(long_text, chunk_size=200, overlap=50)
        assert len(chunks) > 1


class TestInterestSignalTracker:
    """Tests for interest_signal_tracker.py"""
    
    def test_extract_topics(self):
        """Test topic extraction"""
        from interest_signal_tracker import extract_topics
        
        text = "I want to use lm studio for fine-tune"
        topics = extract_topics(text)
        
        assert "lm-studio" in topics
        assert "fine-tuning" in topics  # maps to fine-tune keyword
    
    def test_load_signals(self):
        """Test signal loading"""
        from interest_signal_tracker import load_signals
        
        signals = load_signals()
        assert isinstance(signals, dict)
        assert 'topic_frequency' in signals


class TestFreshnessScore:
    """Tests for freshness_score.py"""
    
    def test_freshness_runs(self):
        """Test freshness scoring runs"""
        import subprocess
        
        result = subprocess.run(
            ["python3", str(WIKI_PATH / "scripts" / "freshness_score.py")],
            capture_output=True,
            timeout=30,
            cwd=str(WIKI_PATH)
        )
        
        assert result.returncode == 0, f"freshness_score.py failed: {result.stderr}"


class TestDuplicateDetector:
    """Tests for duplicate_detector.py"""
    
    def test_duplicate_runs(self):
        """Test duplicate detection runs"""
        import subprocess
        
        result = subprocess.run(
            ["python3", str(WIKI_PATH / "scripts" / "duplicate_detector.py"), "--find-merges"],
            capture_output=True,
            timeout=30,
            cwd=str(WIKI_PATH)
        )
        
        assert result.returncode == 0, f"duplicate_detector.py failed: {result.stderr}"


class TestContradictionDetector:
    """Tests for contradiction_detector.py"""
    
    def test_contradiction_runs(self):
        """Test contradiction detection runs"""
        import subprocess
        
        result = subprocess.run(
            ["python3", str(WIKI_PATH / "scripts" / "contradiction_detector.py")],
            capture_output=True,
            timeout=30,
            cwd=str(WIKI_PATH)
        )
        
        assert result.returncode == 0, f"contradiction_detector.py failed: {result.stderr}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
