#!/bin/bash
# SOUL.md Fable-5 Enforcement Checker
# Đảm bảo MỌI SOUL.md file (hiện tại + tương lai) có 4 Fable-5 patterns
# Created: 2026-06-16 — Tuấn Anh yêu cầu bắt buộc toàn hệ thống

set -e

HERMES_ROOT="${HOME}/.hermes"
# Match cả tên đầy đủ + tên viết tắt (để pass khi SOUL.md dùng reference ngắn gọn)
PATTERNS=(
  "MCP CONNECTOR"
  "PERSISTENT STORAGE"
  "SKILLS-FIRST"
  "SEARCH DISCIPLINE"
)

# Tìm tất cả SOUL.md files
# Tìm tất cả SOUL.md files (BỎ docker templates)
SOUL_FILES=$(find "$HERMES_ROOT" -name "SOUL.md" -type f -not -path "*/docker/*" 2>/dev/null)

if [ -z "$SOUL_FILES" ]; then
  echo "❌ No SOUL.md files found in $HERMES_ROOT"
  exit 1
fi

FAILED=0
echo "=================================="
echo "FABLE-5 SOUL.md ENFORCEMENT CHECK"
echo "=================================="
echo ""

for file in $SOUL_FILES; do
  echo "📄 Checking: $file"
  MISSING=()

  for pattern in "${PATTERNS[@]}"; do
    if ! grep -qi "$pattern" "$file"; then
      MISSING+=("$pattern")
    fi
  done

  if [ ${#MISSING[@]} -eq 0 ]; then
    echo "   ✅ All 4 Fable-5 patterns present"
  else
    echo "   ❌ Missing ${#MISSING[@]} pattern(s):"
    for m in "${MISSING[@]}"; do
      echo "      - $m"
    done
    FAILED=$((FAILED + 1))
  fi
  echo ""
done

echo "=================================="
if [ $FAILED -eq 0 ]; then
  echo "✅ PASS — All SOUL.md files comply with Fable-5 mandate"
  exit 0
else
  echo "❌ FAIL — $FAILED file(s) need Fable-5 patterns added"
  echo ""
  echo "Run this to fix:"
  echo "  bash $HERMES_ROOT/scripts/add-fable5-to-soul.sh <file>"
  exit 1
fi
