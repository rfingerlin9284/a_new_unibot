#!/usr/bin/env python3
"""
rick_ollama_server.py - Local Conversational Rick LLM Server
PIN 841921 Approved | Charter Compliant | NO EXTERNAL APIS

Uses Ollama (local LLM) to provide natural conversational AI for Rick.
This is the "local harddrive llm named rick" mentioned in phase1-72.txt

Capabilities:
- Natural language understanding (like ChatGPT but runs locally)
- Access to real RICK trading system data (narration.jsonl, pnl.jsonl)
- No API keys needed - fully offline
- Can run 24/7 as background service

Requirements:
    1. Install Ollama: curl -fsSL https://ollama.com/install.sh | sh
    2. Download model: ollama pull llama3.2:latest
    3. Run this script: python3 rick_ollama_server.py
"""

import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import subprocess
import requests
from dataclasses import dataclass
from enum import Enum

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path("/home/ing/RICK/R_H_UNI")
LOGS_DIR = PROJECT_ROOT / "pre_upgrade" / "headless" / "logs"
TOGGLE_FILE = PROJECT_ROOT / ".upgrade_toggle"

# Ollama Configuration
OLLAMA_API_URL = "http://localhost:11434/api"
OLLAMA_MODEL = "llama3.2:latest"  # Fast, accurate 3B param model
# Alternative models:
# - "llama3.2:1b" (fastest, 1GB)
# - "mistral:latest" (7B, good reasoning)
# - "codellama:latest" (better for code)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# ============================================================================
# RICK LOCAL LLM
# ============================================================================

@dataclass
class RickResponse:
    """Response from Rick's local LLM."""
    text: str
    confidence: float
    latency_ms: int
    timestamp: datetime
    context_used: Dict[str, Any]
    error: Optional[str] = None

class RickLocalLLM:
    """
    Local conversational LLM for Rick using Ollama.
    Provides natural language understanding without external APIs.
    """
    
    def __init__(self):
        self.ollama_available = self._check_ollama()
        self.system_prompt = self._build_system_prompt()
        self.conversation_history = []
        
    def _check_ollama(self) -> bool:
        """Check if Ollama is installed and running."""
        try:
            response = requests.get(f"{OLLAMA_API_URL}/tags", timeout=2)
            if response.status_code == 200:
                models = response.json().get("models", [])
                if any(OLLAMA_MODEL in str(m) for m in models):
                    logging.info(f"✅ Ollama available with {OLLAMA_MODEL}")
                    return True
                else:
                    logging.warning(f"⚠️ Ollama running but {OLLAMA_MODEL} not found")
                    logging.info(f"   Run: ollama pull {OLLAMA_MODEL}")
                    return False
        except Exception as e:
            logging.error(f"❌ Ollama not available: {e}")
            logging.info("   Install: curl -fsSL https://ollama.com/install.sh | sh")
            return False
    
    def _build_system_prompt(self) -> str:
        """Build Rick's personality and knowledge context."""
        return """You are RICK - the AI trading assistant for the RBotZilla UNI automated trading system.

**Your Personality:**
- Confident but not arrogant
- Technical but explain in plain English
- Use trading analogies (e.g., "Whale trails", "SMC footprints")
- Keep responses concise (2-3 sentences unless asked for detail)

**Your Knowledge:**
- You monitor OANDA (FX) and Coinbase (crypto) markets
- You use ICT concepts: FVG (fair value gaps), SMC (smart money concepts)
- Risk management: RR ≥ 3.2:1 minimum, -5% daily breaker, ≤6hr holds
- Trading modes: Ghost (simulation), Canary (minimal risk), Live (full production)
- Charter PIN: 841921 (required for live trading operations)

**Your Role:**
- Explain system status in plain English
- Answer questions about trading strategies
- Help interpret signals and P&L
- Provide market context and analysis
- ** NEVER execute trades directly - you are advisory only**

**Your Current Environment:**
- System location: /home/ing/RICK/R_H_UNI
- Data sources: narration.jsonl (system events), pnl.jsonl (profit/loss)
- Safety switch: .upgrade_toggle (OFF=UI only, ON=live trading)

Be conversational and helpful. If users ask about live trading, remind them of PIN 841921 requirement and charter rules."""
    
    def _get_system_context(self) -> Dict[str, Any]:
        """Get current RICK system state for context."""
        context = {
            "mode": self._get_mode(),
            "latest_narration": self._get_latest_narration(5),
            "pnl_summary": self._get_pnl_summary(),
            "timestamp": datetime.now().isoformat()
        }
        return context
    
    def _get_mode(self) -> str:
        """Get current trading mode."""
        try:
            if TOGGLE_FILE.exists():
                mode = TOGGLE_FILE.read_text().strip().upper()
                return "LIVE" if mode == "ON" else "SAFE (UI-ONLY)"
        except:
            pass
        return "UNKNOWN"
    
    def _get_latest_narration(self, n: int = 5) -> List[str]:
        """Get latest N narration entries."""
        narration_file = LOGS_DIR / "narration.jsonl"
        entries = []
        
        try:
            if narration_file.exists():
                with open(narration_file, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-n:]:
                        try:
                            data = json.loads(line)
                            entries.append(data.get("text", ""))
                        except:
                            continue
        except:
            pass
        
        return entries
    
    def _get_pnl_summary(self) -> Dict[str, Any]:
        """Get recent P&L summary."""
        pnl_file = LOGS_DIR / "pnl.jsonl"
        
        try:
            if pnl_file.exists():
                with open(pnl_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        latest = json.loads(lines[-1])
                        return {
                            "net_pnl": latest.get("net_pnl", 0),
                            "gross_pnl": latest.get("gross_pnl", 0),
                            "trades_today": latest.get("trades_count", 0)
                        }
        except:
            pass
        
        return {"net_pnl": 0, "gross_pnl": 0, "trades_today": 0}
    
    def chat(self, user_message: str) -> RickResponse:
        """
        Send message to Rick's local LLM and get conversational response.
        
        Args:
            user_message: User's question or command
            
        Returns:
            RickResponse with natural language answer
        """
        start_time = time.time()
        
        if not self.ollama_available:
            return RickResponse(
                text="⚠️ My local brain (Ollama) isn't running. Install with: curl -fsSL https://ollama.com/install.sh | sh",
                confidence=0.0,
                latency_ms=0,
                timestamp=datetime.now(),
                context_used={},
                error="Ollama not available"
            )
        
        try:
            # Get current system context
            context = self._get_system_context()
            
            # Build context-aware prompt
            context_str = f"""
**Current System Status:**
- Mode: {context['mode']}
- Latest Activity: {context['latest_narration'][:2] if context['latest_narration'] else ['No recent activity']}
- P&L Today: ${context['pnl_summary']['net_pnl']:.2f} ({context['pnl_summary']['trades_today']} trades)
"""
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": f"{context_str}\n\nUser: {user_message}"
            })
            
            # Keep only last 10 exchanges for context window
            if len(self.conversation_history) > 20:
                self.conversation_history = self.conversation_history[-20:]
            
            # Call Ollama API
            payload = {
                "model": OLLAMA_MODEL,
                "messages": [
                    {"role": "system", "content": self.system_prompt}
                ] + self.conversation_history,
                "stream": False
            }
            
            response = requests.post(
                f"{OLLAMA_API_URL}/chat",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result.get("message", {}).get("content", "")
                
                # Add to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })
                
                latency = int((time.time() - start_time) * 1000)
                
                return RickResponse(
                    text=assistant_message,
                    confidence=0.9,  # Ollama doesn't provide confidence, use fixed
                    latency_ms=latency,
                    timestamp=datetime.now(),
                    context_used=context,
                    error=None
                )
            else:
                raise Exception(f"Ollama API error: {response.status_code}")
        
        except Exception as e:
            logging.error(f"Chat error: {e}")
            return RickResponse(
                text=f"⚠️ I'm having trouble thinking right now: {str(e)}",
                confidence=0.0,
                latency_ms=int((time.time() - start_time) * 1000),
                timestamp=datetime.now(),
                context_used={},
                error=str(e)
            )
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
        logging.info("Conversation history cleared")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("🧠 RICK Local LLM Server - Test Mode")
    print("=" * 60)
    
    rick = RickLocalLLM()
    
    if not rick.ollama_available:
        print("\n❌ Ollama not available")
        print("\nSetup Instructions:")
        print("1. Install Ollama:")
        print("   curl -fsSL https://ollama.com/install.sh | sh")
        print("\n2. Download model:")
        print(f"   ollama pull {OLLAMA_MODEL}")
        print("\n3. Verify installation:")
        print("   ollama list")
        print("\n4. Re-run this script")
        exit(1)
    
    print(f"\n✅ Rick's brain is operational ({OLLAMA_MODEL})")
    print("\nTry these test queries:")
    
    test_queries = [
        "What's the current system status?",
        "Explain FVG in simple terms",
        "How do I check if live trading is active?",
        "What's the charter PIN?"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"USER: {query}")
        print(f"{'='*60}")
        
        response = rick.chat(query)
        
        print(f"RICK: {response.text}")
        print(f"[{response.latency_ms}ms, confidence: {response.confidence:.1f}]")
        time.sleep(1)
    
    print(f"\n{'='*60}")
    print("✅ Test complete")
    print("\nTo integrate with dashboard:")
    print("1. Import: from rick_ollama_server import RickLocalLLM")
    print("2. Create: rick = RickLocalLLM()")
    print("3. Chat: response = rick.chat(user_message)")
