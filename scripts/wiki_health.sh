#!/bin/bash
# Wiki Health Check + Self-Heal - Daily cron (4AM)
# Check health, auto-fix broken wikilinks, report to Telegram

REPORT_DIR="$HOME/.hermes/memories"
REPORT_FILE="$REPORT_DIR/wiki_health_report.json"
mkdir -p "$REPORT_DIR"

WIKI_PATH="/Volumes/Storage-1/Hermes/wiki"
cd "$WIKI_PATH" || exit 1

# Phase 1: Run semantic health check (fast, for health score)
python3 scripts/wiki_semantic_health.py > /tmp/wiki_health_output.txt 2>&1
TOTAL=$(grep "SUMMARY:" /tmp/wiki_health_output.txt | grep -oP '\d+' | tail -1)

# Phase 2: Auto-fix broken wikilinks (create stubs for missing pages)
# Run in fix mode — creates stub pages for every broken link
STUBS_LOG="/tmp/wiki_self_heal_stubs.log"
> "$STUBS_LOG"
python3 scripts/wiki_self_heal.py --fix --links > "$STUBS_LOG" 2>&1

# Count results
STUBS_CREATED=$(grep -c "Creating stub\|Created:" "$STUBS_LOG" 2>/dev/null || echo "0")
BROKEN_COUNT=$(grep "Found [0-9]* broken links" "$STUBS_LOG" 2>/dev/null | grep -oP '\d+' | head -1 || echo "0")
SKIPPED_COUNT=$(grep "Skipped [0-9]* path" "$STUBS_LOG" 2>/dev/null | grep -oP '\d+' | head -1 || echo "0")

echo "=== Wiki Health + Self-Heal — $(date '+%Y-%m-%d %H:%M') ===" > /tmp/wiki_health_summary.txt
echo "Wiki path: $WIKI_PATH" >> /tmp/wiki_health_summary.txt
echo "Files scanned: $(grep 'Files scanned:' "$STUBS_LOG" | grep -oP '\d+' | head -1 || echo '?')" >> /tmp/wiki_health_summary.txt
echo "Broken wikilinks found: $BROKEN_COUNT" >> /tmp/wiki_health_summary.txt
echo "Stubs created: $STUBS_CREATED" >> /tmp/wiki_health_summary.txt
echo "Path-separator links (skipped): $SKIPPED_COUNT" >> /tmp/wiki_health_summary.txt
echo "Semantic health total issues: $TOTAL" >> /tmp/wiki_health_summary.txt
echo "" >> /tmp/wiki_health_summary.txt

# Show top broken link categories (first 5 examples)
if [ -n "$BROKEN_COUNT" ] && [ "$BROKEN_COUNT" -gt 0 ]; then
    echo "Top broken link examples (first 5):" >> /tmp/wiki_health_summary.txt
    grep "^  " "$STUBS_LOG" 2>/dev/null | head -5 >> /tmp/wiki_health_summary.txt
fi

# SILENT if healthy, SPEAK if issues
if [ -z "$TOTAL" ] || [ "$TOTAL" = "0" ]; then
    echo "[SILENT] Wiki semantically healthy ✓"
else
    echo "⚠️  Wiki health issues: $TOTAL (semantic) + $BROKEN_COUNT broken links"
    cat /tmp/wiki_health_summary.txt
fi