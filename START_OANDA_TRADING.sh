#!/bin/bash
# ONE-CLICK OANDA PAPER TRADING STARTUP
# PIN: 841921 | OANDA Practice Account: 101-001-31210531-002
# Capital: $1,970.79 (Paper Money)

set -e

echo "════════════════════════════════════════════════════════════════"
echo "  🤖 RBOTZILLA OANDA PAPER TRADING - ONE-CLICK STARTUP"
echo "  PIN: 841921 | Account: 101-001-31210531-002"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Step 1: Check if Ollama is running (for Rick's narration)
echo "🔍 Step 1/4: Checking Ollama (Rick's AI Narration)..."
if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Ollama is running"
else
    echo "   ⚠️  Ollama not running - starting it..."
    nohup ollama serve > /tmp/ollama.log 2>&1 &
    sleep 3
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
        echo "   ✅ Ollama started successfully"
    else
        echo "   ⚠️  Ollama failed to start - narration will be disabled"
    fi
fi

# Step 2: Check OANDA credentials
echo ""
echo "🔍 Step 2/4: Verifying OANDA credentials..."
if [ -f "env_new.env" ]; then
    OANDA_ACCOUNT=$(grep "OANDA_PRACTICE_ACCOUNT_ID" env_new.env | cut -d'=' -f2)
    if [ ! -z "$OANDA_ACCOUNT" ]; then
        echo "   ✅ OANDA Account: $OANDA_ACCOUNT"
    else
        echo "   ❌ OANDA credentials not found in env_new.env"
        exit 1
    fi
else
    echo "   ❌ env_new.env not found"
    exit 1
fi

# Step 3: Check if trading engine is already running
echo ""
echo "🔍 Step 3/4: Checking for existing trading processes..."
if pgrep -f "oanda_trading_engine.py" > /dev/null; then
    echo "   ⚠️  Trading engine is already running!"
    echo ""
    read -p "   Stop existing and restart? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "   🛑 Stopping existing trading engine..."
        pkill -f "oanda_trading_engine.py" || true
        sleep 2
        echo "   ✅ Stopped"
    else
        echo "   ℹ️  Keeping existing process running"
        exit 0
    fi
else
    echo "   ✅ No existing processes"
fi

# Step 4: Start the trading engine
echo ""
echo "🚀 Step 4/4: Starting OANDA Paper Trading Engine..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Run in foreground so you can see the output
python3 oanda_trading_engine.py --env practice

# If user stops with Ctrl+C, show summary
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  🛑 Trading engine stopped"
echo "════════════════════════════════════════════════════════════════"
