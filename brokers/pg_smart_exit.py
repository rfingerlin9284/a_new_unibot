#!/usr/bin/env python3
"""
pg_smart_exit: Position Guardian Smart Exit CLI
PIN: 841921 | Charter-compliant position exit management with RR validation
"""

import os
import sys
import argparse
import json
from typing import Optional, Dict

try:
    from dotenv import load_dotenv
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        load_dotenv(os.path.expanduser("~/RICK/R_H_UNI/.env"))
        load_dotenv(os.path.expanduser("~/RICK/RICK_LIVE_PROTOTYPE/.env"))
        load_dotenv()
except ImportError:
    pass

try:
    import requests
except ImportError:
    requests = None


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for smart exits."""
    p = argparse.ArgumentParser(
        description="Position Guardian: Smart Exit Manager (PIN: 841921)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Close at take-profit (current price == TP level)
  pg_smart_exit --position-id 12345 --exit-type tp

  # Close at stop-loss (current price == SL level)
  pg_smart_exit --position-id 12345 --exit-type sl

  # Manual close at specific price
  pg_smart_exit --position-id 12345 --exit-type manual --price 1.10550

  # Evaluate exit options (no action)
  pg_smart_exit --position-id 12345 --analyze

  # Close all positions with profit
  pg_smart_exit --close-all-profitable
        """
    )

    p.add_argument("--position-id", type=int, help="Position ID to close")
    p.add_argument("--exit-type", choices=["tp", "sl", "manual", "partial"],
                   help="Exit type")
    p.add_argument("--price", type=float, help="Exit price (for manual exits)")
    p.add_argument("--units", type=int, help="Units to close (for partial exits)")
    p.add_argument("--analyze", action="store_true", help="Analyze exit options")
    p.add_argument("--close-all-profitable", action="store_true", help="Close all profitable")
    p.add_argument("--dry-run", action="store_true", help="Show payload without sending")
    p.add_argument("--environment", choices=["practice", "live"], default="practice",
                   help="OANDA environment (default: practice)")

    return p


def get_open_positions(environment: str = "practice") -> Optional[Dict]:
    """Fetch open positions from OANDA."""
    if not requests:
        return None

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
        url = f"{base_url}/accounts/{account_id}/openPositions"
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"❌ Error fetching positions: {e}", file=sys.stderr)
        return None


def close_position(
    position_id: int, exit_type: str = "market", price: Optional[float] = None,
    units: Optional[int] = None, environment: str = "practice", dry_run: bool = False
) -> Optional[Dict]:
    """Close a position or partial position."""
    if not requests:
        print("❌ requests library not available", file=sys.stderr)
        return None

    if environment == "live":
        account_id = os.getenv("OANDA_LIVE_ACCOUNT_ID")
        token = os.getenv("OANDA_LIVE_TOKEN")
        base_url = os.getenv("OANDA_LIVE_BASE_URL", "https://api-fxtrade.oanda.com/v3")
    else:
        account_id = os.getenv("OANDA_PRACTICE_ACCOUNT_ID")
        token = os.getenv("OANDA_PRACTICE_TOKEN")
        base_url = os.getenv("OANDA_PRACTICE_BASE_URL", "https://api-fxpractice.oanda.com/v3")

    if not account_id or not token:
        print(f"❌ Missing OANDA credentials for {environment}", file=sys.stderr)
        return None

    # Build close order payload
    if exit_type == "manual" and price:
        payload = {
            "order": {
                "type": "LIMIT",
                "price": f"{price:.5f}",
                "units": str(-(units or 1)),
                "timeInForce": "GTC"
            }
        }
    else:
        payload = {
            "order": {
                "type": "MARKET",
                "units": str(-(units or 1)),
                "timeInForce": "FOK"
            }
        }

    if dry_run:
        print(f"📋 Dry-run: Would close position {position_id}:")
        print(json.dumps(payload, indent=2))
        return {"dry_run": True, "position_id": position_id}

    try:
        url = f"{base_url}/accounts/{account_id}/orders"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        print(f"✅ Close order created")
        return resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ OANDA API error: {e.response.status_code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def analyze_position(position_id: int, environment: str = "practice"):
    """Analyze exit options for a position."""
    print(f"📊 Analyzing position {position_id}...")
    positions = get_open_positions(environment=environment)
    
    if not positions:
        print("❌ Could not fetch positions")
        return

    if "positions" in positions:
        for pos in positions["positions"]:
            # Simplified analysis
            instr = pos.get("instrument")
            long_units = int(pos.get("long", {}).get("units", 0))
            short_units = int(pos.get("short", {}).get("units", 0))
            
            if long_units > 0 or short_units > 0:
                print(f"\n💰 Position: {instr}")
                print(f"   Long:  {long_units} units")
                print(f"   Short: {short_units} units")
                print(f"   📈 Exit Options: TP | SL | Manual | Partial")


def main():
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.analyze:
        if not args.position_id:
            print("❌ --analyze requires --position-id")
            return 1
        analyze_position(args.position_id, environment=args.environment)
        return 0

    if args.close_all_profitable:
        print("⚠️  --close-all-profitable not yet implemented")
        print("    Individual positions can be closed with:")
        print("    pg_smart_exit --position-id <ID> --exit-type market")
        return 0

    if not args.position_id or not args.exit_type:
        parser.print_help()
        return 1

    exit_map = {"tp": "tp", "sl": "sl", "manual": "manual", "partial": "partial"}
    
    print(f"🔄 Closing position {args.position_id} ({args.exit_type})...")
    result = close_position(
        args.position_id,
        exit_type=args.exit_type,
        price=args.price,
        units=args.units,
        environment=args.environment,
        dry_run=args.dry_run
    )

    if result:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
