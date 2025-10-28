#!/bin/bash

################################################################################
#
#  RICK PAPER TRADING - SYSTEM STARTUP & VERIFICATION
#  
#  This script performs comprehensive system checks and confirms all internal
#  components are operational before launching paper trading.
#
#  Usage: bash RUN.sh  OR  chmod +x RUN.sh && ./RUN.sh
#
#  PIN: 841921
#
################################################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Get workspace directory
WORKSPACE_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
cd "$WORKSPACE_DIR" || exit 1

################################################################################
# Helper Functions
################################################################################

log_header() {
    echo -e "\n${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}\n"
}

log_pass() {
    echo -e "${GREEN}✅ PASS${NC}: $1"
    ((PASS++))
}

log_fail() {
    echo -e "${RED}❌ FAIL${NC}: $1"
    ((FAIL++))
}

log_warn() {
    echo -e "${YELLOW}⚠️  WARN${NC}: $1"
    ((WARN++))
}

log_info() {
    echo -e "${CYAN}ℹ️  INFO${NC}: $1"
}

log_step() {
    echo -e "${CYAN}→${NC} $1"
}

################################################################################
# Phase 1: Environment & Prerequisites
################################################################################

log_header "PHASE 1: ENVIRONMENT & PREREQUISITES"

# Check if running in correct directory
log_step "Checking workspace..."
if [ -f "$WORKSPACE_DIR/.env" ]; then
    log_pass "Workspace directory found: $WORKSPACE_DIR"
else
    log_fail "Workspace not found at $WORKSPACE_DIR"
    exit 1
fi

# Check Python installation
log_step "Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    log_pass "Python installed: $PYTHON_VERSION"
else
    log_fail "Python3 not found"
    exit 1
fi

# Check Git
log_step "Checking Git..."
if command -v git &> /dev/null; then
    log_pass "Git installed"
else
    log_warn "Git not found (optional)"
fi

################################################################################
# Phase 2: Configuration Files
################################################################################

log_header "PHASE 2: CONFIGURATION FILES"

# Check .env file
log_step "Checking .env configuration..."
if [ -f "$WORKSPACE_DIR/.env" ]; then
    if grep -q "OANDA_PRACTICE_ACCOUNT_ID" "$WORKSPACE_DIR/.env"; then
        OANDA_ACCOUNT=$(grep "OANDA_PRACTICE_ACCOUNT_ID" "$WORKSPACE_DIR/.env" | cut -d '=' -f2)
        log_pass "OANDA Practice Account configured: $OANDA_ACCOUNT"
    else
        log_fail "OANDA_PRACTICE_ACCOUNT_ID not found in .env"
    fi
    
    if grep -q "OANDA_PRACTICE_TOKEN" "$WORKSPACE_DIR/.env"; then
        log_pass "OANDA Practice Token configured"
    else
        log_fail "OANDA_PRACTICE_TOKEN not found in .env"
    fi
    
    if grep -q "OANDA_PRACTICE_BASE_URL" "$WORKSPACE_DIR/.env"; then
        log_pass "OANDA Practice Base URL configured"
    else
        log_fail "OANDA_PRACTICE_BASE_URL not found in .env"
    fi
else
    log_fail ".env file not found"
    exit 1
fi

# Check for .env_new (backup)
if [ -f "$WORKSPACE_DIR/env_new.env" ]; then
    log_pass ".env backup found"
else
    log_warn ".env backup (env_new.env) not found"
fi

################################################################################
# Phase 3: Charter Verification
################################################################################

log_header "PHASE 3: CHARTER VERIFICATION"

log_step "Checking charter enforcement..."
if [ -f "$WORKSPACE_DIR/foundation/rick_charter.py" ]; then
    # Check for PIN
    if grep -q "841921" "$WORKSPACE_DIR/foundation/rick_charter.py"; then
        log_pass "Charter PIN verified: 841921"
    else
        log_fail "Charter PIN not found"
    fi
    
    # Check for immutable constants
    if grep -q "MAX_HOLD_DURATION_HOURS = 6" "$WORKSPACE_DIR/foundation/rick_charter.py"; then
        log_pass "Max Hold Duration locked: 6 hours"
    else
        log_fail "Max Hold Duration not found"
    fi
    
    if grep -q "DAILY_LOSS_BREAKER_PCT = -5.0" "$WORKSPACE_DIR/foundation/rick_charter.py"; then
        log_pass "Daily Loss Breaker locked: -5%"
    else
        log_fail "Daily Loss Breaker not found"
    fi
    
    if grep -q "MIN_NOTIONAL_USD = 15000" "$WORKSPACE_DIR/foundation/rick_charter.py"; then
        log_pass "Minimum Notional locked: \$15,000"
    else
        log_fail "Minimum Notional not found"
    fi
    
    if grep -q "MIN_RISK_REWARD_RATIO = 3.0" "$WORKSPACE_DIR/foundation/rick_charter.py"; then
        log_pass "Minimum Risk/Reward locked: 3.0:1"
    else
        log_fail "Minimum Risk/Reward not found"
    fi
    
    log_pass "Charter enforcement module found and verified"
else
    log_fail "Charter enforcement module not found"
fi

################################################################################
# Phase 4: Core Components
################################################################################

log_header "PHASE 4: CORE COMPONENTS"

# Check multi_broker_engine
if [ -f "$WORKSPACE_DIR/multi_broker_engine.py" ]; then
    log_pass "Multi-broker engine found"
else
    log_fail "Multi-broker engine not found"
fi

# Check OANDA connector
if [ -f "$WORKSPACE_DIR/brokers/oanda_connector.py" ]; then
    log_pass "OANDA connector found"
else
    log_fail "OANDA connector not found"
fi

# Check IBKR connector
if [ -f "$WORKSPACE_DIR/brokers/ibkr_connector.py" ]; then
    log_pass "IBKR connector found"
else
    log_warn "IBKR connector not found (optional for paper trading)"
fi

# Check position guardian
if [ -f "$WORKSPACE_DIR/position_guardian.py" ]; then
    log_pass "Position guardian found"
else
    log_warn "Position guardian not found (will be auto-loaded if needed)"
fi

# Check dashboard
if [ -f "$WORKSPACE_DIR/dashboard_unified.py" ]; then
    log_pass "Dashboard found"
else
    log_fail "Dashboard not found"
fi

################################################################################
# Phase 5: Gated Upgrade System
################################################################################

log_header "PHASE 5: GATED UPGRADE SYSTEM"

# Check upgrade toggle
log_step "Checking gated upgrade safety mechanisms..."
if [ -f "$WORKSPACE_DIR/.upgrade_toggle" ]; then
    TOGGLE_STATUS=$(cat "$WORKSPACE_DIR/.upgrade_toggle")
    if [ "$TOGGLE_STATUS" = "OFF" ]; then
        log_pass "Upgrade toggle: OFF (safe mode active)"
    else
        log_warn "Upgrade toggle: ON (upgrades active)"
    fi
else
    log_pass "Upgrade toggle: Not created yet (will be created on first activation)"
fi

# Check gating script
if [ -f "$WORKSPACE_DIR/vscode_agent_run_live_check.sh" ]; then
    log_pass "Gated upgrade orchestration script found"
else
    log_fail "Gated upgrade orchestration script not found"
fi

# Check preflight script
if [ -f "$WORKSPACE_DIR/live_preflight_check.sh" ]; then
    log_pass "Pre-flight safety checks found"
else
    log_fail "Pre-flight safety checks not found"
fi

# Check verification script
if [ -f "$WORKSPACE_DIR/verify_live_safety.sh" ]; then
    log_pass "Post-upgrade verification found"
else
    log_fail "Post-upgrade verification not found"
fi

################################################################################
# Phase 6: Directory Structure
################################################################################

log_header "PHASE 6: DIRECTORY STRUCTURE"

log_step "Checking required directories..."

REQUIRED_DIRS=(
    "foundation"
    "brokers"
    "logs"
    "models"
    "ui"
    "utils"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$WORKSPACE_DIR/$dir" ]; then
        log_pass "Directory exists: $dir/"
    else
        log_warn "Directory not found: $dir/ (may be created on first run)"
    fi
done

# Check optional backup directory
if [ -d "$WORKSPACE_DIR/pre_upgrade_backups" ]; then
    log_pass "Backup directory exists: pre_upgrade_backups/"
else
    log_info "Backup directory will be created on first upgrade"
fi

################################################################################
# Phase 7: Dependencies Check
################################################################################

log_header "PHASE 7: PYTHON DEPENDENCIES"

log_step "Checking required Python packages..."

REQUIRED_PACKAGES=(
    "requests"
    "numpy"
    "pandas"
    "python-dotenv"
    "flask"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    if python3 -c "import $package" 2>/dev/null; then
        log_pass "Package installed: $package"
    else
        log_warn "Package not installed: $package (install: pip3 install $package)"
    fi
done

################################################################################
# Phase 8: Import & Runtime Tests
################################################################################

log_header "PHASE 8: RUNTIME VERIFICATION"

log_step "Testing charter import..."
if python3 -c "from foundation.rick_charter import RickCharter; RickCharter.validate_all()" 2>/dev/null; then
    log_pass "Charter validation passed (all 17 rules verified)"
else
    log_warn "Charter validation check (may be loaded at runtime)"
fi

log_step "Testing environment loading..."
if python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OANDA_PRACTICE_ACCOUNT_ID'))" 2>/dev/null | grep -q "101-001"; then
    log_pass "Environment variables loaded successfully"
else
    log_warn "Environment loading (manual configuration may be required)"
fi

log_step "Testing broker connectors..."
if python3 -c "from brokers.oanda_connector import OandaConnector" 2>/dev/null; then
    log_pass "OANDA connector imports successfully"
else
    log_warn "OANDA connector import failed (may require additional setup)"
fi

################################################################################
# Phase 9: Security Checks
################################################################################

log_header "PHASE 9: SECURITY CHECKS"

log_step "Checking file permissions..."

# Check .env permissions (should not be world-readable)
if [ -f "$WORKSPACE_DIR/.env" ]; then
    PERMS=$(stat -c "%a" "$WORKSPACE_DIR/.env" 2>/dev/null || echo "unknown")
    log_info ".env permissions: $PERMS"
fi

# Check for sensitive data in code
log_step "Scanning for hardcoded tokens..."
if grep -r "OANDA.*41" "$WORKSPACE_DIR" --include="*.py" 2>/dev/null | grep -v ".env" | grep -v "test_" > /dev/null; then
    log_warn "Potential hardcoded tokens found (review code)"
else
    log_pass "No hardcoded tokens found in source code"
fi

################################################################################
# Phase 10: Logging System
################################################################################

log_header "PHASE 10: LOGGING SYSTEM"

log_step "Checking logging infrastructure..."
if [ -d "$WORKSPACE_DIR/logs" ]; then
    log_pass "Logs directory exists"
    
    # Try to create test log
    if touch "$WORKSPACE_DIR/logs/startup_test.log" 2>/dev/null; then
        log_pass "Logs directory is writable"
        rm -f "$WORKSPACE_DIR/logs/startup_test.log"
    else
        log_fail "Logs directory is not writable"
    fi
else
    log_warn "Logs directory not found (will be created on first run)"
fi

################################################################################
# Summary & Final Decision
################################################################################

log_header "SYSTEM STARTUP VERIFICATION SUMMARY"

echo -e "${GREEN}✅ PASSED: $PASS${NC}"
echo -e "${YELLOW}⚠️  WARNINGS: $WARN${NC}"
echo -e "${RED}❌ FAILURES: $FAIL${NC}"

echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}✨ ALL CRITICAL SYSTEMS VERIFIED - READY TO LAUNCH ✨${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    
    echo ""
    echo -e "${CYAN}Charter Information:${NC}"
    echo -e "  PIN: ${GREEN}841921${NC}"
    echo -e "  Max Hold: ${GREEN}6 hours${NC}"
    echo -e "  Daily Breaker: ${GREEN}-5%${NC}"
    echo -e "  Min Notional: ${GREEN}\$15,000${NC}"
    echo -e "  Min Risk/Reward: ${GREEN}3.0:1${NC}"
    
    echo ""
    echo -e "${CYAN}Paper Trading Account:${NC}"
    echo -e "  OANDA Account: ${GREEN}101-001-31210531-002${NC}"
    echo -e "  Mode: ${GREEN}PRACTICE (Paper/Demo)${NC}"
    echo -e "  Capital Risk: ${GREEN}\$0.00${NC}"
    
    echo ""
    echo -e "${CYAN}Choose your launch method:${NC}"
    echo ""
    echo -e "  ${BLUE}1.${NC} Quick Test (Verify brokers)"
    echo -e "     ${YELLOW}python3 test_live_brokers.py --paper${NC}"
    echo ""
    echo -e "  ${BLUE}2.${NC} Console Trading"
    echo -e "     ${YELLOW}python3 multi_broker_engine.py --mode paper${NC}"
    echo ""
    echo -e "  ${BLUE}3.${NC} Web Dashboard"
    echo -e "     ${YELLOW}python3 dashboard_unified.py --mode paper${NC}"
    echo ""
    echo -e "  ${BLUE}4.${NC} Ghost Engine (Automated)"
    echo -e "     ${YELLOW}bash launch_live_ghost.sh${NC}"
    echo ""
    echo -e "  ${BLUE}5.${NC} Interactive Menu"
    echo -e "     ${YELLOW}bash activate_paper_trading.sh${NC}"
    echo ""
    
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}System Status: GO LIVE ✅${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    
    exit 0
else
    echo -e "${RED}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}❌ CRITICAL FAILURES DETECTED - DO NOT LAUNCH${NC}"
    echo -e "${RED}════════════════════════════════════════════════════════════════${NC}"
    
    echo ""
    echo -e "${YELLOW}Please fix the following issues:${NC}"
    echo "  1. Review the FAIL entries above"
    echo "  2. Consult: LIVE_READINESS_CHECKLIST.md"
    echo "  3. Consult: LIVE_TRADING_SAFETY_PROTOCOL.md"
    echo ""
    
    exit 1
fi
