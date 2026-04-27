#!/opt/homebrew/bin/python3.14
"""
Deep Research Script v3 — 7 rounds × 5 queries + last30days social round
With multi-source bypass (ddgs → Searx → Brave → Tavily) + last30days social trends
"""

import json
import os
import sys
import subprocess
import time
import random
from datetime import datetime
from pathlib import Path
from collections import Counter

# Load .env manually (no dotenv dependency)
import re as _re
_env_file = os.path.expanduser('~/.hermes/.env')
if os.path.exists(_env_file):
    for _line in open(_env_file):
        _line = _line.strip()
        if '=' in _line and not _line.startswith('#'):
            _k, _v = _line.split('=', 1)
            os.environ[_k.strip()] = _v.strip()

# Config
WIKI_DIR = Path("/Volumes/Storage-1/Hermes/wiki")
CRON_DIR = Path.home() / ".hermes" / "cron"
KEYWORDS_FILE = CRON_DIR / "agent_keywords.json"
STATE_FILE = CRON_DIR / "research_state.json"
LAST30DAYS_SCRIPT = Path.home() / ".claude" / "skills" / "last30days" / "scripts" / "last30days.py"

# User agents for rotation (helps bypass bot detection)
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]

# Base queries (will be expanded with dynamic keywords)
BASE_QUERIES = {
    "Round 1 - Core Trends": [
        "AI agents 2026 latest",
        "agentic AI breakthrough 2026",
        "self-improving autonomous agents",
        "multi-agent systems tutorial",
        "LLM agent trends"
    ],
    "Round 2 - Apple Silicon & Local": [
        "Apple Silicon MLX LLM agents",
        "local LLM model MacBook",
        "MLX models Apple Silicon",
        "llama.cpp Mac performance",
        "local AI agent Apple M-chip"
    ],
    "Round 3 - Frameworks & Tools": [
        "LangGraph multi-agent tutorial",
        "CrewAI agent systems",
        "MCP Model Context Protocol servers",
        "Claude Code agent skills",
        "OpenAI Agents SDK",
        "n8n AI workflow automation"
    ],
    "Round 4 - Developer & Building": [
        "vibe coding AI tools",
        "solo developer AI agent workflow",
        "build AI startup one person",
        "agentic workflow automation",
        "affiliate marketing AI tools"
    ],
    "Round 5 - Business & Money": [
        "make money with AI agents 2026",
        "one person billion dollar AI company",
        "AI agent business case study",
        "AI startup success stories 2026",
        "AI SaaS business model"
    ],
    "Round 6 - Technical Deep Dive": [
        "agent memory architecture RAG",
        "agent planning reasoning LLM",
        "tool calling function calling agents",
        "multi-agent collaboration architecture",
        "agent orchestrator framework"
    ],
    "Round 7 - Research & Papers": [
        "arXiv AI agents paper 2026",
        "Hugging Face local agent models",
        "open source AI agent frameworks",
        "new LLM releases Apple Silicon",
        "agent development GitHub trending"
    ]
}


def get_random_ua():
    return random.choice(USER_AGENTS)


def load_keywords():
    """Load keyword database"""
    if KEYWORDS_FILE.exists():
        with open(KEYWORDS_FILE) as f:
            return json.load(f)
    return {
        "trending": [],
        "frameworks": [],
        "tools": [],
        "last_updated": None
    }


def save_keywords(kw):
    """Save keyword database"""
    kw["last_updated"] = datetime.now().isoformat()
    CRON_DIR.mkdir(parents=True, exist_ok=True)
    with open(KEYWORDS_FILE, "w") as f:
        json.dump(kw, f, indent=2)


def extract_keywords_from_results(results):
    """Extract new keywords from search results"""
    new_trending = []
    new_frameworks = []
    new_tools = []

    framework_names = [
        "LangGraph", "CrewAI", "AutoGen", "Flowise", "n8n", "LlamaIndex",
        "Hayashi", "MCP", "OpenAI Agents SDK", "Anthropic", "LangChain",
        "AutoGPT", "BabyAGI", "MetaGPT", "ChatDev"
    ]

    tool_names = [
        "MCP server", "RAG", "vector database", "tool calling",
        "function calling", "ReAct", "chain-of-thought"
    ]

    import re
    for r in results:
        content = r.get("content", "").lower()
        title = r.get("title", "").lower()
        text = content + " " + title

        for fw in framework_names:
            if fw.lower() in text and fw not in new_frameworks:
                new_frameworks.append(fw)

        for tool in tool_names:
            if tool.lower() in text and tool not in new_tools:
                new_tools.append(tool)

        caps = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', r.get("title", ""))
        for cap in caps[:3]:
            if len(cap) > 4 and cap not in new_trending:
                new_trending.append(cap)

    return new_trending, new_frameworks, new_tools


def web_search(query, limit=15):
    """
    Execute web search with multi-source bypass.
    Priority: ddgs (python3.14) → duckduckgo_search (python3.9) → Searx → Brave → Tavily

    Returns {"results": [...]} or {"results": []} on failure.
    """
    errors = []

    # --- Source 1: ddgs with python3.14 (SSL fix) ---
    python14_bins = ["python3.14", "python3.13"]
    for pybin in python14_bins:
        try:
            result = subprocess.run(
                [pybin, "-c", f"""
from ddgs import DDGS
import sys
results = []
with DDGS() as d:
    r = list(d.text({repr(query)}, max_results={limit}))
    for item in r:
        results.append({{
            "title": item.get("title", ""),
            "url": item.get("href", ""),
            "content": item.get("body", "")[:300]
        }})
print(len(results))
sys.exit(0 if results else 1)
"""],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode == 0:
                # Re-run to get actual results
                out = subprocess.run(
                    [pybin, "-c", f"""
from ddgs import DDGS
import json
results = []
with DDGS() as d:
    r = list(d.text({repr(query)}, max_results={limit}))
    for item in r:
        results.append({{
            "title": item.get("title", ""),
            "url": item.get("href", ""),
            "content": item.get("body", "")[:300]
        }})
print(json.dumps(results))
"""],
                    capture_output=True, text=True, timeout=30
                )
                if out.stdout.strip():
                    try:
                        results = json.loads(out.stdout.strip())
                        if results:
                            return {"results": results, "source": f"ddgs/{pybin}"}
                    except json.JSONDecodeError:
                        pass
        except Exception:
            continue

    # --- Source 2: duckduckgo_search (python3.9, older) ---
    try:
        from duckduckgo_search import DDGS as _DDGS
        results = []
        with _DDGS() as d:
            r = list(d.text(query, max_results=limit))
            for item in r:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("href", ""),
                    "content": item.get("body", "")[:300]
                })
        if results:
            return {"results": results, "source": "duckduckgo_search"}
    except ImportError:
        errors.append("duckduckgo_search not installed")
    except Exception as e:
        errors.append(f"duckduckgo_search: {e}")

    # --- Source 3: Searx (privacy metasearch, rarely blocks) ---
    searx_instances = [
        "https://searx.space",
        "https://searxng.site",
    ]
    for instance in searx_instances:
        try:
            import urllib.parse, urllib.request
            encoded_q = urllib.parse.quote(query)
            url = f"{instance}/search?q={encoded_q}&format=json&engines=duckduckgo,google&limit={limit}"
            req = urllib.request.Request(
                url,
                headers={"User-Agent": get_random_ua()},
                timeout=20
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode())
                results = []
                for item in data.get("results", [])[:limit]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "content": item.get("content", "")[:300]
                    })
                if results:
                    return {"results": results, "source": f"searx ({instance})"}
        except Exception:
            continue

    # --- Source 4: Brave Search (free tier: 2,000 queries/month) ---
    brave_key = os.environ.get("BRAVE_API_KEY", "")
    if brave_key:
        try:
            import urllib.parse, urllib.request
            encoded_q = urllib.parse.quote(query)
            url = f"https://api.search.brave.com/res/v1/web/search?q={encoded_q}&count={limit}"
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": get_random_ua(),
                    "Accept": "application/json",
                    "X-Subscription-Token": brave_key
                },
                timeout=20
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode())
                results = []
                for item in data.get("web", {}).get("results", {}).get("results", [])[:limit]:
                    results.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "content": item.get("description", "")[:300]
                    })
                if results:
                    return {"results": results, "source": "brave"}
        except Exception as e:
            errors.append(f"brave: {e}")

    # --- Source 5: Tavily (paid, best quality when available) ---
    tavily_key = os.environ.get("TAVILY_API_KEY", "")
    if tavily_key:
        try:
            import requests
            resp = requests.post('https://api.tavily.com/search', json={
                'api_key': tavily_key,
                'query': query,
                'max_results': limit,
                'search_depth': 'basic'
            }, timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                results = [{
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "content": r.get("content", "")[:300]
                } for r in data.get("results", [])]
                if results:
                    return {"results": results, "source": "tavily"}
            else:
                errors.append(f"tavily {resp.status_code}")
        except Exception as e:
            errors.append(f"tavily: {e}")

    # All sources failed
    if errors:
        print(f"  [Search failed for '{query}': {'; '.join(errors[:3])}]", file=sys.stderr)
    return {"results": [], "source": "none"}


def run_last30days(query):
    """
    Run last30days for a query using Python 3.14+.
    Saves raw output to CRON_DIR/last30days_output/ and returns structured summary.
    """
    if not LAST30DAYS_SCRIPT.exists():
        return {"results": [], "source": "last30days (script not found)", "raw_output": ""}

    # Find python3.14+
    python_bins = ["python3.14", "python3.13", "python3.12"]
    python_cmd = None
    for py in python_bins:
        try:
            result = subprocess.run([py, "--version"], capture_output=True, timeout=5)
            if result.returncode == 0:
                python_cmd = py
                break
        except Exception:
            continue

    if not python_cmd:
        return {"results": [], "source": "last30days (no python3.12+)", "raw_output": ""}

    # Create output dir
    output_dir = CRON_DIR / "last30days_output"
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Run last30days with --agent for non-interactive compact output
        cmd = [
            python_cmd, str(LAST30DAYS_SCRIPT),
            query,
            "--emit", "compact",
            "--quick",
            "--save-dir", str(output_dir),
            "--save-suffix", "dr",
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=180
        )

        raw_output = result.stdout + (result.stderr if result.stderr else "")

        if result.returncode != 0 and not raw_output:
            return {"results": [], "source": f"last30days failed ({result.returncode})", "raw_output": ""}

        # Parse clusters from compact output
        results = []
        lines = raw_output.split('\n')
        current_cluster = None

        for line in lines:
            line = line.rstrip()
            # Cluster header: "### N. Cluster title (score N, M items, sources: X, Reddit)"
            if line.startswith('### '):
                import re
                # Extract cluster title and score
                match = re.match(r'### \d+\. (.+?) \(score (\d+)', line)
                if match:
                    current_cluster = {
                        "title": match.group(1),
                        "score": int(match.group(2)),
                        "items": []
                    }
                continue

            # Item line: "1. [reddit] Title"
            if line.startswith('1. [') or line.startswith('2. [') or line.startswith('3. ['):
                if current_cluster is None:
                    continue
                # Extract source and title
                import re
                item_match = re.match(r'\d+\. \[([^\]]+)\] (.+)', line)
                if item_match:
                    source = item_match.group(1)
                    title = item_match.group(2).strip()
                    # Extract URL from same line
                    url_match = re.search(r'https?://[^\s\)\]]+', line)
                    url = url_match.group(0) if url_match else ""
                    # Extract metadata: date, upvotes, etc
                    meta_match = re.search(r'(\d{4}-\d{2}-\d{2}) \| ([^|]+) \| \[([^\]]+)\]', line)
                    meta = {}
                    if meta_match:
                        meta = {"date": meta_match.group(1), "sub": meta_match.group(2).strip(), "engagement": meta_match.group(3)}
                    current_cluster["items"].append({
                        "title": title,
                        "url": url,
                        "source": source,
                        "meta": meta
                    })
                continue

            # End of cluster
            if current_cluster and line.startswith('### ') or (current_cluster and line.startswith('## ') and not line.startswith('## Ranked')):
                if current_cluster["items"]:
                    for item in current_cluster["items"]:
                        results.append({
                            "title": f"[{item['source']}] {item['title']}",
                            "url": item['url'],
                            "content": f"Cluster: {current_cluster['title']} (score:{current_cluster['score']}) | {item.get('meta', {}).get('engagement', '')}",
                            "social_source": item['source']
                        })
                current_cluster = None

        # Don't forget last cluster
        if current_cluster and current_cluster["items"]:
            for item in current_cluster["items"]:
                results.append({
                    "title": f"[{item['source']}] {item['title']}",
                    "url": item['url'],
                    "content": f"Cluster: {current_cluster['title']} (score:{current_cluster['score']}) | {item.get('meta', {}).get('engagement', '')}",
                    "social_source": item['source']
                })

        return {
            "results": results,
            "source": "last30days",
            "raw_output": raw_output[:2000]  # First 2k chars for summary
        }

    except subprocess.TimeoutExpired:
        return {"results": [], "source": "last30days (timeout)", "raw_output": ""}
    except Exception as e:
        return {"results": [], "source": f"last30days error: {e}", "raw_output": ""}


def get_all_queries():
    """Get all queries, expanded with trending keywords"""
    keywords = load_keywords()
    queries = []

    for round_name, round_queries in BASE_QUERIES.items():
        if keywords.get("trending") and "Round 1" in round_name:
            if keywords["trending"]:
                flat = [k[0] if isinstance(k, list) else k for k in keywords["trending"]]
                for kw in flat[:2]:
                    round_queries = round_queries + [f"{kw} AI agents"]

        queries.append({
            "round": round_name,
            "queries": round_queries
        })

    # Round 8: Social Trends via last30days
    # Key social topics from Tuấn Anh's interests
    social_queries = [
        "AI agents vibe coding solo developer",
        "Claude Code vs Cursor AI tools",
        "Apple Silicon MLX local LLM",
        "one person AI startup success",
        "agentic workflow automation tools",
    ]
    queries.append({
        "round": "Round 8 - Social Trends (last30days)",
        "queries": social_queries
    })

    return queries


def run_research_round(round_name, queries, use_last30days=False):
    """Run one research round. Returns (all_results, raw_outputs_dict)"""
    print(f"\n{'='*60}")
    print(f"{round_name}")
    print('='*60)

    all_results = []
    raw_outputs = {}  # query -> raw_output for last30days

    for query in queries:
        print(f"  Searching: {query}")

        if use_last30days:
            result = run_last30days(query)
            raw_out = result.get("raw_output", "")
            if raw_out:
                raw_outputs[query] = raw_out
            if result.get("results"):
                for r in result["results"]:
                    r["query"] = query
                    r["round"] = round_name
                    r["search_source"] = result.get("source", "last30days")
                all_results.extend(result["results"])
                print(f"    last30days: got {len(result['results'])} items")
            else:
                print(f"    last30days: no results ({result.get('source', 'unknown')})")
                # Fallback to regular search
                results = web_search(query)
                if results.get("results"):
                    for r in results["results"]:
                        r["query"] = query
                        r["round"] = round_name
                        r["search_source"] = results.get("source", "unknown")
                    all_results.extend(results["results"])
                    print(f"    fallback ({results.get('source', '?')}): {len(results['results'])} items")
        else:
            results = web_search(query)
            if results.get("results"):
                for r in results["results"]:
                    r["query"] = query
                    r["round"] = round_name
                    r["search_source"] = results.get("source", "unknown")
                all_results.extend(results["results"])
                print(f"    ({results.get('source', '?')}): {len(results['results'])} items")
            else:
                print(f"    no results from any source")

        time.sleep(0.5)

    return all_results, raw_outputs


def generate_report(all_results, last30days_raw=None):
    """Generate comprehensive research report"""
    keywords = load_keywords()

    # Extract and update keywords
    new_trending, new_frameworks, new_tools = extract_keywords_from_results(all_results)

    if new_trending:
        existing = keywords.get("trending", [])
        flat_existing = [k[0] if isinstance(k, list) else k for k in existing]
        keywords["trending"] = list((Counter(flat_existing + new_trending)).most_common(20))

    if new_frameworks:
        existing = keywords.get("frameworks", [])
        flat_existing = [k[0] if isinstance(k, list) else k for k in existing]
        keywords["frameworks"] = list((Counter(flat_existing + new_frameworks)).most_common(15))

    if new_tools:
        existing = keywords.get("tools", [])
        flat_existing = [k[0] if isinstance(k, list) else k for k in existing]
        keywords["tools"] = list((Counter(flat_existing + new_tools)).most_common(15))

    save_keywords(keywords)

    # Sort by credibility
    credibility_order = {
        "arxiv.org": 95,
        "github.com": 85,
        "huggingface.co": 85,
        "stackoverflow.com": 70,
        "medium.com": 65,
        "reddit.com": 55,
        "news.ycombinator.com": 55,
        "twitter.com": 40,
        "x.com": 40
    }

    def get_credibility(url):
        for domain, score in credibility_order.items():
            if domain in url.lower():
                return score
        return 50

    sorted_results = sorted(all_results, key=lambda x: get_credibility(x.get("url", "")), reverse=True)

    # Remove duplicates by URL
    seen = set()
    unique_results = []
    for r in sorted_results:
        url = r.get("url", "")
        if url and url not in seen:
            seen.add(url)
            unique_results.append(r)

    # Separate social results (from last30days)
    social_results = [r for r in all_results if r.get("search_source") == "last30days" or r.get("social_source")]
    web_results = [r for r in unique_results if r.get("search_source") != "last30days" and not r.get("social_source")]

    today = datetime.now().strftime("%Y-%m-%d")

    report = f"""# AI Agent Trends — {today}

> Auto-generated report | {len(unique_results)} web sources | {len(social_results)} social posts | {len(all_results)} total findings

## Executive Summary

"""

    # Group web results by round
    by_round = {}
    for r in all_results:
        if r.get("social_source"):
            continue  # Skip social in web section
        round_name = r.get("round", "Unknown")
        if round_name not in by_round:
            by_round[round_name] = []
        by_round[round_name].append(r)

    for round_name, results in by_round.items():
        if round_name == "Round 8 - Social Trends (last30days)":
            continue
        report += f"\n### {round_name}\n\n"
        for r in results[:5]:
            title = r.get("title", "Untitled")
            url = r.get("url", "")
            content = r.get("content", "")[:150]
            source = r.get("search_source", "")
            report += f"- [{title}]({url})\n"
            if content:
                report += f"  > {content}...\n"
            if source:
                report += f"  _(via {source})_\n"
        report += "\n"

    # Social trends section
    if social_results or last30days_raw:
        report += "\n## Social Trends (Reddit, X, HN, TikTok — last30days)\n\n"

        # Add raw last30days output for full fidelity
        if last30days_raw:
            for query, raw in last30days_raw.items():
                report += f"\n### {query}\n\n"
                # Include the ranked evidence clusters section
                lines = raw.split('\n')
                in_clusters = False
                for line in lines:
                    if '## Ranked Evidence Clusters' in line:
                        in_clusters = True
                    if in_clusters and line.strip():
                        report += f"{line}\n"
                    if in_clusters and line.startswith('## ') and '## Ranked' not in line:
                        break
                report += "\n"

        # Structured items from parsing
        by_social = {}
        for r in social_results:
            src = r.get("social_source", "other")
            if src not in by_social:
                by_social[src] = []
            by_social[src].append(r)

        for src, items in by_social.items():
            report += f"\n### {src.upper()} ({len(items)} posts)\n\n"
            for r in items[:5]:
                title = r.get("title", "Untitled")
                url = r.get("url", "")
                content = r.get("content", "")[:150]
                if url:
                    report += f"- [{title}]({url})"
                else:
                    report += f"- {title}"
                if content:
                    report += f"\n  > {content}..."
                report += "\n"
            report += "\n"

    report += "\n## Trending Keywords Detected\n\n"
    if new_trending:
        report += f"**New trending:** {', '.join(new_trending[:10])}\n\n"
    if new_frameworks:
        report += f"**Frameworks:** {', '.join(new_frameworks)}\n\n"
    if new_tools:
        report += f"**Tools:** {', '.join(new_tools)}\n\n"

    report += "\n## Top Sources (by credibility)\n\n"
    for i, r in enumerate(web_results[:30], 1):
        title = r.get("title", "Untitled")
        url = r.get("url", "")
        score = get_credibility(url)
        src = r.get("search_source", "")
        report += f"{i}. [{title}]({url}) (credibility: {score})"
        if src:
            report += f" — via {src}"
        report += "\n"

    report += f"""

---

*Report generated: {datetime.now().isoformat()}*
*Keyword database updated: {KEYWORDS_FILE}*
"""

    return report


def main():
    print("="*60)
    print("DEEP RESEARCH v3 — AI Agent Trends")
    print("(ddgs → Searx → Brave → Tavily + last30days social)")
    print("="*60)

    # Get queries
    all_query_sets = get_all_queries()

    all_results = []
    all_raw_outputs = {}

    # Run all rounds
    for query_set in all_query_sets:
        use_last30days = "Round 8" in query_set["round"]
        round_results, raw_outputs = run_research_round(
            query_set["round"], query_set["queries"], use_last30days=use_last30days
        )
        all_results.extend(round_results)
        all_raw_outputs.update(raw_outputs)

    # Generate report
    report = generate_report(all_results, last30days_raw=all_raw_outputs if all_raw_outputs else None)

    # Save report
    today = datetime.now().strftime("%Y-%m-%d")
    report_file = WIKI_DIR / "concepts" / f"ai-agent-trends-{today}.md"

    with open(report_file, "w") as f:
        f.write(report)

    print(f"\n{'='*60}")
    print(f"Report saved: {report_file}")
    print(f"Total results: {len(all_results)}")
    print(f"Unique sources: {len(set(r.get('url','') for r in all_results if r.get('url')))}")
    print("="*60)


if __name__ == "__main__":
    main()
