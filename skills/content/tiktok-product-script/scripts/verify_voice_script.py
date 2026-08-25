#!/usr/bin/env python3
"""
verify_voice_script.py - 8-bài-học văn nói checklist cho TikTok script.

Run sau khi viết xong script (TRƯỚC khi generate voice):

    python3 scripts/verify_voice_script.py <script-file.md>

Pass tất cả 8 check → mới generate voice. Fail bất kỳ check nào → fix script trước.

Bài học gốc: wiki/concepts/tiktok-script-natural-voice-2026-07-21.md (v0.10.0).
Verified case: ULANZI MA66 V4A/B/C (21/07, pass all 8 checks).
"""

import sys
import re
from pathlib import Path


# Sentence-final particles (Bắc dialect - anh Tuấn Anh style)
PARTICLES = ['đấy', 'nhá', 'nhé', 'nhỉ', 'ấy', 'thôi', 'luôn']

# Forbidden words (Kapwing research - polished tone fail)
FORBIDDEN = ['toàn bộ', 'mọi người', 'đặc biệt', 'vô cùng', 'rất nhiều']

# Formal openers (must NOT start script with these)
FORMAL_OPENERS = ['Xin chào', 'Có ai', 'Hôm nay mình', 'Chào mọi người', 'Hello các bạn']

# Số từ tiếng Việt (heuristic - script cần nhiều từ Việt để tự nhiên)
MIN_VIETNAMESE_CHARS = 0.6  # ≥60% ký tự là tiếng Việt có dấu


def extract_keep_blocks(content: str) -> str:
    """Extract text inside KEEP blocks (script content, skip checklist/notes)."""
    keep_blocks = re.findall(r'\*\*KEEP[^"]*\|\s*"([^"]+)"', content, re.DOTALL)
    if keep_blocks:
        return ' '.join(keep_blocks)
    # Fallback: extract all > *<text>* blockquotes
    blockquotes = re.findall(r'^>\s*\*?(.+?)\*?\s*$', content, re.MULTILINE)
    return ' '.join(blockquotes)


def extract_script_text(content: str) -> str:
    """Strip markdown, keep only actual spoken content."""
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove frontmatter
    content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)
    # Remove checklists (lines starting with - [ ])
    content = re.sub(r'^\s*-\s*\[[ x]\]', '', content, flags=re.MULTILINE)
    # Remove tables (lines with |)
    content = re.sub(r'^\s*\|.*\|\s*$', '', content, flags=re.MULTILINE)
    # Remove headers
    content = re.sub(r'^#+\s.*$', '', content, flags=re.MULTILINE)
    # Keep only KEEP blocks
    return extract_keep_blocks(content)


def count_particles(text: str) -> int:
    """Count sentence-final particles."""
    count = 0
    for p in PARTICLES:
        # Match as standalone word (not inside other words)
        count += len(re.findall(rf'\b{p}\b', text, re.IGNORECASE))
    return count


def count_fragments(text: str, max_words: int = 6) -> int:
    """Count sentences with ≤max_words."""
    # Split by sentence terminators (Vietnamese uses . ! ? but also can end without)
    sentences = re.split(r'[.!?]\s+', text)
    fragments = 0
    for s in sentences:
        s = s.strip()
        if 0 < len(s.split()) <= max_words:
            # Make sure it's not a heading/checklist (heuristic: contains at least one verb/noun)
            if any(c in s for c in 'àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ'):
                fragments += 1
    return fragments


def count_wpm(text: str, duration_seconds: int = 75) -> int:
    """Estimate words per minute. Default 75s script duration."""
    words = len(text.split())
    return int(words * 60 / duration_seconds)


def check_vietnamese_ratio(text: str) -> float:
    """Check ratio of Vietnamese diacritic characters."""
    vietnamese = sum(1 for c in text if c in 'àáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵĂÂĐÊÔƠƯ')
    return vietnamese / max(len(text), 1)


def run_checks(content: str) -> dict:
    """Run all 8 checks, return dict of check_name → (passed: bool, detail: str)."""
    script_text = extract_script_text(content)
    results = {}

    # 1. Particles
    p_count = count_particles(script_text)
    results['1. Particles ≥5'] = (p_count >= 5, f"Found {p_count}, need ≥5")

    # 2. Fragments
    f_count = count_fragments(script_text)
    results['2. Fragments ≥3'] = (f_count >= 3, f"Found {f_count}, need ≥3")

    # 3. Forbidden words
    f_hits = [(w, script_text.count(w)) for w in FORBIDDEN if script_text.count(w) > 0]
    results['3. Forbidden = 0'] = (len(f_hits) == 0, f"Found: {f_hits}" if f_hits else "Clean")

    # 4. Length rhythm (câu 11 từ → fragment → câu 11 từ) - approximate
    sentences = re.split(r'[.!?]\s+', script_text)
    long_sentences = sum(1 for s in sentences if len(s.split()) > 8)
    short_sentences = sum(1 for s in sentences if 0 < len(s.split()) <= 6)
    rhythm_ok = long_sentences >= 2 and short_sentences >= 3
    results['4. Length rhythm OK'] = (
        rhythm_ok,
        f"{long_sentences} long + {short_sentences} short sentences"
    )

    # 5. WPM ≥ 200
    wpm = count_wpm(script_text, duration_seconds=75)
    results['5. WPM ≥200'] = (wpm >= 200, f"{wpm} WPM, target 200-250")

    # 6. No formal opener
    formal_hit = [op for op in FORMAL_OPENERS if script_text.startswith(op)]
    results['6. Mid-thought start'] = (not formal_hit, f"Hit: {formal_hit}" if formal_hit else "OK")

    # 7. Sensory check (placeholder - manual review needed for "không hoa mỹ")
    # Detect common hoa mỹ words
    hoa_my = ['POV', 'cinematic', 'sensory', 'signature', 'masterpiece', 'flat lay',
              'nam châm tủ lạnh', 'Magnetic N52', '1/4 inch', 'đẳng cấp', 'tuyệt vời']
    hoa_my_hits = [(w, script_text.count(w)) for w in hoa_my if script_text.count(w) > 0]
    results['7. No từ hoa mỹ'] = (len(hoa_my_hits) == 0, f"Found: {hoa_my_hits}" if hoa_my_hits else "Clean")

    # 8. Vietnamese ratio ≥60%
    vn_ratio = check_vietnamese_ratio(script_text)
    results['8. Vietnamese ≥60%'] = (vn_ratio >= MIN_VIETNAMESE_CHARS, f"{vn_ratio*100:.0f}% Vietnamese")

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_voice_script.py <script-file.md>")
        print("\nVerifies 8 bài học văn nói tự nhiên cho TikTok script (v0.10.0).")
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"❌ File not found: {path}")
        sys.exit(1)

    content = path.read_text(encoding='utf-8')

    print(f"=== Verify: {path.name} ===\n")
    results = run_checks(content)

    passed = 0
    failed = 0
    for check, (ok, detail) in results.items():
        icon = '✅' if ok else '❌'
        print(f"  {icon} {check}: {detail}")
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n=== Summary: {passed}/8 passed, {failed} failed ===")

    if failed == 0:
        print("\n✅ Script passed all 8 văn nói checks - ready to generate voice!")
        sys.exit(0)
    else:
        print(f"\n❌ Fix {failed} check(s) trước khi generate voice.")
        sys.exit(1)


if __name__ == '__main__':
    main()