#!/usr/bin/env bash
# ============================================================================
# HIVE REFLECTION ORCHESTRATOR - Installation & Setup Helper
# PIN: 841921 | Generated: 2025-10-20
# ============================================================================

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  HIVE MIND REFLECTION ORCHESTRATOR - Setup Helper              ║"
echo "║  30-Second Autonomous Trade Management                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    echo "❌ This script requires root privileges (for systemd installation)"
    echo "   Run with: sudo bash install_reflection_orchestrator.sh"
    exit 1
fi

PROJECT_ROOT="/home/ing/RICK/RICK_LIVE_PROTOTYPE"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_NAME="reflection_orchestrator"
SERVICE_FILE="$SYSTEMD_DIR/${SERVICE_NAME}.service"
TIMER_FILE="$SYSTEMD_DIR/${SERVICE_NAME}.timer"

echo "📋 Installation Plan:"
echo "  1. Copy systemd units to $SYSTEMD_DIR"
echo "  2. Reload systemd daemon"
echo "  3. Enable timer and service"
echo "  4. Start the service"
echo "  5. Verify installation"
echo ""

# ============================================================================
# STEP 1: COPY SYSTEMD UNITS
# ============================================================================

echo "Step 1: Installing systemd units..."

if [ ! -f "$PROJECT_ROOT/systemd/${SERVICE_NAME}.service" ]; then
    echo "❌ Error: Service file not found at $PROJECT_ROOT/systemd/${SERVICE_NAME}.service"
    exit 1
fi

if [ ! -f "$PROJECT_ROOT/systemd/${SERVICE_NAME}.timer" ]; then
    echo "❌ Error: Timer file not found at $PROJECT_ROOT/systemd/${SERVICE_NAME}.timer"
    exit 1
fi

# Copy files
cp "$PROJECT_ROOT/systemd/${SERVICE_NAME}.service" "$SERVICE_FILE"
cp "$PROJECT_ROOT/systemd/${SERVICE_NAME}.timer" "$TIMER_FILE"

# Set permissions
chmod 644 "$SERVICE_FILE"
chmod 644 "$TIMER_FILE"

echo "✅ Systemd units installed"
echo "   Service: $SERVICE_FILE"
echo "   Timer: $TIMER_FILE"
echo ""

# ============================================================================
# STEP 2: RELOAD SYSTEMD
# ============================================================================

echo "Step 2: Reloading systemd daemon..."
systemctl daemon-reload
echo "✅ Systemd daemon reloaded"
echo ""

# ============================================================================
# STEP 3: ENABLE SERVICE & TIMER
# ============================================================================

echo "Step 3: Enabling service and timer..."
systemctl enable "${SERVICE_NAME}.service"
systemctl enable "${SERVICE_NAME}.timer"
echo "✅ Service and timer enabled for auto-start"
echo ""

# ============================================================================
# STEP 4: START THE SERVICE
# ============================================================================

echo "Step 4: Starting reflection orchestrator..."

if systemctl start "${SERVICE_NAME}.timer"; then
    echo "✅ Timer started"
else
    echo "❌ Failed to start timer"
    exit 1
fi

sleep 2

if systemctl is-active --quiet "${SERVICE_NAME}.timer"; then
    echo "✅ Timer is active"
else
    echo "❌ Timer failed to start"
    systemctl status "${SERVICE_NAME}.timer"
    exit 1
fi

echo ""

# ============================================================================
# STEP 5: VERIFY INSTALLATION
# ============================================================================

echo "Step 5: Verifying installation..."
echo ""

echo "📋 Service Status:"
systemctl status "${SERVICE_NAME}.service" || true
echo ""

echo "📋 Timer Status:"
systemctl status "${SERVICE_NAME}.timer" || true
echo ""

echo "📋 Timer Schedule:"
systemctl list-timers "${SERVICE_NAME}.timer" || true
echo ""

echo "📋 Recent Logs:"
journalctl -u "${SERVICE_NAME}.service" -n 20 --no-pager || echo "No logs yet"
echo ""

# ============================================================================
# COMPLETION
# ============================================================================

echo "✅ Installation Complete!"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "🧠 HIVE REFLECTION ORCHESTRATOR STATUS"
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Service:       ${SERVICE_NAME}.service"
echo "Timer:         ${SERVICE_NAME}.timer"
echo "Interval:      Every 30 seconds"
echo "Environment:   practice (edit service file for live)"
echo "Status:        ✅ ACTIVE"
echo ""
echo "Useful Commands:"
echo "  systemctl status reflection_orchestrator.service"
echo "  systemctl status reflection_orchestrator.timer"
echo "  journalctl -u reflection_orchestrator.service -f     (follow logs)"
echo "  systemctl stop reflection_orchestrator.timer         (stop)"
echo "  systemctl start reflection_orchestrator.timer        (start)"
echo ""
echo "Makefile Integration:"
echo "  make reflection-status     Check status"
echo "  make reflection-logs       Tail logs"
echo "  make reflection-stop       Stop daemon"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 Next Steps:"
echo "  1. Monitor: tail -f /home/ing/RICK/RICK_LIVE_PROTOTYPE/narration.jsonl"
echo "  2. Check status: systemctl status reflection_orchestrator.timer"
echo "  3. View hive decisions: cat hive_status.json"
echo ""
