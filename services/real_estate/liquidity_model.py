import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RELiquidityModel:
    """Compares the liquidity math of REITs vs Direct property."""
    
    def calculate_exit_costs(self, asset_type: str, portfolio_value: float) -> Dict[str, Any]:
        """
        Policy: 
        - REIT: 0.05% bid-ask spread.
        - DIRECT: 6% broker commission + 2% closing costs.
        """
        if asset_type.upper() == "REIT":
            cost_pct = 0.0005
            time_to_cash_days = 2
        else:
            cost_pct = 0.08
            time_to_cash_days = 90
            
        total_cost = portfolio_value * cost_pct
        
        logger.info(f"RE_LOG: Liquidity analysis for {asset_type}: ${total_cost:,.2f} exit cost, {time_to_cash_days} days.")
        
        return {
            "exit_cost": round(total_cost, 2),
            "exit_cost_pct": cost_pct,
            "days_to_cash": time_to_cash_days
        }
