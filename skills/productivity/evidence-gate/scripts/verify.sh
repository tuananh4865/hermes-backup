#!/usr/bin/env bash
# 5-Evidence Gate Verifier
# Usage: ./verify.sh <path> [<expected_keyword>]
#
# Runs the structural portion of the 5-Evidence Gate for a single file:
#   1. File exists on disk
#   2. Size > 0
#   3. First 3 lines (or keyword grep) match expectation
#   4. (Tool return) — caller must supply separately
#   5. (Visual/render) — caller must supply separately for semantic artifacts
#
# Exits 0 if all structural checks pass, non-zero otherwise. Output is the
# evidence table the assistant can paste into the reply.

set -e

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <path> [<expected_keyword>]"
  echo "  <path>             File to verify (absolute or relative)"
  echo "  <expected_keyword> Optional: phrase that must appear at least once"
  exit 64
fi

FILE="$1"
KEYWORD="${2:-}"

echo "## ✅ 5-Evidence Gate — $(basename "$FILE")"
echo ""
echo "| # | Evidence | Result |"
echo "|---|---|---|"

# 1. File exists
if [[ -e "$FILE" ]]; then
  PERMS=$(ls -la "$FILE" | awk '{print $1, $3, $4, $5}')
  echo "| 1 | File exists | \`$PERMS\` ✓ |"
else
  echo "| 1 | File exists | **NOT FOUND** at \`$FILE\` ✗ |"
  exit 1
fi

# 2. Size > 0
SIZE=$(wc -c < "$FILE" | tr -d ' ')
if [[ "$SIZE" -gt 0 ]]; then
  echo "| 2 | Size > 0 | $SIZE bytes ✓ |"
else
  echo "| 2 | Size > 0 | 0 bytes ✗ |"
  exit 2
fi

# 3. Content (head -3 + optional keyword)
echo "| 3 | First 3 lines |"
echo "|   | \`\`\` |"
head -3 "$FILE" | sed 's/^/| | /'
echo "|   | \`\`\` |"

if [[ -n "$KEYWORD" ]]; then
  COUNT=$(grep -c "$KEYWORD" "$FILE" 2>/dev/null || echo 0)
  if [[ "$COUNT" -gt 0 ]]; then
    echo "| 3b | Keyword \"$KEYWORD\" present | $COUNT match(es) ✓ |"
  else
    echo "| 3b | Keyword \"$KEYWORD\" present | 0 matches ✗ |"
    exit 3
  fi
fi

# 4. (Tool return) — printed as reminder, must be supplied by caller
echo "| 4 | Tool return | (caller: paste \`bytes_written\` / \`exit_code\` / HTTP status) |"

# 5. (Visual/render) — semantic check, caller must perform
echo "| 5 | Visual/render | (caller: smoke test for semantic artifacts) |"

echo ""
echo "Structural checks 1-3 PASS. Checks 4 and 5 require caller evidence."
echo "Run with: $0 $FILE $KEYWORD"
