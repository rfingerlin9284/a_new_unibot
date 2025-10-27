from __future__ import annotations
import os, requests
from datetime import datetime, timezone
from typing import List, Dict, Tuple
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from position_guardian.rules import Position, AccountState, split_symbol, pip_size_for

def _env(name, default=None):
    v=os.environ.get(name, default)
    if v is None: 
        raise RuntimeError(f"Missing env: {name}")
    return v

def _api_base():
    """Get OANDA API base URL from env, stripping any duplicate /v3."""
    explicit=os.environ.get("OANDA_API_URL", "").strip()
    if explicit: 
        url = explicit.rstrip("/")
        if url.endswith("/v3"):
            url = url[:-3]
        return url
    env=os.environ.get("OANDA_ENV","practice").lower()
    return "https://api-fxtrade.oanda.com" if env in ("live","fxtrade","production") else "https://api-fxpractice.oanda.com"

def _hdrs():
    return {"Authorization": f"Bearer {_env('OANDA_API_KEY')}", "Content-Type":"application/json"}

def _iso_to_dt(s:str):
    s=s.replace("Z","+00:00")
    return datetime.fromisoformat(s).astimezone(timezone.utc)

def _flat(sym:str)->str:
    return sym.replace("_","")

class OandaClient:
    def __init__(self):
        self.base=_api_base()
        self.account=_env("OANDA_ACCOUNT_ID")

    def account_summary(self)->Dict:
        r=requests.get(f"{self.base}/v3/accounts/{self.account}/summary",headers=_hdrs(),timeout=15)
        r.raise_for_status()
        return r.json()["account"]

    def open_trades(self)->List[Dict]:
        r=requests.get(f"{self.base}/v3/accounts/{self.account}/openTrades",headers=_hdrs(),timeout=20)
        r.raise_for_status()
        return r.json().get("trades",[])

    def pricing_mid(self, instruments:List[str])->Dict[str,float]:
        if not instruments: 
            return {}
        ins=",".join(sorted(set(instruments)))
        r=requests.get(f"{self.base}/v3/accounts/{self.account}/pricing",params={"instruments":ins},headers=_hdrs(),timeout=20)
        r.raise_for_status()
        mids={}
        for p in r.json().get("prices",[]):
            bid=float(p["closeoutBid"])
            ask=float(p["closeoutAsk"])
            mids[p["instrument"]]=(bid+ask)/2.0
        return mids

    def set_stop_loss(self, trade_id:str, price:float):
        url=f"{self.base}/v3/accounts/{self.account}/trades/{trade_id}/orders"
        payload={"stopLoss":{"price":f"{price:.10f}","timeInForce":"GTC"}}
        r=requests.put(url, json=payload, headers=_hdrs(), timeout=20)
        r.raise_for_status()
        return r.json()

    def close_trade_all(self, trade_id:str):
        url=f"{self.base}/v3/accounts/{self.account}/trades/{trade_id}/close"
        r=requests.put(url, json={"units":"ALL"}, headers=_hdrs(), timeout=20)
        r.raise_for_status()
        return r.json()

    def snapshot_positions_and_account(self)->Tuple[list,AccountState,dict]:
        trades=self.open_trades()
        instr=[t["instrument"] for t in trades]
        mids=self.pricing_mid(instr) if instr else {}
        acct=self.account_summary()
        positions=[]
        for t in trades:
            instr=t["instrument"]
            symbol=_flat(instr)
            units=float(t["currentUnits"])
            side="long" if units>0 else "short"
            entry=float(t["price"])
            cur=mids.get(instr, entry)
            opened=_iso_to_dt(t["openTime"])
            positions.append(Position(
                id=t["id"], symbol=symbol, side=side, units=abs(units),
                entry_price=entry, current_price=cur, stop_loss=None, opened_at=opened
            ))
        acct_state=AccountState(
            nav=float(acct["NAV"]),
            margin_used=float(acct["marginUsed"]),
            now_utc=datetime.now(timezone.utc),
        )
        return positions, acct_state, {"raw_account":acct,"mids":mids}
