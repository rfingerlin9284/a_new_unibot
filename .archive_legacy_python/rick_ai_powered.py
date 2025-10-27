#!/usr/bin/env python3
"""
rick_ai_powered.py - Real OpenAI GPT-Powered Rick Trading Assistant
PIN 841921 Approved | Charter Compliant | OpenAI API Integration

Connects to OpenAI GPT-4 for natural conversation while maintaining
access to real RICK trading system data (narration.jsonl, pnl.jsonl).

Requirements:
    pip install openai python-dotenv
    
Environment Variables (.env):
    OPENAI_API_KEY=sk-...
"""

import streamlit as st
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import OpenAI
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.warning("⚠️ OpenAI library not installed. Run: pip install openai python-dotenv")

# ============================================================================
# CONFIGURATION
# ============================================================================

CHARTER_PIN = "841921"
PROJECT_ROOT = Path("/home/ing/RICK/R_H_UNI")
LOGS_DIR = PROJECT_ROOT / "pre_upgrade" / "headless" / "logs"
TOGGLE_FILE = PROJECT_ROOT / ".upgrade_toggle"

# OpenAI Configuration
OPENAI_MODEL = "gpt-4-turbo-preview"  # or "gpt-3.5-turbo" for faster/cheaper
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ============================================================================
# RICK AI INTERFACE
# ============================================================================

class RickAIPowered:
    """OpenAI-powered Rick with real backend data access."""
    
    def __init__(self):
        self.initialize_session_state()
        
        # Initialize OpenAI client
        if OPENAI_AVAILABLE and OPENAI_API_KEY:
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.ai_enabled = True
        else:
            self.client = None
            self.ai_enabled = False
    
    def initialize_session_state(self):
        """Initialize chat session state."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'input_key' not in st.session_state:
            st.session_state.input_key = 0
    
    # ========================================================================
    # BACKEND DATA READERS (REAL DATA)
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
    
    def get_latest_events(self, max_count: int = 10) -> List[Dict]:
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
    
    def get_latest_pnl(self, max_count: int = 5) -> List[Dict]:
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
    
    def get_system_context(self) -> str:
        """Build comprehensive system context for GPT."""
        mode = self.get_system_mode()
        events = self.get_latest_events(10)
        pnl = self.get_latest_pnl(3)
        engine_running = self.check_ghost_engine_running()
        
        # Format latest events
        events_text = "No recent activity"
        if events:
            events_text = "\n".join([
                f"- [{e.get('timestamp', 'N/A')[:19]}] {e.get('text', e.get('message', 'Activity'))}"
                for e in events[-5:]
            ])
        
        # Format P&L
        pnl_text = "No P&L data"
        if pnl:
            latest_pnl = pnl[-1]
            net = latest_pnl.get('net_pnl', 0)
            gross = latest_pnl.get('gross_pnl', 0)
            fees = latest_pnl.get('fees', 0)
            pnl_text = f"Net: ${net:.2f}, Gross: ${gross:.2f}, Fees: ${fees:.2f}"
        
        context = f"""
RICK TRADING SYSTEM - REAL-TIME STATUS

Trading Mode: {mode} {"(Paper Trading - No Real Money)" if mode == "GHOST" else "(LIVE TRADING - REAL MONEY)"}
Engine Status: {"Running" if engine_running else "Stopped"}

Recent Bot Activity:
{events_text}

Latest P&L:
{pnl_text}

CHARTER RULES (IMMUTABLE):
- Risk/Reward: ≥3.2:1 minimum (reject anything lower)
- Daily Breaker: -5% max loss (auto-halt system)
- Max Hold: 6 hours (forced exit after)
- Min Position: $15,000 notional
- Timeframes: M15, M30, H1 only (M1, M5 rejected)
- PIN Required: 841921 for all system changes

PLAIN ENGLISH ANALOGIES:
- FVG (Fair Value Gap) = "Empty parking spot on busy street"
- RR 3.2:1 = "Betting odds: risk $1 to make $3.20"
- Session Breaker = "Emergency brake for bad days"
- OCO Orders = "Safety net (parachute + ejection seat)"
- Hive Mind = "Bee colony voting system"
- Wolfpack = "Team strategy coordination"

SYSTEM COMMANDS (PIN-GATED):
- RICK> START GHOST - Launch trading engine
- RICK> TOGGLE MODE - Switch GHOST ↔ LIVE
- RICK> HALT - Emergency stop
- RICK> SET RISK 0.5 - Adjust risk percentage

You are Rick, an AI trading coach. Use this real system data to answer questions.
Be conversational, helpful, and explain concepts in plain English.
If user tries system commands, remind them PIN 841921 is required.
"""
        return context
    
    # ========================================================================
    # AI RESPONSE GENERATION
    # ========================================================================
    
    def generate_ai_response(self, prompt: str, conversation_history: List[Dict]) -> str:
        """Generate response using OpenAI GPT with real system context."""
        
        if not self.ai_enabled:
            return """❌ **OpenAI Not Available**

To enable AI-powered Rick:

1. Install dependencies:
```bash
pip install openai python-dotenv
```

2. Create `.env` file in project root:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

3. Get API key from: https://platform.openai.com/api-keys

4. Restart Rick

For now, I'm running in limited mode with pre-defined responses."""
        
        try:
            # Build system context with real data
            system_context = self.get_system_context()
            
            # Prepare messages for OpenAI
            messages = [
                {
                    "role": "system",
                    "content": system_context
                }
            ]
            
            # Add conversation history (last 10 messages to stay within token limits)
            for msg in conversation_history[-10:]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            # Add current user prompt
            messages.append({
                "role": "user",
                "content": prompt
            })
            
            # Call OpenAI API with streaming
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=800,
                stream=True
            )
            
            # Stream the response
            full_response = ""
            placeholder = st.empty()
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    placeholder.markdown(full_response + "▌")
            
            # Final response without cursor
            placeholder.markdown(full_response)
            
            return full_response
            
        except Exception as e:
            return f"""⚠️ **OpenAI API Error**

{str(e)}

**Possible Issues:**
- Invalid API key in `.env`
- Rate limit exceeded
- Network connectivity
- Insufficient API credits

**Check:**
```bash
cat .env | grep OPENAI_API_KEY
```

**Fallback:** I can still access system status from logs, but responses will be basic."""
    
    # ========================================================================
    # UI RENDERING
    # ========================================================================
    
    def render(self):
        """Render AI-powered chat interface."""
        
        # Show API status
        if not self.ai_enabled:
            st.warning("⚠️ OpenAI not configured. Install `openai` and set OPENAI_API_KEY in .env")
        else:
            st.success(f"✅ AI-Powered Rick (Model: {OPENAI_MODEL})")
        
        # Chat message history
        chat_container = st.container()
        
        with chat_container:
            # Show welcome message if first time
            if len(st.session_state.messages) == 0:
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown("""👋 Hey! I'm **Rick**, your AI-powered trading coach.

I'm connected to:
• **Your RICK trading system** (real-time data from logs)
• **OpenAI GPT-4** (natural language understanding)

I can discuss anything trading-related in natural conversation. Try:
- "What's the system doing right now?"
- "Explain how the hive mind makes decisions"
- "Should I be worried about current market conditions?"
- "What's your opinion on momentum strategies?"

Or just chat naturally - I'll understand! 💬""")
            
            # Display conversation history
            for message in st.session_state.messages:
                avatar = "🧑" if message["role"] == "user" else "🤖"
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Chat with Rick...", key=f"chat_input_{st.session_state.input_key}"):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message
            with st.chat_message("user", avatar="🧑"):
                st.markdown(prompt)
            
            # Generate AI response
            with st.chat_message("assistant", avatar="🤖"):
                if self.ai_enabled:
                    response = self.generate_ai_response(prompt, st.session_state.messages)
                else:
                    response = "⚠️ OpenAI not configured. Set OPENAI_API_KEY in .env to enable AI responses."
                    st.markdown(response)
            
            # Add to history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Increment input key
            st.session_state.input_key += 1
            st.rerun()

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    
    st.set_page_config(
        page_title="Rick AI Trading Assistant",
        page_icon="🤖",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # ChatGPT-style CSS
    st.markdown("""
    <style>
    .stApp {
        max-width: 900px;
        margin: 0 auto;
        background: #1a1f3a;
    }
    
    [data-testid="stChatMessage"] {
        padding: 1.5rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        background: rgba(17, 22, 42, 0.6);
    }
    
    [data-testid="stChatInput"] {
        border: 1px solid rgba(0, 255, 208, 0.3);
        border-radius: 12px;
        padding: 12px;
        background: rgba(11, 16, 32, 0.8);
    }
    
    code {
        background: rgba(0, 255, 208, 0.15);
        padding: 3px 8px;
        border-radius: 4px;
        color: #00ffd0;
    }
    
    pre {
        background: rgba(11, 16, 32, 0.8);
        border: 1px solid rgba(0, 255, 208, 0.3);
        border-radius: 8px;
        padding: 16px;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize and render Rick
    rick = RickAIPowered()
    rick.render()

if __name__ == "__main__":
    main()
