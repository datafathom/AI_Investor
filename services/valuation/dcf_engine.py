import logging
from typing import Dict, Any
from services.ingestion.sec_scraper import SECScraper

logger = logging.getLogger(__name__)

class DCFEngine:
    """
    Calculates Intrinsic Value using Discounted Cash Flow (DCF).
    Powered by live financial data.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DCFEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.scraper = SECScraper()
        logger.info("DCFEngine initialized")

    def calculate_intrinsic_value(self, ticker: str) -> Dict[str, float]:
        """
        Orchestrates Data Fetch -> DCF Calculation.
        Returns valuation metrics.
        """
        logger.info(f"DCF Engine: Auto-calculating fair value for {ticker}...")
        
        # 1. Fetch Data
        try:
            fin_data = self.scraper.get_financials(ticker)
        except Exception as e:
            logger.error(f"Could not fetch data for {ticker}: {e}")
            return {"fair_value": 0.0, "current_price": 0.0, "margin_of_safety_pct": 0.0}

        free_cash_flow = fin_data.get("free_cash_flow", 0)
        growth_rate = fin_data.get("growth_rate_5y", 0.05)
        wacc = fin_data.get("wacc", 0.09)
        shares_outstanding = fin_data.get("shares_outstanding", 1)
        current_price = fin_data.get("current_price", 0)
        
        # 2. Perform Calculation
        fair_value = self._compute_dcf(
            free_cash_flow, 
            growth_rate, 
            wacc, 
            shares_outstanding=shares_outstanding
        )
        
        # 3. Compute Margin of Safety
        margin_pct = 0.0
        if current_price > 0:
            margin_pct = ((fair_value - current_price) / current_price) * 100
        
        return {
            "ticker": ticker,
            "current_price": current_price,
            "fair_value": fair_value,
            "margin_of_safety_pct": margin_pct
        }

    def _compute_dcf(
        self, 
        free_cash_flow: float, 
        growth_rate: float, 
        wacc: float, 
        terminal_growth: float = 0.02,
        projection_years: int = 5,
        shares_outstanding: int = 1
    ) -> float:
        """
        Internal 2-Stage DCF Math.
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
        
        if shares_outstanding <= 0:
            return 0.0
            
        fair_value_per_share = total_enterprise_value / shares_outstanding
        return round(fair_value_per_share, 2)
