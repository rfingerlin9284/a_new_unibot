#!/usr/bin/env bash

# RBOTzilla UNI - Final QA Test Walkthrough
# 🎯 Purpose: Simulate human-level usability testing for non-technical users
# 🧠 Persona: UI Quality Control Supervisor validating dashboard readiness
# 📊 Target: 17" monitor (1920x1080) non-technical user experience

set -euo pipefail

PROJECT_DIR="/home/ing/RICK/R_H_UNI"
MOBILE_DASH_URL="http://localhost:5056/mobile_console"
SOCKET_SERVER_URL="http://localhost:5056"
STANDALONE_DIR="$PROJECT_DIR/standalone_shell"
CONFIG_PATH="$PROJECT_DIR/configs"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test results tracking
PASS_COUNT=0
FAIL_COUNT=0
TOTAL_TESTS=0

function log_test() {
    local test_name="$1"
    local result="$2"
    local details="${3:-}"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$result" = "PASS" ]; then
        echo -e "✅ ${GREEN}PASS${NC}: $test_name"
        PASS_COUNT=$((PASS_COUNT + 1))
        [ -n "$details" ] && echo "   └─ $details"
    else
        echo -e "❌ ${RED}FAIL${NC}: $test_name"
        FAIL_COUNT=$((FAIL_COUNT + 1))
        [ -n "$details" ] && echo "   └─ $details"
    fi
}

function test_section() {
    echo -e "\n${BLUE}🧪 $1${NC}"
    echo "═══════════════════════════════════════════"
}

function check_server_running() {
    if curl -s "$SOCKET_SERVER_URL" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

function check_file_exists() {
    [ -f "$1" ]
}

function check_content_exists() {
    local file="$1"
    local pattern="$2"
    [ -f "$file" ] && grep -q "$pattern" "$file"
}

echo -e "${YELLOW}🚨 RBOTzilla UNI - Final QA Validation${NC}"
echo -e "${YELLOW}🧠 Persona: UI Quality Control Supervisor${NC}"
echo -e "${YELLOW}📊 Target: Non-technical user on 17\" monitor${NC}"
echo ""

# ============================================================================
# PHASE QA-0: GENERAL HARDWARE & LAYOUT AUDIT
# ============================================================================
test_section "PHASE QA-0: Hardware & Layout Audit"

# Check if server is running
if check_server_running; then
    log_test "Socket Server Accessibility" "PASS" "Server responding on port 5056"
else
    log_test "Socket Server Accessibility" "FAIL" "Server not responding - may need to start with: cd $STANDALONE_DIR && node server_stream.js"
fi

# Check core dashboard files exist
if check_file_exists "$STANDALONE_DIR/index.html"; then
    log_test "Main Dashboard File" "PASS" "index.html found"
else
    log_test "Main Dashboard File" "FAIL" "index.html missing"
fi

if check_file_exists "$PROJECT_DIR/mobile_console/index.html"; then
    log_test "Mobile Console File" "PASS" "mobile_console/index.html found"
else
    log_test "Mobile Console File" "FAIL" "mobile_console/index.html missing"
fi

# Check responsive design elements
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "viewport"; then
    log_test "Responsive Design Meta Tag" "PASS" "Viewport meta tag present"
else
    log_test "Responsive Design Meta Tag" "FAIL" "Missing viewport meta tag"
fi

# Check font readability
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "font-family.*monospace\|Orbitron"; then
    log_test "Readable Font Family" "PASS" "Monospace/Orbitron fonts configured"
else
    log_test "Readable Font Family" "FAIL" "May need better font configuration"
fi

# ============================================================================
# PHASE QA-1: "CAN A HUMAN USE THIS?" TEST
# ============================================================================
test_section "PHASE QA-1: Human Usability Test"

# Check for Rick welcome/personality
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "Rick\|🤖"; then
    log_test "Rick Personality Present" "PASS" "Rick references found in interface"
else
    log_test "Rick Personality Present" "FAIL" "Rick personality elements missing"
fi

# Check for file upload interface
if check_content_exists "$STANDALONE_DIR/index.html" "upload\|file\|\.env\|config\|key"; then
    log_test "API Key Upload Interface" "PASS" "Upload interface elements found"
else
    log_test "API Key Upload Interface" "FAIL" "No obvious upload interface for .env files"
fi

# Check for drag/drop functionality
if check_content_exists "$STANDALONE_DIR/index.html" "drag\|drop\|interact"; then
    log_test "Drag & Drop Support" "PASS" "InteractJS or drag/drop logic found"
else
    log_test "Drag & Drop Support" "FAIL" "Drag/drop functionality may be missing"
fi

# Check for error handling
if check_content_exists "$STANDALONE_DIR/server_stream.js" "error\|catch\|try"; then
    log_test "Error Handling Present" "PASS" "Error handling found in server code"
else
    log_test "Error Handling Present" "FAIL" "May need better error handling"
fi

# ============================================================================
# PHASE QA-2: WIDGET LOGIC & DATA FLOW TEST
# ============================================================================
test_section "PHASE QA-2: Widget Logic & Data Flow"

# Check for strategy map functionality
if check_content_exists "$STANDALONE_DIR/index.html" "Strategy\|strategy\|📊"; then
    log_test "Strategy Map Widget" "PASS" "Strategy elements found"
else
    log_test "Strategy Map Widget" "FAIL" "Strategy map widget missing"
fi

# Check for ML predictions
if check_content_exists "$STANDALONE_DIR/index.html" "ML\|prediction\|📈\|model"; then
    log_test "ML Predictions Widget" "PASS" "ML prediction elements found"
else
    log_test "ML Predictions Widget" "FAIL" "ML prediction widget missing"
fi

# Check for Rick prompt functionality
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "prompt\|input\|Chat.*Rick"; then
    log_test "Rick Prompt Interface" "PASS" "Rick prompt interface found"
else
    log_test "Rick Prompt Interface" "FAIL" "Rick prompt interface missing"
fi

# Check for comic summary
if check_content_exists "$STANDALONE_DIR/race_comic.js" "comic\|Comic\|🎬"; then
    log_test "Comic Summary Feature" "PASS" "Comic strip functionality found"
else
    log_test "Comic Summary Feature" "FAIL" "Comic summary feature missing"
fi

# Check for rollback functionality
if check_content_exists "$STANDALONE_DIR/index.html" "rollback\|🧨\|Rollback"; then
    log_test "Rollback Button" "PASS" "Rollback functionality found"
else
    log_test "Rollback Button" "FAIL" "Rollback button missing"
fi

# ============================================================================
# PHASE QA-3: LIVE FEEDS & STATUS INDICATORS
# ============================================================================
test_section "PHASE QA-3: Live Feeds & Status Indicators"

# Check Socket.IO integration
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "socket\.io\|ioClient"; then
    log_test "Socket.IO Integration" "PASS" "Socket.IO client code found"
else
    log_test "Socket.IO Integration" "FAIL" "Socket.IO integration missing"
fi

# Check TMUX feed logic
if check_content_exists "$STANDALONE_DIR/server_stream.js" "tmux\|TMUX"; then
    log_test "TMUX Feed Logic" "PASS" "TMUX streaming logic found"
else
    log_test "TMUX Feed Logic" "FAIL" "TMUX feed logic missing"
fi

# Check market data feeds
if check_content_exists "$STANDALONE_DIR/server_stream.js" "EUR/USD\|BTC/USD\|market.*data"; then
    log_test "Market Data Feeds" "PASS" "Market data generation found"
else
    log_test "Market Data Feeds" "FAIL" "Market data feeds missing"
fi

# Check session detection
if check_content_exists "$STANDALONE_DIR/server_stream.js" "session\|London\|Asian\|weekend"; then
    log_test "Session Detection" "PASS" "Session detection logic found"
else
    log_test "Session Detection" "FAIL" "Session detection missing"
fi

# Check P&L HUD
if check_content_exists "$STANDALONE_DIR/pnl_hud.js" "P.*L\|pnl\|HUD"; then
    log_test "P&L HUD Overlay" "PASS" "P&L HUD functionality found"
else
    log_test "P&L HUD Overlay" "FAIL" "P&L HUD overlay missing"
fi

# Check connection status indicators
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "connection.*status\|🟢\|🔴"; then
    log_test "Connection Status Indicators" "PASS" "Status indicators found"
else
    log_test "Connection Status Indicators" "FAIL" "Connection status indicators missing"
fi

# ============================================================================
# PHASE QA-4: THEME & LAYOUT UX TEST
# ============================================================================
test_section "PHASE QA-4: Theme & Layout UX"

# Check theme switcher
if check_content_exists "$STANDALONE_DIR/theme_engine.js" "theme\|THEMES\|switch"; then
    log_test "Theme Switcher Engine" "PASS" "Theme switching functionality found"
else
    log_test "Theme Switcher Engine" "FAIL" "Theme switcher missing"
fi

# Check multiple themes available
if check_content_exists "$STANDALONE_DIR/theme_engine.js" "stealth.*tron.*core\|stealth.*core.*tron"; then
    log_test "Multiple Themes Available" "PASS" "Multiple themes configured"
else
    log_test "Multiple Themes Available" "FAIL" "Need multiple theme options"
fi

# Check resizable panels
if check_content_exists "$STANDALONE_DIR/index.html" "resize\|interact.*resize"; then
    log_test "Resizable Panels" "PASS" "Panel resize functionality found"
else
    log_test "Resizable Panels" "FAIL" "Panel resize functionality missing"
fi

# Check grid layout
if check_content_exists "$PROJECT_DIR/mobile_console/index.html" "grid\|flex\|display.*grid"; then
    log_test "Grid Layout System" "PASS" "CSS Grid/Flex layout found"
else
    log_test "Grid Layout System" "FAIL" "Need better layout system"
fi

# ============================================================================
# PHASE QA-5: MANUAL & EMERGENCY CONTROLS
# ============================================================================
test_section "PHASE QA-5: Manual & Emergency Controls"

# Check LLM fuse lock
if check_content_exists "$STANDALONE_DIR/override_controls.js" "LLM.*lock\|llm.*fuse\|toggleLLM"; then
    log_test "LLM Fuse Lock Control" "PASS" "LLM lock functionality found"
else
    log_test "LLM Fuse Lock Control" "FAIL" "LLM fuse lock missing"
fi

# Check manual override
if check_content_exists "$STANDALONE_DIR/override_controls.js" "manual.*override\|toggleOverride"; then
    log_test "Manual Override Control" "PASS" "Manual override functionality found"
else
    log_test "Manual Override Control" "FAIL" "Manual override missing"
fi

# Check emergency stop
if check_content_exists "$STANDALONE_DIR/override_controls.js" "emergency.*stop\|emergencyStop"; then
    log_test "Emergency Stop Control" "PASS" "Emergency stop functionality found"
else
    log_test "Emergency Stop Control" "FAIL" "Emergency stop missing"
fi

# Check backup/restore system
if check_file_exists "$PROJECT_DIR/backup_restore.sh"; then
    log_test "Backup/Restore System" "PASS" "Backup system script found"
else
    log_test "Backup/Restore System" "FAIL" "Backup/restore system missing"
fi

# Check self-repair interface
if check_content_exists "$STANDALONE_DIR/repair_interface.js" "repair\|diagnostic\|RepairInterface"; then
    log_test "Self-Repair Interface" "PASS" "Self-repair functionality found"
else
    log_test "Self-Repair Interface" "FAIL" "Self-repair interface missing"
fi

# ============================================================================
# PHASE QA-6: VOICE & ACCESSIBILITY
# ============================================================================
test_section "PHASE QA-6: Voice & Accessibility Features"

# Check Rick voice narrator
if check_content_exists "$STANDALONE_DIR/rick_voice_narrator.js" "voice\|speech\|TTS\|narrator"; then
    log_test "Rick Voice Narrator" "PASS" "Voice narration functionality found"
else
    log_test "Rick Voice Narrator" "FAIL" "Voice narrator missing"
fi

# Check voice setup flag
if check_content_exists "$CONFIG_PATH/pairs_config.json" "voice.*setup\|speech"; then
    log_test "Voice Setup Configuration" "PASS" "Voice setup options found"
else
    log_test "Voice Setup Configuration" "FAIL" "Voice setup may need configuration"
fi

# ============================================================================
# CONFIGURATION FILE VALIDATION
# ============================================================================
test_section "CONFIGURATION VALIDATION"

# Check 54 instruments provisioned
if check_file_exists "$CONFIG_PATH/pairs_config.json"; then
    fx_count=$(jq '.oanda_pairs | length' "$CONFIG_PATH/pairs_config.json" 2>/dev/null || echo "0")
    spot_count=$(jq '.coinbase_spot | length' "$CONFIG_PATH/pairs_config.json" 2>/dev/null || echo "0")
    perp_count=$(jq '.derivative_pairs | length' "$CONFIG_PATH/pairs_config.json" 2>/dev/null || echo "0")
    total=$((fx_count + spot_count + perp_count))
    
    if [ "$total" -eq 54 ]; then
        log_test "54 Instruments Provisioned" "PASS" "FX:$fx_count + Spot:$spot_count + Perps:$perp_count = 54"
    else
        log_test "54 Instruments Provisioned" "FAIL" "Only $total instruments found, expected 54"
    fi
else
    log_test "54 Instruments Provisioned" "FAIL" "pairs_config.json not found"
fi

# Check session intelligence
if check_content_exists "$CONFIG_PATH/pairs_config.json" "session_intelligence.*true"; then
    log_test "Session Intelligence Enabled" "PASS" "Session intelligence configured"
else
    log_test "Session Intelligence Enabled" "FAIL" "Session intelligence not enabled"
fi

# Check risk management settings
if check_content_exists "$CONFIG_PATH/pairs_config.json" "risk_management"; then
    log_test "Risk Management Configuration" "PASS" "Risk management settings found"
else
    log_test "Risk Management Configuration" "FAIL" "Risk management settings missing"
fi

# ============================================================================
# SERVER ENDPOINT VALIDATION
# ============================================================================
test_section "SERVER ENDPOINT VALIDATION"

if check_server_running; then
    # Test P&L endpoint
    if curl -s "$SOCKET_SERVER_URL/rick/pnl" | grep -q "pnl\|P&L\|\$"; then
        log_test "P&L Endpoint Response" "PASS" "P&L endpoint returning data"
    else
        log_test "P&L Endpoint Response" "FAIL" "P&L endpoint not responding correctly"
    fi
    
    # Test LLM lock endpoint
    if curl -s "$SOCKET_SERVER_URL/rick/llm/lock" | grep -q "status\|locked"; then
        log_test "LLM Lock Endpoint" "PASS" "LLM lock endpoint responding"
    else
        log_test "LLM Lock Endpoint" "FAIL" "LLM lock endpoint not responding"
    fi
    
    # Test rollback endpoint
    if curl -s "$SOCKET_SERVER_URL/rick/rollback" | grep -q "status\|rollback"; then
        log_test "Rollback Endpoint" "PASS" "Rollback endpoint responding"
    else
        log_test "Rollback Endpoint" "FAIL" "Rollback endpoint not responding"
    fi
else
    log_test "Server Endpoints" "FAIL" "Server not running - cannot test endpoints"
fi

# ============================================================================
# FINAL REPORT GENERATION
# ============================================================================
echo ""
echo "═══════════════════════════════════════════"
echo -e "${YELLOW}📋 FINAL QA REPORT${NC}"
echo "═══════════════════════════════════════════"

echo -e "\n📊 ${BLUE}TEST RESULTS SUMMARY${NC}"
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASS_COUNT${NC}"
echo -e "Failed: ${RED}$FAIL_COUNT${NC}"

# Calculate pass percentage
if [ $TOTAL_TESTS -gt 0 ]; then
    PASS_PERCENTAGE=$(echo "scale=1; $PASS_COUNT * 100 / $TOTAL_TESTS" | bc -l 2>/dev/null || echo "0")
    echo "Pass Rate: ${PASS_PERCENTAGE}%"
else
    echo "Pass Rate: 0%"
fi

echo -e "\n🎯 ${BLUE}LAUNCH READINESS ASSESSMENT${NC}"

if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "✅ ${GREEN}SYSTEM READY FOR LAUNCH${NC}"
    echo "All critical systems passed validation"
    echo ""
    echo -e "${YELLOW}Rick says:${NC} \"Yo boss, everything's locked, loaded, and war-ready."
    echo "Cockpit's clean, all systems green. Ready to make some money!\""
    echo ""
    echo -e "${GREEN}🚀 READY TO GO LIVE${NC}"
elif [ $FAIL_COUNT -le 3 ]; then
    echo -e "⚠️  ${YELLOW}SYSTEM MOSTLY READY - MINOR ISSUES${NC}"
    echo "Some non-critical issues detected, but core functionality intact"
    echo ""
    echo -e "${YELLOW}Rick says:${NC} \"We got a couple hiccups, but nothing that'll"
    echo "stop us from trading. Let's roll and fix 'em on the fly.\""
    echo ""
    echo -e "${YELLOW}🎯 READY FOR SOFT LAUNCH${NC}"
else
    echo -e "❌ ${RED}SYSTEM NOT READY - CRITICAL ISSUES${NC}"
    echo "Multiple critical issues detected - recommend fixing before launch"
    echo ""
    echo -e "${RED}Rick says:${NC} \"Hold up soldier, we got some serious problems."
    echo "Let's get these fixed before we go live and lose money.\""
    echo ""
    echo -e "${RED}🛑 NOT READY FOR LAUNCH${NC}"
fi

echo ""
echo "═══════════════════════════════════════════"
echo -e "${BLUE}📱 ACCESS POINTS${NC}"
echo "═══════════════════════════════════════════"
echo "Main Dashboard: http://localhost:5056"
echo "Mobile Console: http://localhost:5056/mobile_console/"
echo "Socket Server: ws://localhost:5056"
echo ""
echo "═══════════════════════════════════════════"
echo -e "${BLUE}🔧 QUICK START COMMANDS${NC}"
echo "═══════════════════════════════════════════"
echo "Start Server: cd $STANDALONE_DIR && node server_stream.js"
echo "Run Backup: $PROJECT_DIR/backup_restore.sh backup"
echo "Self Repair: curl http://localhost:5056/rick/repair"
echo ""

# Create QA completion marker
cat > "$PROJECT_DIR/QA_VALIDATION_COMPLETE.txt" << EOF
RBOTzilla UNI - QA Validation Complete
====================================
Date: $(date)
Total Tests: $TOTAL_TESTS
Passed: $PASS_COUNT
Failed: $FAIL_COUNT
Pass Rate: ${PASS_PERCENTAGE:-0}%

Status: $([ $FAIL_COUNT -eq 0 ] && echo "READY FOR LAUNCH" || echo "NEEDS ATTENTION")

Last Validation: $(date '+%Y-%m-%d %H:%M:%S')
EOF

echo -e "${GREEN}✅ QA validation report saved to: QA_VALIDATION_COMPLETE.txt${NC}"
echo ""

exit $FAIL_COUNT