#!/usr/bin/env python3
"""
RBOTzilla UNI - Micro Trading Engine
⛔ DISABLED - Minimum 5-minute trade interval enforced
PIN: 841921 | Micro Canary Deployment (INACTIVE)
"""

import asyncio
import json
import time
import logging
import sys
import os
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
import signal
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/micro_canary/micro_engine.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# ⛔ MICRO TRADING DISABLED - Enforcing minimum 5-minute intervals
MICRO_TRADING_DISABLED = True
MINIMUM_TRADE_INTERVAL_SECONDS = 300  # 5 minutes

class AssetClass(Enum):
    """Asset class enumeration"""
    FX = "fx"
    CRYPTO = "crypto"

class TradeResult(Enum):
    """Trade result enumeration"""
    WIN = "win"
    LOSS = "loss"
    PENDING = "pending"

@dataclass
class TradeSignal:
    """Trade signal data structure"""
    signal_id: str
    asset_class: AssetClass
    symbol: str
    strategy: str
    direction: str  # 'long' or 'short'
    entry_price: float
    stop_loss: float
    take_profit: float
    position_size: float
    confidence: float
    timestamp: datetime

@dataclass
class ExecutedTrade:
    """Executed trade data structure"""
    trade_id: str
    signal: TradeSignal
    execution_timestamp: datetime
    actual_entry_price: float
    actual_exit_price: Optional[float]
    result: TradeResult
    pnl: float
    duration_seconds: int
    slippage: float

class MicroTradingEngine:
    """
    Micro trading engine for canary deployment
    Handles real-time trade execution across FX and crypto markets
    """
    
    def __init__(self, config_path: str):
        """Initialize micro trading engine"""
        # ⛔ GUARD: Micro trading is DISABLED
        if MICRO_TRADING_DISABLED:
            logger.error("❌ MICRO TRADING ENGINE DISABLED - Minimum 5-minute trade interval enforced")
            logger.error("   Cannot initialize micro trading. Use oanda_trading_engine.py instead.")
            logger.error("   All trades will respect 5-minute minimum interval (300 seconds)")
            raise RuntimeError("Micro Trading Engine is disabled. Minimum 5-minute intervals enforced.")
        
        self.config = self._load_config(config_path)
        self.trades_executed = 0
        self.fx_trades = 0
        self.crypto_trades = 0
        self.wins = 0
        self.losses = 0
        self.total_pnl = 0.0
        self.consecutive_losses = 0
        self.latency_failures = 0
        self.active = False
        self.trade_queue = queue.Queue()
        self.results_queue = queue.Queue()
        self.trade_history: List[ExecutedTrade] = []
        self.start_time = datetime.now(timezone.utc)
        
        # Strategy configurations
        self.fx_strategies = ["trend_following", "mean_reversion", "momentum"]
        self.crypto_strategies = ["defi_arbitrage", "volatility_harvest", "cross_exchange"]
        
        # Asset pairs
        self.fx_pairs = ["EUR_USD", "GBP_USD", "USD_JPY", "AUD_USD", "USD_CAD"]
        self.crypto_pairs = ["BTC-USD", "ETH-USD", "ADA-USD", "DOT-USD", "LINK-USD"]
        
        # Risk parameters
        self.max_consecutive_losses = self.config.get("risk_parameters", {}).get("max_consecutive_losses", 3)
        self.max_latency_failures = self.config.get("risk_parameters", {}).get("max_latency_failures", 3)
        self.position_size_usd = self.config.get("risk_parameters", {}).get("position_size_usd", 10.0)
        
        logger.info(f"Micro trading engine initialized for {self.config['total_trades']} trades")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Return default configuration"""
        return {
            "canary_id": f"micro_{int(time.time())}",
            "total_trades": 100,
            "fx_trades_target": 50,
            "crypto_trades_target": 50,
            "target_win_rate": 65.0,
            "target_sharpe": 1.2,
            "risk_parameters": {
                "max_consecutive_losses": 3,
                "max_latency_failures": 3,
                "max_cpu_load": 80.0,
                "max_risk_per_trade": 0.01,
                "position_size_usd": 10.0
            }
        }
    
    def generate_signal(self, asset_class: AssetClass, trade_id: int) -> TradeSignal:
        """Generate trading signal for given asset class"""
        if asset_class == AssetClass.FX:
            symbol = self.fx_pairs[trade_id % len(self.fx_pairs)]
            strategy = self.fx_strategies[trade_id % len(self.fx_strategies)]
            base_price = 1.0000 + (trade_id * 0.0001)  # Simulated FX price
        else:
            symbol = self.crypto_pairs[trade_id % len(self.crypto_pairs)]
            strategy = self.crypto_strategies[trade_id % len(self.crypto_strategies)]
            base_price = 30000.0 + (trade_id * 100.0)  # Simulated crypto price
        
        # Generate signal parameters
        direction = "long" if trade_id % 2 == 0 else "short"
        entry_price = base_price * (1 + (hash(str(trade_id)) % 100 - 50) / 10000.0)
        
        # Calculate stop loss and take profit
        risk_ratio = 0.02  # 2% risk per trade
        reward_ratio = 0.03  # 3% reward per trade
        
        if direction == "long":
            stop_loss = entry_price * (1 - risk_ratio)
            take_profit = entry_price * (1 + reward_ratio)
        else:
            stop_loss = entry_price * (1 + risk_ratio)
            take_profit = entry_price * (1 - reward_ratio)
        
        return TradeSignal(
            signal_id=f"{asset_class.value}_{trade_id}",
            asset_class=asset_class,
            symbol=symbol,
            strategy=strategy,
            direction=direction,
            entry_price=entry_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            position_size=self.position_size_usd,
            confidence=0.7 + (hash(str(trade_id)) % 30) / 100.0,  # 70-100% confidence
            timestamp=datetime.now(timezone.utc)
        )
    
    def simulate_execution(self, signal: TradeSignal) -> ExecutedTrade:
        """Simulate trade execution with realistic outcomes"""
        trade_id = f"{signal.asset_class.value}_{self.trades_executed + 1}"
        execution_time = datetime.now(timezone.utc)
        
        # Simulate execution latency
        execution_delay = 0.1 + (hash(trade_id) % 100) / 1000.0  # 0.1-0.2 seconds
        time.sleep(execution_delay)
        
        # Simulate slippage
        slippage = (hash(trade_id) % 20 - 10) / 10000.0  # -0.1% to +0.1%
        actual_entry_price = signal.entry_price * (1 + slippage)
        
        # Simulate trade duration (1-30 seconds for micro trades)
        duration = 1 + (hash(trade_id) % 30)
        time.sleep(min(duration / 10.0, 3.0))  # Accelerated for simulation
        
        # Determine trade outcome based on strategy and market conditions
        win_probability = self._calculate_win_probability(signal)
        outcome_random = hash(trade_id) % 100
        
        if outcome_random < win_probability:
            # Winning trade - hits take profit
            actual_exit_price = signal.take_profit
            result = TradeResult.WIN
            
            # Calculate PnL
            if signal.direction == "long":
                pnl = (actual_exit_price - actual_entry_price) * signal.position_size / actual_entry_price
            else:
                pnl = (actual_entry_price - actual_exit_price) * signal.position_size / actual_entry_price
                
            self.wins += 1
            self.consecutive_losses = 0
        else:
            # Losing trade - hits stop loss
            actual_exit_price = signal.stop_loss
            result = TradeResult.LOSS
            
            # Calculate PnL
            if signal.direction == "long":
                pnl = (actual_exit_price - actual_entry_price) * signal.position_size / actual_entry_price
            else:
                pnl = (actual_entry_price - actual_exit_price) * signal.position_size / actual_entry_price
                
            self.losses += 1
            self.consecutive_losses += 1
        
        self.total_pnl += pnl
        
        executed_trade = ExecutedTrade(
            trade_id=trade_id,
            signal=signal,
            execution_timestamp=execution_time,
            actual_entry_price=actual_entry_price,
            actual_exit_price=actual_exit_price,
            result=result,
            pnl=pnl,
            duration_seconds=duration,
            slippage=slippage
        )
        
        self.trade_history.append(executed_trade)
        return executed_trade
    
    def _calculate_win_probability(self, signal: TradeSignal) -> float:
        """Calculate win probability based on signal characteristics"""
        base_probability = 60.0  # Base 60% win rate
        
        # Adjust based on asset class
        if signal.asset_class == AssetClass.FX:
            asset_adjustment = 3.0  # FX slightly more predictable
        else:
            asset_adjustment = -2.0  # Crypto more volatile
        
        # Adjust based on confidence
        confidence_adjustment = (signal.confidence - 0.8) * 10.0
        
        # Adjust based on strategy
        strategy_adjustments = {
            "trend_following": 2.0,
            "mean_reversion": 1.0,
            "momentum": 1.5,
            "defi_arbitrage": 3.0,
            "volatility_harvest": -1.0,
            "cross_exchange": 2.5
        }
        strategy_adjustment = strategy_adjustments.get(signal.strategy, 0.0)
        
        final_probability = base_probability + asset_adjustment + confidence_adjustment + strategy_adjustment
        return max(45.0, min(75.0, final_probability))  # Cap between 45-75%
    
    def check_safety_conditions(self) -> bool:
        """Check if it's safe to continue trading"""
        # Check consecutive losses
        if self.consecutive_losses >= self.max_consecutive_losses:
            logger.warning(f"Safety stop: {self.consecutive_losses} consecutive losses")
            return False
        
        # Check latency failures
        if self.latency_failures >= self.max_latency_failures:
            logger.warning(f"Safety stop: {self.latency_failures} latency failures")
            return False
        
        # Check system resources (simplified)
        try:
            load_avg = os.getloadavg()[0]
            cpu_cores = os.cpu_count() or 1
            cpu_load_pct = (load_avg / cpu_cores) * 100
            
            if cpu_load_pct > self.config.get("risk_parameters", {}).get("max_cpu_load", 80.0):
                logger.warning(f"Safety stop: High CPU load {cpu_load_pct:.1f}%")
                return False
        except:
            # If we can't check system load, continue but log warning
            logger.warning("Could not check system load")
        
        return True
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current trading statistics"""
        total_completed = self.wins + self.losses
        win_rate = (self.wins / total_completed * 100) if total_completed > 0 else 0.0
        avg_pnl = (self.total_pnl / total_completed) if total_completed > 0 else 0.0
        
        # Simple Sharpe estimation
        if total_completed > 10:
            returns = [t.pnl for t in self.trade_history[-10:]]
            avg_return = sum(returns) / len(returns)
            std_return = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
            sharpe_estimate = (avg_return / std_return) * (252 ** 0.5) if std_return > 0 else 0.0
        else:
            sharpe_estimate = 0.0
        
        return {
            "trades_executed": self.trades_executed,
            "fx_trades": self.fx_trades,
            "crypto_trades": self.crypto_trades,
            "wins": self.wins,
            "losses": self.losses,
            "win_rate_pct": win_rate,
            "total_pnl": self.total_pnl,
            "avg_pnl": avg_pnl,
            "consecutive_losses": self.consecutive_losses,
            "sharpe_estimate": sharpe_estimate,
            "elapsed_time": (datetime.now(timezone.utc) - self.start_time).total_seconds()
        }
    
    def execute_trade(self, signal: TradeSignal) -> ExecutedTrade:
        """Execute a single trade"""
        logger.info(f"Executing trade: {signal.signal_id} - {signal.symbol} {signal.strategy}")
        
        executed_trade = self.simulate_execution(signal)
        
        # Update counters
        self.trades_executed += 1
        if signal.asset_class == AssetClass.FX:
            self.fx_trades += 1
        else:
            self.crypto_trades += 1
        
        # Log result
        result_str = "WIN" if executed_trade.result == TradeResult.WIN else "LOSS"
        logger.info(f"Trade {executed_trade.trade_id}: {result_str} - PnL: ${executed_trade.pnl:.2f}")
        
        return executed_trade
    
    async def run_canary(self) -> Dict[str, Any]:
        """Run the micro trading canary"""
        logger.info("Starting micro trading canary")
        self.active = True
        
        target_fx = self.config["fx_trades_target"]
        target_crypto = self.config["crypto_trades_target"]
        total_target = self.config["total_trades"]
        
        try:
            while (self.trades_executed < total_target and 
                   self.active and 
                   self.check_safety_conditions()):
                
                # Determine next trade type
                fx_remaining = target_fx - self.fx_trades
                crypto_remaining = target_crypto - self.crypto_trades
                
                if fx_remaining > 0 and crypto_remaining > 0:
                    # Both available, alternate
                    asset_class = AssetClass.FX if self.trades_executed % 2 == 0 else AssetClass.CRYPTO
                elif fx_remaining > 0:
                    asset_class = AssetClass.FX
                elif crypto_remaining > 0:
                    asset_class = AssetClass.CRYPTO
                else:
                    break
                
                # Generate and execute signal
                signal = self.generate_signal(asset_class, self.trades_executed + 1)
                executed_trade = self.execute_trade(signal)
                
                # Checkpoint every 15 trades
                if self.trades_executed % 15 == 0:
                    stats = self.get_current_stats()
                    logger.info(f"Checkpoint {self.trades_executed}/{total_target}: "
                              f"Win Rate: {stats['win_rate_pct']:.1f}%, "
                              f"PnL: ${stats['total_pnl']:.2f}")
                
                # Small delay between trades
                await asyncio.sleep(0.5 + (hash(str(self.trades_executed)) % 15) / 10.0)
        
        except Exception as e:
            logger.error(f"Error during canary execution: {e}")
            self.active = False
        
        finally:
            self.active = False
            logger.info("Micro trading canary completed")
        
        return self.get_final_results()
    
    def get_final_results(self) -> Dict[str, Any]:
        """Get final canary results"""
        stats = self.get_current_stats()
        
        # Evaluate against targets
        target_win_rate = self.config.get("target_win_rate", 65.0)
        target_sharpe = self.config.get("target_sharpe", 1.2)
        
        win_rate_pass = stats["win_rate_pct"] >= target_win_rate
        sharpe_pass = stats["sharpe_estimate"] >= target_sharpe
        pnl_pass = stats["total_pnl"] > 0.0
        
        overall_pass = win_rate_pass and sharpe_pass and pnl_pass
        
        results = {
            **stats,
            "targets": {
                "win_rate_target": target_win_rate,
                "sharpe_target": target_sharpe,
                "win_rate_pass": win_rate_pass,
                "sharpe_pass": sharpe_pass,
                "pnl_pass": pnl_pass,
                "overall_pass": overall_pass
            },
            "trade_history": [asdict(trade) for trade in self.trade_history],
            "canary_config": self.config
        }
        
        return results
    
    def save_results(self, results: Dict[str, Any], output_path: str) -> None:
        """Save results to file"""
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            logger.info(f"Results saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to save results: {e}")

async def main():
    """Main entry point"""
    if len(sys.argv) != 2:
        print("Usage: python3 micro_trading_engine.py <config_path>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    # Setup signal handler for graceful shutdown
    engine = None
    
    def signal_handler(signum, frame):
        logger.info("Received shutdown signal")
        if engine:
            engine.active = False
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Initialize and run engine
        engine = MicroTradingEngine(config_path)
        results = await engine.run_canary()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"logs/micro_canary/canary_results_{timestamp}.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        engine.save_results(results, output_path)
        
        # Print summary
        print(f"\n{'='*70}")
        print("🐤 MICRO CANARY RESULTS")
        print(f"{'='*70}")
        print(f"Trades Executed: {results['trades_executed']}")
        print(f"Win Rate: {results['win_rate_pct']:.1f}% (Target: ≥{results['targets']['win_rate_target']}%)")
        print(f"Total P&L: ${results['total_pnl']:.2f}")
        print(f"Sharpe Estimate: {results['sharpe_estimate']:.2f} (Target: ≥{results['targets']['sharpe_target']})")
        print(f"FX Trades: {results['fx_trades']} | Crypto Trades: {results['crypto_trades']}")
        print(f"{'='*70}")
        
        if results['targets']['overall_pass']:
            print("🎉 MICRO CANARY PASSED - ALL TARGETS ACHIEVED")
        else:
            print("❌ MICRO CANARY FAILED - TARGETS NOT MET")
        
        print(f"Results saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())