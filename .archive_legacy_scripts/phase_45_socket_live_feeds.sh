#!/usr/bin/env bash

# PHASE 45: Socket + Live Widget Feeds
# Adds Socket.IO real-time streaming to RBOTzilla UNI dashboard
# PIN-locked checkpoint for immutable deployment

set -euo pipefail

echo "🚀 Starting Phase 45: Socket + Live Widget Feeds"
echo "Adding real-time data streaming to dashboard fusion..."

SHELL_DIR="/home/ing/RICK/R_H_UNI/standalone_shell"
MOBILE_DIR="/home/ing/RICK/R_H_UNI/mobile_console"

# Phase 45.1 — Install Socket.IO and create streaming server
echo "📦 Phase 45.1: Installing Socket.IO dependencies..."
cd "$SHELL_DIR"

# Install socket.io
npm install socket.io

# Create real-time streaming server
cat > "$SHELL_DIR/server_stream.js" << 'EOF'
const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});

const PORT = 5056;

// Serve static files
app.use(express.static('.'));
app.use('/mobile_console', express.static('/home/ing/RICK/R_H_UNI/mobile_console'));

console.log('🔌 RBOT ZILLA UNI - Live Socket Server');
console.log(`🎯 Streaming TMUX feeds on port ${PORT}`);

// Market data simulation for widgets
const generateMarketData = () => {
  const instruments = ['EUR/USD', 'GBP/USD', 'BTC/USD', 'ETH/USD', 'SOL/USD'];
  const data = {};
  
  instruments.forEach(symbol => {
    data[symbol] = {
      price: (Math.random() * 100 + 1000).toFixed(4),
      change: (Math.random() - 0.5) * 10,
      volume: Math.floor(Math.random() * 1000000),
      spread: (Math.random() * 0.5).toFixed(4),
      timestamp: new Date().toISOString()
    };
  });
  
  return data;
};

// Trading session detection
const getSessionStatus = () => {
  const now = new Date();
  const utcHour = now.getUTCHours();
  const weekday = now.getUTCDay();
  
  let session = 'CLOSED';
  let description = '';
  
  if (weekday === 0 || weekday === 6) {
    session = 'WEEKEND';
    description = '🌙 Weekend - Crypto Alpha Mode';
  } else if (utcHour >= 22 || utcHour < 6) {
    session = 'ASIAN';
    description = '🌅 Asian Session - Tokyo/Sydney';
  } else if (utcHour >= 6 && utcHour < 14) {
    session = 'LONDON';
    description = '🌍 London Session - High Volatility';
  } else if (utcHour >= 14 && utcHour < 22) {
    session = 'NEWYORK';
    description = '🗽 New York Session - Major Volume';
  }
  
  return { session, description, utcHour, weekday };
};

// Risk metrics simulation
const generateRiskMetrics = () => {
  return {
    portfolio_var: (Math.random() * 0.05).toFixed(4),
    max_drawdown: (Math.random() * 0.15).toFixed(4),
    sharpe_ratio: (Math.random() * 3).toFixed(2),
    active_positions: Math.floor(Math.random() * 24),
    daily_pnl: (Math.random() - 0.5) * 10000,
    win_rate: (Math.random() * 0.4 + 0.5).toFixed(3)
  };
};

io.on('connection', (socket) => {
  console.log('📡 Client connected to live stream');
  
  // Send initial connection data
  socket.emit('stream-init', {
    message: '🤖 RBOTzilla UNI Live Stream Connected',
    timestamp: new Date().toISOString(),
    client_id: socket.id.substring(0, 8)
  });
  
  // TMUX feed streaming (every 2 seconds)
  const tmuxInterval = setInterval(() => {
    const proc = spawn('tmux', ['capture-pane', '-pJS-', '-t', '0'], {
      timeout: 1000
    });
    
    let tmuxOutput = '';
    
    proc.stdout.on('data', (data) => {
      tmuxOutput += data.toString();
    });
    
    proc.on('close', (code) => {
      if (tmuxOutput.length > 0) {
        socket.emit('tmux-update', {
          content: tmuxOutput.slice(-2000), // Last 2000 chars
          timestamp: new Date().toISOString(),
          lines: tmuxOutput.split('\n').length
        });
      }
    });
    
    proc.on('error', (err) => {
      socket.emit('tmux-update', {
        content: '🚫 TMUX stream unavailable\n📊 Simulation mode active...',
        timestamp: new Date().toISOString(),
        error: true
      });
    });
  }, 2000);
  
  // Market data streaming (every 1 second)
  const marketInterval = setInterval(() => {
    socket.emit('market-data', generateMarketData());
  }, 1000);
  
  // Session status updates (every 30 seconds)
  const sessionInterval = setInterval(() => {
    socket.emit('session-update', getSessionStatus());
  }, 30000);
  
  // Risk metrics updates (every 5 seconds)
  const riskInterval = setInterval(() => {
    socket.emit('risk-metrics', generateRiskMetrics());
  }, 5000);
  
  // Trading signals simulation (every 10 seconds)
  const signalInterval = setInterval(() => {
    const signals = [
      { symbol: 'EUR/USD', action: 'BUY', confidence: 0.85, reason: 'Bullish divergence' },
      { symbol: 'BTC/USD', action: 'SELL', confidence: 0.72, reason: 'Overbought RSI' },
      { symbol: 'GBP/USD', action: 'HOLD', confidence: 0.45, reason: 'Consolidation' }
    ];
    
    const randomSignal = signals[Math.floor(Math.random() * signals.length)];
    socket.emit('trading-signal', {
      ...randomSignal,
      timestamp: new Date().toISOString(),
      id: Math.random().toString(36).substr(2, 9)
    });
  }, 10000);
  
  // Send immediate session status on connect
  socket.emit('session-update', getSessionStatus());
  
  // Cleanup on disconnect
  socket.on('disconnect', () => {
    console.log('📡 Client disconnected from live stream');
    clearInterval(tmuxInterval);
    clearInterval(marketInterval);
    clearInterval(sessionInterval);
    clearInterval(riskInterval);
    clearInterval(signalInterval);
  });
  
  // Handle client requests
  socket.on('request-snapshot', () => {
    socket.emit('market-snapshot', {
      market_data: generateMarketData(),
      session_status: getSessionStatus(),
      risk_metrics: generateRiskMetrics(),
      timestamp: new Date().toISOString()
    });
  });
});

server.listen(PORT, () => {
  console.log(`🔌 Live socket streaming on http://localhost:${PORT}`);
  console.log('📊 Real-time feeds: TMUX, Market Data, Sessions, Risk Metrics');
  console.log('🎯 Widgets ready for live updates');
});
EOF

# Update package.json with stream script
echo "📝 Updating package.json with stream script..."
if [ -f package.json ]; then
  npx jq '.scripts.stream = "node server_stream.js"' package.json > tmp && mv tmp package.json
else
  cat > package.json << 'EOF'
{
  "name": "rbotzilla-uni-streaming",
  "version": "1.0.0",
  "description": "Live Socket.IO streaming for RBOTzilla UNI",
  "main": "server_stream.js",
  "scripts": {
    "start": "node server_stream.js",
    "stream": "node server_stream.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "socket.io": "^4.7.2",
    "ws": "^8.14.2",
    "interactjs": "^1.10.18"
  }
}
EOF
fi

# Phase 45.2 — Update mobile console with Socket.IO client
echo "📱 Phase 45.2: Integrating Socket.IO into mobile console..."

# First, let's check if the mobile console index.html exists and add Socket.IO
if [ -f "$MOBILE_DIR/index.html" ]; then
  # Add Socket.IO client script before closing body tag
  cat > "$MOBILE_DIR/socket_integration.html" << 'EOF'
<!-- Socket.IO Live Feed Integration -->
<script src="/socket.io/socket.io.js"></script>
<script>
// RBOTzilla UNI - Live Socket Integration
console.log('🔌 Initializing RBOTzilla UNI live feeds...');

const ioClient = io('http://localhost:5056', {
  transports: ['websocket', 'polling']
});

// Connection status
ioClient.on('connect', () => {
  console.log('📡 Connected to RBOTzilla live stream');
  document.getElementById('connection-status').textContent = '🟢 LIVE';
  ioClient.emit('request-snapshot'); // Get initial data
});

ioClient.on('disconnect', () => {
  console.log('📡 Disconnected from live stream');
  document.getElementById('connection-status').textContent = '🔴 OFFLINE';
});

// TMUX feed updates
ioClient.on('tmux-update', (data) => {
  const tmuxElement = document.getElementById('tmux-feed');
  if (tmuxElement) {
    tmuxElement.innerText = data.content;
    tmuxElement.scrollTop = tmuxElement.scrollHeight;
  }
  
  // Update timestamp
  const timestampEl = document.getElementById('tmux-timestamp');
  if (timestampEl) {
    timestampEl.textContent = new Date(data.timestamp).toLocaleTimeString();
  }
});

// Market data updates
ioClient.on('market-data', (data) => {
  Object.keys(data).forEach(symbol => {
    const priceEl = document.getElementById(`price-${symbol.replace('/', '-')}`);
    const changeEl = document.getElementById(`change-${symbol.replace('/', '-')}`);
    
    if (priceEl) {
      priceEl.textContent = data[symbol].price;
      priceEl.className = data[symbol].change > 0 ? 'price-up' : 'price-down';
    }
    
    if (changeEl) {
      changeEl.textContent = `${data[symbol].change > 0 ? '+' : ''}${data[symbol].change.toFixed(2)}%`;
      changeEl.className = data[symbol].change > 0 ? 'change-positive' : 'change-negative';
    }
  });
});

// Session status updates
ioClient.on('session-update', (data) => {
  const sessionEl = document.getElementById('session-status');
  if (sessionEl) {
    sessionEl.innerHTML = `
      <div class="session-${data.session.toLowerCase()}">
        ${data.description}
      </div>
      <div class="session-time">UTC: ${data.utcHour}:00</div>
    `;
  }
});

// Risk metrics updates
ioClient.on('risk-metrics', (data) => {
  const metricsEl = document.getElementById('risk-metrics');
  if (metricsEl) {
    metricsEl.innerHTML = `
      <div class="metric">VaR: ${(data.portfolio_var * 100).toFixed(2)}%</div>
      <div class="metric">Drawdown: ${(data.max_drawdown * 100).toFixed(2)}%</div>
      <div class="metric">Sharpe: ${data.sharpe_ratio}</div>
      <div class="metric">Positions: ${data.active_positions}/24</div>
      <div class="metric pnl-${data.daily_pnl > 0 ? 'positive' : 'negative'}">
        Daily P&L: $${data.daily_pnl.toFixed(0)}
      </div>
    `;
  }
});

// Trading signals
ioClient.on('trading-signal', (signal) => {
  const signalsEl = document.getElementById('trading-signals');
  if (signalsEl) {
    const signalDiv = document.createElement('div');
    signalDiv.className = `signal signal-${signal.action.toLowerCase()}`;
    signalDiv.innerHTML = `
      <span class="signal-symbol">${signal.symbol}</span>
      <span class="signal-action">${signal.action}</span>
      <span class="signal-confidence">${(signal.confidence * 100).toFixed(0)}%</span>
      <span class="signal-reason">${signal.reason}</span>
    `;
    
    signalsEl.insertBefore(signalDiv, signalsEl.firstChild);
    
    // Keep only last 5 signals
    while (signalsEl.children.length > 5) {
      signalsEl.removeChild(signalsEl.lastChild);
    }
  }
});

// Add CSS for live feed styling
const liveStyles = `
<style>
.price-up { color: #00ff00; animation: flash-green 0.5s; }
.price-down { color: #ff4444; animation: flash-red 0.5s; }
.change-positive { color: #00ff00; }
.change-negative { color: #ff4444; }

.session-weekend { color: #ffaa00; }
.session-asian { color: #66ccff; }
.session-london { color: #00ff00; }
.session-newyork { color: #ff6600; }

.metric { 
  display: inline-block; 
  margin: 0.2rem 0.5rem; 
  padding: 0.2rem 0.5rem; 
  background: rgba(0,255,0,0.1); 
  border-radius: 3px; 
}

.pnl-positive { background: rgba(0,255,0,0.2); }
.pnl-negative { background: rgba(255,68,68,0.2); }

.signal { 
  display: flex; 
  justify-content: space-between; 
  padding: 0.3rem; 
  margin: 0.1rem 0; 
  border-radius: 3px; 
  font-size: 0.8rem;
}

.signal-buy { background: rgba(0,255,0,0.1); border-left: 3px solid #00ff00; }
.signal-sell { background: rgba(255,68,68,0.1); border-left: 3px solid #ff4444; }
.signal-hold { background: rgba(255,255,0,0.1); border-left: 3px solid #ffff00; }

@keyframes flash-green { 0% { box-shadow: 0 0 10px #00ff00; } 100% { box-shadow: none; } }
@keyframes flash-red { 0% { box-shadow: 0 0 10px #ff4444; } 100% { box-shadow: none; } }

#connection-status {
  position: fixed;
  top: 10px;
  right: 10px;
  padding: 0.3rem 0.6rem;
  background: rgba(0,0,0,0.8);
  color: #00ff00;
  border-radius: 15px;
  font-size: 0.8rem;
  z-index: 1000;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', liveStyles);

console.log('✅ Socket.IO live feeds initialized');
</script>
EOF

  # Add the socket integration to the existing index.html
  awk '/<\/body>/ { system("cat /home/ing/RICK/R_H_UNI/mobile_console/socket_integration.html"); print; next } 1' "$MOBILE_DIR/index.html" > "$MOBILE_DIR/index_with_sockets.html"
  mv "$MOBILE_DIR/index_with_sockets.html" "$MOBILE_DIR/index.html"
  
  echo "✅ Socket.IO integration added to mobile console"
else
  echo "⚠️  Mobile console not found, creating minimal version..."
  
  # Create minimal mobile console with socket integration
  cat > "$MOBILE_DIR/index.html" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RBOTzilla UNI - Live Dashboard</title>
    <style>
        body { 
            font-family: 'Orbitron', monospace; 
            background: #0a0a0a; 
            color: #00ff00; 
            margin: 0; 
            padding: 1rem; 
        }
        .dashboard-grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 1rem; 
        }
        .widget { 
            background: rgba(0,255,0,0.1); 
            border: 1px solid #00ff00; 
            border-radius: 8px; 
            padding: 1rem; 
        }
        .widget h3 { margin-top: 0; color: #00ffaa; }
        #tmux-feed { 
            background: #000; 
            color: #00ff00; 
            padding: 1rem; 
            height: 200px; 
            overflow-y: auto; 
            font-family: monospace; 
            white-space: pre-wrap; 
        }
    </style>
</head>
<body>
    <div id="connection-status">🔴 CONNECTING...</div>
    
    <h1>🤖 RBOTzilla UNI - Live Dashboard</h1>
    
    <div class="dashboard-grid">
        <div class="widget">
            <h3>📊 Market Session</h3>
            <div id="session-status">Loading...</div>
        </div>
        
        <div class="widget">
            <h3>💹 Live TMUX Feed</h3>
            <div id="tmux-feed">Connecting to live stream...</div>
            <small>Last update: <span id="tmux-timestamp">--:--:--</span></small>
        </div>
        
        <div class="widget">
            <h3>⚡ Risk Metrics</h3>
            <div id="risk-metrics">Loading metrics...</div>
        </div>
        
        <div class="widget">
            <h3>🎯 Trading Signals</h3>
            <div id="trading-signals">Waiting for signals...</div>
        </div>
        
        <div class="widget">
            <h3>💱 FX Prices</h3>
            <div>EUR/USD: <span id="price-EUR-USD">--</span> <span id="change-EUR-USD">--%</span></div>
            <div>GBP/USD: <span id="price-GBP-USD">--</span> <span id="change-GBP-USD">--%</span></div>
        </div>
        
        <div class="widget">
            <h3>₿ Crypto Prices</h3>
            <div>BTC/USD: <span id="price-BTC-USD">--</span> <span id="change-BTC-USD">--%</span></div>
            <div>ETH/USD: <span id="price-ETH-USD">--</span> <span id="change-ETH-USD">--%</span></div>
        </div>
    </div>
    
    <!-- Socket.IO integration will be added here -->
</body>
</html>
EOF

  # Add socket integration to the new file
  cat "$MOBILE_DIR/socket_integration.html" >> "$MOBILE_DIR/index.html"
fi

# Create phase completion marker
echo "📝 Creating Phase 45 completion marker..."
cat > "$MOBILE_DIR/phase_45_complete.txt" << 'EOF'
✅ Phase 45 Complete: Socket + Live Widget Feeds

Components Added:
- Socket.IO real-time streaming server (port 5056)
- Live TMUX feed streaming
- Market data simulation feeds
- Session status real-time updates
- Risk metrics streaming
- Trading signals simulation
- WebSocket client integration in mobile console

Features:
🔌 Real-time TMUX terminal streaming
📊 Live market data updates (1-second intervals)
⏰ Session status monitoring (30-second intervals)
📈 Risk metrics updates (5-second intervals)
🎯 Trading signal simulation (10-second intervals)
📱 Mobile console integration
🎨 Live feed styling and animations

Access:
- Socket Server: http://localhost:5056
- Mobile Dashboard: /mobile_console/index.html
- Stream Script: npm run stream

PIN-locked checkpoint: Phase 45 immutable deployment complete
EOF

chmod 444 "$MOBILE_DIR/phase_45_complete.txt"

echo ""
echo "✅ Phase 45 Complete: Socket + Live Widget Feeds"
echo ""
echo "🔌 Components deployed:"
echo "  • Socket.IO streaming server (port 5056)"
echo "  • Real-time TMUX feed integration"
echo "  • Live market data simulation"
echo "  • Session-aware status updates"
echo "  • Risk metrics streaming"
echo "  • Trading signals feed"
echo ""
echo "🚀 To start live streaming:"
echo "  cd $SHELL_DIR"
echo "  npm run stream"
echo ""
echo "📱 Access dashboard:"
echo "  http://localhost:5056/mobile_console/"
echo ""
echo "🎯 Ready for Phase 46: GPT/Grok Browser Relay!"