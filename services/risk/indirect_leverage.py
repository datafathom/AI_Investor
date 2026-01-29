import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class IndirectLeverageCalculator:
    """Calculates 'True Leverage' including notional values of derivatives."""
    
    def calculate_true_leverage(self, equity: float, stock_value: float, 
                                options_notional: float, futures_notional: float) -> Dict[str, Any]:
        """
        Policy: True Leverage = (Stock + OptionsNotional + FuturesNotional) / Equity
        """
        if equity <= 0: return {"leverage_ratio": 99.9, "status": "BANKRUPT"}
        
        gross_exposure = stock_value + options_notional + futures_notional
        ratio = gross_exposure / equity
        
        if ratio > 3.0:
            status = "CRITICAL"
        elif ratio > 2.0:
            status = "WARNING"
        else:
            status = "SAFE"
            
        logger.info(f"RISK_LOG: True Leverage: {ratio:.2f}x (Exposure: ${gross_exposure:,.2f} on ${equity:,.2f} Equity)")
        
        return {
            "gross_exposure": round(float(gross_exposure), 2),
            "leverage_ratio": round(float(ratio), 4),
            "status": status
        }
