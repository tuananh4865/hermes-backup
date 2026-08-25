#!/usr/bin/env python3
"""
verify_clip.py v3.21.4 (12/07/2026) - Verify TOÀN BỘ goal của skill tiktok-video-editor

Tool BẮT BUỘC chạy ở Bước 8 (VERIFY RE-READ) để đảm bảo file .mp4 cuối
đạt goal của skill v3.21.4 trước khi public.

Quy tắc verify (v3.21.4 - bỏ "đó" và "thì" khỏi filler):
- FILLER: ơ, ờ, ừm, ừ, ó, à, á đứng đầu/cuối câu hoặc sau dấu câu
- ỰM / Ờ: chỉ cần 1 từ đứng đơn (cả seg) hoặc đứng đầu câu
- CÂU TREO: câu vô nghĩa/yếu nghĩa từ 3+ từ (bridge không có predicate rõ ràng)
- LẶP NGHĨA: 2+ từ đầu giống nhau giữa các segs
- HOOK LẶP: 3+ từ đầu giống nhau giữa các segs (gần nhau <15 segs)

GOAL: File final có thể public ngay, không còn lỗi.

Cách dùng:
python3 scripts/verify_clip.py <audio.json> <keeps.json> [render.mp4]
"""

import json
import os
import sys
import subprocess

# FILLER v3.21.4: bỏ "đó" và "thì" (chỉ giữ 7 từ 1-syllable)
FILLERS = ['ơ', 'ờ', 'ừm', 'ừ', 'ó', 'à', 'á']
UM_O_STANDALONE = ['ờ', 'à', 'ừm', 'ơ', 'ừ', 'uh', 'um']


def verify_clip(clip_id, audio_json, keeps_json, render_mp4=None):
    """Verify TOÀN BỘ goal skill v3.21.4"""
    issues = {
        'filler': [],
        'um_o': [],
        'treo': [],
        'lap_nghia': [],
        'hook_lap': [],
    }

    # Load source
    with open(audio_json) as f:
        src = json.load(f)['segments']
    with open(keeps_json) as f:
        keeps = [tuple(k) for k in json.load(f)]

    # 0. Check render file (optional)
    if render_mp4:
        if not os.path.exists(render_mp4):
            return {"error": "❌ File render không tồn tại"}

        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                               'format=duration',
                               '-of', 'default=noprint_wrappers=1:nokey=1',
                               render_mp4], capture_output=True, text=True)
        dur = float(result.stdout.strip())
        if dur < 60 or dur > 180:
            issues['treo'].append(f"⚠️ Duration {dur:.1f}s ngoài khoảng 60-180s")

        result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                               'stream=width,height,sample_rate',
                               '-of', 'default=noprint_wrappers=1',
                               render_mp4], capture_output=True, text=True)
        if '1080' not in result.stdout or '1920' not in result.stdout:
            issues['treo'].append("⚠️ Resolution không đúng 1080x1920")
        if '44100' not in result.stdout:
            issues['treo'].append("⚠️ Audio sample rate không phải 44100Hz")

    chosen_segs = []
    for seg in src:
        for s_start, s_end in keeps:
            if seg['start'] >= s_start - 0.3 and seg['end'] <= s_end + 0.5:
                chosen_segs.append(seg)
                break

    # 1. FILLER đứng đầu/cuối câu (7 từ 1-syllable v3.21.4)
    for seg in chosen_segs:
        text = seg['text'].strip()
        words = text.split()
        if not words: continue
        for j, w in enumerate(words):
            wc = w.lower().strip('.,!?')
            if wc in FILLERS:
                is_filler = (j == 0 or j == len(words) - 1)
                prev_punct = j > 0 and words[j-1][-1] in ',.;:'
                next_punct = j < len(words)-1 and words[j+1][0] in ',.;:'
                if is_filler or prev_punct or next_punct:
                    issues['filler'].append((seg['id'], j, w))
                    break

    # 2. ỰM / Ờ - 1 từ đứng đơn hoặc đầu câu (v3.21.3+)
    for seg in chosen_segs:
        text = seg['text'].strip()
        words = text.split()
        if not words: continue

        # Case 2a: cả seg chỉ là 1 từ filler ờ/à/ừm/ơ
        if len(words) == 1 and words[0].lower().strip('.,!?') in UM_O_STANDALONE:
            issues['um_o'].append((seg['id'], 'STANDALONE', text))
            continue

        # Case 2b: từ ờ/à/ừm/ơ đứng đầu câu
        first_word = words[0].lower().strip('.,!?')
        if first_word in UM_O_STANDALONE:
            issues['um_o'].append((seg['id'], 'FIRST_WORD', text[:80]))

    # 3. CÂU TREO - câu vô nghĩa/yếu nghĩa từ 3+ từ (v3.21.3+)
    USP_KEYWORDS = ['sẽ', 'là', 'có thể', 'giúp', 'cho', 'được', 'hơn', 'nhất', 'đặc biệt',
                    '1m6', '1.6m', '90 độ', '180 độ', '360 độ', '3kg', '2.5kg',
                    'gấp', 'gọn', 'bền', 'chắc', 'đa năng', 'thông minh', 'chắc chắn']
    BRIDGE_ONLY = ['ờ', 'à', 'ừm', 'ơ', 'bởi', 'vì', 'thôi', 'nha',
                   'cái', 'này', 'như', 'mà', 'cũng', 'đều', 'rất', 'đã', 'có']

    for seg in chosen_segs:
        text = seg['text'].strip()
        words = text.split()
        if 3 <= len(words) <= 8:
            has_usp = any(kw in text.lower() for kw in USP_KEYWORDS)
            has_only_bridge = all(w.lower().strip('.,!?') in BRIDGE_ONLY for w in words)

            # Câu bắt đầu bằng filler ờ/à/ừm + chỉ bridge → TREO
            if (has_only_bridge or
                (not has_usp and words[0].lower().strip('.,!?') in ['ờ', 'à', 'ừm'])):
                issues['treo'].append((seg['id'], text[:80]))

    # 4. LẶP NGHĨA - 2+ từ đầu giống (v3.21.3+)
    for i in range(len(chosen_segs) - 1):
        s1, s2 = chosen_segs[i], chosen_segs[i+1]
        t1 = s1['text'].strip()
        t2 = s2['text'].strip()
        if not t1 or not t2: continue
        w1 = t1.split()
        w2 = t2.split()
        if len(w1) < 3 or len(w2) < 3: continue
        match = sum(1 for a, b in zip(w1[:2], w2[:2])
                   if a.lower().strip('.,!?') == b.lower().strip('.,!?'))
        if match >= 2:
            issues['lap_nghia'].append((s1['id'], s2['id'], t1[:50], t2[:50]))

    # 5. HOOK LẶP - 3+ từ đầu giống (v3.21.3+)
    seen_starts = {}
    for seg in chosen_segs:
        words = seg['text'].strip().split()
        if len(words) < 3: continue
        first3 = ' '.join(words[:3]).lower().strip('.,!?')
        if first3 in seen_starts:
            other_id = seen_starts[first3]
            if abs(seg['id'] - other_id) < 15:
                issues['hook_lap'].append((other_id, seg['id'], first3))
        else:
            seen_starts[first3] = seg['id']

    return issues


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 verify_clip.py <audio.json> <keeps.json> [render.mp4]")
        sys.exit(1)

    audio_json = sys.argv[1]
    keeps_json = sys.argv[2]
    render_mp4 = sys.argv[3] if len(sys.argv) > 3 else None

    issues = verify_clip(None, audio_json, keeps_json, render_mp4)

    if 'error' in issues:
        print(issues['error'])
        sys.exit(1)

    print(f"\n{'='*70}")
    print(f"VERIFY REPORT v3.21.4 - {os.path.basename(audio_json)}")
    print(f"{'='*70}\n")

    total = sum(len(v) for v in issues.values() if isinstance(v, list))

    if total == 0:
        print("✅ ĐẠT GOAL - file có thể public!")
        sys.exit(0)
    else:
        print(f"❌ CHƯA ĐẠT GOAL - {total} vấn đề:\n")
        for key, val in issues.items():
            if isinstance(val, list) and val:
                print(f"  🚨 {key.upper()} ({len(val)}):")
                for item in val[:5]:
                    print(f"     {item}")
        print("\n→ Quay lại Bước 3 (ĐỌC-HIỂU-CẢM-XÚC), sửa keeps, re-render, re-verify")
        sys.exit(1)