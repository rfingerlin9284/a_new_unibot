#!/bin/bash
# quick_dashboard_commands.sh - Quick Reference for RICK Dashboard
# Copy-paste these commands for common operations

# ============================================================================
# DASHBOARD OPERATIONS
# ============================================================================

# Start enhanced dashboard (if not running)
start_dashboard() {
    cd /home/ing/RICK/R_H_UNI
    pre_upgrade/standalone/.venv/bin/streamlit run dashboard_enhanced.py \
        --server.port 8501 \
        --server.address localhost \
        --server.headless true \
        --browser.gatherUsageStats false &
}

# Stop dashboard
stop_dashboard() {
    pkill -f "streamlit run dashboard_enhanced.py"
}

# Restart dashboard (fresh cache)
restart_dashboard() {
    pkill -f "streamlit run dashboard_enhanced.py"
    sleep 2
    rm -rf ~/.streamlit/cache .streamlit/cache
    start_dashboard
}

# Check dashboard status
check_dashboard() {
    if pgrep -f "streamlit run dashboard_enhanced.py" > /dev/null; then
        echo "✅ Dashboard ONLINE at http://localhost:8501"
        ps aux | grep -E "streamlit.*dashboard_enhanced" | grep -v grep
    else
        echo "❌ Dashboard OFFLINE"
    fi
}

# ============================================================================
# TMUX OPERATIONS
# ============================================================================

# Launch TMUX monitoring dashboard
launch_tmux() {
    /home/ing/RICK/R_H_UNI/scripts/launch_unified_dashboard.sh
}

# Attach to existing TMUX session
attach_tmux() {
    tmux attach-session -t RICK_UNIFIED_DASH
}

# Kill TMUX session
kill_tmux() {
    tmux kill-session -t RICK_UNIFIED_DASH
}

# Check TMUX status
check_tmux() {
    if tmux has-session -t RICK_UNIFIED_DASH 2>/dev/null; then
        echo "✅ TMUX session ACTIVE"
        tmux list-windows -t RICK_UNIFIED_DASH
    else
        echo "❌ TMUX session NOT FOUND"
    fi
}

# ============================================================================
# TESTING & DEBUGGING
# ============================================================================

# Test narration bridge
test_narration() {
    cd /home/ing/RICK/R_H_UNI
    python3 dashboard/narrate_plain.py
}

# Test data bridge
test_data_bridge() {
    cd /home/ing/RICK/R_H_UNI
    python3 -c "
from dashboard.bridge_readonly import get_narration_feed, get_system_mode, get_pnl_stream
print('=== Data Bridge Test ===')
print('Mode:', get_system_mode())
print('Recent Events:', len(get_narration_feed(5)))
print('Recent P&L:', len(get_pnl_stream(5)))
"
}

# View live logs
view_logs() {
    cd /home/ing/RICK/R_H_UNI
    tail -f pre_upgrade/headless/logs/narration.jsonl | jq -C '.'
}

# View P&L stream
view_pnl() {
    cd /home/ing/RICK/R_H_UNI
    tail -f pre_upgrade/headless/logs/pnl.jsonl | jq -C '.'
}

# ============================================================================
# MAINTENANCE
# ============================================================================

# Clear Streamlit cache
clear_cache() {
    rm -rf ~/.streamlit/cache .streamlit/cache
    echo "✅ Cache cleared"
}

# Check disk usage of logs
check_logs_size() {
    du -sh /home/ing/RICK/R_H_UNI/pre_upgrade/headless/logs/
}

# Backup dashboard files
backup_dashboard() {
    cd /home/ing/RICK/R_H_UNI
    tar -czf ~/dashboard_backup_$(date +%Y%m%d_%H%M%S).tar.gz \
        dashboard/ \
        dashboard_enhanced.py \
        scripts/launch_unified_dashboard.sh
    echo "✅ Backup created in ~/"
}

# ============================================================================
# QUICK STATUS CHECK
# ============================================================================

status_all() {
    echo "╔════════════════════════════════════════╗"
    echo "║   🤖 RICK DASHBOARD STATUS            ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    
    # Mode
    if [[ -f /home/ing/RICK/R_H_UNI/.upgrade_toggle ]]; then
        MODE=$(cat /home/ing/RICK/R_H_UNI/.upgrade_toggle 2>/dev/null || echo "UNKNOWN")
        echo "  Mode: $MODE"
    fi
    
    echo ""
    
    # Dashboard
    if pgrep -f "streamlit run dashboard_enhanced.py" > /dev/null; then
        echo "  Dashboard:    ✅ ONLINE (http://localhost:8501)"
    else
        echo "  Dashboard:    ❌ OFFLINE"
    fi
    
    # Standalone feed
    if pgrep -f "streamlit run dashboard/live_activity_feed.py" > /dev/null; then
        echo "  Test Feed:    ✅ ONLINE (http://localhost:8502)"
    else
        echo "  Test Feed:    ⚪ NOT RUNNING"
    fi
    
    # TMUX
    if tmux has-session -t RICK_UNIFIED_DASH 2>/dev/null; then
        echo "  TMUX Monitor: ✅ ACTIVE"
    else
        echo "  TMUX Monitor: ⚪ NOT RUNNING"
    fi
    
    # Engine
    if pgrep -f "ghost_trading_engine\|live_ghost_engine" > /dev/null; then
        echo "  Trading Bot:  ✅ RUNNING"
    else
        echo "  Trading Bot:  ⚫ STOPPED"
    fi
    
    echo ""
    echo "════════════════════════════════════════"
}

# ============================================================================
# HELP
# ============================================================================

show_help() {
    echo "🤖 RICK Dashboard Quick Commands"
    echo ""
    echo "DASHBOARD:"
    echo "  start_dashboard       - Launch enhanced dashboard"
    echo "  stop_dashboard        - Stop dashboard"
    echo "  restart_dashboard     - Restart with fresh cache"
    echo "  check_dashboard       - Show dashboard status"
    echo ""
    echo "TMUX:"
    echo "  launch_tmux           - Launch 4-window monitoring"
    echo "  attach_tmux           - Attach to existing session"
    echo "  kill_tmux             - Kill TMUX session"
    echo "  check_tmux            - Show TMUX status"
    echo ""
    echo "TESTING:"
    echo "  test_narration        - Test plain English translations"
    echo "  test_data_bridge      - Test data bridge connectivity"
    echo "  view_logs             - Stream narration logs"
    echo "  view_pnl              - Stream P&L logs"
    echo ""
    echo "MAINTENANCE:"
    echo "  clear_cache           - Clear Streamlit cache"
    echo "  check_logs_size       - Check log disk usage"
    echo "  backup_dashboard      - Backup dashboard files"
    echo ""
    echo "QUICK:"
    echo "  status_all            - Show all component status"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

# If sourced, define functions. If executed, show help
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    show_help
fi
