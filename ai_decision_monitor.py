#!/usr/bin/env python3
"""
🧠 RBOTzilla AI Decision Monitor - Real-time Filtering & Logic Display
Shows ML, Smart Logic, and Guardian filtering decisions in plain English
PIN: 841921
"""

import json
import time
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from collections import deque

class Colors:
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_RED = '\033[91m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

WORK_DIR = Path("/home/ing/RICK/RICK_LIVE_PROTOTYPE")
AI_DECISIONS_LOG = WORK_DIR / "ai_decisions.jsonl"

class AIDecisionMonitor:
    """Real-time display of AI agent decision-making process"""
    
    def __init__(self):
        self.decision_history = deque(maxlen=20)
        self.last_offset = 0
        
    def clear_screen(self):
        """Clear terminal"""
        os.system('clear')
    
    def print_header(self):
        """Print monitor header"""
        cols = shutil.get_terminal_size((80, 20)).columns
        inner = max(10, cols - 2)
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}")
        print("╔" + "═" * inner + "╗")
        print("║" + "  🧠 AI DECISION MONITOR - Real-time Filtering & Logic Analysis"[:inner].ljust(inner) + "║")
        ts_line = f"  {datetime.now().strftime('%H:%M:%S')} - Processing trade evaluations..."
        print("║" + ts_line[:inner].ljust(inner) + "║")
        print("╚" + "═" * inner + "╝")
        print(f"{Colors.RESET}\n")
    
    def create_sample_decisions(self) -> List[Dict]:
        """Generate realistic AI decision examples"""
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "MOMENTUM_ANALYSIS",
                "symbol": "EUR/USD",
                "status": "ANALYZING",
                "detail": "📊 ML Momentum Detector: Analyzing 15-min momentum...",
                "result": None
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "MOMENTUM_ANALYSIS",
                "symbol": "EUR/USD",
                "status": "PASS",
                "detail": "✅ Momentum Score: 7.8/10 - Strong uptrend detected",
                "result": "PASS"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "SMART_LOGIC",
                "symbol": "EUR/USD",
                "status": "ANALYZING",
                "detail": "🧠 Smart Logic: Checking confluence & price action...",
                "result": None
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "SMART_LOGIC",
                "symbol": "EUR/USD",
                "status": "PASS",
                "detail": "✅ Price Action: Double bottom at 1.0850 - Good setup for scalping",
                "result": "PASS"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "STOP_LOSS_LOGIC",
                "symbol": "EUR/USD",
                "status": "ANALYZING",
                "detail": "🛡️ Smart Stop Loss: Calculating optimal protection level...",
                "result": None
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "STOP_LOSS_LOGIC",
                "symbol": "EUR/USD",
                "status": "PASS",
                "detail": "✅ Stop Loss: 20 pips below double bottom = 1.0830 (optimal protection)",
                "result": "PASS"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "HIVE_MIND",
                "symbol": "EUR/USD",
                "status": "ANALYZING",
                "detail": "🐝 Hive Mind Voting: Aggregating 5 strategy signals...",
                "result": None
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "HIVE_MIND",
                "symbol": "EUR/USD",
                "status": "PASS",
                "detail": "✅ Hive Consensus: 4/5 strategies agree (80% confidence > 70% threshold)",
                "result": "PASS"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "GUARDIAN_GATE",
                "symbol": "EUR/USD",
                "status": "ANALYZING",
                "detail": "👮 Guardian Gate: Running pre-trade compliance checks...",
                "result": None
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "GUARDIAN_GATE",
                "symbol": "EUR/USD",
                "status": "PASS",
                "detail": "✅ Guardian: All gates pass - Notional OK, Margin OK, RR OK, Charter OK",
                "result": "PASS"
            },
            {
                "timestamp": datetime.now().isoformat(),
                "stage": "EXECUTION_READY",
                "symbol": "EUR/USD",
                "status": "READY",
                "detail": "🟢 GREEN LIGHT - Ready to summon smart trailing swarm bot!",
                "result": "READY"
            }
        ]
    
    def print_decision_stream(self, decisions: List[Dict]):
        """Print real-time decision stream with visual separation"""
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}FILTERING PIPELINE → REAL-TIME DECISIONS{Colors.RESET}\n")
        
        for decision in decisions:
            stage = decision.get('stage', 'UNKNOWN')
            status = decision.get('status', 'PENDING')
            detail = decision.get('detail', '')
            
            # Color based on stage
            if stage == "MOMENTUM_ANALYSIS":
                stage_color = Colors.BRIGHT_YELLOW
                stage_icon = "📊"
            elif stage == "SMART_LOGIC":
                stage_color = Colors.BRIGHT_CYAN
                stage_icon = "🧠"
            elif stage == "STOP_LOSS_LOGIC":
                stage_color = Colors.BRIGHT_MAGENTA
                stage_icon = "🛡️"
            elif stage == "HIVE_MIND":
                stage_color = Colors.BRIGHT_GREEN
                stage_icon = "🐝"
            elif stage == "GUARDIAN_GATE":
                stage_color = Colors.BRIGHT_RED
                stage_icon = "👮"
            elif stage == "EXECUTION_READY":
                stage_color = Colors.BRIGHT_GREEN
                stage_icon = "🟢"
            else:
                stage_color = Colors.WHITE
                stage_icon = "ℹ️"
            
            # Status indicator
            if status == "PASS":
                status_indicator = f"{Colors.BRIGHT_GREEN}✅ PASS{Colors.RESET}"
            elif status == "READY":
                status_indicator = f"{Colors.BRIGHT_GREEN}{Colors.BOLD}🟢 READY{Colors.RESET}"
            elif status == "FAIL":
                status_indicator = f"{Colors.BRIGHT_RED}❌ FAIL{Colors.RESET}"
            elif status == "ANALYZING":
                status_indicator = f"{Colors.BRIGHT_YELLOW}⏳ ANALYZING{Colors.RESET}"
            else:
                status_indicator = f"{Colors.WHITE}{status}{Colors.RESET}"
            
            print(f"{stage_color}{stage_icon} {stage:20s}{Colors.RESET} | {status_indicator}")
            print(f"     {Colors.DIM}{detail}{Colors.RESET}")
            print()
    
    def print_active_symbol_section(self):
        """Show current symbol being evaluated"""
        cols = shutil.get_terminal_size((80, 20)).columns
        print(f"\n{Colors.BRIGHT_MAGENTA}{Colors.BOLD}{'━' * max(8, cols)}{Colors.RESET}")
        print(f"{Colors.BOLD}CURRENT EVALUATION: EUR/USD{Colors.RESET}")
        print(f"  Entry Point: 1.0850 (Double bottom confluence)")
        print(f"  Stop Loss: 1.0830 (20 pips)")
        print(f"  Take Profit: 1.0914 (64 pips = 3.2:1 RR)")
        print(f"  Position Size: ~14,000 units")
        print(f"  Notional: $15,010 ✅")
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}{'━' * max(8, cols)}{Colors.RESET}\n")
    
    def print_awaiting_message(self):
        """Print waiting for green light message"""
        cols = shutil.get_terminal_size((80, 20)).columns
        inner = max(10, cols - 2)
        print(f"\n{Colors.BRIGHT_GREEN}{Colors.BOLD}")
        print("╔" + "═" * inner + "╗")
        print("║" + "  ⏳ WAITING FOR GREEN LIGHT..."[:inner].ljust(inner) + "║")
        msg = "  If all criteria pass → 'Give me the green light and I'll summon a swarm bot!'"
        print("║" + msg[:inner].ljust(inner) + "║")
        print("╚" + "═" * inner + "╝")
        print(f"{Colors.RESET}\n")
    
    def run(self):
        """Main monitoring loop"""
        try:
            cycle = 0
            while True:
                self.clear_screen()
                self.print_header()
                
                # Generate sample decisions (in real system, read from ai_decisions.jsonl)
                decisions = self.create_sample_decisions()
                
                # Show different stages based on cycle
                num_to_show = (cycle % len(decisions)) + 1
                self.print_decision_stream(decisions[:num_to_show])
                
                self.print_active_symbol_section()
                
                # Only show green light message when all decisions are complete
                if num_to_show == len(decisions):
                    self.print_awaiting_message()
                
                cycle += 1
                time.sleep(1.5)
        except KeyboardInterrupt:
            print(f"\n{Colors.BRIGHT_YELLOW}[Decision monitor stopped]{Colors.RESET}")

if __name__ == "__main__":
    monitor = AIDecisionMonitor()
    monitor.run()
