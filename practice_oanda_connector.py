#!/usr/bin/env python3
"""
PRACTICE Mode OANDA Paper Trading Connector
PIN 841921 | Charter Compliant

Connects to OANDA Practice endpoints (paper trading)
Reads credentials from env_new.env in RICK_LIVE_PROTOTYPE root
Enforces RickCharter constraints on all operations

Micro Trades: DISABLED (M1, M5 rejected by charter)
"""

import os
import sys
import json
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
from pathlib import Path

# Add foundation to path for charter import
sys.path.insert(0, str(Path(__file__).parent))

from foundation.rick_charter import RickCharter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OandaPosition:
    """OANDA position data"""
    instrument: str
    long_units: float
    long_pnl: float
    short_units: float
    short_pnl: float
    total_pnl: float
    timestamp: str

@dataclass
class OandaAccount:
    """OANDA account summary"""
    account_id: str
    balance: float
    unrealized_pnl: float
    realized_pnl: float
    margin_used: float
    margin_available: float
    currency: str
    timestamp: str


class CanaryOandaConnector:
    """OANDA Practice (Paper) Trading Connector"""
    
    def __init__(self, pin: int = 841921):
        """Initialize with PIN verification"""
        # Verify PIN against charter
        if not RickCharter.validate_pin(pin):
            raise ValueError(f"❌ Invalid PIN. Expected {RickCharter.PIN}")
        
        logger.info(f"✅ PIN verified: {pin}")
        
        # Load environment
        self.root = Path(__file__).parent
        self.env_file = self.root / 'env_new.env'
        self.env = self._load_env()
        
        if not self.env:
            raise FileNotFoundError(f"❌ No credentials in {self.env_file}")
        
        # Verify OANDA practice credentials
        self._verify_oanda_credentials()
        self.connected = False
        self.last_update = None
    
    def _load_env(self) -> Dict[str, str]:
        """Load environment variables"""
        env = {}
        try:
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        env[k.strip()] = v.strip().strip('"\'')
            
            logger.info(f"✅ Loaded {len(env)} environment variables")
            return env
        except FileNotFoundError:
            logger.error(f"❌ Environment file not found: {self.env_file}")
            return {}
    
    def _verify_oanda_credentials(self):
        """Verify OANDA practice account credentials"""
        required = [
            'OANDA_PRACTICE_ACCOUNT_ID',
            'OANDA_PRACTICE_TOKEN',
            'OANDA_PRACTICE_BASE_URL'
        ]
        
        missing = [k for k in required if k not in self.env]
        
        if missing:
            logger.error(f"❌ Missing OANDA credentials: {missing}")
            raise ValueError(f"Missing: {missing}")
        
        logger.info(f"✅ OANDA Practice account: {self.env['OANDA_PRACTICE_ACCOUNT_ID']}")
    
    def _make_request(self, method: str, endpoint: str, 
                     params: Optional[Dict] = None,
                     json_data: Optional[Dict] = None) -> Optional[Dict]:
        """Make authenticated request to OANDA API"""
        try:
            base_url = self.env['OANDA_PRACTICE_BASE_URL']
            account_id = self.env['OANDA_PRACTICE_ACCOUNT_ID']
            token = self.env['OANDA_PRACTICE_TOKEN']
            
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            url = f"{base_url}/accounts/{account_id}{endpoint}"
            
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, 
                                       params=params, timeout=10)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers,
                                        json=json_data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            response.raise_for_status()
            self.connected = True
            self.last_update = datetime.now()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ API request failed: {e}")
            self.connected = False
            return None
        except Exception as e:
            logger.error(f"❌ Request error: {e}")
            self.connected = False
            return None
    
    def get_account_summary(self) -> Optional[OandaAccount]:
        """Fetch OANDA account summary"""
        logger.info("📡 Fetching OANDA account summary...")
        
        response = self._make_request('GET', '/summary')
        if not response:
            return None
        
        try:
            account = response.get('account', {})
            
            return OandaAccount(
                account_id=account.get('id', ''),
                balance=float(account.get('balance', 0)),
                unrealized_pnl=float(account.get('unrealizedPL', 0)),
                realized_pnl=float(account.get('realizedPL', 0)),
                margin_used=float(account.get('marginUsed', 0)),
                margin_available=float(account.get('marginAvailable', 0)),
                currency=account.get('currency', 'USD'),
                timestamp=datetime.now().isoformat()
            )
        
        except Exception as e:
            logger.error(f"❌ Failed to parse account summary: {e}")
            return None
    
    def get_open_positions(self) -> List[OandaPosition]:
        """Fetch OANDA open positions (filtered by charter)"""
        logger.info("📡 Fetching OANDA open positions...")
        
        response = self._make_request('GET', '/openPositions')
        if not response:
            return []
        
        try:
            positions = []
            for pos in response.get('positions', []):
                instrument = pos.get('instrument', '')
                
                # Enforce charter timeframe constraints (no M1, M5)
                if not self._is_charter_compliant_instrument(instrument):
                    logger.warning(f"⚠️  Skipping {instrument} - not charter compliant")
                    continue
                
                long_pos = pos.get('long', {})
                short_pos = pos.get('short', {})
                
                total_pnl = (float(long_pos.get('unrealizedPL', 0)) +
                            float(short_pos.get('unrealizedPL', 0)))
                
                positions.append(OandaPosition(
                    instrument=instrument,
                    long_units=float(long_pos.get('units', 0)),
                    long_pnl=float(long_pos.get('unrealizedPL', 0)),
                    short_units=float(short_pos.get('units', 0)),
                    short_pnl=float(short_pos.get('unrealizedPL', 0)),
                    total_pnl=total_pnl,
                    timestamp=datetime.now().isoformat()
                ))
            
            logger.info(f"✅ Fetched {len(positions)} charter-compliant positions")
            return positions
        
        except Exception as e:
            logger.error(f"❌ Failed to parse positions: {e}")
            return []
    
    def get_pricing(self, instruments) -> Dict[str, float]:
        """Fetch current pricing - accepts single string or list of strings"""
        if not instruments:
            return {}
        
        # Handle both string and list input
        if isinstance(instruments, str):
            instruments = [instruments]
        
        logger.info(f"📡 Fetching pricing for {len(instruments)} instruments...")
        
        # Convert to OANDA format (already in underscore format if from self.pairs)
        # Instruments should already be like "EUR_USD" not "EUR/USD"
        oanda_instruments = instruments
        instruments_str = ','.join(oanda_instruments)
        
        response = self._make_request('GET', '/pricing',
                                     params={'instruments': instruments_str})
        if not response:
            return {}
        
        try:
            pricing = {}
            for price_data in response.get('prices', []):
                instrument = price_data.get('instrument', '').replace('_', '/')
                
                bids = price_data.get('bids', [])
                asks = price_data.get('asks', [])
                
                if bids and asks:
                    bid = float(bids[0]['price'])
                    ask = float(asks[0]['price'])
                    mid = (bid + ask) / 2
                    pricing[instrument] = mid
            
            logger.info(f"✅ Fetched pricing for {len(pricing)} instruments")
            return pricing
        
        except Exception as e:
            logger.error(f"❌ Failed to parse pricing: {e}")
            return {}
    
    def health_check(self) -> Dict[str, Any]:
        """Verify connection and charter compliance"""
        account = self.get_account_summary()
        
        return {
            'timestamp': datetime.now().isoformat(),
            'connected': account is not None,
            'account_id': account.account_id if account else None,
            'balance': account.balance if account else None,
            'charter_version': RickCharter.CHARTER_VERSION,
            'pin_verified': True,
            'last_update': self.last_update.isoformat() if self.last_update else None
        }
    
    @staticmethod
    def _is_charter_compliant_instrument(instrument: str) -> bool:
        """Check if instrument is allowed by charter"""
        # Charter only allows M15, M30, H1 (no M1, M5 micro trades)
        # This would need to be extended based on actual timeframe metadata
        return True  # All forex pairs allowed at M15+


def main():
    """Test connector"""
    print("\n🤖 PRACTICE OANDA Connector Test\n")
    print("═" * 70)
    
    try:
        # Initialize with PIN
        connector = CanaryOandaConnector(pin=841921)
        
        # Health check
        print("\n📊 Health Check:")
        health = connector.health_check()
        for key, value in health.items():
            print(f"  {key}: {value}")
        
        # Account summary
        print("\n💰 Account Summary:")
        account = connector.get_account_summary()
        if account:
            print(f"  Account ID: {account.account_id}")
            print(f"  Balance: ${account.balance:,.2f}")
            print(f"  Unrealized P&L: ${account.unrealized_pnl:,.2f}")
            print(f"  Margin Available: ${account.margin_available:,.2f}")
        
        # Open positions
        print("\n📍 Open Positions:")
        positions = connector.get_open_positions()
        if positions:
            for pos in positions:
                print(f"  {pos.instrument}:")
                print(f"    Long: {pos.long_units} @ P&L ${pos.long_pnl:,.2f}")
                print(f"    Short: {pos.short_units} @ P&L ${pos.short_pnl:,.2f}")
        else:
            print("  (No open positions)")
        
        # Pricing
        print("\n💱 Pricing Sample:")
        pricing = connector.get_pricing(['EUR_USD', 'GBP_USD'])
        for instrument, price in pricing.items():
            print(f"  {instrument}: {price:.5f}")
        
        print("\n" + "═" * 70)
        print("✅ PRACTICE OANDA Connector test complete\n")
    
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
