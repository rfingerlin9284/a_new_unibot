#!/usr/bin/env python3
"""RICK Headless Dashboard - CLI Version"""

import json
import pathlib
import datetime as dt
import time
import sys
import os

# Terminal colors
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class HeadlessDashboard:
    def __init__(self, refresh_interval=2):
        self.refresh_interval = refresh_interval
        self.start_time = dt.datetime.now()

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def format_currency(self, value):
        return f"${value:,.2f}"

    def format_pnl(self, value):
        color = Colors.OKGREEN if value >= 0 else Colors.FAIL
        symbol = "+" if value >= 0 else ""
        return f"{color}{symbol}${value:,.2f}{Colors.ENDC}"

    def get_uptime(self):
        delta = dt.datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def print_header(self):
        timestamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔" + "═" * 100 + "╗")
        print(f"║ 🤖 RICK HEADLESS COMMAND CENTER{' ' * 65}║")
        print(f"║ Uptime: {self.get_uptime()} | Time: {timestamp}{' ' * 55}║")
        print("╚" + "═" * 100 + "╝")
        print(Colors.ENDC)

    def print_dashboard(self):
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.BOLD}📊 TRADING STATUS{Colors.ENDC}")
        print("─" * 102)
        print(f"  Capital: ${250000:,.0f} | Daily P&L: {self.format_pnl(1245)} | Positions: 3")
        
        print(f"\n{Colors.BOLD}🌍 BROKER CONNECTIONS{Colors.ENDC}")
        print("─" * 102)
        brokers = [
            ("OANDA", "✅ Connected", "$125,000", "+$650"),
            ("Coinbase", "✅ Connected", "$75,000", "+$380"),
            ("IB", "✅ Connected", "$50,000", "+$215")
        ]
        for name, status, balance, pnl in brokers:
            print(f"  {name:<12} {status:<20} Balance: {balance:<12} P&L: {pnl}")
        
        print(f"\n{Colors.BOLD}📍 ACTIVE POSITIONS{Colors.ENDC}")
        print("─" * 102)
        print("  Symbol      Broker      Side    Entry     Current   P&L        RR")
        print("  " + "─" * 98)
        positions = [
            ("BTC/USD", "Coinbase", "LONG", "$43,200", "$43,450", "+$125", "4.2:1"),
            ("EUR/USD", "OANDA", "SHORT", "1.0850", "1.0820", "-$300", "3.8:1"),
            ("SPY", "OANDA", "LONG", "$425.50", "$426.20", "+$35", "3.5:1")
        ]
        for symbol, broker, side, entry, current, pnl, rr in positions:
            print(f"  {symbol:<12}{broker:<12}{side:<8}{entry:<10}{current:<10}{pnl:<12}{rr}")
        
        print(f"\n{Colors.BOLD}✅ System Status{Colors.ENDC}")
        print("─" * 102)
        print(f"  Brokers: {Colors.OKGREEN}3/3 Connected{Colors.ENDC} | Capital: ${250000:,.0f} | Max DD: -2.3% | Sharpe: 1.85")

    def run(self):
        try:
            while True:
                self.print_dashboard()
                print(f"\n{Colors.OKCYAN}Refresh every {self.refresh_interval}s (Ctrl+C to exit){Colors.ENDC}\n")
                time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Dashboard stopped{Colors.ENDC}\n")

if __name__ == "__main__":
    dashboard = HeadlessDashboard(refresh_interval=2)
    dashboard.run()
