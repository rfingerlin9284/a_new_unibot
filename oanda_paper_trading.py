#!/usr/bin/env python3
"""
OANDA Paper Trading Engine - PIN 841921
OANDA-only paper trading with your $1,970.79 practice account
Charter-compliant autonomous trading
"""

import sys
import time
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent))

from canary_oanda_connector import CanaryOandaConnector
from foundation.rick_charter import RickCharter

class OandaPaperTradingEngine:
    """OANDA-only paper trading engine"""
    
    def __init__(self, pin: int = 841921):
        """Initialize with PIN verification"""
        print("=" * 80)
        print("🤖 OANDA PAPER TRADING ENGINE - PIN 841921")
        print("=" * 80)
        
        if not RickCharter.validate_pin(pin):
            raise ValueError(f"❌ Invalid PIN. Expected {RickCharter.PIN}")
        
        self.pin = pin
        self.charter = RickCharter
        
        # Initialize OANDA connector
        print("🔌 Connecting to OANDA Practice API...")
        self.oanda = CanaryOandaConnector(pin=pin)
        
        # Get account info
        account = self.oanda.get_account_summary()
        self.account_id = account.account_id
        self.capital = account.balance
        
        print(f"✅ OANDA Practice Connected")
        print(f"   Account: {self.account_id}")
        print(f"   Capital: ${self.capital:.2f}")
        print(f"   Charter: {self.charter.CHARTER_VERSION}")
        print("=" * 80)
        
        # Trading pairs (charter-compliant: M15, M30, H1 only)
        # Major pairs - highest liquidity
        self.pairs = [
            # Major USD pairs
            "EUR_USD",  # Euro
            "GBP_USD",  # British Pound
            "USD_JPY",  # Japanese Yen
            "USD_CHF",  # Swiss Franc
            "AUD_USD",  # Australian Dollar
            "USD_CAD",  # Canadian Dollar
            "NZD_USD",  # New Zealand Dollar
            
            # Major crosses (no USD)
            "EUR_GBP",  # Euro/Pound
            "EUR_JPY",  # Euro/Yen
            "GBP_JPY",  # Pound/Yen
            "EUR_CHF",  # Euro/Swiss
            "GBP_CHF",  # Pound/Swiss
            "AUD_JPY",  # Aussie/Yen
            "NZD_JPY",  # Kiwi/Yen
            
            # Commodity currencies
            "AUD_CAD",  # Aussie/Canadian
            "AUD_NZD",  # Aussie/Kiwi
            "EUR_AUD",  # Euro/Aussie
            "EUR_CAD",  # Euro/Canadian
            "GBP_AUD",  # Pound/Aussie
            "GBP_CAD",  # Pound/Canadian
        ]
        
        # Stats
        self.iteration = 0
        self.trades_today = 0
        self.daily_pnl = 0.0
        self.open_positions = []
        
    def run(self, max_iterations: int = None):
        """Run trading loop"""
        print(f"\n🚀 Starting OANDA paper trading session...")
        print(f"   Max iterations: {max_iterations or 'Infinite'}")
        print(f"   Pairs: {', '.join(self.pairs)}")
        print(f"   Update frequency: Every 5 seconds")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            iteration = 0
            while max_iterations is None or iteration < max_iterations:
                iteration += 1
                self.iteration = iteration
                
                # Display header
                print("\n" + "=" * 80)
                print(f"⏱️  Iteration {iteration} - {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC")
                print("=" * 80)
                
                # Get account status
                account = self.oanda.get_account_summary()
                
                print(f"\n💰 Account Status:")
                print(f"   Balance: ${account.balance:.2f}")
                print(f"   Unrealized P&L: ${account.unrealized_pnl:.2f}")
                print(f"   Margin Used: ${account.margin_used:.2f}")
                print(f"   Margin Available: ${account.margin_available:.2f}")
                
                # Get positions
                positions = self.oanda.get_open_positions()
                
                print(f"\n📍 Open Positions: {len(positions)}")
                if positions:
                    for pos in positions:
                        net_units = pos.long_units + pos.short_units
                        direction = "LONG" if net_units > 0 else "SHORT"
                        print(f"   {pos.instrument}: {direction} {abs(net_units):.0f} units | P&L: ${pos.total_pnl:.2f}")
                else:
                    print("   No open positions")
                
                # Get live pricing
                print(f"\n💱 Live Pricing:")
                try:
                    # Get all prices at once
                    pricing = self.oanda.get_pricing(self.pairs)
                    if pricing:
                        for pair in self.pairs:
                            pair_format = pair.replace('_', '/')
                            if pair_format in pricing:
                                mid_price = pricing[pair_format]
                                print(f"   {pair}: {mid_price:.5f}")
                            else:
                                print(f"   {pair}: No pricing data")
                    else:
                        print("   No pricing data available")
                except Exception as e:
                    print(f"   ⚠️ Pricing error: {e}")
                
                # Charter compliance check
                print(f"\n✅ Charter Compliance:")
                print(f"   Max Concurrent Positions: {len(positions)}/{self.charter.MAX_CONCURRENT_POSITIONS}")
                print(f"   Daily Trades: {self.trades_today}/{self.charter.MAX_DAILY_TRADES}")
                print(f"   Daily P&L: ${self.daily_pnl:.2f}")
                
                daily_pnl_pct = (self.daily_pnl / self.capital * 100) if self.capital > 0 else 0
                if daily_pnl_pct <= self.charter.DAILY_LOSS_BREAKER_PCT:
                    print(f"   ⚠️ DAILY LOSS BREAKER HIT: {daily_pnl_pct:.2f}% (limit: {self.charter.DAILY_LOSS_BREAKER_PCT}%)")
                    print(f"   🛑 Trading halted for today")
                
                # Wait before next iteration
                print(f"\n⏳ Next update in 5 seconds...")
                time.sleep(5)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Trading session stopped by user")
            self._print_session_summary()
        except Exception as e:
            print(f"\n❌ Error: {e}")
            self._print_session_summary()
            raise
    
    def _print_session_summary(self):
        """Print session summary"""
        print("\n" + "=" * 80)
        print("📊 SESSION SUMMARY")
        print("=" * 80)
        print(f"Total iterations: {self.iteration}")
        print(f"Trades today: {self.trades_today}")
        print(f"Daily P&L: ${self.daily_pnl:.2f}")
        
        # Final account status
        try:
            account = self.oanda.get_account_summary()
            print(f"\nFinal Balance: ${account.balance:.2f}")
            print(f"Unrealized P&L: ${account.unrealized_pnl:.2f}")
        except:
            pass
        
        print("=" * 80)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='OANDA Paper Trading Engine')
    parser.add_argument('--pin', type=int, default=841921, help='Charter PIN')
    parser.add_argument('--iterations', type=int, default=None, help='Max iterations (default: infinite)')
    args = parser.parse_args()
    
    # Start engine
    engine = OandaPaperTradingEngine(pin=args.pin)
    engine.run(max_iterations=args.iterations)

if __name__ == "__main__":
    main()
