import logging
from enum import Enum
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class MarketRegime(Enum):
    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    UNCERTAIN = "UNCERTAIN"

class RegimeDetectorService:
    """
    Detects the current market regime (Bull vs Bear) to trigger defensive protocols.
    Primary Logic: Price vs 200-Day SMA.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RegimeDetectorService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("RegimeDetectorService initialized")

    def detect_regime(self, ticker: str = 'SPY', current_price: float = None, sma_200: float = None) -> MarketRegime:
        """
        Determines if we are in Risk On or Risk Off.
        Rule: If Price < 200 SMA -> Risk Off (Bear Market Defense).
        """
        if current_price is None or sma_200 is None:
            # In a real scenario, fetch from MarketDataService if not provided
            logger.warning("RegimeDetector: Missing price data, returning UNCERTAIN")
            return MarketRegime.UNCERTAIN

        if current_price < sma_200:
            logger.info(f"Regime Check: {ticker} ${current_price} < 200SMA ${sma_200} -> RISK OFF")
            return MarketRegime.RISK_OFF
        else:
            logger.info(f"Regime Check: {ticker} ${current_price} >= 200SMA ${sma_200} -> RISK ON")
            return MarketRegime.RISK_ON
