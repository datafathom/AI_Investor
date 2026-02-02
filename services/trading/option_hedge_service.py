import logging
from typing import Dict, List, Any
from decimal import Decimal

logger = logging.getLogger(__name__)

class OptionHedgeService:
    """
    Phase 189.1: Options Hedging & Volatility Strategy Engine.
    Analyzes VIX and tax state to recommend optimal protective strategies.
    """
    
    def analyze_vix_regime(self, vix: float) -> str:
        if vix < 15: return "LOW_VOL"
        if vix < 25: return "NORMAL_VOL"
        if vix < 40: return "HIGH_VOL"
        return "EXTREME_VOL"

    def recommend_hedge(self, ticker: str, spot_price: float, vix: float, unrealized_gain: Decimal) -> Dict[str, Any]:
        """
        Phase 189.1: VolEnvAnalyzer.
        Identifies the best strategy based on VIX and tax state.
        """
        regime = self.analyze_vix_regime(vix)
        
        # Logic: If gains are high, we favor hedges that avoid selling (Tax Shield)
        tax_shield_priority = unrealized_gain > Decimal("100000")
        
        strategy = ""
        justification = ""
        
        if regime == "LOW_VOL":
            strategy = "PUT_COLLAR"
            justification = "Cheap protection; downside limited with capped upside."
        elif regime == "NORMAL_VOL":
            strategy = "LONG_PUT"
            justification = "Direct downside protection without capping gains."
        else:
            strategy = "VIX_CALLS"
            justification = "Direct volatility exposure to offset systemic crash."
            
        if tax_shield_priority:
            justification += " Optimized to avoid forced sale and realized gains."

        logger.info(f"HEDGE_LOG: Recommended {strategy} for {ticker} in {regime} regime.")
        
        return {
            "ticker": ticker,
            "regime": regime,
            "strategy": strategy,
            "justification": justification,
            "strikes": {
                "put": round(spot_price * 0.95, 2),
                "call": round(spot_price * 1.10, 2) if strategy == "PUT_COLLAR" else None
            }
        }

    def calculate_tax_shield(self, hedge_cost: Decimal, potential_tax_hit: Decimal) -> Dict[str, Any]:
        """
        Phase 189.2: Tax Shield Calculator.
        """
        net_benefit = potential_tax_hit - hedge_cost
        efficiency = (net_benefit / potential_tax_hit) * 100 if potential_tax_hit > 0 else 0
        
        return {
            "hedge_cost": hedge_cost,
            "tax_saved": potential_tax_hit,
            "net_benefit": net_benefit,
            "efficiency_pct": round(efficiency, 2)
        }
