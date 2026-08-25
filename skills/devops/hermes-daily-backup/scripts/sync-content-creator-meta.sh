#!/bin/bash
# sync-content-creator-meta.sh
# Generate metadata-only snapshot of Content Creator folder for backup.
# STRUCTURE + SIZES ONLY — NEVER include file content bodies.
#
# Usage: ./sync-content-creator-meta.sh [source_dir] [output_dir]
# Defaults:
#   source_dir = ~/Workspace/Claude/Projects/Content Creator/
#   output_dir = ~/.hermes/backups/content-creator-meta-YYYY-MM-DD/
#
# Idempotent — safe to re-run daily. Each run creates a new date-stamped dir.

set -euo pipefail

SRC="${1:-$HOME/Workspace/Claude/Projects/Content Creator}"
DATE=$(date +%Y-%m-%d)
DEST="${2:-$HOME/.hermes/backups/content-creator-meta-$DATE}"

# Fail-fast if source doesn't exist (operator should be aware)
if [ ! -d "$SRC" ]; then
    echo "ERROR: Source directory does not exist: $SRC" >&2
    exit 1
fi

mkdir -p "$DEST"

# === metadata.json: structure + sizes only ===
# CRITICAL: never include file content. Only paths, sizes, dates, tree.
cd "$SRC"

{
  echo "{"
  echo "  \"synced_at\": \"$(date -Iseconds)\","
  echo "  \"source_root\": \"$SRC\","
  echo "  \"total_size_bytes\": $(find . -type f -exec stat -f%z {} \; 2>/dev/null | awk '{s+=$1} END {print s+0}'),"
  echo "  \"total_files\": $(find . -type f 2>/dev/null | wc -l | tr -d ' '),"
  echo "  \"total_dirs\": $(find . -type d 2>/dev/null | wc -l | tr -d ' '),"
  echo "  \"files\": ["
  find . -type f -exec stat -f"%N|%z|%Sm" {} \; 2>/dev/null | sort | while IFS='|' read -r path size mtime; do
    rel="${path#./}"
    # Escape quotes in path
    safe_rel=$(printf '%s' "$rel" | sed 's/"/\\"/g')
    printf "    {\"path\": \"%s\", \"size_bytes\": %s, \"modified\": \"%s\"},\n" "$safe_rel" "$size" "$mtime"
  done
  echo "  ],"
  echo "  \"note\": \"Metadata only — full content NOT synced (per backup policy)\""
  echo "}"
} > "$DEST/metadata-$DATE.json"

# === tree.txt: visual tree ===
{
  echo "Content Creator Folder Tree — $DATE"
  echo "Source: $SRC"
  echo ""
  find . -mindepth 1 \( -type d -o -type f \) 2>/dev/null | sort | sed 's|[^/]*/|  |g;s|  |├── |'
} > "$DEST/tree-$DATE.txt"

echo "Generated:"
echo "  $DEST/metadata-$DATE.json"
echo "  $DEST/tree-$DATE.txt"
echo ""
echo "Sizes:"
ls -la "$DEST/"
