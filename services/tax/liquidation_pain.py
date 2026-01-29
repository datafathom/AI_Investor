import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LiquidationPainCalculator:
    """Calculates the 'true cost' of forced liquidation."""
    
    def calculate_pain(self, amount: float, cost_basis: float, tax_rate: float, spread_bps: int = 50) -> Dict[str, Any]:
        """
        Pain components:
        1. Capital Gains Tax
        2. Bid/Ask Spread (Timing)
        3. Commission
        """
        gain = max(0, amount - cost_basis)
        tax_hit = gain * tax_rate
        
        # Spread cost (default 0.5%)
        spread_cost = amount * (spread_bps / 10000)
        
        total_lost = tax_hit + spread_cost
        efficiency = (amount - total_lost) / amount
        
        logger.info(f"TAX_LOG: Liquidation Pain: ${total_lost:,.2f} on ${amount:,.2f} sale ({efficiency*100:.1f}% efficiency)")
        
        return {
            "gross_amount": amount,
            "tax_hit": round(tax_hit, 2),
            "spread_latency_cost": round(spread_cost, 2),
            "net_proceeds": round(amount - total_lost, 2),
            "pain_index": round(1 - efficiency, 4) # 0 to 1
        }
