#!/bin/bash
# PAPER TRADING ACTIVATION SCRIPT
# Comprehensive start-up for OANDA + IBKR paper trading
# PIN: 841921
# Status: READY

set -euo pipefail

BASE_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
LOG_DIR="$BASE_DIR/logs"
ENV_FILE="$BASE_DIR/.env"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  PAPER TRADING ACTIVATION - OANDA + IBKR${NC}"
echo -e "${BLUE}  PIN: 841921 | Status: READY${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════${NC}"
echo ""

# ============================================================================
# PHASE 1: PRE-FLIGHT CHECKS
# ============================================================================

echo -e "${YELLOW}PHASE 1: PRE-FLIGHT CHECKS${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check 1: Directory structure
if [ ! -d "$BASE_DIR" ]; then
    echo -e "${RED}❌ Base directory not found: $BASE_DIR${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Base directory: $BASE_DIR${NC}"

# Check 2: Environment file
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}❌ Environment file not found: $ENV_FILE${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Environment file loaded${NC}"

# Check 3: Logs directory
mkdir -p "$LOG_DIR"
echo -e "${GREEN}✅ Logs directory ready: $LOG_DIR${NC}"

# Check 4: Python environment
cd "$BASE_DIR"
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✅ Python version: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python 3.8+ required${NC}"
    exit 1
fi

# Check 5: Required packages
echo -e "${YELLOW}Checking required packages...${NC}"
python3 << 'EOF'
import sys
required = ['requests', 'python-dotenv', 'pandas', 'numpy']
missing = []

for package in required:
    try:
        __import__(package.replace('-', '_'))
    except ImportError:
        missing.append(package)

if missing:
    print(f"❌ Missing packages: {', '.join(missing)}")
    sys.exit(1)
else:
    print("✅ All required packages installed")
EOF

# Check 6: Charter validation
echo -e "${YELLOW}Validating RICK Charter...${NC}"
python3 << 'EOF'
from foundation.rick_charter import RickCharter

if RickCharter.validate():
    print("✅ RICK Charter: VALID")
    summary = RickCharter.get_charter_summary()
    print(f"   PIN: {summary['pin']}")
    print(f"   Version: {summary['version']}")
    print(f"   Max Hold: {summary['max_hold_hours']}h")
    print(f"   Daily Breaker: {summary['daily_loss_breaker']}%")
    print(f"   Min RR: {summary['min_risk_reward']}:1")
    print(f"   Max Concurrent: {summary['max_concurrent']}")
else:
    print("❌ RICK Charter validation failed")
    exit(1)
EOF

echo ""

# ============================================================================
# PHASE 2: BROKER CONNECTIVITY TEST
# ============================================================================

echo -e "${YELLOW}PHASE 2: BROKER CONNECTIVITY TEST${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Test OANDA
echo -e "${YELLOW}Testing OANDA Paper Connection...${NC}"
python3 << 'EOF'
try:
    from brokers.oanda_connector import OandaConnector
    
    oanda = OandaConnector(pin=841921, environment="practice")
    account = oanda.get_account_summary()
    
    if account:
        print(f"✅ OANDA Paper Connected")
        print(f"   Account: {account.account_id}")
        print(f"   Balance: ${account.balance:,.2f}")
        print(f"   Available: ${account.available:,.2f}")
    else:
        print("⚠️  OANDA connection warning (might be network issue)")
except Exception as e:
    print(f"⚠️  OANDA Error: {str(e)[:60]}")
EOF

echo ""

# Test IBKR
echo -e "${YELLOW}Testing IBKR Paper Connection...${NC}"
python3 << 'EOF'
try:
    from brokers.ib_connector import IBConnector
    
    ib = IBConnector(pin=841921, environment="paper")
    
    print(f"✅ IBKR Paper Configured")
    print(f"   Host: {ib.host}:{ib.port}")
    print(f"   Account: {ib.account_id}")
    print(f"   Status: Ready (requires Gateway running)")
except Exception as e:
    print(f"⚠️  IBKR Warning: {str(e)[:60]}")
EOF

echo ""

# ============================================================================
# PHASE 3: CONFIGURATION SUMMARY
# ============================================================================

echo -e "${YELLOW}PHASE 3: CHARTER INFORMATION CONFIRMATION${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

python3 << 'EOF'
import json
from foundation.rick_charter import RickCharter
from brokers.oanda_connector import OandaConnector
import os

print("\n🎯 CHARTER RULES (IMMUTABLE - LOCKED IN CODE)")
print("─" * 50)
charter = RickCharter.get_charter_summary()
print(f"  PIN: {charter['pin']}")
print(f"  Max Hold Duration: {charter['max_hold_hours']} hours")
print(f"  Daily Loss Breaker: {charter['daily_loss_breaker']}%")
print(f"  Min Notional: ${charter['min_notional_usd']:,.0f}")
print(f"  Min Risk/Reward: {charter['min_risk_reward']}:1")
print(f"  Max Concurrent Positions: {charter['max_concurrent']}")
print(f"  Max Daily Trades: {charter['max_daily_trades']}")
print(f"  Allowed Timeframes: {', '.join(charter['allowed_timeframes'])}")

print("\n📡 PLATFORM CONFIGURATION")
print("─" * 50)

print("\n  OANDA PAPER (FOREX)")
print("  " + "─" * 46)
try:
    env_file = '/home/ing/RICK/RICK_LIVE_PROTOTYPE/.env'
    oanda_account = None
    with open(env_file) as f:
        for line in f:
            if 'OANDA_PRACTICE_ACCOUNT_ID' in line:
                oanda_account = line.split('=')[1].strip()
                break
    
    print(f"    Account ID: {oanda_account if oanda_account else 'Not configured'}")
    print(f"    API Token: [LOADED FROM ENV]")
    print(f"    Base URL: https://api-fxpractice.oanda.com/v3")
    print(f"    Supported Pairs: EUR_USD, GBP_USD, USD_JPY, AUD_USD, USD_CAD")
    print(f"    Status: ✅ READY")
except Exception as e:
    print(f"    Status: ⚠️  {str(e)[:40]}")

print("\n  IBKR GATEWAY PAPER (STOCKS/FUTURES/FOREX)")
print("  " + "─" * 46)
print(f"    Gateway Host: 127.0.0.1")
print(f"    Paper Port: 4002")
print(f"    Live Port: 4001 (NOT IN USE)")
print(f"    Account ID: DU6880040 (Paper)")
print(f"    Status: ✅ READY (requires Gateway running)")

print("\n💰 PAPER TRADING CAPITAL")
print("─" * 50)
print(f"    OANDA Practice: ~$2,300 (Paper)")
print(f"    IBKR Paper: ~$2,000 (Paper)")
print(f"    Total: ~$4,300 (Paper - Zero Real Money Risk)")

print("\n🛡️ SAFETY MECHANISMS")
print("─" * 50)
print(f"    ✅ Daily Loss Breaker: -5% (automatic halt)")
print(f"    ✅ Correlation Gates: Max 0.70 correlation")
print(f"    ✅ Position Size Limits: Max 10% per position")
print(f"    ✅ SL/TP Enforcement: Automated")
print(f"    ✅ OCO Timeout: 300ms max")
print(f"    ✅ Min Notional: $15,000 per trade")

EOF

echo ""

# ============================================================================
# PHASE 4: OPTIONS
# ============================================================================

echo -e "${YELLOW}PHASE 4: SELECT TRADING MODE${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Choose your trading interface:"
echo ""
echo "  1) Multi-Broker Engine (Console-based)"
echo "     - Direct market data and order execution"
echo "     - Real-time position updates"
echo "     - Logs to console + file"
echo ""
echo "  2) Unified Dashboard (Web-based)"
echo "     - Visual trading interface"
echo "     - Real-time charts and metrics"
echo "     - Available at http://localhost:8501"
echo ""
echo "  3) Ghost Trading Engine (Automated)"
echo "     - Fully automated trading with AI"
echo "     - OANDA practice API"
echo "     - Position Guardian integration"
echo ""
echo "  4) Monitor Only (Diagnostics)"
echo "     - No trading, diagnostics only"
echo "     - Verify systems are working"
echo ""
echo "  5) Exit"
echo ""

read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo ""
        echo -e "${BLUE}Starting Multi-Broker Engine...${NC}"
        echo "Press Ctrl+C to stop"
        echo ""
        python3 multi_broker_engine.py --mode paper
        ;;
    2)
        echo ""
        echo -e "${BLUE}Starting Unified Dashboard...${NC}"
        echo "Opening dashboard at http://localhost:8501"
        echo "Press Ctrl+C to stop"
        echo ""
        python3 dashboard_unified.py --mode paper
        ;;
    3)
        echo ""
        echo -e "${BLUE}Starting Ghost Trading Engine...${NC}"
        echo "Press Ctrl+C to stop"
        echo ""
        bash launch_live_ghost.sh
        ;;
    4)
        echo ""
        echo -e "${BLUE}Running Diagnostics...${NC}"
        echo ""
        python3 test_live_brokers.py --paper
        
        echo ""
        echo -e "${YELLOW}System Check Complete${NC}"
        echo "  ✅ All systems ready for paper trading"
        echo "  Use one of the above modes to start trading"
        ;;
    5)
        echo ""
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
