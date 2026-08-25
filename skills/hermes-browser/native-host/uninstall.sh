#!/bin/bash
# Hermes Browser Control — Native Host Uninstaller
# Phase 2: One-click removal. Removes manifest + kills any running host process.
# HARD RULE: log every uninstall event.

set -euo pipefail

HOST_NAME="com.hermes.browser_extension"
LOG_FILE="$HOME/.hermes/logs/hermes-browser-host-install.log"
CHROME_NM_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
TARGET_MANIFEST="$CHROME_NM_DIR/${HOST_NAME}.json"

echo "=== Hermes Browser Control — Uninstaller ==="
echo ""

if [ ! -f "$TARGET_MANIFEST" ]; then
    echo "ℹ️  No manifest found at $TARGET_MANIFEST"
    echo "   (Maybe already uninstalled?)"
else
    echo "🗑️  Removing manifest: $TARGET_MANIFEST"
    rm -f "$TARGET_MANIFEST"
fi

# === KILL any running host processes ===
echo ""
echo "🔪 Killing any running host processes..."
pkill -f "hermes_browser_host.js" 2>/dev/null && echo "   killed processes" || echo "   no processes running"

# === LOG UNINSTALL EVENT ===
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] UNINSTALL host=$HOST_NAME manifest=$TARGET_MANIFEST pid=$$" >> "$LOG_FILE"

echo ""
echo "✅ UNINSTALL COMPLETE"
echo "   Manifest removed: $([ -f "$TARGET_MANIFEST" ] && echo NO || echo YES)"
echo "   Log: $LOG_FILE"
echo ""
echo "ℹ️  Restart Chrome for changes to take effect"
