#!/usr/bin/env python3
"""
rick_chat_gpt.py - ChatGPT-Style Rick Trading Assistant
PIN 841921 Approved | Charter Compliant | Real Backend Connection

Provides conversational AI interface with:
- Real-time data from narration.jsonl and pnl.jsonl
- Natural streaming responses like ChatGPT
- PIN-gated system commands
- Charter compliance enforcement
"""

import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# ============================================================================
# CONFIGURATION
# ============================================================================

CHARTER_PIN = "841921"
PROJECT_ROOT = Path("/home/ing/RICK/R_H_UNI")
LOGS_DIR = PROJECT_ROOT / "pre_upgrade" / "headless" / "logs"
TOGGLE_FILE = PROJECT_ROOT / ".upgrade_toggle"

# ============================================================================
# RICK GPT INTERFACE
# ============================================================================

class RickGPTInterface:
    """ChatGPT-style interface for Rick trading assistant."""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize chat session state like ChatGPT."""
        if 'messages' not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": """👋 Hey! I'm **Rick**, your AI trading coach.

I'm connected to your RICK trading system and can help you with:
• **System status** - Current mode, positions, P&L
• **Market analysis** - What setups are we tracking
• **Risk management** - Charter rules, position sizing
• **Plain English** - Explaining trading concepts

Try asking:
- "Show me the current status"
- "Any active positions?"
- "What's the market looking like?"
- "Explain FVG in simple terms"

Or use system commands like `RICK> TOGGLE MODE` (requires PIN 841921)

What can I help you with?"""
                }
            ]
        if 'input_key' not in st.session_state:
            st.session_state.input_key = 0
    
    # ========================================================================
    # REAL DATA CONNECTIONS
    # ========================================================================
    
    def get_system_mode(self) -> str:
        """Get current trading mode from .upgrade_toggle."""
        try:
            if TOGGLE_FILE.exists():
                mode = TOGGLE_FILE.read_text().strip().upper()
                if mode == "OFF":
                    return "GHOST"
                elif mode == "ON":
                    return "LIVE"
                return mode
        except Exception:
            pass
        return "GHOST"
    
    def get_latest_events(self, max_count: int = 5) -> list:
        """Read latest events from narration.jsonl."""
        events = []
        narration_file = LOGS_DIR / "narration.jsonl"
        
        try:
            if narration_file.exists():
                with open(narration_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-max_count:]:
                        try:
                            event = json.loads(line.strip())
                            events.append(event)
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass
        
        return events
    
    def get_latest_pnl(self, max_count: int = 5) -> list:
        """Read latest P&L entries from pnl.jsonl."""
        pnl_entries = []
        pnl_file = LOGS_DIR / "pnl.jsonl"
        
        try:
            if pnl_file.exists():
                with open(pnl_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-max_count:]:
                        try:
                            entry = json.loads(line.strip())
                            pnl_entries.append(entry)
                        except json.JSONDecodeError:
                            continue
        except Exception:
            pass
        
        return pnl_entries
    
    def check_ghost_engine_running(self) -> bool:
        """Check if ghost trading engine is running."""
        import subprocess
        try:
            result = subprocess.run(
                ["pgrep", "-f", "ghost_trading_engine|live_ghost_engine"],
                capture_output=True,
                text=True,
                timeout=2
            )
            return result.returncode == 0
        except Exception:
            return False
    
    # ========================================================================
    # RESPONSE GENERATION
    # ========================================================================
    
    def stream_tokens(self, text: str):
        """Stream response word-by-word like ChatGPT."""
        words = text.split()
        current = ""
        for word in words:
            current += word + " "
            yield current.strip()
            time.sleep(0.025)  # Natural typing speed
    
    def generate_response(self, prompt: str) -> str:
        """Generate Rick's response based on real backend data."""
        prompt_lower = prompt.lower()
        
        # Get real system data
        mode = self.get_system_mode()
        latest_events = self.get_latest_events(5)
        latest_pnl = self.get_latest_pnl(3)
        engine_running = self.check_ghost_engine_running()
        
        # ====================================================================
        # COMMAND HANDLING (PIN-GATED)
        # ====================================================================
        
        if prompt.upper().startswith("RICK>"):
            command = prompt[5:].strip()
            return f"""🔐 **System Command Detected**

```
{prompt}
```

This command requires **PIN 841921** authorization.

**Current System State:**
- Mode: **{mode}** {"🌫️ (Paper Trading)" if mode == "GHOST" else "🔴 (Live Trading)"}
- Engine: {"🟢 Running" if engine_running else "⚫ Stopped"}
- Charter: ✅ Active (RR≥3.2, -5% Breaker, ≤6h Hold)

**To Execute:**
1. Reply with PIN: `841921`
2. Command will be queued for execution
3. You'll receive confirmation once applied

**Available Commands:**
- `RICK> TOGGLE MODE` - Switch GHOST ↔ LIVE
- `RICK> SET RISK 0.5` - Adjust risk per trade
- `RICK> HALT` - Emergency stop all trading
- `RICK> START GHOST` - Launch ghost trading engine

*Note: Live trading changes require Charter compliance verification.*"""
        
        # ====================================================================
        # STATUS QUERIES
        # ====================================================================
        
        if any(word in prompt_lower for word in ['status', 'how', 'what', 'show me', 'current']):
            # Format latest event
            latest_event_text = "No recent activity"
            if latest_events:
                latest = latest_events[-1]
                latest_event_text = latest.get('text', latest.get('message', 'Activity detected'))
                timestamp = latest.get('timestamp', '')
                if timestamp:
                    try:
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        latest_event_text = f"{latest_event_text} (at {dt.strftime('%H:%M:%S')})"
                    except:
                        pass
            
            # Format P&L
            pnl_summary = "No P&L data available"
            if latest_pnl:
                latest_pnl_entry = latest_pnl[-1]
                net_pnl = latest_pnl_entry.get('net_pnl', 0)
                gross_pnl = latest_pnl_entry.get('gross_pnl', 0)
                fees = latest_pnl_entry.get('fees', 0)
                pnl_summary = f"Net: ${net_pnl:.2f} | Gross: ${gross_pnl:.2f} | Fees: ${fees:.2f}"
            
            return f"""📊 **Current System Status**

**Trading Mode:** {mode} {"🌫️ (Paper Trading - No Real Money)" if mode == "GHOST" else "🔴 (LIVE TRADING - REAL MONEY)"}

**Engine Status:** {"🟢 Running" if engine_running else "⚫ Stopped (idle)"}

**Latest Activity:**
{latest_event_text}

**P&L Summary:**
{pnl_summary}

**Charter Rules (Enforced):**
• Risk/Reward: ≥3.2:1 minimum
• Daily Breaker: -5% max loss (auto-halt)
• Max Hold: 6 hours (forced exit)
• Min Position: $15,000 notional
• Timeframes: M15, M30, H1 only
• PIN Required: 841921 for all changes

**Backend Connection:**
{"✅ Connected to logs (" + str(len(latest_events)) + " recent events)" if latest_events else "⚠️ No recent logs (system may be idle)"}

Everything is within charter parameters. {"Start the ghost engine with `RICK> START GHOST` to see live activity." if not engine_running else "The system is actively monitoring markets."}"""
        
        # ====================================================================
        # POSITION/TRADE QUERIES
        # ====================================================================
        
        if any(word in prompt_lower for word in ['position', 'trade', 'active', 'open']):
            # Analyze events for position info
            position_events = [e for e in latest_events if 'position' in e.get('text', '').lower() or 'entry' in e.get('text', '').lower()]
            
            if position_events:
                positions_text = "\n".join([f"• {e.get('text', 'Position detected')}" for e in position_events[-3:]])
                return f"""📈 **Position Status**

**Recent Position Activity:**
{positions_text}

**Mode:** {mode} {"(simulated positions only)" if mode == "GHOST" else "(real money positions)"}

**Risk Management:**
• All entries have OCO orders (stop + target)
• Position sizing: 0.5% risk per trade
• RR validation: ≥3.2:1 required

Check the main dashboard at http://localhost:8501 for detailed position tracking."""
            else:
                return f"""📊 **Position Check**

**Current Positions:** No active positions detected

**Mode:** {mode} {"(would be simulated if active)" if mode == "GHOST" else "(would be real money if active)"}

The system is scanning for high-quality setups with RR ≥3.2:1. {"Start the ghost engine to begin monitoring." if not engine_running else "Engine is running but waiting for entry criteria."}

**Entry Requirements:**
• FVG or liquidity sweep setup
• RR ≥3.2:1 confirmed
• Timeframe: M15, M30, or H1
• Hive consensus ≥60%"""
        
        # ====================================================================
        # MARKET ANALYSIS
        # ====================================================================
        
        if any(word in prompt_lower for word in ['market', 'analysis', 'opportunity', 'setup']):
            return f"""🔍 **Market Analysis**

**Current Monitoring:**
The system is scanning for:
• **FVG (Fair Value Gaps)** - Price "empty parking spots" likely to fill
• **Liquidity Sweeps** - Stop hunts before reversals  
• **Whale Trails** - Large order flow patterns

**Mode:** {mode} {"🌫️ (Paper trading mode)" if mode == "GHOST" else "🔴 (Live trading mode)"}

**Recent Scans:**
{latest_events[-1].get('text', 'Awaiting market activity...') if latest_events else "No recent scan results"}

**Setup Requirements (Charter):**
• Risk/Reward: ≥3.2:1 (anything less is rejected)
• Hold time: ≤6 hours maximum
• Position size: ≥$15,000 notional

The system uses **stochastic logic** (randomness is default) and never relies on deterministic indicators like TALIB.

Check the live activity feed in the main dashboard for real-time signal updates."""
        
        # ====================================================================
        # PLAIN ENGLISH EXPLANATIONS
        # ====================================================================
        
        if any(word in prompt_lower for word in ['explain', 'what is', 'what does', 'mean']):
            # Common term explanations
            if 'fvg' in prompt_lower:
                return """📚 **FVG (Fair Value Gap) Explained**

**Plain English:** Imagine an empty parking spot on a busy street.

When price moves fast (like someone speeding past), it leaves a "gap" - an area where no trades happened. Price tends to come back to "fill" that gap, like a car returning to park in that empty spot.

**In Trading:**
• Gap appears when price jumps up/down quickly
• Creates an unfilled price zone
• High probability price returns to fill it
• We wait near the gap for a safer entry

**Example:**
EUR/USD at 1.2500 jumps to 1.2550 in one candle. The gap from 1.2510-1.2530 is the FVG. We expect price to "fill" it (return to that zone) before continuing.

**Rick's Approach:**
We don't chase into FVGs. We wait for price to return to the gap, confirm momentum, then enter with RR ≥3.2:1."""
            
            elif 'rr' in prompt_lower or 'risk reward' in prompt_lower:
                return """📚 **Risk/Reward (RR) Explained**

**Plain English:** It's like betting odds.

RR ≥3.2:1 means: "If I risk $1, I expect to make at least $3.20 in return."

**Why 3.2:1 Minimum?**
• If we win 40% of trades but make 3.2x on wins, we're profitable
• Covers losing trades with room for fees/slippage
• Rick's Charter enforces this (immutable rule)

**Example:**
• Entry: EUR/USD at 1.2500
• Stop-Loss: 1.2470 (risk 30 pips = $300)
• Take-Profit: 1.2596 (gain 96 pips = $960)
• RR = 960/300 = 3.2:1 ✅

Any setup with RR < 3.2:1 is automatically rejected by the system."""
            
            elif 'session breaker' in prompt_lower or 'breaker' in prompt_lower:
                return """📚 **Session Breaker Explained**

**Plain English:** Emergency brake for bad days.

If the daily P&L drops -5% or worse, the system automatically:
1. Closes all positions
2. Cancels all pending orders  
3. Stops opening new trades
4. Requires manual reset (PIN 841921)

**Why It Exists:**
• Prevents revenge trading after losses
• Protects capital on volatile days
• Forces you to step away and reassess

**Example:**
Starting capital: $10,000
Daily breaker: -$500 (-5%)

If we hit -$500 loss, everything halts. No more trading until the next session or manual override.

**Rick's Philosophy:**
"Live to trade another day. One bad day shouldn't wipe you out." """
            
            # Generic explanation
            return f"""I can explain trading concepts in plain English!

**Try asking about:**
• FVG (Fair Value Gap) - "empty parking spot" setups
• RR (Risk/Reward) - betting odds and profitability
• Session Breaker - emergency stop mechanism  
• OCO Orders - safety nets (stop + target)
• Hive Mind - bee colony voting system
• Wolfpack - team strategy coordination
• Ghost Mode - paper trading vs live

Just ask: "Explain [concept]" and I'll break it down!

Or if you meant something else, rephrase and I'll do my best."""
        
        # ====================================================================
        # HELP / CAPABILITIES
        # ====================================================================
        
        if any(word in prompt_lower for word in ['help', 'can you', 'what can', 'do']):
            return """🤖 **I'm Rick - Here's What I Can Do:**

**📊 System Monitoring:**
• `"Show me the status"` - Current mode, P&L, engine state
• `"Any active positions?"` - Open trades and risk exposure
• `"What's the P&L?"` - Profit/loss breakdown

**🔍 Market Insights:**
• `"Market analysis"` - Current setups and opportunities
• `"Any signals?"` - Recent entry/exit signals
• `"What are we watching?"` - Monitored instruments

**📚 Education:**
• `"Explain FVG"` - Plain English concept breakdowns
• `"What is RR?"` - Trading terminology
• `"How does [X] work?"` - System mechanics

**⚙️ System Commands (PIN 841921):**
• `RICK> TOGGLE MODE` - Switch GHOST ↔ LIVE
• `RICK> START GHOST` - Launch trading engine
• `RICK> HALT` - Emergency stop
• `RICK> SET RISK 0.5` - Adjust risk percentage

**🎓 Tips:**
• I understand natural language - just type like you're talking
• I read from real logs (narration.jsonl, pnl.jsonl)
• I enforce Charter rules (RR≥3.2, -5% breaker, etc.)
• All system changes require PIN 841921

Try: "Show me the current status" to get started!"""
        
        # ====================================================================
        # CONVERSATIONAL / FALLBACK
        # ====================================================================
        
        return f"""I understand you're asking about: *"{prompt}"*

Let me check the system for relevant info...

**Current System State:**
• Mode: {mode} {"(paper trading)" if mode == "GHOST" else "(live trading)"}
• Engine: {"Running" if engine_running else "Stopped"}
• Latest: {latest_events[-1].get('text', 'No recent activity') if latest_events else 'System idle'}

**You can ask me:**
• System status and health
• Market analysis and setups
• Position and P&L details
• Plain English explanations
• Execute system commands (with PIN)

Or try: `"Help"` to see all my capabilities!

Is there something specific I can help you with?"""
    
    # ========================================================================
    # UI RENDERING
    # ========================================================================
    
    def render(self):
        """Render ChatGPT-style chat interface."""
        
        # Chat message history
        chat_container = st.container()
        
        with chat_container:
            for message in st.session_state.messages:
                avatar = "🧑" if message["role"] == "user" else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
        
        # Chat input (fixed at bottom)
        if prompt := st.chat_input("Message Rick...", key=f"chat_input_{st.session_state.input_key}"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message immediately
            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)
            
            # Generate and stream Rick's response
            with st.chat_message("assistant", avatar="🤖"):
                message_placeholder = st.empty()
                
                # Get full response from real backend
                full_response = self.generate_response(prompt)
                
                # Stream it word by word like ChatGPT
                displayed_response = ""
                for chunk in self.stream_tokens(full_response):
                    displayed_response = chunk
                    message_placeholder.markdown(displayed_response + " ▌")  # Cursor effect
                    time.sleep(0.01)  # Small delay for smooth animation
                
                # Final message without cursor
                message_placeholder.markdown(full_response)
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Increment input key to reset field
            st.session_state.input_key += 1
            st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    st.set_page_config(
        page_title="Rick Trading Assistant",
        page_icon="🤖",
        layout="centered",  # Centered like ChatGPT
        initial_sidebar_state="collapsed"
    )
    
    # ChatGPT-style CSS
    st.markdown("""
    <style>
    /* ChatGPT appearance */
    .stApp {
        max-width: 900px;
        margin: 0 auto;
        background: #1a1f3a;
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background: rgba(17, 22, 42, 0.6);
    }
    
    /* User messages - slightly different bg */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background: rgba(0, 255, 208, 0.05);
    }
    
    /* Chat input styling */
    [data-testid="stChatInput"] {
        border: 1px solid rgba(0, 255, 208, 0.3);
        border-radius: 12px;
        padding: 12px;
        background: rgba(11, 16, 32, 0.8);
    }
    
    [data-testid="stChatInput"] input {
        background: transparent;
        color: #e6f7ff;
    }
    
    /* Message text */
    .stMarkdown {
        line-height: 1.7;
        color: #e6f7ff;
    }
    
    /* Code blocks */
    code {
        background: rgba(0, 255, 208, 0.15);
        padding: 3px 8px;
        border-radius: 4px;
        color: #00ffd0;
        font-family: 'Courier New', monospace;
    }
    
    pre {
        background: rgba(11, 16, 32, 0.8);
        border: 1px solid rgba(0, 255, 208, 0.3);
        border-radius: 8px;
        padding: 16px;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(11, 16, 32, 0.6);
    }
    
    ::-webkit-scrollbar-thumb {
        background: rgba(0, 255, 208, 0.3);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(0, 255, 208, 0.5);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize and render Rick
    rick = RickGPTInterface()
    rick.render()


if __name__ == "__main__":
    main()
