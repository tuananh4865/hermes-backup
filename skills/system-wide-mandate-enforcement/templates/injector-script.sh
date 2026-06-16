#!/bin/bash
# IDEMPOTENT INJECTOR TEMPLATE
# Copy this file, customize the variables, save as add-<your-mandate>.sh
# Usage: bash add-<your-mandate>.sh <target-file>

set -e

# === CONFIGURATION (customize these) ===

# Path to target file (passed as $1)
TARGET_FILE="$1"

# Path to shared reference file
REFERENCE_FILE="~/.hermes/profiles/_shared/<your-mandate>.md"

# Marker to detect if already injected (must be unique)
MARKER="<YOUR-MANDATE> BẮT BUỘC"

# Title for the injected section
SECTION_TITLE="<YOUR-MANDATE> (BẮT BUỘC — YYYY-MM-DD)"

# Mandate date
MANDATE_DATE="YYYY-MM-DD"

# === VALIDATION ===

if [ -z "$TARGET_FILE" ] || [ ! -f "$TARGET_FILE" ]; then
  echo "Usage: $0 <path-to-target-file>"
  echo ""
  echo "Inject '<your-mandate>' compliance block into target file."
  echo "Idempotent: re-running on compliant file is a no-op."
  exit 1
fi

# === IDEMPOTENCY CHECK ===

if grep -q "$MARKER" "$TARGET_FILE"; then
  echo "✅ $TARGET_FILE already has $MARKER — skipping"
  exit 0
fi

# === INJECT ===

cat >> "$TARGET_FILE" << EOF

---

## $SECTION_TITLE

> **Mandate:** <one-line summary of why this exists>
> **Full detail:** \`$REFERENCE_FILE\`
> **CI gate:** \`bash ~/.hermes/scripts/check-<your-mandate>.sh\`

**Summary:**

| # | Item | Trigger |
|---|------|---------|
| 1 | <name> | <1-line> |
| 2 | <name> | <1-line> |

**Compliance status:** ✅ Injected by \`$(basename "$0")\` (idempotent).

---

*See shared reference for full implementation details.*
EOF

echo "✅ Injected $SECTION_TITLE into $TARGET_FILE"
echo "📊 Size: $(wc -l < "$TARGET_FILE") lines (was $(($(wc -l < "$TARGET_FILE") - 20)) before)"
