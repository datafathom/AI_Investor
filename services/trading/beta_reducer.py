import logging
from typing import List, Dict, Any
from services.strategies.regime_detector import MarketRegime

logger = logging.getLogger(__name__)

class BetaReducerService:
    """
    Manages portfolio Beta exposure based on Market Regime.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BetaReducerService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("BetaReducerService initialized")

    def recommend_rotation(self, current_holdings: List[Dict[str, Any]], regime: MarketRegime) -> List[Dict[str, Any]]:
        """
        If Risk Off, suggests reducing High Beta assets.
        """
        recommendations = []
        
        if regime == MarketRegime.RISK_OFF:
            logger.info("BetaReducer: Generating defense rotation plan.")
            for asset in current_holdings:
                beta = asset.get('beta', 1.0)
                ticker = asset.get('ticker', 'UNKNOWN')
                
                # If Beta is significantly high in a bear market, reduce
                if beta > 1.2:
                    recommendations.append({
                        "action": "REDUCE",
                        "ticker": ticker,
                        "reason": f"High Beta ({beta}) in Risk Off Regime",
                        "suggested_allocation_delta": -0.5 # Cut position in half
                    })
                elif beta < 0.8:
                    recommendations.append({
                        "action": "INCREASE",
                        "ticker": ticker,
                        "reason": f"Low Beta ({beta}) Defensive Anchor",
                        "suggested_allocation_delta": 0.2 # boost
                    })
        else:
            logger.info("BetaReducer: Risk On. No defensive beta reduction needed.")
            
        return recommendations
