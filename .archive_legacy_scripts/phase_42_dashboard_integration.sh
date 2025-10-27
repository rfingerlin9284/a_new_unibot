#!/bin/bash

# PHASE 42: Dashboard Integration & Concurrency Management
# Integrates 54 instruments with trading dashboard and implements concurrency controls

echo "🚀 Starting Phase 42: Dashboard Integration & Concurrency Management"
echo "Integrating 54 instruments with live trading system..."

# Create dashboard configuration directory
mkdir -p /home/ing/RICK/R_H_UNI/dashboard/config
mkdir -p /home/ing/RICK/R_H_UNI/dashboard/toggles
mkdir -p /home/ing/RICK/R_H_UNI/dashboard/widgets

# Create instrument toggle configuration
cat > /home/ing/RICK/R_H_UNI/dashboard/config/instrument_toggles.json << 'EOF'
{
  "fx_instruments": {
    "enabled": true,
    "active_pairs": [],
    "concurrency_limit": 6,
    "risk_per_trade": 0.02,
    "venue": "oanda"
  },
  "crypto_spot": {
    "enabled": true,
    "active_pairs": [],
    "concurrency_limit": 8,
    "risk_per_trade": 0.03,
    "venue": "coinbase"
  },
  "derivatives": {
    "enabled": true,
    "active_pairs": [],
    "concurrency_limit": 10,
    "risk_per_trade": 0.025,
    "venue": "binance_futures"
  },
  "global_settings": {
    "max_total_concurrent": 24,
    "emergency_stop": false,
    "session_awareness": true,
    "weekend_crypto_boost": true
  }
}
EOF

# Create dashboard HTML with 54-instrument grid
cat > /home/ing/RICK/R_H_UNI/dashboard/trading_dashboard.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RBOT ZILLA UNI - 54 Instrument Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace; 
            background: #0a0a0a; 
            color: #00ff00; 
            overflow-x: hidden;
        }
        
        .header {
            background: linear-gradient(90deg, #1a1a1a, #2a2a2a);
            padding: 1rem;
            border-bottom: 2px solid #00ff00;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .title { font-size: 1.5rem; font-weight: bold; }
        .status { font-size: 0.9rem; }
        
        .controls {
            background: #1a1a1a;
            padding: 1rem;
            border-bottom: 1px solid #333;
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }
        
        .control-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .control-group label { font-size: 0.8rem; color: #888; }
        
        .toggle-switch {
            position: relative;
            width: 60px;
            height: 30px;
            background: #333;
            border-radius: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .toggle-switch.active { background: #00ff00; }
        
        .toggle-switch::after {
            content: '';
            position: absolute;
            width: 26px;
            height: 26px;
            background: white;
            border-radius: 50%;
            top: 2px;
            left: 2px;
            transition: all 0.3s;
        }
        
        .toggle-switch.active::after { left: 32px; }
        
        .instrument-grid {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 1rem;
            padding: 1rem;
            height: calc(100vh - 200px);
            overflow-y: auto;
        }
        
        .instrument-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 1rem;
            transition: all 0.3s;
            cursor: pointer;
            position: relative;
        }
        
        .instrument-card:hover { border-color: #00ff00; transform: scale(1.02); }
        .instrument-card.active { border-color: #00ff00; background: #0f2f0f; }
        .instrument-card.trading { border-color: #ff6600; background: #2f1f0f; }
        
        .instrument-symbol { font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem; }
        .instrument-venue { font-size: 0.8rem; color: #888; margin-bottom: 0.5rem; }
        .instrument-status { font-size: 0.9rem; margin-bottom: 0.5rem; }
        .instrument-pnl { font-size: 1rem; font-weight: bold; }
        
        .venue-fx { border-left: 4px solid #4169E1; }
        .venue-spot { border-left: 4px solid #FFD700; }
        .venue-perp { border-left: 4px solid #FF4500; }
        
        .pnl-positive { color: #00ff00; }
        .pnl-negative { color: #ff4444; }
        .pnl-neutral { color: #888; }
        
        .concurrency-bar {
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            background: #00ff00;
            transition: all 0.3s;
        }
        
        @media (max-width: 1200px) { .instrument-grid { grid-template-columns: repeat(4, 1fr); } }
        @media (max-width: 800px) { .instrument-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 500px) { .instrument-grid { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="header">
        <div class="title">🤖 RBOT ZILLA UNI - 54 Instrument Dashboard</div>
        <div class="status">
            <span id="session-status">Loading...</span> | 
            <span id="active-count">0/54</span> | 
            <span id="concurrent-count">0/24</span>
        </div>
    </div>
    
    <div class="controls">
        <div class="control-group">
            <label>FX Trading</label>
            <div class="toggle-switch" id="fx-toggle"></div>
        </div>
        <div class="control-group">
            <label>Crypto Spot</label>
            <div class="toggle-switch" id="spot-toggle"></div>
        </div>
        <div class="control-group">
            <label>Derivatives</label>
            <div class="toggle-switch" id="perp-toggle"></div>
        </div>
        <div class="control-group">
            <label>Session Awareness</label>
            <div class="toggle-switch active" id="session-toggle"></div>
        </div>
        <div class="control-group">
            <label>Weekend Crypto Boost</label>
            <div class="toggle-switch active" id="weekend-toggle"></div>
        </div>
        <div class="control-group">
            <label>Emergency Stop</label>
            <div class="toggle-switch" id="emergency-toggle"></div>
        </div>
    </div>
    
    <div class="instrument-grid" id="instrument-grid">
        <!-- Instruments will be populated by JavaScript -->
    </div>

    <script>
        class TradingDashboard {
            constructor() {
                this.instruments = [];
                this.config = {};
                this.activeTrades = new Set();
                this.init();
            }
            
            async init() {
                await this.loadConfig();
                await this.loadInstruments();
                this.setupEventListeners();
                this.startSessionMonitoring();
                this.renderInstruments();
                console.log('📊 Trading Dashboard initialized with 54 instruments');
            }
            
            async loadConfig() {
                try {
                    const response = await fetch('/dashboard/config/instrument_toggles.json');
                    this.config = await response.json();
                } catch (error) {
                    console.warn('Using default config:', error);
                    this.config = {
                        fx_instruments: { enabled: false, concurrency_limit: 6 },
                        crypto_spot: { enabled: false, concurrency_limit: 8 },
                        derivatives: { enabled: false, concurrency_limit: 10 },
                        global_settings: { max_total_concurrent: 24 }
                    };
                }
            }
            
            async loadInstruments() {
                try {
                    const response = await fetch('/configs/pairs_config.json');
                    const data = await response.json();
                    
                    // Convert to unified format
                    this.instruments = [
                        ...data.oanda_pairs.map(pair => ({
                            symbol: pair,
                            venue: 'OANDA',
                            type: 'fx',
                            status: 'inactive',
                            pnl: 0
                        })),
                        ...data.coinbase_spot.map(pair => ({
                            symbol: pair,
                            venue: 'Coinbase',
                            type: 'spot',
                            status: 'inactive',
                            pnl: 0
                        })),
                        ...data.derivative_pairs.map(pair => ({
                            symbol: pair,
                            venue: 'Derivatives',
                            type: 'perp',
                            status: 'inactive',
                            pnl: 0
                        }))
                    ];
                } catch (error) {
                    console.error('Failed to load instruments:', error);
                }
            }
            
            setupEventListeners() {
                // Toggle switches
                document.getElementById('fx-toggle').onclick = () => this.toggleVenue('fx');
                document.getElementById('spot-toggle').onclick = () => this.toggleVenue('spot');
                document.getElementById('perp-toggle').onclick = () => this.toggleVenue('perp');
                document.getElementById('session-toggle').onclick = () => this.toggleSession();
                document.getElementById('weekend-toggle').onclick = () => this.toggleWeekend();
                document.getElementById('emergency-toggle').onclick = () => this.emergencyStop();
            }
            
            toggleVenue(venueType) {
                const toggle = document.getElementById(`${venueType === 'fx' ? 'fx' : venueType === 'spot' ? 'spot' : 'perp'}-toggle`);
                toggle.classList.toggle('active');
                
                const isActive = toggle.classList.contains('active');
                this.config[`${venueType === 'fx' ? 'fx_instruments' : venueType === 'spot' ? 'crypto_spot' : 'derivatives'}`].enabled = isActive;
                
                // Update instrument states
                this.instruments.filter(i => i.type === venueType).forEach(instrument => {
                    instrument.status = isActive ? 'active' : 'inactive';
                });
                
                this.renderInstruments();
                console.log(`${venueType.toUpperCase()} venues ${isActive ? 'enabled' : 'disabled'}`);
            }
            
            toggleSession() {
                const toggle = document.getElementById('session-toggle');
                toggle.classList.toggle('active');
                this.config.global_settings.session_awareness = toggle.classList.contains('active');
                console.log('Session awareness:', this.config.global_settings.session_awareness);
            }
            
            toggleWeekend() {
                const toggle = document.getElementById('weekend-toggle');
                toggle.classList.toggle('active');
                this.config.global_settings.weekend_crypto_boost = toggle.classList.contains('active');
                console.log('Weekend crypto boost:', this.config.global_settings.weekend_crypto_boost);
            }
            
            emergencyStop() {
                const toggle = document.getElementById('emergency-toggle');
                toggle.classList.toggle('active');
                
                if (toggle.classList.contains('active')) {
                    // Stop all trading
                    this.instruments.forEach(i => i.status = 'stopped');
                    this.activeTrades.clear();
                    console.log('🚨 EMERGENCY STOP ACTIVATED');
                } else {
                    // Resume normal operation
                    this.instruments.forEach(i => i.status = 'inactive');
                    console.log('✅ Emergency stop cleared');
                }
                
                this.renderInstruments();
            }
            
            toggleInstrument(index) {
                const instrument = this.instruments[index];
                const venueConfig = this.getVenueConfig(instrument.type);
                
                if (!venueConfig.enabled) {
                    console.log(`${instrument.type.toUpperCase()} venue not enabled`);
                    return;
                }
                
                const totalConcurrent = this.activeTrades.size;
                const venueConcurrent = Array.from(this.activeTrades).filter(i => 
                    this.instruments[i].type === instrument.type
                ).length;
                
                if (instrument.status === 'inactive') {
                    // Check concurrency limits
                    if (totalConcurrent >= this.config.global_settings.max_total_concurrent) {
                        console.log('Global concurrency limit reached');
                        return;
                    }
                    
                    if (venueConcurrent >= venueConfig.concurrency_limit) {
                        console.log(`${instrument.type.toUpperCase()} concurrency limit reached`);
                        return;
                    }
                    
                    instrument.status = 'trading';
                    this.activeTrades.add(index);
                    console.log(`Started trading ${instrument.symbol}`);
                } else if (instrument.status === 'trading') {
                    instrument.status = 'active';
                    this.activeTrades.delete(index);
                    console.log(`Stopped trading ${instrument.symbol}`);
                }
                
                this.renderInstruments();
                this.updateStatus();
            }
            
            getVenueConfig(type) {
                const mapping = {
                    'fx': 'fx_instruments',
                    'spot': 'crypto_spot',
                    'perp': 'derivatives'
                };
                return this.config[mapping[type]] || { enabled: false, concurrency_limit: 0 };
            }
            
            renderInstruments() {
                const grid = document.getElementById('instrument-grid');
                grid.innerHTML = '';
                
                this.instruments.forEach((instrument, index) => {
                    const card = document.createElement('div');
                    card.className = `instrument-card venue-${instrument.type} ${instrument.status}`;
                    card.onclick = () => this.toggleInstrument(index);
                    
                    const pnlClass = instrument.pnl > 0 ? 'pnl-positive' : 
                                    instrument.pnl < 0 ? 'pnl-negative' : 'pnl-neutral';
                    
                    card.innerHTML = `
                        <div class="instrument-symbol">${instrument.symbol}</div>
                        <div class="instrument-venue">${instrument.venue}</div>
                        <div class="instrument-status">Status: ${instrument.status.toUpperCase()}</div>
                        <div class="instrument-pnl ${pnlClass}">P&L: ${instrument.pnl >= 0 ? '+' : ''}${instrument.pnl.toFixed(2)}%</div>
                        <div class="concurrency-bar" style="width: ${this.getConcurrencyPercentage(instrument.type)}%"></div>
                    `;
                    
                    grid.appendChild(card);
                });
            }
            
            getConcurrencyPercentage(type) {
                const venueConfig = this.getVenueConfig(type);
                const active = Array.from(this.activeTrades).filter(i => 
                    this.instruments[i].type === type
                ).length;
                return (active / venueConfig.concurrency_limit) * 100;
            }
            
            startSessionMonitoring() {
                this.updateSessionStatus();
                setInterval(() => this.updateSessionStatus(), 60000); // Update every minute
            }
            
            updateSessionStatus() {
                const now = new Date();
                const utcHour = now.getUTCHours();
                const weekday = now.getUTCDay();
                
                let sessionText = '';
                if (weekday === 0 || weekday === 6) {
                    sessionText = '🌙 Weekend - Crypto Only';
                } else if (utcHour >= 6 && utcHour <= 22) {
                    sessionText = '🌍 Forex + Crypto Active';
                } else {
                    sessionText = '🌃 Asian Session - Crypto Focus';
                }
                
                document.getElementById('session-status').textContent = sessionText;
                this.updateStatus();
            }
            
            updateStatus() {
                const activeCount = this.instruments.filter(i => i.status !== 'inactive').length;
                const tradingCount = this.activeTrades.size;
                
                document.getElementById('active-count').textContent = `${activeCount}/54`;
                document.getElementById('concurrent-count').textContent = `${tradingCount}/${this.config.global_settings.max_total_concurrent}`;
            }
        }
        
        // Initialize dashboard when page loads
        window.addEventListener('load', () => {
            new TradingDashboard();
        });
    </script>
</body>
</html>
EOF

# Create dashboard server
cat > /home/ing/RICK/R_H_UNI/dashboard/dashboard_server.js << 'EOF'
const express = require('express');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 8080;

// Serve static files
app.use(express.static('/home/ing/RICK/R_H_UNI/dashboard'));
app.use('/configs', express.static('/home/ing/RICK/R_H_UNI/configs'));

// API endpoints for dashboard data
app.get('/api/instruments', (req, res) => {
    try {
        const configPath = '/home/ing/RICK/R_H_UNI/configs/pairs_config.json';
        const data = JSON.parse(fs.readFileSync(configPath, 'utf8'));
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to load instruments' });
    }
});

app.get('/api/toggles', (req, res) => {
    try {
        const togglePath = '/home/ing/RICK/R_H_UNI/dashboard/config/instrument_toggles.json';
        const data = JSON.parse(fs.readFileSync(togglePath, 'utf8'));
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: 'Failed to load toggle config' });
    }
});

app.post('/api/toggles', express.json(), (req, res) => {
    try {
        const togglePath = '/home/ing/RICK/R_H_UNI/dashboard/config/instrument_toggles.json';
        fs.writeFileSync(togglePath, JSON.stringify(req.body, null, 2));
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: 'Failed to save toggle config' });
    }
});

// WebSocket for real-time updates
const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8081 });

wss.on('connection', (ws) => {
    console.log('📡 Dashboard client connected');
    
    // Send initial data
    ws.send(JSON.stringify({
        type: 'init',
        timestamp: new Date().toISOString()
    }));
    
    // Simulate real-time updates
    const interval = setInterval(() => {
        ws.send(JSON.stringify({
            type: 'market_update',
            data: {
                // Simulate P&L updates
                instruments: Math.floor(Math.random() * 54),
                pnl: (Math.random() - 0.5) * 10
            },
            timestamp: new Date().toISOString()
        }));
    }, 5000);
    
    ws.on('close', () => {
        console.log('📡 Dashboard client disconnected');
        clearInterval(interval);
    });
});

app.listen(PORT, () => {
    console.log(`🚀 Phase 42 Dashboard Server running on http://localhost:${PORT}`);
    console.log(`📡 WebSocket server running on ws://localhost:8081`);
    console.log(`📊 Access the 54-instrument dashboard at http://localhost:${PORT}/trading_dashboard.html`);
});
EOF

# Create concurrency manager service
cat > /home/ing/RICK/R_H_UNI/core/concurrency_manager.py << 'EOF'
#!/usr/bin/env python3
"""
RBOT ZILLA UNI - Concurrency Manager
Manages trading concurrency limits across 54 instruments
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Set
import logging

class ConcurrencyManager:
    def __init__(self, config_path: str = '/home/ing/RICK/R_H_UNI/dashboard/config/instrument_toggles.json'):
        self.config_path = config_path
        self.config = {}
        self.active_trades: Set[str] = set()
        self.venue_trades: Dict[str, Set[str]] = {
            'fx': set(),
            'spot': set(), 
            'perp': set()
        }
        self.lock = threading.Lock()
        self.load_config()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load concurrency configuration"""
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.logger.warning("Config not found, using defaults")
            self.config = {
                "fx_instruments": {"concurrency_limit": 6},
                "crypto_spot": {"concurrency_limit": 8},
                "derivatives": {"concurrency_limit": 10},
                "global_settings": {"max_total_concurrent": 24}
            }
    
    def can_start_trade(self, instrument: str, venue_type: str) -> bool:
        """Check if new trade can be started given concurrency limits"""
        with self.lock:
            # Check global limit
            if len(self.active_trades) >= self.config['global_settings']['max_total_concurrent']:
                self.logger.warning(f"Global concurrency limit reached: {len(self.active_trades)}")
                return False
            
            # Check venue-specific limit
            venue_key = f"{venue_type}_{'instruments' if venue_type == 'fx' else venue_type}"
            if venue_key in self.config:
                limit = self.config[venue_key]['concurrency_limit']
                current = len(self.venue_trades[venue_type])
                if current >= limit:
                    self.logger.warning(f"{venue_type.upper()} concurrency limit reached: {current}/{limit}")
                    return False
            
            return True
    
    def start_trade(self, instrument: str, venue_type: str) -> bool:
        """Start a new trade if concurrency allows"""
        if self.can_start_trade(instrument, venue_type):
            with self.lock:
                self.active_trades.add(instrument)
                self.venue_trades[venue_type].add(instrument)
                self.logger.info(f"Started trade: {instrument} ({venue_type})")
                self.log_status()
                return True
        return False
    
    def stop_trade(self, instrument: str, venue_type: str) -> bool:
        """Stop an active trade"""
        with self.lock:
            if instrument in self.active_trades:
                self.active_trades.remove(instrument)
                self.venue_trades[venue_type].discard(instrument)
                self.logger.info(f"Stopped trade: {instrument} ({venue_type})")
                self.log_status()
                return True
            return False
    
    def emergency_stop_all(self):
        """Emergency stop all trading"""
        with self.lock:
            count = len(self.active_trades)
            self.active_trades.clear()
            for venue in self.venue_trades:
                self.venue_trades[venue].clear()
            self.logger.critical(f"EMERGENCY STOP: Cleared {count} active trades")
    
    def get_status(self) -> Dict:
        """Get current concurrency status"""
        with self.lock:
            return {
                'total_active': len(self.active_trades),
                'max_total': self.config['global_settings']['max_total_concurrent'],
                'venue_breakdown': {
                    'fx': {
                        'active': len(self.venue_trades['fx']),
                        'limit': self.config.get('fx_instruments', {}).get('concurrency_limit', 0)
                    },
                    'spot': {
                        'active': len(self.venue_trades['spot']), 
                        'limit': self.config.get('crypto_spot', {}).get('concurrency_limit', 0)
                    },
                    'perp': {
                        'active': len(self.venue_trades['perp']),
                        'limit': self.config.get('derivatives', {}).get('concurrency_limit', 0)
                    }
                },
                'active_instruments': list(self.active_trades)
            }
    
    def log_status(self):
        """Log current status"""
        status = self.get_status()
        self.logger.info(f"Concurrency Status: {status['total_active']}/{status['max_total']} total | "
                        f"FX: {status['venue_breakdown']['fx']['active']}/{status['venue_breakdown']['fx']['limit']} | "
                        f"Spot: {status['venue_breakdown']['spot']['active']}/{status['venue_breakdown']['spot']['limit']} | "
                        f"Perp: {status['venue_breakdown']['perp']['active']}/{status['venue_breakdown']['perp']['limit']}")

def main():
    """Test the concurrency manager"""
    manager = ConcurrencyManager()
    
    print("🚀 RBOT ZILLA UNI - Concurrency Manager Test")
    print(f"📊 Initial Status: {manager.get_status()}")
    
    # Test adding trades
    test_instruments = [
        ('EUR/USD', 'fx'),
        ('BTC/USD', 'spot'), 
        ('BTC-PERP', 'perp'),
        ('GBP/USD', 'fx'),
        ('ETH/USD', 'spot')
    ]
    
    for instrument, venue in test_instruments:
        result = manager.start_trade(instrument, venue)
        print(f"✅ Started {instrument}: {result}")
        time.sleep(0.1)
    
    print(f"\n📊 Final Status: {manager.get_status()}")
    
    # Test emergency stop
    print("\n🚨 Testing emergency stop...")
    manager.emergency_stop_all()
    print(f"📊 After Emergency Stop: {manager.get_status()}")

if __name__ == "__main__":
    main()
EOF

# Make scripts executable
chmod +x /home/ing/RICK/R_H_UNI/core/concurrency_manager.py

# Install dashboard dependencies
echo "📦 Installing dashboard dependencies..."
cd /home/ing/RICK/R_H_UNI/dashboard
if [ ! -f package.json ]; then
    npm init -y
fi
npm install express ws

echo "✅ Phase 42 Complete: Dashboard Integration & Concurrency Management"
echo ""
echo "Created components:"
echo "  📊 Trading Dashboard (54 instruments)"
echo "  🎛️ Instrument toggle controls"
echo "  ⚡ Concurrency management system"
echo "  🔧 Real-time WebSocket updates"
echo ""
echo "To start the dashboard:"
echo "  cd /home/ing/RICK/R_H_UNI/dashboard"
echo "  node dashboard_server.js"
echo ""
echo "Access at: http://localhost:8080/trading_dashboard.html"
echo ""
echo "🚀 Ready for Phase 43: Live Data Integration!"