import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SCMService:
    """
    Social Class Maintenance (SCM) Service.
    Calculates ROL (Return on Lifestyle) and Class Retention metrics.
    """
    
    DEFAULT_CLEW_BASKET = {
        "education": Decimal("0.07"),  # Ivy League tuition inflation
        "travel": Decimal("0.12"),     # Luxury travel inflation
        "staff": Decimal("0.05"),      # Domestic staff wages
        "real_estate": Decimal("0.08"),# Prime property maintenance
        "security": Decimal("0.06")    # Private security costs
    }

    def calculate_clew_inflation(self, custom_weights: Dict[str, Decimal] = None) -> Decimal:
        """
        Calculates the weighted 'CLEW' inflation rate.
        CLEW = Cost of Living Extremely Well.
        """
        weights = custom_weights or self.DEFAULT_CLEW_BASKET
        # Simplified weighted average assuming equal weight for simplicity or using provided weights
        total_inflation = sum(weights.values()) / len(weights)
        
        logger.info(f"SCM: Calculated CLEW Inflation Rate: {total_inflation:.2%}")
        return total_inflation

    def project_lifestyle_burn(self, current_annual_spend: Decimal, years: int, inflation_rate: Decimal = None) -> Decimal:
        """
        Projects annual spend into the future based on lifestyle inflation.
        """
        rate = inflation_rate if inflation_rate is not None else self.calculate_clew_inflation()
        projected_spend = current_annual_spend * ((1 + rate) ** years)
        
        logger.info(f"SCM: Projected spend in {years} years: ${projected_spend:,.2f}")
        return projected_spend

    def calculate_scm_score(self, portfolio_yield_pct: Decimal, lifestyle_burn_pct: Decimal) -> Decimal:
        """
        SCM Score = (Portfolio Yield - CLEW Inflation) / Lifestyle Burn
        A score > 1.0 means the social class is expanding.
        A score < 1.0 means the social class is diluting.
        """
        clew = self.calculate_clew_inflation()
        net_alpha = portfolio_yield_pct - clew
        
        if lifestyle_burn_pct == 0:
            return Decimal("99.9") # Infinity
            
        score = net_alpha / lifestyle_burn_pct
        return round(score, 2)
