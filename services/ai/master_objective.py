import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class MasterObjectiveService:
    """
    The 'Ghost in the Machine'.
    Defines the ultimate utility function the AI is trying to maximize.
    
    Objective: Maximize Return on Lifestyle (ROL)
    Constraint: Probability of Ruin < 0.01%
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MasterObjectiveService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("MasterObjectiveService initialized")

    def calculate_rol(self, current_wealth: float, annual_burn: float, happiness_factor: float) -> float:
        """
        ROL = (Sustainable Spend * Happiness) / Stress
        Simplified for now: Wealth / Burn * Happiness
        """
        if annual_burn == 0:
            return 0.0
        
        years_of_freedom = current_wealth / annual_burn
        rol_score = years_of_freedom * happiness_factor
        
        logger.info(f"MasterObjective: Calculated ROL Score: {rol_score:.2f}")
        return rol_score

    def check_survival_constraint(self, liquidity_ratio: float, value_at_risk: float) -> bool:
        """
        Ensures the portfolio survives Max Pain scenarios.
        """
        is_safe = True
        if liquidity_ratio < 0.10: # Must have 10% cash/equivalents
            is_safe = False
        if value_at_risk > 0.25: # Cannot risk losing > 25% in a month
            is_safe = False
            
        logger.info(f"MasterObjective: Survival Check -> {'PASSED' if is_safe else 'FAILED'}")
        return is_safe
