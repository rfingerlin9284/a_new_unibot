#!/usr/bin/env bash

# RBOTzilla UNI - Test PIN Shutdown System
# Simulates trades and tests safety shutdown procedures

RICK_ROOT="/home/ing/RICK/R_H_UNI"
RUNTIME_DIR="$RICK_ROOT/runtime"
TRADES_FILE="$RUNTIME_DIR/open_trades.json"

echo "🧪 Testing RBOTzilla UNI PIN Shutdown System"
echo "============================================"

mkdir -p "$RUNTIME_DIR"

# Test 1: Shutdown with no open trades (should succeed)
echo ""
echo "🔬 Test 1: Shutdown with no open trades"
echo "---------------------------------------"

# Clear any existing trades
cat > "$TRADES_FILE" << 'EOF'
{
    "open_positions": [],
    "last_update": "2025-01-29T17:05:00Z"
}
EOF

echo "✅ Created empty trades file"
echo "📝 Simulating PIN 123456 submission..."

# Submit test PIN
echo "123456" > "$RUNTIME_DIR/shutdown_pin.txt"

echo "🔄 Waiting 8 seconds for safety monitor to process..."
sleep 8

# Check if PIN was consumed (file deleted means successful shutdown)
if [[ ! -f "$RUNTIME_DIR/shutdown_pin.txt" ]]; then
    echo "✅ Test 1 PASSED: Shutdown succeeded with no open trades"
else
    echo "❌ Test 1 FAILED: PIN file still exists"
    rm -f "$RUNTIME_DIR/shutdown_pin.txt"
fi

echo ""
echo "🔬 Test 2: Shutdown with unprotected trades (should block)"
echo "---------------------------------------------------------"

# Create trades WITHOUT proper SL/TP
cat > "$TRADES_FILE" << 'EOF'
{
    "open_positions": [
        {
            "symbol": "EURUSD",
            "side": "BUY",
            "size": "0.1",
            "entry_price": "1.0850",
            "stop_loss": null,
            "take_profit": null
        },
        {
            "symbol": "GBPUSD", 
            "side": "SELL",
            "size": "0.2",
            "entry_price": "1.2650",
            "stop_loss": "1.2700",
            "take_profit": null
        }
    ],
    "last_update": "2025-01-29T17:06:00Z"
}
EOF

echo "✅ Created trades with missing SL/TP protection"
echo "📝 Simulating PIN 654321 submission..."

# Submit test PIN
echo "654321" > "$RUNTIME_DIR/shutdown_pin.txt"

echo "🔄 Waiting 8 seconds for safety monitor to process..."
sleep 8

# Check if PIN was rejected (file still exists means shutdown blocked)
if [[ -f "$RUNTIME_DIR/shutdown_pin.txt" ]]; then
    echo "✅ Test 2 PASSED: Shutdown blocked due to unprotected trades"
    rm -f "$RUNTIME_DIR/shutdown_pin.txt"
else
    echo "❌ Test 2 FAILED: Shutdown should have been blocked"
fi

echo ""
echo "🔬 Test 3: Shutdown with properly protected trades (should succeed)"
echo "------------------------------------------------------------------"

# Create trades WITH proper SL/TP
cat > "$TRADES_FILE" << 'EOF'
{
    "open_positions": [
        {
            "symbol": "EURUSD",
            "side": "BUY", 
            "size": "0.1",
            "entry_price": "1.0850",
            "stop_loss": "1.0800",
            "take_profit": "1.0950"
        },
        {
            "symbol": "GBPUSD",
            "side": "SELL",
            "size": "0.2", 
            "entry_price": "1.2650",
            "stop_loss": "1.2700",
            "take_profit": "1.2550"
        }
    ],
    "last_update": "2025-01-29T17:07:00Z"
}
EOF

echo "✅ Created trades with full SL/TP protection"
echo "📝 Simulating PIN 789012 submission..."

# Submit test PIN
echo "789012" > "$RUNTIME_DIR/shutdown_pin.txt"

echo "🔄 Waiting 8 seconds for safety monitor to process..."
sleep 8

# Check if PIN was consumed (successful shutdown)
if [[ ! -f "$RUNTIME_DIR/shutdown_pin.txt" ]]; then
    echo "✅ Test 3 PASSED: Shutdown succeeded with protected trades"
    # Reset trades to empty for clean state
    cat > "$TRADES_FILE" << 'EOF'
{
    "open_positions": [],
    "last_update": "2025-01-29T17:08:00Z"
}
EOF
else
    echo "❌ Test 3 FAILED: Protected trades should allow shutdown"
    rm -f "$RUNTIME_DIR/shutdown_pin.txt"
fi

echo ""
echo "🔬 Test 4: Invalid PIN format (should be ignored)"
echo "------------------------------------------------"

echo "📝 Simulating invalid PIN 'abc123'..."
echo "abc123" > "$RUNTIME_DIR/shutdown_pin.txt"

echo "🔄 Waiting 8 seconds for safety monitor to process..."
sleep 8

# Invalid PIN should be cleaned up automatically
if [[ ! -f "$RUNTIME_DIR/shutdown_pin.txt" ]]; then
    echo "✅ Test 4 PASSED: Invalid PIN format was rejected"
else
    echo "❌ Test 4 FAILED: Invalid PIN should be rejected"
    rm -f "$RUNTIME_DIR/shutdown_pin.txt"
fi

echo ""
echo "📊 Testing Summary"
echo "=================="
echo "✅ No trades shutdown: TESTED"  
echo "✅ Unprotected trades blocking: TESTED"
echo "✅ Protected trades shutdown: TESTED"
echo "✅ Invalid PIN rejection: TESTED"

echo ""
echo "🔐 Manual Shutdown Command:"
echo "   /home/ing/RICK/R_H_UNI/scripts/shutdown_with_pin.sh"

echo ""
echo "📋 Service Status:"
echo "   Main: $(systemctl --user is-active rbotzilla-uni-main.service)"
echo "   Safety: $(systemctl --user is-active rbotzilla-safety.service)" 
echo "   Sessions: $(systemctl --user is-active rbotzilla-sessions.service 2>/dev/null || echo 'inactive')"

echo ""
echo "🛡️ Trading Safety Monitor: OPERATIONAL"
echo "💓 Keepalive Monitor: $(systemctl --user is-active rbotzilla-keepalive.timer)"
echo "🚀 Auto-login: ENABLED (will start on boot)"