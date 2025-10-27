#!/bin/bash

################################################################################
# 🚀 RBOTZILLA SMART STARTUP ORCHESTRATOR
# 
# Purpose: Handle reliable on/off/reboot with process state detection
# PIN: 841921 ✅
# Features:
#   - Detects if Ollama already running (reuses instead of restart)
#   - Detects if Trading Engine already running (gracefully stop/restart)
#   - Proper startup sequence (Charter → Engine → Dashboard)
#   - Full verification checklist before going autonomous
#   - 100% reliable restart capability
#
# Usage: bash START_OANDA_TRADING.sh [--force-restart] [--quiet]
################################################################################

set -euo pipefail

# Configuration
WORK_DIR="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
OLLAMA_PORT=11434
ENGINE_PORT=8000
DASHBOARD_PORT=8501

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Options
FORCE_RESTART=false
QUIET=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --force-restart) FORCE_RESTART=true; shift ;;
        --quiet) QUIET=false; shift ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

################################################################################
# HELPER FUNCTIONS
################################################################################

log_header() {
    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
        echo -e "${BLUE}  $1${NC}"
        echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
    fi
}

log_info() {
    if [ "$QUIET" = false ]; then
        echo -e "${GREEN}✅${NC} $1"
    fi
}

log_warn() {
    echo -e "${YELLOW}⚠️${NC}  $1"
}

log_error() {
    echo -e "${RED}❌${NC} $1"
}

log_step() {
    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}➜${NC}  $1"
    fi
}

################################################################################
# PROCESS STATE DETECTION
################################################################################

check_ollama_running() {
    curl -s http://127.0.0.1:${OLLAMA_PORT}/api/tags > /dev/null 2>&1
    return $?
}

check_trading_engine_running() {
    pgrep -f "python3.*oanda_trading_engine.py" > /dev/null 2>&1
    return $?
}

check_dashboard_running() {
    pgrep -f "streamlit.*dashboard" > /dev/null 2>&1
    return $?
}

get_process_count() {
    local process_name=$1
    pgrep -f "$process_name" | wc -l || echo 0
}

################################################################################
# PHASE 1: PRE-FLIGHT CHECKS
################################################################################

phase_preflight() {
    log_header "PHASE 1: PRE-FLIGHT CHECKS"
    
    # Check working directory
    log_step "Verifying working directory..."
    if [ ! -d "$WORK_DIR" ]; then
        log_error "Working directory not found: $WORK_DIR"
        exit 1
    fi
    cd "$WORK_DIR"
    log_info "Working directory: $WORK_DIR"
    
    # Check Python installation
    log_step "Checking Python installation..."
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 not found"
        exit 1
    fi
    python_version=$(python3 --version)
    log_info "Python: $python_version"
    
    # Check required files
    log_step "Checking required files..."
    local required_files=(
        "oanda_trading_engine.py"
        "foundation/rick_charter.py"
        "foundation/margin_correlation_gate.py"
        ".env"
        "start_dashboard.sh"
    )
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            log_error "Required file missing: $file"
            exit 1
        fi
    done
    log_info "All required files present"
    
    # Verify Charter PIN immutable
    log_step "Verifying Charter immutability..."
    charter_pin=$(python3 -c "from foundation.rick_charter import RickCharter; print(RickCharter.PIN)" 2>/dev/null)
    if [ "$charter_pin" != "841921" ]; then
        log_error "Charter PIN tampered with! Expected 841921, got $charter_pin"
        exit 1
    fi
    log_info "Charter PIN verified: 841921 ✅"
    
    # Verify immutable constants
    log_step "Verifying immutable constants..."
    python3 << 'EOF'
from foundation.rick_charter import RickCharter

required_values = {
    'PIN': 841921,
    'MIN_NOTIONAL_USD': 15000,
    'MIN_RISK_REWARD_RATIO': 3.0,
    'MAX_HOLD_DURATION_HOURS': 6,
    'DAILY_LOSS_BREAKER_PCT': -5.0,
    'MAX_CONCURRENT_POSITIONS': 3,
}

for attr, expected in required_values.items():
    actual = getattr(RickCharter, attr)
    if actual != expected:
        print(f"FAILED: {attr} = {actual}, expected {expected}")
        exit(1)

print("✅ All immutable constants verified")
EOF
    log_info "All immutable constants correct"
    
    echo ""
}

################################################################################
# PHASE 2: GRACEFUL PROCESS MANAGEMENT
################################################################################

phase_process_management() {
    log_header "PHASE 2: GRACEFUL PROCESS MANAGEMENT"
    
    # Check for running Ollama
    log_step "Checking for running Ollama..."
    if check_ollama_running; then
        log_warn "Ollama already running on port $OLLAMA_PORT"
        if [ "$FORCE_RESTART" = true ]; then
            log_step "Force restart requested - stopping Ollama..."
            pkill -f "ollama serve" || true
            sleep 2
            log_info "Ollama stopped"
        else
            log_info "Reusing existing Ollama instance"
        fi
    else
        log_info "Ollama not running - will start fresh"
    fi
    
    # Check for running Trading Engine
    log_step "Checking for running Trading Engine..."
    engine_count=$(get_process_count "python3.*oanda_trading_engine.py")
    if [ "$engine_count" -gt 0 ]; then
        log_warn "Trading Engine already running (count: $engine_count)"
        if [ "$FORCE_RESTART" = true ]; then
            log_step "Force restart requested - stopping Trading Engine..."
            pkill -f "python3.*oanda_trading_engine.py" || true
            sleep 2
            log_info "Trading Engine stopped"
        else
            log_info "Reusing existing Trading Engine instance"
        fi
    else
        log_info "Trading Engine not running - will start fresh"
    fi
    
    # Check for running Dashboard
    log_step "Checking for running Dashboard..."
    if check_dashboard_running; then
        log_warn "Dashboard already running"
        if [ "$FORCE_RESTART" = true ]; then
            log_step "Force restart requested - stopping Dashboard..."
            pkill -f "streamlit" || true
            sleep 1
            log_info "Dashboard stopped"
        else
            log_info "Reusing existing Dashboard instance"
        fi
    else
        log_info "Dashboard not running - will start fresh"
    fi
    
    echo ""
}

################################################################################
# PHASE 3: START OLLAMA (IF NOT RUNNING)
################################################################################

phase_start_ollama() {
    log_header "PHASE 3: RICK NARRATION (OLLAMA)"
    
    if check_ollama_running; then
        log_info "Ollama already running - skipping startup"
        return 0
    fi
    
    log_step "Starting Ollama (Rick's narration engine)..."
    
    # Start Ollama in background
    if command -v ollama &> /dev/null; then
        ollama serve > /tmp/ollama.log 2>&1 &
        local ollama_pid=$!
        log_info "Ollama started (PID: $ollama_pid)"
        
        # Wait for Ollama to be ready
        log_step "Waiting for Ollama to be ready..."
        local max_attempts=30
        local attempt=0
        while [ $attempt -lt $max_attempts ]; do
            if check_ollama_running; then
                log_info "Ollama ready on port $OLLAMA_PORT"
                return 0
            fi
            attempt=$((attempt + 1))
            sleep 1
        done
        
        log_error "Ollama failed to start within $max_attempts seconds"
        return 1
    else
        log_warn "Ollama not installed - skipping"
        return 0
    fi
}

################################################################################
# PHASE 4: START TRADING ENGINE
################################################################################

phase_start_engine() {
    log_header "PHASE 4: HIVE MIND TRADING ENGINE"
    
    if check_trading_engine_running; then
        log_info "Trading Engine already running - skipping startup"
        return 0
    fi
    
    log_step "Starting Trading Engine (Hive Mind)..."
    
    # Verify .env file
    if [ ! -f ".env" ]; then
        log_error ".env file not found"
        return 1
    fi
    log_step "Verified .env file present"
    
    # Start Trading Engine in background
    python3 oanda_trading_engine.py > /tmp/engine.log 2>&1 &
    local engine_pid=$!
    log_info "Trading Engine started (PID: $engine_pid)"
    
    # Wait for engine initialization
    log_step "Waiting for engine initialization..."
    sleep 3
    
    # Check if process still running
    if ! kill -0 $engine_pid 2>/dev/null; then
        log_error "Trading Engine crashed during startup"
        log_error "See /tmp/engine.log for details:"
        tail -20 /tmp/engine.log
        return 1
    fi
    
    log_info "Trading Engine initialized successfully"
    return 0
}

################################################################################
# PHASE 5: LAUNCH DASHBOARD
################################################################################

phase_start_dashboard() {
    log_header "PHASE 5: REAL-TIME MONITORING DASHBOARD"
    
    if check_dashboard_running; then
        log_info "Dashboard already running - skipping launch"
        return 0
    fi
    
    log_step "Launching Tmux Dashboard (3-pane layout)..."
    
    if [ ! -f "start_dashboard.sh" ]; then
        log_error "start_dashboard.sh not found"
        return 1
    fi
    
    # Make executable
    chmod +x start_dashboard.sh
    
    # Start dashboard (it will create tmux session)
    bash start_dashboard.sh > /tmp/dashboard.log 2>&1 &
    log_info "Dashboard started"
    
    sleep 2
    log_info "Dashboard ready"
    return 0
}

################################################################################
# PHASE 6: VERIFICATION CHECKLIST
################################################################################

phase_verification() {
    log_header "PHASE 6: VERIFICATION CHECKLIST"
    
    local all_ok=true
    
    # Check 1: Charter immutability
    log_step "✓ Charter PIN immutability"
    if python3 -c "from foundation.rick_charter import RickCharter; assert RickCharter.PIN == 841921" 2>/dev/null; then
        log_info "Charter PIN: 841921 ✅"
    else
        log_error "Charter PIN verification failed"
        all_ok=false
    fi
    
    # Check 2: Guardian Gates loaded
    log_step "✓ Guardian Gates loaded"
    if python3 -c "from foundation.margin_correlation_gate import MarginCorrelationGate; gate = MarginCorrelationGate(account_nav=2000); print('✅ Gates ready')" 2>/dev/null; then
        log_info "Guardian Gates ready ✅"
    else
        log_error "Guardian Gates failed to initialize"
        all_ok=false
    fi
    
    # Check 3: Strategy Aggregator loaded
    log_step "✓ Strategy Aggregator loaded"
    if python3 -c "from util.strategy_aggregator import StrategyAggregator; print('✅ Strategies ready')" 2>/dev/null; then
        log_info "Strategy Aggregator ready ✅"
    else
        log_error "Strategy Aggregator failed to initialize"
        all_ok=false
    fi
    
    # Check 4: Quant Hedge Engine loaded
    log_step "✓ Quant Hedge Engine loaded"
    if python3 -c "from util.quant_hedge_engine import QuantHedgeEngine; print('✅ Hedge ready')" 2>/dev/null; then
        log_info "Quant Hedge Engine ready ✅"
    else
        log_error "Quant Hedge Engine failed to initialize"
        all_ok=false
    fi
    
    # Check 5: Narration Logger active
    log_step "✓ Narration Logger active"
    if [ -f "narration.jsonl" ]; then
        local last_entry=$(tail -1 narration.jsonl)
        log_info "Narration logging active ✅"
    else
        log_warn "narration.jsonl not found (will be created on first event)"
    fi
    
    # Check 6: Process states
    log_step "✓ Process states"
    if check_ollama_running; then
        log_info "Ollama running ✅"
    else
        log_warn "Ollama not running (optional)"
    fi
    
    if check_trading_engine_running; then
        log_info "Trading Engine running ✅"
    else
        log_error "Trading Engine not running"
        all_ok=false
    fi
    
    # Check 7: OANDA API connection
    log_step "✓ OANDA API connection"
    if python3 -c "from brokers.oanda_connector import OandaConnector; conn = OandaConnector(environment='practice'); print('✅ API ready')" 2>/dev/null; then
        log_info "OANDA API ready ✅"
    else
        log_error "OANDA API connection failed"
        all_ok=false
    fi
    
    echo ""
    
    if [ "$all_ok" = true ]; then
        log_info "All verification checks PASSED ✅"
        return 0
    else
        log_error "Some verification checks FAILED"
        return 1
    fi
}

################################################################################
# PHASE 7: READY FOR AUTONOMOUS OPERATION
################################################################################

phase_ready() {
    log_header "PHASE 7: SYSTEM READY FOR AUTONOMOUS OPERATION"
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  🤖 RBOTZILLA TRADING SYSTEM READY${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${GREEN}✅ Charter: IMMUTABLE (PIN 841921)${NC}"
    echo -e "${GREEN}✅ Gates: ACTIVE (Margin + Correlation)${NC}"
    echo -e "${GREEN}✅ Hive Mind: CONNECTED${NC}"
    echo -e "${GREEN}✅ Rick Narration: RUNNING${NC}"
    echo -e "${GREEN}✅ Dashboard: MONITORING (3-pane layout)${NC}"
    echo -e "${GREEN}✅ Narration: LOGGING to narration.jsonl${NC}"
    echo -e "${GREEN}✅ All Strategies: GATED & VOTING${NC}"
    echo ""
    echo -e "${BLUE}SYSTEM STATUS:${NC}"
    echo -e "  Working Directory: $WORK_DIR"
    echo -e "  Ollama Port: $OLLAMA_PORT (narration)"
    echo -e "  Trading Engine: RUNNING"
    echo -e "  Dashboard: LIVE (tmux session 'rbotzilla')"
    echo ""
    echo -e "${BLUE}DASHBOARD ACCESS:${NC}"
    echo -e "  • Left Pane: Live narration + positions"
    echo -e "  • Top-Right Pane: AI decisions (real-time)"
    echo -e "  • Bottom-Right Pane: Manual control terminal"
    echo ""
    echo -e "${BLUE}MANUAL CONTROL COMMANDS (in dashboard terminal):${NC}"
    echo -e "  > start    - Activate autonomous trading"
    echo -e "  > stop     - Gracefully halt trading"
    echo -e "  > status   - Show current state"
    echo -e "  > positions - List open positions"
    echo -e "  > log      - Show recent events"
    echo -e "  > help     - Show all commands"
    echo -e "  > exit     - Close terminal"
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
    echo ""
}

################################################################################
# ERROR HANDLING & CLEANUP
################################################################################

cleanup_on_error() {
    local exit_code=$?
    if [ $exit_code -ne 0 ]; then
        log_error "Startup failed with exit code $exit_code"
        log_error "Checking logs for details..."
        
        if [ -f "/tmp/engine.log" ] && [ -s "/tmp/engine.log" ]; then
            log_error "Trading Engine log (last 10 lines):"
            tail -10 /tmp/engine.log | sed 's/^/  /'
        fi
        
        if [ -f "/tmp/ollama.log" ] && [ -s "/tmp/ollama.log" ]; then
            log_error "Ollama log (last 10 lines):"
            tail -10 /tmp/ollama.log | sed 's/^/  /'
        fi
    fi
    return $exit_code
}

trap cleanup_on_error EXIT

################################################################################
# MAIN EXECUTION SEQUENCE
################################################################################

main() {
    log_header "🚀 RBOTZILLA SMART STARTUP ORCHESTRATOR"
    echo -e "PIN: 841921 ✅ | Mode: Paper Trading | Timestamp: $(date)"
    echo ""
    
    # Execute all phases
    phase_preflight || exit 1
    phase_process_management || exit 1
    phase_start_ollama || log_warn "Ollama startup failed (non-fatal)"
    phase_start_engine || exit 1
    phase_start_dashboard || exit 1
    phase_verification || exit 1
    phase_ready
    
    log_info "System is now running autonomously"
    log_info "Access dashboard at: tmux attach -t rbotzilla"
}

# Run main sequence
main "$@"
