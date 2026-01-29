import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class StockLendingService:
    """
    Models borrowing capacity against concentrated stock positions.
    Analyzes LTV (Loan-to-Value) vs volatility.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StockLendingService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("StockLendingService initialized")

    def calculate_borrowing_power(self, symbol: str, position_value: Decimal, volatility_pct: float) -> Dict[str, Any]:
        """
        Policy: Capacity restricted by volatility.
        - Vol < 20%: 50% LTV
        - Vol < 40%: 35% LTV
        - Vol > 40%: 20% LTV
        """
        if volatility_pct < 20.0:
            ltv = Decimal('0.50')
        elif volatility_pct < 40.0:
            ltv = Decimal('0.35')
        else:
            ltv = Decimal('0.20')
            
        capacity = position_value * ltv
        
        logger.info(f"LENDING_LOG: {symbol} borrowing capacity: ${capacity:,.2f} ({ltv:.0%} LTV)")
        
        return {
            "symbol": symbol,
            "max_ltv": ltv,
            "available_liquidity": round(capacity, 2),
            "vol_risk_bucket": "LOW" if volatility_pct < 25 else "HIGH"
        }

    def analyze_borrow_vs_sell(self, position_value: Decimal, cost_basis: Decimal, cap_gains_rate: Decimal, loan_interest_rate: Decimal) -> Dict[str, Any]:
        """
        Decision Logic: If Cost of Interest < Immediate Tax Hit on Sale.
        """
        capital_gains_tax = (position_value - cost_basis) * cap_gains_rate
        annual_interest = position_value * Decimal('0.50') * loan_interest_rate # Assuming 50% LTV loan
        
        # Simple break-even: How many years of interest equals one-time tax hit
        breakeven_years = capital_gains_tax / annual_interest if annual_interest > 0 else 99
        
        return {
            "one_time_tax_cost": round(capital_gains_tax, 2),
            "annual_loan_interest": round(annual_interest, 2),
            "breakeven_years": round(float(breakeven_years), 2),
            "recommendation": "BORROW" if breakeven_years > 3.0 else "SELL"
        }
