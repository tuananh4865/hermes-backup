#!/bin/bash
# restore-env.sh — Restore ~/.hermes/.env từ safe backup
# Created: 2026-06-25 — sau incident cron 3AM xoá .env liên tục (06-18 + 06-25, gap 7 ngày)
#
# Usage:
#   ./restore-env.sh           # Restore từ backup volume
#   ./restore-env.sh --dry-run # Check status, không write
#   ./restore-env.sh --from <path>  # Restore từ path khác
#
# Backup location: /Volumes/Storage-1/Hermes/secrets/.env.hermes.backup
# Pattern: Cron hermes-daily-backup 3AM dùng `git reset --hard origin/main`
#   → xoá file .env khỏi working tree khi file đó đã bị `git rm --cached`
#   → file secret gốc trên local bị wipe. Đây là bug, KHÔNG phải feature.

set -euo pipefail

BACKUP_DEFAULT="/Volumes/Storage-1/Hermes/secrets/.env.hermes.backup"
TARGET="$HOME/.hermes/.env"
DRY_RUN=false
FROM=""

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run) DRY_RUN=true; shift ;;
    --from) FROM="$2"; shift 2 ;;
    -h|--help)
      grep '^#' "$0" | sed 's/^# \?//'
      exit 0
      ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

BACKUP="${FROM:-$BACKUP_DEFAULT}"

# Pre-flight checks
if [[ ! -f "$BACKUP" ]]; then
  echo "❌ Backup file not found: $BACKUP" >&2
  echo "   Cần restore thủ công từ iCloud/notes/keychain" >&2
  exit 1
fi

BACKUP_SIZE=$(wc -c < "$BACKUP" | tr -d ' ')
BACKUP_MTIME=$(stat -f "%Sm" "$BACKUP" 2>/dev/null || stat -c "%y" "$BACKUP" 2>/dev/null || echo "unknown")
echo "📦 Backup: $BACKUP"
echo "   Size:   $BACKUP_SIZE bytes"
echo "   Mtime:  $BACKUP_MTIME"

if [[ -f "$TARGET" ]]; then
  TARGET_SIZE=$(wc -c < "$TARGET" | tr -d ' ')
  TARGET_MTIME=$(stat -f "%Sm" "$TARGET" 2>/dev/null || stat -c "%y" "$TARGET" 2>/dev/null || echo "unknown")
  echo "📍 Target: $TARGET"
  echo "   Size:   $TARGET_SIZE bytes"
  echo "   Mtime:  $TARGET_MTIME"

  # Check if backup is newer
  if [[ "$TARGET_SIZE" == "$BACKUP_SIZE" ]]; then
    echo "✅ Target size matches backup — nothing to do"
    exit 0
  fi

  if [[ "$TARGET_SIZE" -gt "$BACKUP_SIZE" ]]; then
    echo "⚠️  Target ($TARGET_SIZE B) > backup ($BACKUP_SIZE B) — target có vẻ đầy đủ hơn"
    read -p "   Overwrite anyway? (y/N) " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Yy]$ ]] && { echo "Aborted."; exit 1; }
  fi
else
  echo "⚠️  Target MISSING: $TARGET (sẽ restore mới)"
fi

if $DRY_RUN; then
  echo ""
  echo "🔍 DRY-RUN — sẽ copy:"
  echo "   $BACKUP → $TARGET"
  echo "   chmod 600 $TARGET"
  exit 0
fi

# Actual restore
mkdir -p "$(dirname "$TARGET")"
cp "$BACKUP" "$TARGET"
chmod 600 "$TARGET"
echo ""
echo "✅ Restored: $TARGET"
echo "   Size: $(wc -c < "$TARGET" | tr -d ' ') bytes"
echo "   Perm: $(stat -f '%Sp' "$TARGET")"
echo ""
echo "🔍 Verify (5 evidence gate):"
echo "   1. File exists:      $(test -f "$TARGET" && echo ✅ || echo ❌)"
echo "   2. Size non-zero:    $(test $(wc -c < "$TARGET") -gt 0 && echo ✅ || echo ❌)"
echo "   3. Permissions 600:  $(test "$(stat -f '%Lp' "$TARGET")" = "600" && echo ✅ || echo ❌)"
echo "   4. Key count:        $(grep -cE '^[A-Z_]+=' "$TARGET") keys"
echo "   5. Sample key check: $(grep -c 'MINIMAX_API_KEY' "$TARGET") (expect: 1)"