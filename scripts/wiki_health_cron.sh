#!/bin/bash
# Wiki Health Check - Daily cron
# Run semantic health check and save report

REPORT_DIR="$HOME/.hermes/memories"
REPORT_FILE="$REPORT_DIR/wiki_health_report.json"
mkdir -p "$REPORT_DIR"

# Run health check and capture output
python3 /Volumes/Storage-1/Hermes/wiki/scripts/wiki_semantic_health.py > /tmp/wiki_health_output.txt 2>&1

# Check total issues from the script output
TOTAL=$(grep "SUMMARY:" /tmp/wiki_health_output.txt | grep -oP '\d+' | tail -1)
if [ -z "$TOTAL" ]; then
    echo "Wiki health check failed to run"
    exit 1
fi

if [ "$TOTAL" = "0" ]; then
    echo "[SILENT] Wiki is semantically healthy ✓"
else
    echo "⚠️  Wiki health issues: $TOTAL total"
    BROKEN=$(grep -c "broken_link" "$REPORT_FILE" 2>/dev/null || echo "0")
    echo "- Broken wikilinks: $(grep 'broken_links' -A2 "$REPORT_FILE" 2>/dev/null | grep count | grep -oP '\d+' | head -1)"
    echo "- Orphan pages: $(grep 'orphan_pages' -A2 "$REPORT_FILE" 2>/dev/null | grep count | grep -oP '\d+' | head -1)"
    echo "- Duplicate titles: $(grep 'duplicate_titles' -A2 "$REPORT_FILE" 2>/dev/null | grep count | grep -oP '\d+' | head -1)"
fi