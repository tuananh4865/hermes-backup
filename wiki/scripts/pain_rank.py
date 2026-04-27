#!/opt/homebrew/bin/python3.14
"""
Pain Rank Script — Rank insights by business value

Usage:
    python3 scripts/pain_rank.py --insights "insight1|insight2|insight3"
    python3 scripts/pain_rank.py --input outputs/research/latest.md
    python3 scripts/pain_rank.py --daily  # Rank from today's research
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Ranking criteria weights
WEIGHTS = {
    "frequency": 0.3,      # How often this pain point appears
    "urgency": 0.25,       # How time-sensitive
    "business_value": 0.25, # Impact on goals
    "prevalence": 0.2       # How many sources mention it
}

# Keywords for scoring
URGENCY_KEYWORDS = [
    "critical", "urgent", "asap", "immediately", "breaking",
    "security", "vulnerability", "breach", "outage", "down"
]

BUSINESS_VALUE_KEYWORDS = [
    "revenue", "cost", "saving", "efficiency", "productivity",
    "user", "customer", "growth", "scale", "automate"
]

FREQUENCY_PATTERNS = [
    r"\b(multiple|many|various)\b",
    r"\b(consistently|repeatedly|often)\b",
    r"\b(frequently|recurring)\b"
]


def score_frequency(text: str) -> float:
    """Score based on frequency indicators"""
    score = 0.0
    text_lower = text.lower()
    
    # Direct frequency mentions
    if re.search(r"\b\d+\s*(times|sources|articles|papers)\b", text_lower):
        match = re.search(r"(\d+)\s*(times|sources|articles|papers)", text_lower)
        if match:
            count = int(match.group(1))
            score = min(count / 10, 1.0)  # Cap at 1.0
    
    # Pattern-based frequency
    for pattern in FREQUENCY_PATTERNS:
        if re.search(pattern, text_lower):
            score += 0.3
    
    return min(score, 1.0)


def score_urgency(text: str) -> float:
    """Score based on urgency indicators"""
    text_lower = text.lower()
    score = 0.0
    
    for keyword in URGENCY_KEYWORDS:
        if keyword in text_lower:
            score += 0.25
    
    # Check for deadline indicators
    if re.search(r"\b(deadline|by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)|end of|expires?\b)", text_lower):
        score += 0.3
    
    return min(score, 1.0)


def score_business_value(text: str) -> float:
    """Score based on business value indicators"""
    text_lower = text.lower()
    score = 0.0
    
    for keyword in BUSINESS_VALUE_KEYWORDS:
        if keyword in text_lower:
            score += 0.15
    
    # Impact quantifiers
    if re.search(r"\b(significant|substantial|major|drastic)\b", text_lower):
        score += 0.2
    
    return min(score, 1.0)


def score_prevalence(sources: List[str]) -> float:
    """Score based on number of unique sources"""
    unique_sources = len(set(sources))
    return min(unique_sources / 10, 1.0)  # Cap at 10 sources


def rank_pain_points(insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Rank insights by pain score"""
    ranked = []
    
    for insight in insights:
        text = insight.get("description", "") + " " + insight.get("title", "")
        sources = insight.get("sources", [])
        
        frequency = score_frequency(text)
        urgency = score_urgency(text)
        business_value = score_business_value(text)
        prevalence = score_prevalence(sources)
        
        total_score = (
            WEIGHTS["frequency"] * frequency +
            WEIGHTS["urgency"] * urgency +
            WEIGHTS["business_value"] * business_value +
            WEIGHTS["prevalence"] * prevalence
        )
        
        ranked.append({
            "title": insight.get("title", "Untitled"),
            "description": insight.get("description", ""),
            "category": insight.get("category", "general"),
            "sources_count": len(sources),
            "scores": {
                "frequency": round(frequency, 2),
                "urgency": round(urgency, 2),
                "business_value": round(business_value, 2),
                "prevalence": round(prevalence, 2)
            },
            "total_score": round(total_score, 3),
            "sources": sources[:5]  # Top 5 sources
        })
    
    # Sort by total score descending
    ranked.sort(key=lambda x: x["total_score"], reverse=True)
    
    return ranked


def generate_report(ranked: List[Dict], date: str) -> str:
    """Generate markdown report"""
    report = f"""# Pain Point Rankings — {date}

## Summary
- **Total Pain Points:** {len(ranked)}
- **High Priority (score > 0.7):** {len([p for p in ranked if p['total_score'] > 0.7])}
- **Medium Priority (0.4-0.7):** {len([p for p in ranked if 0.4 <= p['total_score'] <= 0.7])}
- **Low Priority (< 0.4):** {len([p for p in ranked if p['total_score'] < 0.4])}

---

## Rankings

"""
    
    for i, pain in enumerate(ranked, 1):
        emoji = "🔴" if pain['total_score'] > 0.7 else "🟡" if pain['total_score'] > 0.4 else "🟢"
        
        report += f"""### {i}. {emoji} {pain['title']}
**Score:** {pain['total_score']} | **Category:** {pain['category']} | **Sources:** {pain['sources_count']}

{pain['description']}

**Scores:** freq={pain['scores']['frequency']} | urgency={pain['scores']['urgency']} | biz_value={pain['scores']['business_value']} | prevalence={pain['scores']['prevalence']}

---
"""
    
    report += f"""
## Methodology

| Weight | Factor | Description |
|--------|--------|-------------|
| {WEIGHTS['frequency']:.0%} | Frequency | How often this pain point appears |
| {WEIGHTS['urgency']:.0%} | Urgency | Time-sensitive indicators |
| {WEIGHTS['business_value']:.0%} | Business Value | Impact indicators |
| {WEIGHTS['prevalence']:.0%} | Prevalence | Number of unique sources |

*Generated at {datetime.now().isoformat()}*
"""
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Rank pain points by business value")
    parser.add_argument("--insights", help="Pipe-separated list of insights")
    parser.add_argument("--input", help="Input file with insights JSON")
    parser.add_argument("--daily", action="store_true", help="Read from today's research")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--limit", type=int, default=10, help="Top N results")
    args = parser.parse_args()
    
    insights = []
    date = datetime.now().strftime("%Y-%m-%d")
    
    if args.insights:
        # Parse pipe-separated format: "title|description|category"
        for line in args.insights.split("|"):
            parts = line.split("|")
            insights.append({
                "title": parts[0].strip() if len(parts) > 0 else "Untitled",
                "description": parts[1].strip() if len(parts) > 1 else "",
                "category": parts[2].strip() if len(parts) > 2 else "general"
            })
    
    elif args.input:
        input_path = Path(args.input)
        if input_path.exists():
            data = json.loads(input_path.read_text())
            if isinstance(data, list):
                insights = data
            elif isinstance(data, dict):
                insights = data.get("insights", [data])
    
    elif args.daily:
        # Read from today's research output
        research_dir = Path("~/wiki/outputs/research").expanduser()
        today_file = research_dir / f"{date}.md"
        
        if today_file.exists():
            content = today_file.read_text()
            # Extract insights from markdown (simple parsing)
            insights = extract_insights_from_markdown(content)
    
    if not insights:
        print("No insights to rank. Use --insights, --input, or --daily")
        return
    
    ranked = rank_pain_points(insights)
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        report = generate_report(ranked[:args.limit], date)
        output_path.write_text(report)
        print(f"Report saved to {output_path}")
    else:
        # Print top N
        print(generate_report(ranked[:args.limit], date))


def extract_insights_from_markdown(content: str) -> List[Dict]:
    """Simple markdown insight extraction"""
    insights = []
    
    # Look for bullet points with insights
    for line in content.split("\n"):
        if line.strip().startswith("- ") or line.strip().startswith("* "):
            text = line.strip()[2:]
            # Try to extract title
            if ":" in text:
                title = text.split(":")[0].strip()
                desc = ":".join(text.split(":")[1:]).strip()
            else:
                title = text[:50]
                desc = text
            
            insights.append({
                "title": title,
                "description": desc,
                "category": "research"
            })
    
    return insights


if __name__ == "__main__":
    main()
