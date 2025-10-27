#!/usr/bin/env python3
"""
pg_trail: Position Guardian Trailing Stop CLI
PIN: 841921 | Charter-compliant trailing stop management
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
    """Build CLI parser for trailing stop management."""
    p = argparse.ArgumentParser(
        description="Position Guardian: Trailing Stop Manager (PIN: 841921)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Set trailing stop on open position
  pg_trail --position-id 12345 --trail-pips 25 --dry-run

  # Modify existing trailing stop
  pg_trail --position-id 12345 --trail-pips 50

  # List all open positions with trailing stops
  pg_trail --list

  # Live environment
  pg_trail --position-id 12345 --trail-pips 20 --environment live
        """
    )

    p.add_argument("--position-id", type=int, help="Position ID to modify")
    p.add_argument("--trail-pips", type=float, help="Trailing stop distance in pips")
    p.add_argument("--list", action="store_true", help="List all open positions")
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


def modify_trailing_stop(
    position_id: int, trail_pips: float, environment: str = "practice", dry_run: bool = False
) -> Optional[Dict]:
    """Modify trailing stop for an open position."""
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

    # Build trailing stop payload
    payload = {
        "trailingStopDistance": f"{trail_pips * 0.0001:.4f}"  # Convert pips to price units (majors)
    }

    if dry_run:
        print(f"📋 Dry-run: Would modify position {position_id} with:")
        print(json.dumps(payload, indent=2))
        return {"dry_run": True, "position_id": position_id}

    try:
        url = f"{base_url}/accounts/{account_id}/positions/{position_id}/clientExtensions"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp = requests.put(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ OANDA API error: {e.response.status_code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def main():
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        print(f"📍 Fetching open positions ({args.environment})...")
        positions = get_open_positions(environment=args.environment)
        if positions:
            if "positions" in positions:
                for pos in positions["positions"]:
                    instr = pos.get("instrument")
                    long = pos.get("long", {})
                    short = pos.get("short", {})
                    long_units = int(long.get("units", 0))
                    short_units = int(short.get("units", 0))
                    
                    if long_units > 0:
                        print(f"  {instr}: +{long_units} units (long)")
                    if short_units > 0:
                        print(f"  {instr}: {short_units} units (short)")
            else:
                print("No open positions")
        return 0

    if not args.position_id or not args.trail_pips:
        parser.print_help()
        return 1

    print(f"🔄 Modifying position {args.position_id} (trail={args.trail_pips} pips)...")
    result = modify_trailing_stop(
        args.position_id,
        args.trail_pips,
        environment=args.environment,
        dry_run=args.dry_run
    )

    if result:
        if args.dry_run:
            print("✅ Dry-run complete")
        else:
            print("✅ Trailing stop updated")
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
