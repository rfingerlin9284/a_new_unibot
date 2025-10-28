#!/usr/bin/env python3
"""
IBKR Paper Account Status
Quick, plain-English status for IB Gateway paper connection and account summary.
"""
import os
import sys
import json
import logging
from pathlib import Path

# Keep output short and human
logging.basicConfig(level=logging.WARNING)

# Ensure repository root on path for 'brokers' package imports
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

try:
    from brokers.ib_connector import IBConnector
except Exception as e:
    print("IBKR status: not available (connector import failed)")
    print(f"Why: {e}")
    sys.exit(1)


def main():
    # Default to paper
    env = os.getenv("IB_TRADING_MODE", "paper")
    try:
        ib = IBConnector(pin=841921, environment=env)
        if getattr(ib, 'connected', False):
            summary = ib.get_account_summary()
            acct = summary.get('account_id', 'unknown')
            nav = summary.get('net_liquidation') or summary.get('balance') or 0.0
            avail = summary.get('available_capital', 0.0)
            print(f"IBKR paper: connected | account {acct} | equity ${nav:,.2f} | available ${avail:,.2f}")
        else:
            print("IBKR paper: not connected")
        try:
            ib.disconnect()
        except Exception:
            pass
        sys.exit(0)
    except Exception as e:
        print("IBKR paper: not connected")
        print(f"Why: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
