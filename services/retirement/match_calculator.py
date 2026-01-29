import logging
from decimal import Decimal
from typing import Dict, Any, Optional
from models.employer_match import EmployerMatchConfig

logger = logging.getLogger(__name__)

class MatchCalculator:
    """Calculates employer matching contributions based on configuration."""
    
    def calculate_match(self, salary: float, contribution_pct: float, config: EmployerMatchConfig) -> float:
        """Calculates the dollar amount of the employer match."""
        employee_contribution = (salary * contribution_pct) / 100
        
        match_amount = 0.0
        
        if config.match_type == "DOLLAR_FOR_DOLLAR":
            # Match 100% up to max %
            matchable_pct = min(contribution_pct, config.max_match_percentage or 100.0)
            match_amount = (salary * matchable_pct) / 100
            
        elif config.match_type == "PARTIAL":
            # Match % of contribution up to max %
            matchable_pct = min(contribution_pct, config.max_match_percentage or 100.0)
            base_match = (salary * matchable_pct) / 100
            match_amount = base_match * (config.match_percentage or 0.5)
            
        elif config.match_type == "TIERED":
            # Complex tiers (e.g. 100% of first 3%, 50% of next 2%)
            t1_bound = config.tier_1_employee_pct or 0.0
            t1_match_multiplier = config.tier_1_employer_pct or 1.0
            
            t1_contrib_pct = min(contribution_pct, t1_bound)
            match_amount += (salary * t1_contrib_pct / 100) * t1_match_multiplier
            
            if contribution_pct > t1_bound:
                t2_bound = config.tier_2_employee_pct or 0.0
                t2_match_multiplier = config.tier_2_employer_pct or 0.5
                
                t2_contrib_pct = min(contribution_pct - t1_bound, t2_bound)
                match_amount += (salary * t2_contrib_pct / 100) * t2_match_multiplier

        # Apply annual cap if exists
        if config.annual_match_cap:
            match_amount = min(match_amount, config.annual_match_cap)

        logger.info(f"MATCH_LOG: Match for {config.employer_name}: ${match_amount:,.2f} on {contribution_pct}% contrib")
        return round(match_amount, 2)
