import logging
from decimal import Decimal
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class StaffAttributionEngine:
    """
    Phase 163.4: Staff Productivity Metric (Portfolio Alpha).
    Attributes portfolio performance to specific investment professionals.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(StaffAttributionEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("StaffAttributionEngine initialized")

    def calculate_professional_alpha(
        self, 
        staff_id: str, 
        actual_return: Decimal, 
        benchmark_return: Decimal, 
        aum_managed: Decimal
    ) -> Dict[str, Any]:
        """
        Logic: actual - benchmark = alpha.
        """
        alpha_bps = (actual_return - benchmark_return) * Decimal('10000')
        alpha_dollars = aum_managed * (actual_return - benchmark_return)
        
        logger.info(f"PERF_LOG: Staff {staff_id} generated {alpha_bps:.2f} bps alpha on ${aum_managed:,.2f}.")
        
        return {
            "staff_id": staff_id,
            "alpha_bps": round(float(alpha_bps), 2),
            "alpha_dollar_value": float(round(alpha_dollars, 2)),
            "is_outperforming": actual_return > benchmark_return
        }

    def get_comp_benchmark(self, role: str) -> Dict[str, Any]:
        """
        Phase 163.1: Market benchmarking for FO roles.
        """
        benchmarks = {
            "CIO": {"base": (400000, 800000), "bonus_pct": 50},
            "PM": {"base": (250000, 450000), "bonus_pct": 100},
            "ANALYST": {"base": (120000, 200000), "bonus_pct": 30},
            "CONTROLLER": {"base": (150000, 250000), "bonus_pct": 20}
        }
        
        data = benchmarks.get(role.upper(), {"base": (100000, 150000), "bonus_pct": 10})
        return {
            "role": role.upper(),
            "market_base_range": data["base"],
            "target_bonus_pct": data["bonus_pct"]
        }
