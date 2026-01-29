import logging
from decimal import Decimal
from typing import Dict, Any

logger = logging.getLogger(__name__)

class OperationsOutsourceCalculator:
    """
    Evaluates 'Build vs. Buy' for Family Office back-office functions.
    Compares hiring internal staff (Controller, Accountant) vs. outsourced firms.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(OperationsOutsourceCalculator, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info("OperationsOutsourceCalculator initialized")

    def evaluate_hiring_choice(self, function_name: str, transaction_vol: int) -> Dict[str, Any]:
        """
        Policy: Hiring is usually better for core alpha; outsourcing for fixed complexity.
        """
        # Internal hiring costs: Salary, Benefits (+30%), Seats, Tech
        internal_salaries = {"CONTROLLER": 180000, "ACCOUNTANT": 90000, "OPS_ANALYST": 110000}
        base = Decimal(str(internal_salaries.get(function_name.upper(), 100000)))
        internal_est = base * Decimal('1.4') # Add benefits/overhead
        
        # Outsourcing: tiered by volume
        vendor_est = Decimal(str(transaction_vol)) * Decimal('50.00') + Decimal('20000')
        
        logger.info(f"OPS_LOG: Evaluating {function_name}. Internal: ${internal_est:,.2f} vs External: ${vendor_est:,.2f}")
        
        return {
            "function": function_name,
            "estimated_internal_cost": round(internal_est, 2),
            "estimated_vendor_cost": round(vendor_est, 2),
            "recommendation": "HIRE_INTERNAL" if internal_est < vendor_est else "OUTSOURCE_FUNCTION"
        }
