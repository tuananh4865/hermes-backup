#!/bin/bash
# Inject Fable-5 patterns vào SOUL.md (idempotent)
# Usage: bash add-fable5-to-soul.sh <soul-file>
# Created: 2026-06-16

set -e

SOUL_FILE="$1"
if [ -z "$SOUL_FILE" ] || [ ! -f "$SOUL_FILE" ]; then
  echo "Usage: $0 <path-to-SOUL.md>"
  exit 1
fi

# Check if already has Fable-5 section (more robust — check BOTH the header AND shared ref link)
# Use case-sensitive grep to avoid false matches on "Fable-5" mentions
if grep -q "FABLE-5 PATTERNS" "$SOUL_FILE" && grep -q "fable5-patterns.md" "$SOUL_FILE"; then
  echo "✅ $SOUL_FILE already has Fable-5 section + shared ref — skipping"
  exit 0
fi

# Append Fable-5 patterns
cat >> "$SOUL_FILE" << 'EOF'

---

## 🆕 FABLE-5 PATTERNS (BẮT BUỘC — 2026-06-16)

> **Tuấn Anh mandate:** 4 patterns này PHẢI áp dụng MỌI agent context.
> **Full detail:** [`~/.hermes/profiles/_shared/fable5-patterns.md`](../../_shared/fable5-patterns.md)
> **CI gate:** `bash ~/.hermes/scripts/check-fable5-compliance.sh`

**4 patterns (1-line summary):**

| # | Pattern | Trigger |
|---|---------|---------|
| 🔌 | MCP Connector | Trước khi browser → check MCP |
| 💾 | Persistent Storage | Key `domain:id`, tiered save |
| 📚 | Skills-First | Load skill TRƯỚC complex task |
| 🔍 | Search Discipline | Scale searches, copyright safe |

**Compliance status:** ✅ Injected by `add-fable5-to-soul.sh` (idempotent).

---

*See `_shared/fable5-patterns.md` for full implementation details.*
EOF

echo "✅ Injected Fable-5 patterns into $SOUL_FILE"
echo "📊 Size: $(wc -l < "$SOUL_FILE") lines"
