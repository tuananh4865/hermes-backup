#!/bin/bash
# Voice QA Gate — Block delivery if voice violations found
# Scan cho: "mấy con vợ", "mấy đứa", "mấy chị", "các bạn ơi"
# Usage: ./voice-scan.sh <file_or_stdin>
# Exit 0 = pass, Exit 1 = BLOCK

set -e

INPUT="${1:-/dev/stdin}"

if [ "$INPUT" != "/dev/stdin" ] && [ ! -f "$INPUT" ]; then
    echo "❌ No content provided (file not found: $INPUT)"
    exit 1
fi

# Voice violations list (post-2026-06-13 — anh đã loại bỏ HOÀN TOÀN)
# Pattern mở rộng để cover cả "anh + mấy con vợ" và "các bạn ơi" variations
VIOLATIONS=$(grep -cE "mấy con vợ|mấy đứa|mấy chị|các bạn ơi|các bạn à|các mom ơi" "$INPUT" 2>/dev/null || echo "0")

if [ "$VIOLATIONS" -gt 0 ]; then
    echo "🚨 VOICE BLOCK: $VIOLATIONS violation(s) found"
    echo "--- Violations: ---"
    grep -nE "mấy con vợ|mấy đứa|mấy chị|các bạn ơi|các bạn à|các mom ơi" "$INPUT"
    echo ""
    echo "FIX REQUIRED — edit inline, re-scan, then deliver"
    echo "Wiki rule: wiki/entities/learned-about-tuananh.md → Voice & Pronouns"
    echo "Voice đã đổi từ 13/06/2026: LOẠI BỎ 'anh + mấy con vợ' + 'mấy đứa' + 'các bạn ơi'"
    echo "Voice MỚI: Trung tính, chuyên nghiệp — dùng 'mình'/'bạn'/neutral"
    exit 1
fi

echo "✅ VOICE PASS — content clean"
exit 0