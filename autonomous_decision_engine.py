#!/usr/bin/env python3
"""
UNIFIED AUTONOMOUS TRADING ENGINE v3
Opens new positions AND manages existing positions autonomously.
Combines signal generation + position management + Charter compliance.
NO HUMAN INTERVENTION REQUIRED.

Features:
- Generates trading signals (random walk or external signal integration)
- Opens Charter-compliant positions with OCO orders
- Monitors and manages existing positions (profit-taking, loss-cutting, SL/TP management)
- Full OANDA API integration (practice/live)
- Immutable risk management (PIN: 841921)
- Pre-trade gate validation (margin + correlation)
"""

import os
import sys
import json
import time
import requests
import argparse
import random
import logging
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import subprocess
from pathlib import Path

# Import Guardian Gate System
try:
    from foundation.margin_correlation_gate import MarginCorrelationGate, Position as GatePosition, Order as GateOrder, HookResult
    GATES_AVAILABLE = True
except ImportError:
    print("[WARN] Guardian gates not available - running without pre-trade validation")
    GATES_AVAILABLE = False

# Simple environment loader (proven working from practice_oanda_connector.py)
def _load_env_file(env_file: Path) -> Dict[str, str]:
    """Load environment variables from file (simple key=value parsing)"""
    env = {}
    try:
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    env[k.strip()] = v.strip().strip('"\'')
        return env
    except FileNotFoundError:
        return {}

# Resolve project base dynamically (folder containing this script)
BASE_PATH = Path(__file__).resolve().parent
BASE = str(BASE_PATH)

# Load from env_new.env (proven working approach from Oct 17th)
ENV_DATA = _load_env_file(BASE_PATH / "env_new.env")

# Extract OANDA credentials
OANDA_ACCOUNT_ID = ENV_DATA.get("OANDA_PRACTICE_ACCOUNT_ID")
OANDA_API_TOKEN = ENV_DATA.get("OANDA_PRACTICE_TOKEN")
OANDA_ENV = "practice"

LOG_DIR = os.path.join(BASE, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

AUDIT_LOG = os.path.join(LOG_DIR, "autonomous_decisions.jsonl")
STATUS_FILE = os.path.join(LOG_DIR, "autonomous_status.json")

# Dashboard integration files
NARRATION_LOG = os.path.join(BASE, "narration.jsonl")
CONNECTION_STATE_FILE = os.path.join(BASE, "connection_state.json")
OPEN_POSITIONS_FILE = os.path.join(BASE, "open_positions.json")

# Fail fast with clear message if creds missing
if not OANDA_ACCOUNT_ID or not OANDA_API_TOKEN:
    sys.stderr.write("[FATAL] Missing OANDA credentials. Expected OANDA_ACCOUNT_ID and OANDA_API_TOKEN.\n")
    sys.stderr.write("        Checked .env and env_new.env. Please set practice credentials or define OANDA_ENV/live creds.\n")
    sys.exit(2)

API_BASE = "https://api-fxpractice.oanda.com" if OANDA_ENV == "practice" else "https://api-fxtrade.oanda.com"
HEADERS = {
    "Authorization": f"Bearer {OANDA_API_TOKEN}",
    "Content-Type": "application/json"
}

# DECISION THRESHOLDS (tunable)
PROFIT_TAKE_THRESHOLD = float(os.getenv("PROFIT_TAKE_THRESHOLD", "150"))  # USD
LOSS_HALT_THRESHOLD = float(os.getenv("LOSS_HALT_THRESHOLD", "-300"))  # USD
BREAKEVEN_HOLD_TIME = float(os.getenv("BREAKEVEN_HOLD_TIME", "300"))  # seconds (5 min)
MAX_HOLD_TIME = 6 * 3600  # seconds (6 hours, from charter)
DAILY_LOSS_LIMIT = -0.05  # -5% (from charter)
MAX_MARGIN = 0.35  # 35% (from charter)
MIN_SL_PIPS = int(os.getenv("MIN_SL_PIPS", "10"))  # Reduced from 18 → 10 pips for tighter stops (avg loss $1.09 → $0.60)

# Hive consensus thresholds
CONSENSUS_ALLOW_THRESHOLD = 0.85
CONSENSUS_REDUCE_THRESHOLD = 0.75

# Position size scaling
SCALE_OUT_50_PCT = 0.5  # At profit, sell 50%
SCALE_OUT_25_PCT = 0.25  # At loss, reduce 25%

# MARKET HOURS (FX opens Sunday 5 PM ET, closes Friday 5 PM ET)
def is_forex_market_open() -> bool:
    """Check if forex markets are currently open (Mon-Fri 5 PM ET to Fri 5 PM ET UTC+0)"""
    now = datetime.now(timezone.utc)
    
    # Forex hours: Sunday 21:00 UTC to Friday 21:00 UTC (5 PM ET to 5 PM ET)
    weekday = now.weekday()  # 0=Monday, 6=Sunday
    hour = now.hour
    minute = now.minute
    
    # Sunday: opens at 21:00 UTC (hour >= 21)
    if weekday == 6:
        return hour >= 21
    
    # Monday-Thursday: open all day
    if weekday < 4:
        return True
    
    # Friday: open until 21:00 UTC (5 PM ET close)
    if weekday == 4:
        return hour < 21
    
    # Saturday: closed all day
    return False

# TRADING SIGNAL SETTINGS
TRADING_PAIRS = [
    "EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD", 
    "NZD_USD", "EUR_GBP", "EUR_JPY"
]
MAX_CONCURRENT_POSITIONS = 3
MIN_TRADE_INTERVAL_SECONDS = 300  # 5 minutes between new trades

# CHARTER COMPLIANCE (Immutable - $15k minimum notional enforced)
# Charter requires $15,000 minimum notional for all trades (paper and live)
# BOOTSTRAP MODE: Accounts under $15k use progressive scaling to reach Charter minimums
# - Under $5k: 20% NAV per trade (aggressive growth phase)
# - $5k-$10k: 25% NAV per trade (scaling phase)
# - $10k-$15k: 30% NAV per trade (pre-Charter phase)
# - $15k+: Full Charter compliance ($15k-$50k notional based on confidence)
MIN_NOTIONAL_USD = 15000  # Charter requirement (immutable at $15k+ NAV)
MAX_NOTIONAL_USD = 50000  # Charter requirement - max for high-confidence signals (90%+ win rate)
BOOTSTRAP_MODE = True  # Enable intelligent scaling for accounts under $15k
MIN_RR_RATIO = 3.2  # Charter requirement (3.2:1)
CHARTER_PIN = 841921

@dataclass
class Position:
    instrument: str
    trade_id: str
    side: str
    units: float
    entry_price: float
    current_price: float
    pnl_pips: float
    pnl_usd: float
    opened_at: datetime
    hold_time_seconds: float
    sl_price: Optional[float] = None
    tp_price: Optional[float] = None

@dataclass
class Decision:
    timestamp: str
    instrument: str
    trade_id: str
    decision: str  # HOLD, SELL, SCALE_OUT_50, SCALE_OUT_25, SET_SL, SET_TP, EXIT_EMERGENCY
    reason: str
    action_taken: bool
    result: str = ""

def narrate(message: str, event_type: str = "LOG"):
    """Write Rick's narration to dashboard"""
    try:
        entry = {
            "timestamp": datetime.now(timezone.utc).strftime('%H:%M:%S'),
            "narration": message,
            "event_type": event_type
        }
        with open(NARRATION_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Silent fail - don't break trading on narration errors

def log_decision(decision: Decision):
    """Append decision to audit log"""
    with open(AUDIT_LOG, "a") as f:
        f.write(json.dumps(asdict(decision)) + "\n")
    print(f"[DECISION] {decision.instrument:10} {decision.decision:20} → {decision.reason}")

def read_hive_consensus() -> float:
    """Read current hive consensus (0.0-1.0)"""
    try:
        path = os.path.join(BASE, "config", "hive_consensus.json")
        with open(path, "r") as f:
            return float(json.load(f).get("consensus", 0.95))
    except Exception:
        return float(os.getenv("UNIBOT_HIVE_CONSENSUS", "0.95"))

def get_oanda_trades() -> List[Dict]:
    """Fetch all open trades from OANDA"""
    try:
        r = requests.get(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/openTrades",
            headers=HEADERS,
            timeout=10
        )
        r.raise_for_status()
        return r.json().get("trades", [])
    except Exception as e:
        print(f"[ERR] Failed to fetch trades: {e}")
        return []

def get_pending_orders() -> List[Dict]:
    """Fetch all pending orders from OANDA (LIMIT/STOP/OCO legs not yet filled).
    Returns empty list on error. Plain-English errors only."""
    try:
        r = requests.get(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/pendingOrders",
            headers=HEADERS,
            timeout=10
        )
        r.raise_for_status()
        return r.json().get("orders", [])
    except Exception as e:
        print(f"[ERR] Failed to fetch pending orders: {e}")
        return []

def get_current_price(instrument: str) -> Tuple[float, float]:
    """Fetch bid/ask for instrument"""
    try:
        r = requests.get(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/pricing",
            headers=HEADERS,
            params={"instruments": instrument},
            timeout=10
        )
        r.raise_for_status()
        prices = r.json().get("prices", [])
        if prices:
            bid = float(prices[0]["bids"][0]["price"])
            ask = float(prices[0]["asks"][0]["price"])
            return bid, ask
    except Exception as e:
        print(f"[ERR] Failed to fetch price for {instrument}: {e}")
    return None, None

def pip_size(instrument: str) -> float:
    """Return pip size for instrument"""
    return 0.01 if instrument.endswith("JPY") else 0.0001

def parse_position(trade: Dict) -> Position:
    """Convert OANDA trade to Position object"""
    instrument = trade["instrument"]
    units = float(trade["currentUnits"])
    entry_price = float(trade["price"])
    
    # Get current price
    bid, ask = get_current_price(instrument)
    if bid is None:
        current_price = entry_price
    else:
        current_price = bid if units > 0 else ask
    
    # Calculate PnL
    ps = pip_size(instrument)
    pnl_pips = (current_price - entry_price) / ps * (1 if units > 0 else -1)
    pnl_usd = (current_price - entry_price) * abs(units)
    
    # Hold time
    opened_at = datetime.fromisoformat(trade["openTime"].replace("Z", "+00:00"))
    hold_time = (datetime.now(timezone.utc) - opened_at).total_seconds()
    
    # SL/TP
    sl = trade.get("stopLoss", {}).get("price")
    tp = trade.get("takeProfitOnFill", {}).get("price")
    
    return Position(
        instrument=instrument,
        trade_id=trade["id"],
        side="LONG" if units > 0 else "SHORT",
        units=abs(units),
        entry_price=entry_price,
        current_price=current_price,
        pnl_pips=pnl_pips,
        pnl_usd=pnl_usd,
        opened_at=opened_at,
        hold_time_seconds=hold_time,
        sl_price=float(sl) if sl else None,
        tp_price=float(tp) if tp else None
    )

def set_stop_loss(trade_id: str, instrument: str, price: float) -> bool:
    """Set stop loss on trade
    - Uses correct price precision (JPY pairs use 3 decimals, others 5)
    - Sets timeInForce to GTC for broker persistence
    - Treats already-exists responses as success
    """
    try:
        # OANDA price precision: JPY pairs typically 3 decimals, others 5
        decimals = 3 if instrument.endswith("JPY") else 5
        body = {
            "stopLoss": {
                "price": float(f"{price:.{decimals}f}"),
                "timeInForce": "GTC"
            }
        }
        r = requests.put(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/trades/{trade_id}/orders",
            headers=HEADERS,
            json=body,
            timeout=10
        )
        if r.status_code == 200:
            return True
        else:
            # Check if SL already exists (common error)
            txt = (r.text or "")
            if "STOP_LOSS_ORDER_ALREADY_EXISTS" in txt or "OrderAlreadyExists" in txt:
                return True  # Consider success if SL already set
            print(f"[WARN] SL update failed: {r.status_code} - {txt[:240]}")
            return False
    except Exception as e:
        print(f"[ERR] Failed to set SL on {instrument}: {e}")
        return False

def set_trailing_stop(trade_id: str, instrument: str, distance_pips: float) -> bool:
    """Set trailing stop on trade"""
    try:
        ps = pip_size(instrument)
        distance = distance_pips * ps
        body = {"trailingStopLoss": {"distance": f"{distance:.10f}"}}
        r = requests.put(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/trades/{trade_id}/orders",
            headers=HEADERS,
            json=body,
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        print(f"[ERR] Failed to set trailing SL on {instrument}: {e}")
        return False

def close_units(trade_id: str, instrument: str, units_to_close: float, side: str) -> bool:
    """Close partial position"""
    try:
        # OANDA sign convention: positive for long reduction, negative for short reduction
        close_units = -abs(units_to_close) if side == "LONG" else abs(units_to_close)
        body = {"units": str(int(close_units))}
        r = requests.put(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/trades/{trade_id}/close",
            headers=HEADERS,
            json=body,
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        print(f"[ERR] Failed to close {units_to_close} units on {instrument}: {e}")
        return False

def close_full(trade_id: str, instrument: str, side: str) -> bool:
    """Close entire position"""
    try:
        r = requests.put(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/trades/{trade_id}/close",
            headers=HEADERS,
            timeout=10
        )
        return r.status_code == 200
    except Exception as e:
        print(f"[ERR] Failed to close {instrument} fully: {e}")
        return False

def decide_action(position: Position, consensus: float, account_nav: float) -> Decision:
    """
    DECISION ENGINE - determines action for a position
    
    Returns: Decision object with action recommendation
    """
    
    now = datetime.now(timezone.utc).isoformat()
    
    # ========== EMERGENCY HALTS (HIGHEST PRIORITY) ==========
    
    # 1. SL already set and being hit? Exit (but this is broker-side, so just flag)
    if position.sl_price is not None:
        if position.side == "LONG" and position.current_price <= position.sl_price:
            return Decision(
                timestamp=now,
                instrument=position.instrument,
                trade_id=position.trade_id,
                decision="EXIT_EMERGENCY",
                reason=f"SL hit at {position.current_price:.5f}",
                action_taken=False  # Broker handles this
            )
        elif position.side == "SHORT" and position.current_price >= position.sl_price:
            return Decision(
                timestamp=now,
                instrument=position.instrument,
                trade_id=position.trade_id,
                decision="EXIT_EMERGENCY",
                reason=f"SL hit at {position.current_price:.5f}",
                action_taken=False
            )
    
    # 2. Hold time exceeded (6 hours)?
    if position.hold_time_seconds > MAX_HOLD_TIME:
        if is_forex_market_open():
            narrate(f"⏰ {position.instrument} held {position.hold_time_seconds/3600:.1f}h - Charter time limit - closing", "TIME_STOP")
            return Decision(
                timestamp=now,
                instrument=position.instrument,
                trade_id=position.trade_id,
                decision="EXIT_EMERGENCY",
                reason=f"Max hold time exceeded ({position.hold_time_seconds/3600:.1f}h > 6h)",
                action_taken=close_full(position.trade_id, position.instrument, position.side)
            )
        else:
            # Market closed - cannot exit, flag but don't attempt action
            return Decision(
                timestamp=now,
                instrument=position.instrument,
                trade_id=position.trade_id,
                decision="HOLD",
                reason=f"Max hold time exceeded ({position.hold_time_seconds/3600:.1f}h > 6h) - WAITING FOR MARKET OPEN",
                action_taken=False
            )
    
    # 3. Major loss (< -300 USD)?
    if position.pnl_usd < LOSS_HALT_THRESHOLD:
        narrate(f"🚨 Emergency exit on {position.instrument} - loss ${position.pnl_usd:.2f} hit threshold", "LOSS_HALT")
        return Decision(
            timestamp=now,
            instrument=position.instrument,
            trade_id=position.trade_id,
            decision="EXIT_EMERGENCY",
            reason=f"Loss exceeds halt threshold ({position.pnl_usd:.2f} < {LOSS_HALT_THRESHOLD})",
            action_taken=close_full(position.trade_id, position.instrument, position.side)
        )
    
    # ========== PROTECTIVE ACTIONS (SET SL IF MISSING) ==========
    
    # 4. No SL set? Set MIN_SL_PIPS below entry
    if position.sl_price is None:
        ps = pip_size(position.instrument)
        sl_price = position.entry_price - (MIN_SL_PIPS * ps if position.side == "LONG" else -MIN_SL_PIPS * ps)
        action = set_stop_loss(position.trade_id, position.instrument, sl_price)
        if action:  # Only log if we actually set it
            narrate(f"🛡️ Setting {MIN_SL_PIPS}-pip stop loss on {position.instrument} at {sl_price:.5f}", "PROTECTION")
            return Decision(
                timestamp=now,
                instrument=position.instrument,
                trade_id=position.trade_id,
                decision="SET_SL",
                reason=f"Setting protective SL at {sl_price:.5f} ({MIN_SL_PIPS} pips)",
                action_taken=action
            )
    
    # ========== PROFIT-TAKING (HIGHEST PROBABILITY ACTIONS) ==========
    
    # 5. Position in profit > PROFIT_TAKE_THRESHOLD? Scale out 50%
    if position.pnl_usd > PROFIT_TAKE_THRESHOLD:
        units_to_close = position.units * SCALE_OUT_50_PCT
        action = close_units(position.trade_id, position.instrument, units_to_close, position.side)
        narrate(f"💰 Taking profit on {position.instrument} - ${position.pnl_usd:.2f} - scaling out 50%", "PROFIT_TAKE")
        return Decision(
            timestamp=now,
            instrument=position.instrument,
            trade_id=position.trade_id,
            decision="SCALE_OUT_50",
            reason=f"Profit {position.pnl_usd:.2f} > {PROFIT_TAKE_THRESHOLD}; closing {units_to_close:.0f} units (50%)",
            action_taken=action
        )
    
    # ========== HIVE CONSENSUS CHECKS ==========
    
    # 6. Low consensus (<0.75)? Reduce position 25%
    if consensus < CONSENSUS_REDUCE_THRESHOLD:
        units_to_close = position.units * SCALE_OUT_25_PCT
        action = close_units(position.trade_id, position.instrument, units_to_close, position.side)
        return Decision(
            timestamp=now,
            instrument=position.instrument,
            trade_id=position.trade_id,
            decision="SCALE_OUT_25",
            reason=f"Hive consensus low ({consensus:.2f} < {CONSENSUS_REDUCE_THRESHOLD}); reducing 25%",
            action_taken=action
        )
    
    # ========== DEFAULT: HOLD ==========
    
    # 7. All clear; HOLD position and monitor
    reason = f"Breakeven; hold for move ({position.pnl_pips:.1f}p, {position.hold_time_seconds/60:.1f}m held)"
    if position.pnl_usd > 0:
        reason = f"Small profit {position.pnl_usd:.2f}; let runner run"
    elif position.pnl_usd < -100:
        reason = f"Small loss {position.pnl_usd:.2f}; SL active; awaiting recovery"
    
    return Decision(
        timestamp=now,
        instrument=position.instrument,
        trade_id=position.trade_id,
        decision="HOLD",
        reason=reason,
        action_taken=False
    )

def update_dashboard_state(positions: List[Position], account: Dict, connected: bool = True):
    """Update dashboard files with current trading state"""
    try:
        # Update connection state
        connection_state = {
            "connected": connected,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "account_nav": account.get("nav", 0),
            "account_balance": account.get("balance", 0),
            "margin_used": account.get("margin_used", 0),
            "open_trades": []
        }
        
        # Add position data
        for pos in positions:
            connection_state["open_trades"].append({
                "instrument": pos.instrument,
                "trade_id": pos.trade_id,
                "side": pos.side,
                "units": pos.units,
                "entry_price": pos.entry_price,
                "current_price": pos.current_price,
                "pnl": pos.pnl_usd,
                "pnl_pips": pos.pnl_pips,
                "sl_price": pos.sl_price,
                "tp_price": pos.tp_price,
                "hold_time_seconds": pos.hold_time_seconds
            })
        
        # Write connection state
        with open(CONNECTION_STATE_FILE, "w") as f:
            json.dump(connection_state, f, indent=2)
        
        # Write open positions (separate file for compatibility)
        with open(OPEN_POSITIONS_FILE, "w") as f:
            json.dump({"positions": connection_state["open_trades"]}, f, indent=2)
            
    except Exception as e:
        print(f"[WARN] Failed to update dashboard state: {e}")

def get_account_info() -> Dict:
    """Fetch account NAV and margin info"""
    try:
        r = requests.get(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/summary",
            headers=HEADERS,
            timeout=10
        )
        r.raise_for_status()
        acct = r.json().get("account", {})
        return {
            "nav": float(acct.get("NAV", 0)),
            "balance": float(acct.get("balance", 0)),
            "margin_used": float(acct.get("marginUsed", 0) or 0),
            "margin_available": float(acct.get("marginAvailable", 0) or 0),
        }
    except Exception as e:
        print(f"[ERR] Failed to fetch account: {e}")
        return {"nav": 0, "balance": 0, "margin_used": 0, "margin_available": 0}

def calculate_position_size(instrument: str, entry_price: float, nav: float, confidence: float = 0.75) -> int:
    """
    Calculate position size with intelligent Bootstrap Mode for accounts under $15k.
    
    BOOTSTRAP MODE (NAV < $15k):
    - Automatically scales position size as account grows
    - Uses percentage-of-NAV sizing to compound growth
    - Maintains Charter safety (35% margin cap, proper R:R)
    - Progressive tiers: 20% NAV → 25% NAV → 30% NAV as account grows
    
    CHARTER MODE (NAV >= $15k):
    - Full Charter compliance with confidence-based sizing
    - 70-75% confidence: $15k notional (minimum)
    - 75-85% confidence: $20k notional  
    - 85-90% confidence: $30k notional
    - 90%+ confidence: $50k notional (only if sustained 90%+ win rate)
    
    Args:
        instrument: Trading pair (e.g., "EUR_USD")
        entry_price: Entry price for the instrument
        nav: Net asset value (account balance)
        confidence: Signal confidence 0.0-1.0
    
    Returns:
        Position size in units
    """
    
    # BOOTSTRAP MODE: Intelligent scaling for accounts under $15k
    if BOOTSTRAP_MODE and nav < MIN_NOTIONAL_USD:
        # Progressive scaling tiers based on account size
        if nav < 5000:
            # Phase 1: Aggressive growth (20% NAV per trade)
            nav_percentage = 0.20
            tier_name = "Bootstrap-Aggressive"
        elif nav < 10000:
            # Phase 2: Scaling phase (25% NAV per trade)
            nav_percentage = 0.25
            tier_name = "Bootstrap-Scaling"
        else:
            # Phase 3: Pre-Charter (30% NAV per trade)
            nav_percentage = 0.30
            tier_name = "Bootstrap-PreCharter"
        
        # Confidence boost: higher confidence = larger position within tier
        confidence_multiplier = 0.8 + (confidence - 0.7) * 0.8  # 0.8x to 1.0x at 95% confidence
        target_notional = nav * nav_percentage * confidence_multiplier
        
        # Calculate units
        units_for_notional = int(target_notional / entry_price)
        
        # Ensure we don't exceed 35% margin (Charter safety rule)
        max_margin_units = int((nav * MAX_MARGIN) / entry_price)
        final_units = min(units_for_notional, max_margin_units)
        final_notional = final_units * entry_price
        
        logging.info(f"🚀 BOOTSTRAP MODE: {tier_name} | NAV ${nav:,.2f} → {nav_percentage:.0%} allocation")
        logging.info(f"   {instrument} @ {entry_price} | Confidence: {confidence:.1%} → Multiplier: {confidence_multiplier:.2f}x")
        logging.info(f"   Target: ${target_notional:,.2f} | Final: ${final_notional:,.2f} ({final_units:,} units)")
        
        return final_units
    
    # CHARTER MODE: Full compliance (NAV >= $15k)
    # Determine target notional based on signal confidence
    if confidence >= 0.90:
        target_notional = MAX_NOTIONAL_USD  # $50k for very high confidence
    elif confidence >= 0.85:
        target_notional = 30000  # $30k for high confidence
    elif confidence >= 0.75:
        target_notional = 20000  # $20k for medium confidence
    else:
        target_notional = MIN_NOTIONAL_USD  # $15k for low confidence (minimum)
    
    # Calculate units needed to meet target notional
    units_for_notional = int(target_notional / entry_price)
    
    # Ensure we don't exceed 35% margin (Charter rule)
    max_margin_units = int((nav * MAX_MARGIN) / entry_price)
    
    # Use the minimum of:
    # 1. Units needed for target notional
    # 2. Max units allowed by margin
    # Prioritize meeting target notional if possible within margin constraints
    final_units = min(units_for_notional, max_margin_units)
    final_notional = final_units * entry_price
    
    logging.info(f"📊 CHARTER MODE: {instrument} @ {entry_price} | Confidence: {confidence:.1%}")
    logging.info(f"   Target: ${target_notional:,} | Final: ${final_notional:,.2f} ({final_units:,} units)")
    
    return final_units

def generate_trading_signal() -> Optional[Dict]:
    """
    Generate trading signal
    Currently: Random walk (for demo/testing)
    TODO: Replace with real signal logic (ML, indicators, external signals)
    """
    # Simple random signal for now
    if random.random() < 0.3:  # 30% chance to generate signal
        return {
            "instrument": random.choice(TRADING_PAIRS),
            "direction": random.choice(["BUY", "SELL"]),
            "confidence": random.uniform(0.7, 0.95),
            "source": "random_walk"  # Change this when using real signals
        }
    return None

def open_position(signal: Dict, account: Dict, gate=None, existing_positions: List = None, pending_orders: List = None) -> Optional[str]:
    """
    Open a new Charter-compliant position with OCO orders
    Includes pre-trade gate validation
    Returns trade_id if successful, None otherwise
    """
    instrument = signal["instrument"]
    direction = signal["direction"]
    
    try:
        # Get current price
        bid, ask = get_current_price(instrument)
        if bid is None:
            print(f"[ERR] Could not get price for {instrument}")
            return None
        
        entry_price = ask if direction == "BUY" else bid
        
        # Calculate position size using signal confidence
        units = calculate_position_size(instrument, entry_price, account["nav"], signal.get("confidence", 0.75))
        
        # Sign convention: positive for BUY, negative for SELL
        signed_units = units if direction == "BUY" else -units
        
        # Calculate notional
        notional = abs(signed_units) * entry_price
        
        # Charter check: Min notional (allow bootstrap mode for accounts under $15k)
        if BOOTSTRAP_MODE and account["nav"] < MIN_NOTIONAL_USD:
            # Bootstrap mode: allow smaller positions to grow account
            min_notional_required = max(100, account["nav"] * 0.10)  # At least $100 or 10% NAV
            if notional < min_notional_required:
                print(f"[WARN] Bootstrap: Notional ${notional:,.0f} < ${min_notional_required:,.0f} (10% NAV minimum) - skipping")
                return None
        elif notional < MIN_NOTIONAL_USD:
            # Charter mode: enforce $15k minimum
            print(f"[WARN] Charter: Notional ${notional:,.0f} < ${MIN_NOTIONAL_USD:,} (Charter violation) - skipping")
            return None
        
        # ========== DUPLICATE-PROOFING (engine-level) ==========
        # 1) If there is already an open trade on this instrument, skip opening another
        if existing_positions:
            already_open = any(getattr(p, "instrument", None) == instrument for p in existing_positions)
            if already_open:
                print(f"  ℹ️  Duplicate prevention: {instrument} already has an open trade — skipping new entry")
                narrate(f"🛑 Skipping duplicate entry for {instrument} — existing position detected", "DUPLICATE_PROTECT")
                return None

        # 2) If there is a pending order on this instrument (any side), skip
        if pending_orders:
            has_pending = any((o.get("instrument") == instrument) for o in pending_orders)
            if has_pending:
                print(f"  ℹ️  Duplicate prevention: {instrument} has pending order — skipping new entry")
                narrate(f"🛑 Skipping duplicate entry for {instrument} — pending order exists", "DUPLICATE_PROTECT")
                return None

        # ========== PRE-TRADE GATE VALIDATION ==========
        if GATES_AVAILABLE and gate is not None and existing_positions is not None:
            # Create gate order object
            gate_order = GateOrder(
                symbol=instrument,
                side="BUY" if direction == "BUY" else "SELL",
                units=abs(signed_units),
                price=entry_price,
                order_id=f"signal_{instrument}_{int(time.time())}",
            )
            
            # Run pre-trade gate
            gate_result = gate.pre_trade_gate(
                new_order=gate_order,
                current_positions=existing_positions,
                pending_orders=pending_orders or [],
                total_margin_used=account["margin_used"],
            )
            
            if not gate_result.allowed:
                print(f"  ❌ GUARDIAN GATE BLOCKED: {gate_result.reason}")
                print(f"     Action: {gate_result.action}")
                
                narrate(f"🛡️ Guardian BLOCKED {instrument} {direction} - {gate_result.reason}", "GATE_REJECTION")
                
                # Log gate rejection
                with open(AUDIT_LOG, "a") as f:
                    f.write(json.dumps({
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "event": "GATE_REJECTION",
                        "instrument": instrument,
                        "direction": direction,
                        "units": abs(signed_units),
                        "notional_usd": notional,
                        "reason": gate_result.reason,
                        "action": gate_result.action,
                    }) + "\n")
                
                return None
            else:
                print(f"  ✅ Guardian gate PASSED")
                narrate(f"✅ Guardian approved {instrument} {direction} - ${notional:,.0f} notional", "GATE_APPROVED")
        
        # Calculate stop loss and take profit
        ps = pip_size(instrument)
        
        if direction == "BUY":
            sl_price = entry_price - (MIN_SL_PIPS * ps)
            tp_price = entry_price + (MIN_SL_PIPS * MIN_RR_RATIO * ps)  # 3.2:1 R:R
        else:
            sl_price = entry_price + (MIN_SL_PIPS * ps)
            tp_price = entry_price - (MIN_SL_PIPS * MIN_RR_RATIO * ps)
        
        # Verify R:R ratio
        risk = abs(entry_price - sl_price)
        reward = abs(tp_price - entry_price)
        actual_rr = reward / risk if risk > 0 else 0
        
        if actual_rr < (MIN_RR_RATIO - 0.1):  # Small tolerance
            print(f"[WARN] R:R {actual_rr:.2f} < {MIN_RR_RATIO} (Charter violation) - skipping")
            return None
        
        # Build order payload (respect instrument precision for SL/TP)
        decimals = 3 if instrument.endswith("JPY") else 5
        sl_str = f"{sl_price:.{decimals}f}"
        tp_str = f"{tp_price:.{decimals}f}"
        order_data = {
            "order": {
                "type": "MARKET",
                "instrument": instrument,
                "units": str(signed_units),
                "timeInForce": "FOK",  # Fill or Kill
                "positionFill": "DEFAULT",
                "stopLossOnFill": {
                    "price": sl_str,
                    "timeInForce": "GTC"
                },
                "takeProfitOnFill": {
                    "price": tp_str,
                    "timeInForce": "GTC"
                },
                # Client extensions for traceability (unique per order)
                "clientExtensions": {
                    "id": f"mk:{instrument}:{int(time.time())}",
                    "comment": "autonomous_v3"
                }
            }
        }
        
        # Place order
        r = requests.post(
            f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/orders",
            headers=HEADERS,
            json=order_data,
            timeout=10
        )
        
        if r.status_code == 201:
            response = r.json()
            trade_id = response.get("orderFillTransaction", {}).get("tradeOpened", {}).get("tradeID")
            
            # Rick's narration
            direction_icon = "📈" if direction == "BUY" else "📉"
            narrate(f"{direction_icon} OPENED {instrument} {direction} @ {entry_price:.5f} | SL: {sl_price:.5f} TP: {tp_price:.5f} | ${notional:,.0f} notional", "TRADE_OPENED")
            
            # Fancy formatted trade output
            print()
            print("  ▶ MARKET SCAN")
            print("  " + "─" * 78)
            print("  ✅ Real-time OANDA API data")
            spread_pips = (ask - bid) / pip_size(instrument)
            print(f"    📊 {instrument} BID: {bid:.5f} | ASK: {ask:.5f} | Spread: {spread_pips:.1f} pips")
            print(f"    • Position Size: {abs(signed_units):,} units (dynamic)")
            print(f"    • Notional Value: ${notional:,.0f} ✅")
            print(f"    • R:R Ratio: {actual_rr:.2f}:1 ✅")
            print()
            print(f"  ℹ️  Placing Charter-compliant {direction} OCO order for {instrument}...")
            print()
            
            print(f"   OPEN  {instrument} {direction} @ {entry_price:.5f} {direction_icon}")
            print(f"        Stop: {sl_price:.5f} | Target: {tp_price:.5f} | Size: {abs(signed_units):,} units | Notional: ${notional:,.0f}")
            print(f"    • 🛡️ Position tracked for autonomous management")
            print(f"    • 🆔 Trade ID: {trade_id}")
            print()
            
            # Log to audit
            with open(AUDIT_LOG, "a") as f:
                f.write(json.dumps({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "TRADE_OPENED",
                    "instrument": instrument,
                    "trade_id": trade_id,
                    "direction": direction,
                    "entry_price": entry_price,
                    "units": abs(signed_units),
                    "notional_usd": notional,
                    "sl_price": sl_price,
                    "tp_price": tp_price,
                    "rr_ratio": actual_rr,
                    "signal_source": signal.get("source", "unknown")
                }) + "\n")
            
            return trade_id
        else:
            print(f"  ❌ Order failed: {r.status_code}")
            print(f"     Error: {r.text[:200]}")
            return None
            
    except Exception as e:
        print(f"[ERR] Failed to open position: {e}")
        return None

def analyze_gate_rejections(limit: int = 20) -> Dict:
    """
    Analyze recent Guardian Gate rejections from audit log
    
    Returns summary of rejection reasons and frequencies
    """
    try:
        rejections = {"total": 0, "by_reason": {}, "recent": []}
        
        with open(AUDIT_LOG, "r") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    if record.get("event") == "GATE_REJECTION":
                        rejections["total"] += 1
                        reason = record.get("reason", "unknown")
                        rejections["by_reason"][reason] = rejections["by_reason"].get(reason, 0) + 1
                        rejections["recent"].append({
                            "timestamp": record.get("timestamp"),
                            "instrument": record.get("instrument"),
                            "direction": record.get("direction"),
                            "reason": reason,
                            "action": record.get("action")
                        })
                except json.JSONDecodeError:
                    continue
        
        # Keep only most recent
        rejections["recent"] = rejections["recent"][-limit:]
        
        return rejections
    except FileNotFoundError:
        return {"total": 0, "by_reason": {}, "recent": []}

def print_gate_rejection_summary():
    """Print a summary of Guardian Gate rejections if any"""
    try:
        rejection_stats = analyze_gate_rejections()
        
        if rejection_stats["total"] > 0:
            print()
            print("▶ GUARDIAN GATE REJECTION SUMMARY")
            print("─" * 80)
            print(f"  Total rejections: {rejection_stats['total']}")
            
            # Show top rejection reasons
            if rejection_stats["by_reason"]:
                print()
                print("  Top rejection reasons:")
                sorted_reasons = sorted(
                    rejection_stats["by_reason"].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )
                for reason, count in sorted_reasons[:5]:
                    pct = (count / rejection_stats["total"]) * 100
                    print(f"    • {reason}: {count} times ({pct:.1f}%)")
            
            # Show recent ones
            if rejection_stats["recent"]:
                print()
                print("  Recent rejections (last 5):")
                for rej in rejection_stats["recent"][-5:]:
                    print(f"    • {rej['instrument']} {rej['direction']:4} - {rej['reason']}")
            
            print()
    except Exception as e:
        pass  # Silently skip if there's any error

def main_loop():
    """
    UNIFIED AUTONOMOUS LOOP
    1. Monitors and manages existing positions (profit-taking, loss-cutting)
    2. Generates signals and opens new positions (if < MAX_CONCURRENT)
    Runs every CYCLE_SECONDS
    """
    
    CYCLE_SECONDS = int(os.getenv("AUTONOMOUS_CYCLE_SECONDS", "30"))
    
    # Fancy startup banner
    print("\n" + "="*80)
    print("            🤖 UNIFIED AUTONOMOUS TRADING ENGINE v3 (PRACTICE)            ")
    print(f"    Charter-Compliant OANDA | PIN: {CHARTER_PIN} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}")
    print("="*80)
    print()
    
    print("▶ CHARTER COMPLIANCE STATUS")
    print("─" * 80)
    print(f"  • PIN Validated: {CHARTER_PIN} ✅")
    print("  • Charter Version: RBOTzilla UNI Phase 9")
    print("  • Immutable OCO: ENFORCED (All orders)")
    print(f"  • Min R:R Ratio: {MIN_RR_RATIO}:1 (Charter Immutable)")
    
    # Bootstrap mode status
    if BOOTSTRAP_MODE:
        print(f"  • Bootstrap Mode: ACTIVE (intelligent scaling for NAV < $15k)")
        print(f"    → Phase 1 (<$5k): 20% NAV per trade (aggressive growth)")
        print(f"    → Phase 2 ($5k-$10k): 25% NAV per trade (scaling)")
        print(f"    → Phase 3 ($10k-$15k): 30% NAV per trade (pre-Charter)")
        print(f"    → Phase 4 ($15k+): Charter compliance ($15k-$50k notional)")
    else:
        print(f"  • Min Notional: ${MIN_NOTIONAL_USD:,} (Charter Immutable)")
    
    print(f"  • Max Daily Loss: {abs(DAILY_LOSS_LIMIT)*100:.1f}% (Charter Breaker)")
    print(f"  • Max Hold Time: {MAX_HOLD_TIME/3600:.0f}h (Charter Rule)")
    print()
    
    print("▶ AUTONOMOUS DECISION ENGINE")
    print("─" * 80)
    print(f"  • Cycle Interval: {CYCLE_SECONDS}s")
    print(f"  • Profit Take: ${PROFIT_TAKE_THRESHOLD} (Scale out 50%)")
    print(f"  • Loss Halt: ${LOSS_HALT_THRESHOLD} (Emergency exit)")
    print(f"  • Max Concurrent: {MAX_CONCURRENT_POSITIONS} positions")
    print(f"  • Trade Interval: {MIN_TRADE_INTERVAL_SECONDS}s between new trades")
    print()
    
    print("▶ TRADING CONFIGURATION")
    print("─" * 80)
    print(f"  • Trading Pairs: {len(TRADING_PAIRS)} pairs ({', '.join(TRADING_PAIRS[:3])}, ...)")
    print(f"  • Signal Source: Random Walk (30% probability)")
    print(f"  • Position Size: ${MIN_NOTIONAL_USD:,} - ${MAX_NOTIONAL_USD:,} notional (dynamic per confidence)")
    print(f"  • Stop Loss: {MIN_SL_PIPS} pips")
    print(f"  • Take Profit: {int(MIN_SL_PIPS * MIN_RR_RATIO)} pips ({MIN_RR_RATIO}:1 R:R)")
    print()
    
    print("▶ OANDA CONNECTION")
    print("─" * 80)
    print(f"  🟢 OANDA PRACTICE API   READY")
    print()
    
    if GATES_AVAILABLE:
        print("▶ GUARDIAN GATE SYSTEM")
        print("─" * 80)
        print(f"  🛡️  Margin Gate: ACTIVE (35% cap)")
        print(f"  🛡️  Correlation Gate: ACTIVE (currency buckets)")
        print(f"  🛡️  Pre-Trade Validation: ENABLED")
        print()
    
    print("✅ Unified Autonomous Trading Engine Ready - PRACTICE Environment")
    print("─" * 80)
    print()
    print("⚠️  Charter enforces $15k minimum notional - account needs sufficient capital")
    print()
    
    print("✅ Starting unified engine with PRACTICE API...")
    print()
    print("ℹ️  📊 Market Data: PRACTICE OANDA API (real-time)")
    print("ℹ️  💰 Orders: PRACTICE OANDA API")
    print("ℹ️  🧠 Position Management: Autonomous (30s cycles)")
    if GATES_AVAILABLE:
        print("ℹ️  🛡️  Guardian Gates: ACTIVE (margin + correlation)")
    print()
    print("─" * 80)
    
    # Initial narration
    narrate("🤖 Autonomous engine started - Charter PIN 841921 validated", "SYSTEM")
    narrate(f"⚙️ Configuration: {MAX_CONCURRENT_POSITIONS} max positions | ${MIN_NOTIONAL_USD:,} min notional | {MIN_RR_RATIO}:1 R:R", "SYSTEM")
    
    cycle_count = 0
    last_trade_time = 0
    gate = None  # Will initialize per cycle with fresh account state
    
    while True:
        cycle_count += 1
        now = datetime.now(timezone.utc).isoformat()
        
        print(f"\n▶ CYCLE {cycle_count} | {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("─" * 80)
        
        try:
            # 1. Get account state
            acct = get_account_info()
            consensus = read_hive_consensus()
            
            # Initialize guardian gate with current account state
            if GATES_AVAILABLE:
                gate = MarginCorrelationGate(account_nav=acct["nav"])
            
            print(f"  💰 Account: NAV ${acct['nav']:,.2f} | Balance ${acct['balance']:,.2f} | Margin ${acct['margin_used']:,.2f}")
            margin_pct = (acct['margin_used'] / acct['nav']) * 100 if acct['nav'] > 0 else 0
            margin_status = "✅" if margin_pct < 35 else "⚠️"
            print(f"  📊 Positions: {len(get_oanda_trades())}/{MAX_CONCURRENT_POSITIONS} open | Margin: {margin_status} {margin_pct:.1f}% | Hive: {consensus:.2%}")
            
            # 2. Get all open positions
            trades = get_oanda_trades()
            positions = [parse_position(t) for t in trades]

            # Also fetch any pending orders (for duplicate protection + gate visibility)
            pending = get_pending_orders()
            
            # Update dashboard with current state
            update_dashboard_state(positions, acct, connected=True)
            
            # Convert positions to gate format for validation
            gate_positions = []
            if GATES_AVAILABLE:
                for pos in positions:
                    gate_pos = GatePosition(
                        symbol=pos.instrument,
                        side=pos.side,
                        units=pos.units,
                        entry_price=pos.entry_price,
                        current_price=pos.current_price,
                        pnl=pos.pnl_usd,
                        pnl_pips=pos.pnl_pips,
                        margin_used=acct['margin_used'] / len(positions) if positions else 0,
                        position_id=pos.trade_id,
                    )
                    gate_positions.append(gate_pos)
            
            # 3. POSITION MANAGEMENT: Decide on each existing position
            if positions:
                print(f"\n  🎯 POSITION MANAGEMENT")
                print("  " + "─" * 78)
                decisions = []
                for pos in positions:
                    decision = decide_action(pos, consensus, acct["nav"])
                    decisions.append(decision)
                    
                    # Format decision output
                    status_icon = "✅" if decision.decision == "HOLD" else "⚠️" if decision.decision.startswith("SCALE") else "🔴"
                    print(f"  {status_icon} [{decision.decision:15}] {pos.instrument:8} | {decision.reason}")
                    
                    # Small delay between actions to avoid rate-limiting
                    if decision.action_taken:
                        log_decision(decision)
                        time.sleep(2)
                
                # Update status file
                status = {
                    "timestamp": now,
                    "cycle": cycle_count,
                    "positions_count": len(positions),
                    "consensus": consensus,
                    "account_nav": acct["nav"],
                    "margin_used": acct["margin_used"],
                    "decisions": [asdict(d) for d in decisions]
                }
                
                with open(STATUS_FILE, "w") as f:
                    json.dump(status, f, indent=2, default=str)
            else:
                print("  ℹ️  No open positions to manage")
            
            # 4. SIGNAL GENERATION: Try to open new position if we have capacity
            current_time = time.time()
            time_since_last_trade = current_time - last_trade_time
            
            # Only generate signals when markets are open
            if not is_forex_market_open():
                print(f"\n  🌙 MARKET CLOSED - Engine waiting for market open (Sunday 5 PM ET / Friday 5 PM ET)")
                print("  " + "─" * 78)
                print(f"  ℹ️  No new signals generated during market hours.")
                print(f"  ⏳ Existing positions will remain open until market reopens or Charter rules trigger closure.")
            elif len(positions) < MAX_CONCURRENT_POSITIONS:
                # Check if enough time has passed since last trade
                if time_since_last_trade >= MIN_TRADE_INTERVAL_SECONDS:
                    print(f"\n  🔍 SIGNAL SCAN | Capacity: {len(positions)}/{MAX_CONCURRENT_POSITIONS}")
                    print("  " + "─" * 78)
                    
                    # Generate signal
                    signal = generate_trading_signal()
                    
                    if signal:
                        print(f"  📡 Signal detected: {signal['instrument']} {signal['direction']} (confidence {signal['confidence']:.0%})")
                        print(f"  ℹ️  Evaluating Charter compliance...")
                        
                        narrate(f"📡 Signal: {signal['instrument']} {signal['direction']} ({signal['confidence']:.0%} confidence) - evaluating...", "SIGNAL")
                        
                        # Try to open position (with gate validation)
                        trade_id = open_position(signal, acct, gate, gate_positions, pending_orders=pending)
                        
                        if trade_id:
                            last_trade_time = current_time
                        else:
                            print(f"  ❌ Trade rejected (Charter/Gate violation or API error)")
                    else:
                        print(f"  ℹ️  No signal generated this cycle")
                else:
                    wait_remaining = MIN_TRADE_INTERVAL_SECONDS - time_since_last_trade
                    print(f"\n  ⏳ Trade cooldown: {wait_remaining:.0f}s remaining (min interval: {MIN_TRADE_INTERVAL_SECONDS}s)")
            else:
                print(f"\n  🛑 Max positions reached ({MAX_CONCURRENT_POSITIONS}) - no new trades until closure")
            
            # 5. Sleep and repeat
            print(f"\n  💤 Sleeping {CYCLE_SECONDS}s until next cycle...")
            print("─" * 80)
            time.sleep(CYCLE_SECONDS)
        
        except KeyboardInterrupt:
            print("\n[SHUTDOWN] Stopping autonomous engine...")
            narrate("🛑 Autonomous engine stopped by user", "SYSTEM")
            break
        except Exception as e:
            print(f"[ERR] Cycle {cycle_count} failed: {e}")
            narrate(f"⚠️ Cycle error: {str(e)[:100]}", "ERROR")
            import traceback
            traceback.print_exc()
            time.sleep(CYCLE_SECONDS)

def diagnose_run() -> int:
    """One-shot diagnostics: verify credentials and API endpoints.
    Returns process exit code (0 on success)."""
    print("\n🩺 Autonomous Engine Diagnostics\n" + "="*70)
    print(f"Env: {OANDA_ENV} | Account: {OANDA_ACCOUNT_ID}")

    ok = True

    # 1) Account summary
    try:
        url = f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/summary"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        acct = r.json().get("account", {})
        nav = float(acct.get("NAV", 0))
        bal = float(acct.get("balance", 0))
        print(f"✅ Account summary OK | Balance: ${bal:,.2f} | NAV: ${nav:,.2f}")
    except Exception as e:
        print(f"❌ Account summary failed: {e}")
        ok = False

    # 2) Open trades
    try:
        url = f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/openTrades"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        trades = r.json().get("trades", [])
        syms = sorted({t.get("instrument") for t in trades})
        print(f"✅ Open trades OK | Count: {len(trades)} | Instruments: {', '.join(syms) if syms else '(none)'}")
    except Exception as e:
        print(f"❌ Open trades failed: {e}")
        ok = False

    # 3) Pricing sample
    try:
        sample = "EUR_USD"
        url = f"{API_BASE}/v3/accounts/{OANDA_ACCOUNT_ID}/pricing"
        r = requests.get(url, headers=HEADERS, params={"instruments": sample}, timeout=10)
        r.raise_for_status()
        prices = r.json().get("prices", [])
        if prices:
            bid = float(prices[0]["bids"][0]["price"]) ; ask = float(prices[0]["asks"][0]["price"]) ; mid = (bid+ask)/2
            print(f"✅ Pricing OK | {sample} mid ~ {mid:.5f}")
        else:
            print("⚠️  Pricing returned no data")
    except Exception as e:
        print(f"❌ Pricing failed: {e}")
        ok = False

    print("="*70)
    print("DIAGNOSTICS:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Decision Engine")
    parser.add_argument("--diagnose", action="store_true", help="Run one-shot connectivity diagnostics and exit")
    args = parser.parse_args()

    if args.diagnose:
        sys.exit(diagnose_run())
    else:
        main_loop()
