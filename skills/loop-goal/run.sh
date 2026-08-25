#!/usr/bin/env bash
# loop-goal/run.sh — Universal loop runner
# Usage: ./run.sh "<goal>" --condition "<expr>" --max-runs N --profile NAME

set -e

# === Defaults ===
MAX_RUNS=5
PROFILE="main"
ON_PASS="deliver"
ON_FAIL="archive"
GOAL=""
CONDITION=""

# === Parse args ===
while [[ $# -gt 0 ]]; do
    case $1 in
        --condition) CONDITION="$2"; shift 2 ;;
        --max-runs) MAX_RUNS="$2"; shift 2 ;;
        --profile) PROFILE="$2"; shift 2 ;;
        --on-pass) ON_PASS="$2"; shift 2 ;;
        --on-fail) ON_FAIL="$2"; shift 2 ;;
        *) GOAL="$1"; shift ;;
    esac
done

if [[ -z "$GOAL" || -z "$CONDITION" ]]; then
    echo "❌ Usage: $0 '<goal>' --condition '<expr>' [--max-runs N] [--profile NAME] [--on-pass deliver] [--on-fail archive]"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_DIR="$HOME/.hermes/profiles/$PROFILE"
STATE_FILE="$STATE_DIR/state.md"

# Ensure state dir exists
mkdir -p "$STATE_DIR"
[[ ! -f "$STATE_FILE" ]] && touch "$STATE_FILE"

echo "🚀 /goal loop started"
echo "   Goal: $GOAL"
echo "   Condition: $CONDITION"
echo "   Profile: $PROFILE"
echo "   Max runs: $MAX_RUNS"
echo ""

# === Loop ===
for ((i=1; i<=MAX_RUNS; i++)); do
    RUN_NUM=$i
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📍 RUN #$RUN_NUM / $MAX_RUNS"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # === Maker (placeholder — real impl calls worker agent) ===
    # In production: invoke worker sub-agent with goal + previous feedback
    OUTPUT_FILE="/tmp/loop-goal-run-$RUN_NUM.json"
    cat > "$OUTPUT_FILE" <<EOF
{
  "run": $RUN_NUM,
  "goal": "$GOAL",
  "profile": "$PROFILE",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "verdict": "PENDING",
  "score": 0,
  "issues": []
}
EOF
    echo "   (Maker output: $OUTPUT_FILE)"
    echo ""
    
    # === Checker (placeholder — real impl invokes quality-checker skill) ===
    # Simulate verdict for demo
    if [[ $RUN_NUM -eq 1 ]]; then
        VERDICT="FAIL"
        SCORE=7.5
        ISSUES='["Score below 9.0", "Voice dùng mấy con vợ"]'
    elif [[ $RUN_NUM -eq 2 ]]; then
        VERDICT="WARN"
        SCORE=8.5
        ISSUES='["Score cải thiện nhưng chưa đạt"]'
    else
        VERDICT="PASS"
        SCORE=9.3
        ISSUES='[]'
    fi
    
    # Update output with verdict
    cat > "$OUTPUT_FILE" <<EOF
{
  "run": $RUN_NUM,
  "goal": "$GOAL",
  "profile": "$PROFILE",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "verdict": "$VERDICT",
  "score": $SCORE,
  "issues": $ISSUES
}
EOF
    
    # === Condition check ===
    echo "   Verdict: $VERDICT (score: $SCORE)"
    
    if python3 "$SCRIPT_DIR/condition-parser.py" --check "$VERDICT" "$SCORE" --condition "$CONDITION" 2>/dev/null; then
        echo ""
        echo "✅ CONDITION MET after run $RUN_NUM"
        echo "   → Action: $ON_PASS"
        # TODO: invoke $ON_PASS action
        echo ""
        echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | Run $RUN_NUM/$MAX_RUNS | $VERDICT ($SCORE) | PASS" >> "$STATE_FILE"
        exit 0
    fi
    
    echo "   → Re-running maker with feedback"
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | Run $RUN_NUM/$MAX_RUNS | $VERDICT ($SCORE) | FAIL" >> "$STATE_FILE"
    echo ""
done

# === Max runs exceeded ===
echo "❌ CONDITION NOT MET after $MAX_RUNS runs"
echo "   → Action: $ON_FAIL"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) | Max runs exceeded | FAIL" >> "$STATE_FILE"
exit 1
