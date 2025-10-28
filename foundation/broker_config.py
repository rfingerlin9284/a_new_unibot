"""
Paper Broker Config - Broker-agnostic paper trading setup (Phase 9)
PIN: 841921 | Profile: Non-HFT (M15-H1)
Reads environment variables for paper API credentials
"""
import os
from pathlib import Path

class PaperBrokerConfig:
    """
    Paper API broker configuration.
    Reads credentials from environment variables.
    Falls back to OANDA credentials if PAPER_API_* not set.
    """
    
    # Try PAPER_API_* first, fallback to OANDA_* for compatibility
    BASE_URL = os.getenv("PAPER_API_BASE_URL") or os.getenv("OANDA_API_URL", "https://api-fxpractice.oanda.com")
    KEY = os.getenv("PAPER_API_KEY") or os.getenv("OANDA_API_KEY", "")
    SECRET = os.getenv("PAPER_API_SECRET") or os.getenv("OANDA_ACCOUNT_ID", "")
    MODE = os.getenv("BROKER_MODE", "paper")
    TIMEFRAME_DEFAULT = os.getenv("TIMEFRAME_DEFAULT", "H1")
    
    @classmethod
    def ready(cls) -> bool:
        """
        Check if all required credentials are configured.
        
        Returns:
            bool: True if ready for paper trading
        """
        return bool(cls.KEY and cls.SECRET and cls.BASE_URL and cls.MODE == "paper")
    
    @classmethod
    def summary(cls) -> dict:
        """
        Get configuration summary (sanitized for logging).
        
        Returns:
            dict: Configuration snapshot
        """
        return {
            "mode": cls.MODE,
            "timeframe": cls.TIMEFRAME_DEFAULT,
            "base_url": cls.BASE_URL[:30] + "..." if len(cls.BASE_URL) > 30 else cls.BASE_URL,
            "has_key": bool(cls.KEY),
            "has_secret": bool(cls.SECRET),
            "ready": cls.ready()
        }

CONFIG = PaperBrokerConfig()
