# 🟢 QUICK REFERENCE - STARTUP & VERIFICATION
**PIN:** 841921 ✅ | **Status:** PRODUCTION READY

---

## ⚡ 30-SECOND STARTUP

### Method 1: VS Code (EASIEST)
```
1. Press: Ctrl+Shift+B
2. Select: "🟢 START EVERYTHING (Rick + Hive Mind + Dashboard)"
3. Wait 10 seconds
4. Dashboard opens
5. ✅ Ready
```

### Method 2: Command Line
```bash
cd /home/ing/RICK/RICK_LIVE_PROTOTYPE
bash SMART_STARTUP.sh
```

---

## ✅ VERIFY SYSTEM READY (1 MINUTE)

```bash
python3 verify_complete_system.py
```

**Expected:** ✅ SYSTEM READY FOR AUTONOMOUS OPERATION

---

## 🎮 CONTROL COMMANDS (In Dashboard Terminal)

```
> start          Start autonomous trading
> stop           Stop gracefully
> status         Show current state
> positions      List open positions
> log            Show recent events
> help           Show all commands
> exit           Exit terminal
```

---

## 🛑 SHUTDOWN (GRACEFUL)

### Method 1: Dashboard Terminal
```
> stop
# Closes positions → Saves state → Exits
```

### Method 2: Command Line
```bash
pkill -f "oanda_trading_engine.py"
pkill -f "ollama serve"
pkill -f "streamlit"
```

---

## 🔄 RESTART (GUARANTEED SAFE)

```bash
# 1. Stop gracefully
> stop
sleep 5

# 2. Verify state saved
cat connection_state.json
tail -5 narration.jsonl

# 3. Start fresh
bash SMART_STARTUP.sh

# 4. Verify ready
python3 verify_complete_system.py
```

---

## 🔍 TROUBLESHOOTING

### "Ollama already running"
```bash
# Smart startup handles this automatically
bash SMART_STARTUP.sh
# Reuses existing Ollama instead of restart
```

### Unknown System State
```bash
python3 verify_complete_system.py
# Shows exactly what's working/broken
```

### Need Full Restart
```bash
bash SMART_STARTUP.sh --force-restart
# Kills everything and starts fresh
```

### Check Logs
```bash
tail -50 narration.jsonl          # Event history
tail -20 /tmp/engine.log          # Engine output
tail -20 /tmp/ollama.log          # Ollama output
```

---

## 📋 VERIFICATION CHECKLIST

Before pressing `> start`:

```
✅ Charter PIN: 841921
✅ Immutable constants loaded
✅ Guardian gates initialized
✅ OANDA API connected
✅ All subsystems ready
✅ Narration logging active
✅ Dashboard showing 3 panes
✅ Recent events in narration.jsonl
✅ No error messages
✅ Account balance visible
```

---

## 🛡️ WHAT'S PROTECTED

**Cannot Accidentally Break:**
- ✅ Charter constants (hardcoded)
- ✅ Guardian gates (always active)
- ✅ Event logging (append-only)
- ✅ PIN validation (enforced)
- ✅ Position sizing (Charter-compliant)

**Automatically Recovered After Restart:**
- ✅ Previous positions
- ✅ Event history
- ✅ System configuration
- ✅ All state

---

## 📚 DOCUMENTATION

| Document | Purpose |
|----------|---------|
| **STARTUP_VERIFICATION_GUIDE.md** | Complete turn-on/off/reboot guide |
| **FUNCTIONAL_STATE_MAINTENANCE.md** | Protection strategy & best practices |
| **COMPLETE_SOLUTION_SUMMARY.md** | Full solution overview |
| **verify_complete_system.py** | 9-section verification checklist |
| **SMART_STARTUP.sh** | Intelligent startup orchestrator |

---

## 🎯 DAILY WORKFLOW

**Morning:**
```bash
# Start system
bash SMART_STARTUP.sh

# Verify ready
python3 verify_complete_system.py

# In dashboard terminal:
> start   # Begin trading
```

**Throughout Day:**
```
Monitor dashboard:
• Left: Rick narration + positions
• Top-right: AI decisions (real-time)
• Bottom-right: Manual control
```

**Evening:**
```
In dashboard terminal:
> stop    # Graceful shutdown
```

**Next Day:**
```bash
# Automatic state recovery on restart
bash SMART_STARTUP.sh
# Previous positions & events loaded
```

---

## 🚀 YOU'RE READY TO GO

Everything is set up for:
- ✅ **Reliable startup** (3 methods available)
- ✅ **Graceful shutdown** (state saved)
- ✅ **Safe restart** (state recovered)
- ✅ **Full verification** (9-section checklist)
- ✅ **Complete protection** (3-layer system)
- ✅ **Autonomous trading** (ready to run 24/7)

**PIN: 841921 ✅ | Gates: ACTIVE ✅ | System: READY ✅**

Start now:
```bash
Ctrl+Shift+B → "🟢 START EVERYTHING"
```

Or:
```bash
bash SMART_STARTUP.sh
```

---

**Questions?** See full documentation files above.  
**Need details?** Read COMPLETE_SOLUTION_SUMMARY.md  
**Ready to trade?** Just run startup and press `> start`
