#!/bin/bash
cd /Volumes/Storage-1/Hermes/wiki
python3 scripts/wiki_semantic_health.py > /tmp/wiki_health_output.txt 2>&1
TOTAL=$(grep "SUMMARY:" /tmp/wiki_health_output.txt | sed 's/[^0-9]//g' | tail -c 5)
if [ -z "$TOTAL" ]; then
    echo "Wiki health check failed"
elif [ "$TOTAL" = "0" ]; then
    echo "[SILENT] Wiki healthy"
else
    echo "Wiki issues: $TOTAL"
    grep "Broken wikilinks:" /tmp/wiki_health_output.txt | head -1
    grep "Orphan pages:" /tmp/wiki_health_output.txt | head -1
    grep "Duplicate titles:" /tmp/wiki_health_output.txt | head -1
fi