#!/usr/bin/env python3
"""
IBKR Gateway Port Check (Plain-English)
- Checks if the local IB Gateway/TWS API port is reachable.
- Defaults: paper=4002, live=4001 (override via IB_API_PORT)
"""
import os
import sys
import socket
from datetime import datetime, timezone

MODE = os.getenv("IB_TRADING_MODE", "paper").lower()
PORT = int(os.getenv("IB_API_PORT", "0")) or (4002 if MODE == "paper" else 4001)
HOST = os.getenv("IB_API_HOST", "127.0.0.1")

def check_port(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

if __name__ == "__main__":
    reachable = check_port(HOST, PORT)
    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    if reachable:
        print(f"IB Gateway: {MODE} port {PORT} reachable on {HOST} | {ts}")
        print("API looks up — ensure API is enabled in settings and Client ID is configured.")
    else:
        print(f"IB Gateway: not reachable on {HOST}:{PORT} ({MODE}) | {ts}")
        print("Start IB Gateway/TWS and enable API (paper default port 4002, live 4001).")
        sys.exit(1)
