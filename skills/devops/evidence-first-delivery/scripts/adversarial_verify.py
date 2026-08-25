#!/usr/bin/env python3
"""
Adversarial Subagent Verifier - CLI prompt builder (v1.0, 2026-07-12)

Mục đích: bên thứ 3 verify em tự đánh giá — tránh confirmation bias.

Use case:
    Trước khi em báo "xong" bất kỳ task nào quan trọng, em wrap call này
    để dispatch 1 subagent chạy independent context, KHÔNG biết em đã làm gì.

Nguyên tắc:
    1. INDEPENDENT — subagent chạy isolated context, không thấy quá trình em làm
    2. FAIL-FIRST — giả định claim SAI, tìm evidence phá vỡ
    3. 3-LAYER — STRUCTURAL (file tồn tại) + SEMANTIC (nội dung đúng) + FUNCTIONAL (chạy được)
    4. EVIDENCE SPECIFIC — báo cáo cụ thể + raw data, không abstract
    5. TOOL BUILT-IN — dùng ffprobe/wc/grep, KHÔNG dùng tool do em (tác giả) viết

Companion to: ~/.hermes/scripts/adversarial_verify.py (canonical location)

Usage:
    python3 scripts/adversarial_verify.py "TASK_DESC" "CLAIM" [evidence1] [evidence2] ...

Output: prompt chuẩn để wrap vào delegate_task(goal=..., context="Independent verifier")
"""

import subprocess
import sys


PROMPT_TEMPLATE = """Bạn là INDEPENDENT ADVERSARIAL VERIFIER.

Nhiệm vụ: TÌM BẰNG CHỨNG PHÁ VỠ claim. ĐỪNG tin task author.

═══════════════════════════════════════════════════════════════
TASK DESCRIPTION (author báo cáo):
{claim}

═══════════════════════════════════════════════════════════════
EVIDENCE AUTHOR CUNG CẤP:
{evidence}

═══════════════════════════════════════════════════════════════
BẮT BUỘC — 5 bước kiểm tra:

1. INDEPENDENT VERIFIER
   - Chạy tool BUILT-IN (độc lập với author) để verify
   - Dùng ffprobe/wc/grep/cat/file/chạy được — KHÔNG dùng tool author viết
   - KHÔNG copy verdict từ claim author

2. 3 LAYERS (mỗi layer phải CÓ raw data):
   - LAYER 1 STRUCTURAL: file/folder tồn tại, đúng format, đúng path?
     Ví dụ: file size > 0, extension đúng, permissions ok
   - LAYER 2 SEMANTIC: nội dung khớp với claim?
     Ví dụ: nội dung text/markdown đúng spec, không fabricate, không thiếu phần
   - LAYER 3 FUNCTIONAL: chạy thử / test logic
     Ví dụ: command chạy exit 0, output khớp expected, end-to-end ok

3. FAIL-FIRST MINDSET
   - Giả định claim là SAI từ đầu
   - Tìm evidence phá vỡ claim TRƯỚC
   - Nếu không tìm được evidence fail → đó là PASS

4. EVIDENCE SPECIFIC (không abstract)
   - Báo cáo bằng raw data, số liệu cụ thể
   - KHÔNG nói "có vẻ ok", "khá tốt", "pass" mà không có evidence
   - Mỗi verdict phải kèm:
     * ĐÃ chạy command nào
     * Output raw là gì
     * So với expected ra sao

5. VERDICT — output format:
   - PASS / FAIL / PARTIAL_PASS (1 verdict)
   - Reasoning ngắn (1-2 câu)
   - 3 layers check: mỗi layer 1 dòng evidence
   - Nếu FAIL: liệt kê 3 khả năng sai cụ thể + cách verify từng cái

═══════════════════════════════════════════════════════════════

⚠️ QUAN TRỌNG: Bạn PHẢI trả lời FAIL nếu:
- Không có evidence rõ ràng cho claim
- Layer nào thiếu evidence (không chạy tool để check)
- Khả năng sai nào chưa được kiểm tra

Author sẽ dùng verdict của bạn để quyết định SHIP hay KHÔNG.
Nói PASS không có evidence = vô trách nhiệm. Nói FAIL có evidence = giúp author fix đúng.
"""


def build_prompt(task_description, claim, evidence_list, scope_hint=""):
    """Build adversarial verifier prompt."""
    evidence_str = (
        "\n".join(f"  - {e}" for e in evidence_list) if evidence_list else "  (không có)"
    )
    return PROMPT_TEMPLATE.format(claim=claim, evidence=evidence_str)


def quick_self_check(tool="echo", args=None):
    """Sanity check tool có chạy được không trước khi wrap full prompt."""
    try:
        cmd = [tool]
        if args:
            cmd.extend(args if isinstance(args, list) else [args])
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
        return False


def main():
    """CLI mode: print prompt for subagent verifier."""
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python3 adversarial_verify.py TASK_DESCRIPTION CLAIM [EVIDENCE...]")
        print()
        print("Example:")
        print('  python3 adversarial_verify.py \\')
        print('    "Edit clip 0704" \\')
        print('    "Clip đạt 14/14 features + 1080x1920 + filler=0" \\')
        print('    "file:/path/clip.mp4" "keeps.json"')
        sys.exit(1)

    task_desc = sys.argv[1]
    claim = sys.argv[2]
    evidence = sys.argv[3:] if len(sys.argv) > 3 else []

    print("=" * 60)
    print(f"🎯 ADVERSARIAL VERIFY REQUEST")
    print("=" * 60)
    print(f"Task: {task_desc}")
    print(f"Claim: {claim}")
    print(f"Evidence count: {len(evidence)}")
    for e in evidence:
        print(f"  - {e}")
    print()
    print("Self-check tools trước khi ship:")
    print(f"  - ffprobe: {'✅' if quick_self_check('ffprobe', ['-version']) else '❌'}")
    print(f"  - wc: {'✅' if quick_self_check('wc') else '❌'}")
    print(f"  - grep: {'✅' if quick_self_check('grep', ['--version']) else '❌'}")
    print()
    print("PROMPT CHO SUBAGENT:")
    print("=" * 60)
    prompt = build_prompt(task_desc, claim, evidence)
    print(prompt)
    print("=" * 60)


if __name__ == "__main__":
    main()