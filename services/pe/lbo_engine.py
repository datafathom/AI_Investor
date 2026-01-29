import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LBOEngine:
    """
    Mathematical engine for Private Equity Leveraged Buyouts.
    Projects IRR and MOIC based on deleveraging, EBITDA growth, and multiple expansion.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LBOEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("LBOEngine initialized")

    def project_deal_returns(
        self, 
        entry_ebitda: Decimal, 
        entry_multiple: Decimal, 
        equity_contribution_pct: Decimal,
        exit_multiple: Decimal,
        years: int,
        revenue_growth_pct: Decimal
    ) -> Dict[str, Any]:
        """
        Core PE Math.
        """
        enterprise_value_entry = entry_ebitda * entry_multiple
        equity_entry = enterprise_value_entry * equity_contribution_pct
        debt_entry = enterprise_value_entry - equity_entry
        
        # Compound EBITDA growth
        exit_ebitda = entry_ebitda * (Decimal('1') + revenue_growth_pct) ** years
        enterprise_value_exit = exit_ebitda * exit_multiple
        
        # Heuristic deleveraging: pay down 50% of debt
        debt_exit = debt_entry * Decimal('0.5')
        equity_exit = enterprise_value_exit - debt_exit
        
        moic = equity_exit / equity_entry
        irr = (float(moic) ** (1.0/years)) - 1
        
        logger.info(f"PE_LOG: LBO Projection: MOIC {moic:.2f}x, IRR {irr:.1%}")
        
        return {
            "entry_equity": round(equity_entry, 2),
            "exit_equity": round(equity_exit, 2),
            "moic": round(moic, 2),
            "irr_pct": round(Decimal(str(irr * 100)), 2)
        }
