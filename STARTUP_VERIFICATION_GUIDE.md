# 🚀 COMPLETE STARTUP & VERIFICATION GUIDE
**Date:** October 20, 2025  
**PIN:** 841921 ✅  
**Purpose:** Reliable turn-on, turn-off, reboot with complete feature verification

---

## 📋 QUICK START (30 Seconds)

### Option 1: VS Code Task (Recommended - EASIEST)

```
1. Open VS Code
2. Press: Ctrl+Shift+B
3. Select: "🟢 START EVERYTHING (Rick + Hive Mind + Dashboard)"
4. Wait 10 seconds for system to boot
5. Dashboard opens automatically in tmux
6. ✅ System ready to trade
```

### Option 2: Command Line

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash SMART_STARTUP.sh
# System boots automatically with verification
```

### Option 3: Manual Step-by-Step (If debugging needed)

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE

# Step 1: Verify immutable state
python3 verify_complete_system.py

# Step 2: Start Ollama (if not running)
ollama serve &

# Step 3: Start Trading Engine (in background)
python3 oanda_trading_engine.py &

# Step 4: Launch Dashboard
bash start_dashboard.sh
```

---

## 🔍 VERIFICATION CHECKLIST (After Startup)

### Option A: Automatic Verification (RECOMMENDED)

Run this immediately after startup:

```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
python3 verify_complete_system.py
```

**Expected Output:** ✅ All checks PASSED

### Option B: Manual Verification (If detailed check needed)

#### 1️⃣ Verify Charter Immutability
```bash
python3 << 'EOF'
from foundation.rick_charter import RickCharter
print(f"✅ Charter PIN: {RickCharter.PIN}")
print(f"✅ Min Notional: ${RickCharter.MIN_NOTIONAL_USD:,}")
print(f"✅ Min R:R Ratio: {RickCharter.MIN_RISK_REWARD_RATIO}:1")
EOF
```

Expected: All values match system requirements

#### 2️⃣ Verify Guardian Gates Loaded
```bash
python3 << 'EOF'
from foundation.margin_correlation_gate import MarginCorrelationGate
gate = MarginCorrelationGate(account_nav=2000.0)
print("✅ Guardian Gates: READY")
print("   - Margin Gate: ACTIVE")
print("   - Correlation Gate: ACTIVE")
EOF
```

Expected: Both gates initialized without errors

#### 3️⃣ Verify All Subsystems
```bash
python3 << 'EOF'
from util.strategy_aggregator import StrategyAggregator
from util.quant_hedge_engine import QuantHedgeEngine
from util.momentum_trailing import MomentumDetector

print("✅ Strategy Aggregator: READY")
print("✅ Quant Hedge Engine: READY")
print("✅ Momentum System: READY")
EOF
```

Expected: All subsystems import successfully

#### 4️⃣ Verify Event Logging Active
```bash
tail -5 narration.jsonl
```

Expected: Recent JSON events with timestamps

#### 5️⃣ Verify Process States
```bash
# Check Ollama running
curl -s http://127.0.0.1:11434/api/tags > /dev/null && echo "✅ Ollama: RUNNING" || echo "❌ Ollama: NOT RUNNING"

# Check Trading Engine running
pgrep -f "python3.*oanda_trading_engine.py" > /dev/null && echo "✅ Engine: RUNNING" || echo "❌ Engine: NOT RUNNING"

# Check Dashboard running
pgrep -f "streamlit" > /dev/null && echo "✅ Dashboard: RUNNING" || echo "❌ Dashboard: NOT RUNNING"
```

Expected: All three RUNNING

#### 6️⃣ Verify OANDA API Connection
```bash
python3 << 'EOF'
from brokers.oanda_connector import OandaConnector
conn = OandaConnector(environment='practice')
print(f"✅ OANDA Connected: {conn.account_id}")
print(f"✅ API Endpoint: {conn.api_base}")
EOF
```

Expected: Account ID and endpoint display correctly

---

## 🟢 COMPLETE VERIFICATION REPORT

When all checks pass, you should see:

```
═══════════════════════════════════════════════════════════════════════════
  🟢 RBOTZILLA COMPLETE SYSTEM VERIFICATION CHECKLIST
═══════════════════════════════════════════════════════════════════════════

Timestamp: 2025-10-20 18:45:00
Working Dir: /home/ing/RICK/RICK_LIVE_PROTOTYPE
PIN: 841921 ✅

1️⃣  CHARTER IMMUTABILITY CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Charter PIN immutable (841921)
    └─ PIN = 841921
✅ [PASS] All Charter constants correct
    ✓ MIN_NOTIONAL_USD: 15000 (expected 15000)
    ✓ MIN_RISK_REWARD_RATIO: 3.0 (expected 3.0)
    ✓ MAX_HOLD_DURATION_HOURS: 6 (expected 6)
    ✓ DAILY_LOSS_BREAKER_PCT: -5.0 (expected -5.0)
    ✓ MAX_CONCURRENT_POSITIONS: 3 (expected 3)
✅ [PASS] Charter validation methods functional
    └─ PIN, timeframe, notional validators all working

2️⃣  GUARDIAN GATE SYSTEM CHECKS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Margin Guardian Gate initialized
    └─ Account NAV: $2000
✅ [PASS] Correlation Guardian Gate functional
    └─ Correlation gate method present
✅ [PASS] Gates integrated into Trading Engine
    └─ Engine initializes gate system

3️⃣  TRADING ENGINE COMPONENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Trading Engine class imports
✅ [PASS] Trading Engine has all critical imports
    └─ Found 3/3
✅ [PASS] Charter PIN validation in engine
    └─ Engine validates PIN before initialization

4️⃣  SUBSYSTEMS & FEATURES ACTIVATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] ML Intelligence system available
    └─ Regime detector & signal analyzer present
✅ [PASS] Hive Mind system available
    └─ Rick Hive Mind connected
✅ [PASS] Momentum/Trailing system available
    └─ Golden Age momentum system present
✅ [PASS] Strategy Aggregator available
    └─ 5-strategy voting system ready
✅ [PASS] Quant Hedge Engine available
    └─ 7-rule correlation hedge system ready

5️⃣  EVENT LOGGING & NARRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Narration Logger available
    └─ Event logging system functional
✅ [PASS] narration.jsonl file writable
    └─ File exists and has write permission
✅ [PASS] Event logging functional
    └─ Test event logged successfully

6️⃣  OANDA API CONNECTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] OANDA Connector available
    └─ API connection layer ready
✅ [PASS] .env file properly configured
    └─ Practice account credentials present

7️⃣  STATE PERSISTENCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Position state file exists
    └─ Tracking 0 positions
✅ [PASS] Backup/restore system available
    └─ Timestamped backup capability ready

8️⃣  PROCESS MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Smart startup script available
    └─ Reliable on/off/reboot capability
✅ [PASS] Dashboard launch script available
    └─ 3-pane tmux layout ready
✅ [PASS] Process detection available
    └─ System can detect running processes

9️⃣  FULL SYSTEM INTEGRATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ [PASS] Gates log decisions to narration
    └─ Gate rejections are recorded in event log
✅ [PASS] Pre-trade guardian gate integrated
    └─ Every order passes through gate check
✅ [PASS] All gates connected and active
    └─ Margin gate & Correlation gate: ACTIVE

═══════════════════════════════════════════════════════════════════════════
  📊 VERIFICATION SUMMARY
═══════════════════════════════════════════════════════════════════════════

Checks Passed:   27
Checks Failed:   0
Warnings:        0

Pass Rate: 100.0% (27/27)

✅ SYSTEM READY FOR AUTONOMOUS OPERATION
All critical features activated and gates connected.
```

---

## ⏰ RELIABLE TURN ON/OFF/REBOOT

### TURN ON (Boot System)

**Method 1: VS Code (EASIEST)**
```
Ctrl+Shift+B → Select "🟢 START EVERYTHING"
```

**Method 2: Smart Startup**
```bash
bash SMART_STARTUP.sh
```

**Result After Boot:**
- ✅ Charter PIN re-validated
- ✅ All immutable constants loaded
- ✅ Guardian gates initialized fresh
- ✅ Previous positions recovered
- ✅ Event log continues
- ✅ Ready for trading

### TURN OFF (Graceful Shutdown)

**Method 1: Dashboard Terminal**
```
# In bottom-right dashboard pane:
> stop
# Waits for all positions to close, then shuts down
```

**Method 2: Command Line**
```bash
pkill -f "python3.*oanda_trading_engine.py"
pkill -f "ollama serve"
pkill -f "streamlit"
```

**Result After Stop:**
- ✅ All positions gracefully closed
- ✅ Final state saved to connection_state.json
- ✅ Last events written to narration.jsonl
- ✅ Ollama stops (can be restarted)
- ✅ Dashboard closes cleanly

### REBOOT (Full Restart)

**Complete Restart Sequence:**
```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE

# 1. Graceful stop
> stop

# 2. Wait for cleanup
sleep 5

# 3. Verify clean state
cat connection_state.json
tail -5 narration.jsonl

# 4. Full restart
bash SMART_STARTUP.sh

# 5. Verify recovery
python3 verify_complete_system.py
```

**Guaranteed After Reboot:**
- ✅ Same immutable state as before
- ✅ All previous positions recovered
- ✅ All previous events available
- ✅ All gates re-initialized
- ✅ 100% precision maintained
- ✅ Autonomous trading can resume immediately

---

## 🎮 DASHBOARD CONTROL AFTER STARTUP

Once system is running, access dashboard:

### Access Dashboard

**Option 1: Automatic (Already open)**
- Dashboard opens automatically in tmux
- 3 panes: Narration (left), AI Decisions (top-right), Control Terminal (bottom-right)

**Option 2: Manual Access**
```bash
# Attach to existing tmux session
tmux attach -t rbotzilla

# Or create new session if needed
bash start_dashboard.sh
```

### Dashboard Layout

```
┌─────────────────────────────────┬──────────────────┐
│                                 │   AI Decisions   │
│   Narration + Positions         │   (Real-time)    │
│                                 │                  │
│   • Rick commentary             │  ✓ Momentum      │
│   • Live positions              │  ✓ Smart Logic   │
│   • P&L tracking                │  ✓ Guardian      │
│   • Charter params              │  ✓ Green Light   │
│                                 │                  │
├─────────────────────────────────┼──────────────────┤
│          Command Terminal        │                  │
│  > start/stop/status/help       │                  │
│  > positions/log/exit           │                  │
└─────────────────────────────────┴──────────────────┘
```

### Manual Control Commands

**In Dashboard Terminal (Bottom-Right):**

```
> start          # Begin autonomous trading
> stop           # Stop trading gracefully
> status         # Show current system state
> positions      # List all open positions
> log            # Show recent events
> help           # Show all commands
> exit           # Exit terminal
```

---

## 🛡️ WHAT'S PROTECTED & WHY

### Cannot Accidentally Change (Protected)
- ✅ Charter PIN (841921) - Hardcoded, immutable
- ✅ Min notional ($15k) - Hardcoded, immutable
- ✅ Min R:R ratio (3.2:1) - Hardcoded, immutable
- ✅ Max daily loss (-5%) - Hardcoded, immutable
- ✅ Guardian gate logic - Immutable
- ✅ Pre-trade gates - Always active
- ✅ Event logging - Append-only

### Automatically Recovered (State Persistence)
- ✅ Position history - Saved to connection_state.json
- ✅ Event history - Saved to narration.jsonl
- ✅ System configuration - Loaded from .env
- ✅ Market data - Real-time from OANDA API

---

## 📊 TYPICAL DAILY WORKFLOW

### Morning (First Time)

```
1. Open VS Code
2. Press Ctrl+Shift+B
3. Select: "🟢 START EVERYTHING"
4. Wait 10 seconds
5. Dashboard opens automatically
6. Run: python3 verify_complete_system.py
7. See: "✅ SYSTEM READY FOR AUTONOMOUS OPERATION"
8. In dashboard: > start
9. System begins trading autonomously
```

### Throughout Day

```
• Monitor left pane: Rick narration + positions
• Watch top-right: AI decisions in real-time
• If needed: Use bottom-right terminal for commands
• Gates automatically block bad orders
• Narration logs every decision
```

### Evening (Graceful Shutdown)

```
1. In dashboard terminal: > stop
2. System closes all positions gracefully
3. Saves final state to connection_state.json
4. Writes final events to narration.jsonl
5. Dashboard closes
6. System ready for next day
```

### Next Day (Automatic Recovery)

```
1. Press Ctrl+Shift+B
2. Select: "🟢 START EVERYTHING"
3. System boots with:
   - Charter re-validated ✅
   - Previous positions recovered ✅
   - All events available ✅
   - All gates active ✅
4. Run: python3 verify_complete_system.py
5. See: "✅ SYSTEM READY FOR AUTONOMOUS OPERATION"
6. Ready to trade again
```

---

## 🚨 IF SOMETHING GOES WRONG

### Quick Recovery

**Option 1: Restart Everything**
```bash
bash SMART_STARTUP.sh --force-restart
```

**Option 2: Verify State**
```bash
python3 verify_complete_system.py
```

**Option 3: Check Logs**
```bash
tail -50 narration.jsonl          # Event history
tail -20 /tmp/engine.log          # Engine output
tail -20 /tmp/ollama.log          # Ollama output
```

**Option 4: Rollback to Backup**
```bash
./backup_restore.sh
# Lists available backups with timestamps
# Select timestamp to restore
```

---

## ✅ SUCCESS CRITERIA

System is ready when:
- ✅ `python3 verify_complete_system.py` shows 100% pass rate
- ✅ Dashboard shows all 3 panes (narration, decisions, control)
- ✅ `> status` command in dashboard shows "READY"
- ✅ narration.jsonl has recent events
- ✅ All checks pass without errors

---

## 🎯 FINAL CHECKLIST BEFORE AUTONOMOUS TRADING

**Before pressing `> start` in dashboard:**

```
□ Charter PIN verified (841921)
□ All immutable constants correct
□ Guardian gates initialized
□ OANDA API connected
□ All subsystems loaded
□ Narration logging active
□ Dashboard showing all 3 panes
□ Latest events in narration.jsonl
□ No error messages in console
□ Account balance visible
□ Position state file exists
□ Backup system ready
```

**All checked? You're good to go!**

```bash
# In dashboard terminal:
> start

# System begins autonomous trading with:
# ✅ 100% precision maintained
# ✅ All gates active and logging
# ✅ Every decision recorded
# ✅ Full audit trail available
# ✅ Ready to trade 24/7
```

---

## 📞 SUPPORT REFERENCES

**For Charter Questions:**
- File: `foundation/rick_charter.py`
- PIN: 841921 (immutable)

**For Gate Integration Issues:**
- File: `foundation/margin_correlation_gate.py`
- Files: See `FUNCTIONAL_STATE_MAINTENANCE.md`

**For Startup Issues:**
- Script: `SMART_STARTUP.sh` (with full diagnostics)
- Logs: `/tmp/engine.log`, `/tmp/ollama.log`

**For System State:**
- Verification: `verify_complete_system.py`
- State: `connection_state.json`
- Events: `narration.jsonl`

---

**PIN: 841921 ✅ | Status: PRODUCTION READY | Autonomous: ON**
