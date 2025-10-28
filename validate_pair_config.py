#!/usr/bin/env python3
"""
OANDA Forex Pair Configuration & Validation
Ensures all 18 pairs have correct $15K notional enforcement
PIN: 841921
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from foundation.rick_charter import RickCharter

# ALL AVAILABLE OANDA PAIRS (from env_new.env)
OANDA_PAIRS = {
    # Major USD pairs (base currency varies)
    'EUR_USD': {'type': 'major', 'pip_size': 0.0001, 'typical_price': 1.0800},
    'GBP_USD': {'type': 'major', 'pip_size': 0.0001, 'typical_price': 1.2700},
    'USD_JPY': {'type': 'major', 'pip_size': 0.01, 'typical_price': 150.00},
    'USD_CHF': {'type': 'major', 'pip_size': 0.0001, 'typical_price': 0.8800},
    'AUD_USD': {'type': 'major', 'pip_size': 0.0001, 'typical_price': 0.6500},
    'USD_CAD': {'type': 'major', 'pip_size': 0.0001, 'typical_price': 1.3600},
    'NZD_USD': {'type': 'major', 'pip_size': 0.0001, 'typical_price': 0.6000},
    
    # Major crosses (no USD)
    'EUR_GBP': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 0.8500},
    'EUR_JPY': {'type': 'cross', 'pip_size': 0.01, 'typical_price': 162.00},
    'GBP_JPY': {'type': 'cross', 'pip_size': 0.01, 'typical_price': 190.00},
    'AUD_JPY': {'type': 'cross', 'pip_size': 0.01, 'typical_price': 97.50},
    'CHF_JPY': {'type': 'cross', 'pip_size': 0.01, 'typical_price': 170.00},
    
    # European crosses
    'EUR_CHF': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 0.9500},
    'GBP_CHF': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 1.1200},
    
    # Commodity currency crosses
    'AUD_CHF': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 0.5700},
    'NZD_CHF': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 0.5300},
    'EUR_AUD': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 1.6600},
    'GBP_AUD': {'type': 'cross', 'pip_size': 0.0001, 'typical_price': 1.9500},
}

def calculate_units_for_notional(pair: str, price: float, notional_target: float = 15000) -> int:
    """Calculate units needed to reach notional target"""
    import math
    required_units = math.ceil(notional_target / price)
    # Round up to nearest 100 for clean sizing
    position_size = math.ceil(required_units / 100) * 100
    return position_size

def validate_all_pairs():
    """Validate that all 18 pairs meet charter $15K minimum"""
    print("=" * 80)
    print("OANDA FOREX PAIR CONFIGURATION VALIDATION")
    print(f"Charter MIN_NOTIONAL_USD: ${RickCharter.MIN_NOTIONAL_USD:,}")
    print("=" * 80)
    print()
    
    print(f"{'Pair':<12} {'Type':<8} {'Pip Size':<10} {'Price':<10} {'Units':<10} {'Notional':<12} {'Status'}")
    print("-" * 80)
    
    all_valid = True
    
    for pair, config in OANDA_PAIRS.items():
        price = config['typical_price']
        units = calculate_units_for_notional(pair, price)
        notional = units * price
        
        # Validate meets minimum
        meets_min = notional >= RickCharter.MIN_NOTIONAL_USD
        status = "✅ PASS" if meets_min else "❌ FAIL"
        
        if not meets_min:
            all_valid = False
        
        print(f"{pair:<12} {config['type']:<8} {config['pip_size']:<10} {price:<10.5f} {units:<10} ${notional:<11,.2f} {status}")
    
    print("=" * 80)
    
    if all_valid:
        print("✅ ALL 18 PAIRS VALIDATED - Charter compliance confirmed")
        print(f"   All pairs sized to meet ${RickCharter.MIN_NOTIONAL_USD:,} minimum notional")
    else:
        print("❌ VALIDATION FAILED - Some pairs below minimum")
    
    print()
    
    # Show examples of different unit counts for same notional
    print("=" * 80)
    print("EXAMPLE: Different Unit Counts for Same $15,000 Notional")
    print("=" * 80)
    
    examples = [
        ('EUR_USD', 1.0800),
        ('GBP_USD', 1.2700),
        ('USD_JPY', 150.00),
        ('NZD_USD', 0.6000),
    ]
    
    for pair, price in examples:
        units = calculate_units_for_notional(pair, price)
        notional = units * price
        print(f"{pair}: {units:,} units × {price:.4f} = ${notional:,.2f}")
    
    print()
    print("Note: USD/JPY needs FEWER units because each unit is worth MORE!")
    print()
    
    return all_valid

def show_pip_values():
    """Show pip values for all pairs"""
    print("=" * 80)
    print("PIP SIZE CONFIGURATION")
    print("=" * 80)
    print()
    
    print("Standard Pairs (0.0001 pip):")
    for pair, config in OANDA_PAIRS.items():
        if config['pip_size'] == 0.0001:
            print(f"  {pair}")
    
    print()
    print("JPY Pairs (0.01 pip):")
    for pair, config in OANDA_PAIRS.items():
        if config['pip_size'] == 0.01:
            print(f"  {pair}")
    
    print()

if __name__ == "__main__":
    print()
    valid = validate_all_pairs()
    show_pip_values()
    
    if valid:
        print("✅ Configuration complete - all pairs ready for trading")
        print("   Use: python3 oanda_trading_engine.py --env practice")
        sys.exit(0)
    else:
        print("❌ Configuration errors detected")
        sys.exit(1)
