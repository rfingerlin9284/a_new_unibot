# 🤖 RICK + HIVE MIND ARCHITECTURE - ALWAYS-RUNNING SYSTEM

**Status:** ✅ COMPLETE  
**Date:** October 20, 2025  
**PIN:** 841921

---

## 🎯 YOUR REQUIREMENT

> "I want Rick and Hive Mind ALWAYS part of the system. I just don't want to use any VSCode agents to turn on/off or open tmux. I want all control through individually selecting task.json list."

---

## ✅ WHAT WAS DELIVERED

### **NEW ARCHITECTURE: Task.json-Based Complete Control**

All control now through **Ctrl+Shift+B** task selection - NO VSCode agents needed.

---

## 🚀 THE MAIN TASKS (You'll Use These Most)

### **1. 🟢 START EVERYTHING (ONE-CLICK)**
```
Ctrl+Shift+B → Select: "🟢 START EVERYTHING (Rick + Hive Mind + Dashboard)"
```
**What happens:**
- ✅ Ollama (Rick) starts in background
- ✅ Trading Engine (Hive Mind) starts in background  
- ✅ Dashboard opens (3-pane tmux layout)
- ✅ Everything running and monitoring

**This is your "turn on the system" button**

---

### **2. 🎮 OPEN DASHBOARD ONLY**
```
Ctrl+Shift+B → Select: "🎮 OPEN DASHBOARD ONLY (Rick + Hive already running)"
```
**What happens:**
- Opens 3-pane tmux dashboard
- Assumes Rick and Hive are already running
- Perfect when system already started, you just want to view

---

### **3. 🛑 STOP EVERYTHING**
```
Ctrl+Shift+B → Select: "🛑 STOP EVERYTHING (Rick + Hive + Dashboard)"
```
**What happens:**
- ✅ Kills Ollama (Rick)
- ✅ Kills Trading Engine (Hive)
- ✅ Kills all dashboard processes
- ✅ Kills tmux session

**This is your "turn off the system" button**

---

### **4. 🔄 RESTART EVERYTHING**
```
Ctrl+Shift+B → Select: "🔄 RESTART EVERYTHING (Clean kill + fresh start)"
```
**What happens:**
- Force kills EVERYTHING (clean slate)
- Waits 2 seconds
- Restarts everything fresh
- Opens dashboard

**Use if something gets stuck**

---

## 📊 MONITORING/VIEWING TASKS (Use While System Running)

### **5. 💬 VIEW RICK NARRATION**
```
Ctrl+Shift+B → Select: "💬 TALK TO RICK: View Narration Stream"
```
Shows real-time narration from Rick about market activity

### **6. 🐝 CHECK HIVE STATUS**
```
Ctrl+Shift+B → Select: "🐝 HIVE STATUS: Check Trading Engine Status"
```
Verify Rick (Ollama) and Hive Mind (Engine) are running

### **7. 📈 VIEW ACCOUNT BALANCE**
```
Ctrl+Shift+B → Select: "📈 VIEW: Account Balance & Stats"
```
Quick check of OANDA practice account

### **8. 🧪 TEST CONNECTION**
```
Ctrl+Shift+B → Select: "🧪 TEST: Verify OANDA Connection"
```
Test OANDA API connectivity

### **9. 📋 LIST RUNNING PROCESSES**
```
Ctrl+Shift+B → Select: "📋 LIST: Show All Running Processes"
```
See what's currently running

---

## 🎮 ADVANCED/INDIVIDUAL COMPONENT TASKS

### **Rick (Ollama) Only**
```
Ctrl+Shift+B → Select: "🤖 START Rick LLM (Ollama) - Always Running"
```
Start just Rick (narration engine) by itself

### **Hive Mind (Engine) Only**
```
Ctrl+Shift+B → Select: "🐝 START Hive Mind (Trading Engine) - Always Running"
```
Start just Hive Mind (trading logic) by itself

### **Dashboard Panes Individually**
```
Ctrl+Shift+B → Select: "📊 MONITOR: Live Narration + Positions (Left Pane)"
Ctrl+Shift+B → Select: "🧠 MONITOR: AI Decision Filtering (Top-Right Pane)"
Ctrl+Shift+B → Select: "🎮 CONTROL: Manual Command Terminal (Bottom-Right Pane)"
```

---

## 📌 TYPICAL WORKFLOW

### **Morning Startup:**
```bash
# Step 1: One-click start
Ctrl+Shift+B → Select "🟢 START EVERYTHING"

# Result: Rick + Hive Mind running, Dashboard opens
# You see real-time narration, positions, AI decisions
```

### **During Trading:**
```bash
# Check status anytime
Ctrl+Shift+B → Select "🐝 HIVE STATUS: Check Trading Engine Status"

# View Rick's thoughts
Ctrl+Shift+B → Select "💬 TALK TO RICK: View Narration Stream"

# Check positions
Ctrl+Shift+B → Select "📈 VIEW: Account Balance & Stats"
```

### **Control System (In Dashboard):**
```
Bottom-right terminal (interactive):
  > start              (if stopped)
  > stop               (if running)
  > status             (check status)
  > positions          (see open trades)
  > log I'm watching   (add custom note)
```

### **End of Day Shutdown:**
```bash
# Step 1: Stop everything
Ctrl+Shift+B → Select "🛑 STOP EVERYTHING"

# Result: Rick + Hive + Dashboard all stopped
```

---

## 🏗️ ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                    YOUR VS CODE                                │
│                  (Task Selection Only)                         │
└────────────────────┬────────────────────────────────────────────┘
                     │
         ┌───────────┴────────────┬──────────────────┬───────────┐
         │                        │                  │           │
    ┌────▼────┐          ┌───────▼──────┐    ┌─────▼────┐  ┌───▼──┐
    │  RICK   │          │  HIVE MIND   │    │ DASHBOARD│  │CONTROL│
    │ (Ollama)│          │   (Engine)   │    │  (Tmux)  │  │(Tasks)│
    └────┬────┘          └───────┬──────┘    └─────┬────┘  └───┬──┘
         │ Narration            │ Trading         │ Monitoring  │
         │ Commentary           │ Decisions       │ Display     │
         │ AI Voice             │ Guardian        │ 3-Panes     │
         │                      │ Hedge Logic     │ Real-time   │
         │                      │                 │             │
         └──────────────────────┼─────────────────┴─────────────┘
                                │
                         ┌──────▼───────┐
                         │  OANDA API   │
                         │  Practice    │
                         │  Account     │
                         └──────────────┘
```

**Key Point:** Rick and Hive ALWAYS run together. Dashboard just VIEWS their activity. All control via task.json.

---

## 🎯 CONTROL FLOW

```
YOUR ACTION                    TASK SELECTION              SYSTEM RESPONSE
─────────────────────────────────────────────────────────────────────────────
Want to start?        →    "🟢 START EVERYTHING"   →  Rick + Hive running
                                                      Dashboard opens

Already running,
want to see dashboard?  →   "🎮 OPEN DASHBOARD"    →  Dashboard opens

Want to stop?         →    "🛑 STOP EVERYTHING"    →  All stopped

Need to restart?      →    "🔄 RESTART"           →  Fresh start

Check Rick's thoughts? →    "💬 TALK TO RICK"      →  Narration stream shown

Verify everything OK? →    "🐝 HIVE STATUS"       →  Shows running processes

Need other task?      →    Ctrl+Shift+B            →  Full task list shown
```

---

## 📋 COMPLETE TASK LIST (Ctrl+Shift+B)

### **PRIMARY (Use Most Often):**
1. 🟢 START EVERYTHING (Rick + Hive Mind + Dashboard)
2. 🎮 OPEN DASHBOARD ONLY (Rick + Hive already running)
3. 🛑 STOP EVERYTHING (Rick + Hive + Dashboard)
4. 🔄 RESTART EVERYTHING (Clean kill + fresh start)

### **MONITORING:**
5. 💬 TALK TO RICK: View Narration Stream
6. 🐝 HIVE STATUS: Check Trading Engine Status
7. 📈 VIEW: Account Balance & Stats
8. 🧪 TEST: Verify OANDA Connection
9. 📋 LIST: Show All Running Processes

### **COMPONENTS:**
10. 🤖 START Rick LLM (Ollama) - Always Running
11. 🐝 START Hive Mind (Trading Engine) - Always Running
12. 📊 MONITOR: Live Narration + Positions (Left Pane)
13. 🧠 MONITOR: AI Decision Filtering (Top-Right Pane)
14. 🎮 CONTROL: Manual Command Terminal (Bottom-Right Pane)

### **UTILITIES:**
15. 🔧 SETUP: Make All Scripts Executable
16. 📚 GUIDE: Show Quick Start Reference

---

## ✅ NO VSCode AGENTS NEEDED

✅ Start system: **One task selection**  
✅ Stop system: **One task selection**  
✅ View dashboard: **One task selection**  
✅ Check status: **One task selection**  
✅ Restart: **One task selection**  

**All control through Ctrl+Shift+B task menu. No agents required.**

---

## 🔒 KEY PRINCIPLES

1. **Rick Always Runs** - Ollama stays in background
2. **Hive Always Runs** - Trading engine stays active
3. **Dashboard On Demand** - Open/close independently
4. **One Master Control** - Ctrl+Shift+B task selection
5. **Manual Override Available** - Command terminal in dashboard
6. **No External Agents** - Everything controlled via tasks

---

## 🎬 QUICK REFERENCE CARD

```
MORNING:        Ctrl+Shift+B → "🟢 START EVERYTHING"
TRADING:        (Watch dashboard, use bottom-right terminal)
EVENING:        Ctrl+Shift+B → "🛑 STOP EVERYTHING"

STUCK?          Ctrl+Shift+B → "🔄 RESTART EVERYTHING"
CHECK STATUS:   Ctrl+Shift+B → "🐝 HIVE STATUS"
VIEW RICK:      Ctrl+Shift+B → "💬 TALK TO RICK"
```

---

## 📊 DASHBOARD WHILE RUNNING

Once started, in the tmux dashboard:

**LEFT PANE (70%):**
- Rick's narration stream
- Active positions
- Charter parameters

**TOP-RIGHT PANE (30% x 50%):**
- AI decision filtering
- Momentum → Logic → Stop Loss → Guardian
- Green light messages

**BOTTOM-RIGHT PANE (30% x 50%):**
- Command terminal
- Type: `> start`, `> stop`, `> status`, `> positions`, `> log`

---

## 🚀 YOU ARE NOW READY

Everything is set up for:
- ✅ Full system control via task.json
- ✅ Rick + Hive always part of system
- ✅ No external agents needed
- ✅ One-button start/stop
- ✅ Real-time monitoring
- ✅ Manual control when needed

**System operational. Rick and Hive always running. All control through tasks.json.** 🎯

