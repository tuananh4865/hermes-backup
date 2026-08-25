#!/usr/bin/env python3
"""
verify_script_7_checks.py — Re-runnable verification cho TikTok script 4-PART
=====================================================================

Được viết 2026-07-25 từ session Dodoto Lux Air V3 để verify script TikTok lifestyle
theo 7 rules vĩnh viễn đã codify trong skill tiktok-product-script v0.13.0.

Usage:
    python3 verify_script_7_checks.py <path-to-script.md>
    python3 verify_script_7_checks.py /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/scripts/dodoto-lux-air-v3-problem-solution.md

7 Checks:
    1. Từ hoa mỹ = 0 (loại NEGATIVE examples trong Tone rule)
    2. Particles (đấy/nhá/nhé/nhỉ/ấy/thôi/luôn) ≥5
    3. Fragments 3-5 từ ≥3
    4. WPM 200-280 (target 230)
    5. First-person "mình" ≥6/version
    6. Từ cấm kỵ (toàn bộ/mọi người/đặc biệt/vô cùng/rất nhiều) = 0
    7. Hook VN ≤12 từ (đếm theo đoạn trước em-dash đầu tiên)

Output: PASS / PARTIAL / FAIL với số check pass + chi tiết từng check.

Exit code: 0 nếu PASS tất cả, 1 nếu FAIL.
"""

import re
import sys
from pathlib import Path


# === CONFIG ===
HOA_MY = [
    "POV", "sensory", "cinematic", "signature", "masterpiece",
    "Magnetic N52", "Arca-Swiss", "tuyệt vời", "hoàn hảo", "đẳng cấp",
    "đỉnh cao", "sắc nét", "trau chuốt", "mỹ miều",
]
PARTICLES = ["đấy", "nhá", "nhé", "nhỉ", "ấy", "thôi", "luôn"]
FORBIDDEN = ["toàn bộ", "mọi người", "đặc biệt", "vô cùng", "rất nhiều"]
FRAGMENT_MIN = 3
FRAGMENT_MAX = 6
WPM_MIN = 200
WPM_MAX = 280
WPM_TARGET = 230
FIRST_PERSON_MIN = 6
HOOK_VN_MAX = 12


def extract_script_only(text: str) -> str:
    """Loại bỏ frontmatter + Tone rule + Sources section để tính toán voice-only."""
    script = re.sub(r"^---.*?---", "", text, count=1, flags=re.DOTALL)
    script = re.sub(r"## 📚 SOURCES.*$", "", script, flags=re.DOTALL)
    # Loại bỏ NEGATIVE examples trong Tone rule
    script = re.sub(r"- KHÔNG từ hoa mỹ:.*", "", script)
    script = re.sub(r"- KHÔNG dùng.*", "", script)
    return script


def count_hoa_my(text: str) -> int:
    pattern = r"\b(" + "|".join(re.escape(w) for w in HOA_MY) + r")\b"
    return len(re.findall(pattern, text, re.IGNORECASE))


def count_particles(text: str) -> int:
    pattern = r"\b(" + "|".join(PARTICLES) + r")\b"
    return len(re.findall(pattern, text, re.IGNORECASE))


def count_fragments(text: str) -> int:
    """Đếm câu ngắn 3-5 từ trong blockquotes."""
    cau = re.findall(r'> \*?"?([^.\n]+)"?\*?', text)
    return sum(1 for c in cau if FRAGMENT_MIN <= len(c.split()) <= FRAGMENT_MAX)


def count_wpm(text: str, total_duration_sec: float = 330) -> float:
    """Tính WPM. Default 3 version × 110s = 330s."""
    text_only = re.sub(r"[#*\[\]>|\-\d\.\(\)]", " ", text)
    words = len(text_only.split())
    return words / (total_duration_sec / 60)


def count_first_person(text: str) -> int:
    return len(re.findall(r"\bmình\b", text, re.IGNORECASE))


def count_forbidden(text: str) -> int:
    pattern = r"\b(" + "|".join(FORBIDDEN) + r")\b"
    return len(re.findall(pattern, text, re.IGNORECASE))


def count_hook_words(text: str) -> tuple:
    """Đếm từ trong hook Version A (đoạn trước em-dash đầu tiên)."""
    match = re.search(r'## 🅰️.*?### \[0-5s\].*?> \*"([^"]+)"\*', text, re.DOTALL)
    if not match:
        return -1, ""
    hook_text = match.group(1)
    parts = [p.strip() for p in re.split(r"—", hook_text) if p.strip()]
    if not parts:
        return -1, hook_text[:80]
    return len(parts[0].split()), parts[0]


def verify(script_path: str) -> dict:
    path = Path(script_path)
    if not path.exists():
        return {"error": f"File not found: {script_path}"}

    raw = path.read_text()
    script = extract_script_only(raw)

    hoa_my = count_hoa_my(script)
    particles = count_particles(script)
    fragments = count_fragments(script)
    wpm = count_wpm(script)
    first_person = count_first_person(script)
    forbidden = count_forbidden(script)
    hook_words, hook_text = count_hook_words(script)

    checks = [
        (f"1. Từ hoa mỹ = 0", hoa_my == 0, hoa_my),
        (f"2. Particles ≥{5}", particles >= 5, particles),
        (f"3. Fragments {FRAGMENT_MIN}-{FRAGMENT_MAX} từ ≥3", fragments >= 3, fragments),
        (f"4. WPM {WPM_MIN}-{WPM_MAX} (target {WPM_TARGET})", WPM_MIN <= wpm <= WPM_MAX, f"{wpm:.0f}"),
        (f"5. First-person 'mình' ≥{FIRST_PERSON_MIN}", first_person >= FIRST_PERSON_MIN, first_person),
        (f"6. Từ cấm kỵ = 0", forbidden == 0, forbidden),
        (f"7. Hook VN ≤{HOOK_VN_MAX} từ", 0 < hook_words <= HOOK_VN_MAX, f"{hook_words} ('{hook_text[:50]}')"),
    ]

    passed = sum(1 for _, ok, _ in checks if ok)
    if passed == len(checks):
        verdict = "PASS"
    elif passed >= len(checks) - 2:
        verdict = "PARTIAL"
    else:
        verdict = "FAIL"

    return {
        "file": str(path),
        "size_bytes": path.stat().st_size,
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "verdict": verdict,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 verify_script_7_checks.py <path-to-script.md>")
        sys.exit(2)

    result = verify(sys.argv[1])

    if "error" in result:
        print(f"❌ {result['error']}")
        sys.exit(1)

    print("=" * 60)
    print(f"VERIFY: {Path(result['file']).name}")
    print("=" * 60)
    for name, ok, val in result["checks"]:
        icon = "✅" if ok else "❌"
        print(f"  {icon} {name}: {val}")

    print(f"\n🎯 {result['verdict']} {result['passed']}/{result['total']}")
    print(f"File: {result['size_bytes']:,} bytes")

    sys.exit(0 if result["verdict"] == "PASS" else 1)


if __name__ == "__main__":
    main()
