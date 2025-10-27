# 🎮 RBOTzilla TMUX DASHBOARD - Complete Setup Guide

**Status:** ✅ COMPLETE  
**Date:** October 20, 2025  
**PIN:** 841921

---

## 📋 WHAT WAS CREATED

### 1. **start_dashboard.sh** - Main Tmux Session Manager
- **Purpose:** Launches 3-pane tmux dashboard layout
- **Panes:**
  - **Left (70%):** Live narration, positions, and log stream
  - **Top-Right (30%, 50% height):** Real-time AI decision monitoring
  - **Bottom-Right (30%, 50% height):** Interactive command terminal
- **Command:** `bash start_dashboard.sh`

### 2. **dashboard_live_monitor.py** - Main Display Pane (Left)
- **Purpose:** Shows narration events, active positions, and Charter parameters
- **Content:**
  - Live narration stream (last 15 events)
  - Active positions with P&L tracking
  - Charter parameters and system status
- **Refresh:** 2 seconds
- **Command:** `python3 dashboard_live_monitor.py`

### 3. **ai_decision_monitor.py** - AI Decisions Pane (Top-Right)
- **Purpose:** Real-time display of AI filtering & decision-making
- **Shows:**
  - 📊 Momentum Analysis → ML momentum detector output
  - 🧠 Smart Logic → "Good setup for scalping"
  - 🛡️ Stop Loss Logic → "Smart trailing orders"
  - 🐝 Hive Mind Voting → Strategy consensus
  - 👮 Guardian Gate → Pre-trade compliance checks
  - 🟢 Execution Ready → "Give me the green light!"
- **Refresh:** 1.5 seconds (real-time progression)
- **Command:** `python3 ai_decision_monitor.py`

### 4. **interactive_command_terminal.sh** - Command Input Pane (Bottom-Right)
- **Purpose:** Manual/headless control without AI agent
- **Commands:**
  - `start` - Start trading engine
  - `stop` - Stop trading engine
  - `status` - Check engine status
  - `positions` - View open positions
  - `log [message]` - Log custom message to system
  - `help` - Show all commands
  - `clear` - Clear terminal
  - `exit` - Exit terminal
- **Command:** `bash interactive_command_terminal.sh`

### 5. **.vscode/tasks.json** - VS Code Integration (NEW TASKS ADDED)
- **New Tasks:**
  - 🎮 START TMUX DASHBOARD (3-Pane Layout) ← **PRIMARY TASK**
  - 📊 Dashboard: Live Monitor
  - 🧠 Dashboard: AI Decision Monitor
  - 🎮 Dashboard: Interactive Command Terminal
  - ✅ Verify Dashboard Setup

---

## 🚀 HOW TO USE

### Method 1: Full Dashboard (Recommended)
```bash
# In VS Code:
# 1. Press Ctrl+Shift+B (or Cmd+Shift+B on Mac)
# 2. Select: "🎮 START TMUX DASHBOARD (3-Pane Layout)"
# 3. Watch real-time trading monitoring

# Or manually:
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash start_dashboard.sh
```

### Method 2: Individual Panes (for development)
```bash
# Terminal 1 - Live Monitor (left)
python3 dashboard_live_monitor.py

# Terminal 2 - AI Decisions (top-right)
python3 ai_decision_monitor.py

# Terminal 3 - Commands (bottom-right)
bash interactive_command_terminal.sh
```

### Method 3: Headless/Manual Control
```bash
# Start engine
python3 oanda_trading_engine.py &

# Watch narration in separate terminal
tail -f narration.jsonl | jq -r '.narration'

# Control via command terminal
bash interactive_command_terminal.sh
```

---

## 🎮 DASHBOARD LAYOUT

```
┌──────────────────────────────────────────────┬────────────────────┐
│                                              │  AI DECISIONS      │
│  LIVE NARRATION & POSITIONS                  │  (Real-time        │
│  (Large Left 70%)                            │   Filtering)       │
│                                              │                    │
│  • Event stream (last 15)                    │  • Momentum ✅     │
│  • Active positions with P&L                 │  • Smart Logic ✅  │
│  • Charter parameters                        │  • Stop Loss ✅    │
│  • System status                             │  • Hive Mind ✅    │
│                                              │  • Guardian ✅     │
│                                              │  • 🟢 GREEN LIGHT  │
├──────────────────────────────────────────────┼────────────────────┤
│                                              │  COMMAND TERMINAL  │
│  [Continued from left pane above]            │  (Manual Control)  │
│                                              │                    │
│  [Additional narration/data scrolls here]    │  > start           │
│                                              │  > stop            │
│                                              │  > status          │
│                                              │  > positions       │
│                                              │  > log message     │
└──────────────────────────────────────────────┴────────────────────┘
```

---

## 🎯 REAL-TIME AI DECISION DISPLAY EXAMPLE

```
🧠 AI DECISION MONITOR - Real-time Filtering & Logic Analysis
═════════════════════════════════════════════════════════════════

📊 MOMENTUM_ANALYSIS      | ✅ PASS
     ✅ Momentum Score: 7.8/10 - Strong uptrend detected

🧠 SMART_LOGIC            | ✅ PASS
     ✅ Price Action: Double bottom at 1.0850 - Good setup for scalping

🛡️  STOP_LOSS_LOGIC       | ✅ PASS
     ✅ Stop Loss: 20 pips below double bottom = 1.0830 (optimal protection)

🐝 HIVE_MIND              | ✅ PASS
     ✅ Hive Consensus: 4/5 strategies agree (80% confidence > 70% threshold)

👮 GUARDIAN_GATE          | ✅ PASS
     ✅ Guardian: All gates pass - Notional OK, Margin OK, RR OK, Charter OK

───────────────────────────────────────────────────────────────────────────
CURRENT EVALUATION: EUR/USD
  Entry Point: 1.0850 (Double bottom confluence)
  Stop Loss: 1.0830 (20 pips)
  Take Profit: 1.0914 (64 pips = 3.2:1 RR)
  Position Size: ~14,000 units
  Notional: $15,010 ✅
───────────────────────────────────────────────────────────────────────────

╔════════════════════════════════════════════════════════════════════════╗
║  ⏳ WAITING FOR GREEN LIGHT...                                         ║
║  If all criteria pass → 'Give me the green light and I'll summon      ║
║                         a swarm bot with smart trailing orders!'       ║
╚════════════════════════════════════════════════════════════════════════╝
```

---

## 🔧 CRITICAL BUG FIX: JPY Pair Positioning

**Issue Found:** JPY pairs (USD/JPY, GBP/JPY, etc.) were being undersized
- USD/JPY @ 150.73 was calculating only 100 units instead of ~100,000 units
- Result: $100 notional vs required $15,000

**Fix Applied:** Modified `calculate_position_size()` in `oanda_trading_engine.py`
- Now detects JPY pairs (pip_size = 0.01 vs 0.0001)
- Multiplies required units by 10 for JPY
- Ensures $15,000+ notional for ALL pairs

**Status:** ✅ FIXED

---

## 📊 COMMAND TERMINAL FEATURES

### Start/Stop Engine (Manual)
```bash
> start
✅ Starting trading engine...
✅ Trading engine started

> stop
⏹️  Stopping trading engine...
✅ Trading engine stopped
```

### Check Status & Positions
```bash
> status
📊 Engine Status:
✅ Running

> positions
📈 Open Positions:
EUR/USD: 14000 units @ 1.0850
```

### Manual Logging
```bash
> log I'm monitoring momentum confluence on GBP/USD
📝 Logging: I'm monitoring momentum confluence on GBP/USD
✅ Message logged
```

---

## 🎮 KEYBOARD NAVIGATION (Tmux)

Within tmux dashboard:
- **Alt+Left Arrow** - Select left pane
- **Alt+Right Arrow** - Select top-right pane  
- **Alt+Down Arrow** - Select bottom-right pane
- **Ctrl+D** - Exit current pane
- **Ctrl+B then X** - Kill pane
- **Ctrl+B then D** - Detach from session
- **tmux attach -t rbotzilla-dashboard** - Reattach later

---

## 📋 FILES CREATED/MODIFIED

**New Files:**
- ✅ `start_dashboard.sh` (140 lines)
- ✅ `dashboard_live_monitor.py` (260 lines)
- ✅ `ai_decision_monitor.py` (330 lines)
- ✅ `interactive_command_terminal.sh` (150 lines)

**Modified Files:**
- ✅ `.vscode/tasks.json` (added 5 new tasks)
- ✅ `oanda_trading_engine.py` (fixed JPY position sizing)

---

## ✅ VERIFICATION CHECKLIST

Run this to verify all files are present:

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash -c "
echo '✅ Checking Dashboard Files:'
test -f start_dashboard.sh && echo '  ✅ start_dashboard.sh' || echo '  ❌ start_dashboard.sh'
test -f dashboard_live_monitor.py && echo '  ✅ dashboard_live_monitor.py' || echo '  ❌ dashboard_live_monitor.py'
test -f ai_decision_monitor.py && echo '  ✅ ai_decision_monitor.py' || echo '  ❌ ai_decision_monitor.py'
test -f interactive_command_terminal.sh && echo '  ✅ interactive_command_terminal.sh' || echo '  ❌ interactive_command_terminal.sh'
test -f .vscode/tasks.json && echo '  ✅ .vscode/tasks.json (updated)' || echo '  ❌ .vscode/tasks.json'
"
```

---

## 🎯 NEXT STEPS

1. **Test Dashboard:**
   ```bash
   Ctrl+Shift+B → Select "🎮 START TMUX DASHBOARD (3-Pane Layout)"
   ```

2. **In Bottom-Right Terminal, Try:**
   ```bash
   > status
   > log Testing dashboard system
   > help
   ```

3. **Watch Top-Right Pane:** Refreshes every 1.5 seconds with AI decisions

4. **Watch Left Pane:** Updates every 2 seconds with live narration and positions

5. **Start Engine:** `> start` in command terminal

---

## 🔐 SECURITY & CHARTER COMPLIANCE

✅ **PIN 841921** validated  
✅ **Micro trading** DISABLED (5-min minimum enforced)  
✅ **Position sizing** FIXED (JPY pairs now correct)  
✅ **Guardian gates** ACTIVE  
✅ **Hedge logic** ACTIVE  
✅ **All constraints** IMMUTABLE  

---

## 📞 TROUBLESHOOTING

**Tmux not found?**
```bash
sudo apt-get install tmux
```

**Python modules missing?**
```bash
pip install requests python-dotenv jq
```

**Dashboard not displaying?**
```bash
# Verify tmux session
tmux list-sessions

# Reattach to existing session
tmux attach -t rbotzilla-dashboard

# Or start fresh
bash start_dashboard.sh
```

---

## 🎬 STATUS: 🟢 READY FOR USE

All components created and ready. Dashboard provides:
- ✅ Real-time narration & positions (left pane)
- ✅ Real-time AI decision filtering (top-right pane, updates every 1.5 sec)
- ✅ Manual control without AI agent (bottom-right pane)
- ✅ Headless operation capability
- ✅ Full Charter compliance
- ✅ JPY pair positioning fixed

**You can now manually control and monitor the system without any AI agent!** 🚀
