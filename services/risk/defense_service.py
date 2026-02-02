import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class DefenseService:
    """
    Phase 198: Bear Market Defense.
    Handles regime detection and portfolio beta rotation.
    """
    
    def detect_market_regime(self, price: float, sma200: float, momentum_30d: float) -> str:
        """
        Phase 198.1: Regime Detector.
        Identifies BULL, BEAR, or TRANSITION regimes.
        """
        is_above_sma = price > sma200
        
        if is_above_sma and momentum_30d > 0:
            return "BULL"
        elif not is_above_sma and momentum_30d < 0:
            return "BEAR"
        else:
            return "TRANSITION"

    def calculate_beta_reduction(self, current_beta: float, sector_exposures: Dict[str, float]) -> Dict[str, Any]:
        """
        Phase 198.2: Beta Reducer (Sector Rotation).
        Recommends shifts from high-beta tech to low-beta defensives.
        """
        target_beta = 0.7
        reduction_needed = max(0.0, current_beta - target_beta)
        
        trades = []
        if reduction_needed > 0:
            if sector_exposures.get("TECH", 0) > 0.2:
                trades.append({"action": "SELL", "sector": "TECH", "amount": "TRIM_TO_LOW_BETA"})
            trades.append({"action": "BUY", "sector": "UTILITIES", "amount": "ALLOCATE_DEFENSIVE"})
            trades.append({"action": "BUY", "sector": "HEALTHCARE", "amount": "ALLOCATE_DEFENSIVE"})
            
        logger.info(f"DEFENSE_LOG: Beta reduction recommended: {reduction_needed:.2f}")
        
        return {
            "current_beta": current_beta,
            "target_beta": target_beta,
            "reduction_needed": reduction_needed,
            "recommended_trades": trades
        }

    def evaluate_dividend_safety(self, payout_ratio: float, dividend_yield: float) -> Dict[str, Any]:
        """
        Phase 198.5: Dividend Safety (Aristocrats).
        """
        is_safe = payout_ratio < 0.6 and dividend_yield < 0.08
        
        status = "SAFE" if is_safe else "DANGER"
        if dividend_yield > 0.10: status = "TRAP"
        
        return {
            "safety_status": status,
            "payout_ratio": payout_ratio,
            "is_sustainable": is_safe
        }
