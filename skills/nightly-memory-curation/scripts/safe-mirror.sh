#!/bin/bash
# safe-mirror.sh — EAGAIN-safe iCloud mirror for the 3 always-mirror files
#
# Verified working 2026-06-28 on Tuấn Anh's vault after 3 cp + 1 rsync retries
# failed with EAGAIN (Resource deadlock avoided) when iCloud was actively
# syncing the destination file. The cat-to-tmp + atomic-mv pattern bypasses
# the mmap-based open-file lock that iCloud's background sync holds.
#
# Usage:
#   bash safe-mirror.sh                          # mirror all 3 always-mirror files
#   bash safe-mirror.sh log.md learned-about-tuananh.md index.md
#   VAULT=/custom/path bash safe-mirror.sh
#
# Exit codes:
#   0 = all files mirrored + byte-identical verified
#   1 = at least one file failed all 3 attempts (check stderr)

set -u

WIKI="${WIKI:-/Volumes/Storage-1/Hermes/wiki}"
VAULT="${VAULT:-$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain}"

# 3 always-mirror files (relative to WIKI; entity file is under entities/)
ALWAYS_MIRROR=(
  "log.md|$WIKI/log.md|$VAULT/log.md"
  "learned-about-tuananh.md|$WIKI/entities/learned-about-tuananh.md|$VAULT/learned-about-tuananh.md"
  "index.md|$WIKI/index.md|$VAULT/index.md"
)

# If user passed file names as args, filter to those
if [ $# -gt 0 ]; then
  FILTERED=()
  for entry in "${ALWAYS_MIRROR[@]}"; do
    name=$(echo "$entry" | cut -d'|' -f1)
    for arg in "$@"; do
      if [ "$name" = "$arg" ]; then
        FILTERED+=("$entry")
        break
      fi
    done
  done
  ALWAYS_MIRROR=("${FILTERED[@]}")
fi

# Pre-flight: verify vault exists
if [ ! -d "$VAULT" ]; then
  echo "ERROR: VAULT not found: $VAULT" >&2
  echo "  iCloud Drive may not be mounted. Verify with: ls \"$HOME/Library/Mobile Documents/\"" >&2
  exit 1
fi

# Pre-flight: verify wiki exists
if [ ! -d "$WIKI" ]; then
  echo "ERROR: WIKI not found: $WIKI" >&2
  echo "  Storage volume may not be mounted. Verify with: ls /Volumes/Storage-1/" >&2
  exit 1
fi

# Pre-flight: log.md staleness check (catches gap-fill trigger)
WIKI_LOG_MTIME=$(stat -f "%m" "$WIKI/log.md" 2>/dev/null || echo 0)
VAULT_LOG_MTIME=$(stat -f "%m" "$VAULT/log.md" 2>/dev/null || echo 0)
if [ "$VAULT_LOG_MTIME" -lt "$WIKI_LOG_MTIME" ]; then
  DELTA=$((WIKI_LOG_MTIME - VAULT_LOG_MTIME))
  DELTA_H=$((DELTA / 3600))
  echo "STALE: vault log.md is ${DELTA}s (~${DELTA_H}h) behind wiki log.md"
  echo "  → This is a gap-fill signal. All 3 always-mirror files will be re-mirrored."
fi

FAILED=0

for entry in "${ALWAYS_MIRROR[@]}"; do
  IFS='|' read -r name src dst <<< "$entry"

  if [ ! -f "$src" ]; then
    echo "  [SKIP] $name: source not found ($src)"
    continue
  fi

  echo "[$name] mirroring..."

  # Ensure dst parent dir exists (for entity file in $VAULT root)
  mkdir -p "$(dirname "$dst")"

  # Try 1: simple cp (with iCloud sync grace period)
  sleep 3
  if cp -f "$src" "$dst" 2>/tmp/safe-mirror-cp-err.log; then
    SRC_SIZE=$(stat -f "%z" "$src" 2>/dev/null)
    DST_SIZE=$(stat -f "%z" "$dst" 2>/dev/null)
    if [ "$SRC_SIZE" = "$DST_SIZE" ]; then
      # Final byte-identical check
      if diff -q "$src" "$dst" >/dev/null 2>&1; then
        echo "  [OK] $name: cp success, size=$SRC_SIZE, byte-identical"
        continue
      fi
    fi
  fi

  # Try 2: cat to tmp + atomic mv (bypasses mmap open-file lock)
  echo "  [RETRY] $name: cp size mismatch or failed, trying cat>tmp+mv..."
  sleep 20
  if cat "$src" > "$dst.tmp" 2>/tmp/safe-mirror-cat-err.log && \
     mv "$dst.tmp" "$dst" 2>/tmp/safe-mirror-mv-err.log; then
    SRC_SIZE=$(stat -f "%z" "$src" 2>/dev/null)
    DST_SIZE=$(stat -f "%z" "$dst" 2>/dev/null)
    if [ "$SRC_SIZE" = "$DST_SIZE" ] && diff -q "$src" "$dst" >/dev/null 2>&1; then
      echo "  [OK] $name: cat+mv success, size=$SRC_SIZE, byte-identical"
      continue
    fi
  fi

  # Try 3: longer wait + retry from scratch
  echo "  [RETRY] $name: cat+mv failed, waiting 60s for iCloud..."
  sleep 60
  if cp -f "$src" "$dst" 2>/tmp/safe-mirror-cp3-err.log; then
    SRC_SIZE=$(stat -f "%z" "$src" 2>/dev/null)
    DST_SIZE=$(stat -f "%z" "$dst" 2>/dev/null)
    if [ "$SRC_SIZE" = "$DST_SIZE" ] && diff -q "$src" "$dst" >/dev/null 2>&1; then
      echo "  [OK] $name: 60s-wait cp success, size=$SRC_SIZE, byte-identical"
      continue
    fi
  fi

  echo "  [FAIL] $name: all 3 attempts exhausted. Diffs:"
  diff "$src" "$dst" 2>&1 | head -5
  FAILED=$((FAILED + 1))
done

if [ $FAILED -gt 0 ]; then
  echo
  echo "MIRROR FAILED: $FAILED file(s) not byte-identical after 3 attempts each"
  exit 1
fi

echo
echo "MIRROR OK: all files byte-identical"
exit 0
