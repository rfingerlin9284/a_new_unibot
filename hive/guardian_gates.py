"""
Guardian Gates - Risk control gate system (Phase 7)
PIN: 841921 | Profile: Non-HFT (M15-H1)
Emits TRADE_BLOCKED events when gates reject trades
"""

from typing import Dict, Any, Optional
import logging

# Import hardened narration
try:
    from util.narration_logger import log_event, start_listener
except ImportError:
    def log_event(*args, **kwargs):
        pass
    def start_listener(*args, **kwargs):
        pass

logger = logging.getLogger(__name__)

# Start narration
start_listener(sample_one_in_n=0, max_bytes=25*1024*1024, backup_count=7, daily_rotation=True)


def _positions_gate(ctx) -> bool:
    """
    Gate: Maximum concurrent positions limit
    
    Args:
        ctx: Context object with open_positions and max_positions attributes
        
    Returns:
        bool: True if gate passes, False if blocked
    """
    ok = len(ctx.open_positions) < ctx.max_positions
    if not ok:
        log_event(
            "TRADE_BLOCKED",
            gate="positions",
            open=len(ctx.open_positions),
            max=ctx.max_positions,
            reason="Max concurrent positions reached"
        )
    return ok


def _margin_gate(ctx) -> bool:
    """
    Gate: Maximum margin usage limit
    
    Args:
        ctx: Context object with margin_used_pct and max_margin_pct
        
    Returns:
        bool: True if gate passes, False if blocked
    """
    ok = (ctx.margin_used_pct <= ctx.max_margin_pct)
    if not ok:
        log_event(
            "TRADE_BLOCKED",
            gate="margin",
            used_pct=round(ctx.margin_used_pct, 2),
            max_pct=ctx.max_margin_pct,
            reason="Margin limit exceeded"
        )
    return ok


def _correlation_gate(ctx) -> bool:
    """
    Gate: Maximum correlation/USD beta limit
    
    Args:
        ctx: Context object with usd_beta_corr and max_corr
        
    Returns:
        bool: True if gate passes, False if blocked
    """
    ok = (ctx.usd_beta_corr <= ctx.max_corr)
    if not ok:
        log_event(
            "TRADE_BLOCKED",
            gate="correlation",
            usd_beta_corr=round(ctx.usd_beta_corr, 3),
            max_corr=ctx.max_corr,
            reason="Correlation risk threshold exceeded"
        )
    return ok


def _crypto_gate(ctx) -> bool:
    """
    Gate: Hive consensus requirement for crypto positions
    
    Args:
        ctx: Context object with hive_consensus and hive_consensus_min
        
    Returns:
        bool: True if gate passes, False if blocked
    """
    ok = (ctx.hive_consensus >= ctx.hive_consensus_min)
    if not ok:
        log_event(
            "TRADE_BLOCKED",
            gate="crypto_hive_consensus",
            consensus=round(ctx.hive_consensus, 2),
            min_required=ctx.hive_consensus_min,
            reason="Insufficient hive consensus for crypto entry"
        )
    return ok


class GuardianGates:
    """
    Composite gate system - All gates must pass for trade execution
    """
    
    def __init__(self):
        """Initialize guardian gates"""
        self.gates = {
            "positions": _positions_gate,
            "margin": _margin_gate,
            "correlation": _correlation_gate,
            "crypto": _crypto_gate,
        }
        self.logger = logger
    
    def can_trade(self, ctx) -> bool:
        """
        Check if all gates allow trading.
        
        Args:
            ctx: Context object with all gate requirements
            
        Returns:
            bool: True if ALL gates pass
        """
        for gate_name, gate_fn in self.gates.items():
            if not gate_fn(ctx):
                return False
        return True
    
    def evaluate_gates(self, ctx) -> Dict[str, bool]:
        """
        Evaluate each gate individually and return results.
        
        Args:
            ctx: Context object
            
        Returns:
            dict: {gate_name: pass/fail}
        """
        results = {}
        for gate_name, gate_fn in self.gates.items():
            results[gate_name] = gate_fn(ctx)
        return results
