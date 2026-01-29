import logging
import math
from models.ira_optimization import IRAOptimizationProfile, AnalysisResult

logger = logging.getLogger(__name__)

class TraditionalVsRothAnalyzer:
    """Analyzes Traditional vs Roth IRA benefits."""
    
    def analyze(self, profile: IRAOptimizationProfile) -> AnalysisResult:
        """Determines which account type provides better after-tax return."""
        years = profile.retirement_age - profile.current_age
        growth_rate = 0.07 # Annual growth assumption
        
        # Scenario: $1 investment
        # Traditional: Grows tax-deferred, taxed at exit
        trad_fv = (1 * (1 + growth_rate)**years) * (1 - (profile.projected_retirement_rate or 0.25))
        
        # Roth: Taxed at entry, grows tax-free
        # To make it fair, we invest $1 (1 - current_rate) since Roth is after-tax
        roth_invested = 1 * (1 - profile.current_marginal_rate)
        roth_fv = roth_invested * (1 + growth_rate)**years
        
        breakeven = profile.current_marginal_rate
        
        rec = "ROTH" if roth_fv > trad_fv else "TRADITIONAL"
        if abs(roth_fv - trad_fv) < 0.05:
            rec = "SPLIT"

        logger.info(f"IRA_ANALYSIS: {profile.user_id} recommendation: {rec} (Roth FV: {roth_fv:.2f}, Trad FV: {trad_fv:.2f})")
        
        return AnalysisResult(
            traditional_value=round(trad_fv, 4),
            roth_value=round(roth_fv, 4),
            breakeven_rate=round(breakeven, 4),
            recommendation=rec
        )
