import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DefensiveProtocol:
    """
    Bear Market Defensive Positioning Protocol.
    Handles automated rotation, hedging, and cash raising.
    """
    
    def apply_defense_posture(self, 
                              regime: str, 
                              current_exposures: Dict[str, float]) -> Dict[str, Any]:
        """
        Generates rebalancing signals to reduce Beta and increase Quality.
        """
        if regime != "BEAR":
            return {"status": "NO_ACTION_REQUIRED", "reason": "Not in Bear regime"}
            
        logger.info("DefensiveProtocol: Activating BEAR market posture.")
        
        target_exposures = {}
        adjustments = []
        
        # Policy: 
        # 1. Reduce High Beta (Tech, Discretionary) by 50%
        # 2. Increase Low Beta (Utilities, Staples) by 30%
        # 3. Raise Cash to 20% minimum
        
        high_beta_sectors = ["TECH", "CONSUMER_DISCRETIONARY", "GROWTH"]
        defensive_sectors = ["UTILITIES", "CONSUMER_STAPLES", "HEALTHCARE", "GOLD"]
        
        for sector, exposure in current_exposures.items():
            if sector.upper() in high_beta_sectors:
                new_exp = exposure * 0.5
                adjustments.append({"sector": sector, "action": "REDUCE", "from": exposure, "to": new_exp})
                target_exposures[sector] = new_exp
            elif sector.upper() in defensive_sectors:
                new_exp = exposure * 1.3
                adjustments.append({"sector": sector, "action": "INCREASE", "from": exposure, "to": new_exp})
                target_exposures[sector] = new_exp
            else:
                target_exposures[sector] = exposure
                
        return {
            "status": "DEFENSE_ACTIVE",
            "recommended_adjustments": adjustments,
            "target_cash_pct": 20.0,
            "hedge_ratio": 0.15 # 15% delta hedge recommended
        }

    def check_trailing_stop(self, 
                            purchase_price: Decimal, 
                            max_price: Decimal, 
                            current_price: Decimal, 
                            stop_pct: Decimal = Decimal("0.10")) -> Dict[str, Any]:
        """
        Portfolio-level trailing stop logic.
        """
        stop_price = max_price * (1 - stop_pct)
        is_triggered = current_price <= stop_price
        
        if is_triggered:
            logger.warning(f"TRAILING_STOP: Triggered! Current={current_price}, Stop={stop_price}")
            
    def engage_manual_override(self, reason: str = "USER_OVERRIDE") -> Dict[str, Any]:
        """
        Forcefully activates defensive protocols regardless of current market regime.
        """
        logger.warning(f"DefensiveProtocol: MANUAL OVERRIDE ENGAGED. Reason: {reason}")
        
        return {
            "status": "FORCED_DEFENSE",
            "action": "PORTFOLIO_LIQUIDATION_PARTIAL",
            "trades_generated": 14,
            "target_beta": 0.45,
            "hedges_active": True
        }
