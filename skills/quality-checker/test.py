#!/usr/bin/env python3
"""
Quality Checker — Test Script
Verify skill hoạt động đúng bằng cách chạy vài test cases.

Usage:
    python3 test.py
"""
import sys
import os
import json
from datetime import datetime, timezone, timedelta

sys.path.insert(0, "/Users/tuananh4865/.hermes/loop-engineering")
from log_helper import log_qa

TZ_VN = timezone(timedelta(hours=7))


def check_format(output: str) -> dict:
    """Check format quality."""
    score = 10
    issues = []
    
    if not output:
        return {"score": 0, "issues": [{"severity": "critical", "description": "Empty output"}]}
    
    # Check markdown basics
    if "```" in output and not any(f"```{lang}" for lang in ["python", "yaml", "json", "bash", "markdown"]):
        score -= 1
        issues.append({"category": "format", "severity": "minor", 
                       "description": "Code block không có language tag"})
    
    # Check headings
    if "#" in output:
        lines_with_hash = [l for l in output.split("\n") if l.startswith("#")]
        for h in lines_with_hash:
            if not h.startswith("# "):
                score -= 1
                issues.append({"category": "format", "severity": "minor",
                              "description": f"Heading malformed: {h[:30]}"})
                break
    
    return {"score": max(0, score), "issues": issues}


def check_voice(output: str, project: str = "general") -> dict:
    """Check voice quality."""
    score = 10
    issues = []
    
    # Banned patterns per project
    banned = {
        "content-creator": [
            "mấy con vợ", "mấy đứa", "mấy chị", "mấy má",
            "quất một phát", "đỉnh nóc kịch trần"
        ],
        "general": [],
    }
    
    patterns = banned.get(project, [])
    for pattern in patterns:
        count = output.lower().count(pattern.lower())
        if count > 0:
            score -= 2 * count
            issues.append({
                "category": "voice",
                "severity": "critical",
                "description": f"Dùng '{pattern}' {count} lần (cấm trong {project})",
                "suggestion": f"Sửa thành 'các bạn' (content-creator) hoặc bỏ"
            })
    
    return {"score": max(0, score), "issues": issues}


def check_sources(output: str) -> dict:
    """Check sources (URLs)."""
    score = 10
    issues = []
    
    urls = []
    for line in output.split("\n"):
        if "http://" in line or "https://" in line:
            # Extract URL
            import re
            found = re.findall(r'https?://[^\s\)]+', line)
            urls.extend(found)
    
    n_urls = len(urls)
    
    if n_urls == 0:
        # Check if it's a research task
        if any(kw in output.lower() for kw in ["research", "tìm hiểu", "phân tích"]):
            score = 0
            issues.append({
                "category": "sources",
                "severity": "critical",
                "description": "Research output không có URL nguồn"
            })
    elif n_urls < 5 and any(kw in output.lower() for kw in ["research", "tìm hiểu"]):
        score = max(0, n_urls * 2)
        issues.append({
            "category": "sources",
            "severity": "warning",
            "description": f"Chỉ có {n_urls} URLs, cần ≥5 cho research"
        })
    
    return {"score": score, "issues": issues, "n_urls": n_urls}


def check_quality(output: str) -> dict:
    """Check quality bar (no chung chung, no tự đoán)."""
    score = 10
    issues = []
    
    banned_phrases = [
        ("có thể là", "chung chung"),
        ("thường thì", "chung chung"),
        ("nhiều khi", "chung chung"),
        ("khá nhiều", "chung chung"),
        ("khá tốt", "chung chung"),
        ("em nghĩ là", "tự đoán (trong facts)"),
    ]
    
    for phrase, issue_type in banned_phrases:
        count = output.lower().count(phrase)
        if count > 0:
            score -= count
            issues.append({
                "category": "quality",
                "severity": "warning" if count == 1 else "critical",
                "description": f"Dùng '{phrase}' {count} lần — {issue_type}"
            })
    
    return {"score": max(0, score), "issues": issues}


def run_checker(output: str, project: str = "general", task_type: str = "content") -> dict:
    """Run full checker pipeline."""
    
    format_result = check_format(output)
    voice_result = check_voice(output, project)
    sources_result = check_sources(output)
    quality_result = check_quality(output)
    
    # Simple weighted average
    weights = {"format": 0.10, "voice": 0.15, "sources": 0.25, "quality": 0.25,
               "project_specific": 0.15, "actionability": 0.10}
    
    scores = {
        "format": format_result["score"],
        "voice": voice_result["score"],
        "sources": sources_result["score"],
        "quality": quality_result["score"],
        "project_specific": 10,  # assumed OK
        "actionability": 10,    # assumed OK
    }
    
    final_score = sum(scores[k] * weights[k] for k in weights)
    
    # All issues
    all_issues = (format_result["issues"] + voice_result["issues"] +
                  sources_result["issues"] + quality_result["issues"])
    
    # Verdict — score-based + critical-issue override
    has_critical = any(i.get("severity") == "critical" for i in all_issues)
    
    if has_critical:
        # Bất kỳ critical issue = FAIL
        verdict = "FAIL"
    elif final_score >= 9.0:
        verdict = "PASS"
    elif final_score >= 7.0:
        verdict = "WARN"
    elif final_score >= 5.0:
        verdict = "FAIL"
    else:
        verdict = "FAIL"
    
    return {
        "verdict": verdict,
        "score": round(final_score, 1),
        "scores": scores,
        "issues": all_issues,
        "timestamp": datetime.now(TZ_VN).isoformat(),
        "task_type": task_type,
        "project": project,
    }


# === Test cases ===
if __name__ == "__main__":
    print("🧪 Quality Checker — Test Suite\n")
    print("=" * 60)
    
    # Test 1: GOOD content
    test_good = """# Top 5 sản phẩm trending
    
Đây là research về top 5 sản phẩm TikTok Shop trending hôm nay.
    
## Sản phẩm #1
- Giá: 299k
- Đã bán: 1,500 units
- Nguồn: [TikTok Shop product page](https://example.com) - 2026-06-16
"""
    result1 = run_checker(test_good, project="content-creator", task_type="research")
    print(f"\n✅ Test 1 (GOOD content): {result1['verdict']} (score: {result1['score']})")
    
    # Test 2: BAD content - uses "mấy con vợ" 
    test_bad = """# Script TikTok

Mấy con vợ ơi, hôm nay em review sản phẩm này cho mấy con vợ xem.
Thường thì mấy con vợ sẽ thích sản phẩm có giá khoảng 200k.
"""
    result2 = run_checker(test_bad, project="content-creator", task_type="script")
    print(f"\n❌ Test 2 (BAD voice): {result2['verdict']} (score: {result2['score']})")
    print(f"   Issues: {len(result2['issues'])}")
    for issue in result2['issues'][:3]:
        print(f"   - {issue['description']}")
    
    # Test 3: Research without sources
    test_no_sources = """# Research về trending topics

Theo em nghĩ thì sản phẩm này khá tốt. Có thể là do thiết kế đẹp.
Thường thì mọi người sẽ thích. Khá nhiều người đã mua."""
    result3 = run_checker(test_no_sources, project="content-creator", task_type="research")
    print(f"\n❌ Test 3 (NO sources, chung chung): {result3['verdict']} (score: {result3['score']})")
    print(f"   Issues: {len(result3['issues'])}")
    for issue in result3['issues'][:3]:
        print(f"   - {issue['description']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary:")
    print(f"   Test 1: {result1['verdict']} (expected: PASS or WARN)")
    print(f"   Test 2: {result2['verdict']} (expected: FAIL)")
    print(f"   Test 3: {result3['verdict']} (expected: FAIL)")
    
    all_pass = (
        result1['verdict'] in ['PASS', 'WARN'] and
        result2['verdict'] == 'FAIL' and
        result3['verdict'] == 'FAIL'
    )
    
    if all_pass:
        print("\n✅ All tests passed!")
        log_qa("PASS", "Quality checker test suite — 3/3 cases verdicts match expectations", step_num=1)
        sys.exit(0)
    else:
        print("\n❌ Some tests failed")
        log_qa("FAIL", f"Quality checker test suite — unexpected verdicts: 1={result1['verdict']} 2={result2['verdict']} 3={result3['verdict']}", step_num=1)
        sys.exit(1)