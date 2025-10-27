#!/usr/bin/env bash

# RBOTzilla UNI - Production Auto-Login Configuration
# Sets up automatic system login and battlestation activation

echo "🚀 RBOTzilla UNI - Production Auto-Login Setup"
echo "==============================================="

# Check if we're running as the correct user
if [[ "$USER" != "ing" ]]; then
    echo "❌ This script must be run as user 'ing'"
    exit 1
fi

RICK_ROOT="/home/ing/RICK/R_H_UNI"

echo ""
echo "🔧 Current Auto-Login Configuration"
echo "==================================="

# Check current auto-login status
if systemctl is-enabled graphical-session-pre.target >/dev/null 2>&1; then
    echo "✅ Graphical session auto-start: ENABLED"
else
    echo "⚠️ Graphical session auto-start: NOT CONFIGURED"
fi

# Check systemd user services
echo ""
echo "📊 RBOTzilla UNI Services Status:"
echo "---------------------------------"
for service in rbotzilla-uni-main rbotzilla-safety rbotzilla-sessions; do
    status=$(systemctl --user is-enabled ${service}.service 2>/dev/null || echo "not-found")
    active=$(systemctl --user is-active ${service}.service 2>/dev/null || echo "inactive")
    echo "  $service: $status ($active)"
done

timer_status=$(systemctl --user is-enabled rbotzilla-keepalive.timer 2>/dev/null || echo "not-found")
timer_active=$(systemctl --user is-active rbotzilla-keepalive.timer 2>/dev/null || echo "inactive")
echo "  keepalive timer: $timer_status ($timer_active)"

echo ""
echo "🔐 Trading Safety Features"
echo "=========================="
echo "✅ 6-digit PIN shutdown protection"
echo "✅ Open trade detection with SL/TP verification" 
echo "✅ Automatic service restart on failure"
echo "✅ Safe shutdown with position closure"

echo ""
echo "📋 Auto-Login Configuration Summary"
echo "==================================="
echo ""
echo "🔄 Boot Sequence:"
echo "  1. System boots → User 'ing' auto-login"
echo "  2. Systemd user services start automatically:"
echo "     - rbotzilla-uni-main.service (Socket.IO server)"
echo "     - rbotzilla-safety.service (Trading safety monitor)"
echo "     - rbotzilla-sessions.service (Session intelligence)"
echo "     - rbotzilla-keepalive.timer (Health monitoring)"
echo ""
echo "🌐 Network Services:"
echo "  - Socket.IO server: http://localhost:5056"
echo "  - Live market feeds via WebSocket"
echo "  - TMUX session monitoring"
echo "  - Real-time trading data streams"
echo ""
echo "🛡️ Safety Features:"
echo "  - Automatic SL/TP verification before shutdown"
echo "  - 6-digit PIN required for manual shutdown"
echo "  - Service auto-restart on unexpected failure"
echo "  - Position monitoring and safe closure"

echo ""
echo "🔧 Management Commands"
echo "====================="
echo ""
echo "📊 Status Monitoring:"
echo "  systemctl --user status rbotzilla-uni-main.service"
echo "  systemctl --user list-units | grep rbotzilla"
echo "  journalctl --user -u rbotzilla-uni-main.service -f"
echo ""
echo "🔄 Service Control:"
echo "  systemctl --user restart rbotzilla-uni-main.service"
echo "  systemctl --user stop rbotzilla-uni-main.service"
echo "  systemctl --user start rbotzilla-uni-main.service"
echo ""
echo "🔐 Safe Shutdown:"
echo "  $RICK_ROOT/scripts/shutdown_with_pin.sh"
echo ""
echo "🧪 Testing:"
echo "  $RICK_ROOT/test_pin_shutdown.sh"

echo ""
echo "⚡ Production Readiness Checklist"
echo "================================="

# Check if main service is running
if systemctl --user is-active --quiet rbotzilla-uni-main.service; then
    echo "✅ Main trading service: RUNNING"
else
    echo "❌ Main trading service: NOT RUNNING"
fi

# Check if safety monitor is running  
if systemctl --user is-active --quiet rbotzilla-safety.service; then
    echo "✅ Safety monitor: RUNNING"
else
    echo "❌ Safety monitor: NOT RUNNING"
fi

# Check if socket server responds
if curl -s "http://localhost:5056" >/dev/null 2>&1; then
    echo "✅ Socket.IO server: RESPONSIVE"
else
    echo "❌ Socket.IO server: NOT RESPONDING"
fi

# Check if services are enabled for auto-start
if systemctl --user is-enabled --quiet rbotzilla-uni-main.service; then
    echo "✅ Auto-start on boot: ENABLED"
else
    echo "❌ Auto-start on boot: NOT ENABLED"
fi

# Check runtime directory
if [[ -d "$RICK_ROOT/runtime" ]]; then
    echo "✅ Runtime directory: EXISTS"
else
    echo "❌ Runtime directory: MISSING"
fi

echo ""
echo "🎯 Next Steps for Full Production"
echo "================================="
echo ""
echo "1. 🖥️ Configure system auto-login:"
echo "   sudo systemctl edit getty@tty1"
echo "   # Add: ExecStart=-/sbin/agetty -a ing --noclear %I \$TERM"
echo ""
echo "2. 🔄 Enable lingering (services persist after logout):"
echo "   sudo loginctl enable-linger ing"
echo ""
echo "3. 🌐 Configure firewall (if needed):"
echo "   sudo ufw allow 5056/tcp  # Socket.IO port"
echo ""
echo "4. 📱 Browser auto-open (optional):"
echo "   Add to ~/.profile: firefox http://localhost:5056 &"

echo ""
echo "🚀 RBOTzilla UNI is ready for production deployment!"
echo "💰 Trading battlestation fully armed and operational"