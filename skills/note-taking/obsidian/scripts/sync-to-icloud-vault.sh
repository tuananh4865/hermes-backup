#!/bin/bash
# sync-to-icloud-vault.sh
# Mirror wiki/ → iCloud Obsidian vault with iCloud-Drive-deadlock retry.
#
# Verified 2026-06-26 on Tuấn Anh's vault:
#   ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/
#
# Why this exists: iCloud Drive can hold a write lock during sync, causing
# `cp` / `rsync` to fail with EAGAIN ("Resource deadlock avoided"). A naive
# loop will silently lose the file. This script:
#   1. Compares mtime before touching the file
#   2. Retries with backoff on EAGAIN
#   3. Verifies mtime actually advanced after each copy
#   4. Logs skipped files for manual follow-up
#
# Usage:
#   bash sync-to-icloud-vault.sh                  # sync default wiki → vault
#   bash sync-to-icloud-vault.sh path/to/file.md  # sync single file
#   WIKI_SRC=/custom/wiki bash sync-to-icloud-vault.sh
#
# Exit codes:
#   0 = all files synced
#   1 = one or more files skipped (see log)
#   2 = source wiki path missing

set -u

WIKI_SRC="${WIKI_SRC:-/Volumes/Storage-1/Hermes/wiki}"
VAULT_DST="${VAULT_DST:-$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain}"
MAX_ATTEMPTS=3
RETRY_SLEEP=10

if [ ! -d "$WIKI_SRC" ]; then
  echo "[FATAL] wiki source not found: $WIKI_SRC" >&2
  exit 2
fi
if [ ! -d "$VAULT_DST" ]; then
  echo "[FATAL] vault destination not found: $VAULT_DST" >&2
  exit 2
fi

log() { printf '[%s] %s\n' "$(date '+%H:%M:%S')" "$*"; }

# sync_one <src> <dst>
# Returns 0 on success, 1 on skip, 2 on source missing.
sync_one() {
  local src="$1" dst="$2"
  if [ ! -f "$src" ]; then
    log "SKIP (no source): $src"
    return 2
  fi

  local src_mtime dst_mtime
  src_mtime=$(stat -f "%m" "$src")
  dst_mtime=$(stat -f "%m" "$dst" 2>/dev/null || echo 0)

  if [ "$dst" = "$VAULT_DST/$(basename "$src")" ] && [ -f "$dst" ] && [ "$src_mtime" -le "$dst_mtime" ]; then
    log "UP-TO-DATE: $(basename "$src")"
    return 0
  fi

  mkdir -p "$(dirname "$dst")"

  local attempt=1
  while [ $attempt -le $MAX_ATTEMPTS ]; do
    cp -f "$src" "$dst" 2>/tmp/sync_eicloud_err
    local rc=$?
    # Verify the copy actually wrote
    if [ -f "$dst" ] && [ "$(stat -f "%m" "$dst")" -ge "$src_mtime" ]; then
      log "OK ($attempt/$MAX_ATTEMPTS): $(basename "$src")"
      return 0
    fi
    if grep -q "Resource deadlock avoided" /tmp/sync_eicloud_err 2>/dev/null; then
      log "EAGAIN ($attempt/$MAX_ATTEMPTS): $(basename "$src") — sleeping ${RETRY_SLEEP}s"
      sleep $RETRY_SLEEP
    else
      log "FAIL ($attempt/$MAX_ATTEMPTS): $(basename "$src") — $(cat /tmp/sync_eicloud_err)"
      return 1
    fi
    attempt=$((attempt + 1))
  done

  log "SKIP after $MAX_ATTEMPTS attempts: $(basename "$src")"
  return 1
}

SKIPPED=0
SYNCED=0

# Mirror top-level files
for f in log.md index.md learned-about-tuananh.md; do
  if sync_one "$WIKI_SRC/$f" "$VAULT_DST/$f"; then
    SYNCED=$((SYNCED + 1))
  else
    SKIPPED=$((SKIPPED + 1))
  fi
done

# Mirror entities/ (only if source dir exists)
if [ -d "$WIKI_SRC/entities" ]; then
  mkdir -p "$VAULT_DST/entities"
  for f in "$WIKI_SRC/entities/"*.md; do
    bn=$(basename "$f")
    if sync_one "$f" "$VAULT_DST/entities/$bn"; then
      SYNCED=$((SYNCED + 1))
    else
      SKIPPED=$((SKIPPED + 1))
    fi
  done
fi

# Mirror comparisons/
if [ -d "$WIKI_SRC/comparisons" ]; then
  mkdir -p "$VAULT_DST/comparisons"
  for f in "$WIKI_SRC/comparisons/"*.md; do
    bn=$(basename "$f")
    if sync_one "$f" "$VAULT_DST/comparisons/$bn"; then
      SYNCED=$((SYNCED + 1))
    else
      SKIPPED=$((SKIPPED + 1))
    fi
  done
fi

log "DONE — synced: $SYNCED, skipped: $SKIPPED"
[ $SKIPPED -eq 0 ] && exit 0 || exit 1
