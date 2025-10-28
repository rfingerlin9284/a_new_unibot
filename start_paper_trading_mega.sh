#!/usr/bin/env bash
#
# Start Paper Trading with MEGA PROMPT Instrumentation
# PIN: 841921 | Profile: Non-HFT (M15-H1) with hardened narration
#
set -euo pipefail

cd "$(dirname "$0")"

echo "🎯 Starting Paper Trading with MEGA PROMPT Instrumentation..."
echo "   Profile: Non-HFT (H1 timeframe)"
echo "   Narration: Hardened JSONL queue"
echo "   Events: PACK_ROUTED, HEDGE_ON/OFF, TRADE_BLOCKED"
echo ""

# Load environment (extract only OANDA vars)
if [ -f .env ]; then
    export $(grep "^OANDA" .env | xargs)
    # Map practice vars to expected names
    export OANDA_API_KEY="${OANDA_PRACTICE_TOKEN}"
    export OANDA_ACCOUNT_ID="${OANDA_PRACTICE_ACCOUNT_ID}"
    export OANDA_API_URL="https://api-fxpractice.oanda.com/v3"
    # Ensure paper-friendly min notional for small accounts (can override before calling)
    export BROKER_MODE="paper"
    export PAPER_MIN_NOTIONAL_USD="${PAPER_MIN_NOTIONAL_USD:-500}"
    echo "✅ Environment loaded (OANDA practice credentials)"
else
    echo "❌ .env not found"
    exit 1
fi

# Stop any existing engines
echo "🛑 Stopping existing engines..."
pkill -f autonomous_decision_engine.py 2>/dev/null || true
pkill -f oanda_paper_trading.py 2>/dev/null || true
sleep 2

# Verify OANDA credentials
if [ -z "${OANDA_API_KEY:-}" ]; then
    echo "❌ OANDA_API_KEY not set"
    exit 1
fi
if [ -z "${OANDA_ACCOUNT_ID:-}" ]; then
    echo "❌ OANDA_ACCOUNT_ID not set"
    exit 1
fi

echo "✅ OANDA credentials verified"
echo ""

# Start autonomous engine with instrumentation
echo "🚀 Starting autonomous_decision_engine.py..."
nohup python3 -u autonomous_decision_engine.py >> logs/autonomous_engine.log 2>&1 &
ENGINE_PID=$!
echo $ENGINE_PID > logs/autonomous_engine.pid

sleep 3

# Verify it's running
if ps -p $ENGINE_PID > /dev/null; then
    echo "✅ Engine started (PID: $ENGINE_PID)"
    echo ""
    echo "📊 Monitor with:"
    echo "   tail -f logs/narration.jsonl"
    echo "   tail -f logs/autonomous_engine.log"
    echo "   python3 scripts/print_narration_stats.py"
    echo ""
    echo "🛑 Stop with:"
    echo "   kill $ENGINE_PID"
    echo "   # or: pkill -f autonomous_decision_engine.py"
else
    echo "❌ Engine failed to start"
    exit 1
fi
