#!/bin/bash
# tmux_ghost_monitor.sh
# Opens comprehensive tmux monitoring windows for ghost trading

echo "🖥️ SETTING UP GHOST TRADING MONITORING WINDOWS"
echo "=============================================="

# Kill any existing monitoring session
tmux kill-session -t ghost_monitor 2>/dev/null || true

# Create monitoring session
tmux new-session -d -s ghost_monitor -n "Real_Time_Log"

# Window 1: Real-time ghost trading log
tmux send-keys -t ghost_monitor:0 "echo 'Real-time Ghost Trading Log'; echo '============================'; tail -f logs/ghost_trading.log 2>/dev/null || (echo 'Waiting for ghost trading to start...'; sleep 2; tail -f logs/ghost_trading.log)" Enter

# Window 2: Session progress tracking
tmux new-window -t ghost_monitor -n "Progress" 
tmux send-keys -t ghost_monitor:1 "watch -n 3 'echo \"=== GHOST TRADING PROGRESS ===\"; echo \"Time: \$(date +\"%H:%M:%S\")\"; echo \"\"; if [ -f logs/ghost_session.jsonl ]; then echo \"Latest Progress:\"; tail -3 logs/ghost_session.jsonl | jq -r \". | \\\"Trades: \\(.total_trades) | Win Rate: \\(.win_rate)% | PnL: $\\(.total_pnl) | Time Left: \\(.time_remaining)min\\\"\" 2>/dev/null || tail -3 logs/ghost_session.jsonl; else echo \"No progress data yet...\"; fi; echo \"\"; echo \"=== FILES ===\"; ls -la logs/ghost* 2>/dev/null || echo \"No ghost files yet\"'" Enter

# Window 3: System status and toggle
tmux new-window -t ghost_monitor -n "System_Status"
tmux send-keys -t ghost_monitor:2 "watch -n 2 'echo \"=== SYSTEM STATUS ===\"; echo \"Upgrade Toggle: \$(cat .upgrade_toggle 2>/dev/null || echo OFF)\"; echo \"Ghost Engine: \$(pgrep -f ghost_trading_engine.py >/dev/null && echo RUNNING || echo STOPPED)\"; echo \"\"; echo \"=== PROMOTION CRITERIA ===\"; echo \"✓ Min 10 trades\"; echo \"✓ 70%+ win rate\"; echo \"✓ \$50+ total PnL\"; echo \"✓ ≤3 consecutive losses\"; echo \"\"; echo \"=== MEMORY/CPU ===\"; free -h | head -2; echo \"\"; ps aux | grep ghost_trading | grep -v grep || echo \"No ghost trading process\"'" Enter

# Window 4: Final report viewer
tmux new-window -t ghost_monitor -n "Final_Report"
tmux send-keys -t ghost_monitor:3 "watch -n 5 'echo \"=== FINAL REPORT WATCH ===\"; if [ -f ghost_trading_final_report.json ]; then echo \"Final Results Available:\"; cat ghost_trading_final_report.json | jq . 2>/dev/null || cat ghost_trading_final_report.json; else echo \"Ghost trading still in progress...\"; echo \"Session will auto-complete after 45 minutes\"; echo \"\"; echo \"Manual stop: pkill -f ghost_trading_engine\"; fi'" Enter

# Window 5: Emergency controls
tmux new-window -t ghost_monitor -n "Emergency_Controls"
tmux send-keys -t ghost_monitor:4 "echo '🚨 EMERGENCY CONTROLS'; echo '===================='; echo ''; echo 'Available commands:'; echo ''; echo '1. Stop ghost trading:'; echo '   pkill -f ghost_trading_engine.py'; echo ''; echo '2. Prevent live promotion:'; echo '   echo OFF > .upgrade_toggle'; echo ''; echo '3. Check current status:'; echo '   cat .upgrade_toggle'; echo ''; echo '4. View final report:'; echo '   cat ghost_trading_final_report.json'; echo ''; echo '5. Kill all tmux sessions:'; echo '   tmux kill-server'; echo ''; echo 'Type commands above as needed...'; bash" Enter

# Select the real-time log window
tmux select-window -t ghost_monitor:0

# Attach to the monitoring session
echo "🚀 Launching Ghost Trading Monitoring Dashboard..."
echo "📊 Windows: Real-Time Log | Progress | System Status | Final Report | Emergency Controls"
echo ""
tmux attach-session -t ghost_monitor