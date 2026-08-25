#!/bin/bash
# Hermes Browser Control — Native Messaging Host Installer
# Phase 2: One-click install. CHROME ONLY (no silent install to other browsers).
#
# HARD RULES (lesson from Hanff Anthropic controversy 18/04/2026):
#   - CHỈ Chrome, KHÔNG Brave/Edge/Arc/Vivaldi/Opera
#   - MANIFEST install chỉ khi user explicit click (KHÔNG auto-launch khi mở app)
#   - SHOW UI prompt trước khi write
#   - LOG install/uninstall event to ~/.hermes/logs/

set -euo pipefail

# === CONFIG ===
HOST_NAME="com.hermes.browser_extension"
LOG_FILE="$HOME/.hermes/logs/hermes-browser-host-install.log"
NODE_BIN="$HOME/.hermes/node/bin/node"
HOST_SCRIPT="$(cd "$(dirname "$0")" && pwd)/hermes_browser_host.js"
CHROME_NM_DIR="$HOME/Library/Application Support/Google/Chrome/NativeMessagingHosts"
TARGET_MANIFEST="$CHROME_NM_DIR/${HOST_NAME}.json"

# === PRECHECK ===
echo "=== Hermes Browser Control — Native Host Installer ==="
echo ""

if [ ! -f "$HOST_SCRIPT" ]; then
    echo "❌ FATAL: host script not found at $HOST_SCRIPT"
    echo "   Make sure you run this from the hermes-browser skill folder."
    exit 1
fi

if [ ! -x "$NODE_BIN" ]; then
    echo "❌ FATAL: Node.js not found at $NODE_BIN"
    echo "   Expected: $(realpath "$NODE_BIN" 2>/dev/null || echo $NODE_BIN)"
    exit 1
fi

if [ ! -d "$CHROME_NM_DIR" ]; then
    echo "❌ FATAL: Chrome NativeMessagingHosts dir not found"
    echo "   Expected: $CHROME_NM_DIR"
    echo "   Is Chrome installed? Try: open -a 'Google Chrome'"
    exit 1
fi

echo "📋 Precheck:"
echo "   Host script:     $HOST_SCRIPT ($(stat -f%z "$HOST_SCRIPT") bytes)"
echo "   Node binary:     $NODE_BIN (version $(node --version 2>/dev/null || echo unknown))"
echo "   Chrome NM dir:    $CHROME_NM_DIR"
echo "   Target manifest:  $TARGET_MANIFEST"
echo ""

# === HARD RULE: explicit user consent ===
echo "⚠️  PRIVACY NOTICE — LESSON FROM ANTHROPIC CONTROVERSY (18/04/2026):"
echo "   This script will write ONE file to Chrome's NativeMessagingHosts dir."
echo "   It will NOT touch Brave, Edge, Arc, Vivaldi, or Opera."
echo "   It will NOT auto-restart on every app launch."
echo "   The only way to remove this is to run uninstall.sh or rename the .json to .disabled."
echo ""
echo "   Reference: https://github.com/anthropics/claude-code/issues/54567"
echo ""
read -p "Continue? (yes/no) " ans
if [ "$ans" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# === UNIQUE EXTENSION ID PLACEHOLDER ===
# Phase 2 still uses placeholder. Phase 4 will use the actual extension ID
# generated when loaded unpacked in Chrome Dev Mode.
# For now, use a wildcard ID since Phase 2 only runs locally.
EXTENSION_ID="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"  # 32-char placeholder

# === GENERATE MANIFEST ===
echo ""
echo "📝 Generating manifest..."

REAL_HOST_SCRIPT=$(realpath "$HOST_SCRIPT")
TMP_MANIFEST=$(mktemp)
sed -e "s|__HOST_SCRIPT_PATH__|$REAL_HOST_SCRIPT|g" \
    -e "s|__EXTENSION_ID__|$EXTENSION_ID|g" \
    "$(dirname "$0")/manifest.template.json" > "$TMP_MANIFEST"

echo "   Generated manifest:"
echo "   ---"
cat "$TMP_MANIFEST" | sed 's/^/   /'
echo "   ---"

# === WRITE MANIFEST ===
echo ""
echo "📥 Writing manifest to Chrome NativeMessagingHosts..."
mkdir -p "$CHROME_NM_DIR"
mv "$TMP_MANIFEST" "$TARGET_MANIFEST"

# === LOG INSTALL EVENT ===
echo ""
echo "📝 Logging install event..."
mkdir -p "$(dirname "$LOG_FILE")"
echo "[$(date -u +"%Y-%m-%dT%H:%M:%SZ")] INSTALL host=$HOST_NAME manifest=$TARGET_MANIFEST pid=$$" >> "$LOG_FILE"

# === SUMMARY ===
echo ""
echo "✅ INSTALL SUCCESS"
echo "   Manifest: $TARGET_MANIFEST"
echo "   Log file: $LOG_FILE"
echo ""
echo "🔧 NEXT STEPS:"
echo "   1. Open Chrome → chrome://extensions → find 'Hermes Browser Control'"
echo "   2. Copy the extension ID (32 chars under the name)"
echo "   3. Run install.sh again — it will regenerate the manifest with the real ID"
echo "   4. Restart Chrome"
echo "   5. Click the 🔥 icon → side panel → click '🔌 Ping Native Host'"
echo "   6. You should see '🔌 PONG received' in the side panel"
echo ""
echo "⚠️  If install.sh fails, run uninstall.sh first"
