#!/usr/bin/env python3
from datetime import datetime, timezone
from dataclasses import dataclass
import os, sys, requests
from pathlib import Path

# Minimal OANDA snapshot with fallback to env_new.env in the same project root
ROOT = Path(__file__).resolve().parents[2]  # .../RICK_LIVE_PROTOTYPE
ENV_FALLBACK = ROOT / 'env_new.env'

def _parse_env_file(path: Path) -> dict:
    env = {}
    try:
        for raw in path.read_text().splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            k, v = line.split('=', 1)
            v = v.strip().strip("'\"")
            if v.startswith('-----BEGIN '):
                continue
            env[k.strip()] = v
    except Exception:
        pass
    return env

fallback_env = _parse_env_file(ENV_FALLBACK)
BASE = os.environ.get('OANDA_PRACTICE_BASE_URL') or fallback_env.get('OANDA_PRACTICE_BASE_URL','https://api-fxpractice.oanda.com/v3')
ACCT = os.environ.get('OANDA_PRACTICE_ACCOUNT_ID') or os.environ.get('OANDA_ACCOUNT_ID') or fallback_env.get('OANDA_PRACTICE_ACCOUNT_ID')
TOK  = os.environ.get('OANDA_PRACTICE_TOKEN') or os.environ.get('OANDA_API_TOKEN') or os.environ.get('OANDA_TOKEN') or fallback_env.get('OANDA_PRACTICE_TOKEN')

if not ACCT or not TOK:
    print("[status] Missing OANDA practice credentials. Set env vars or ensure env_new.env exists with OANDA_PRACTICE_*.")
    sys.exit(2)

HDR = {'Authorization': f'Bearer {TOK}', 'Content-Type': 'application/json'}

def pip_size(symbol: str) -> float:
    return 0.01 if symbol.endswith('JPY') else 0.0001

@dataclass
class Position:
    symbol: str
    side: str
    units: float
    entry_price: float
    current_price: float
    opened_at: datetime
    stop_loss: float|None

def fetch_account():
    r = requests.get(f"{BASE}/accounts/{ACCT}/summary", headers=HDR, timeout=10)
    r.raise_for_status()
    a = r.json()['account']
    return float(a['NAV']), float(a.get('marginUsed',0) or 0)

def fetch_positions():
    r = requests.get(f"{BASE}/accounts/{ACCT}/openPositions", headers=HDR, timeout=10)
    r.raise_for_status()
    out = []
    for p in r.json().get('positions', []):
        instr = p['instrument']
        for leg, side in (('long','long'),('short','short')):
            legd = p.get(leg, {})
            units = float(legd.get('units', 0))
            if units == 0:
                continue
            entry = float(legd.get('averagePrice') or legd.get('price', 0) or 0)
            pr = requests.get(f"{BASE}/accounts/{ACCT}/pricing", headers=HDR, params={'instruments': instr}, timeout=10)
            pr.raise_for_status()
            prj = pr.json()['prices'][0]
            bid = float(prj['bids'][0]['price']); ask=float(prj['asks'][0]['price'])
            cur = bid if side=='long' else ask
            opened_at = datetime.now(timezone.utc)
            stop = None
            out.append( Position(instr, side, abs(units), entry, cur, opened_at, stop) )
    return out

if __name__ == '__main__':
    nav, used = fetch_account()
    mu = 0.0 if nav<=0 else used/nav
    pos = fetch_positions()

    def net_usd_exposure(p: Position) -> float:
        b,q = p.symbol.split('_')
        s = 1 if p.side=='long' else -1
        if q=='USD':
            return -s*p.units
        if b=='USD':
            return  s*p.units
        return 0.0

    net_usd = sum(net_usd_exposure(p) for p in pos)

    print(f"UTC: {datetime.now(timezone.utc).isoformat()}")
    print(f"NAV: ${nav:,.2f} | Margin Used: ${used:,.2f} | Utilization: {mu*100:.1f}% | Net USD units: {net_usd:,.0f}")

    if mu>0.35:
        print("⚠️  Over 35% margin: reduce or hedge before adding risk.")
    if net_usd!=0:
        print(f"ℹ️  Single-sided USD exposure detected ({'short' if net_usd<0 else 'long'} USD). Consider a cross/hedge.")

    if not pos:
        print("\nOpen positions: (none)")
        sys.exit(0)

    print("\nOpen positions:")
    for p in pos:
        pip = pip_size(p.symbol)
        pips = (p.current_price - p.entry_price) * (1 if p.side=='long' else -1) / pip
        age_h = (datetime.now(timezone.utc) - p.opened_at).total_seconds()/3600
        flags = []
        if pips>=25: flags.append("BE+5 eligible")
        if pips>=40: flags.append("Trail start")
        if pips>=60: flags.append("Trail tighten")
        if age_h>=6: flags.append("6h cap CLOSE")
        elif age_h>=3 and pips<0.5: flags.append("3h <0.5R CLOSE (approx)")
        print(f" - {p.symbol} {p.side} {int(p.units)} | pips {pips:.1f} | age {age_h:.2f}h | flags: {', '.join(flags) or '—'}")
