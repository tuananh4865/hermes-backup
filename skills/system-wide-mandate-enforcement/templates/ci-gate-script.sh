#!/bin/bash
# CI GATE TEMPLATE
# Copy this file, customize the variables, save as check-<your-mandate>.sh
# Exit 0 = all compliant, Exit 1 = at least one file missing mandate

set -e

# === CONFIGURATION (customize these) ===

HERMES_ROOT="${HOME}/.hermes"

# Filename pattern to scan (e.g. "SOUL.md", "*.py", "*.yaml")
FILE_PATTERN="<your-file-pattern>"

# Exclude paths (templates, build artifacts, etc.)
EXCLUDE_PATHS=(
  "*/docker/*"
  "*/templates/*"
  "*/_archive/*"
  "*/node_modules/*"
)

# Keyword markers (shortest unique substrings)
# These must appear (case-insensitive) in compliant files
MARKERS=(
  "<MARKER_1>"
  "<MARKER_2>"
  "<MARKER_3>"
)

# === BUILD FIND COMMAND ===

EXCLUDE_ARGS=""
for path in "${EXCLUDE_PATHS[@]}"; do
  EXCLUDE_ARGS="$EXCLUDE_ARGS -not -path \"$path\""
done

# === SCAN ===

TARGET_FILES=$(eval "find '$HERMES_ROOT' -name '$FILE_PATTERN' -type f $EXCLUDE_ARGS" 2>/dev/null)

if [ -z "$TARGET_FILES" ]; then
  echo "❌ No $FILE_PATTERN files found in $HERMES_ROOT"
  exit 1
fi

# === CHECK EACH FILE ===

FAILED=0
TOTAL=$(echo "$TARGET_FILES" | wc -l | tr -d ' ')

echo "=================================="
echo "<YOUR-MANDATE> COMPLIANCE CHECK"
echo "=================================="
echo ""
echo "Scanning $TOTAL $FILE_PATTERN file(s)..."
echo ""

for file in $TARGET_FILES; do
  MISSING=()

  for marker in "${MARKERS[@]}"; do
    if ! grep -qi "$marker" "$file"; then
      MISSING+=("$marker")
    fi
  done

  if [ ${#MISSING[@]} -eq 0 ]; then
    echo "✅ $file"
  else
    echo "❌ $file"
    for m in "${MISSING[@]}"; do
      echo "      Missing: $m"
    done
    FAILED=$((FAILED + 1))
  fi
done

# === RESULT ===

echo ""
echo "=================================="
if [ $FAILED -eq 0 ]; then
  echo "✅ PASS — All $TOTAL file(s) comply with <your-mandate>"
  exit 0
else
  echo "❌ FAIL — $FAILED of $TOTAL file(s) need <your-mandate> added"
  echo ""
  echo "To fix, run:"
  echo "  bash $HERMES_ROOT/scripts/add-<your-mandate>.sh <file>"
  exit 1
fi
