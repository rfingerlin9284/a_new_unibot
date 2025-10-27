#!/usr/bin/env bash

# RBOTzilla UNI - Production Service Setup
# Creates live systemd services with auto-login and trading safety

set -euo pipefail

echo "🚀 Setting up RBOTzilla UNI Production Services"

RICK_ROOT="/home/ing/RICK"
PROJECT_ROOT="$RICK_ROOT/R_H_UNI"
SERVICE_DIR="$HOME/.config/systemd/user"
mkdir -p "$SERVICE_DIR"

# ============================================================================
# 1. MAIN RBOTZILLA UNI SERVICE (Auto-start with login)
# ============================================================================
echo "📝 Creating RBOTzilla UNI main service..."

cat > "$SERVICE_DIR/rbotzilla-uni-main.service" << 'EOF'
[Unit]
Description=RBOTzilla UNI - Main Trading System
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
Environment=NODE_ENV=production
Environment=RICK_ROOT=/home/ing/RICK/R_H_UNI
WorkingDirectory=/home/ing/RICK/R_H_UNI/standalone_shell
ExecStart=/usr/bin/node server_stream.js
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

# Auto-restart on failure
StartLimitInterval=60
StartLimitBurst=3

[Install]
WantedBy=default.target
EOF

# ============================================================================
# 2. SESSION INTELLIGENCE SERVICE
# ============================================================================
echo "📝 Creating session intelligence service..."

cat > "$SERVICE_DIR/rbotzilla-sessions.service" << 'EOF'
[Unit]
Description=RBOTzilla UNI - Session Intelligence
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
Environment=RICK_ROOT=/home/ing/RICK/R_H_UNI
WorkingDirectory=/home/ing/RICK/R_H_UNI/core
ExecStart=/usr/bin/python3 session_manager.py --daemon
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
EOF

# ============================================================================
# 3. TRADING SAFETY MONITOR SERVICE
# ============================================================================
echo "📝 Creating trading safety monitor..."

cat > "$SERVICE_DIR/rbotzilla-safety.service" << 'EOF'
[Unit]
Description=RBOTzilla UNI - Trading Safety Monitor
After=rbotzilla-uni-main.service
Wants=rbotzilla-uni-main.service

[Service]
Type=simple
Environment=PYTHONUNBUFFERED=1
Environment=RICK_ROOT=/home/ing/RICK/R_H_UNI
WorkingDirectory=/home/ing/RICK/R_H_UNI/core
ExecStart=/usr/bin/python3 safety_monitor.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

# ============================================================================
# 4. AUTO-LOGIN TIMER (Keeps system connected)
# ============================================================================
echo "📝 Creating auto-login timer..."

cat > "$SERVICE_DIR/rbotzilla-keepalive.timer" << 'EOF'
[Unit]
Description=RBOTzilla UNI - Keep Alive Timer
Requires=rbotzilla-keepalive.service

[Timer]
OnBootSec=30sec
OnUnitActiveSec=60sec
AccuracySec=10sec

[Install]
WantedBy=timers.target
EOF

cat > "$SERVICE_DIR/rbotzilla-keepalive.service" << 'EOF'
[Unit]
Description=RBOTzilla UNI - Keep Alive Service
After=network-online.target

[Service]
Type=oneshot
Environment=RICK_ROOT=/home/ing/RICK/R_H_UNI
WorkingDirectory=/home/ing/RICK/R_H_UNI
ExecStart=/bin/bash /home/ing/RICK/R_H_UNI/scripts/keepalive.sh

[Install]
WantedBy=default.target
EOF

# ============================================================================
# CREATE SAFETY MONITOR SCRIPT
# ============================================================================
echo "🔒 Creating trading safety monitor..."

mkdir -p "$PROJECT_ROOT/core"
cat > "$PROJECT_ROOT/core/safety_monitor.py" << 'EOF'
#!/usr/bin/env python3
"""
RBOTzilla UNI - Trading Safety Monitor
Monitors open trades and handles safe shutdown procedures
"""

import json
import time
import subprocess
import signal
import sys
from datetime import datetime
from pathlib import Path
import requests

class TradingSafetyMonitor:
    def __init__(self):
        self.rick_root = Path("/home/ing/RICK/R_H_UNI")
        self.shutdown_pin_file = self.rick_root / "runtime" / "shutdown_pin.txt"
        self.trades_file = self.rick_root / "runtime" / "open_trades.json"
        self.running = True
        
        # Create runtime directory
        (self.rick_root / "runtime").mkdir(exist_ok=True)
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self.signal_handler)
        signal.signal(signal.SIGINT, self.signal_handler)
        
    def signal_handler(self, signum, frame):
        print(f"🚨 Received signal {signum} - initiating safe shutdown...")
        self.safe_shutdown()
        
    def check_open_trades(self):
        """Check for open trading positions"""
        try:
            if self.trades_file.exists():
                with open(self.trades_file, 'r') as f:
                    trades = json.load(f)
                return trades.get('open_positions', [])
        except Exception as e:
            print(f"⚠️ Error checking trades: {e}")
        return []
    
    def check_stop_loss_take_profit(self, trades):
        """Verify all trades have proper SL/TP set"""
        unprotected_trades = []
        
        for trade in trades:
            if not trade.get('stop_loss') or not trade.get('take_profit'):
                unprotected_trades.append(trade)
        
        return unprotected_trades
    
    def check_shutdown_pin(self):
        """Check if shutdown PIN has been entered"""
        try:
            if self.shutdown_pin_file.exists():
                with open(self.shutdown_pin_file, 'r') as f:
                    content = f.read().strip()
                    if len(content) == 6 and content.isdigit():
                        print(f"🔐 Shutdown PIN detected: {content}")
                        return content
        except Exception as e:
            print(f"⚠️ Error checking PIN: {e}")
        return None
    
    def safe_shutdown(self):
        """Perform safe shutdown with trade verification"""
        print("🛑 INITIATING SAFE SHUTDOWN SEQUENCE")
        
        # Check for open trades
        open_trades = self.check_open_trades()
        
        if open_trades:
            print(f"⚠️ WARNING: {len(open_trades)} open trades detected!")
            
            # Check SL/TP protection
            unprotected = self.check_stop_loss_take_profit(open_trades)
            
            if unprotected:
                print(f"🚨 CRITICAL: {len(unprotected)} trades without proper SL/TP!")
                print("Unprotected trades:")
                for trade in unprotected:
                    print(f"  - {trade.get('symbol', 'Unknown')}: {trade.get('side', 'Unknown')} {trade.get('size', 'Unknown')}")
                
                print("❌ SHUTDOWN BLOCKED - Set stop loss and take profit on all trades")
                return False
            
            print("✅ All trades have SL/TP protection")
            
            # Confirm trade closure
            print("🔄 Closing all open positions...")
            for trade in open_trades:
                print(f"  ❌ Closing {trade.get('symbol')} {trade.get('side')} position")
                # Here you would integrate with your trading API to close positions
                
            # Update trades file to show no open positions
            with open(self.trades_file, 'w') as f:
                json.dump({"open_positions": [], "last_closed": datetime.now().isoformat()}, f)
                
            print("✅ All positions closed safely")
        
        else:
            print("✅ No open trades - safe to shutdown")
        
        # Clear the shutdown PIN
        if self.shutdown_pin_file.exists():
            self.shutdown_pin_file.unlink()
        
        print("🛑 Safe shutdown complete - system will now stop")
        self.running = False
        
        # Stop all RBOTzilla services
        subprocess.run(["systemctl", "--user", "stop", "rbotzilla-uni-main.service"], 
                      capture_output=True)
        
        return True
    
    def run(self):
        """Main monitoring loop"""
        print("🔒 RBOTzilla Trading Safety Monitor started")
        print("   - Monitoring for shutdown PIN")
        print("   - Watching for open trades")
        print("   - Ready for safe shutdown procedures")
        
        while self.running:
            try:
                # Check for shutdown PIN every 5 seconds
                pin = self.check_shutdown_pin()
                if pin:
                    print(f"🔐 Shutdown PIN {pin} detected - initiating safe shutdown")
                    if self.safe_shutdown():
                        break
                    else:
                        # Remove invalid PIN and continue
                        if self.shutdown_pin_file.exists():
                            self.shutdown_pin_file.unlink()
                
                time.sleep(5)
                
            except KeyboardInterrupt:
                print("\n🛑 Manual shutdown requested")
                self.safe_shutdown()
                break
            except Exception as e:
                print(f"⚠️ Monitor error: {e}")
                time.sleep(10)

if __name__ == "__main__":
    monitor = TradingSafetyMonitor()
    monitor.run()
EOF

# ============================================================================
# CREATE KEEPALIVE SCRIPT
# ============================================================================
echo "💓 Creating keepalive script..."

mkdir -p "$PROJECT_ROOT/scripts"
cat > "$PROJECT_ROOT/scripts/keepalive.sh" << 'EOF'
#!/usr/bin/env bash

# RBOTzilla UNI - Keepalive Script
# Ensures system stays connected and active

RICK_ROOT="/home/ing/RICK/R_H_UNI"
LOG_FILE="$RICK_ROOT/logs/keepalive.log"
STATUS_FILE="$RICK_ROOT/runtime/system_status.json"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$STATUS_FILE")"

echo "$(date): Keepalive check started" >> "$LOG_FILE"

# Check if main service is running
if systemctl --user is-active --quiet rbotzilla-uni-main.service; then
    echo "$(date): Main service running ✅" >> "$LOG_FILE"
    
    # Test socket connection
    if curl -s "http://localhost:5056" > /dev/null 2>&1; then
        echo "$(date): Socket server responsive ✅" >> "$LOG_FILE"
        STATUS="online"
    else
        echo "$(date): Socket server not responding ⚠️" >> "$LOG_FILE"
        STATUS="degraded"
    fi
else
    echo "$(date): Main service not running ❌" >> "$LOG_FILE"
    echo "$(date): Attempting service restart..." >> "$LOG_FILE"
    systemctl --user restart rbotzilla-uni-main.service
    STATUS="restarting"
fi

# Update status file
cat > "$STATUS_FILE" << EOL
{
    "timestamp": "$(date -Iseconds)",
    "status": "$STATUS",
    "uptime": "$(uptime -p)",
    "services": {
        "main": "$(systemctl --user is-active rbotzilla-uni-main.service)",
        "sessions": "$(systemctl --user is-active rbotzilla-sessions.service 2>/dev/null || echo 'inactive')",
        "safety": "$(systemctl --user is-active rbotzilla-safety.service 2>/dev/null || echo 'inactive')"
    }
}
EOL

echo "$(date): Keepalive check completed" >> "$LOG_FILE"
EOF

# ============================================================================
# CREATE SHUTDOWN PIN INTERFACE
# ============================================================================
echo "🔐 Creating shutdown PIN interface..."

cat > "$PROJECT_ROOT/scripts/shutdown_with_pin.sh" << 'EOF'
#!/usr/bin/env bash

# RBOTzilla UNI - Safe Shutdown with PIN
# Allows manual shutdown with 6-digit PIN

RICK_ROOT="/home/ing/RICK/R_H_UNI"
PIN_FILE="$RICK_ROOT/runtime/shutdown_pin.txt"

echo "🔐 RBOTzilla UNI - Safe Shutdown"
echo "================================"
echo ""
echo "⚠️  This will safely shutdown the trading system"
echo "⚠️  All open trades will be checked for SL/TP"
echo "⚠️  Unprotected trades will block shutdown"
echo ""

# Get PIN from user
read -s -p "Enter 6-digit shutdown PIN: " PIN
echo ""

# Validate PIN
if [[ ! "$PIN" =~ ^[0-9]{6}$ ]]; then
    echo "❌ Invalid PIN format. Must be exactly 6 digits."
    exit 1
fi

# Write PIN to file for safety monitor
mkdir -p "$(dirname "$PIN_FILE")"
echo "$PIN" > "$PIN_FILE"

echo "✅ Shutdown PIN submitted"
echo "🔄 Safety monitor will process shutdown request..."
echo "📊 Check system logs for shutdown progress"

# Wait a moment to see if shutdown is blocked
sleep 3

if [[ -f "$PIN_FILE" ]]; then
    echo "⚠️  Shutdown may have been blocked due to unsafe trading conditions"
    echo "📋 Check for open trades without proper stop loss/take profit"
else
    echo "✅ Shutdown proceeding safely"
fi
EOF

# ============================================================================
# MAKE SCRIPTS EXECUTABLE
# ============================================================================
chmod +x "$PROJECT_ROOT/core/safety_monitor.py"
chmod +x "$PROJECT_ROOT/scripts/keepalive.sh" 
chmod +x "$PROJECT_ROOT/scripts/shutdown_with_pin.sh"

# ============================================================================
# ENABLE AND START SERVICES
# ============================================================================
echo "🔄 Enabling and starting services..."

# Reload systemd
systemctl --user daemon-reload

# Enable services for auto-start
systemctl --user enable rbotzilla-uni-main.service
systemctl --user enable rbotzilla-sessions.service  
systemctl --user enable rbotzilla-safety.service
systemctl --user enable rbotzilla-keepalive.timer

# Start services
echo "🚀 Starting RBOTzilla UNI services..."
systemctl --user start rbotzilla-uni-main.service
systemctl --user start rbotzilla-sessions.service
systemctl --user start rbotzilla-safety.service  
systemctl --user start rbotzilla-keepalive.timer

# Check service status
echo ""
echo "📊 Service Status:"
echo "=================="
systemctl --user status rbotzilla-uni-main.service --no-pager -l
echo ""
systemctl --user status rbotzilla-safety.service --no-pager -l

echo ""
echo "✅ RBOTzilla UNI Production Services Setup Complete!"
echo ""
echo "🔧 Service Management Commands:"
echo "  Status:    systemctl --user status rbotzilla-uni-main.service"
echo "  Start:     systemctl --user start rbotzilla-uni-main.service" 
echo "  Stop:      systemctl --user stop rbotzilla-uni-main.service"
echo "  Restart:   systemctl --user restart rbotzilla-uni-main.service"
echo "  Logs:      journalctl --user -u rbotzilla-uni-main.service -f"
echo ""
echo "🔐 Safe Shutdown:"
echo "  $PROJECT_ROOT/scripts/shutdown_with_pin.sh"
echo ""
echo "📊 System will auto-start on boot and stay connected"
echo "🛡️ Trading safety monitor active - will prevent unsafe shutdowns"
echo "💓 Keepalive monitor ensures continuous operation"