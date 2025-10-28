#!/usr/bin/env python3
"""
Manager Integration — Wires Position Guardian into your trading pipeline.
All orders route through pg_trade, which enforces correlation/margin gates + Autopilot.
"""
import sys
import json
import logging
from datetime import datetime, timezone
from pathlib import Path

# Add Position Guardian to path
sys.path.insert(0, str(Path.home() / "RICK" / "R_H_UNI" / "plugins"))

from position_guardian import (
    Position, Order, AccountState, pre_trade_hook, tick_enforce, tl_dr_actions
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(Path.home() / "RICK" / "R_H_UNI" / "logs" / "position_guardian.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("position_guardian_mgr")


class PositionGuardianManager:
    """
    Manager that enforces Position Guardian rules on all trades.
    """
    def __init__(self):
        self.positions: dict[str, Position] = {}
        self.account: AccountState = None
        self.state_file = Path.home() / "RICK" / "R_H_UNI" / "logs" / "guardian_metrics.json"
        self.metrics = self._load_metrics()

    def _load_metrics(self) -> dict:
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {
                "total_orders_checked": 0,
                "blocked_by_correlation": 0,
                "blocked_by_margin": 0,
                "auto_breakeven_applied": 0,
                "trailing_ratchets_applied": 0,
                "peak_giveback_exits": 0,
                "time_based_exits": 0,
                "profitable_exits_count": 0,
                "cumulative_profit_pips": 0.0
            }

    def _save_metrics(self):
        try:
            with open(self.state_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

    def set_account(self, nav: float, margin_used: float):
        """Update account state."""
        self.account = AccountState(
            nav=nav,
            margin_used=margin_used,
            now_utc=datetime.now(timezone.utc)
        )

    def add_position(self, pos: Position):
        """Register a new position."""
        self.positions[pos.id] = pos

    def remove_position(self, pos_id: str):
        """Remove a closed position."""
        if pos_id in self.positions:
            del self.positions[pos_id]
            logger.info(f"Position {pos_id} closed")

    def pg_trade(self, symbol: str, side: str, units: float) -> tuple[bool, str]:
        """
        Main entry point: Pre-flight check on all orders.
        Returns (allowed, reason)
        """
        if not self.account:
            return False, "Account state not initialized"

        order = Order(symbol=symbol, side=side, units=units)
        positions_list = list(self.positions.values())

        # Check hooks
        result = pre_trade_hook(order, positions_list, self.account)

        self.metrics["total_orders_checked"] += 1

        if not result.allowed:
            reason = result.reason or "Unknown gate failure"
            if "correlation" in reason.lower():
                self.metrics["blocked_by_correlation"] += 1
            elif "margin" in reason.lower():
                self.metrics["blocked_by_margin"] += 1
            logger.warning(f"Order BLOCKED: {symbol} {side} {units} | {reason}")
            self._save_metrics()
            return False, reason

        logger.info(f"Order ALLOWED: {symbol} {side} {units}")
        return True, "Order passed all gates"

    def tick_enforce_positions(self):
        """
        Called periodically (every tick/minute) to apply autopilot rules.
        """
        if not self.account:
            return []

        positions_list = list(self.positions.values())
        actions = tl_dr_actions(positions_list, self.account, datetime.now(timezone.utc))

        if not actions:
            return []

        executed_actions = []
        for action in actions:
            action_type = action.get("type", "")
            why = action.get("why", "")
            pos_id = action.get("position_id", "")

            # Count metric
            if action_type == "modify_sl":
                if "auto_breakeven" in why:
                    self.metrics["auto_breakeven_applied"] += 1
                elif "trail" in why:
                    self.metrics["trailing_ratchets_applied"] += 1
            elif action_type == "close":
                if "giveback" in why:
                    self.metrics["peak_giveback_exits"] += 1
                elif "time_stop" in why:
                    self.metrics["time_based_exits"] += 1
                self.metrics["profitable_exits_count"] += 1

            logger.info(f"Action: {action_type:15} | {why:30} | Pos: {pos_id}")
            executed_actions.append(action)

        self._save_metrics()
        return executed_actions

    def report(self) -> dict:
        """Generate performance report."""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "active_positions": len(self.positions),
            "account_nav": self.account.nav if self.account else None,
            "margin_utilization": self.account.margin_utilization * 100 if self.account else None,
            "metrics": self.metrics
        }


# Example usage
if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("Position Guardian Manager — Integration Demo")
    logger.info("=" * 80)

    mgr = PositionGuardianManager()
    mgr.set_account(nav=1952.22, margin_used=966.0)

    # Add test positions (same as demo)
    gbpusd = Position(
        id="GBPUSD_1",
        symbol="GBPUSD",
        side="long",
        units=11200,
        entry_price=1.34038,
        current_price=1.34340,
        stop_loss=None,
        opened_at=datetime.now(timezone.utc),
        initial_sl=1.33839
    )
    mgr.add_position(gbpusd)

    # Test gate: try to add correlated long
    logger.info("\n🚧 Test 1: Try to add correlated long (EURUSD)")
    allowed, reason = mgr.pg_trade(symbol="EURUSD", side="buy", units=10000)
    logger.info(f"   Result: {allowed} | {reason}")

    # Test gate: hedge is allowed
    logger.info("\n🚧 Test 2: Try to hedge (USDJPY)")
    allowed, reason = mgr.pg_trade(symbol="USDJPY", side="buy", units=8000)
    logger.info(f"   Result: {allowed} | {reason}")

    # Test autopilot tick
    logger.info("\n🤖 Test 3: Tick enforce (apply autopilot)")
    actions = mgr.tick_enforce_positions()
    logger.info(f"   Actions: {len(actions)}")

    # Report
    logger.info("\n📊 Metrics Report:")
    report = mgr.report()
    for k, v in report["metrics"].items():
        logger.info(f"   {k}: {v}")

    logger.info("=" * 80)
