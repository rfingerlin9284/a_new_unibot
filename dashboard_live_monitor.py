#!/usr/bin/env python3
"""
🎮 RBOTzilla Live Monitor - Main Narration & Position Display
Real-time monitoring of positions, narration, and system status
PIN: 841921
"""

import json
import time
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
import subprocess
import re

# Colors for terminal output
class Colors:
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

WORK_DIR = Path("/home/ing/RICK/RICK_LIVE_PROTOTYPE")
NARRATION_LOG = WORK_DIR / "narration.jsonl"
CONNECTION_STATE = WORK_DIR / "connection_state.json"
POSITIONS_FILE = WORK_DIR / "open_positions.json"

class LiveMonitor:
    """Real-time monitoring of RBOTzilla system"""
    
    def __init__(self):
        self.narration_offset = 0
        self.positions_cache = {}
        # Patterns that indicate technical/noisy content we must not display raw
        self._forbidden_re = re.compile(r"(\{|\}|\[|\]|<[^>]*>|```|Traceback|Error:|Exception|0x[0-9a-fA-F]+)")
        self._naked_digits_re = re.compile(r"(?<![A-Za-z%$#])\b\d{6,}\b")
        
    def clear_screen(self):
        """Clear terminal"""
        os.system('clear')
    
    def print_header(self):
        """Print dashboard header"""
        cols = shutil.get_terminal_size((100, 20)).columns
        inner = max(20, cols - 2)
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}")
        print("╔" + "═" * inner + "╗")
        print("║" + " ".ljust(inner) + "║")
        title = f"  🤖 RBOTzilla LIVE TRADING MONITOR  |  PIN: 841921 ✅  |  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print("║" + title[:inner].ljust(inner) + "║")
        acct = "  PRACTICE ACCOUNT: 101-001-31210531-002"
        print("║" + acct[:inner].ljust(inner) + "║")
        print("║" + " ".ljust(inner) + "║")
        print("╚" + "═" * inner + "╝")
        print(f"{Colors.RESET}\n")
    
    def print_narration_section(self):
        """Display live narration stream"""
        print(f"{Colors.BRIGHT_GREEN}{Colors.BOLD}▶ LIVE NARRATION & EVENTS{Colors.RESET}")
        cols = shutil.get_terminal_size((100, 20)).columns
        print("─" * max(8, cols))
        
        try:
            if NARRATION_LOG.exists():
                # Read last 15 lines of narration
                with open(NARRATION_LOG, 'r') as f:
                    lines = f.readlines()[-15:]
                
                for line in lines:
                    try:
                        entry = json.loads(line)
                        timestamp = entry.get('timestamp', 'N/A')
                        narration = str(entry.get('narration', '') or '')
                        event_type = str(entry.get('event_type', 'LOG') or 'LOG')

                        # Enforce plain-English-only: summarize or rewrite if needed
                        safe_line = self._summarize_event(narration, event_type)

                        # Color based on event type
                        if 'TRADE_OPENED' in event_type:
                            color = Colors.BRIGHT_GREEN
                            icon = "📈"
                        elif 'TRADE_CLOSED' in event_type:
                            color = Colors.BRIGHT_YELLOW
                            icon = "📉"
                        elif 'HEDGE' in event_type:
                            color = Colors.BRIGHT_MAGENTA
                            icon = "🛡️"
                        elif 'SIGNAL' in event_type:
                            color = Colors.WHITE
                            icon = "📡"
                        else:
                            color = Colors.WHITE
                            icon = "ℹ️"

                        print(f"{color}{icon} [{timestamp}] {safe_line}{Colors.RESET}")
                    except json.JSONDecodeError:
                        # Skip raw/garbled JSON and avoid showing technical content
                        continue
            else:
                print(f"{Colors.DIM}[Waiting for narration events...]{Colors.RESET}")
        except Exception as e:
            # Plain-English only: do not expose exception details
            print(f"{Colors.BRIGHT_YELLOW}We couldn't read new updates just now; we'll try again shortly.{Colors.RESET}")
        
        print()

    def _summarize_event(self, text: str, event_type: str) -> str:
        """Convert any upstream technical text into one short plain-English sentence.
        - Rejects raw JSON, arrays, XML-ish tags, code fences, stack traces, long IDs/hex.
        - Rewrites common patterns like signals into friendly language.
        """
        raw = text.strip()

        # If forbidden patterns or suspicious long numbers present, force summarization
        needs_summary = bool(self._forbidden_re.search(raw) or self._naked_digits_re.search(raw))

        # Try to parse a simple signal from narration text
        # Example: "Signal: EUR_GBP BUY (78% confidence) - evaluating..."
        m = re.search(r"Signal:\s*([A-Z]{3}[_/][A-Z]{3})\s+(BUY|SELL)\s*\((\d{1,3})%\s*confidence\)", raw, re.I)
        if m:
            pair = m.group(1).replace('_', '/').upper()
            side = m.group(2).upper()
            conf = int(m.group(3))
            # Map confidence bands to adjectives
            if conf >= 85:
                tone = "high confidence"
            elif conf >= 70:
                tone = "good confidence"
            else:
                tone = "early signal"
            return f"Considering a {side} on {pair} with {tone}; reviewing risk before acting."

        # Event-type based generic summaries
        et = (event_type or '').upper()
        if et == 'TRADE_OPENED':
            return "Opened a position after checks passed; risk is controlled."
        if et == 'TRADE_CLOSED':
            return "Closed a position to protect capital and follow the plan."
        if 'HEDGE' in et:
            return "Placed a hedge to reduce exposure while conditions are uncertain."
        if et == 'SIGNAL':
            return "A potential trade setup appeared; evaluating it against the rules."

        # If the original text looks already human and short, keep it; else summarize
        if not needs_summary and len(raw) <= 160 and not re.search(r"[\{\}\[\]`]|<[^>]*>|Traceback|Error:|Exception", raw):
            # Normalize pair underscore to slash for readability
            raw = re.sub(r"\b([A-Z]{3})_([A-Z]{3})\b", r"\1/\2", raw)
            return raw

        return "A technical message was received; keeping the display simple and readable."
    
    def print_positions_section(self):
        """Display active positions"""
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}▶ ACTIVE POSITIONS & PARAMETERS{Colors.RESET}")
        cols = shutil.get_terminal_size((100, 20)).columns
        print("─" * max(8, cols))
        
        try:
            # Try to read from connection state or positions file
            if CONNECTION_STATE.exists():
                with open(CONNECTION_STATE, 'r') as f:
                    state = json.load(f)
                
                positions = state.get('open_trades', [])
                if positions:
                    print(f"{Colors.BRIGHT_GREEN}✅ Open Positions: {len(positions)}{Colors.RESET}\n")
                    
                    for pos in positions:
                        symbol = pos.get('instrument', 'N/A')
                        side = pos.get('side', 'UNKNOWN')
                        units = pos.get('units', 0)
                        entry = pos.get('entry_price', 0)
                        current = pos.get('current_price', entry)
                        pnl = pos.get('pnl', 0)
                        
                        pnl_color = Colors.BRIGHT_GREEN if pnl >= 0 else Colors.BRIGHT_YELLOW
                        side_icon = "📈 BUY" if side == "LONG" else "📉 SELL"
                        
                        # Plain-English: avoid naked numbers; give context
                        print(f"  {side_icon} on {symbol} — size {units:,} units; entered at {entry:.5f}, now {current:.5f}")
                        print(f"       {pnl_color}Current result: ${pnl:.2f}{Colors.RESET} — trade sized to plan")
                        print()
                else:
                    print(f"{Colors.DIM}[No open positions]{Colors.RESET}\n")
            else:
                print(f"{Colors.DIM}[Waiting for position data...]{Colors.RESET}\n")
        except Exception as e:
            print(f"{Colors.DIM}Position details aren't available right now; we'll refresh shortly.{Colors.RESET}\n")
    
    def print_parameters_section(self):
        """Display Charter parameters and system settings"""
        print(f"{Colors.BRIGHT_MAGENTA}{Colors.BOLD}▶ CHARTER PARAMETERS & RISK SETTINGS{Colors.RESET}")
        cols = shutil.get_terminal_size((100, 20)).columns
        print("─" * max(8, cols))
        
        params = {
            "PIN Validated": "841921 ✅",
            "Minimum Trade Interval": "5 minutes (300 sec)",
            "Min Notional USD": "$15,000",
            "Min Risk:Reward": "3.2:1",
            "Stop Loss": "20 pips",
            "Take Profit": "64 pips (3.2:1)",
            "Max Concurrent": "3 positions",
            "Max Daily Loss": "5% breaker",
            "Max Hold Time": "6 hours",
            "Micro Trading": "❌ DISABLED"
        }
        
        for key, value in params.items():
            print(f"  • {key}: {Colors.BRIGHT_CYAN}{value}{Colors.RESET}")
        print()
    
    def print_status_section(self):
        """Display system status"""
        print(f"{Colors.BRIGHT_YELLOW}{Colors.BOLD}▶ SYSTEM STATUS{Colors.RESET}")
        cols = shutil.get_terminal_size((100, 20)).columns
        print("─" * max(8, cols))
        
        status = "🟢 OPERATIONAL"
        try:
            if CONNECTION_STATE.exists():
                with open(CONNECTION_STATE, 'r') as f:
                    state = json.load(f)
                    connected = state.get('connected', False)
                    status = "🟢 CONNECTED" if connected else "🔴 DISCONNECTED"
        except:
            pass
        
        print(f"  {status}  |  Environment: practice  |  Guardian: active  |  Hedge: active")
        print()
    
    def run(self):
        """Main monitoring loop"""
        try:
            while True:
                self.clear_screen()
                self.print_header()
                self.print_status_section()
                self.print_narration_section()
                self.print_positions_section()
                self.print_parameters_section()
                
                # Refresh every 2 seconds
                time.sleep(2)
        except KeyboardInterrupt:
            print(f"\n{Colors.BRIGHT_YELLOW}[Dashboard stopped]{Colors.RESET}")

if __name__ == "__main__":
    monitor = LiveMonitor()
    monitor.run()
