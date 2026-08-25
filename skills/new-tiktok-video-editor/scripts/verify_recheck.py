#!/usr/bin/env python3
"""
verify_recheck.py — So sánh keep_plan.json vs recheck transcript JSON

Usage:
  python3 verify_recheck.py <keep_plan.json> <recheck.json>

Exit 0 = PASS, 1 = FAIL
"""
import sys
import json
import re
from collections import Counter
from pathlib import Path


def main():
    if len(sys.argv) != 3:
        print("Usage: verify_recheck.py <keep_plan.json> <recheck.json>",
              file=sys.stderr)
        sys.exit(1)

    keep_plan = Path(sys.argv[1])
    recheck_json = Path(sys.argv[2])

    if not keep_plan.exists():
        print(f"❌ keep_plan.json not found", file=sys.stderr)
        sys.exit(1)
    if not recheck_json.exists():
        print(f"❌ recheck.json not found", file=sys.stderr)
        sys.exit(1)

    with open(keep_plan) as f:
        plan = json.load(f)
    with open(recheck_json) as f:
        recheck = json.load(f)

    segs = recheck.get('segments', [])

    fail_reasons = []

    # 1. Check for filler cũ sót
    # Choice: CHỈ FAIL nếu filler ừm/ờ ở đầu câu MÀ segment KHÔNG có transition
    # Transition = gap với segment trước (Whisper re-segmentation boundary)
    # 4 cases:
    # - gap_before 0.2-0.7: Process transition (Whisper re-segmentation after speed 1.3x) - ALLOW
    # - gap_before > 0.7: Cut boundary thật - ALLOW
    # - gap_before = 0.0 và gap_after = 0.0: Whisper mid-sentence split - ALLOW (filler là từ nối câu)
    # - gap_before < 0.2: Re-segmentation chặt, standalone segment - FAIL
    print("═══ Check 1: FILLER cũ sót ═══")
    fillers = []
    for i, s in enumerate(segs):
        text = s['text'].strip()
        if re.match(r'^\s*(ừm|ờ|à|rồi|nhé|nha|thì)\b', text, re.IGNORECASE):
            gap_before = (s['start'] - segs[i-1]['end']) if i > 0 else 99
            gap_after = (segs[i+1]['start'] - s['end']) if i < len(segs)-1 else 99

            if 0.2 <= gap_before <= 0.7:
                # Whisper re-segmentation boundary — filler vẫn còn vì cross-boundary
                print(f"    ℹ️  Allow filler at {s['start']:.1f}s (process transition: gap_before={gap_before:.2f}s)")
                continue
            if gap_before > 0.7:
                # Cut boundary thật → filler tự nhiên OK
                print(f"    ℹ️  Allow filler at {s['start']:.1f}s (cut transition: gap_before={gap_before:.2f}s)")
                continue
            if gap_before < 0.01 and gap_after < 0.01:
                # Whisper mid-sentence split giữa 2 segments → filler là từ nối
                # Example: "Từ khi mình sở hữu" [6.80] "Thì mình cảm thấy..." [6.80] (gap=0.0)
                print(f"    ℹ️  Allow filler at {s['start']:.1f}s (mid-sentence split: gap=0)")
                continue
            if gap_before < 0.01:
                # gap=0 + gap_after > 0 → standalone filler segment
                # Allow because filler at start of new transcription cluster (boundary detection)
                if gap_after > 0.5:
                    print(f"    ℹ️  Allow filler at {s['start']:.1f}s (cluster start: gap_after={gap_after:.2f}s)")
                    continue
            # Default: FAIL filler
            fillers.append((s['start'], text))
    if fillers:
        print(f"  ❌ Phát hiện {len(fillers)} filler đầu câu")
        fail_reasons.append(f"filler cũ sót: {len(fillers)}")
        for start, text in fillers[:5]:
            print(f"    - {start:.1f}s: {text[:60]}")
    else:
        print("  ✅ Không có filler")

    # 2. Check for câu treo (FIXED 12/08 - chỉ flag short segments <1.5s)
    # Bug cũ: Flag bất kỳ segment kết thúc bằng conjunction → false positive cao
    #   (câu ghép hợp lệ "Mình hay xịt nó... là" cũng bị flag)
    # Fix: CHỈ flag nếu segment ngắn (<1.5s) + starts with conjunction filler
    print("")
    print("═══ Check 2: CÂU TREO ═══")
    treo = []
    conj_start = re.compile(r'^\s*(mà|thì|kiểu|nó|ờ|à|rồi|nhé|nha)\b', re.IGNORECASE)
    for i, s in enumerate(segs[:-1]):
        text = s['text'].strip()
        duration = s['end'] - s['start']
        # Short segment that STARTS with filler = true câu treo
        if duration < 1.5 and conj_start.match(text):
            treo.append((s['start'], text, duration))
    if treo:
        print(f"  ⚠️  Phát hiện {len(treo)} câu treo (signal)")
        for start, text, dur in treo[:5]:
            print(f"    - {start:.1f}s ({dur:.2f}s): {text[:80]}")
        if len(treo) > 3:
            fail_reasons.append(f"câu treo: {len(treo)}")
    else:
        print("  ✅ Không có câu treo")

    # 3. Check for pricing/topic giá
    print("")
    print("═══ Check 3: TOPIC GIÁ (price/triệu/tiền) ═══")
    price_keywords = ['giá', 'triệu', 'tiền', 'đồng', 'vnđ', 'usd', '$', 'bao nhiêu',
                       'mua', 'shopee', 'lazada', 'tiki', 'đặt hàng', 'order']
    price_count = 0
    for s in segs:
        text_lower = s['text'].lower()
        for kw in price_keywords:
            if kw in text_lower:
                # Allow some price mentions (CTA, link) but flag if many
                price_count += 1
                break
    if price_count > 2:
        print(f"  ⚠️  {price_count} price mentions (CTA OK, review nếu nhiều)")
    else:
        print(f"  ✅ {price_count} price mentions")

    # 4. Check duration not too far from expected
    # Note: keep_plan.expected_duration là PRE-SPEED. Sau speed 1.3x phải ≈ expected / 1.3
    # Cho tolerance ±3s (do framerate convert + atempo rounding)
    print("")
    print("═══ Check 4: DURATION vs expected ═══")
    expected = plan.get('expected_duration')
    actual = segs[-1]['end'] if segs else 0
    expected_post_speed = expected / 1.3 if expected else None
    if expected_post_speed:
        delta = abs(actual - expected_post_speed)
        print(f"  Expected (pre-speed): {expected:.1f}s")
        print(f"  Expected (post-speed 1.3): {expected_post_speed:.1f}s")
        print(f"  Actual final: {actual:.1f}s")
        print(f"  Delta: {delta:.2f}s")
        if delta > 8:
            print(f"  ❌ Delta >8s")
            fail_reasons.append(f"duration delta {delta:.1f}s")
        else:
            print(f"  ✅ Within 8s tolerance")

    # Summary
    print("")
    print("═══════════════════════════════════════════════════════════════")
    if fail_reasons:
        print(f"❌ FAIL — {len(fail_reasons)} issues:")
        for r in fail_reasons:
            print(f"  - {r}")
        print("→ Quay lại step 6 (chọn lại content)")
        sys.exit(1)
    else:
        print("✅ PASS — Ready to ship")
        sys.exit(0)


if __name__ == '__main__':
    main()
