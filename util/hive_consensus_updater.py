#!/usr/bin/env python3
"""
Hive Consensus Updater (Practice)

Purpose:
- Generate a live "hive consensus" value [0.0-1.0] from practice (paper) market data
- Writes to config/hive_consensus.json, which the engine already reads each cycle

Notes:
- This is a lightweight placeholder until a full Hive Mind service is online.
- Consensus is computed from short-term momentum agreement across TRADING_PAIRS.
  If most pairs move in the same direction (up or down) over the last poll,
  consensus increases; otherwise it decreases toward neutral.

Usage:
  python3 util/hive_consensus_updater.py             # loop (default 15s interval)
  python3 util/hive_consensus_updater.py --oneshot   # compute once & exit
  python3 util/hive_consensus_updater.py --interval 10

Environment:
- Reads OANDA practice credentials from env_new.env (same as autonomous engine)

Output file format (created if missing):
  config/hive_consensus.json
  {
    "consensus": 0.87,
    "timestamp": "2025-10-21T12:34:56Z",
    "method": "practice_momentum_v1"
  }
"""

import os
import sys
import time
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional

BASE_PATH = Path(__file__).resolve().parents[1]
CONFIG_DIR = BASE_PATH / "config"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONSENSUS_FILE = CONFIG_DIR / "hive_consensus.json"
DATA_DIR = BASE_PATH / "data"
PRICING_CACHE = DATA_DIR / "pricing.json"

# Reuse a tiny env loader (same shape as in autonomous_decision_engine)
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

# Keep in sync with engine's TRADING_PAIRS if possible
TRADING_PAIRS = [
    "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD",
    "NZD_USD", "EUR_GBP", "EUR_JPY"
]


# Ensure local util/ is NOT on sys.path as a top-level entry to avoid shadowing stdlib 'logging'
# Some scripts add `${workspace}/util` to sys.path; remove that here before importing requests
UTIL_DIR = str(BASE_PATH / "util")
try:
    import sys as _sys, os as _os
    _abs_paths = [
        _os.path.abspath(p) for p in list(_sys.path)
    ]
    _filtered = [p for p in _abs_paths if p != _os.path.abspath(UTIL_DIR)]
    # Preserve order by rebuilding path with filtered entries
    if len(_filtered) != len(_abs_paths):
        _sys.path[:] = _filtered
except Exception:
    pass

# Import after path hygiene
import requests


def read_cache_prices() -> Optional[Dict[str, float]]:
    """Optional: read mid prices from shared cache if fresh."""
    try:
        if not PRICING_CACHE.exists():
            return None
        # consider fresh if updated within last 60s
        mtime = PRICING_CACHE.stat().st_mtime
        if time.time() - mtime > 60:
            return None
        data = json.loads(PRICING_CACHE.read_text())
        mids = {}
        for sym, d in data.get("prices", {}).items():
            # expected d: {"bid": ..., "ask": ..., "mid": ...}
            mid = d.get("mid")
            if mid is None and "bid" in d and "ask" in d:
                mid = (float(d["bid"]) + float(d["ask"])) / 2
            if mid is not None:
                mids[sym] = float(mid)
        return mids or None
    except Exception:
        return None

def fetch_mid_prices(pairs: List[str]) -> Dict[str, float]:
    mids: Dict[str, float] = {}
    # Try cache first to unify data source across agents
    cache = read_cache_prices()
    if cache:
        # Return only the requested symbols
        return {k: v for k, v in cache.items() if k in pairs}
    # Batch-request: OANDA allows comma-separated instruments
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
            mids[p["instrument"]] = mid
    except Exception as e:
        print(f"[CONSENSUS] Pricing fetch failed: {e}")
    return mids


def compute_consensus(prev: Dict[str, float], curr: Dict[str, float]) -> float:
    """
    Momentum agreement consensus in [0.6, 0.95]:
      - Count fraction moving up vs down; take the dominant side's fraction
      - Map 50% → 0.60 (neutralish) and 100% → 0.95 (strong agreement)
    """
    if not prev or not curr:
        return 0.75  # neutral default until we have two samples

    ups = downs = 0
    for sym, mid_now in curr.items():
        mid_prev = prev.get(sym)
        if mid_prev is None:
            continue
        if mid_now > mid_prev:
            ups += 1
        elif mid_now < mid_prev:
            downs += 1
    total = ups + downs
    if total == 0:
        return 0.75

    dominant = max(ups, downs) / total  # 0.5..1.0
    # Map 0.5..1.0 → 0.60..0.95 linearly
    low_in, high_in = 0.5, 1.0
    low_out, high_out = 0.60, 0.95
    x = min(max(dominant, low_in), high_in)
    consensus = low_out + (x - low_in) * (high_out - low_out) / (high_in - low_in)
    return round(consensus, 4)


def write_consensus(value: float, *, plain: bool = False, quiet: bool = False):
    payload = {
        "consensus": float(value),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method": "practice_momentum_v1",
    }
    try:
        with open(CONSENSUS_FILE, "w") as f:
            json.dump(payload, f)
        if not quiet:
            if plain:
                pct = f"{value*100:.2f}%"
                print(f"Hive consensus {pct} — submitting to RBOTzilla for further analysis (smart logic, dynamic leverage & scaling, compounding, strategy logic, OCO TP/SL, adaptive trailing swarm shepherd bot).")
            else:
                print(f"[CONSENSUS] {value:.2%} → {CONSENSUS_FILE}")
    except Exception as e:
        print(f"[CONSENSUS] Failed to write file: {e}")


def validate_creds():
    if not OANDA_ACCOUNT_ID or not OANDA_API_TOKEN:
        sys.stderr.write("[FATAL] Missing OANDA practice credentials in env_new.env (OANDA_PRACTICE_ACCOUNT_ID/TOKEN)\n")
        sys.exit(2)


def main():
    parser = argparse.ArgumentParser(description="Live Hive Consensus updater (practice)")
    parser.add_argument("--interval", type=int, default=15, help="Polling interval seconds (default: 15)")
    parser.add_argument("--oneshot", action="store_true", help="Compute once and exit")
    parser.add_argument("--plain", action="store_true", help="Print plain-English status lines (no file paths)")
    parser.add_argument("--quiet", action="store_true", help="No console prints; just update the JSON file")
    args = parser.parse_args()

    validate_creds()

    prev = fetch_mid_prices(TRADING_PAIRS)
    time.sleep(1.0)  # small gap for first delta

    while True:
        curr = fetch_mid_prices(TRADING_PAIRS)
        value = compute_consensus(prev, curr)
        write_consensus(value, plain=args.plain, quiet=args.quiet)
        prev = curr

        if args.oneshot:
            break
        time.sleep(max(1, args.interval))


if __name__ == "__main__":
    main()
