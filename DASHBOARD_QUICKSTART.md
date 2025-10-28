# 🎮 QUICK START - TMUX DASHBOARD

## ⚡ START DASHBOARD IN 3 SECONDS

### Option 1: VS Code (Easiest)
```
Press: Ctrl+Shift+B (or Cmd+Shift+B)
Select: "🎮 START TMUX DASHBOARD (3-Pane Layout)"
Watch: Real-time trading monitor appears
```

### Option 2: Terminal
```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash start_dashboard.sh
```

---

## 📺 WHAT YOU'LL SEE

```
┌─ LEFT PANE ──────────────────────────┬─ TOP-RIGHT ──────┐
│ 🎙️ Live Narration                    │ 🧠 AI Decisions  │
│ • Trade events (colored icons)       │ • Momentum ✅    │
│ • Active positions with P&L          │ • Smart Logic ✅ │
│ • Charter parameters                 │ • Stop Loss ✅   │
│ • System status (🟢 OPERATIONAL)    │ • Guardian ✅    │
├──────────────────────────────────────┼──────────────────┤
│ [Narration continues]                │ 🎮 COMMANDS      │
│                                      │ > start/stop     │
│ 📊 Chart updates every 2 sec        │ > status         │
│                                      │ > log message    │
└──────────────────────────────────────┴──────────────────┘
```

---

## 🎮 BOTTOM-RIGHT: COMMAND TERMINAL

Type these commands to control the system manually:

| Command | What It Does |
|---------|--------------|
| `start` | 🤖 Start trading engine |
| `stop` | 🛑 Stop trading engine |
| `status` | 📊 Show if engine is running |
| `positions` | 📈 List open positions |
| `log I see momentum` | 📝 Log custom message |
| `help` | ❓ Show all commands |
| `clear` | 🧹 Clear terminal |
| `exit` | 🚪 Exit command terminal |

---

## 🧠 TOP-RIGHT: AI DECISION MONITOR

Watch real-time as the system analyzes trades:

```
📊 MOMENTUM_ANALYSIS      | ✅ PASS
     ML analyzing momentum...

🧠 SMART_LOGIC            | ✅ PASS
     Good setup for scalping

🛡️  STOP_LOSS_LOGIC       | ✅ PASS
     Smart trailing stop calculated

🐝 HIVE_MIND              | ✅ PASS
     4/5 strategies agree (80%)

👮 GUARDIAN_GATE          | ✅ PASS
     All compliance checks pass

🟢 EXECUTION_READY        | READY
     "Give me the green light and I'll summon swarm bot!"
```

**Refreshes every 1.5 seconds** as each component analyzes

---

## 📊 LEFT PANE: LIVE MONITORING

Shows everything happening in real-time:

### Narration Stream
```
🎙️ [2025-10-20 21:47:15] Just opened long EUR/USD
📈 [2025-10-20 21:47:20] Hedge check: No inverse pair found
ℹ️  [2025-10-20 21:47:25] Waiting 5 minutes before next trade
```

### Active Positions
```
📈 BUY EUR/USD | Units: 14000 | Entry: 1.0850
     P&L: +$180.50 | Notional: $15,190

📉 SELL GBP/USD | Units: 13500 | Entry: 1.2750
     P&L: -$95.25 | Notional: $17,213
```

### Charter Parameters
```
• Minimum Trade Interval: 5 minutes ✅
• Min Risk:Reward: 3.2:1 ✅
• Stop Loss: 20 pips ✅
• Max Concurrent: 3 positions ✅
• Micro Trading: ❌ DISABLED ✅
```

---

## 🚀 TYPICAL WORKFLOW

### 1. Start Dashboard
```bash
bash start_dashboard.sh
```
*Dashboard opens with 3 panes side-by-side*

### 2. Start Trading (in command terminal)
```
> start
✅ Trading engine started
```

### 3. Watch AI Analysis (top-right)
- Sees momentum progression
- Watches smart logic decisions
- Real-time filtering display
- "Give me the green light" message when ready

### 4. Monitor Live Trading (left)
- See narration of each event
- Watch positions open/close
- Track P&L in real-time
- See Chart compliance parameters

### 5. Control Manually (bottom-right)
- Start/stop any time
- Log notes about market conditions
- Check positions
- Type commands for system control

### 6. Stop Trading (when done)
```
> stop
✅ Trading engine stopped
```

---

## 🔧 TMUX KEYBOARD SHORTCUTS

Inside the dashboard:

| Shortcut | Action |
|----------|--------|
| `Alt+←` | Switch to left pane |
| `Alt+→` | Switch to top-right pane |
| `Alt+↓` | Switch to bottom-right pane |
| `Ctrl+D` | Exit current pane |
| `Ctrl+B, D` | Detach (leave session running) |
| `tmux attach` | Reattach to session |
| `Ctrl+C` | Stop current process in pane |

---

## 📌 IMPORTANT NOTES

✅ **No AI Agent Needed** - Manual/headless control fully functional  
✅ **Real-time Display** - AI decisions update every 1.5 seconds  
✅ **Charter Protected** - PIN 841921 validated, all rules enforced  
✅ **JPY Pairs Fixed** - Position sizing now correct for all pairs  
✅ **5-Min Minimum** - Micro trading disabled, 300-second intervals enforced  
✅ **Fully Logged** - All events in narration.jsonl  

---

## 🆘 QUICK TROUBLESHOOTING

**"tmux: command not found"**
```bash
sudo apt-get install tmux
```

**Dashboard won't start**
```bash
# Check if already running
tmux list-sessions

# Kill old session
tmux kill-session -t rbotzilla-dashboard

# Start fresh
bash start_dashboard.sh
```

**Commands not working in terminal pane**
```bash
# Make sure you're in bottom-right pane
# Press Alt+↓ to switch to it
# Then type commands
```

---

## 📞 SUPPORT

**Reference Files:**
- `TMUX_DASHBOARD_SETUP.md` - Full documentation
- `.vscode/tasks.json` - All available tasks
- `SIMPLE_AI_AGENT_INSTRUCTION.md` - AI reference (if needed)

**All systems operational. Dashboard ready for use!** 🎮✅
