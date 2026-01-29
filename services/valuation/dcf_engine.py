import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class DCFEngineService:
    """
    Calculates Intrinsic Value using Discounted Cash Flow (DCF).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DCFEngineService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("DCFEngineService initialized")

    def calculate_intrinsic_value(
        self, 
        free_cash_flow: float, 
        growth_rate: float, 
        wacc: float, 
        terminal_growth: float = 0.02,
        projection_years: int = 5,
        shares_outstanding: int = 1
    ) -> float:
        """
        2-Stage DCF Model:
        1. Growth Phase: FCF grows at `growth_rate` for `projection_years`.
        2. Terminal Phase: Perpetuity growth at `terminal_growth`.
        Returns Fair Value per Share.
        """
        fcf = float(free_cash_flow)
        discounted_sum = 0.0
        
        # Stage 1: Projection Period
        for i in range(1, projection_years + 1):
            fcf = fcf * (1 + growth_rate)
            discounted_fcf = fcf / ((1 + wacc) ** i)
            discounted_sum += discounted_fcf
            
        # Stage 2: Terminal Value
        # TV = (Final FCF * (1 + g_term)) / (WACC - g_term)
        terminal_value = (fcf * (1 + terminal_growth)) / (wacc - terminal_growth)
        discounted_tv = terminal_value / ((1 + wacc) ** projection_years)
        
        total_enterprise_value = discounted_sum + discounted_tv
        
        # Equity Value (assuming no net debt for simplicity in this mock, or provided FCF is FCFF)
        fair_value_per_share = total_enterprise_value / shares_outstanding
        
        logger.info(f"DCF Calc: EV=${total_enterprise_value:,.0f} -> Share Price ${fair_value_per_share:.2f}")
        return round(fair_value_per_share, 2)
