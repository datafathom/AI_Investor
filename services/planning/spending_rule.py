import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SpendingRule:
    """
    Phase 178.2: Inflation-Adjusted Principal Protection Gate.
    Calculates spendable income to ensure principal preservation across generations.
    """
    
    def calculate_safe_spend(
        self,
        portfolio_value: Decimal,
        nominal_return: Decimal,
        inflation_rate: Decimal
    ) -> Dict[str, Any]:
        """
        Policy: Only spend 'Real Return' (Nominal - Inflation).
        """
        real_return = nominal_return - inflation_rate
        # Floor real return at 0 to prevent principal erosion
        spendable_rate = max(Decimal('0'), real_return)
        
        # Buffer: Always keep 10% of real return as surplus
        conservative_spend_rate = spendable_rate * Decimal('0.9')
        spend_amount = portfolio_value * conservative_spend_rate
        
        logger.info(f"PLANNING_LOG: Safe spend calculated. Inflation: {inflation_rate:.1%}, Real Spend: {conservative_spend_rate:.1%}")
        
        return {
            "portfolio_value": float(portfolio_value),
            "nominal_return_pct": float(nominal_return * 100),
            "inflation_rate_pct": float(inflation_rate * 100),
            "safe_spend_rate_pct": float(conservative_spend_rate * 100),
            "max_spend_usd": round(float(spend_amount), 2),
            "status": "PRINCIPAL_PROTECTED" if real_return > 0 else "CAUTION_EROSION"
        }
