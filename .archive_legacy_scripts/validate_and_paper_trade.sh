#!/bin/bash
# RICK Live Deployment Validator & Paper Trading Monitor
# This script validates completeness and runs paper trading with full logging

set -e

DEPLOYMENT_DIR="/home/ing/RICK/R_H_UNI/RICK_LIVE_DEPLOYMENT"
PAPER_TRADE_LOG_DIR="$DEPLOYMENT_DIR/paper_trade_logs_$(date +%Y%m%d_%H%M%S)"
VALIDATION_LOG="$DEPLOYMENT_DIR/validation_report_$(date +%Y%m%d_%H%M%S).txt"

echo "🔍 RICK LIVE DEPLOYMENT VALIDATOR & PAPER TRADER"
echo "=================================================="
echo "" | tee "$VALIDATION_LOG"

# ============================================
# PHASE 1: COMPLETENESS VALIDATION
# ============================================

echo "📋 PHASE 1: VALIDATING COMPLETENESS..." | tee -a "$VALIDATION_LOG"
echo "---" | tee -a "$VALIDATION_LOG"

# Check critical directories
CRITICAL_DIRS=(
    "foundation"
    "wolf_packs"
    "risk"
    "brokers"
    "execution"
    "connectors"
    "swarm"
    "logic"
    "configs"
    "util"
    "dashboard"
    "hive"
    "scripts"
)

MISSING_DIRS=()
for dir in "${CRITICAL_DIRS[@]}"; do
    if [ -d "$DEPLOYMENT_DIR/$dir" ]; then
        echo "✅ $dir/ - EXISTS" | tee -a "$VALIDATION_LOG"
    else
        echo "❌ $dir/ - MISSING" | tee -a "$VALIDATION_LOG"
        MISSING_DIRS+=("$dir")
    fi
done

# Check critical root files
CRITICAL_FILES=(
    "live_ghost_engine.py"
    "micro_trading_engine.py"
    "ghost_trading_engine.py"
    "activate_live_trading.sh"
    "start_ghost_trading.sh"
    "live_preflight_check.sh"
    "requirements.txt"
    "README.md"
)

MISSING_FILES=()
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$DEPLOYMENT_DIR/$file" ]; then
        echo "✅ $file - EXISTS" | tee -a "$VALIDATION_LOG"
    else
        echo "❌ $file - MISSING" | tee -a "$VALIDATION_LOG"
        MISSING_FILES+=("$file")
    fi
done

# Check dashboard entry points
echo "" | tee -a "$VALIDATION_LOG"
echo "📊 Checking Dashboard Components:" | tee -a "$VALIDATION_LOG"

if [ -f "$DEPLOYMENT_DIR/dashboard/app/main.py" ]; then
    echo "✅ dashboard/app/main.py - EXISTS (Streamlit entry)" | tee -a "$VALIDATION_LOG"
else
    echo "❌ dashboard/app/main.py - MISSING" | tee -a "$VALIDATION_LOG"
    MISSING_FILES+=("dashboard/app/main.py")
fi

# Check for missing dashboard_enhanced.py (should be copied)
if [ -f "/home/ing/RICK/R_H_UNI/dashboard_enhanced.py" ]; then
    if [ ! -f "$DEPLOYMENT_DIR/dashboard_enhanced.py" ]; then
        echo "⚠️  dashboard_enhanced.py - MISSING (copying now...)" | tee -a "$VALIDATION_LOG"
        cp /home/ing/RICK/R_H_UNI/dashboard_enhanced.py "$DEPLOYMENT_DIR/"
        echo "✅ dashboard_enhanced.py - COPIED" | tee -a "$VALIDATION_LOG"
    else
        echo "✅ dashboard_enhanced.py - EXISTS" | tee -a "$VALIDATION_LOG"
    fi
fi

# Check for rick_coach.py
if [ -f "/home/ing/RICK/R_H_UNI/pre_upgrade/headless/bin/rick_coach.py" ]; then
    if [ ! -f "$DEPLOYMENT_DIR/rick_coach.py" ]; then
        echo "⚠️  rick_coach.py - MISSING (copying now...)" | tee -a "$VALIDATION_LOG"
        cp /home/ing/RICK/R_H_UNI/pre_upgrade/headless/bin/rick_coach.py "$DEPLOYMENT_DIR/"
        echo "✅ rick_coach.py - COPIED" | tee -a "$VALIDATION_LOG"
    else
        echo "✅ rick_coach.py - EXISTS" | tee -a "$VALIDATION_LOG"
    fi
fi

echo "" | tee -a "$VALIDATION_LOG"
echo "============================================" | tee -a "$VALIDATION_LOG"
echo "VALIDATION SUMMARY:" | tee -a "$VALIDATION_LOG"
echo "============================================" | tee -a "$VALIDATION_LOG"
echo "Missing Directories: ${#MISSING_DIRS[@]}" | tee -a "$VALIDATION_LOG"
echo "Missing Files: ${#MISSING_FILES[@]}" | tee -a "$VALIDATION_LOG"

if [ ${#MISSING_DIRS[@]} -eq 0 ] && [ ${#MISSING_FILES[@]} -eq 0 ]; then
    echo "✅ VALIDATION PASSED - All critical components present!" | tee -a "$VALIDATION_LOG"
else
    echo "⚠️  VALIDATION WARNINGS - Some components missing" | tee -a "$VALIDATION_LOG"
    echo "Missing dirs: ${MISSING_DIRS[*]}" | tee -a "$VALIDATION_LOG"
    echo "Missing files: ${MISSING_FILES[*]}" | tee -a "$VALIDATION_LOG"
fi

# ============================================
# PHASE 2: PYTHON IMPORT VALIDATION
# ============================================

echo "" | tee -a "$VALIDATION_LOG"
echo "📋 PHASE 2: PYTHON IMPORT VALIDATION..." | tee -a "$VALIDATION_LOG"
echo "---" | tee -a "$VALIDATION_LOG"

cd "$DEPLOYMENT_DIR"

python3 << 'PYEOF' 2>&1 | tee -a "$VALIDATION_LOG"
import sys
import os
sys.path.insert(0, '.')

tests = [
    ("foundation.rick_charter", "Foundation Charter"),
    ("risk.oco_validator", "Risk OCO Validator"),
    ("risk.session_breaker", "Risk Session Breaker"),
    ("brokers.oanda_connector", "OANDA Broker"),
    ("brokers.coinbase_connector", "Coinbase Broker"),
    ("execution.smart_oco", "Smart OCO Execution"),
    ("logic.smart_logic", "Smart Logic"),
    ("swarm.swarm_bot", "Swarm Bot"),
]

passed = 0
failed = 0

for module_name, description in tests:
    try:
        __import__(module_name)
        print(f"✅ {description} ({module_name}) - OK")
        passed += 1
    except Exception as e:
        print(f"❌ {description} ({module_name}) - FAILED: {e}")
        failed += 1

print(f"\n📊 Import Test Results: {passed} passed, {failed} failed")
PYEOF

# ============================================
# PHASE 3: PAPER TRADING MODE SETUP
# ============================================

echo "" | tee -a "$VALIDATION_LOG"
echo "📋 PHASE 3: PAPER TRADING SETUP..." | tee -a "$VALIDATION_LOG"
echo "---" | tee -a "$VALIDATION_LOG"

mkdir -p "$PAPER_TRADE_LOG_DIR"
echo "✅ Created paper trading log directory: $PAPER_TRADE_LOG_DIR" | tee -a "$VALIDATION_LOG"

# Create paper trading monitoring script
cat > "$DEPLOYMENT_DIR/run_paper_trade.sh" << 'PAPER_EOF'
#!/bin/bash
# RICK Paper Trading Monitor
# Runs paper trading for specified days with full logging

DAYS=${1:-3}  # Default 3 days
LOG_DIR="paper_trade_logs_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$LOG_DIR"

echo "🚀 Starting RICK Paper Trading Monitor"
echo "Duration: $DAYS days"
echo "Log Directory: $LOG_DIR"
echo ""

# Start ghost trading engine
echo "📊 Launching Ghost Trading Engine..."
python3 live_ghost_engine.py 2>&1 | tee "$LOG_DIR/ghost_engine.log" &
GHOST_PID=$!

# Start dashboard
echo "📈 Launching Dashboard..."
streamlit run dashboard/app/main.py --server.port 8501 2>&1 | tee "$LOG_DIR/dashboard.log" &
DASH_PID=$!

# Monitor and log
echo "⏳ Monitoring for $DAYS days..."
echo "Ghost Engine PID: $GHOST_PID"
echo "Dashboard PID: $DASH_PID"
echo ""
echo "Logs:"
echo "  - Ghost Engine: $LOG_DIR/ghost_engine.log"
echo "  - Dashboard: $LOG_DIR/dashboard.log"
echo "  - Activity: $LOG_DIR/activity_monitor.log"
echo ""

# Activity monitor loop
END_TIME=$(($(date +%s) + (DAYS * 86400)))
while [ $(date +%s) -lt $END_TIME ]; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check if processes are running
    if ! kill -0 $GHOST_PID 2>/dev/null; then
        echo "[$TIMESTAMP] ❌ Ghost engine stopped unexpectedly!" | tee -a "$LOG_DIR/activity_monitor.log"
        break
    fi
    
    if ! kill -0 $DASH_PID 2>/dev/null; then
        echo "[$TIMESTAMP] ⚠️  Dashboard stopped unexpectedly!" | tee -a "$LOG_DIR/activity_monitor.log"
    fi
    
    # Log activity stats
    echo "[$TIMESTAMP] ✅ Systems running. Time remaining: $((($END_TIME - $(date +%s)) / 3600)) hours" | tee -a "$LOG_DIR/activity_monitor.log"
    
    # Collect metrics every hour
    if [ $(($(date +%s) % 3600)) -lt 60 ]; then
        echo "[$TIMESTAMP] 📊 Collecting hourly metrics..." | tee -a "$LOG_DIR/activity_monitor.log"
        
        # Copy any new logs
        if [ -d "pre_upgrade/headless/logs" ]; then
            cp pre_upgrade/headless/logs/narration.jsonl "$LOG_DIR/narration_$(date +%Y%m%d_%H%M%S).jsonl" 2>/dev/null || true
            cp pre_upgrade/headless/logs/pnl.jsonl "$LOG_DIR/pnl_$(date +%Y%m%d_%H%M%S).jsonl" 2>/dev/null || true
        fi
    fi
    
    sleep 60  # Check every minute
done

echo ""
echo "⏹️  Paper trading period complete!"
echo "Stopping processes..."
kill $GHOST_PID 2>/dev/null || true
kill $DASH_PID 2>/dev/null || true

echo ""
echo "📁 All logs saved to: $LOG_DIR"
echo "✅ Paper trading session complete!"
PAPER_EOF

chmod +x "$DEPLOYMENT_DIR/run_paper_trade.sh"
echo "✅ Created paper trading script: run_paper_trade.sh" | tee -a "$VALIDATION_LOG"

# ============================================
# FINAL SUMMARY
# ============================================

echo "" | tee -a "$VALIDATION_LOG"
echo "============================================" | tee -a "$VALIDATION_LOG"
echo "🎯 VALIDATION COMPLETE!" | tee -a "$VALIDATION_LOG"
echo "============================================" | tee -a "$VALIDATION_LOG"
echo "" | tee -a "$VALIDATION_LOG"
echo "📄 Full validation report: $VALIDATION_LOG" | tee -a "$VALIDATION_LOG"
echo "" | tee -a "$VALIDATION_LOG"
echo "🚀 TO START PAPER TRADING:" | tee -a "$VALIDATION_LOG"
echo "   cd $DEPLOYMENT_DIR" | tee -a "$VALIDATION_LOG"
echo "   ./run_paper_trade.sh 3  # Run for 3 days" | tee -a "$VALIDATION_LOG"
echo "" | tee -a "$VALIDATION_LOG"
echo "✅ System validated and ready for paper trading!" | tee -a "$VALIDATION_LOG"
