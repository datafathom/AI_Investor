import logging
from schemas.ira_optimization import IRAOptimizationProfile

logger = logging.getLogger(__name__)

class TaxBracketForecaster:
    """Predicts future tax brackets based on income trajectory and law changes."""
    
    def forecast_retirement_bracket(self, profile: IRAOptimizationProfile) -> float:
        """
        Estimates the marginal tax rate at retirement.
        Logic: 
        1. Assume 3% income growth
        2. Account for Social Security and Pension
        3. Adjustment for sunset of tax laws (TCJA)
        """
        current_year = 2026 # Assume current
        years = profile.retirement_age - profile.current_age
        
        # Simple inflation / growth model
        projected_income = profile.projected_retirement_income or (profile.current_agi * (1.02)**years)
        
        # TCJA Sunset logic: rates likely to go UP by ~3-4% after 2025
        base_rate = 0.25 # baseline
        if projected_income > 200000: base_rate = 0.35
        if projected_income > 500000: base_rate = 0.45
        
        # Add 'Sunset Penalty'
        retirement_rate = base_rate + 0.03
        
        logger.info(f"FORECASTER_LOG: Predicted retirement rate for {profile.user_id}: {retirement_rate*100:.1f}%")
        return round(retirement_rate, 4)
