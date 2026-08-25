#!/bin/bash
# backup-encrypted-env.sh
# Auto-backup ~/.hermes/.env to encrypted archive.
# Cron 2AM (chạy cùng autoresearch).
# Rotate: giữ 30 backup gần nhất.
#
# Requirements: openssl (built-in macOS), ~/.hermes/.env tồn tại.
# Passphrase: $HERMES_ENV_BACKUP_PASSPHRASE trong shell environment
#             (set 1 lần: echo 'export HERMES_ENV_BACKUP_PASSPHRASE=...' >> ~/.zshrc)

set -euo pipefail

ENV_FILE="$HOME/.hermes/.env"
BACKUP_DIR="/Volumes/Storage-1/Hermes/backups/env-encrypted"
MAX_KEEP=30
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/hermes-env-$TIMESTAMP.tar.gz.enc"

# Pre-checks
if [ ! -f "$ENV_FILE" ]; then
    echo "[$(date)] SKIP: $ENV_FILE not found" >> "$BACKUP_DIR/backup.log"
    exit 0
fi

if [ -z "${HERMES_ENV_BACKUP_PASSPHRASE:-}" ]; then
    echo "[$(date)] ERROR: HERMES_ENV_BACKUP_PASSPHRASE not set" >> "$BACKUP_DIR/backup.log"
    exit 1
fi

mkdir -p "$BACKUP_DIR"

# Backup (tar gzip + openssl encrypt)
tar czf - -C "$(dirname "$ENV_FILE")" "$(basename "$ENV_FILE")" | \
    openssl enc -aes-256-cbc -salt -pbkdf2 \
    -pass "env:HERMES_ENV_BACKUP_PASSPHRASE" \
    -out "$BACKUP_FILE"

# Verify
if [ -s "$BACKUP_FILE" ]; then
    SIZE=$(stat -f%z "$BACKUP_FILE" 2>/dev/null || stat -c%s "$BACKUP_FILE" 2>/dev/null || echo 0)
    if [ "$SIZE" -gt 100 ]; then
        echo "[$(date)] OK: $BACKUP_FILE ($SIZE bytes)" >> "$BACKUP_DIR/backup.log"
        chmod 600 "$BACKUP_FILE"
    else
        echo "[$(date)] FAIL: backup too small ($SIZE bytes)" >> "$BACKUP_DIR/backup.log"
        rm -f "$BACKUP_FILE"
        exit 1
    fi
else
    echo "[$(date)] FAIL: backup file empty" >> "$BACKUP_DIR/backup.log"
    rm -f "$BACKUP_FILE"
    exit 1
fi

# Rotate: keep only MAX_KEEP newest
cd "$BACKUP_DIR"
ls -t hermes-env-*.tar.gz.enc 2>/dev/null | tail -n +$((MAX_KEEP + 1)) | xargs -r rm -f

# Optional: monthly summary log
if [ "$(date +%d)" = "01" ]; then
    COUNT=$(ls hermes-env-*.tar.gz.enc 2>/dev/null | wc -l | tr -d ' ')
    echo "[$(date)] MONTHLY: $COUNT encrypted backups in $BACKUP_DIR" >> "$BACKUP_DIR/backup.log"
fi
