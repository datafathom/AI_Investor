import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SWRAdjuster:
    """
    Adjusts the standard 4% Rule for UHNW realities.
    Considers:
    1. CLEW Inflation (High personal cost growth)
    2. Long Life Expectancy (Top 0.1% health outcomes)
    3. Generational Dilution (Wealth split among heirs)
    """
    
    def calculate_safe_withdrawal(self, 
                                 net_worth: Decimal, 
                                 num_heirs: int, 
                                 life_expectancy_offset: int = 15) -> Dict[str, Any]:
        """
        Standard Saftey = 4.0%
        UHNW Adjusted = Safety - (CLEW_Premium) - (Longevity_Penalty)
        """
        base_rate = Decimal("0.04")
        clew_premium = Decimal("0.01") # CLEW is usually ~1% higher than CPI
        longevity_penalty = Decimal("0.005") # To cover 15+ extra years
        
        adjusted_rate = base_rate - clew_premium - longevity_penalty
        
        # Generational Dilution Factor
        # Per-capita wealth reduces as family expands
        dilution_factor = Decimal("1.0") / Decimal(str(max(1, num_heirs)))
        
        safe_annual_draw = net_worth * adjusted_rate
        per_heir_draw = (net_worth * dilution_factor) * adjusted_rate
        
        logger.info(f"SWR: Adjusted Rate {adjusted_rate:.2%}. Safe annual draw: ${safe_annual_draw:,.2f}")
        
        return {
            "base_rate_pct": float(base_rate * 100),
            "adjusted_rate_pct": float(adjusted_rate * 100),
            "safe_annual_withdrawal": round(safe_annual_draw, 2),
            "per_heir_safe_withdrawal": round(per_heir_draw, 2),
            "dilution_warning": num_heirs > 2
        }
