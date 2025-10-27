#!/usr/bin/env python3
"""
RICK CLI Dashboard
PIN 841921 | CANARY Mode | Real OANDA Paper Trading
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from canary_oanda_connector import CanaryOandaConnector
from datetime import datetime
import time

def main():
    print("\n✅ Connecting to OANDA Paper Trading...\n")
    
    try:
        conn = CanaryOandaConnector(pin=841921)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return
    
    print("🤖 RICK OANDA PAPER DASHBOARD\n")
    
    refresh = 0
    try:
        while True:
            refresh += 1
            acct = conn.get_account_summary()
            
            if acct:
                print(f"\n📊 Refresh #{refresh} | {datetime.now().strftime('%H:%M:%S')}")
                print(f"   Account:  {acct.account_id}")
                print(f"   Balance:  ${acct.balance:,.2f}")
                print(f"   P&L:      ${acct.unrealized_pnl:,.2f}")
                print(f"   Margin:   ${acct.margin_available:,.2f}")
            
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n\n✅ Done.\n")

if __name__ == "__main__":
    main()
