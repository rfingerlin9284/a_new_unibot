#!/usr/bin/env python3
"""
Trade Shim with Bracket Auto-Generation (--tp-pips, --sl-pips, --trail-pips)
Charter-compliant auto-bracketing for OANDA orders
PIN: 841921 | Generated: 2025-10-20
"""

import os
import sys
import json
import argparse
from typing import Dict, Optional, Tuple
from math import copysign

# Load environment (optional - graceful fallback if dotenv not available)
try:
    from dotenv import load_dotenv
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        load_dotenv(os.path.expanduser("~/RICK/R_H_UNI/.env"))
        load_dotenv(os.path.expanduser("~/RICK/RICK_LIVE_PROTOTYPE/.env"))
        load_dotenv()
except ImportError:
    pass  # dotenv optional; env vars can be set manually

# HTTP/requests for OANDA API
try:
    import requests
except ImportError:
    requests = None

# Charter guardrails (immutable per addendum - PIN 841921)
MIN_SL_PIPS = float(os.getenv("MIN_SL_PIPS", "18"))      # immutable gate
MIN_RR = float(os.getenv("MIN_RR", "3.2"))              # immutable gate


def build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser with bracket controls."""
    p = argparse.ArgumentParser(
        description="Trade shim with auto-bracket generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Market buy with full bracket & trailing
  python trade_shim.py \\
    --instrument EUR_USD --units 12900 --type MARKET --entry 1.16550 \\
    --tp-pips 60 --sl-pips 24 --trail-pips 20 --dry-run

  # Limit sell with bracket (no trailing)
  python trade_shim.py \\
    --instrument GBP_USD --units -11200 --type LIMIT --price 1.34500 \\
    --tp-pips 66 --sl-pips 22

  # Market order without bracket (explicit)
  python trade_shim.py \\
    --instrument AUD_JPY --units 200 --type MARKET --no-bracket
        """
    )

    # Required arguments
    p.add_argument("--instrument", required=True, help="e.g., EUR_USD")
    p.add_argument("--units", type=int, required=True, help="positive=buy, negative=sell")
    p.add_argument("--type", choices=["MARKET", "LIMIT", "STOP"], default="MARKET",
                   help="Order type (default: MARKET)")

    # Conditional arguments
    p.add_argument("--price", type=float, help="Order price (required for LIMIT/STOP)")
    p.add_argument("--entry", type=float, 
                   help="Override entry price for bracket calc (MARKET only); if not set, fetches quote")

    # Bracket controls (auto-on if any specified, unless --no-bracket)
    p.add_argument("--tp-pips", type=float, default=None,
                   help="Take-profit distance in pips")
    p.add_argument("--sl-pips", type=float, default=None,
                   help="Stop-loss distance in pips (>= %.1f pips per charter)" % MIN_SL_PIPS)
    p.add_argument("--trail-pips", type=float, default=None,
                   help="Trailing stop distance in pips (broker-native)")
    p.add_argument("--no-bracket", action="store_true",
                   help="Send order without TP/SL/trailing (explicit override)")

    # Validation & debugging
    p.add_argument("--dry-run", action="store_true",
                   help="Print payload instead of sending")
    p.add_argument("--validate-only", action="store_true",
                   help="Validate arguments, print warnings, but don't send")
    
    # Environment selection
    p.add_argument("--environment", choices=["practice", "live"], default="practice",
                   help="OANDA environment (default: practice)")

    return p


def fetch_instrument_meta(instrument: str) -> Dict[str, int]:
    """
    Fetch instrument metadata (pip location, precision).
    In production, cache this from OANDA /v3/accounts/{id}/instruments endpoint.
    For now, use sensible defaults.
    """
    meta = {}
    if instrument.upper().endswith("_JPY"):
        meta["pipLocation"] = -2          # 0.01 per pip
        meta["displayPrecision"] = 3
    else:
        meta["pipLocation"] = -4          # 0.0001 per pip
        meta["displayPrecision"] = 5
    return meta


def pip_size(instrument: str) -> float:
    """Return the pip size (price increment) for an instrument."""
    meta = fetch_instrument_meta(instrument)
    return 10 ** meta["pipLocation"]


def fmt_price(instrument: str, price: float) -> str:
    """Format a price to the correct precision."""
    meta = fetch_instrument_meta(instrument)
    dp = meta.get("displayPrecision", 5)
    return f"{price:.{dp}f}"


def build_brackets(
    instrument: str,
    side: str,
    entry_price: float,
    tp_pips: Optional[float],
    sl_pips: Optional[float],
    trail_pips: Optional[float]
) -> Dict[str, Dict]:
    """
    Build OANDA 'OnFill' blocks from pip distances.

    Args:
        instrument: Trading pair
        side: "buy" or "sell"
        entry_price: Anchor price for bracket calculation
        tp_pips: Take-profit distance (in pips)
        sl_pips: Stop-loss distance (in pips)
        trail_pips: Trailing stop distance (in pips, broker-native)

    Returns:
        Dict with 'takeProfitOnFill', 'stopLossOnFill', 'trailingStopLossOnFill'
        (as appropriate)

    Raises:
        ValueError: If SL < MIN_SL_PIPS or R:R < MIN_RR
    """
    p = pip_size(instrument)
    sign = 1 if side.lower() == "buy" else -1
    out = {}

    # Validate SL if provided
    if sl_pips is not None and sl_pips < MIN_SL_PIPS:
        raise ValueError(
            f"❌ SL {sl_pips} pips violates MIN_SL_PIPS {MIN_SL_PIPS} "
            f"(Charter immutable gate - PIN 841921)"
        )

    # Build take-profit
    if tp_pips is not None and tp_pips > 0:
        tp_price = entry_price + sign * tp_pips * p
        out["takeProfitOnFill"] = {
            "price": fmt_price(instrument, tp_price)
        }

    # Build stop-loss
    if sl_pips is not None and sl_pips > 0:
        sl_price = entry_price - sign * sl_pips * p
        out["stopLossOnFill"] = {
            "price": fmt_price(instrument, sl_price)
        }

    # Build trailing stop (broker-native)
    if trail_pips is not None and trail_pips > 0:
        # OANDA expects trailing distance in price units, not pips
        trail_price = trail_pips * p
        out["trailingStopLossOnFill"] = {
            "distance": fmt_price(instrument, trail_price)
        }

    # Validate Risk:Reward if both TP and SL present
    if tp_pips is not None and sl_pips is not None and tp_pips > 0 and sl_pips > 0:
        rr = tp_pips / sl_pips
        if rr < MIN_RR - 1e-9:  # Allow for floating-point precision
            raise ValueError(
                f"❌ Risk/Reward ratio {rr:.2f}:1 < MIN_RR {MIN_RR}:1 "
                f"(Charter immutable gate - PIN 841921)"
            )

    return out


def place_order(args: argparse.Namespace) -> Dict:
    """
    Build OANDA order payload with optional brackets.

    Returns:
        Dict with order payload (ready to POST to OANDA /v3/accounts/{id}/orders)
    """
    instrument = args.instrument.replace("/", "_").upper()
    order_side = "buy" if args.units > 0 else "sell"

    # Validate type-specific requirements
    if args.type in ("LIMIT", "STOP"):
        if args.price is None:
            raise ValueError(f"--price is required for {args.type} orders")

    # Construct base order
    order = {
        "order": {
            "instrument": instrument,
            "units": str(args.units),
            "type": args.type,
            "timeInForce": "FOK" if args.type == "MARKET" else "GTC",
            "positionFill": "DEFAULT"
        }
    }

    # Add price for LIMIT/STOP
    if args.type in ("LIMIT", "STOP"):
        order["order"]["price"] = fmt_price(instrument, args.price)

    # Auto-bracket unless --no-bracket specified
    if not args.no_bracket and any(v is not None for v in (args.tp_pips, args.sl_pips, args.trail_pips)):
        # Determine entry price anchor
        if args.type == "MARKET":
            if args.entry is not None:
                entry = args.entry
            else:
                # In production, fetch from live quote stream
                raise ValueError(
                    "For MARKET orders with brackets, provide --entry (e.g., --entry 1.16550) "
                    "or wire get_quote() to your pricing client"
                )
        else:
            # LIMIT/STOP: anchor to order price
            entry = args.price

        # Build brackets
        onfill = build_brackets(
            instrument=instrument,
            side=order_side,
            entry_price=entry,
            tp_pips=args.tp_pips,
            sl_pips=args.sl_pips,
            trail_pips=args.trail_pips
        )
        order["order"].update(onfill)

    return order


def get_quote(instrument: str, environment: str = "practice") -> Optional[float]:
    """
    Fetch live quote for an instrument from OANDA.
    
    Args:
        instrument: Trading pair (e.g., EUR_USD)
        environment: 'practice' or 'live'
    
    Returns:
        Mid-price as float, or None if unavailable
    """
    if not requests:
        return None
    
    # Get OANDA credentials from environment
    if environment == "live":
        account_id = os.getenv("OANDA_LIVE_ACCOUNT_ID")
        token = os.getenv("OANDA_LIVE_TOKEN")
        base_url = os.getenv("OANDA_LIVE_BASE_URL", "https://api-fxtrade.oanda.com/v3")
    else:
        account_id = os.getenv("OANDA_PRACTICE_ACCOUNT_ID")
        token = os.getenv("OANDA_PRACTICE_TOKEN")
        base_url = os.getenv("OANDA_PRACTICE_BASE_URL", "https://api-fxpractice.oanda.com/v3")
    
    if not account_id or not token:
        return None
    
    try:
        url = f"{base_url}/accounts/{account_id}/pricing"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        params = {"instruments": instrument}
        
        resp = requests.get(url, headers=headers, params=params, timeout=5)
        resp.raise_for_status()
        
        data = resp.json()
        if "prices" in data and len(data["prices"]) > 0:
            price_obj = data["prices"][0]
            bid = float(price_obj.get("bids", [{}])[0].get("price", 0))
            ask = float(price_obj.get("asks", [{}])[0].get("price", 0))
            if bid > 0 and ask > 0:
                return (bid + ask) / 2
    except Exception:
        pass
    
    return None


def send_order_to_oanda(order_payload: Dict, environment: str = "practice") -> Optional[Dict]:
    """
    Send order payload to OANDA REST API.
    
    Args:
        order_payload: Dict with 'order' key containing OANDA order spec
        environment: 'practice' or 'live'
    
    Returns:
        Response JSON dict if successful, None on error
    """
    if not requests:
        print("❌ requests library not available", file=sys.stderr)
        return None
    
    # Get OANDA credentials
    if environment == "live":
        account_id = os.getenv("OANDA_LIVE_ACCOUNT_ID")
        token = os.getenv("OANDA_LIVE_TOKEN")
        base_url = os.getenv("OANDA_LIVE_BASE_URL", "https://api-fxtrade.oanda.com/v3")
    else:
        account_id = os.getenv("OANDA_PRACTICE_ACCOUNT_ID")
        token = os.getenv("OANDA_PRACTICE_TOKEN")
        base_url = os.getenv("OANDA_PRACTICE_BASE_URL", "https://api-fxpractice.oanda.com/v3")
    
    if not account_id or not token:
        print(
            f"❌ Missing OANDA credentials for {environment} environment",
            file=sys.stderr
        )
        return None
    
    try:
        url = f"{base_url}/accounts/{account_id}/orders"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        resp = requests.post(
            url,
            headers=headers,
            json=order_payload,
            timeout=10
        )
        resp.raise_for_status()
        
        result = resp.json()
        return result
    
    except requests.exceptions.HTTPError as e:
        print(f"❌ OANDA API error: {e.response.status_code} {e.response.text}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def main():
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        order = place_order(args)

        if args.dry_run or args.validate_only:
            print(json.dumps(order, indent=2))
            if args.validate_only:
                print("\n✅ Validation passed (--validate-only, no order sent)")
            return 0

        # Production: send to OANDA via HTTP
        print(f"📤 Sending {args.type} order to OANDA ({args.environment})...")
        result = send_order_to_oanda(order, environment=args.environment)
        
        if result:
            if "orderCreateTransaction" in result:
                txn = result["orderCreateTransaction"]
                order_id = txn.get("orderID")
                status = txn.get("type")
                print(f"✅ Order created: ID={order_id}, Status={status}")
                print(json.dumps(result, indent=2))
                return 0
            else:
                print("⚠️  Response received but no order transaction:")
                print(json.dumps(result, indent=2))
                return 0
        else:
            print("❌ Failed to send order to OANDA", file=sys.stderr)
            return 1

    except ValueError as e:
        print(f"❌ Validation error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
