import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class SFOJustificationEngine:
    """
    Analyzes the economic feasibility of creating a Single Family Office (SFO).
    Compares external RIA AUM fees vs. internal staffing and overhead costs.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SFOJustificationEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("SFOJustificationEngine initialized")

    def run_breakeven_analysis(self, total_aum: Decimal, external_fee_bps: int = 100) -> Dict[str, Any]:
        """
        Policy: External fees are usually ~100bps (1.00%).
        SFO costs are step-functions: minimum staff usually costs $1M-$2M.
        """
        external_cost = total_aum * (Decimal(str(external_fee_bps)) / Decimal('10000'))
        
        # Heuristic SFO budget: CIO ($400k), PM ($250k), Ops ($150k), Rent/Tech ($200k)
        internal_base_cost = Decimal('1000000.00')
        
        # Scaling complexity: Add 10bps for every $500M over $1B
        overage = max(Decimal('0'), total_aum - Decimal('1000000000'))
        complexity_premium = (overage / Decimal('100000000')) * Decimal('50000') # $50k per $100M
        
        total_internal_cost = internal_base_cost + complexity_premium
        is_justified = external_cost > total_internal_cost
        
        logger.info(f"SFO_LOG: External (${external_cost:,.2f}) vs Internal (${total_internal_cost:,.2f}). "
                    f"Justified: {is_justified}")
                    
        # Log to UnifiedActivityService
        try:
            from services.unified_activity_service import UnifiedActivityService
            UnifiedActivityService.log_activity(
                "SFO_FEASIBILITY_ANALYSIS",
                f"AUM: ${total_aum:,.2f} | External Cost: ${external_cost:,.2f} | Internal: ${total_internal_cost:,.2f} | Viable: {is_justified}",
                "SYSTEM"
            )
        except ImportError:
            pass

        return {
            "external_annual_fees": float(round(external_cost, 2)),
            "internal_operating_est": float(round(total_internal_cost, 2)),
            "annual_savings": float(round(external_cost - total_internal_cost, 2)),
            "is_sfo_economically_viable": is_justified
        }

    def get_standard_budget(self) -> Dict[str, Any]:
        """
        Returns a target $1M SFO budget template for UHNW families.
        """
        return {
            "personnel": {
                "cio": 400000,
                "portfolio_manager": 250000,
                "operations_manager": 150000,
                "legal_counsel_retainer": 100000
            },
            "infrastructure": {
                "office_rent": 120000,
                "technology_bloomberg_terminal": 30000,
                "cybersecurity_audits": 50000
            },
            "total_op_ex": 1100000
        }
