import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class FeeMarginCalculator:
    """Calculates the operational margin on AUM fees relative to the cost of beta."""
    
    BETA_COST = 0.0003 # 0.03% (Standard low-cost ETF)

    def calculate_margin(self, gross_fee: float, operational_cost: float) -> Dict[str, Any]:
        """
        Net Margin = Gross Fee - Operational Cost - Cost of Beta
        """
        net_fee = gross_fee - operational_cost
        margin_vs_beta = net_fee - self.BETA_COST
        
        logger.info(f"FINANCE_LOG: Fee Margin analysis: Gross {gross_fee:.2%}, Net {net_fee:.2%}. Surplus over Beta: {margin_vs_beta:.2%}")
        
        return {
            "gross_fee_pct": round(gross_fee, 4),
            "net_fee_pct": round(net_fee, 4),
            "margin_vs_beta_bps": round(margin_vs_beta * 10000, 0),
            "profitability": "HIGH" if margin_vs_beta > 0 else "PRESSURED"
        }
