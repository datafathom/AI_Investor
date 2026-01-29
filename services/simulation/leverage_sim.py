import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LeverageSimulator:
    """Simulates returns with leverage (the double-edged sword)."""
    
    def simulate_outcome(self, principal: float, leverage_ratio: float, gross_return: float) -> Dict[str, Any]:
        """
        Policy: Multiplies gains/losses by the ratio.
        """
        net_return = gross_return * leverage_ratio
        ending_equity = principal * (1 + net_return)
        
        logger.info(f"SIM_LOG: {leverage_ratio}x leverage: Gross {gross_return:+.1%} -> Net {net_return:+.1%}. Equity: ${ending_equity:,.2f}")
        
        return {
            "net_return_pct": round(float(net_return), 4),
            "ending_equity": round(float(ending_equity), 2),
            "is_wiped_out": ending_equity <= 0
        }
