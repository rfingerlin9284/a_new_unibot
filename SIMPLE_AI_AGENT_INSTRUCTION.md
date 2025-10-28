# 📋 AI AGENT HELPER - FILE ROOTS & COPY-PASTE COMMANDS

**Date:** October 20, 2025  
**Purpose:** Learn OANDA API connection pattern from reference files  
**PIN:** 841921 ✅

---

## 🤖 SIMPLE COPY-PASTE COMMAND FOR AI AGENT HELPER

**Copy everything below and give to your AI agent helper:**

```
Study these 9 files for reference ONLY to understand how the RBOTzilla system 
connects to OANDA API. Learn HOW the connection works, but do NOT modify any 
trading logic, strategy, Guardian gates, or Hedge decisions.

FILE 1 - MAIN ENGINE & OANDA CONNECTION HUB:
/home/ing/RICK/RICK_LIVE_PROTOTYPE/oanda_trading_engine.py
Purpose: Study lines 1-50 (imports), 90-230 (__init__), 280-330 (get prices), 1100-1150 (place orders)

FILE 2 - CORE OANDA API CONNECTION:
/home/ing/RICK/RICK_LIVE_PROTOTYPE/brokers/oanda_connector.py
Purpose: Study authentication (lines 60-100), API endpoint config, price fetching, order placement

FILE 3 - DISPLAY SYSTEM:
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/terminal_display.py
Purpose: Study how the display shows connection status and system information

FILE 4 - CHARTER VALIDATION (PIN 841921):
/home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/rick_charter.py
Purpose: Study constant definitions and PIN validation - NO changes allowed

FILE 5 - EVENT LOGGING:
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/narration_logger.py
Purpose: Study how events are logged to JSON files

FILE 6 - NARRATION SYSTEM:
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/rick_narrator.py
Purpose: Study how Rick narrates events

FILE 7 - HEDGE ENGINE (REFERENCE ONLY):
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/quant_hedge_engine.py
Purpose: Reference - do NOT modify

FILE 8 - STRATEGY AGGREGATOR (REFERENCE ONLY):
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/strategy_aggregator.py
Purpose: Reference - do NOT modify

FILE 9 - MOMENTUM SYSTEM (REFERENCE ONLY):
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/momentum_trailing.py
Purpose: Reference - do NOT modify

GOAL: Understand the OANDA API connection flow without changing any trading logic.

OUTPUT: Provide documentation on how the system connects to OANDA API.
```

---

## 📁 FILE ROOTS - COPY & PASTE LIST

```
/home/ing/RICK/RICK_LIVE_PROTOTYPE/oanda_trading_engine.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/brokers/oanda_connector.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/terminal_display.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/foundation/rick_charter.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/narration_logger.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/rick_narrator.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/quant_hedge_engine.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/strategy_aggregator.py
/home/ing/RICK/RICK_LIVE_PROTOTYPE/util/momentum_trailing.py
```

---

## 🔑 KEY LEARNING POINTS (For AI Agent)

### File 1: oanda_trading_engine.py
**LEARN:** How main engine initializes and connects to OANDA API
- Line 90-230: Full initialization sequence
- Line 280-330: How to fetch real-time prices from OANDA
- Line 1100-1150: How to send orders to OANDA
- **DO NOT CHANGE:** Trading logic, strategy voting, Guardian gates

### File 2: brokers/oanda_connector.py
**LEARN:** Core OANDA API authentication and endpoints
- How tokens are used for authentication
- How API base URL is configured (practice vs live)
- How HTTP requests are structured
- **DO NOT CHANGE:** Connection parameters or authentication

### File 3: util/terminal_display.py
**LEARN:** How to display system status and information
- Color formatting
- Section headers
- Connection status display
- **DO NOT CHANGE:** Display logic affecting status

### File 4: foundation/rick_charter.py
**LEARN:** How Charter constraints are defined and validated
- MIN_RR_RATIO = 3.2
- MIN_NOTIONAL_USD = 15000
- PIN validation (841921)
- **DO NOT CHANGE:** Any Charter values or validation logic

### File 5: util/narration_logger.py
**LEARN:** How events are logged to narration.jsonl
- JSON structure
- Timestamp capture
- Event documentation
- **DO NOT CHANGE:** Logging destination or format

### File 6: util/rick_narrator.py
**LEARN:** How narration system works
- Generates commentary
- Ollama integration (optional)
- **DO NOT CHANGE:** Narration generation logic

### File 7-9: Reference Files
**LEARN:** How these systems work but understand they are reference only
- **DO NOT CHANGE:** Any of these files' logic

---

## ✅ DO's FOR AI AGENT

- ✅ Read and understand all 9 files
- ✅ Create documentation on OANDA API connection
- ✅ Create flowcharts showing the connection flow
- ✅ Document authentication pattern
- ✅ Document request/response structure
- ✅ Create integration guides for reference
- ✅ Add comments to files (non-invasive)
- ✅ Create diagrams

---

## ❌ DON'Ts FOR AI AGENT

- ❌ Do NOT modify oanda_trading_engine.py logic
- ❌ Do NOT modify Guardian gate logic
- ❌ Do NOT modify Hedge decision logic
- ❌ Do NOT modify Strategy voting
- ❌ Do NOT modify risk parameters
- ❌ Do NOT modify Charter constraints
- ❌ Do NOT modify OANDA order placement code
- ❌ Do NOT alter any trading behavior

---

## 📊 WHAT AI AGENT SHOULD DELIVER

After analyzing these 9 files, the AI agent should provide:

1. **OANDA Connection Flow Documentation**
   - How authentication works
   - How prices are fetched
   - How orders are placed
   - How responses are handled

2. **System Architecture Diagram**
   - How oanda_trading_engine.py connects to oanda_connector.py
   - How subsystems integrate
   - Data flow through the system

3. **API Request Examples**
   - Show exact structure of API calls
   - Show headers and authentication
   - Show request/response cycle

4. **Integration Points Reference**
   - Where display connects
   - Where logging connects
   - Where Charter validation connects

5. **No Code Changes** - Just reference documentation and understanding

---

## 🎯 SUCCESS CRITERIA

✅ AI Agent understands OANDA API connection  
✅ AI Agent provides reference documentation  
✅ NO modifications to any trading logic  
✅ NO modifications to Guardian logic  
✅ NO modifications to Hedge logic  
✅ NO modifications to Charter enforcement  
✅ NO modifications to Strategy voting  
✅ ALL Charter constraints preserved (PIN 841921)  

---

## � PORT ALLOCATION (DO NOT CONFLICT)

**RICK System reserves these ports:**

```
Port 11434 (HTTP)  ← Ollama LLM (optional, localhost only)
Port 443 (HTTPS)   ← OANDA API (standard, shared across all systems)
PTY Terminals      ← Tmux Dashboard (no network port)
```

**Available ports for your other agents:**
```
✅ Port 8000-8999  (Web services)
✅ Port 3000-3999  (Web services)
✅ Port 5000-5999  (Web services)
✅ All other TCP/UDP ports
```

**Network Isolation:**
- RICK uses NO web dashboard ports
- Only Ollama (11434) and HTTPS (443) used
- Tmux dashboard is terminal-only (no network binding)
- File I/O only: narration.jsonl, connection_state.json

**Your agent can safely use:**
- Any port except 11434 (if you need Ollama)
- Standard HTTPS 443 is shared (no conflict)
- READ narration.jsonl and connection_state.json
- DO NOT WRITE to RICK's files

**Verification:**
```bash
# Check RICK's ports before starting your agent
lsof -i :11434  # Check Ollama
lsof -i :443    # Check HTTPS (many processes share this)
tmux list-sessions | grep rbotzilla  # Check dashboard
```

**See full port audit:** `PORT_AUDIT.md`

---

## �🚀 READY TO SHARE WITH AI AGENT

All file roots provided above with clear instructions:
- What to study
- What to learn
- What NOT to modify
- What output to deliver
- What ports to avoid

**Next Step:** Share the file roots and instructions with your AI agent helper.
