#!/bin/bash
# diagnose-flood.sh — Auto-detect which Telegram flood root cause is firing
# Usage: bash diagnose-flood.sh [path/to/gateway.log]
# Output: diagnosis report with root cause identified + fix priority

LOG_FILE="${1:-$HOME/.hermes/logs/gateway.log}"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "❌ Log file not found: $LOG_FILE"
    exit 1
fi

echo "═══════════════════════════════════════════════════════"
echo "🔍 Telegram Flood Diagnosis Report"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Log file: $LOG_FILE"
echo "Log size: $(du -h "$LOG_FILE" | cut -f1)"
echo "Log modified: $(stat -f '%Sm' "$LOG_FILE" 2>/dev/null || stat -c '%y' "$LOG_FILE")"
echo ""

# Total counts
TOTAL_FLOOD=$(grep -c "Flood control exceeded" "$LOG_FILE" || echo 0)
TOTAL_FAILED=$(grep -c "Failed to deliver response after.*retries" "$LOG_FILE" || echo 0)
TOTAL_NETWORK=$(grep -c "Network error on send" "$LOG_FILE" || echo 0)
TOTAL_RICH_TRANSIENT=$(grep -c "sendRichMessage transient failure" "$LOG_FILE" || echo 0)

echo "📊 Raw counts (all time):"
echo "  • Flood control exceeded: $TOTAL_FLOOD"
echo "  • Failed to deliver (user-visible): $TOTAL_FAILED"
echo "  • Network errors (NOT flood): $TOTAL_NETWORK"
echo "  • Rich message transient failures: $TOTAL_RICH_TRANSIENT"
echo ""

# Top 5 dates with most floods
echo "📅 Top dates (by flood events):"
grep "Flood control exceeded" "$LOG_FILE" | awk '{print $1}' | sort | uniq -c | sort -rn | head -5
echo ""

# Diagnosis
echo "═══════════════════════════════════════════════════════"
echo "🎯 Root Cause Diagnosis"
echo "═══════════════════════════════════════════════════════"
echo ""

RC1_CONFIRMED=0
RC2_CONFIRMED=0
RC3_CONFIRMED=0
RC4_CONFIRMED=0

# RC1: Rich message double retry
if [[ $TOTAL_RICH_TRANSIENT -gt 50 ]]; then
    echo "🔴 RC1: Rich message double retry — CONFIRMED"
    echo "   Evidence: $TOTAL_RICH_TRANSIENT 'sendRichMessage transient failure' events"
    echo "   Impact: ~46% of all flood events (per 18/06 baseline)"
    echo "   Fix: Set 'telegram.extra.rich_messages: false' in ~/.hermes/config.yaml"
    echo "   Effort: 2 min (config only, no code change)"
    echo ""
    RC1_CONFIRMED=1
else
    echo "🟢 RC1: Rich message double retry — NOT DETECTED ($TOTAL_RICH_TRANSIENT < 50)"
    echo ""
fi

# RC2: Sub-agent burst
PEAK_DAILY=$(grep "Flood control exceeded" "$LOG_FILE" | awk '{print $1}' | sort | uniq -c | sort -rn | head -1 | awk '{print $1}')
if [[ $PEAK_DAILY -gt 200 ]]; then
    echo "🔴 RC2: Sub-agent parallel burst — CONFIRMED"
    echo "   Evidence: Peak day = $PEAK_DAILY flood events (threshold > 200/day)"
    echo "   Impact: ~37% of all flood events (per 18/06 baseline)"
    echo "   Fix: Add 'no status message from sub-agent' rule + stagger dispatches"
    echo "   Effort: 10 min (workflow update)"
    echo ""
    RC2_CONFIRMED=1
else
    echo "🟢 RC2: Sub-agent parallel burst — NOT DETECTED (peak $PEAK_DAILY < 200/day)"
    echo ""
fi

# RC3: Low retry count
SPECIFIC_2=$(grep "Failed to deliver response after 2 retries" "$LOG_FILE" | wc -l)
if [[ $SPECIFIC_2 -gt 0 ]]; then
    echo "🔴 RC3: Low retry count — CONFIRMED"
    echo "   Evidence: $SPECIFIC_2 'after 2 retries' events (retries too low)"
    echo "   Impact: ~30 user-visible 'Failed to deliver' events"
    echo "   Fix: Bump retry count 2 → 4 in base.py"
    echo "   Effort: 5 min (code change)"
    echo ""
    RC3_CONFIRMED=1
else
    echo "🟢 RC3: Low retry count — NOT DETECTED"
    echo ""
fi

# RC4: No jitter
QUICK_RETRIES=$(grep -E "retrying in [0-4]\.[0-9]s:.*Flood control" "$LOG_FILE" | wc -l)
if [[ $QUICK_RETRIES -gt 0 ]]; then
    echo "🟡 RC4: No jitter / backoff — LIKELY"
    echo "   Evidence: $QUICK_RETRIES 'retrying in <5s' events (Telegram wait 20-30s)"
    echo "   Impact: amplifies RC1+RC2+RC3"
    echo "   Fix: Add exponential backoff + jitter in base.py"
    echo "   Effort: 10 min (code change)"
    echo ""
    RC4_CONFIRMED=1
else
    echo "🟢 RC4: No jitter — NOT DETECTED"
    echo ""
fi

# Summary
echo "═══════════════════════════════════════════════════════"
echo "📋 Recommended Fix Sequence"
echo "═══════════════════════════════════════════════════════"
echo ""

TOTAL_CONFIRMED=$((RC1_CONFIRMED + RC2_CONFIRMED + RC3_CONFIRMED + RC4_CONFIRMED))

if [[ $TOTAL_CONFIRMED -eq 0 ]]; then
    echo "✅ No flood issues detected. User may be reporting transient issue."
    echo "   Try checking logs for specific timeframe of user's complaint."
    exit 0
fi

if [[ $RC1_CONFIRMED -eq 1 ]]; then
    echo "1️⃣  PRIORITY 1 (HIGHEST IMPACT, EASIEST): Apply RC1 fix"
    echo "   Add to ~/.hermes/config.yaml:"
    echo "   platforms:"
    echo "     telegram:"
    echo "       extra:"
    echo "         rich_messages: false"
fi

if [[ $RC2_CONFIRMED -eq 1 ]]; then
    echo ""
    echo "2️⃣  PRIORITY 2: Apply RC2 fix"
    echo "   Add rule to ~/.hermes/profiles/_shared/sub-agent-workflow.md:"
    echo "   'KHÔNG gửi status message từ sub-agent. Return summary only.'"
fi

if [[ $RC3_CONFIRMED -eq 1 ]]; then
    echo ""
    echo "3️⃣  PRIORITY 3: Apply RC3 fix"
    echo "   Edit ~/.hermes/hermes-agent/gateway/platforms/base.py:"
    echo "   Change: max_retries = 2  →  max_retries = 4"
fi

if [[ $RC4_CONFIRMED -eq 1 ]]; then
    echo ""
    echo "4️⃣  PRIORITY 4: Apply RC4 fix"
    echo "   Add exponential + jitter backoff in base.py (see references/hermes-gateway-retry-config.md)"
fi

echo ""
echo "═══════════════════════════════════════════════════════"
echo "💡 All 4 fixes combined: ~99% flood reduction (18/06 baseline)"
echo "═══════════════════════════════════════════════════════"
