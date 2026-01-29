import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OperationalCostCalculator:
    """Calculates Total Cost of Ownership (TCO) for an investment strategy."""
    
    def calculate_tco(self, strategy_name: str, management_fee: float, 
                      avg_spread: float, tax_drag: float, cash_drag: float) -> float:
        """
        TCO = Fee + Spread + TaxDrag + CashDrag
        """
        tco = management_fee + avg_spread + tax_drag + cash_drag
        
        logger.info(f"OPS_LOG: TCO for {strategy_name}: {tco:.2%} (Fee: {management_fee:.2%}, Drag: {tco - management_fee:.2%})")
        
        return round(float(tco), 4)

    def compare_to_beta(self, strategy_tco: float, beta_cost: float = 0.0003) -> float:
        """
        Returns the 'Efficiency Gap' vs a low-cost index (default 0.03%).
        """
        gap = strategy_tco - beta_cost
        return round(float(gap), 4)
