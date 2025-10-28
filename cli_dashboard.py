#!/usr/bin/env python3
"""RICK CLI Dashboard - Real OANDA Paper Trading Data"""
import sys
import os
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent))
from canary_oanda_connector import CanaryOandaConnector

class Colors:
    HEADER = '\033[95m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def fmt_usd(v):
    return f"${v:,.2f}"

def fmt_pnl(v):
    c = Colors.OKGREEN if v >= 0 else Colors.FAIL
    s = "+" if v >= 0 else ""
    return f"{c}{s}${v:,.2f}{Colors.ENDC}"

try:
    conn = CanaryOandaConnector(pin=841921)
    print(f"\n{Colors.OKGREEN}✅ OANDA Paper Trading Connected{Colors.ENDC}\n")
    
    count = 0
    while True:
        clear()
        count += 1
        
        acct = conn.get_account_summary()
        pos = conn.get_open_positions()
        pri = conn.get_pricing(['EUR_USD', 'GBP_USD'])
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}")
        print("╔" + "═" * 90 + "╗")
        print(f"║ 🤖 RICK OANDA PAPER DASHBOARD (PIN 841921){' ' * 42}║")
        print(f"║ {ts} | Refresh #{count}{' ' * 69}║")
        print("╚" + "═" * 90 + "╝")
        print(Colors.ENDC)
        
        if acct:
            print(f"\n{Colors.BOLD}💰 ACCOUNT{Colors.ENDC}")
            print("─" * 90)
            print(f"  Account:  {acct.account_id}")
            print(f"  Balance:  {fmt_usd(acct.balance)}")
            print(f"  Unrealized P&L:  {fmt_pnl(acct.unrealized_pnl)}")
            print(f"  Margin Available:  {fmt_usd(acct.margin_available)}")
        
        print(f"\n{Colors.BOLD}📍 POSITIONS{Colors.ENDC}")
        print("─" * 90)
        if pos:
            print(f"  {'Instrument':<15} {'Long Units':<15} {'Long P&L':<15} {'Short Units':<15} {'Short P&L':<15}")
            for p in pos:
                lc = Colors.OKGREEN if p.long_pnl >= 0 else Colors.FAIL
                sc = Colors.OKGREEN if p.short_pnl >= 0 else Colors.FAIL
                print(f"  {p.instrument:<15} {p.long_units:<15} {lc}${p.long_pnl:,.2f}{Colors.ENDC:<15} {p.short_units:<15} {sc}${p.short_pnl:,.2f}{Colors.ENDC}")
        else:
            print(f"  {Colors.WARNING}(No positions){Colors.ENDC}")
        
        if pri:
            print(f"\n{Colors.BOLD}💱 PRICING{Colors.ENDC}")
            print("─" * 90)
            for pair, price in pri.items():
                print(f"  {pair:<15} {price:>10.5f}")
        
        print(f"\n{Colors.HEADER}{Colors.BOLD}╚" + "═" * 90 + "╝{Colors.ENDC}")
        print(f"\n{Colors.OKCYAN}Next in 5s (Ctrl+C to exit){Colors.ENDC}")
        time.sleep(5)

except KeyboardInterrupt:
    print(f"\n\n{Colors.WARNING}Done.{Colors.ENDC}\n")
except Exception as e:
    print(f"\n{Colors.FAIL}Error: {e}{Colors.ENDC}\n")
