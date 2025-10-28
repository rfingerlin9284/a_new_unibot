#!/usr/bin/env python3
"""
Shared Pricing Cache Updater (Practice)

- Poll OANDA practice pricing for a set of instruments
- Write a shared cache file at data/pricing.json with bid/ask/mid and timestamp
- All agents (Rick, Hive, ML models, logic agents) can read this file to share
  a single unified data source without duplicate API calls.

Usage:
  python3 util/pricing_cache_updater.py --interval 2 --pairs EUR_USD,GBP_USD

Notes:
- Keeps the JSON tiny and easy to parse in any language/tool.
- Designed to run alongside the engine and dashboards.
"""
import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

BASE_PATH = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_PATH / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
CACHE_FILE = DATA_DIR / "pricing.json"

# Avoid util/logging.py shadowing stdlib 'logging' used by requests/urllib3
UTIL_DIR = str(BASE_PATH / "util")
try:
    import sys as _sys, os as _os
    _abs_paths = [_os.path.abspath(p) for p in list(_sys.path)]
    _filtered = [p for p in _abs_paths if p != _os.path.abspath(UTIL_DIR)]
    if len(_filtered) != len(_abs_paths):
        _sys.path[:] = _filtered
except Exception:
    pass

import requests  # after path hygiene

# Load OANDA creds from env_new.env like the engine

def _load_env_file(env_file: Path) -> Dict[str, str]:
    env = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('\"\'')
    except FileNotFoundError:
        pass
    return env

ENV_DATA = _load_env_file(BASE_PATH / "env_new.env")
OANDA_ACCOUNT_ID = ENV_DATA.get("OANDA_PRACTICE_ACCOUNT_ID")
OANDA_API_TOKEN = ENV_DATA.get("OANDA_PRACTICE_TOKEN")
API_BASE = "https://api-fxpractice.oanda.com"
HEADERS = {"Authorization": f"Bearer {OANDA_API_TOKEN}", "Content-Type": "application/json"}

DEFAULT_PAIRS = [
    "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD",
    "NZD_USD", "EUR_GBP", "EUR_JPY"
]


def fetch_pricing(pairs: List[str]) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {}
    chunk = ",".join(pairs)
    try:
        r = requests.get(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/pricing",
            headers=HEADERS,
            params={"instruments": chunk},
            timeout=10,
        )
        r.raise_for_status()
        for p in r.json().get("prices", []):
            bid = float(p["bids"][0]["price"]) ; ask = float(p["asks"][0]["price"]) ; mid = (bid+ask)/2
            out[p["instrument"]] = {"bid": bid, "ask": ask, "mid": mid}
    except Exception as e:
        print(f"[PRICING] fetch failed: {e}")
    return out


def write_cache(prices: Dict[str, Dict[str, float]]):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prices": prices,
    }
    try:
        CACHE_FILE.write_text(json.dumps(payload))
        print(f"[PRICING] Updated {CACHE_FILE} ({len(prices)} symbols)")
    except Exception as e:
        print(f"[PRICING] write failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Shared pricing cache updater (practice)")
    parser.add_argument("--interval", type=float, default=2.0, help="Polling interval seconds (default 2.0)")
    parser.add_argument("--pairs", type=str, default=",".join(DEFAULT_PAIRS), help="Comma-separated instruments")
    args = parser.parse_args()

    pairs = [p.strip() for p in args.pairs.split(',') if p.strip()]
    if not OANDA_ACCOUNT_ID or not OANDA_API_TOKEN:
        raise SystemExit("[FATAL] Missing OANDA practice credentials in env_new.env")

    while True:
        prices = fetch_pricing(pairs)
        if prices:
            write_cache(prices)
        time.sleep(max(0.5, args.interval))


if __name__ == "__main__":
    main()
