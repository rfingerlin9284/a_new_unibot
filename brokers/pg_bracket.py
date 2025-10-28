#!/usr/bin/env python3
"""
pg_bracket: Position Guardian Bracket Generator CLI
PIN: 841921 | Charter-compliant bracket generation and application
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

# Charter constants
MIN_SL_PIPS = float(os.getenv("MIN_SL_PIPS", "18"))
MIN_RR = float(os.getenv("MIN_RR", "3.2"))


def build_parser() -> argparse.ArgumentParser:
    """Build CLI parser for bracket management."""
    p = argparse.ArgumentParser(
        description="Position Guardian: Bracket Generator (PIN: 841921)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add bracket to open position
  pg_bracket --position-id 12345 --tp-pips 100 --sl-pips 20

  # Validate bracket ratios
  pg_bracket --validate --tp-pips 100 --sl-pips 20

  # Dry-run bracket application
  pg_bracket --position-id 12345 --tp-pips 80 --sl-pips 25 --dry-run

  # List bracket templates
  pg_bracket --list-templates
        """
    )

    p.add_argument("--position-id", type=int, help="Position ID to add bracket to")
    p.add_argument("--tp-pips", type=float, help="Take-profit distance in pips")
    p.add_argument("--sl-pips", type=float, help="Stop-loss distance in pips")
    p.add_argument("--validate", action="store_true", help="Validate bracket ratio only")
    p.add_argument("--list-templates", action="store_true", help="Show bracket templates")
    p.add_argument("--dry-run", action="store_true", help="Show payload without sending")
    p.add_argument("--environment", choices=["practice", "live"], default="practice",
                   help="OANDA environment (default: practice)")

    return p


def validate_bracket(tp_pips: float, sl_pips: float) -> bool:
    """Validate bracket against charter guardrails."""
    if sl_pips < MIN_SL_PIPS:
        print(
            f"❌ SL {sl_pips} pips < MIN_SL_PIPS {MIN_SL_PIPS} "
            f"(Charter gate - PIN 841921)",
            file=sys.stderr
        )
        return False

    rr = tp_pips / sl_pips
    if rr < MIN_RR - 1e-9:
        print(
            f"❌ Risk/Reward {rr:.2f}:1 < MIN_RR {MIN_RR}:1 "
            f"(Charter gate - PIN 841921)",
            file=sys.stderr
        )
        return False

    print(f"✅ Bracket valid: RR = {rr:.2f}:1, SL = {sl_pips} pips")
    return True


def apply_bracket_to_position(
    position_id: int, tp_pips: float, sl_pips: float,
    environment: str = "practice", dry_run: bool = False
) -> Optional[Dict]:
    """Apply bracket to an open position."""
    if not requests:
        print("❌ requests library not available", file=sys.stderr)
        return None

    # Validate first
    if not validate_bracket(tp_pips, sl_pips):
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

    # Build bracket payload (typical OANDA format)
    payload = {
        "takeProfitOnFill": {"price": f"TBD"},  # Requires current position price
        "stopLossOnFill": {"price": f"TBD"}
    }

    if dry_run:
        print(f"📋 Dry-run: Would apply bracket to position {position_id}:")
        print(json.dumps(payload, indent=2))
        return {"dry_run": True, "position_id": position_id}

    try:
        url = f"{base_url}/accounts/{account_id}/positions/{position_id}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        resp = requests.put(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        print("✅ Bracket applied to position")
        return resp.json()
    except requests.exceptions.HTTPError as e:
        print(f"❌ OANDA API error: {e.response.status_code}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return None


def show_templates():
    """Display bracket templates."""
    templates = {
        "Conservative": {"tp_pips": 80, "sl_pips": 20, "rr": 4.0},
        "Balanced": {"tp_pips": 100, "sl_pips": 25, "rr": 4.0},
        "Aggressive": {"tp_pips": 120, "sl_pips": 24, "rr": 5.0},
        "Minimal": {"tp_pips": 64, "sl_pips": 20, "rr": 3.2},  # Minimum legal RR
    }

    print("\n📋 BRACKET TEMPLATES (Charter: MIN_SL=18, MIN_RR=3.2:1)")
    print("─" * 60)
    for name, spec in templates.items():
        print(f"{name:15} | TP={spec['tp_pips']:3d} pips | "
              f"SL={spec['sl_pips']:2d} pips | RR={spec['rr']:.1f}:1")


def main():
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.list_templates:
        show_templates()
        return 0

    if args.validate:
        if not args.tp_pips or not args.sl_pips:
            print("❌ --validate requires --tp-pips and --sl-pips")
            return 1
        if validate_bracket(args.tp_pips, args.sl_pips):
            return 0
        else:
            return 1

    if not args.position_id or not args.tp_pips or not args.sl_pips:
        parser.print_help()
        return 1

    print(f"📊 Applying bracket to position {args.position_id}...")
    result = apply_bracket_to_position(
        args.position_id,
        args.tp_pips,
        args.sl_pips,
        environment=args.environment,
        dry_run=args.dry_run
    )

    if result:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
