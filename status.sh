#!/bin/bash
# Quick status check for OANDA trading system

echo "════════════════════════════════════════════════════════════════"
echo "  🤖 RBOTZILLA OANDA TRADING - SYSTEM STATUS"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check Ollama
echo "🔍 Ollama (Rick's AI Narration):"
if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Running"
else
    echo "   ❌ Not running - Rick's narration will be disabled"
    echo "      Start with: ollama serve &"
fi

# Check OANDA credentials
echo ""
echo "🔍 OANDA Credentials:"
if [ -f "env_new.env" ]; then
    ACCOUNT=$(grep "OANDA_PRACTICE_ACCOUNT_ID" env_new.env | cut -d'=' -f2)
    echo "   ✅ Account: $ACCOUNT"
    echo "   ✅ Credentials loaded from: env_new.env"
else
    echo "   ❌ env_new.env not found"
fi

# Check trading processes
echo ""
echo "🔍 Trading Processes:"
if pgrep -f "oanda_trading_engine.py" > /dev/null; then
    PID=$(pgrep -f "oanda_trading_engine.py")
    echo "   ✅ Trading engine RUNNING (PID: $PID)"
    echo "      Stop with: pkill -f oanda_trading_engine.py"
else
    echo "   ⏸️  No trading engine running"
    echo "      Start with: ./START_OANDA_TRADING.sh"
fi

# Check startup script
echo ""
echo "🔍 Startup Files:"
if [ -f "START_OANDA_TRADING.sh" ] && [ -x "START_OANDA_TRADING.sh" ]; then
    echo "   ✅ START_OANDA_TRADING.sh (executable)"
else
    echo "   ⚠️  START_OANDA_TRADING.sh not found or not executable"
fi

if [ -f ".vscode/tasks.json" ]; then
    echo "   ✅ .vscode/tasks.json (VS Code tasks configured)"
else
    echo "   ⚠️  .vscode/tasks.json not found"
fi

# Charter info
echo ""
echo "🔍 Charter Configuration:"
echo "   PIN: 841921"
echo "   Min Notional: $15,000 (IMMUTABLE)"
echo "   Min R:R: 3.2:1"
echo "   Max Daily Loss: 5%"
echo "   Max Positions: 3"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📖 Quick Commands:"
echo "   Start Trading:  ./START_OANDA_TRADING.sh"
echo "   Check Balance:  python3 canary_oanda_connector.py"
echo "   Stop Trading:   pkill -f oanda_trading_engine.py"
echo "   View Logs:      tail -f narration.jsonl"
echo ""
echo "📖 VS Code: Ctrl+Shift+B (or Ctrl+Shift+P → Tasks: Run Task)"
echo ""
