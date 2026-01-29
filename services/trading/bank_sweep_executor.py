import logging
from decimal import Decimal
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class BankSweepExecutor:
    """
    Automatically manages overnight liquidity to capture higher yields.
    Sweeps stagnant broker cash (0.01%) into Treasury Money Market ETFs (SGOV, BIL).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BankSweepExecutor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("BankSweepExecutor initialized")

    def analyze_cash_drag(self, cash_balance: Decimal, broker_yield: Decimal, market_yield: Decimal) -> Dict[str, Any]:
        """
        Policy: Minimize 'Lazy Cash'.
        """
        annual_opportunity_cost = cash_balance * (market_yield - broker_yield)
        is_sweep_profitable = annual_opportunity_cost > Decimal('250') # Minimum $250/yr to bother
        
        return {
            "current_cash": round(cash_balance, 2),
            "opportunity_cost_annual": round(annual_opportunity_cost, 2),
            "sweep_recommendation": "SWEEP_NOW" if is_sweep_profitable else "HOLD_CASH"
        }

    def generate_sweep_orders(self, cash_balance: Decimal, reserve_buffer: Decimal = Decimal('5000')) -> List[Dict[str, Any]]:
        """
        Logic: SELL cash, BUY SGOV for balance > buffer.
        """
        spendable = cash_balance - reserve_buffer
        if spendable < Decimal('1000'):
            return []
            
        logger.warning(f"TREASURY_LOG: GENERATING SWEEP ORDER: BUY SGOV ${spendable:,.2f}")
        return [{
            "symbol": "SGOV",
            "amount": round(spendable, 2),
            "action": "BUY",
            "reason": "BANK_SWEEP_OPTIMIZATION"
        }]
